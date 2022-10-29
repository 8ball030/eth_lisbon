import styled from 'styled-components';
import { Layout } from 'antd';
import { COLOR, MEDIA_QUERY } from 'util/theme';

export const CustomLayout = styled(Layout)`
  background-size: 100%;
  background-color: ${COLOR.WHITE};
  .ant-layout-header {
    z-index: 1;
    position: fixed;
    height: 82px;
    width: 100%;
    padding: 0 1rem;
    background-color: ${COLOR.WHITE};
  }
  .site-layout {
    padding: 0 1rem;
    margin-top: 90px;
  }
  .site-layout-background {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 0;
    min-height: calc(100vh - 8.5rem);
  }
  .ant-layout-footer {
    text-align: center;
  }
  .ant-result-title {
    color: ${COLOR.BLACK};
  }

  ${MEDIA_QUERY.tablet} {
    .ant-layout-header {
      ${MEDIA_QUERY.tablet} {
        position: relative;
        height: auto;
      }
    }
    .site-layout-background {
      ${MEDIA_QUERY.tablet} {
        padding: 1rem 0;
        min-height: calc(100vh - 20rem);
      }
    }
    .site-layout {
      margin-top: 0;
    }
  }
`;

// HEADER
export const HeaderContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  background-color: ${COLOR.WHITE};

  ${MEDIA_QUERY.tablet} {
    margin-bottom: 0;
    .column-1 {
      line-height: normal;
    }
  }

  /* nav-bar for pages except landing-page */
  ${MEDIA_QUERY.mobileL} {
    margin-bottom: 0;
  }

  ${MEDIA_QUERY.mobileM} {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
`;

export const Logo = styled.div`
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: left;
  margin-left: 0.5rem;
  margin-right: 3.5rem;
  font-size: 34px;
  color: ${COLOR.PRIMARY};
  span {
    margin-left: 0.5rem;
  }
`;

// FOOTER
export const Container = styled.div`
  margin-top: 2rem;
  font-size: 20px;
`;

export const SubFooter = styled.div`
  display: flex;
  align-items: flex-start;
  justify-content: center;
  margin-top: 0.5rem;
  padding: 2rem 1rem;
  border: 1px solid ${COLOR.GREY_1};
  border-radius: 0px 0px 20px 20px;
  border-top-color: transparent;

  ${MEDIA_QUERY.tabletL} {
  }

  ${MEDIA_QUERY.tablet} {
    position: relative;
    flex-direction: column;
    font-size: 16px;
    padding: 2rem 0.75rem 1.5rem 0.75rem;
  }

  ${MEDIA_QUERY.mobileS} {
  }
`;
