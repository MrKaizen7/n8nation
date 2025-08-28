import json
import re
import os
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional

def detect_content_language(content: str) -> str:
    """Detect language of content using simple heuristics"""
    # Spanish indicators
    spanish_words = ['qué', 'cómo', 'para', 'con', 'configurar', 'webhook', 'flujo', 'automatización', 'integración']
    # English indicators  
    english_words = ['what', 'how', 'the', 'and', 'configure', 'workflow', 'automation', 'integration']
    
    content_lower = content.lower()
    spanish_count = sum(1 for word in spanish_words if word in content_lower)
    english_count = sum(1 for word in english_words if word in content_lower)
    
    if spanish_count > english_count:
        return 'es'
    elif english_count > spanish_count:
        return 'en'
    else:
        return 'unknown'

def classify_document_type(file_path: str, content: str) -> str:
    """Classify document type based on path and content"""
    path_lower = file_path.lower()
    content_sample = content[:300].lower()
    
    # Check by path patterns
    if 'webhook' in path_lower:
        return 'webhook'
    elif 'api' in path_lower or 'integration' in path_lower:
        return 'integration'  
    elif 'workflow' in path_lower or 'flujo' in path_lower:
        return 'workflow'
    elif 'tutorial' in path_lower or 'guia' in path_lower:
        return 'tutorial'
    elif 'example' in path_lower or 'ejemplo' in path_lower:
        return 'example'
    elif 'readme' in path_lower:
        return 'overview'
    # Check by content patterns
    elif any(word in content_sample for word in ['tutorial', 'step', 'paso']):
        return 'tutorial'
    elif any(word in content_sample for word in ['example', 'ejemplo', 'demo']):
        return 'example'
    elif any(word in content_sample for word in ['api', 'endpoint', 'request']):
        return 'integration'
    else:
        return 'general'

def clean_content(content: str) -> str:
    """Clean and normalize content"""
    # Remove excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    # Remove markdown image syntax but keep alt text
    content = re.sub(r'!\[([^\]]*)\]\([^\)]*\)', r'\1', content)
    # Clean up code blocks markers but keep content
    content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Normalize whitespace
    content = re.sub(r'[ \t]+', ' ', content)
    return content.strip()

def is_content_substantial(content: str) -> bool:
    """Check if content is substantial enough to be useful"""
    # Remove whitespace and count actual content
    clean = re.sub(r'\s+', ' ', content.strip())
    words = clean.split()
    
    # Must have at least 20 words and 100 characters
    return len(words) >= 20 and len(clean) >= 100

