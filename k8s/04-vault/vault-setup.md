# Configuración de HashiCorp Vault

## 1. Instalar Vault vía Helm
```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault -n vault-system --create-namespace
```

## 2. Desellado de Vault (Paso Manual)
```bash
kubectl exec -ti vault-0 -n vault-system -- vault operator init
# ¡Guarda las llaves!
kubectl exec -ti vault-0 -n vault-system -- vault operator unseal <llave1>
kubectl exec -ti vault-0 -n vault-system -- vault operator unseal <llave2>
kubectl exec -ti vault-0 -n vault-system -- vault operator unseal <llave3>
```

## 3. Habilitar Autenticación Kubernetes
```bash
kubectl exec -ti vault-0 -n vault-system -- sh
# Dentro del pod:
vault login <root-token>
vault auth enable kubernetes
vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

## 4. Crear Política y Rol
```bash
vault policy write app-policy - <<EOF
path "secret/data/app-config" {
  capabilities = ["read"]
}
EOF

vault write auth/kubernetes/role/app-role \
    bound_service_account_names=default \
    bound_service_account_namespaces=k8s-lab-app \
    policies=app-policy \
    ttl=24h
```

## 5. Agregar un Secreto
```bash
vault kv put secret/app-config database_url="postgresql://..."
```
