#!/usr/bin/env python3
"""
Demo script for N8Nation AI Copilot System
Shows the complete workflow without external dependencies
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def create_sample_knowledge_base():
    """Create sample knowledge base content for demonstration"""
    
    # Create knowledge-base directory structure
    knowledge_dir = Path("knowledge-base")
    knowledge_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (knowledge_dir / "n8n-spanish").mkdir(exist_ok=True)
    (knowledge_dir / "n8n-english").mkdir(exist_ok=True)
    (knowledge_dir / "workflows").mkdir(exist_ok=True)
    (knowledge_dir / "integrations").mkdir(exist_ok=True)
    
    sample_docs = [
        {
            "path": "knowledge-base/n8n-spanish/webhooks-basico.md",
            "content": """# Webhooks en n8n - Guía Básica

Los webhooks en n8n son endpoints HTTP que permiten recibir datos de servicios externos en tiempo real.

## ¿Qué es un Webhook?

Un webhook es una URL especial que puede recibir datos cuando algo sucede en otro sistema. Es como tener un teléfono que suena cuando alguien quiere enviarte información.

## Configuración Básica

Para configurar un webhook en n8n:

1. **Agregar el nodo Webhook**: Busca "Webhook" en la lista de nodos
2. **Configurar el método HTTP**: GET, POST, PUT, DELETE
3. **Definir la ruta**: Elige un nombre único para tu webhook
4. **Activar el workflow**: El webhook solo funciona cuando el workflow está activo

## Ejemplo Práctico

```json
{
  "webhook_url": "https://tu-instancia-n8n.com/webhook/mi-webhook",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

## Mejores Prácticas

- Usa nombres descriptivos para tus webhooks
- Siempre valida los datos recibidos
- Implementa autenticación si es necesario
- Registra los eventos para debugging
"""
        },
        {
            "path": "knowledge-base/n8n-english/webhooks-advanced.md",
            "content": """# Advanced Webhooks in n8n

Advanced webhook configurations and patterns for enterprise n8n implementations.

## Webhook Security

When implementing webhooks in production environments, security is paramount.

### Authentication Methods

1. **API Keys**: Include API keys in headers
2. **HMAC Signatures**: Verify payload integrity
3. **IP Whitelisting**: Restrict webhook sources
4. **OAuth 2.0**: For complex authentication flows

### Payload Validation

Always validate incoming webhook payloads:

```javascript
// Example validation in Code node
if (!$input.item.json.event_type) {
  throw new Error('Missing required field: event_type');
}

