"""
Configuración centralizada para N8Nation AI Copilot
"""

import os
from pathlib import Path

# === PATHS AND DIRECTORIES ===
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge-base"
CHROMA_DB_PATH = "knowledge_base_db"
PROCESSED_DOCS_FILE = "processed_docs.json"

# === CHROMADB CONFIGURATION ===
COLLECTION_NAME = "n8nation_docs"
BATCH_SIZE = 50  # For embedding processing
MAX_RESULTS = 6  # For similarity search

# === GOOGLE AI CONFIGURATION ===
API_KEY_ENV_VAR = "GOOGLE_API_KEY"
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-1.5-pro"

# === LANGUAGE SETTINGS ===
SUPPORTED_LANGUAGES = ['es', 'en']
DEFAULT_LANGUAGE = 'es'

# === CONTENT PROCESSING ===
MIN_CHUNK_WORDS = 20
MIN_CHUNK_CHARS = 100
MAX_CONTENT_DISPLAY = 800

# === SEARCH PATHS FOR DOCS ===
DEFAULT_SEARCH_PATHS = [
    'knowledge-base',
    'docs',
    '../docs',
    '.',
]

# === LANGUAGE INDICATORS ===
LANGUAGE_INDICATORS = {
    'es': '🇪🇸',
    'en': '🇺🇸',
    'pt': '🇵🇹',
    'fr': '🇫🇷'
}

# === CONTENT TYPE CLASSIFICATIONS ===
CONTENT_TYPES = {
    'webhook': 'webhook',
    'integration': 'integration',
    'workflow': 'workflow',
    'tutorial': 'tutorial',
    'example': 'example',
    'overview': 'overview',
    'general': 'general'
}

# === UTILITY FUNCTIONS ===
def get_api_key() -> str:
    """Get Google API key from environment variables"""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"Environment variable {API_KEY_ENV_VAR} not set. Please set it to your Google API key.")
    return api_key

def ensure_directories():
    """Ensure required directories exist"""
    BASE_DIR.mkdir(exist_ok=True)
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    return True

# === VALIDATION ===
def validate_language(language: str) -> str:
    """Validate and return language code"""
    if language.lower() in SUPPORTED_LANGUAGES:
        return language.lower()
    return DEFAULT_LANGUAGE

# === STATUS MESSAGES ===
MESSAGES = {
    'es': {
        'welcome': '🚀 N8NATION COPILOT - Tu asistente experto en automatización con n8n',
        'ready': '✅ Sistema listo. ¡Pregúntame sobre n8n!',
        'thinking': '🤖 Procesando tu consulta...',
        'searching': '🔍 Buscando información relevante...',
        'no_results': '⚠️ No se encontró información relevante.',
        'error': '❌ Error:',
        'goodbye': '👋 ¡Hasta luego!',
        'sources': '📚 Fuentes consultadas:'
    },
    'en': {
        'welcome': '🚀 N8NATION COPILOT - Your expert n8n automation assistant',
        'ready': '✅ System ready. Ask me about n8n!',
        'thinking': '🤖 Processing your query...',
        'searching': '🔍 Searching for relevant information...',
        'no_results': '⚠️ No relevant information found.',
        'error': '❌ Error:',
        'goodbye': '👋 Goodbye!',
        'sources': '📚 Sources consulted:'
    }
}

def get_message(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Get localized message"""
    return MESSAGES.get(language, MESSAGES[DEFAULT_LANGUAGE]).get(key, key)
