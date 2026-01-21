# Escenarios de Troubleshooting

## 1. Pod en Estado Pending
**Síntoma**: El pod permanece en `Pending`.
**Verificación**: `kubectl describe pod <nombre_pod>`
**Causas Comunes**: Recursos insuficientes de CPU/Memoria, desajuste de Taint/Toleration, PVC no vinculado.

## 2. CrashLoopBackOff
**Síntoma**: El pod inicia y falla repetidamente.
**Verificación**: `kubectl logs <nombre_pod>`
**Causas Comunes**: Variables de entorno faltantes (URL de BD), pánico de la aplicación, comando incorrecto.

## 3. Servicio Inaccesible (ClusterIP)
**Síntoma**: No se puede hacer curl al servicio desde otro pod.
**Verificación**: `kubectl get svc` (revisar selectores), `kubectl get endpoints <nombre_svc>`
**Causas Comunes**: Desajuste en selectores, aplicación escuchando en puerto incorrecto (puerto de contenedor vs servicio).

## 4. Ingress 404 Not Found
**Síntoma**: Acceder a `app.local` retorna 404 desde Nginx.
**Verificación**: Rutas del recurso Ingress, anotaciones de reescritura.
**Causas Comunes**: Falta `nginx.ingress.kubernetes.io/rewrite-target`, desajuste de ruta.

## 5. Fallo de Conexión a Base de Datos
**Síntoma**: Logs del backend muestran "Connection refused".
**Verificación**: NetworkPolicies (¿bloqueando tráfico?), estado del pod Postgres.
**Causas Comunes**: NetworkPolicy deny-all bloqueando acceso, credenciales incorrectas.

## 6. OOMKilled
**Síntoma**: El pod se reinicia con motivo OOMKilled.
**Verificación**: `kubectl get pod -o yaml` -> status.containerStatuses.lastState
**Causas Comunes**: Límite de memoria muy bajo para el heap de Java/proceso Python.

## 7. ImagePullBackOff
**Síntoma**: El pod no puede descargar la imagen.
**Verificación**: Nombre/tag de la imagen, credenciales del registro (imagePullSecrets).
**Causas Comunes**: Registro privado sin secreto, error tipográfico en nombre de imagen.

## 8. HPA No Escala
**Síntoma**: La carga aumenta pero las réplicas no.
**Verificación**: `kubectl get hpa`, instalación de metrics server.
**Causas Comunes**: Solicitudes de recursos faltantes en Deployment (métricas no pueden calcularse).

## 9. Fallo en Inyección de Vault
**Síntoma**: El pod se cuelga en Init (vault-agent-init).
**Verificación**: Logs del inyector Vault, Anotaciones.
**Causas Comunes**: ServiceAccount no vinculado al Rol de Vault, Vault inalcanzable.

## 10. ArgoCD OutOfSync
**Síntoma**: ArgoCD muestra OutOfSync pero no lo corrige.
**Verificación**: Política de sincronización (¿automatizada?), detalles del diff.
**Causas Comunes**: Cambios manuales hechos en el clúster (drift), campos inmutables cambiados.
