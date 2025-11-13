#!/bin/bash
# Script de Deploy Automatizado - Portal AYMA Backend

echo "🚀 DEPLOY AUTOMÁTICO - PORTAL AYMA BACKEND"
echo "=========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Debes ejecutar este script desde el directorio backend/"
    exit 1
fi

echo "✅ Directorio correcto verificado"
echo ""

# Verificar git
if ! command -v git &> /dev/null; then
    echo "❌ Git no está instalado"
    echo "   Instala con: brew install git"
    exit 1
fi

echo "✅ Git instalado"
echo ""

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    echo "✅ Git inicializado"
else
    echo "✅ Repositorio Git ya existe"
fi

echo ""

# Agregar todos los archivos
echo "📝 Agregando archivos al commit..."
git add .
echo "✅ Archivos agregados"
echo ""

# Crear commit
echo "💾 Creando commit..."
git commit -m "Backend Portal AYMA - Deploy $(date +%Y-%m-%d)"
echo "✅ Commit creado"
echo ""

# Verificar GitHub CLI
if command -v gh &> /dev/null; then
    echo "🔐 GitHub CLI detectado"
    echo ""
    echo "¿Quieres crear el repositorio en GitHub automáticamente? (s/n)"
    read -r response
    
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        echo ""
        echo "📤 Creando repositorio en GitHub..."
        gh repo create ayma-portal-backend --public --source=. --remote=origin --push
        echo ""
        echo "✅ Repositorio creado y código subido!"
        echo ""
        echo "🌐 URL del repositorio:"
        gh repo view --web
    else
        echo "⏭️  Saltando creación automática"
    fi
else
    echo "ℹ️  GitHub CLI no detectado"
    echo "   Puedes instalarlo con: brew install gh"
    echo ""
    echo "📖 Instrucciones para subir manualmente:"
    echo "   1. Ve a: https://github.com/new"
    echo "   2. Nombre: ayma-portal-backend"
    echo "   3. Público"
    echo "   4. Crear repositorio"
    echo "   5. Ejecuta estos comandos:"
    echo ""
    echo "   git branch -M main"
    echo "   git remote add origin https://github.com/TU_USUARIO/ayma-portal-backend.git"
    echo "   git push -u origin main"
fi

echo ""
echo "=========================================="
echo "✅ PREPARACIÓN COMPLETA"
echo "=========================================="
echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo ""
echo "1. Ir a: https://railway.app/"
echo "2. Login con GitHub"
echo "3. New Project → Deploy from GitHub repo"
echo "4. Seleccionar: ayma-portal-backend"
echo "5. Agregar PostgreSQL (+ New → Database → PostgreSQL)"
echo "6. Configurar variables de entorno"
echo "7. Generate Domain"
echo ""
echo "📚 Ver guía completa en: GUIA-DEPLOY-RAILWAY.md"
echo ""
