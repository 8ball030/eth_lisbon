export AUTHOR=ethlisbon
export SERVICE=price_prophet

cd agents
autonomy hash all && autonomy packages lock && autonomy push-all --remote
autonomy fetch $AUTHOR/$SERVICE --local --service && \
    cd $SERVICE && \
    autonomy build-image

autonomy deploy build ../generated_keys.json --force --password  password  --aev  && cd abci_build && docker-compose up


