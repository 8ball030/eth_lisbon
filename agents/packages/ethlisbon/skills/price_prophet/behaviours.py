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

import json
import logging
from typing import Generator, List, Set, Type, cast

import requests
import pandas as pd

try:
    import talib
    from talib import abstract
except ImportError:
    raise ImportError("install TA-Lib using the instruction here: https://cloudstrata.io/install-ta-lib-on-ubuntu-server/")

from aea.common import JSONLike
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
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


# __repr__ display them as dicts, all are in fact classes
TA_INDICATORS = list(map(abstract.Function, talib.get_functions()))
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute TA indicators"""
    data = [df]
    for f in TA_INDICATORS:
        name = f._Function__name.decode('utf-8')
        try:
            transformed = f(df)
            if len(transformed.shape) == 1:
                transformed = transformed.to_frame(name=name)
            data.append(transformed)
        except Exception:
            logging.warning(f"could not apply {name}")
    return pd.concat(data, axis=1)


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


class AnnotateDataBehaviour(PriceProphetBaseBehaviour):
    """AnnotateDataBehaviour"""

    behaviour_id: str = "annotate_data"
    matching_round: Type[AbstractRound] = AnnotateDataRound

    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            most_voted: JSONLike = self.synchronized_data.db.get_strict(StoreDataRound.selection_key)
            content = compute_indicators(pd.read_json(most_voted)).to_json()
            sender = self.context.agent_address
            payload = AnnotateDataPayload(sender=sender, content=content)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ModelValidationBehaviour(PriceProphetBaseBehaviour):
    """ModelValidationBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "model_validation"
    matching_round: Type[AbstractRound] = ModelValidationRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ModelValidationPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PredictionBehaviour(PriceProphetBaseBehaviour):
    """PredictionBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "prediction"
    matching_round: Type[AbstractRound] = PredictionRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PredictionPayload(sender=sender, content=...)

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
            content = pd.DataFrame(data, columns=COLUMNS).to_json()
            sender = self.context.agent_address
            payload = RequestDataPayload(sender=sender, content=content)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class StoreDataBehaviour(PriceProphetBaseBehaviour):
    """StoreDataBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "store_data"
    matching_round: Type[AbstractRound] = StoreDataRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = StoreDataPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class TrainModelBehaviour(PriceProphetBaseBehaviour):
    """TrainModelBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "train_model"
    matching_round: Type[AbstractRound] = TrainModelRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = TrainModelPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class TransactionBehaviour(PriceProphetBaseBehaviour):
    """TransactionBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "transaction"
    matching_round: Type[AbstractRound] = TransactionRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = TransactionPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ValidateDataBehaviour(PriceProphetBaseBehaviour):
    """ValidateDataBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "validate_data"
    matching_round: Type[AbstractRound] = ValidateDataRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ValidateDataPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class WeightSharingBehaviour(PriceProphetBaseBehaviour):
    """WeightSharingBehaviour"""

    # TODO: set the following class attributes
    state_id: str
    behaviour_id: str = "weight_sharing"
    matching_round: Type[AbstractRound] = WeightSharingRound

    # TODO: implement logic required to set payload content (e.g. synchronized_data)
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = WeightSharingPayload(sender=sender, content=...)

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
