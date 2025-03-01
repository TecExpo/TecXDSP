# Immersive VR/AR Experience
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import dynamic from 'next/dynamic';
import styles from '../styles/global.css';

const ARVRViewer = dynamic(() => import('../components/ARVRViewer'), { ssr: false });

export default function ARVRSimulation() {
  return (
    <div>
      <Head>
        <title>AR/VR Simulation - HiTech Design Simulation Platform</title>
        <meta name="description" content="Experience immersive AR/VR-based design simulations." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Header />
      <main className={styles.main}>
        <h1>AR/VR Simulation</h1>
        <p>Engage in real-time AR/VR-powered simulations for advanced digital modeling.</p>
        <ARVRViewer />
      </main>
      <Footer />
    </div>
  );
}

