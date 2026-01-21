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
2.  Construye y sube cada servicio (reemplaza `TU_USUARIO_DOCKER`):

    ```bash
    # Users Service
    docker build -t TU_USUARIO_DOCKER/users-service:latest -f docker/Dockerfile.users .
    docker push TU_USUARIO_DOCKER/users-service:latest

    # Orders Service
    docker build -t TU_USUARIO_DOCKER/orders-service:latest -f docker/Dockerfile.orders .
    docker push TU_USUARIO_DOCKER/orders-service:latest

    # Gateway API
    docker build -t TU_USUARIO_DOCKER/gateway-api:latest -f docker/Dockerfile.gateway .
    docker push TU_USUARIO_DOCKER/gateway-api:latest

    # Web App
    docker build -t TU_USUARIO_DOCKER/web-app:latest -f docker/Dockerfile.frontend .
    docker push TU_USUARIO_DOCKER/web-app:latest
    ```

**IMPORTANTE**: Debes actualizar los manifiestos en `k8s/01-app-v1/*.yaml` para usar `image: TU_USUARIO_DOCKER/users-service:latest`, etc. en lugar de `antigravity/...`.
Puedes hacerlo rápido con `sed` en la VM:
```bash
sed -i 's|antigravity/|TU_USUARIO_DOCKER/|g' k8s/01-app-v1/*.yaml
sed -i 's|antigravity/|TU_USUARIO_DOCKER/|g' k8s/03-ha/*.yaml
```

## Paso 3: Despliegue Fase 0 (Base)
```bash
# Crear namespaces
kubectl apply -f k8s/00-namespaces

# Instalar Base de Datos (Postgres)
helm repo add bitnami https://charts.bitnami.com/bitnami
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
