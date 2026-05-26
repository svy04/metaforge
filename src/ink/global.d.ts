import type { ReactNode, Ref } from 'react';
import type { DOMElement } from './dom.js';
import type { Styles, TextStyles } from './styles.js';

type InkIntrinsicProps = {
  ref?: Ref<DOMElement>;
  children?: ReactNode;
  style?: Styles;
  textStyles?: TextStyles;
  [key: string]: unknown;
};

type InkIntrinsicElements = {
  'ink-box': InkIntrinsicProps;
  'ink-link': InkIntrinsicProps;
  'ink-raw-ansi': InkIntrinsicProps;
  'ink-root': InkIntrinsicProps;
  'ink-text': InkIntrinsicProps;
  'ink-virtual-text': InkIntrinsicProps;
};

declare global {
  namespace JSX {
    interface IntrinsicElements extends InkIntrinsicElements {}
  }
}

declare module 'react' {
  namespace JSX {
    interface IntrinsicElements extends InkIntrinsicElements {}
  }
}

export {};