def process_markdown_files(base_paths: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Process markdown files from multiple base paths, splitting them into chunks based on headings,
    and return structured data with enhanced metadata.
    """
    if base_paths is None:
        # Default paths to search
        base_paths = [
            'knowledge-base',
            'docs', 
            '../docs',
            '../../docs'
        ]
    
    all_chunks = []
    total_files_processed = 0
    
    # Regex to find markdown headings (H1, H2, H3, H4)
    heading_pattern = re.compile(r"^(#{1,4})\s+(.+)", re.MULTILINE)
    
    print("🔍 PROCESANDO ARCHIVOS MARKDOWN")
    print("=" * 50)
    
    for base_path in base_paths:
        if not os.path.exists(base_path):
            print(f"⚠️ Ruta no encontrada: {base_path}")
            continue
            
        print(f"\n📂 Buscando en: {base_path}")
        
        # Find all markdown files recursively
        pattern = os.path.join(base_path, '**', '*.md')
        file_paths = glob.glob(pattern, recursive=True)
        
        if not file_paths:
            print(f"   ❌ No se encontraron archivos .md en {base_path}")
            continue
            
        print(f"   ✅ Encontrados {len(file_paths)} archivos .md")
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    print(f"   ⚠️ Archivo vacío: {file_path}")
                    continue

                # Clean the content
                content = clean_content(content)
                
                # Detect language and type
                language = detect_content_language(content)
                doc_type = classify_document_type(file_path, content)
                
                # Normalize file path
                normalized_path = file_path.replace('\\', '/').replace('../', '')
                
                # Find all headings
                headings = list(heading_pattern.finditer(content))
                
                if not headings:
                    # If no headings, treat the whole file as one chunk
                    if is_content_substantial(content):
                        all_chunks.append({
                            "source": normalized_path,
                            "heading": Path(file_path).stem.replace('-', ' ').title(),
                            "content": content,
                            "language": language,
                            "type": doc_type,
                            "word_count": len(content.split()),
                            "char_count": len(content)
                        })
                    continue

                # Process content with headings
                # First chunk: content before the first heading (if substantial)
                first_heading_start = headings[0].start()
                if first_heading_start > 0:
                    intro_content = content[:first_heading_start].strip()
                    if is_content_substantial(intro_content):
                        all_chunks.append({
                            "source": normalized_path,
                            "heading": f"{Path(file_path).stem.replace('-', ' ').title()} - Introducción",
                            "content": intro_content,
                            "language": detect_content_language(intro_content),
                            "type": doc_type,
                            "word_count": len(intro_content.split()),
                            "char_count": len(intro_content)
                        })

                # Process each heading section
                for i, match in enumerate(headings):
                    start_pos = match.end()
                    end_pos = headings[i + 1].start() if i + 1 < len(headings) else len(content)
                    
                    heading_level = match.group(1)  # The # symbols
                    heading_text = match.group(2).strip()
                    chunk_content = content[start_pos:end_pos].strip()

                    if is_content_substantial(chunk_content):
                        chunk_language = detect_content_language(chunk_content)
                        all_chunks.append({
                            "source": normalized_path,
                            "heading": heading_text,
                            "content": chunk_content,
                            "language": chunk_language,
                            "type": doc_type,
                            "heading_level": len(heading_level),
                            "word_count": len(chunk_content.split()),
                            "char_count": len(chunk_content)
                        })

                total_files_processed += 1
                
            except Exception as e:
                print(f"   ❌ Error procesando {file_path}: {e}")

    # Statistics
    print(f"\n📊 ESTADÍSTICAS DE PROCESAMIENTO:")
    print(f"   Archivos procesados: {total_files_processed}")
    print(f"   Chunks creados: {len(all_chunks)}")
    
    if all_chunks:
        # Language distribution
        languages = {}
        types = {}
        for chunk in all_chunks:
            lang = chunk.get('language', 'unknown')
            chunk_type = chunk.get('type', 'general')
            languages[lang] = languages.get(lang, 0) + 1
            types[chunk_type] = types.get(chunk_type, 0) + 1
        
        print(f"   Distribución por idioma: {languages}")
        print(f"   Distribución por tipo: {types}")
        
        # Word count statistics
        word_counts = [chunk['word_count'] for chunk in all_chunks]
        avg_words = sum(word_counts) / len(word_counts)
        print(f"   Promedio de palabras por chunk: {avg_words:.1f}")
        print(f"   Total de palabras: {sum(word_counts):,}")

    return all_chunks

def save_processed_docs(chunks: List[Dict[str, Any]], filename: str = 'processed_docs.json'):
    """Save processed chunks to JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Documentos guardados en: {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Error guardando documentos: {e}")
        return False

def main():
    """Main function to process markdown files"""
    print("🚀 INICIANDO PROCESAMIENTO DE DOCUMENTOS")
    print("=" * 60)
    
    # Define search paths - you can customize these
    search_paths = [
        'knowledge-base',  # Our main knowledge base
        'docs',           # Local docs if any
        '../docs',        # Parent directory docs
        '.',              # Current directory
    ]
    
    # Process all markdown files
    chunks = process_markdown_files(search_paths)
    
    if not chunks:
        print("\n❌ No se encontraron chunks válidos para procesar")
        print("💡 Verifica que existan archivos .md en las rutas especificadas")
        return
    
    # Save processed data
    success = save_processed_docs(chunks)
    
    if success:
        print(f"\n🎉 PROCESAMIENTO COMPLETADO")
        print(f"   {len(chunks)} chunks listos para embedding")
        print(f"   Siguiente paso: ejecutar ai-copilot/embed_and_store.py")
    else:
        print(f"\n❌ PROCESAMIENTO FALLÓ")

if __name__ == "__main__":
    main()