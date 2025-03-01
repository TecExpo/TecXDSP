import { useEffect } from 'react';

export default function ARVRViewer() {
  useEffect(() => {
    if (navigator.xr) {
      console.log('WebXR is supported');
      // Load WebXR-based simulation environment here
    } else {
      console.log('WebXR not supported on this device');
    }
  }, []);

  return (
    <div style={{ width: '100%', height: '500px', backgroundColor: '#222', color: 'white', textAlign: 'center' }}>
      <h2>AR/VR Simulation Viewer</h2>
      <p>Engage in immersive simulations using WebXR technology.</p>
    </div>
  );
}
