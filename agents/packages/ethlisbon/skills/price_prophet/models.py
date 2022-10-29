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

"""This module contains the shared state for the abci skill of PriceProphetAbciApp."""

from typing import Any

from packages.ethlisbon.skills.price_prophet.composition import ComposedPriceProphetAbciApp
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool, BaseParams,
)
from packages.valory.skills.abstract_round_abci.models import Requests as BaseRequests
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,
)
from packages.valory.skills.transaction_settlement_abci.models import (
    RandomnessApi as TransactionSettlementRandomness, TransactionParams,
)

class SharedState(BaseSharedState):
    """Keep the current shared state of the skill."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the state."""
        super().__init__(*args, abci_app_cls=ComposedPriceProphetAbciApp, **kwargs)

class PriceProphetParams(BaseParams):
    """Params object."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the parameters object."""
        self.price_prediction_contract_address = self._ensure(
            "price_prediction_contract_address", kwargs
        )
        super().__init__(*args, **kwargs)


class Params(PriceProphetParams, TransactionParams):
    """A model to represent params for multiple abci apps."""


RandomnessApi = TransactionSettlementRandomness
Requests = BaseRequests
BenchmarkTool = BaseBenchmarkTool
