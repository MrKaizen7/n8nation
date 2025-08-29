#!/usr/bin/env python3
"""
n8nation Knowledge Base Updater
Sistema inteligente para mantener actualizada la base de conocimiento #no testeado
"""

import os
import json
import hashlib
import requests
import chromadb
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContentSource:
    """Represents a content source to be monitored"""
    name: str
    source_type: str  # 'api', 'file', 'url', 'community'
    url: str
    last_updated: datetime
    content_hash: str
    update_frequency: str  # 'daily', 'weekly', 'on_demand'
    is_active: bool = True
    metadata: Optional[Dict] = None

@dataclass
class ProcessedDocument:
    """Represents a processed document chunk"""
    id: str
    source: str
    title: str
    content: str
    content_type: str  # 'tutorial', 'reference', 'example', 'case_study'
    language: str
    complexity_level: str  # 'beginner', 'intermediate', 'advanced'
    tags: List[str]
    last_updated: datetime
    embedding: Optional[List[float]] = None

class KnowledgeUpdater:
    def __init__(self):
        self.chroma_path = "../../../n8n_chroma_db"
        self.collection_name = "n8nation_knowledge"
        self.sources_config_path = "sources_config.json"
        self.embedding_model = "models/text-embedding-004"
        
        self.setup_ai()
        self.setup_chromadb()
        self.load_sources_config()
    
    def setup_ai(self):
        """Configure Google AI API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        logger.info("✅ Google AI configurado")
    
    def setup_chromadb(self):
        """Initialize or connect to ChromaDB"""
        try:
            self.client = chromadb.PersistentClient(path=self.chroma_path)
            
            # Try to get existing collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                logger.info(f"✅ Conectado a colección existente: {self.collection_name}")
            except Exception:
                # Create new collection if it doesn't exist
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "n8nation knowledge base with enhanced metadata"}
                )
                logger.info(f"✅ Creada nueva colección: {self.collection_name}")
        
        except Exception as e:
            logger.error(f"❌ Error conectando a ChromaDB: {e}")
            raise
    
    def load_sources_config(self):
        """Load or create sources configuration"""
        if os.path.exists(self.sources_config_path):
            with open(self.sources_config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sources = [ContentSource(**source) for source in data]
            logger.info(f"✅ Cargadas {len(self.sources)} fuentes de contenido")
        else:
            self.sources = self.create_default_sources()
            self.save_sources_config()
            logger.info("✅ Creada configuración inicial de fuentes")
    
    def create_default_sources(self) -> List[ContentSource]:
        """Create default content sources"""
        now = datetime.now()
        
        default_sources = [
            ContentSource(
                name="n8n_official_nodes",
                source_type="api",
                url="https://api.n8n.io/api/nodes",
                last_updated=now,
                content_hash="",
                update_frequency="weekly",
                metadata={"priority": "high", "language": "en"}
            ),
            ContentSource(
                name="n8n_official_docs",
                source_type="api", 
                url="https://docs.n8n.io/sitemap.xml",
                last_updated=now,
                content_hash="",
                update_frequency="weekly",
                metadata={"priority": "high", "language": "en"}
            ),
            ContentSource(
                name="google_apis_docs",
                source_type="url",
                url="https://developers.google.com/apis-explorer",
                last_updated=now,
                content_hash="",
                update_frequency="weekly",
                metadata={"priority": "medium", "language": "en", "region": "global"}
            ),
            ContentSource(
                name="mercado_pago_api",
                source_type="url",
                url="https://www.mercadopago.com.mx/developers/es/docs",
                last_updated=now,
                content_hash="",
                update_frequency="weekly", 
                metadata={"priority": "high", "language": "es", "region": "latam"}
            ),
            ContentSource(
                name="n8nation_workflows",
                source_type="file",
                url="../knowledge-base/workflows-community/",
                last_updated=now,
                content_hash="",
                update_frequency="on_demand",
                metadata={"priority": "high", "language": "es", "source": "community"}
            ),
            ContentSource(
                name="n8nation_case_studies",
                source_type="file",
                url="../knowledge-base/casos-uso/",
                last_updated=now,
                content_hash="",
                update_frequency="on_demand",
                metadata={"priority": "high", "language": "es", "source": "original"}
            )
        ]
        
        return default_sources
    
    def save_sources_config(self):
        """Save sources configuration to file"""
        data = [asdict(source) for source in self.sources]
        
        # Convert datetime objects to strings for JSON serialization
        for source_data in data:
            source_data['last_updated'] = source_data['last_updated'].isoformat()
        
        with open(self.sources_config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def should_update_source(self, source: ContentSource) -> bool:
        """Determine if a source should be updated"""
        if not source.is_active:
            return False
        
        now = datetime.now()
        
        # Check update frequency
        if source.update_frequency == "daily":
            return (now - source.last_updated).days >= 1
        elif source.update_frequency == "weekly":
            return (now - source.last_updated).days >= 7
        elif source.update_frequency == "on_demand":
            # Check if content has changed
            return self.has_content_changed(source)
        
        return False
    
    def has_content_changed(self, source: ContentSource) -> bool:
        """Check if content has changed since last update"""
        try:
            if source.source_type == "file":
                # Check file modification time or hash
                path = Path(source.url)
                if path.exists():
                    if path.is_file():
                        # Single file
                        current_hash = self.get_file_hash(path)
                    else:
                        # Directory - hash all files
                        current_hash = self.get_directory_hash(path)
                    
                    return current_hash != source.content_hash
                return False
            
            elif source.source_type in ["api", "url"]:
                # Simple content check (could be more sophisticated)
                try:
                    response = requests.head(source.url, timeout=10)
                    # Use ETag or Last-Modified headers if available
                    etag = response.headers.get('ETag', '')
                    last_modified = response.headers.get('Last-Modified', '')
                    current_hash = hashlib.md5((etag + last_modified).encode()).hexdigest()
                    
                    return current_hash != source.content_hash
                except:
                    return False
                    
        except Exception as e:
            logger.warning(f"⚠️ Error checking content change for {source.name}: {e}")
            return False
        
        return False
    
    def get_file_hash(self, file_path: Path) -> str:
        """Get hash of a single file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return ""
    
    def get_directory_hash(self, dir_path: Path) -> str:
        """Get combined hash of all files in directory"""
        hash_md5 = hashlib.md5()
        try:
            for file_path in sorted(dir_path.rglob("*")):
                if file_path.is_file():
                    hash_md5.update(str(file_path).encode())
                    hash_md5.update(str(file_path.stat().st_mtime).encode())
            return hash_md5.hexdigest()
        except:
            return ""
    
    def fetch_content(self, source: ContentSource) -> List[ProcessedDocument]:
        """Fetch and process content from a source"""
        logger.info(f"📥 Fetching content from {source.name}...")
        
        try:
            if source.source_type == "api":
                return self.fetch_api_content(source)
            elif source.source_type == "url":
                return self.fetch_url_content(source)
            elif source.source_type == "file":
                return self.fetch_file_content(source)
            else:
                logger.warning(f"⚠️ Unsupported source type: {source.source_type}")
                return []
        
        except Exception as e:
            logger.error(f"❌ Error fetching content from {source.name}: {e}")
            return []
    
    def fetch_api_content(self, source: ContentSource) -> List[ProcessedDocument]:
        """Fetch content from API sources"""
        documents = []
        
        if "n8n.io/api/nodes" in source.url:
            # Fetch n8n nodes information
            try:
                response = requests.get(source.url, timeout=30)
                response.raise_for_status()
                nodes_data = response.json()
                
                for node in nodes_data.get('nodes', []):
                    doc = ProcessedDocument(
                        id=f"n8n_node_{node.get('name', '')}",
                        source=source.name,
                        title=f"Nodo {node.get('displayName', node.get('name', ''))}",
                        content=self.format_node_content(node),
                        content_type="reference",
                        language="es",  # We'll translate
                        complexity_level="intermediate",
                        tags=["n8n", "node", node.get('name', '')],
                        last_updated=datetime.now()
                    )
                    documents.append(doc)
                
                logger.info(f"✅ Procesados {len(documents)} nodos de n8n")
                
            except Exception as e:
                logger.error(f"❌ Error fetching n8n nodes: {e}")
        
        return documents
    
    def fetch_url_content(self, source: ContentSource) -> List[ProcessedDocument]:
        """Fetch content from URL sources"""
        documents = []
        
        # Implementation would depend on specific URLs
        # For now, placeholder
        logger.info(f"📝 URL content fetching for {source.name} - TODO: implement specific parsers")
        
        return documents
    
    def fetch_file_content(self, source: ContentSource) -> List[ProcessedDocument]:
        """Fetch content from file sources"""
        documents = []
        path = Path(source.url)
        
        if not path.exists():
            logger.warning(f"⚠️ Path does not exist: {source.url}")
            return documents
        
        try:
            if path.is_file() and path.suffix == '.md':
                # Single markdown file
                content = path.read_text(encoding='utf-8')
                doc = ProcessedDocument(
                    id=f"file_{path.stem}",
                    source=source.name,
                    title=path.stem.replace('_', ' ').replace('-', ' ').title(),
                    content=content,
                    content_type="tutorial",
                    language=(source.metadata or {}).get('language', 'es'),
                    complexity_level="intermediate",
                    tags=[source.name, "file"],
                    last_updated=datetime.now()
                )
                documents.append(doc)
            
            elif path.is_dir():
                # Directory of files
                for file_path in path.rglob("*.md"):
                    content = file_path.read_text(encoding='utf-8')
                    doc = ProcessedDocument(
                        id=f"file_{file_path.stem}",
                        source=source.name,
                        title=file_path.stem.replace('_', ' ').replace('-', ' ').title(),
                        content=content,
                        content_type="tutorial",
                        language=(source.metadata or {}).get('language', 'es'),
                        complexity_level="intermediate", 
                        tags=[source.name, "file"],
                        last_updated=datetime.now()
                    )
                    documents.append(doc)
            
            logger.info(f"✅ Procesados {len(documents)} documentos de archivos")
            
        except Exception as e:
            logger.error(f"❌ Error reading files from {source.url}: {e}")
        
        return documents
    
    def format_node_content(self, node_data: Dict) -> str:
        """Format n8n node data into readable content"""
        content = f"""
# {node_data.get('displayName', node_data.get('name', 'Nodo Desconocido'))}

**Descripción:** {node_data.get('description', 'Sin descripción disponible')}

**Categoría:** {node_data.get('group', 'General')}

**Versión:** {node_data.get('version', '1.0')}

## Funcionalidades principales:
"""
        
        # Add operations if available
        operations = node_data.get('operations', [])
        if operations:
            content += "\n### Operaciones disponibles:\n"
            for op in operations:
                content += f"- **{op.get('name', 'Operación')}**: {op.get('description', 'Sin descripción')}\n"
        
        # Add properties if available  
        properties = node_data.get('properties', [])
        if properties:
            content += "\n### Propiedades principales:\n"
            for prop in properties[:5]:  # Limit to first 5 properties
                content += f"- **{prop.get('displayName', prop.get('name', 'Propiedad'))}**: {prop.get('description', 'Sin descripción')}\n"
        
        return content.strip()
    
    def chunk_document(self, doc: ProcessedDocument, chunk_size: int = 1000) -> List[ProcessedDocument]:
        """Split long documents into smaller chunks"""
        if len(doc.content) <= chunk_size:
            return [doc]
        
        chunks = []
        words = doc.content.split()
        
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > chunk_size and current_chunk:
                # Create chunk
                chunk_content = ' '.join(current_chunk)
                chunk_doc = ProcessedDocument(
                    id=f"{doc.id}_chunk_{len(chunks)}",
                    source=doc.source,
                    title=f"{doc.title} (Parte {len(chunks) + 1})",
                    content=chunk_content,
                    content_type=doc.content_type,
                    language=doc.language,
                    complexity_level=doc.complexity_level,
                    tags=doc.tags + ["chunk"],
                    last_updated=doc.last_updated
                )
                chunks.append(chunk_doc)
                
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        # Add final chunk
        if current_chunk:
            chunk_content = ' '.join(current_chunk)
            chunk_doc = ProcessedDocument(
                id=f"{doc.id}_chunk_{len(chunks)}",
                source=doc.source,
                title=f"{doc.title} (Parte {len(chunks) + 1})",
                content=chunk_content,
                content_type=doc.content_type,
                language=doc.language,
                complexity_level=doc.complexity_level,
                tags=doc.tags + ["chunk"],
                last_updated=doc.last_updated
            )
            chunks.append(chunk_doc)
        
        return chunks
    
    def generate_embeddings(self, documents: List[ProcessedDocument]) -> List[ProcessedDocument]:
        """Generate embeddings for documents"""
        logger.info(f"🔄 Generando embeddings para {len(documents)} documentos...")
        
        batch_size = 50  # Process in batches to avoid rate limits
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            contents = [doc.content for doc in batch]
            
            try:
                # Generate embeddings for batch
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=contents,
                    task_type="RETRIEVAL_DOCUMENT"
                )
                
                # Assign embeddings to documents
                if isinstance(result['embedding'][0], list):
                    # Multiple embeddings
                    for j, embedding in enumerate(result['embedding']):
                        if i + j < len(documents):
                            documents[i + j].embedding = embedding
                else:
                    # Single embedding
                    if len(batch) == 1:
                        batch[0].embedding = result['embedding']
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Error generating embeddings for batch {i//batch_size + 1}: {e}")
                # Continue with next batch
                continue
        
        successful_embeddings = sum(1 for doc in documents if doc.embedding is not None)
        logger.info(f"✅ Generados {successful_embeddings} embeddings exitosamente")
        
        return documents
    
    def store_in_chromadb(self, documents: List[ProcessedDocument]):
        """Store documents in ChromaDB"""
        logger.info(f"💾 Almacenando {len(documents)} documentos en ChromaDB...")
        
        # Filter documents with embeddings
        valid_docs = [doc for doc in documents if doc.embedding is not None]
        
        if not valid_docs:
            logger.warning("⚠️ No hay documentos válidos para almacenar")
            return
        
        # Prepare data for ChromaDB
        ids = [doc.id for doc in valid_docs]
        embeddings = [doc.embedding for doc in valid_docs]
        metadatas = []
        documents_content = []
        
        for doc in valid_docs:
            metadata = {
                "source": doc.source,
                "title": doc.title,
                "content_type": doc.content_type,
                "language": doc.language,
                "complexity_level": doc.complexity_level,
                "tags": ",".join(doc.tags),
                "last_updated": doc.last_updated.isoformat()
            }
            metadatas.append(metadata)
            documents_content.append(doc.content)
        
        try:
            # Remove existing documents with same IDs (update)
            try:
                self.collection.delete(ids=ids)
            except:
                pass  # IDs might not exist yet
            
            # Add new documents
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_content
            )
            
            logger.info(f"✅ Almacenados {len(valid_docs)} documentos exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error almacenando documentos: {e}")
    
    def update_source(self, source: ContentSource) -> bool:
        """Update a single source"""
        logger.info(f"🔄 Actualizando fuente: {source.name}")
        
        # Fetch content
        documents = self.fetch_content(source)
        
        if not documents:
            logger.warning(f"⚠️ No se obtuvo contenido de {source.name}")
            return False
        
        # Chunk large documents
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"📄 Total de chunks: {len(all_chunks)}")
        
        # Generate embeddings
        documents_with_embeddings = self.generate_embeddings(all_chunks)
        
        # Store in ChromaDB
        self.store_in_chromadb(documents_with_embeddings)
        
        # Update source metadata
        source.last_updated = datetime.now()
        if source.source_type in ["file", "api", "url"]:
            if source.source_type == "file":
                source.content_hash = self.get_directory_hash(Path(source.url))
            else:
                # Simple hash for API/URL sources
                source.content_hash = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        
        self.save_sources_config()
        
        logger.info(f"✅ Actualización completada para {source.name}")
        return True
    
    def run_update_cycle(self, force_update: bool = False):
        """Run complete update cycle"""
        logger.info("🚀 Iniciando ciclo de actualización de base de conocimiento")
        
        updated_sources = 0
        
        for source in self.sources:
            if force_update or self.should_update_source(source):
                try:
                    if self.update_source(source):
                        updated_sources += 1
                except Exception as e:
                    logger.error(f"❌ Error actualizando {source.name}: {e}")
                    continue
            else:
                logger.info(f"⏭️ Saltando {source.name} - no necesita actualización")
        
        logger.info(f"✅ Ciclo completado. Fuentes actualizadas: {updated_sources}/{len(self.sources)}")
        
        # Show collection stats
        try:
            count = self.collection.count()
            logger.info(f"📊 Total de documentos en base de conocimiento: {count}")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo obtener estadísticas: {e}")
    
    def add_custom_source(self, name: str, source_type: str, url: str, 
                         update_frequency: str = "on_demand", **metadata):
        """Add a custom content source"""
        new_source = ContentSource(
            name=name,
            source_type=source_type,
            url=url,
            last_updated=datetime.now(),
            content_hash="",
            update_frequency=update_frequency,
            metadata=metadata
        )
        
        self.sources.append(new_source)
        self.save_sources_config()
        
        logger.info(f"✅ Agregada nueva fuente: {name}")
        return new_source

def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="n8nation Knowledge Base Updater")
    parser.add_argument("--force", action="store_true", help="Force update all sources")
    parser.add_argument("--source", type=str, help="Update specific source only")
    parser.add_argument("--add-source", nargs=4, metavar=('NAME', 'TYPE', 'URL', 'FREQUENCY'),
                       help="Add new source: name type url frequency")
    
    args = parser.parse_args()
    
    try:
        updater = KnowledgeUpdater()
        
        if args.add_source:
            name, source_type, url, frequency = args.add_source
            updater.add_custom_source(name, source_type, url, frequency)
            print(f"✅ Added source: {name}")
        
        elif args.source:
            # Update specific source
            source = next((s for s in updater.sources if s.name == args.source), None)
            if source:
                updater.update_source(source)
            else:
                print(f"❌ Source not found: {args.source}")
        
        else:
            # Regular update cycle
            updater.run_update_cycle(force_update=args.force)
    
    except Exception as e:
        logger.error(f"❌ Error in main execution: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())