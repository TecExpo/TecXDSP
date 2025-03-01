import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import dynamic from 'next/dynamic';
import styles from '../styles/global.css';

const Viewer3D = dynamic(() => import('../components/3DViewer'), { ssr: false });

export default function Home() {
  return (
    <div>
      <Head>
        <title>HiTech Design Simulation Platform</title>
        <meta name="description" content="AI-driven simulation for CAD, CAE, and digital modeling." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Header />
      <main className={styles.main}>
        <h1>Welcome to HiTech Design Simulation Platform</h1>
        <p>Experience next-gen AI-powered simulations for CAD, CAE, and digital modeling.</p>
        <Viewer3D />
      </main>
      <Footer />
    </div>
  );
}
