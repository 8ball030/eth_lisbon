# PriceProphet
Hackathon repository for ETH Lisbon 2022


[![pypi](https://img.shields.io/pypi/v/open_dev.svg)](https://pypi.org/project/open_dev/)
[![python](https://img.shields.io/pypi/pyversions/open_dev.svg)](https://pypi.org/project/open_dev/)
[![Build Status](https://github.com/8ball030/open_dev/actions/workflows/dev.yml/badge.svg)](https://github.com/8ball030/open_dev/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/8ball030/open_dev/branch/main/graphs/badge.svg)](https://codecov.io/github/8ball030/open_dev)

The PriceProphet is a price prediction oracle.

It is an agent system that polls cryptocurrency price data from different exchanges, annotates it, stores the annotated data on IPFS nodes, and trains a model to estimate the future price. 


## PriceProphet Frontend

   The [PriceProphet](http://146.190.230.176:3000/)

## Deployments

1. Safe contract
   [0xd87bEe9DDD28773ac2EBEE70AE005F2DeB46B400](https://cronoscan.com/address/0xd87bee9ddd28773ac2ebee70ae005f2deb46b400)

2. Price Prediction Contract
   [0xACF6F2b3dfCC96DcE5BdFFC422cbDd3b179727db](https://cronoscan.com/address/0xacf6f2b3dfcc96dce5bdffc422cbdd3b179727db)


# Run the Application
Run the entire stack with the following commands


## The agent operator

In order to run the agent system, one must set a private key for the agent, e.g.

```bash
export RUNNER_KEY=0xa39adb18c75cfca9e6e5d7f32bfd1a80676d5440d5b8ef9cf11c818b8167a003
```

To facilitate the process of getting started, one may use the following code snippet to create a keypair

```bash
function create_keys {
    aea create $1 --local
    cd $1
    aea generate-key ethereum && \
    aea add-key ethereum && \
    echo "" && echo "created: $1"
    echo "    private key: $(cat cosmos_private_key.txt | tr -d \\n )" && \
    echo "    public key:  $(aea get-public-key cosmos)" && \
    echo "" && cd ../ && rm -r $1
}

setup my_agent
```

the output should look as follows:

```bash
created: my_agent
    private key: 401e39213ca22d324c3259b51585571948139cdd0ba0e3d34d93b61bbea292b5
    public key:  025d1076b5571ac239bd269bcd5a6a004d035c17ad8b3de899fa6144e8f57d3310
```

### Output

The output on the terminal will contain, among other logs such as those of the Tendermint process, those of the agent reporting on its current progress and state:

```
Starting AEA 'agent' in 'async' mode...
...
[agent] local height == remote == 2; Sync complete...
...
[agent] Retrieving data for BTC/USD
...
[agent] Data retrieved:
...
[agent] Annotated data:
...
[agent] Annotated data written to: price_prophet.csv
...
[agent] Storing: price_prophet.csv
...
[agent] IPFS hash data: QmaDrsBBSbeuFjQuJ338ZvMJKxvZax3x3RT8XaDuhuq6hc
...
[agent] Validated the data: QmaDrsBBSbeuFjQuJ338ZvMJKxvZax3x3RT8XaDuhuq6hc
...
[agent] Training, current time:
...
[agent] Successfully DONE training at:
...
[agent] Sharing weights:
...
[agent] Model validation:
...
[agent] Price predictions:
...
```



## An overview of the application


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



A collection of tooling to enable open source development.

* Documentation: <https://8ball030.github.io/open_dev>
* GitHub: <https://github.com/8ball030/open_dev>
* PyPI: <https://pypi.org/project/open_dev/>
* Free software: Apache-2.0


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
