#!/bin/bash
# n8nation - Script de Limpieza y Organización
# Elimina archivos innecesarios y organiza el proyecto

echo "🧹 n8nation - Limpieza y Organización del Proyecto"
echo "=================================================="

# Verificar que estamos en la ubicación correcta
if [[ ! -d "/workspaces/n8n_local_docker_ngrok/n8nation" ]]; then
    echo "❌ Error: No se encuentra el directorio n8nation"
    exit 1
fi

cd /workspaces/n8n_local_docker_ngrok

echo "📁 Estado actual del proyecto:"
echo "- n8nation/: $(find n8nation -name "*.md" | wc -l) archivos .md"
echo "- n8n-docs-review/: $(find n8n-docs-review -name "*.md" 2>/dev/null | wc -l) archivos .md"

echo ""
echo "🔍 Elementos útiles ya rescatados de n8n-docs-review:"
echo "  ✅ mkdocs.yml adaptado -> n8nation/docs/mkdocs-setup/"
echo "  ✅ requirements.txt mejorado"
echo "  ✅ .gitignore optimizado"
echo "  ✅ .editorconfig personalizado"

echo ""
read -p "¿Quieres eliminar la carpeta n8n-docs-review? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Eliminando n8n-docs-review..."
    rm -rf n8n-docs-review/
    echo "✅ Carpeta n8n-docs-review eliminada"
    
    echo ""
    echo "📊 Estado final del proyecto:"
    echo "- n8nation/: $(find n8nation -name "*.md" | wc -l) archivos .md"
    echo "- AI Copilot: $(ls -la n8nation/docs/ai-copilot/*.py 2>/dev/null | wc -l) archivos Python"
    echo "- MkDocs Setup: $(ls -la n8nation/docs/mkdocs-setup/ | wc -l) archivos de configuración"
    
    echo ""
    echo "🎉 ¡Proyecto limpio y organizado!"
    echo "📋 Próximo paso: Implementar MkDocs con la configuración rescatada"
    echo "💡 Ejecuta: cd n8nation && pip install -r docs/mkdocs-setup/requirements.txt"
else
    echo "ℹ️  Carpeta n8n-docs-review mantenida"
    echo "💡 Puedes revisarla manualmente si necesitas algo más"
fi

echo ""
echo "📋 TODO actualizado en: n8nation/TODO.md"
echo "🚀 Siguiente paso: MkDocs setup con configuración rescatada"
