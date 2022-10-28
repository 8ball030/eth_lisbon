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

"""This package contains the rounds of PriceProphetAbciApp."""

from enum import Enum
from typing import List, Optional, Set, Tuple

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
    TransactionType
)

from packages.ethlisbon.skills.price_prophet.payloads import (
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


class Event(Enum):
    """PriceProphetAbciApp Events"""

    DONE = "done"
    ROUND_TIMEOUT = "round_timeout"
    NO_MAJORITY = "no_majority"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class AnnotateDataRound(AbstractRound):
    """AnnotateDataRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "annotate_data"
    allowed_tx_type: Optional[TransactionType] = AnnotateDataPayload.transaction_type
    payload_attribute: str = "annotate_data"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: AnnotateDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: AnnotateDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class ModelValidationRound(AbstractRound):
    """ModelValidationRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "model_validation"
    allowed_tx_type: Optional[TransactionType] = ModelValidationPayload.transaction_type
    payload_attribute: str = "model_validation"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: ModelValidationPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: ModelValidationPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PredictionRound(AbstractRound):
    """PredictionRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "prediction"
    allowed_tx_type: Optional[TransactionType] = PredictionPayload.transaction_type
    payload_attribute: str = "prediction"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: PredictionPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PredictionPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class RequestDataRound(AbstractRound):
    """RequestDataRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "request_data"
    allowed_tx_type: Optional[TransactionType] = RequestDataPayload.transaction_type
    payload_attribute: str = "request_data"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: RequestDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: RequestDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class StoreDataRound(AbstractRound):
    """StoreDataRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "store_data"
    allowed_tx_type: Optional[TransactionType] = StoreDataPayload.transaction_type
    payload_attribute: str = "store_data"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: StoreDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: StoreDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class TrainModelRound(AbstractRound):
    """TrainModelRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "train_model"
    allowed_tx_type: Optional[TransactionType] = TrainModelPayload.transaction_type
    payload_attribute: str = "train_model"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: TrainModelPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: TrainModelPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class TransactionRound(AbstractRound):
    """TransactionRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "transaction"
    allowed_tx_type: Optional[TransactionType] = TransactionPayload.transaction_type
    payload_attribute: str = "transaction"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: TransactionPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: TransactionPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class ValidateDataRound(AbstractRound):
    """ValidateDataRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "validate_data"
    allowed_tx_type: Optional[TransactionType] = ValidateDataPayload.transaction_type
    payload_attribute: str = "validate_data"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: ValidateDataPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: ValidateDataPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class WeightSharingRound(AbstractRound):
    """WeightSharingRound"""

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound, CollectSameUntilAllRound, CollectSameUntilThresholdRound, CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound
    round_id: str = "weight_sharing"
    allowed_tx_type: Optional[TransactionType] = WeightSharingPayload.transaction_type
    payload_attribute: str = "weight_sharing"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: WeightSharingPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: WeightSharingPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class FinishedTransactionRound(DegenerateRound):
    """FinishedTransactionRound"""

    round_id: str = "finished_transaction"


class PriceProphetAbciApp(AbciApp[Event]):
    """PriceProphetAbciApp"""

    initial_round_cls: AppState = RequestDataRound
    initial_states: Set[AppState] = {RequestDataRound}
    transition_function: AbciAppTransitionFunction = {
        RequestDataRound: {
            Event.DONE: ValidateDataRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        ValidateDataRound: {
            Event.DONE: StoreDataRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        StoreDataRound: {
            Event.DONE: AnnotateDataRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        AnnotateDataRound: {
            Event.DONE: TrainModelRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        TrainModelRound: {
            Event.DONE: WeightSharingRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        WeightSharingRound: {
            Event.DONE: ModelValidationRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        ModelValidationRound: {
            Event.DONE: PredictionRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        PredictionRound: {
            Event.DONE: TransactionRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        TransactionRound: {
            Event.DONE: FinishedTransactionRound,
            Event.ROUND_TIMEOUT: RequestDataRound,
            Event.NO_MAJORITY: RequestDataRound
        },
        FinishedTransactionRound: {}
    }
    final_states: Set[AppState] = {FinishedTransactionRound}
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: List[str] = []
