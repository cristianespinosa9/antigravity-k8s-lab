# Laboratorio Antigravity K8s

Un entorno completo de laboratorio para Kubernetes.

## Resumen Lógico
- **Servicios**: Usuarios, Órdenes, Gateway (FastAPI), Aplicación Web (React).
- **Base de Datos**: PostgreSQL (Alta Disponibilidad vía Bitnami).
- **Ingress**: Nginx + MetalLB.
- **Seguridad**: NetworkPolicies, RBAC, Vault, Kyverno.
- **Observabilidad**: Prometheus, Grafana.

## Primeros Pasos
1. **Construir Imágenes Docker**: Ejecuta `docker build ...` para cada servicio (ver carpeta `docker/`).
2. **Configurar Kubernetes**:
   - Aplicar namespaces: `kubectl apply -f k8s/00-namespaces`
   - Instalar BD: `helm install postgres bitnami/postgresql -f db/postgres/values.yaml -n k8s-lab-app`
3. **Desplegar Aplicación**: `kubectl apply -f k8s/01-app-v1`
4. **Redes**: Sigue `k8s/02-ingress/setup-guide.md`.

## Fases del Laboratorio
- **01-app-v1**: Despliegue básico.
- **03-ha**: Alta disponibilidad (réplicas, probes). Aplica `k8s/03-ha` para actualizar.
- **04-vault**: Habilitar inyección de secretos.
- **05-monitoring**: Habilitar observabilidad.
