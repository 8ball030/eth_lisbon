# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of PriceProphetAbciApp."""

import time
import json
from typing import Generator, List, Set, Type, cast, Optional, Any
from pathlib import Path
from collections import Counter

import requests
from scipy.stats import linregress
import pandas as pd
import ipfshttpclient
from joblib import dump, load
from packages.ethlisbon.contracts.price_prediction.contract import PricePredictionContract
from packages.valory.contracts.gnosis_safe.contract import GnosisSafeContract
from packages.valory.protocols.contract_api import ContractApiMessage
from packages.valory.skills.transaction_settlement_abci.payload_tools import hash_payload_to_hex
from packages.ethlisbon.skills.price_prophet.composition import ComposedPriceProphetAbciApp
from packages.valory.skills.registration_abci.behaviours import AgentRegistrationRoundBehaviour, \
    RegistrationStartupBehaviour
from packages.valory.skills.safe_deployment_abci.behaviours import SafeDeploymentRoundBehaviour
from packages.valory.skills.transaction_settlement_abci.behaviours import TransactionSettlementRoundBehaviour
from aea.common import JSONLike
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.ethlisbon.skills.price_prophet.ml_tools import (
    COLUMNS,
    STEPS_INTO_THE_FUTURE,
    forecaster,
    compute_indicators,
    train_model, Y_TARGET
)
from packages.ethlisbon.skills.price_prophet.models import Params
from packages.ethlisbon.skills.price_prophet.rounds import (
    SynchronizedData,
    PriceProphetAbciApp,
    AnnotateDataRound,
    ModelValidationRound,
    PredictionRound,
    RequestDataRound,
    StoreDataRound,
    TrainModelRound,
    TransactionRound,
    ValidateDataRound,
    WeightSharingRound,
)
from packages.ethlisbon.skills.price_prophet.rounds import (
    AnnotateDataPayload,
    ModelValidationPayload,
    PredictionPayload,
    RequestDataPayload,
    StoreDataPayload,
    TrainModelPayload,
    TransactionPayload,
    ValidateDataPayload,
    WeightSharingPayload,
)

SAFE_GAS = 0
ETH_VALUE = 0
DEFAULT_REGISTRY = "/dns/registry.autonolas.tech/tcp/443/https"


