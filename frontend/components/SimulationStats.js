import { useEffect, useState } from 'react';

export default function SimulationStats() {
  const [simulations, setSimulations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSimulations() {
      try {
        const response = await fetch('/api/simulations');
        const data = await response.json();
        setSimulations(data);
      } catch (error) {
        console.error('Error fetching simulations:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchSimulations();
  }, []);

  return (
    <div className="p-4 bg-gray-900 text-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-3">Recent Simulations</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="space-y-2">
          {simulations.map((sim) => (
            <li key={sim.id} className="p-2 bg-gray-800 rounded-md">
              <strong>{sim.name}</strong> - Status: <span className={`font-semibold ${sim.status === 'Completed' ? 'text-green-400' : 'text-red-400'}`}>{sim.status}</span> - Duration: {sim.duration}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
