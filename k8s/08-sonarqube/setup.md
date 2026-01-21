# Configuración de SonarQube

## 1. Instalar SonarQube
```bash
helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm repo update
helm install sonarqube sonarqube/sonarqube -n k8s-lab-platform --create-namespace
```

## 2. Integración en CI (Paso de Ejemplo)
Agrega esto a tu GitHub Actions:
```yaml
    - name: SonarQube Scan
      uses: sonarsource/sonarqube-scan-action@master
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```
