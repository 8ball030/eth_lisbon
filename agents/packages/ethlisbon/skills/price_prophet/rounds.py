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
    CollectSameUntilThresholdRound,
    VotingRound,
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
    NEGATIVE = "negative"
    NONE = "none"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class BaseRoundMixin:
    """BaseRoundMixin"""

    synchronized_data_class = SynchronizedData
    done_event = Event.DONE
    no_majority_event = Event.NO_MAJORITY


class AnnotateDataRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """AnnotateDataRound"""

    round_id: str = "annotate_data"
    allowed_tx_type: Optional[TransactionType] = AnnotateDataPayload.transaction_type
    payload_attribute: str = "annotate_data"
    collection_key: str  # TODO
    selection_key: str  # TODO


class ModelValidationRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """ModelValidationRound"""

    round_id: str = "model_validation"
    allowed_tx_type: Optional[TransactionType] = ModelValidationPayload.transaction_type
    payload_attribute: str = "model_validation"
    collection_key: str  # TODO
    selection_key: str  # TODO


class PredictionRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """PredictionRound"""

    round_id: str = "prediction"
    allowed_tx_type: Optional[TransactionType] = PredictionPayload.transaction_type
    payload_attribute: str = "prediction"
    collection_key: str  # TODO
    selection_key: str  # TODO


class RequestDataRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """RequestDataRound"""

    round_id: str = "request_data"
    allowed_tx_type: Optional[TransactionType] = RequestDataPayload.transaction_type
    payload_attribute: str = "request_data"
    collection_key: str  # TODO
    selection_key: str  # TODO


class StoreDataRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """StoreDataRound"""

    round_id: str = "store_data"
    allowed_tx_type: Optional[TransactionType] = StoreDataPayload.transaction_type
    payload_attribute: str = "store_data"
    collection_key: str  # TODO
    selection_key: str  # TODO


class TrainModelRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """TrainModelRound"""

    round_id: str = "train_model"
    allowed_tx_type: Optional[TransactionType] = TrainModelPayload.transaction_type
    payload_attribute: str = "train_model"
    collection_key: str  # TODO
    selection_key: str  # TODO


class TransactionRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """TransactionRound"""

    round_id: str = "transaction"
    allowed_tx_type: Optional[TransactionType] = TransactionPayload.transaction_type
    payload_attribute: str = "transaction"
    collection_key: str  # TODO
    selection_key: str  # TODO


class ValidateDataRound(VotingRound, BaseRoundMixin):
    """ValidateDataRound"""

    round_id: str = "validate_data"
    allowed_tx_type: Optional[TransactionType] = ValidateDataPayload.transaction_type
    payload_attribute: str = "validate_data"
    negative_event = Event.NEGATIVE
    none_event = Event.NONE
    collection_key: str  # TODO

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class WeightSharingRound(CollectSameUntilThresholdRound, BaseRoundMixin):
    """WeightSharingRound"""

    round_id: str = "weight_sharing"
    allowed_tx_type: Optional[TransactionType] = WeightSharingPayload.transaction_type
    payload_attribute: str = "weight_sharing"
    collection_key: str  # TODO
    selection_key: str  # TODO


class FinishedTransactionRound(DegenerateRound, BaseRoundMixin):
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
    event_to_timeout: EventToTimeout = {
        Event.ROUND_TIMEOUT: 30.0,
    }
    cross_period_persisted_keys: List[str] = []
