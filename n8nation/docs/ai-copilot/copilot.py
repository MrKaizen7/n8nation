
import os
import chromadb
import google.generativeai as genai
from typing import Dict, List, Any, Optional

# --- Configuration ---
CHROMA_PATH = "knowledge_base_db"
COLLECTION_NAME = "n8nation_docs"
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-1.5-pro"
API_KEY_ENV_VAR = "GOOGLE_API_KEY"

# --- Helper Functions ---
def get_google_api_key():
    """Gets the Google API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set. Please set it to your Google API key.")
    return api_key

def format_context(results: Dict, user_language: str = 'es') -> str:
    """Formats the retrieved documents into a string for the prompt with language awareness."""
    if not results['documents'][0]:
        return "No se encontró documentación relevante en la base de conocimiento."
    
    context = "\n=== CONTEXTO DE DOCUMENTACIÓN RELEVANTE ===\n"
    
    for i, doc in enumerate(results['documents'][0]):
        metadata = results['metadatas'][0][i]
        source = metadata.get('source', 'Desconocido')
        heading = metadata.get('heading', 'Sin título')
        doc_type = metadata.get('type', 'general')
        doc_lang = metadata.get('language', 'unknown')
        
        # Add language indicator if different from user's preference
        lang_indicator = ""
        if doc_lang != user_language and doc_lang != 'unknown':
            lang_indicators = {
                'en': '🇺🇸 (English content)',
                'es': '🇪🇸 (Contenido en español)',
            }
            lang_indicator = f" {lang_indicators.get(doc_lang, f'({doc_lang})')}"
        
        context += f"\n📄 Fuente {i+1}: {source}{lang_indicator}\n"
        context += f"   Sección: {heading}\n"
        context += f"   Tipo: {doc_type}\n"
        
        # Truncate very long content
        doc_content = doc[:800] if len(doc) <= 800 else doc[:800] + "..."
        context += f"   Contenido: {doc_content}\n"
        context += "   " + "="*50 + "\n"
    
    return context

def get_system_prompt(user_language: str = 'es') -> str:
    """Get system prompt based on user language"""
    if user_language == 'en':
        return """
You are N8Nation Assistant, an expert in n8n automation and enterprise integrations consultant.

RESPONSE INSTRUCTIONS:
1. ALWAYS respond in English
2. If context is in Spanish, automatically translate the information to English
3. Be precise, professional, and solution-oriented
4. Include code examples when relevant
5. If you don't have sufficient information, acknowledge it honestly
6. Maintain consistency with previous conversations

SPECIALTIES:
- Business process automation with n8n
- API integrations and web services
- Complex workflows design
- Webhooks and automatic triggers
- Automation best practices

CONTEXT HANDLING:
- Use ALL available information regardless of original language
- Translate content accurately while maintaining technical precision
- Indicate when you're translating from other languages
"""
    else:
        return """
Eres N8Nation Assistant, un experto en automatización con n8n y consultor en integraciones empresariales.

INSTRUCCIONES DE RESPUESTA:
1. SIEMPRE responde en español
2. Si el contexto está en inglés, traduce automáticamente la información al español
3. Sé preciso, profesional y orientado a soluciones prácticas
4. Incluye ejemplos de código cuando sea relevante
5. Si no tienes información suficiente, reconócelo honestamente
6. Mantén coherencia con conversaciones anteriores

ESPECIALIDADES:
- Automatización de procesos empresariales con n8n
- Integraciones de APIs y servicios web
- Diseño de flujos de trabajo complejos
- Webhooks y triggers automáticos
- Mejores prácticas en automatización

MANEJO DE CONTEXTO:
- Usa TODA la información disponible independientemente del idioma original
- Traduce el contenido con precisión manteniendo la exactitud técnica
- Indica cuando estés traduciendo de otros idiomas
"""

def create_enhanced_prompt(query: str, context: str, user_language: str = 'es') -> str:
    """Create an enhanced prompt with translation instructions"""
    system_prompt = get_system_prompt(user_language)
    
    # Check if context contains mixed languages
    has_english = '🇺🇸' in context
    has_spanish = '🇪🇸' in context
    
    translation_instruction = ""
    if has_english and has_spanish:
        if user_language == 'es':
            translation_instruction = "\n🔄 TRADUCCIÓN AUTOMÁTICA: Se detectó contenido en múltiples idiomas. Traduce automáticamente cualquier información en inglés al español manteniendo la precisión técnica."
        else:
            translation_instruction = "\n🔄 AUTOMATIC TRANSLATION: Mixed language content detected. Automatically translate any Spanish information to English while maintaining technical accuracy."
    
    return f"""{system_prompt}

