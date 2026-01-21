# Cómo subir este repositorio a GitHub

## 1. Crear Repositorio en GitHub
1. Ve a [github.com/new](https://github.com/new).
2. Nombre del repositorio: `antigravity-k8s-lab`.
3. Descripción: `Laboratorio de Kubernetes incremental`.
4. **NO** marques "Initialize this repository with a README" (ya tenemos uno local).
5. Haz clic en **Create repository**.

## 2. Enlazar repositorio local y subir
Abre una terminal en esta carpeta (`g:\Mi unidad\Learning kubernetes\antigravity-k8s-lab`) y ejecuta:

```bash
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/antigravity-k8s-lab.git
git branch -M main
git push -u origin main
```

## 3. Verificación
Refresca la página de GitHub y deberías ver todos los archivos.
