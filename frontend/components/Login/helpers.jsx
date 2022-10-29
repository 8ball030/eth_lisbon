import WalletConnectProvider from '@walletconnect/web3-provider';

export const providerOptions = {
  walletconnect: {
    package: WalletConnectProvider, // required
    options: {
      infuraId: undefined, // required
      rpc: {
        1: process.env.NEXT_PUBLIC_MAINNET_URL,
        25: process.env.NEXT_PUBLIC_CRONOS,
      },
    },
  },
};
