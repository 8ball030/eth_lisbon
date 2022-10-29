import { useEffect, useContext, useCallback } from 'react';
import { connect } from 'react-redux';
import Web3 from 'web3';
import PropTypes from 'prop-types';
import Web3Modal from 'web3modal';
import round from 'lodash/round';
import get from 'lodash/get';
import isNil from 'lodash/isNil';
import { CHAIN_ID } from 'util/constants';
import { getBalance } from 'common-util/functions';
import { Button } from 'antd';
import {
  setUserAccount as setUserAccountFn,
  setUserBalance as setUserBalanceFn,
  setChainId as setChainIdFn,
  setErrorMessage as setErrorMessageFn,
} from 'store/setup/actions';
import { DataContext } from 'common-util/context';
// import { getContract } from 'common-util/Contracts';
import { providerOptions } from './helpers';
import { Container, DetailsContainer, WalletContainer } from './styles';

/* --------------- web3Modal --------------- */
let web3Modal;
if (typeof window !== 'undefined') {
  web3Modal = new Web3Modal({
    network: 'mainnet', // optional
    cacheProvider: true,
    providerOptions, // required
  });
}

/* --------------- Login component --------------- */
const Login = ({
  account,
  balance,
  chainId,
  errorMessage,

  // functions
  setUserAccount,
  setUserBalance,
  setChainId,
  setErrorMessage,
}) => {
  const {
    provider,
    web3Provider,
    setProvider,
    setWeb3Provider,
  } = useContext(DataContext);

  const setBalance = async (accountPassed) => {
    try {
      const result = await getBalance(accountPassed, web3Provider);
      setUserBalance(result);
    } catch (error) {
      setErrorMessage(error);
    }
  };

  useEffect(async () => {
    if (account && web3Provider) {
      setBalance(account);
    }
  }, [account, web3Provider]);

  const handleLogin = useCallback(async () => {
    // This is the initial `provider` that is returned when
    // using web3Modal to connect. Can be MetaMask or WalletConnect.
    try {
      const modalProvider = await web3Modal.connect();

      // ------ setting to the window object! ------
      window.MODAL_PROVIDER = modalProvider;

      // We plug the initial `provider` and get back
      // a Web3Provider. This will add on methods and
      // event listeners such as `.on()` will be different.
      const wProvider = new Web3(modalProvider);

      const address = await wProvider.eth.getAccounts();
      const currentChainId = await wProvider.eth.getChainId();

      setUserAccount(address[0]);
      setProvider(modalProvider);
      setWeb3Provider(wProvider);
      setChainId(currentChainId || null);

      /* --------------- Contract call --------------- */
      // const contract = getContract(modalProvider, currentChainId);
      // const response = await contract.methods
      //   .claimableBalances(address[0])
      //   .call();
    } catch (error) {
      window.console.error(error);
    }
  }, []);

  const disconnectAccount = useCallback(async () => {
    await web3Modal.clearCachedProvider();
    if (provider?.disconnect && typeof provider.disconnect === 'function') {
      await provider.disconnect();
    }

    setUserAccount(null);
    setUserBalance(null);
    setErrorMessage(null);
    setProvider(null);
  }, [provider]);

  // Auto connect to the cached provider
  useEffect(() => {
    if (web3Modal.cachedProvider) {
      handleLogin();
    }
  }, [handleLogin]);

  // A `provider` should come with EIP-1193 events. We'll listen for those events
  // here so that when a user switches accounts or networks, we can update the
  // local React state with that new information.
  useEffect(() => {
    if (provider?.on) {
      const handleAccountsChanged = (accounts) => {
        window.console.log('accountsChanged', accounts);
        setUserAccount(accounts[0]);
      };

      // https://docs.ethers.io/v5/concepts/best-practices/#best-practices--network-changes
      const handleChainChanged = () => {
        window.location.reload();
      };

      const handleDisconnect = (error) => {
        window.console.log('disconnect', error);
        disconnectAccount();
      };

      provider.on('accountsChanged', handleAccountsChanged);
      provider.on('chainChanged', handleChainChanged);
      provider.on('disconnect', handleDisconnect);

      // cleanup
      return () => {
        if (provider.removeListener) {
          provider.removeListener('accountsChanged', handleAccountsChanged);
          provider.removeListener('chainChanged', handleChainChanged);
          provider.removeListener('disconnect', handleDisconnect);
        }
      };
    }

    return () => {};
  }, [provider, disconnectAccount]);

  if (errorMessage) {
    return (
      <Container>
        <WalletContainer data-testid="login-error">
          {errorMessage}
        </WalletContainer>
      </Container>
    );
  }

  if (!account) {
    return (
      <Container>
        <Button type="primary" onClick={handleLogin}>
          Connect Wallet
        </Button>
      </Container>
    );
  }

  return (
    <Container>
      <DetailsContainer>
        <WalletContainer>
          {!CHAIN_ID.includes(chainId) && (
            <div className="unsupported-network">
              Unsupported network
            </div>
          )}
          <div>{isNil(balance) ? '--' : `${round(balance, 2)} ETH`}</div>
          <div className="dash" />
          <div className="address">{account ? `${account}` : 'NA'}</div>
          <Button variant="transparent" onClick={disconnectAccount}>
            Disconnect
          </Button>
        </WalletContainer>
      </DetailsContainer>
    </Container>
  );
};

Login.propTypes = {
  account: PropTypes.oneOfType([PropTypes.string, PropTypes.array]),
  balance: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  chainId: PropTypes.number,
  errorMessage: PropTypes.string,
  setUserAccount: PropTypes.func.isRequired,
  setUserBalance: PropTypes.func.isRequired,
  setChainId: PropTypes.func.isRequired,
  setErrorMessage: PropTypes.func.isRequired,
};

Login.defaultProps = {
  account: null,
  balance: null,
  chainId: null,
  errorMessage: null,
};

const mapStateToProps = (state) => {
  const {
    account, balance, errorMessage, chainId,
  } = get(state, 'setup', {});
  return {
    account,
    balance,
    chainId,
    errorMessage,
  };
};

const mapDispatchToProps = {
  setUserAccount: setUserAccountFn,
  setUserBalance: setUserBalanceFn,
  setChainId: setChainIdFn,
  setErrorMessage: setErrorMessageFn,
};

export default connect(mapStateToProps, mapDispatchToProps)(Login);
