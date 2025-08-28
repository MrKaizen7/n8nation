#!/usr/bin/env python3
"""
Prueba del sistema de traducción automática del copilot
Demuestra cómo el sistema maneja consultas en múltiples idiomas
"""

import sys
import os

# Add the copilot directory to path
sys.path.append(os.path.dirname(__file__))

from enhanced_copilot import EnhancedCopilot
import chromadb
from chromadb.config import Settings

def populate_test_knowledge_base():
    """Populate knowledge base with test data in multiple languages"""
    
    # Create test client
    client = chromadb.PersistentClient(
        path="./test_knowledge_base",
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get or create collection
    try:
        collection = client.get_collection("n8n_docs")
        # Delete existing collection for fresh start
        client.delete_collection("n8n_docs")
    except:
        pass
    
    collection = client.create_collection("n8n_docs")
    
    # Sample documents in different languages
    test_documents = [
        {
            'content': """
            Los webhooks en n8n son endpoints HTTP que permiten recibir datos de servicios externos.
            Para configurar un webhook:
            1. Agrega el nodo Webhook
            2. Configura el método HTTP (GET, POST, PUT, etc.)
            3. Define la ruta del webhook
            4. Activa el workflow
            
            El webhook estará disponible en: https://tu-instancia.com/webhook/tu-ruta
            """,
            'metadata': {
                'source': 'Guía N8N Webhooks ES',
                'heading': 'Configuración de Webhooks',
                'type': 'tutorial',
                'language': 'es'
            }
        },
        {
            'content': """
            Webhooks in n8n are HTTP endpoints that allow you to receive data from external services.
            To configure a webhook:
            1. Add the Webhook node
            2. Configure the HTTP method (GET, POST, PUT, etc.)
            3. Define the webhook path
            4. Activate the workflow
            
            The webhook will be available at: https://your-instance.com/webhook/your-path
            """,
            'metadata': {
                'source': 'N8N Webhooks Guide EN',
                'heading': 'Webhook Configuration',
                'type': 'tutorial',
                'language': 'en'
            }
        },
        {
            'content': """
            La integración de WhatsApp Business API con n8n permite automatizar mensajes y respuestas.
            Requisitos:
            - Token de acceso de WhatsApp Business API
            - Webhook URL configurada en Facebook Developers
            - Números de teléfono verificados
            
            Casos de uso comunes:
            - Respuestas automáticas a consultas
            - Notificaciones de pedidos
            - Soporte al cliente automatizado
            - Marketing directo personalizado
            """,
            'metadata': {
                'source': 'Guía WhatsApp Business N8N ES',
                'heading': 'Integración WhatsApp Business',
                'type': 'integration',
                'language': 'es'
            }
        },
        {
            'content': """
            WhatsApp Business API integration with n8n enables automated messaging and responses.
            Requirements:
            - WhatsApp Business API access token
            - Webhook URL configured in Facebook Developers  
            - Verified phone numbers
            
            Common use cases:
            - Automated responses to inquiries
            - Order notifications
            - Automated customer support
            - Personalized direct marketing
            """,
            'metadata': {
                'source': 'WhatsApp Business N8N Guide EN',
                'heading': 'WhatsApp Business Integration',
                'type': 'integration',
                'language': 'en'
            }
        },
        {
            'content': """
            Los workflows en n8n son secuencias de nodos que procesan datos paso a paso.
            Mejores prácticas:
            - Usar nombres descriptivos para nodos
            - Implementar manejo de errores
            - Documentar workflows complejos
            - Testear con datos reales
            - Usar variables de entorno para configuraciones
            
            Estructura típica:
            1. Trigger (webhook, cron, manual)
            2. Procesamiento de datos
            3. Acciones (envío emails, APIs, bases de datos)
            4. Notificaciones de resultado
            """,
            'metadata': {
                'source': 'Mejores Prácticas N8N ES',
                'heading': 'Diseño de Workflows',
                'type': 'best-practices',
                'language': 'es'
            }
        }
    ]
    
    # Add documents to collection
    documents = [doc['content'] for doc in test_documents]
    metadatas = [doc['metadata'] for doc in test_documents]
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Base de conocimiento de prueba creada con {len(documents)} documentos")
    return client

def test_multilingual_queries():
    """Test the multilingual query system"""
    
    print("🧪 INICIANDO PRUEBAS MULTIIDIOMA")
    print("="*60)
    
    # Populate test knowledge base
    populate_test_knowledge_base()
    
    # Initialize copilot with test database
    try:
        copilot = EnhancedCopilot(db_path="./test_knowledge_base")
        print("✅ Copilot inicializado con base de datos de prueba")
    except Exception as e:
        print(f"❌ Error inicializando copilot: {e}")
        return
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Usuario español pregunta sobre webhooks',
            'user_language': 'es',
            'query': '¿Cómo configurar un webhook en n8n?',
            'expected': 'Debería encontrar info en español e inglés, responder en español'
        },
        {
            'name': 'Usuario inglés pregunta sobre WhatsApp',
            'user_language': 'en',
            'query': 'How do I integrate WhatsApp Business with n8n?',
            'expected': 'Should find info in both languages, respond in English'
        },
        {
            'name': 'Usuario español pregunta sobre tema con más info en inglés',
            'user_language': 'es',
            'query': '¿Cuáles son las mejores prácticas para workflows?',
            'expected': 'Debería traducir info del inglés al español automáticamente'
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 ESCENARIO {i}: {scenario['name']}")
        print(f"   Idioma usuario: {scenario['user_language']}")
        print(f"   Pregunta: {scenario['query']}")
        print(f"   Resultado esperado: {scenario['expected']}")
        
        # Set user context
        copilot.set_user_context(language=scenario['user_language'])
        
        # Test document retrieval
        print("\n   🔍 Probando recuperación de documentos...")
        doc_results = copilot.get_relevant_context(scenario['query'])
        
        if doc_results['documents'][0]:
            print(f"   ✅ Encontrados {len(doc_results['documents'][0])} documentos relevantes")
            
            # Show language distribution
            languages = []
            for metadata in doc_results['metadatas'][0]:
                languages.append(metadata.get('language', 'unknown'))
            
            lang_count = {}
            for lang in languages:
                lang_count[lang] = lang_count.get(lang, 0) + 1
            
            print(f"   📊 Distribución por idioma: {lang_count}")
            
            # Test mixed language detection
            mixed_langs = copilot._detect_mixed_languages(doc_results)
            if len(mixed_langs) > 1:
                print(f"   🔄 Idiomas mixtos detectados: {mixed_langs}")
                instructions = copilot._get_translation_instructions(mixed_langs)
                print(f"   📋 Instrucciones de traducción generadas: {'Sí' if instructions else 'No'}")
            
        else:
            print("   ❌ No se encontraron documentos relevantes")
        
        print("   " + "-"*50)
        
        # Simulate full response (would call generate_response with actual API)
        print("   💭 Respuesta simulada: [Sistema procesaría y traduciría automáticamente]")
        print("   " + "="*60)
    
    print(f"\n🎉 PRUEBAS COMPLETADAS")
    print("💡 Para probar con API real, configura GOOGLE_API_KEY y ejecuta generate_response()")

def clean_up_test_data():
    """Clean up test database"""
    import shutil
    try:
        shutil.rmtree("./test_knowledge_base")
        print("🧹 Datos de prueba limpiados")
    except:
        pass

if __name__ == "__main__":
    try:
        test_multilingual_queries()
        
        # Ask if user wants to keep test data
        response = input("\n¿Mantener datos de prueba? (y/N): ").strip().lower()
        if response != 'y':
            clean_up_test_data()
            
    except KeyboardInterrupt:
        print("\n👋 Prueba interrumpida")
        clean_up_test_data()
    except Exception as e:
        print(f"\n❌ Error en pruebas: {e}")
        clean_up_test_data()
