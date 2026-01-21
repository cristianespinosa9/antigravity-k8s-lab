# Guía de Despliegue en VM Ubuntu (K8s 1.35)

Veo que ya tienes tu clúster Kubernetes v1.35 funcionando con Calico. ¡Excelente!
Sigue estos pasos para desplegar todo el laboratorio "Antigravity" en tu máquina virtual.

## Prerrequisitos en la VM
Asegúrate de tener instaladas las siguientes herramientas en tu Ubuntu:

1.  **Git**: `sudo apt install git`
2.  **Helm** (Gestor de paquetes para K8s):
    ```bash
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    ```
3.  **Docker** (Para construir las imágenes):
    Si no lo tienes: `sudo apt install docker.io`
    *Nota: Si estás usando containerd/nerdctl para K8s, asegúrate de poder construir imágenes y que tu K8s pueda verlas (o usa un registry como Docker Hub).*

## Paso 1: Clonar el Repositorio
En tu terminal de Ubuntu:
```bash
git clone https://github.com/TU_USUARIO/antigravity-k8s-lab.git
cd antigravity-k8s-lab
```

## Paso 2: Construir Imágenes
Como es un laboratorio local, necesitamos que el clúster tenga acceso a las imágenes.
Opción A: Subirlas a Docker Hub (Recomendado).
Opción B: Construirlas localmente (si usas K3s es automático, con K8s estándar es más complejo sin un registry local).

**Vamos con la Opción A (Docker Hub)**:
1.  Loguéate: `docker login`
2.  Construye y sube cada servicio (reemplaza `cristiane89`):

    ```bash
    # Users Service
    docker build -t cristiane89/users-service:latest -f docker/Dockerfile.users .
    docker push cristiane89/users-service:latest

    # Orders Service
    docker build -t cristiane89/orders-service:latest -f docker/Dockerfile.orders .
    docker push cristiane89/orders-service:latest

    # Gateway API
    docker build -t cristiane89/gateway-api:latest -f docker/Dockerfile.gateway .
    docker push cristiane89/gateway-api:latest

    # Web App
    docker build -t cristiane89/web-app:latest -f docker/Dockerfile.frontend .
    docker push cristiane89/web-app:latest
    ```

**IMPORTANTE**: Debes actualizar los manifiestos en `k8s/01-app-v1/*.yaml` para usar `image: cristiane89/users-service:latest`, etc. en lugar de `antigravity/...`.

### Solución de Problemas de Red (Docker Build Fails)
Si ves errores como `TLS handshake timeout` o `failed to resolve source metadata` al hacer build:
1. Probablemente sea un problema de DNS en tu VM.
2. Edita `/etc/resolv.conf` y agrega `nameserver 8.8.8.8`:
   ```bash
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   sudo systemctl restart docker
   ```
3. Si persiste, prueba reiniciando el servicio de Docker o revisando la conexión a internet (`ping google.com`).


## Paso 3: Despliegue Fase 0 (Base)
```bash
# Crear namespaces
kubectl apply -f k8s/00-namespaces

# Instalar Base de Datos (Postgres)
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql -f db/postgres/values.yaml -n k8s-lab-app
```


## Paso 3.1: Reset de Almacenamiento (Si los pods están Pending)
Si ves que `postgres-postgresql-primary-0` se queda en `Pending`, es probable que haya un conflicto con volúmenes viejos. Ejecuta esto para limpiar todo y empezar de cero con la base de datos:

```bash
# 1. Borrar la instalación actual de Postgres
helm uninstall postgres -n k8s-lab-app

# 2. Borrar los PVCs y PVs
kubectl delete pvc -n k8s-lab-app data-postgres-postgresql-primary-0 data-postgres-postgresql-read-0
kubectl delete pv postgres-primary-pv postgres-read-pv

# 3. Limpiar directorios en la VM
sudo rm -rf /mnt/data/postgres-primary/*
sudo rm -rf /mnt/data/postgres-read/*

# 4. Re-aplicar storage y chart
kubectl apply -f k8s/00-namespaces/fix-storage.yaml
helm install postgres bitnami/postgresql -f db/postgres/values.yaml -n k8s-lab-app
```

## Paso 4: Despliegue Fase 1 (Aplicación)
```bash
kubectl apply -f k8s/01-app-v1
```
Verifica que los pods arranquen:
```bash
kubectl get pods -n k8s-lab-app
```

## Paso 5: Ingress y Redes (MetalLB)
Tu clúster necesita poder asignar IPs externas.
1. Instala Ingress Nginx y MetalLB siguiendo `k8s/02-ingress/setup-guide.md`.
2. **CRÍTICO**: En `k8s/02-ingress/setup-guide.md`, verás la configuración del `IPAddressPool`.
   Asegúrate de poner un rango de IPs que esté **dentro de la red de tu VM** pero fuera del rango DHCP.
   *Ejemplo: Si tu VM tiene IP 192.168.1.50, usa 192.168.1.240-192.168.1.250.*

3. Aplica el Ingress:
   ```bash
   kubectl apply -f k8s/02-ingress/ingress.yaml
   ```

## Paso 6: Configurar DNS Local
En tu máquina Windows (donde tienes el navegador), edita `C:\Windows\System32\drivers\etc\hosts` (como Admin) y agrega:
```text
<IP_DEL_INGRESS> app.local
<IP_DEL_INGRESS> gateway.local
```
Puedes obtener la IP del Ingress con: `kubectl get ingress -n k8s-lab-app`

---

¡Listo! Ahora puedes acceder a `http://app.local` en tu navegador de Windows y ver la aplicación corriendo en tu VM.
