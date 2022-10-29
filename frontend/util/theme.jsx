export const COLOR = {
  PRIMARY: '#1D1CE5',
  GREY_1: '#C4C4C4',
  WHITE: '#FFFFFF',
  BLACK: '#000000',
  BORDER_GREY: '#F0F0F0',
  RED: '#FC0E38',

  WALLECT_CONNECT_BLUE: '#1890ff',
};

export const BREAK_POINT = {
  xxxs: '340px',
  xxs: '375px',
  xs: '480px',
  sm: '576px',
  md: '768px',
  lg: '992px',
  xl: '1200px',
  xxl: '1600px',
};

export const MEDIA_QUERY = {
  mobileXS: `@media only screen and (max-width: ${BREAK_POINT.xxxs})`,
  mobileS: `@media only screen and (max-width: ${BREAK_POINT.xxs})`,
  mobileM: `@media only screen and (max-width: ${BREAK_POINT.xs})`,
  mobileL: `@media only screen and (max-width: ${BREAK_POINT.sm})`,
  tablet: `@media only screen and (max-width: ${BREAK_POINT.md})`,
  tabletL: `@media only screen and (max-width: ${BREAK_POINT.lg})`,
  laptop: `@media only screen and (max-width: ${BREAK_POINT.xl})`,
  desktop: `@media only screen and (max-width: ${BREAK_POINT.xxl})`,
};
