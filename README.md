# ![](./frontend/Logo_ETH_Lisbon.webp) PriceProphet ![](./frontend/Logo_ETH_Lisbon.webp)
Hackathon repository for ETH Lisbon 2022


[![pypi](https://img.shields.io/pypi/v/open_dev.svg)](https://pypi.org/project/open_dev/)
[![python](https://img.shields.io/pypi/pyversions/open_dev.svg)](https://pypi.org/project/open_dev/)
[![Build Status](https://github.com/8ball030/open_dev/actions/workflows/dev.yml/badge.svg)](https://github.com/8ball030/open_dev/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/8ball030/open_dev/branch/main/graphs/badge.svg)](https://codecov.io/github/8ball030/open_dev)

The PriceProphet is a price prediction oracle.

It is an agent system that polls cryptocurrency price data from different exchanges, annotates it, stores the annotated data on IPFS nodes, and trains a model to estimate the future price. 

![Price Prohet flow chart](./miscellaneous/priceProhetDiagram.png) 

A short video about Price Prohet can be found unter [this link](https://drive.google.com/file/d/1QyVDWoqrbO1sny8METzD5_V0kQqIvW_W/view?usp=share_link).


## PriceProphet Frontend

   The [PriceProphet](http://146.190.230.176:3000/)

## Deployments

1. Safe contract
   [0xd87bEe9DDD28773ac2EBEE70AE005F2DeB46B400](https://cronoscan.com/address/0xd87bee9ddd28773ac2ebee70ae005f2deb46b400)

2. Price Prediction Contract
   [0xACF6F2b3dfCC96DcE5BdFFC422cbDd3b179727db](https://cronoscan.com/address/0xacf6f2b3dfcc96dce5bdffc422cbdd3b179727db)

3. Price Oracle Storage Contract 
    [ready for deployment on iExec](./contracts/contracts/PriceOracleStorage.sol)
    


# Run the Application
Run the entire stack with the following commands


## Requirements

- Ensure your machine satisfies the following requirements:

    - Python `>= 3.7`
    - [Tendermint](https://docs.tendermint.com/master/introduction/install.html) `==0.34.19`
    - [IPFS node](https://docs.ipfs.io/install/command-line/#official-distributions) `==v0.6.0`
    - [Pip](https://pip.pypa.io/en/stable/installation/)
    - [Pipenv](https://pipenv.pypa.io/en/latest/install/) `>=2021.x.xx`
    - [Go](https://go.dev/doc/install) `==1.17.7`
    - [Kubectl](https://kubernetes.io/docs/tasks/tools/)
    - [Docker Engine](https://docs.docker.com/engine/install/)
    - [Docker Compose](https://docs.docker.com/compose/install/)
    - [Skaffold](https://skaffold.dev/docs/install/#standalone-binary) `>= 1.39.1`
    - [Gitleaks](https://github.com/zricethezav/gitleaks/releases/latest)

- Clone the repository:

      git clone git@github.com:8ball030/eth_lisbon.git


## Installation

make sure to cd into the agents directory first
```bash
cd agents
```

Create and launch a virtual environment
```
make new_env && pipenv shell
```

Fetch the necessary packages
```
autonomy packages sync --update-packages
```


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
    echo "    private key: $(cat ethereum_private_key.txt | tr -d \\n )" && \
    echo "    public key:  $(aea get-public-key ethereum)" && \
    echo "" && cd ../ && rm -r $1
}

create_keys my_agent
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

The IPFS hash traces here: [QmaDrsBBSbeuFjQuJ338ZvMJKxvZax3x3RT8XaDuhuq6hc](https://gateway.autonolas.tech/ipfs/QmaDrsBBSbeuFjQuJ338ZvMJKxvZax3x3RT8XaDuhuq6hc)


## An overview of the application


[![](https://mermaid.ink/img/pako:eNqNlL9ugzAQh18FeU5egKESLR06tEUQtQvLBV_AKtjUf4YoybvXhVQxBpMyWcd9389GnE-kEhRJTGoJfRPt0pKXPLKPMvuxlNTIdY41U1qCZoIn-4olfT-2zd6OZeR0XHiyAg6YYt-KY2e5dVO03T6c0_e357OHueYhyAvJJKswk6Jv8No75R1xjt8GlU5BQy7MzeXXHSThXGjQ6DAhYkE_nNQ3uCfVQuJ_-gPuKe-IP6BldL7teX9APOMd904C46_2P2rvAQG5J3DUn8jqRhcNSMbrdSLgnhsc_WC47tT-cnexQMaSxknJJFJWeQEhJhDhOaZfnyvw9Qv94Y8_4Vdal6bNwQuz75hS_h2xFDDf-w0OZ-WoUGdgFCaPTy9LATfLZMotlnA6kH_j6pTc6Q7eZ2RDOpQdMGpvy9NvuSS6wQ5LEtslBflVkpJfbB8YLYojr0ispcENMf0wCAzsKToSH6BVePkBJgbmIA?type=png)](https://mermaid.live/edit#pako:eNqNlL9ugzAQh18FeU5egKESLR06tEUQtQvLBV_AKtjUf4YoybvXhVQxBpMyWcd9389GnE-kEhRJTGoJfRPt0pKXPLKPMvuxlNTIdY41U1qCZoIn-4olfT-2zd6OZeR0XHiyAg6YYt-KY2e5dVO03T6c0_e357OHueYhyAvJJKswk6Jv8No75R1xjt8GlU5BQy7MzeXXHSThXGjQ6DAhYkE_nNQ3uCfVQuJ_-gPuKe-IP6BldL7teX9APOMd904C46_2P2rvAQG5J3DUn8jqRhcNSMbrdSLgnhsc_WC47tT-cnexQMaSxknJJFJWeQEhJhDhOaZfnyvw9Qv94Y8_4Vdal6bNwQuz75hS_h2xFDDf-w0OZ-WoUGdgFCaPTy9LATfLZMotlnA6kH_j6pTc6Q7eZ2RDOpQdMGpvy9NvuSS6wQ5LEtslBflVkpJfbB8YLYojr0ispcENMf0wCAzsKToSH6BVePkBJgbmIA)

The system starts with AgentRegistration, then transition to SafeDeployment, the PriceProphet, TransactionSubmission and finally ResetAndPause. The individual rounds of the PriceProphet are the only ones depicted here, the others are condensed for the sake of clarity.


A collection of tooling to enable open source development.

* Documentation: <https://8ball030.github.io/open_dev>
* GitHub: <https://github.com/8ball030/open_dev>
* PyPI: <https://pypi.org/project/open_dev/>
* Free software: Apache-2.0


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
