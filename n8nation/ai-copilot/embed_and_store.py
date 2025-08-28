
import json
import os
import chromadb
import google.generativeai as genai
import time
from pathlib import Path

# --- Configuration ---
CHROMA_PATH = "knowledge_base_db"
COLLECTION_NAME = "n8nation_docs"
JSON_FILE = "processed_docs.json"
EMBEDDING_MODEL = "models/text-embedding-004"
API_KEY_ENV_VAR = "GOOGLE_API_KEY"

# --- Helper Functions ---
def get_google_api_key():
    """Gets the Google API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set. Please set it to your Google API key.")
    return api_key

def embed_text_batch(texts, model):
    """Embeds a batch of texts using the Google AI API."""
    try:
        result = genai.embed_content(model=model, content=texts, task_type="RETRIEVAL_DOCUMENT")
        return result['embedding'] if isinstance(texts, str) else result['embedding']
    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        time.sleep(10)  # Wait before retrying or moving on
        return [[] for _ in texts] if isinstance(texts, list) else []

def detect_language(text):
    """Simple language detection based on content patterns"""
    # Simple heuristics - can be improved with proper language detection
    spanish_indicators = ['qué', 'cómo', 'para', 'con', 'configurar', 'webhook', 'flujo']
    english_indicators = ['what', 'how', 'the', 'and', 'configure', 'workflow', 'trigger']
    
    text_lower = text.lower()
    spanish_count = sum(1 for word in spanish_indicators if word in text_lower)
    english_count = sum(1 for word in english_indicators if word in text_lower)
    
    if spanish_count > english_count:
        return 'es'
    elif english_count > spanish_count:
        return 'en'
    else:
        return 'unknown'

def classify_content_type(source_path, heading, content):
    """Classify content type based on path and content"""
    source_lower = source_path.lower()
    heading_lower = heading.lower()
    content_lower = content[:500].lower()
    
    # Determine content type
    if 'webhook' in source_lower or 'webhook' in heading_lower:
        return 'webhook'
    elif 'api' in source_lower or 'integration' in source_lower:
        return 'integration'
    elif 'workflow' in source_lower or 'flujo' in source_lower:
        return 'workflow'
    elif 'tutorial' in source_lower or 'guia' in source_lower:
        return 'tutorial'
    elif 'example' in source_lower or 'ejemplo' in source_lower:
        return 'example'
    else:
        return 'general'

# --- Main Script Logic ---
def main():
    """Main function to read data, create embeddings, and store in ChromaDB."""
    print("🚀 INICIANDO PROCESO DE EMBEDDINGS Y ALMACENAMIENTO")
    print("=" * 60)

    # 1. Configure Google AI API
    try:
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        print("✅ Google AI API configurada correctamente")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Configura tu API key: export GOOGLE_API_KEY='tu-key'")
        return

    # 2. Load the processed documents
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        print(f"✅ Cargados {len(documents)} chunks de documentos desde {JSON_FILE}")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {JSON_FILE}")
        print("💡 Ejecuta primero process_docs.py para procesar los documentos")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: No se pudo decodificar el JSON desde {JSON_FILE}")
        return

    # 3. Initialize ChromaDB
    print(f"🗄️ Inicializando ChromaDB en: {CHROMA_PATH}")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Delete existing collection if it exists for fresh start
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"🗑️ Colección existente '{COLLECTION_NAME}' eliminada")
    except:
        pass
    
    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"✅ Colección ChromaDB '{COLLECTION_NAME}' lista")

    # 4. Process documents in batches
    batch_size = 50  # Reduced batch size for better error handling
    total_docs = len(documents)
    processed_count = 0
    failed_count = 0

    for i in range(0, total_docs, batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_texts = [doc['content'] for doc in batch_docs]
        
        print(f"\n📦 Procesando lote {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}")
        print(f"   Documentos {i+1}-{min(i+batch_size, total_docs)} de {total_docs}")

        # Generate embeddings for the batch
        print("   🔄 Generando embeddings...")
        embeddings = embed_text_batch(batch_texts, EMBEDDING_MODEL)

        # Prepare enhanced data for ChromaDB
        valid_data = []
        for j, (doc, embedding) in enumerate(zip(batch_docs, embeddings)):
            if embedding:  # Only process if embedding was successful
                # Detect language and classify content
                language = detect_language(doc['content'])
                content_type = classify_content_type(doc['source'], doc['heading'], doc['content'])
                
                valid_data.append({
                    'id': f"doc_{i+j}_{hash(doc['source'] + doc['heading'])}",
                    'embedding': embedding,
                    'content': doc['content'],
                    'metadata': {
                        'source': doc['source'],
                        'heading': doc['heading'],
                        'language': language,
                        'type': content_type,
                        'char_count': len(doc['content']),
                        'word_count': len(doc['content'].split())
                    }
                })

        if not valid_data:
            print("   ⚠️ Warning: Falló el embedding para todo el lote. Saltando...")
            failed_count += len(batch_docs)
            continue
        
        if len(valid_data) < len(batch_docs):
            failed_this_batch = len(batch_docs) - len(valid_data)
            print(f"   ⚠️ Fallaron {failed_this_batch} documentos en este lote")
            failed_count += failed_this_batch

        # 5. Add the batch to ChromaDB
        try:
            collection.add(
                ids=[item['id'] for item in valid_data],
                embeddings=[item['embedding'] for item in valid_data],
                metadatas=[item['metadata'] for item in valid_data],
                documents=[item['content'] for item in valid_data]
            )
            processed_count += len(valid_data)
            print(f"   ✅ Agregados {len(valid_data)} documentos a ChromaDB")
        except Exception as e:
            print(f"   ❌ Error agregando documentos a ChromaDB: {e}")
            failed_count += len(valid_data)

        # Small delay to be respectful to the API
        time.sleep(1)

    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN FINAL:")
    print(f"   Total documentos procesados exitosamente: {processed_count}")
    print(f"   Total documentos fallidos: {failed_count}")
    print(f"   Base de datos almacenada en: '{CHROMA_PATH}'")
    print(f"   Colección: '{COLLECTION_NAME}'")
    
    # Show some statistics
    if processed_count > 0:
        print(f"\n📈 ESTADÍSTICAS:")
        # Query some basic stats
        try:
            result = collection.get(limit=processed_count, include=['metadatas'])
            if result['metadatas']:
                # Language distribution
                languages = {}
                types = {}
                for metadata in result['metadatas']:
                    lang = metadata.get('language', 'unknown')
                    content_type = metadata.get('type', 'general')
                    languages[lang] = languages.get(lang, 0) + 1
                    types[content_type] = types.get(content_type, 0) + 1
                
                print(f"   Distribución por idioma: {languages}")
                print(f"   Distribución por tipo: {types}")
        except Exception as e:
            print(f"   ⚠️ No se pudieron obtener estadísticas: {e}")
    
    print(f"\n🎉 PROCESO COMPLETADO!")

if __name__ == '__main__':
    main()
