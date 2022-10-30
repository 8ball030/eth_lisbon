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

"""This module contains the transaction payloads of the PriceProphetAbciApp."""

from abc import ABC
from enum import Enum
from typing import Any, Dict, Hashable, Optional

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


class TransactionType(Enum):
    """Enumeration of transaction types."""

    # TODO: define transaction types: e.g. TX_HASH: "tx_hash"
    ANNOTATE_DATA = "annotate_data"
    MODEL_VALIDATION = "model_validation"
    PREDICTION = "prediction"
    REQUEST_DATA = "request_data"
    STORE_DATA = "store_data"
    TRAIN_MODEL = "train_model"
    TRANSACTION = "transaction"
    VALIDATE_DATA = "validate_data"
    WEIGHT_SHARING = "weight_sharing"

    def __str__(self) -> str:
        """Get the string value of the transaction type."""
        return self.value


class BasePriceProphetPayload(BaseTxPayload, ABC):
    """Base payload for PriceProphetAbciApp."""

    def __init__(self, sender: str, content: Hashable, **kwargs: Any) -> None:
        """Initialize a transaction payload."""

        super().__init__(sender, **kwargs)
        setattr(self, f"_{self.transaction_type}", content)
        p = property(lambda s: getattr(self, f"_{self.transaction_type}"))
        setattr(self.__class__, f"{self.transaction_type}", p)

    @property
    def data(self) -> Dict[str, Hashable]:
        """Get the data."""
        return dict(content=getattr(self, str(self.transaction_type)))


class AnnotateDataPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the AnnotateDataRound."""

    transaction_type = TransactionType.ANNOTATE_DATA


class ModelValidationPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the ModelValidationRound."""

    transaction_type = TransactionType.MODEL_VALIDATION


class PredictionPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the PredictionRound."""

    transaction_type = TransactionType.PREDICTION


class RequestDataPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the RequestDataRound."""

    transaction_type = TransactionType.REQUEST_DATA


class StoreDataPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the StoreDataRound."""

    transaction_type = TransactionType.STORE_DATA


class TrainModelPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the TrainModelRound."""

    transaction_type = TransactionType.TRAIN_MODEL


class TransactionPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the TransactionRound."""

    transaction_type = TransactionType.TRANSACTION


class ValidateDataPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the ValidateDataRound."""

    transaction_type = TransactionType.VALIDATE_DATA

    @property
    def vote(self):
        return self.data.get("content")

class WeightSharingPayload(BasePriceProphetPayload):
    """Represent a transaction payload for the WeightSharingRound."""

    transaction_type = TransactionType.WEIGHT_SHARING

