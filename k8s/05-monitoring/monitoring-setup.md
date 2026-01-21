# Configuración de Monitoreo

## 1. Instalar kube-prometheus-stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack -n k8s-lab-monitoring --create-namespace
```

## 2. Acceder a Grafana
Puedes hacer port-forward para acceder a Grafana:
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n k8s-lab-monitoring
```
Usuario: `admin`
Contraseña: `prom-operator` (por defecto, o revisa el secreto)

## 3. Dashboards
El stack viene con dashboards pre-configurados para:
- Recursos del Clúster (CPU/Memoria)
- Node Exporter (Estadísticas del nodo)
- Componentes Kubernetes (API Server, Kubelet)
POSIX
