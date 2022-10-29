import { get } from 'lodash';
import Home from 'components/Home';

export async function getStaticProps() {
  // const URL = https://futures.kraken.com/api/charts/v1/mark/PI_XBTUSD/1m?from=1625405796&to=1625492256
  // const response = await fetch(URL);
  // console.log(response);
  // const values = await response.json();
  // console.log(values);

  const response = await fetch(
    'https://ftx.com/api/markets/BTC/USD/candles?resolution=60',
    {
      mode: 'no-cors',
    },
  );
  const values = await response.json();
  const ftxData = get(values, 'result') || [];

  return {
    props: { ftxData },
  };
}

export default Home;