class PriceProphetBaseBehaviour(BaseBehaviour):
    """Base behaviour for the common apps' skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)

    def get_strict(self, key: str) -> Any:
        """Get strict from SynchronizedData"""
        return self.synchronized_data.db.get_strict(key)

    @property
    def file_path_for_storage(self):
        """File path for storage"""
        file_path = Path("price_prophet.csv")
        return file_path


class AnnotateDataBehaviour(PriceProphetBaseBehaviour):
    """AnnotateDataBehaviour"""

    behaviour_id: str = "annotate_data"
    matching_round: Type[AbstractRound] = AnnotateDataRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            most_voted: JSONLike = self.get_strict(RequestDataRound.selection_key)
            df = compute_indicators(pd.read_json(most_voted))
            cols = [k for k, v in Counter(df.columns).items() if v == 1]
            content = df[cols].to_json()  # must remove duplicate column names
            sender = self.context.agent_address
            payload = AnnotateDataPayload(sender=sender, content=hash(content))
            self.context.logger.info(f"Annotated data: {content}")
            self.file_path_for_storage.write_text(content)
            self.context.logger.info(f"Annotated data written to: {self.file_path_for_storage}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ModelValidationBehaviour(PriceProphetBaseBehaviour):
    """ModelValidationBehaviour"""

    behaviour_id: str = "model_validation"
    matching_round: Type[AbstractRound] = ModelValidationRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            # ['lags', 'params', 'mean_squared_error', 'max_depth', 'n_estimators']
            most_voted: JSONLike = self.get_strict(WeightSharingRound.selection_key)
            results_grid = pd.read_json(most_voted)
            results_grid.sort_values(by="mean_squared_error", inplace=True)
            forecaster.set_params(**results_grid.params[0])
            forecaster.set_lags(results_grid.lags[0])
            sender = self.context.agent_address
            payload = ModelValidationPayload(sender=sender, content=True)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PredictionBehaviour(PriceProphetBaseBehaviour):
    """PredictionBehaviour"""

    behaviour_id: str = "prediction"
    matching_round: Type[AbstractRound] = PredictionRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            forecaster = load("model_file")
            predictions = forecaster.predict(steps=STEPS_INTO_THE_FUTURE)
            sender, content = self.context.agent_address, predictions.to_json()
            payload = PredictionPayload(sender=sender, content=content)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class RequestDataBehaviour(PriceProphetBaseBehaviour):
    """RequestDataBehaviour"""

    behaviour_id: str = "request_data"
    matching_round: Type[AbstractRound] = RequestDataRound

    # TODO parameterise the endpoint
    resolution = 60
    market = "BTC/USD"
    endpoint_url = f"https://ftx.com/api/markets/{market}/candles?resolution={60}"

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        self.context.logger.info(f"Retrieving data for {self.market}")
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            result = requests.get(self.endpoint_url)
            data: List[List[float]] = json.loads(result.content)["result"]
            # columns must be COLUMNS
            df = pd.DataFrame(data).rename(columns=dict(time="timestamp")).drop("startTime", axis=1)
            df["timestamp"] = df["timestamp"].astype(int) // 10 ** 9  # unix_sec
            sender, content = self.context.agent_address, df.to_json()
            payload = RequestDataPayload(sender=sender, content=content)
            self.context.logger.info(f"Data retrieved: {content}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class StoreDataBehaviour(PriceProphetBaseBehaviour):
    """StoreDataBehaviour"""

    behaviour_id: str = "store_data"
    matching_round: Type[AbstractRound] = StoreDataRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        ipfs_tool = ipfshttpclient.Client(addr=DEFAULT_REGISTRY)

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            file = str(self.file_path_for_storage)
            self.context.logger.info(f"Storing: {file}")
            res = ipfs_tool.add(file, pin=True)
            content = res.as_json()['Hash']
            sender = self.context.agent_address
            payload = StoreDataPayload(sender=sender, content=content)
            self.context.logger.info(f"IPFS hash data: {content}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class TrainModelBehaviour(PriceProphetBaseBehaviour):
    """TrainModelBehaviour"""

    behaviour_id: str = "train_model"
    matching_round: Type[AbstractRound] = TrainModelRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        # TODO: get randomness from randomness beacon
        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            random_state = self.synchronized_data.period_count
            try:
                self.context.logger.info(f"Training, current time: {time.time()}")
                results_grid = train_model(pd.read_json(self.file_path_for_storage), random_state)
                self.context.shared_state[TrainModelRound.selection_key] = results_grid
                self.context.logger.info(f"Successfully DONE training at: {time.time()}")
            except Exception as e:
                results_grid = None
                self.context.logger.error(f"Failed to complete training forecaster: {e}")

            sender = self.context.agent_address
            payload = TrainModelPayload(sender=sender, content=len(results_grid) > 0)
            self.context.logger.info(f"Model trained: {len(results_grid) > 0}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class TransactionBehaviour(PriceProphetBaseBehaviour):
    """TransactionBehaviour"""

    state_id: str = "transaction"
    behaviour_id: str = "transaction_behaviour"
    matching_round: Type[AbstractRound] = TransactionRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            payload_data = yield from self.get_tx()
            sender = self.context.agent_address
            payload = TransactionPayload(sender=sender, content=payload_data)
            self.context.logger.info(f"Transaction: {payload_data}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def get_tx(self) -> Generator[None, None, str]:
        """Prepares the updatePriceData tx."""
        update_weights_gradually_tx_data = (
            yield from self._get_update_price_data_tx()
        )
        if update_weights_gradually_tx_data is None:
            return ""

        safe_tx_hash = yield from self._get_safe_tx_hash(
            update_weights_gradually_tx_data
        )
        if safe_tx_hash is None:
            return ""

        payload_data = hash_payload_to_hex(
            safe_tx_hash=safe_tx_hash,
            ether_value=ETH_VALUE,
            safe_tx_gas=SAFE_GAS,
            to_address=self.params.price_prediction_contract_address,
            data=update_weights_gradually_tx_data,
        )
        return payload_data

    def _get_safe_tx_hash(self, data: bytes) -> Generator[None, None, Optional[str]]:
        """Prepares and returns the safe tx hash."""
        response = yield from self.get_contract_api_response(
            performative=ContractApiMessage.Performative.GET_STATE,  # type: ignore
            contract_address=self.synchronized_data.db.get("safe_contract_address"),
            contract_id=str(GnosisSafeContract.contract_id),
            contract_callable="get_raw_safe_transaction_hash",
            to_address=self.params.price_prediction_contract_address,
            value=ETH_VALUE,
            data=data,
            safe_tx_gas=SAFE_GAS,
        )
        if response.performative != ContractApiMessage.Performative.STATE:
            self.context.logger.error(
                f"Couldn't get safe hash. "
                f"Expected response performative {ContractApiMessage.Performative.STATE.value}, "  # type: ignore
                f"received {response.performative.value}."
            )
            return None

        tx_hash = cast(str, response.state.body["tx_hash"])[2:]
        return tx_hash

    def _get_update_price_data_tx(
        self,
    ) -> Generator[None, None, Optional[bytes]]:
        """Get the tx data."""

        most_voted: JSONLike = self.get_strict(PredictionRound.selection_key)
        predictions: pd.Series = pd.read_json(most_voted)

        rate_of_change = linregress(predictions.reset_index()).slope
        price = predictions[-1]
        response = yield from self.get_contract_api_response(
            performative=ContractApiMessage.Performative.GET_STATE,  # type: ignore
            contract_id=str(PricePredictionContract.contract_id),
            contract_callable="encode_update_price_tx",
            contract_address=self.params.price_prediction_contract_address,
            rate_of_change=rate_of_change,
            price=price,
        )

        if response.performative != ContractApiMessage.Performative.STATE:
            self.context.logger.error(
                f"Couldn't get tx data for updatePriceData(). "
                f"Expected response performative {ContractApiMessage.Performative.STATE.value}, "  # type: ignore
                f"received {response.performative.value}."
            )
            return None

        data_str = cast(str, response.state.body["data"])[2:]
        data = bytes.fromhex(data_str)
        return data


class ValidateDataBehaviour(PriceProphetBaseBehaviour):
    """ValidateDataBehaviour"""

    behaviour_id: str = "validate_data"
    matching_round: Type[AbstractRound] = ValidateDataRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            most_voted = self.get_strict(StoreDataRound.selection_key)
            sender = self.context.agent_address
            payload = ValidateDataPayload(sender=sender, content=True)
            self.context.logger.info(f"Validated the data : {most_voted}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class WeightSharingBehaviour(PriceProphetBaseBehaviour):
    """WeightSharingBehaviour"""

    behaviour_id: str = "weight_sharing"
    matching_round: Type[AbstractRound] = WeightSharingRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            # results_grid must exist from previous round else there is a logic error in the FSM
            results_grid: pd.DataFrame = self.context.shared_state[TrainModelRound.selection_key]
            sender, content = self.context.agent_address, results_grid.to_json()
            payload = WeightSharingPayload(sender=sender, content=content)
            self.context.logger.info(f"Sharing weights: {content}")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PriceProphetRoundBehaviour(AbstractRoundBehaviour):
    """PriceProphetRoundBehaviour"""

    initial_behaviour_cls = RequestDataBehaviour
    abci_app_cls = PriceProphetAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        AnnotateDataBehaviour,
        ModelValidationBehaviour,
        PredictionBehaviour,
        RequestDataBehaviour,
        StoreDataBehaviour,
        TrainModelBehaviour,
        TransactionBehaviour,
        ValidateDataBehaviour,
        WeightSharingBehaviour
    ]


class ComposedPriceProphetRoundBehaviour(AbstractRoundBehaviour):
    """This class contains the composed price prophet behaviour."""
    initial_behaviour_cls = RegistrationStartupBehaviour
    abci_app_cls = ComposedPriceProphetAbciApp
    behaviours: Set[Type[BaseBehaviour]] = [
        *AgentRegistrationRoundBehaviour.behaviours,
        *SafeDeploymentRoundBehaviour.behaviours,
        *TransactionSettlementRoundBehaviour.behaviours,
        *PriceProphetRoundBehaviour.behaviours,
    ]
