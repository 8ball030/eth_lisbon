import styled, { createGlobalStyle } from 'styled-components';
import { MEDIA_QUERY, COLOR } from 'util/theme';

// const GlobalStyles = styled.div`
const GlobalStyle = createGlobalStyle`
  *,
  :after,
  :before {
    box-sizing: border-box;
  }
  body,
  html {
    width: 100%;
    height: 100%;
    overscroll-behavior: none;
    margin: 0;
  }
  /* common */
  .mb-8 {
    margin-bottom: 0.5rem;
  }

  .walletconnect-modal__base {
    .walletconnect-modal__mobile__toggle a {
      color: ${COLOR.WALLECT_CONNECT_BLUE} !important;
    }
  }

  .ant-notification-notice-message {
    margin: 0px !important;
  }

  .ant-alert {
    border-radius: 5px;
  }

  .show-only-sm {
    display: none;
  }
  .hide-only-sm {
    display: initial;
  }
  ${MEDIA_QUERY.mobileL} {
    .show-only-sm {
      display: initial;
    }
    .hide-only-sm {
      display: none;
    }
  }
`;

export default GlobalStyle;

export const Ellipsis = styled.span`
  max-width: 100px;
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  ${MEDIA_QUERY.tablet} {
    max-width: 200px;
  }
`;
