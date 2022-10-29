# Price Prophet


[![pypi](https://img.shields.io/pypi/v/open_dev.svg)](https://pypi.org/project/open_dev/)
[![python](https://img.shields.io/pypi/pyversions/open_dev.svg)](https://pypi.org/project/open_dev/)
[![Build Status](https://github.com/8ball030/open_dev/actions/workflows/dev.yml/badge.svg)](https://github.com/8ball030/open_dev/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/8ball030/open_dev/branch/main/graphs/badge.svg)](https://codecov.io/github/8ball030/open_dev)





Install Dependencies.

(Poetry) Is used to managed the dependencies. (https://python-poetry.org/docs/#installation)
# osx / linux / bashonwindows install instructions
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
```
# windows install instructions
```
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python `
```

```bash
make install

```

# Generate keys

```
cd agents
pipenv shell
python scripts/generate_keys.py
```


# Run the Application
Run the entire stack with the following command;



```bash
docker-compose up
```

## The agent operator

Create agent keys;

```
cd agents
python scripts/generate_keys.py --password password

```
### Manual mode
```bash
export AUTHOR=ethlisbon
export SERVICE=price_prophet
cd agents
pipenv shell

# push the service
autonomy push-all
autonomy fetch $AUTHOR/$SERVICE --local --service
cd $SERVICE

autonomy build-image
autonomy deploy build ../generated_keys.json --force --password  password  --aev  \ 
    && cd abci_build \
    && docker-compose up


```

### DEV mode
```bash
export SERVICE=ethlisbon/ethlisbon
bash scripts/run_agent_service.sh

```


## The front end
```
cd frontend && npm start

```


A collection of tooling to enable open source development.


* Documentation: <https://8ball030.github.io/open_dev>
* GitHub: <https://github.com/8ball030/open_dev>
* PyPI: <https://pypi.org/project/open_dev/>
* Free software: Apache-2.0


## Features



## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
