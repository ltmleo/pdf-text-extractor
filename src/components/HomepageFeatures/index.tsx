import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  link?: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Doces - Vó Elisa',
    Svg: require('@site/static/img/book-closed-svgrepo-com.svg').default,
    link: '/receitas/doces-vo-elisa',
  },
  {
    title: 'Salgados - Vó Elisa (em breve)',
    Svg: require('@site/static/img/book-closed-svgrepo-com-grey.svg').default,
  },
  {
    title: 'Receitas - Vó Cida (em breve)',
    Svg: require('@site/static/img/book-closed-svgrepo-com-grey.svg').default,
  },
  {
    title: 'Receitas - Bisavó Cidona (em breve)',
    Svg: require('@site/static/img/book-closed-svgrepo-com-grey.svg').default,
  },
  {
    title: 'Receitas - Bisavó Romilda (em breve)',
    Svg: require('@site/static/img/book-closed-svgrepo-com-grey.svg').default,
  },
  {
    title: 'Receitas - Bisavó Gera (em breve)',
    Svg: require('@site/static/img/book-closed-svgrepo-com-grey.svg').default,
  },
];

function Feature({title, Svg, link}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.featureItem)}>
      {link ? (
        <Link to={link}>
          <div className="text--center padding-horiz--md">
            <Heading as="h3">{title}</Heading>
          </div>
          <div className="text--center">
            <Svg className={styles.featureSvg} role="img" />
          </div>
        </Link>
      ) : (
        <div>
          <div className="text--center padding-horiz--md">
            <Heading as="h3">{title}</Heading>
          </div>
          <div className="text--center">
            <Svg className={styles.featureSvg} role="img" />
          </div>
        </div>
      )}
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
