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

"""This package contains round behaviours of the Price Prophet."""
import packages.valory.skills.registration_abci.rounds as RegistrationAbci
import packages.valory.skills.safe_deployment_abci.rounds as SafeDeploymentAbci
import packages.valory.skills.transaction_settlement_abci.rounds as TransactionSubmissionAbci
from packages.ethlisbon.skills.price_prophet.rounds import PriceProphetAbciApp, FinishedTransactionRound
from packages.valory.skills.abstract_round_abci.abci_app_chain import (
    AbciAppTransitionMapping,
    chain,
)


abci_app_transition_mapping: AbciAppTransitionMapping = {
    RegistrationAbci.FinishedRegistrationRound: SafeDeploymentAbci.RandomnessSafeRound,
    RegistrationAbci.FinishedRegistrationFFWRound: PriceProphetAbciApp.initial_round_cls,
    FinishedTransactionRound: TransactionSubmissionAbci.TransactionSubmissionAbciApp.initial_round_cls,
    SafeDeploymentAbci.FinishedSafeRound: PriceProphetAbciApp.initial_round_cls,
    TransactionSubmissionAbci.FinishedTransactionSubmissionRound: PriceProphetAbciApp.initial_round_cls,
    TransactionSubmissionAbci.FailedRound: PriceProphetAbciApp.initial_round_cls,
}

ComposedPriceProphetAbciApp = chain(
    (
        RegistrationAbci.AgentRegistrationAbciApp,
        SafeDeploymentAbci.SafeDeploymentAbciApp,
        PriceProphetAbciApp,
        TransactionSubmissionAbci.TransactionSubmissionAbciApp,
    ),
    abci_app_transition_mapping,
)
