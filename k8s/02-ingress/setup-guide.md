# Configuración de Ingress y MetalLB

## 1. Instalar Ingress Nginx
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx -n k8s-lab-platform --create-namespace
```

## 2. Instalar MetalLB
```bash
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb -n metallb-system --create-namespace
```

## 3. Configurar Pool IP de MetalLB
Crea un archivo `metallb-pool.yaml`:
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.1.240-192.168.1.250 # CAMBIA ESTO para que coincida con la red de tu VM
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
```
Aplícalo con `kubectl apply -f metallb-pool.yaml`
