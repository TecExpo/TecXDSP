# orchestration/
#│   ├── istio/
#│   │   ├── install-istio.sh
#│   │   ├── enable-mtls.yaml
#│   │   ├── canary-deployment.yaml
#│   │   ├── blue-green-deployment.yaml
#│   │   ├── traffic-splitting.yaml

#!/bin/bash
# Install Istio with default profile
istioctl install --set profile=default -y

# Enable Istio injection for the default namespace
kubectl label namespace default istio-injection=enabled --overwrite

echo "✅ Istio installation completed."