return {
  json: {
    validated: true,
    event: $input.item.json.event_type,
    timestamp: new Date().toISOString()
  }
};
```

## Error Handling

Implement robust error handling for webhook endpoints:

- Return appropriate HTTP status codes
- Log errors for debugging
- Implement retry mechanisms
- Set up monitoring and alerts

## Performance Considerations

- Use queues for high-volume webhooks
- Implement rate limiting
- Optimize workflow execution paths
- Monitor resource usage
"""
        },
        {
            "path": "knowledge-base/workflows/whatsapp-integration.md",
            "content": """# Integración WhatsApp Business con n8n

Guía completa para integrar WhatsApp Business API con n8n para automatizar mensajes y respuestas.

## Prerrequisitos

- Cuenta de WhatsApp Business verificada
- Token de acceso de WhatsApp Business API
- Webhook URL configurada en Facebook Developers
- Números de teléfono verificados

## Configuración Inicial

### 1. Configurar Credentials

En n8n, configura las credenciales de WhatsApp Business:
- API Token
- Phone Number ID
- WhatsApp Business Account ID

### 2. Webhook Configuration

```json
{
  "webhook_url": "https://tu-n8n.com/webhook/whatsapp",
  "verify_token": "tu_token_secreto",
  "fields": [
    "messages",
    "messaging_feedback",
    "message_deliveries",
    "message_reads",
    "message_echoes"
  ]
}
```

## Casos de Uso Comunes

### Respuestas Automáticas
- Mensajes de bienvenida
- Respuestas fuera de horario
- Confirmaciones de pedidos
- Información de productos

### Notificaciones
- Alertas de pedidos
- Recordatorios de citas
- Actualizaciones de envío
- Promociones personalizadas

### Soporte al Cliente
- Escalamiento automático
- Clasificación de consultas
- Asignación a agentes
- Seguimiento de casos

## Ejemplo de Workflow

1. **Trigger**: Webhook recibe mensaje
2. **Procesamiento**: Analizar contenido del mensaje
3. **Decisión**: Determinar tipo de respuesta
4. **Acción**: Enviar respuesta apropiada
5. **Logging**: Registrar interacción

## Mejores Prácticas

- Implementar límites de velocidad
- Validar números de teléfono
- Manejar errores graciosamente
- Mantener historial de conversaciones
- Cumplir políticas de WhatsApp
"""
        },
        {
            "path": "knowledge-base/integrations/api-terceros.md",
            "content": """# Integraciones con APIs de Terceros

Guía para conectar n8n con servicios externos a través de APIs REST.

## Conceptos Básicos

Las APIs (Application Programming Interfaces) son la forma estándar de comunicación entre diferentes sistemas de software.

## Tipos de Autenticación

### API Key
La más simple, se envía en headers o query parameters.

```json
{
  "headers": {
    "X-API-Key": "tu-api-key-aqui",
    "Content-Type": "application/json"
  }
}
```

### Bearer Token
Común en APIs modernas, especialmente JWT.

```json
{
  "headers": {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "Content-Type": "application/json"
  }
}
```

### OAuth 2.0
Para integraciones más seguras y complejas.

## Servicios Populares en LATAM

### Mercado Pago
- Procesamiento de pagos
- Notificaciones de transacciones
- Gestión de suscripciones

### Tiendanube
- Sincronización de productos
- Gestión de pedidos
- Actualizaciones de inventario

### Vtex
- E-commerce enterprise
- Integraciones con ERPs
- Gestión de catálogos

## Manejo de Errores

```javascript
try {
  const response = await $http.request({
    method: 'POST',
    url: 'https://api.ejemplo.com/data',
    headers: {
      'Authorization': 'Bearer ' + $node["Credentials"].json["token"]
    },
    json: true,
    body: $input.item.json
  });
  
  return { json: response };
} catch (error) {
  console.error('API Error:', error.message);
  
  // Reintento para errores temporales
  if (error.httpCode >= 500) {
    throw new Error('Temporary API error, will retry');
  }
  
  throw error;
}
```

## Rate Limiting

Muchas APIs tienen límites de velocidad:

- Implementar delays entre requests
- Usar batch operations cuando sea posible
- Monitorear headers de rate limiting
- Implementar backoff exponencial
"""
        }
    ]
    
    # Create sample files
    for doc in sample_docs:
        file_path = Path(doc["path"])
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
    
    print("✅ Base de conocimiento de ejemplo creada")
    return len(sample_docs)

def simulate_processing():
    """Simulate document processing without external dependencies"""
    
    print("\n🔄 SIMULANDO PROCESAMIENTO DE DOCUMENTOS")
    print("=" * 50)
    
    # Simulate finding markdown files
    knowledge_dir = Path("knowledge-base")
    if not knowledge_dir.exists():
        print("❌ Directorio knowledge-base no existe")
        return []
    
    md_files = list(knowledge_dir.glob("**/*.md"))
    print(f"📁 Encontrados {len(md_files)} archivos .md")
    
    # Simulate processing each file
    processed_chunks = []
    
    for file_path in md_files:
        print(f"   📄 Procesando: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple language detection
            spanish_words = content.lower().count('qué') + content.lower().count('cómo') + content.lower().count('configurar')
            english_words = content.lower().count('what') + content.lower().count('how') + content.lower().count('configure')
            
            language = 'es' if spanish_words > english_words else 'en'
            
            # Classify content type
            path_str = str(file_path).lower()
            if 'webhook' in path_str:
                doc_type = 'webhook'
            elif 'integration' in path_str or 'api' in path_str:
                doc_type = 'integration'
            elif 'workflow' in path_str:
                doc_type = 'workflow'
            else:
                doc_type = 'general'
            
            # Create chunk
            chunk = {
                'source': str(file_path).replace('\\', '/'),
                'heading': file_path.stem.replace('-', ' ').title(),
                'content': content,
                'language': language,
                'type': doc_type,
                'word_count': len(content.split()),
                'char_count': len(content)
            }
            
            processed_chunks.append(chunk)
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    return processed_chunks

def simulate_embedding(chunks: List[Dict[str, Any]]):
    """Simulate embedding process without external dependencies"""
    
    print(f"\n🧠 SIMULANDO GENERACIÓN DE EMBEDDINGS")
    print("=" * 50)
    
    if not chunks:
        print("❌ No hay chunks para procesar")
        return
    
    print(f"📊 Procesando {len(chunks)} chunks...")
    
    # Simulate language and type distribution
    languages = {}
    types = {}
    
    for chunk in chunks:
        lang = chunk.get('language', 'unknown')
        chunk_type = chunk.get('type', 'general')
        languages[lang] = languages.get(lang, 0) + 1
        types[chunk_type] = types.get(chunk_type, 0) + 1
    
    print(f"   Distribución por idioma: {languages}")
    print(f"   Distribución por tipo: {types}")
    
    # Simulate successful embedding
    print(f"   ✅ Embeddings generados exitosamente")
    print(f"   💾 Base de datos vectorial simulada creada")
    
    return True

def simulate_query_system(chunks: List[Dict[str, Any]]):
    """Simulate the query system"""
    
    print(f"\n🤖 SIMULANDO SISTEMA DE CONSULTAS")
    print("=" * 50)
    
    if not chunks:
        print("❌ No hay base de conocimiento disponible")
        return
    
    # Sample queries
    sample_queries = [
        {
            'query': '¿Cómo configurar un webhook en n8n?',
            'language': 'es'
        },
        {
            'query': 'How to integrate WhatsApp with n8n?',
            'language': 'en'
        },
        {
            'query': '¿Cuáles son las mejores prácticas para APIs?',
            'language': 'es'
        }
    ]
    
    print("📝 Probando consultas de ejemplo:")
    
    for i, test_query in enumerate(sample_queries, 1):
        print(f"\n   🧪 Consulta {i}: {test_query['query']}")
        print(f"      Idioma: {test_query['language']}")
        
        # Simulate finding relevant chunks
        query_lower = test_query['query'].lower()
        relevant_chunks = []
        
        for chunk in chunks:
            content_lower = chunk['content'].lower()
            # Simple keyword matching simulation
            if any(word in content_lower for word in query_lower.split()):
                relevant_chunks.append(chunk)
        
        print(f"      🔍 Encontrados {len(relevant_chunks)} chunks relevantes")
        
        if relevant_chunks:
            # Show first relevant chunk
            best_chunk = relevant_chunks[0]
            print(f"      📄 Fuente principal: {best_chunk['source']}")
            print(f"      🗣️ Idioma del contenido: {best_chunk['language']}")
            print(f"      📋 Tipo: {best_chunk['type']}")
            
            # Simulate response
            if test_query['language'] != best_chunk['language']:
                print(f"      🔄 Traducción automática activada")
            
            print(f"      ✅ Respuesta simulada generada")
        else:
            print(f"      ⚠️ No se encontró información relevante")

def main():
    """Main demo function"""
    
    print("🚀 N8NATION AI COPILOT - DEMOSTRACIÓN COMPLETA")
    print("=" * 60)
    print("Esta demo muestra el flujo completo sin dependencias externas")
    print()
    
    # Step 1: Create sample knowledge base
    print("📚 PASO 1: Crear base de conocimiento de ejemplo")
    doc_count = create_sample_knowledge_base()
    
    # Step 2: Simulate document processing
    chunks = simulate_processing()
    
    if not chunks:
        print("❌ No se pudieron procesar documentos")
        return
    
    # Step 3: Simulate embedding generation
    embedding_success = simulate_embedding(chunks)
    
    if not embedding_success:
        print("❌ Falló la simulación de embeddings")
        return
    
    # Step 4: Simulate query system
    simulate_query_system(chunks)
    
    # Final summary
    print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print(f"📊 Resumen:")
    print(f"   • {doc_count} documentos de muestra creados")
    print(f"   • {len(chunks)} chunks procesados")
    print(f"   • Sistema multiidioma demostrado")
    print(f"   • Clasificación automática de contenido")
    print(f"   • Búsqueda semántica simulada")
    print(f"   • Traducción automática integrada")
    
    print(f"\n💡 Para usar el sistema real:")
    print(f"   1. Configura GOOGLE_API_KEY")
    print(f"   2. Instala dependencias: pip install -r requirements.txt")
    print(f"   3. Ejecuta: python process_docs.py")
    print(f"   4. Ejecuta: python embed_and_store.py") 
    print(f"   5. Ejecuta: python copilot.py")
    
    # Cleanup option
    cleanup = input(f"\n¿Eliminar archivos de demostración? (y/N): ").strip().lower()
    if cleanup == 'y':
        import shutil
        try:
            shutil.rmtree("knowledge-base")
            print("🗑️ Archivos de demostración eliminados")
        except Exception as e:
            print(f"⚠️ Error eliminando archivos: {e}")

if __name__ == "__main__":
    main()
