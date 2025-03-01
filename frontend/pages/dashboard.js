import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import dynamic from 'next/dynamic';
import styles from '../styles/global.css';

const SimulationStats = dynamic(() => import('../components/SimulationStats'), { ssr: false });

export default function Dashboard() {
  return (
    <div>
      <Head>
        <title>Dashboard - HiTech Design Simulation Platform</title>
        <meta name="description" content="User dashboard for managing simulations and analytics." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Header />
      <main className={styles.main}>
        <h1>Dashboard</h1>
        <p>View your recent simulations, performance metrics, and analytics.</p>
        <SimulationStats />
      </main>
      <Footer />
    </div>
  );
}