{translation_instruction}

{context}

PREGUNTA DEL USUARIO: {query}

Responde de manera útil y precisa usando TODA la información disponible. Si la información está incompleta, combina fuentes de ambos idiomas para dar la respuesta más completa posible."""

# --- Main Application Logic ---
def main():
    """Main function to run the interactive N8Nation Copilot."""
    print("🚀 N8NATION COPILOT")
    print("=" * 50)
    print("Tu asistente experto en automatización con n8n")
    print()
    print("Comandos especiales:")
    print("  /lang es|en  - Cambiar idioma")
    print("  /help        - Mostrar ayuda")
    print("  /quit        - Salir")
    print()
    
    # 1. Configure Google AI API
    try:
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        print("✅ Google AI API configurada")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Configura tu API key: export GOOGLE_API_KEY='tu-key'")
        return

    # 2. Initialize ChromaDB Client
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"✅ Conectado a la base de conocimiento: '{COLLECTION_NAME}'")
    except Exception as e:
        print(f"❌ Error conectando a ChromaDB: {e}")
        print("💡 Ejecuta primero embed_and_store.py para crear la base de conocimiento")
        return

    # 3. Initialize Generative Model
    model = genai.GenerativeModel(GENERATION_MODEL)
    print(f"✅ Modelo AI listo: {GENERATION_MODEL}")
    
    # User settings
    user_language = 'es'
    
    print(f"\n💬 ¡Listo! Pregúntame sobre n8n en {user_language}")
    print("Type 'quit' or 'exit' to stop.")

    # 4. Interactive Q&A Loop
    while True:
        try:
            query = input(f"\n[{user_language}] Pregunta: ").strip()
            
            if query.lower() in ['quit', 'exit', 'salir']:
                print("👋 ¡Hasta luego!")
                break
                
            if not query:
                continue
            
            # Handle special commands
            if query.startswith('/'):
                if query.startswith('/lang '):
                    new_lang = query.split()[1].lower()
                    if new_lang in ['es', 'en']:
                        user_language = new_lang
                        lang_name = 'español' if new_lang == 'es' else 'English'
                        print(f"✅ Idioma cambiado a: {lang_name}")
                    else:
                        print("❌ Idiomas disponibles: es, en")
                elif query == '/help':
                    print("\n📚 COMANDOS DISPONIBLES:")
                    print("  /lang es|en  - Cambiar idioma de respuesta")
                    print("  /help        - Mostrar esta ayuda")
                    print("  /quit        - Salir del copilot")
                    print("\n💡 TIPS:")
                    print("  - Pregunta sobre webhooks, integraciones, workflows")
                    print("  - Solicita ejemplos de código específicos")
                    print("  - El sistema busca en contenido multiidioma automáticamente")
                else:
                    print("❌ Comando no reconocido. Usa /help para ver comandos disponibles")
                continue

            # Embed the user's query
            print("🔍 Buscando información relevante...")
            try:
                query_embedding = genai.embed_content(
                    model=EMBEDDING_MODEL, 
                    content=query, 
                    task_type="RETRIEVAL_QUERY"
                )['embedding']
            except Exception as e:
                print(f"❌ Error generando embedding: {e}")
                continue

            # Query ChromaDB for relevant documents
            try:
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=6,  # Get more results for better context
                    include=["documents", "metadatas"]
                )
            except Exception as e:
                print(f"❌ Error consultando base de conocimiento: {e}")
                continue

            if not results['documents'][0]:
                print("⚠️ No se encontró información relevante en la base de conocimiento.")
                continue

            # Format the context and create the prompt
            context = format_context(results, user_language)
            full_prompt = create_enhanced_prompt(query, context, user_language)

            # Generate the answer
            print("🤖 Generando respuesta...")
            try:
                response = model.generate_content(full_prompt)
                
                # Print the results
                print(f"\n{'='*60}")
                print("📝 RESPUESTA:")
                print(response.text)
                print(f"{'='*60}")
                
                # Show sources used
                sources = list(set([metadata.get('source', 'Unknown') for metadata in results['metadatas'][0]]))
                if sources:
                    print(f"\n📚 Fuentes consultadas: {len(sources)} documentos")
                    for i, source in enumerate(sources[:3], 1):  # Show max 3 sources
                        print(f"   {i}. {source}")
                    if len(sources) > 3:
                        print(f"   ... y {len(sources) - 3} más")
                        
            except Exception as e:
                print(f"❌ Error generando respuesta: {e}")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("💡 Intenta reformular tu pregunta")

if __name__ == '__main__':
    main()
