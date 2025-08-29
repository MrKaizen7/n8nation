#!/usr/bin/env python3
"""
n8nation Enhanced AI Copilot
- Memoria conversacional #no testeado
- Prompt engineering especializado #no testeado
- Configuración RAG mejorada #no testeado
- Multi-idioma (español/inglés)
"""

import os
import json
import chromadb
import google.generativeai as genai
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# --- Configuration ---
CHROMA_PATH = "../../../n8n_chroma_db"  # Relativo a n8nation/
COLLECTION_NAME = "n8nation_knowledge"
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-1.5-pro"  # Pro para mejor razonamiento
API_KEY_ENV_VAR = "GOOGLE_API_KEY"

# --- Data Classes ---
@dataclass
class ConversationMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    sources: Optional[List[str]] = None

@dataclass
class UserContext:
    language: str = "es"  # 'es' or 'en'
    expertise_level: str = "intermediate"  # 'beginner', 'intermediate', 'advanced'
    current_project: Optional[str] = None
    preferred_examples: str = "latin_america"  # Para contextualizar ejemplos

class EnhancedCopilot:
    def __init__(self):
        self.conversation_history: List[ConversationMessage] = []
        self.user_context = UserContext()
        self.max_history_length = 10  # Mantener últimas 10 interacciones
        self.setup_ai()
        self.setup_chromadb()
    
    def setup_ai(self):
        """Configure Google AI API"""
        api_key = os.getenv(API_KEY_ENV_VAR)
        if not api_key:
            raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            GENERATION_MODEL,
            generation_config={
                "temperature": 0.7,  # Algo de creatividad, no mucha
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        print("✅ Google AI configurado")
    
    def setup_chromadb(self):
        """Initialize ChromaDB connection"""
        try:
            self.client = chromadb.PersistentClient(path=CHROMA_PATH)
            self.collection = self.client.get_collection(name=COLLECTION_NAME)
            print(f"✅ Conectado a ChromaDB: '{COLLECTION_NAME}'")
        except Exception as e:
            print(f"❌ Error conectando a ChromaDB: {e}")
            print("💡 Ejecuta primero process_enhanced_docs.py para crear la base de conocimiento")
            raise
    
    def get_relevant_context(self, query: str, n_results: int = 5) -> Dict:
        """Retrieve relevant documents with improved scoring and multi-language support"""
        
        # Generate embedding for the query
        query_embedding = genai.embed_content(
            model=EMBEDDING_MODEL, 
            content=query, 
            task_type="RETRIEVAL_QUERY"
        )['embedding']
        
        # Strategy 1: Search in user's preferred language first
        preferred_lang = self.user_context.language
        
        # Try to get results from preferred language
        preferred_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"language": preferred_lang}
        )
        
        # If we don't have enough results, search in other languages
        if len(preferred_results['documents'][0]) < n_results:
            remaining_needed = n_results - len(preferred_results['documents'][0])
            
            # Search in all languages
            all_results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results + remaining_needed,  # Get extra to filter out duplicates
                # No language filter
            )
            
            # Combine results, prioritizing preferred language
            combined_results = {
                'documents': [[]],
                'metadatas': [[]],
                'ids': [[]],
                'distances': [[]]
            }
            
            # Add preferred language results first
            for i in range(len(preferred_results['documents'][0])):
                combined_results['documents'][0].append(preferred_results['documents'][0][i])
                combined_results['metadatas'][0].append(preferred_results['metadatas'][0][i])
                combined_results['ids'][0].append(preferred_results['ids'][0][i])
                combined_results['distances'][0].append(preferred_results['distances'][0][i])
            
            # Add other language results (avoiding duplicates)
            added_ids = set(preferred_results['ids'][0])
            added_count = 0
            
            for i in range(len(all_results['documents'][0])):
                if (added_count < remaining_needed and 
                    all_results['ids'][0][i] not in added_ids):
                    
                    combined_results['documents'][0].append(all_results['documents'][0][i])
                    combined_results['metadatas'][0].append(all_results['metadatas'][0][i])
                    combined_results['ids'][0].append(all_results['ids'][0][i])
                    combined_results['distances'][0].append(all_results['distances'][0][i])
                    
                    added_ids.add(all_results['ids'][0][i])
                    added_count += 1
            
            return combined_results
        
        return preferred_results
    
    def format_context_for_prompt(self, results: Dict) -> str:
        """Format retrieved context for the prompt with smart translation"""
        if not results['documents'][0]:
            return "No se encontró documentación relevante en la base de conocimiento."
        
        context = "\n=== CONTEXTO DE DOCUMENTACIÓN RELEVANTE ===\n"
        
        user_lang = self.user_context.language
        
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            source = metadata.get('source', 'Desconocido')
            heading = metadata.get('heading', 'Sin título')
            doc_type = metadata.get('type', 'general')
            doc_lang = metadata.get('language', 'unknown')
            
            # Smart content handling based on languages
            display_content = doc[:500] if len(doc) <= 500 else doc[:500] + "..."
            
            # Add language indicator if different from user's preference
            lang_indicator = ""
            if doc_lang != user_lang and doc_lang != 'unknown':
                lang_indicators = {
                    'en': '🇺🇸 (Contenido en inglés)',
                    'es': '🇪🇸 (Content in Spanish)',
                }
                lang_indicator = f" {lang_indicators.get(doc_lang, f'({doc_lang})')}"
            
            context += f"\n📄 Fuente {i+1}: {source}{lang_indicator}\n"
            context += f"   Sección: {heading}\n"
            context += f"   Tipo: {doc_type}\n"
            context += f"   Contenido: {display_content}\n"
            context += "   " + "="*50 + "\n"
        
        # Add translation instruction if mixed languages found
        doc_languages = set(metadata.get('language', 'unknown') for metadata in results['metadatas'][0])
        if len(doc_languages) > 1 and user_lang in doc_languages:
            translation_note = {
                'es': "\n💡 INSTRUCCIÓN: Si encuentras contenido en inglés que sea relevante, tradúcelo automáticamente al español en tu respuesta.",
                'en': "\n💡 INSTRUCTION: If you find relevant content in Spanish, automatically translate it to English in your response."
            }
            context += translation_note.get(user_lang, "")
        
        return context
    
    def get_conversation_context(self) -> str:
        """Get recent conversation history for context"""
        if not self.conversation_history:
            return ""
        
        context = "\n=== HISTORIAL DE CONVERSACIÓN RECIENTE ===\n"
        
        # Get last few messages for context
        recent_messages = self.conversation_history[-6:]  # Últimos 3 intercambios
        
        for msg in recent_messages:
            role_emoji = "👤" if msg.role == "user" else "🤖"
            context += f"{role_emoji} {msg.role.capitalize()}: {msg.content[:200]}{'...' if len(msg.content) > 200 else ''}\n"
        
        context += "=" * 50 + "\n"
        return context
    
    def create_system_prompt(self) -> str:
        """Create specialized system prompt for n8nation"""
        
        language_instructions = {
            "es": {
                "identity": "Eres el asistente de IA especializado de n8nation, la comunidad colaborativa de automatización en español.",
                "expertise": "Tienes profundo conocimiento en n8n, automatización de procesos, y integración de APIs populares en Latinoamérica.",
                "style": "Responde en español de manera clara y práctica, con ejemplos específicos para el mercado hispanohablante.",
                "examples": "Usa ejemplos con herramientas como WhatsApp Business, Mercado Pago, bancos latinos, CRMs locales, etc."
            },
            "en": {
                "identity": "You are n8nation's specialized AI assistant, from the collaborative automation community in Spanish.",
                "expertise": "You have deep knowledge in n8n, process automation, and integration of popular APIs in Latin America.",
                "style": "Respond in English clearly and practically, with specific examples for the Spanish-speaking market.",
                "examples": "Use examples with tools like WhatsApp Business, Mercado Pago, Latin banks, local CRMs, etc."
            }
        }
        
        lang_config = language_instructions[self.user_context.language]
        
        return f"""
{lang_config['identity']}

EXPERTISE:
{lang_config['expertise']}

ESTILO DE RESPUESTA:
{lang_config['style']}

EJEMPLOS CONTEXTUALES:
{lang_config['examples']}

NIVEL DE USUARIO ACTUAL: {self.user_context.expertise_level}

INSTRUCCIONES ESPECÍFICAS:
- Si hablan de integraciones, considera herramientas populares en LATAM
- Para casos de uso, piensa en negocios típicos hispanohablantes
- Si mencionan pagos, considera Mercado Pago, transferencias locales, etc.
- Para WhatsApp, recuerda que WhatsApp Business API es popular en LATAM
- Siempre proporciona ejemplos prácticos y accionables

FORMATO DE RESPUESTA:
1. Respuesta directa a la pregunta
2. Ejemplo práctico si es aplicable
3. Recursos adicionales o pasos siguientes
4. Fuentes utilizadas (si las hay)
"""
    
    def get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        lang_names = {
            'es': 'español',
            'en': 'inglés',
            'pt': 'portugués',
            'fr': 'francés'
        }
        return lang_names.get(lang_code, lang_code)
    
    def _detect_mixed_languages(self, doc_results: Dict) -> List[str]:
        """Detect if results contain mixed languages"""
        if not doc_results['metadatas'][0]:
            return []
        
        languages = set()
        for metadata in doc_results['metadatas'][0]:
            lang = metadata.get('language', 'unknown')
            if lang != 'unknown':
                languages.add(lang)
        
        return list(languages)
    
    def _get_translation_instructions(self, languages: List[str]) -> str:
        """Generate translation instructions based on detected languages"""
        if len(languages) <= 1:
            return ""
        
        user_lang = self.user_context.language
        other_langs = [lang for lang in languages if lang != user_lang]
        
        if not other_langs:
            return ""
        
        lang_names = [self.get_language_name(lang) for lang in other_langs]
        
        return f"""
🔄 TRADUCCIÓN AUTOMÁTICA ACTIVADA:
Se detectó contenido en múltiples idiomas: {', '.join(lang_names)}.
INSTRUCCIÓN ESPECIAL: Traduce automáticamente cualquier información relevante al {self.get_language_name(user_lang)}.
Mantén la precisión técnica y menciona brevemente cuando estés traduciendo contenido de otro idioma.
"""

    def generate_response(self, query: str) -> str:
        """Generate AI response with enhanced context and intelligent translation"""
        
        # Get relevant documentation with multi-language search
        doc_results = self.get_relevant_context(query)
        doc_context = self.format_context_for_prompt(doc_results)
        
        # Get conversation history
        conversation_context = self.get_conversation_context()
        
        # Create comprehensive prompt
        system_prompt = self.create_system_prompt()
        
        # Detect if mixed languages are present in context
        mixed_languages = self._detect_mixed_languages(doc_results)
        translation_instructions = self._get_translation_instructions(mixed_languages)
        
        full_prompt = f"""
{system_prompt}

{translation_instructions}

{conversation_context}

{doc_context}

PREGUNTA ACTUAL DEL USUARIO:
{query}

INSTRUCCIONES DE RESPUESTA INTELIGENTE:
1. Si encuentras información relevante en cualquier idioma, úsala
2. Traduce automáticamente cualquier contenido que no esté en {self.get_language_name(self.user_context.language)}
3. Mantén la precisión técnica durante la traducción
4. Si la información está incompleta en un idioma, combina fuentes de ambos idiomas
5. Indica claramente cuando estés traduciendo contenido de otro idioma

Por favor, responde de manera útil y precisa usando TODA la información disponible, independientemente del idioma original. Si no tienes suficiente información en ningún idioma, dilo claramente y sugiere dónde encontrar más información.
"""
        
        # Generate response
        response = self.model.generate_content(full_prompt)
        
        # Store in conversation history
        self.add_to_history("user", query)
        sources = [doc_results['metadatas'][0][i].get('source', 'Unknown') 
                  for i in range(len(doc_results['documents'][0]))] if doc_results['documents'][0] else []
        self.add_to_history("assistant", response.text, sources)
        
        return response.text
    
    def add_to_history(self, role: str, content: str, sources: Optional[List[str]] = None):
        """Add message to conversation history"""
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            sources=sources
        )
        
        self.conversation_history.append(message)
        
        # Keep history manageable
        if len(self.conversation_history) > self.max_history_length * 2:  # *2 porque user + assistant
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def set_user_context(self, **kwargs):
        """Update user context"""
        for key, value in kwargs.items():
            if hasattr(self.user_context, key):
                setattr(self.user_context, key, value)
                print(f"✅ Contexto actualizado: {key} = {value}")
    
    def show_conversation_stats(self):
        """Show conversation statistics"""
        print(f"\n📊 ESTADÍSTICAS DE CONVERSACIÓN:")
        print(f"   Mensajes intercambiados: {len(self.conversation_history)}")
        print(f"   Idioma: {self.user_context.language}")
        print(f"   Nivel técnico: {self.user_context.expertise_level}")
        if self.user_context.current_project:
            print(f"   Proyecto actual: {self.user_context.current_project}")
    
    def demo_multilingual_query(self):
        """Demonstration of multilingual query functionality"""
        print("\n🌍 DEMOSTRACIÓN: Consulta Multiidioma")
        print("="*60)
        
        # Test queries in different scenarios
        test_queries = [
            {
                'query': '¿Cómo configurar un webhook en n8n?',
                'description': 'Pregunta en español sobre webhooks'
            },
            {
                'query': 'How to integrate with WhatsApp Business API?',
                'description': 'Pregunta en inglés sobre WhatsApp'
            },
            {
                'query': 'Como criar um workflow para processar pagamentos?',
                'description': 'Pregunta en portugués sobre workflows'
            }
        ]
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n🧪 Prueba {i}: {test['description']}")
            print(f"   Pregunta: {test['query']}")
            
            # Simulate response process
            print("   Procesando consulta multiidioma...")
            print("   ✅ Sistema detectaría idioma de consulta")
            print("   🔍 Buscaría en contenido de ambos idiomas")
            print("   🔄 Traduciría automáticamente si es necesario")
            print("   📝 Respondería en idioma del usuario")
            print("-" * 50)

    def interactive_session(self):
        """Main interactive session"""
        print("🚀 n8nation Enhanced Copilot")
        print("   Comandos especiales:")
        print("   - /lang es|en : Cambiar idioma")
        print("   - /level beginner|intermediate|advanced : Cambiar nivel técnico")
        print("   - /project <nombre> : Establecer proyecto actual")
        print("   - /stats : Ver estadísticas")
        print("   - /quit : Salir")
        print("\n💡 ¿En qué puedo ayudarte con automatización hoy?")
        
        while True:
            try:
                query = input(f"\n[{self.user_context.language}] Pregunta: ").strip()
                
                if not query:
                    continue
                
                # Handle special commands
                if query.startswith('/'):
                    if query == '/quit':
                        break
                    elif query.startswith('/lang '):
                        lang = query.split()[1]
                        if lang in ['es', 'en']:
                            self.set_user_context(language=lang)
                        else:
                            print("❌ Idiomas disponibles: es, en")
                    elif query.startswith('/level '):
                        level = query.split()[1]
                        if level in ['beginner', 'intermediate', 'advanced']:
                            self.set_user_context(expertise_level=level)
                        else:
                            print("❌ Niveles disponibles: beginner, intermediate, advanced")
                    elif query.startswith('/project '):
                        project = ' '.join(query.split()[1:])
                        self.set_user_context(current_project=project)
                    elif query == '/stats':
                        self.show_conversation_stats()
                    else:
                        print("❌ Comando no reconocido")
                    continue
                
                # Generate and show response
                print("\n🤔 Procesando...")
                response = self.generate_response(query)
                
                print("\n🤖 Respuesta:")
                print("=" * 60)
                print(response)
                print("=" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Intenta reformular tu pregunta")

def main():
    """Main function"""
    try:
        copilot = EnhancedCopilot()
        copilot.interactive_session()
    except Exception as e:
        print(f"❌ Error inicializando copilot: {e}")
        return 1
    return 0

if __name__ == '__main__':
    exit(main())