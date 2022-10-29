import { apiTypes, syncTypes } from './_types';

const initialState = {
  account: null,
  balance: null,
  chainId: null,
  errorMessage: null,
};

export default (state = initialState, action) => {
  const { data } = action;

  switch (action.type) {
    case apiTypes.GET_API: {
      return { ...state, data };
    }

    case syncTypes.SET_ACCOUNT:
    case syncTypes.SET_BALANCE:
    case syncTypes.SET_LOGIN_ERROR:
    case syncTypes.SET_CHAIND_ID:
    case syncTypes.SET_STORE_STATE: {
      return { ...state, ...action.data };
    }

    default:
      return state;
  }
};
