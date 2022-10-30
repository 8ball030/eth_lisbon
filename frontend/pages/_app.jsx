/* eslint-disable jest/require-hook */
import App from 'next/app';
import Head from 'next/head';
import { createWrapper } from 'next-redux-wrapper';
import PropTypes from 'prop-types';

import { Web3ReactProvider } from '@web3-react/core';
import Web3 from 'web3';

import GlobalStyle from 'components/GlobalStyles';
import { DataProvider } from 'common-util/context';
import Layout from 'components/Layout';
import initStore from '../store';

require('../styles/antd.less');

const getLibrary = (p) => new Web3(p);

class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    const pageProps = Component.getInitialProps
      ? await Component.getInitialProps(ctx)
      : {};

    return { pageProps };
  }

  render() {
    const { Component, pageProps } = this.props;

    return (
      <>
        <GlobalStyle />
        <Head>
          <title>Lisbon Hackathon</title>
          <meta name="title" content="Lisbon Hackathon" />
        </Head>
        <DataProvider>
          <Web3ReactProvider getLibrary={getLibrary}>
            <Layout>
              <Component {...pageProps} />
            </Layout>
          </Web3ReactProvider>
        </DataProvider>
      </>
    );
  }
}

MyApp.propTypes = {
  Component: PropTypes.oneOfType([PropTypes.func, PropTypes.shape({})])
    .isRequired,
  pageProps: PropTypes.shape({}).isRequired,
};

const wrapper = createWrapper(initStore);
export default wrapper.withRedux(MyApp);
