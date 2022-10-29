# eth_lisbon
Hackathon repository for ETH Lisbon 2022


To install TA-lib, follow the instructions here:
https://cloudstrata.io/install-ta-lib-on-ubuntu-server/


<figure markdown>
<div class="mermaid">
stateDiagram-v2
    RequestDataRound --> ValidateDataRound: <center>DONE</center>
    RequestDataRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    ValidateDataRound --> StoreDataRound: <center>DONE</center>
    ValidateDataRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    StoreDataRound --> AnnotateDataRound: <center>DONE</center>
    StoreDataRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    AnnotateDataRound --> TrainModelRound: <center>DONE</center>
    AnnotateDataRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    TrainModelRound --> WeightSharingRound: <center>DONE</center>
    TrainModelRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    WeightSharingRound --> ModelValidationRound: <center>DONE</center>
    WeightSharingRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    ModelValidationRound --> PredictionRound: <center>DONE</center>
    ModelValidationRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    PredictionRound --> TransactionRound: <center>DONE</center>
    PredictionRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
    TransactionRound --> FinishedTransactionRound: <center>DONE</center>
    TransactionRound --> RequestDataRound: <center>NO_MAJORITY<br />ROUND_TIMEOUT</center>
</div>
<figcaption>PriceProphetAbciApp</figcaption>
</figure>
