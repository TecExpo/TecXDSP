import { useEffect, useState } from 'react';
import styles from '../styles/global.css';

export default function SimulationStats() {
  const [simulations, setSimulations] = useState([]);

  useEffect(() => {
    // Simulating fetching data from API
    setSimulations([
      { id: 1, name: 'CFD Analysis', status: 'Completed', duration: '12 min' },
      { id: 2, name: 'Structural FEA', status: 'Running', duration: 'N/A' },
      { id: 3, name: 'Thermal Simulation', status: 'Failed', duration: '5 min' },
    ]);
  }, []);

  return (
    <div className={styles.statsContainer}>
      <h2>Recent Simulations</h2>
      <ul>
        {simulations.map((sim) => (
          <li key={sim.id}>
            <strong>{sim.name}</strong> - Status: {sim.status} - Duration: {sim.duration}
          </li>
        ))}
      </ul>
    </div>
  );
}
