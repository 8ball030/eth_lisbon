#! /bin/bash
sudo rm -r ~/.tendermint/data/ && sudo tendermint init validator && sudo cp -r /root/.tendermint ~/  && sudo chown -R $(whoami):$(whoami) ~/.tendermint

cd agents
sudo rm -r agent
rm -rf agent/ && autonomy hash all && autonomy packages lock && \
aea -s fetch ethlisbon/price_prophet:0.1.0 --local --alias agent

cd agent || (echo "agent failed to fetch" && exit 1 )

echo -n $RUNNER_KEY > ethereum_private_key.txt
aea add-key ethereum && \

aea install && \
aea -s run --aev
