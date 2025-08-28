# n8n AI Copilot — Automatización Inteligente Multilingüe

Bienvenido a n8nation, la plataforma colaborativa para automatización de flujos de trabajo con IA, diseñada para equipos globales y desarrolladores. Potencia tus procesos con búsqueda semántica, memoria conversacional y actualizaciones en tiempo real.

## Características principales
- Soporte multilingüe (español/inglés, auto-detección y traducción inteligente)
- Búsqueda semántica avanzada con ChromaDB
- Automatización de workflows y actualizaciones en tiempo real
- Memoria conversacional contextual
- Integraciones con Discord, React y más
- Demo end-to-end sin dependencias externas

## Arquitectura
n8n AI Copilot se compone de módulos Python para procesamiento de documentos, generación de embeddings, gestión de memoria y APIs REST para actualizaciones. Utiliza Google Gemini para IA y ChromaDB para búsquedas vectoriales. Consulta [copilot-instructions.md](.github/copilot-instructions.md) y [symbiotic_development.instructions.md](.github/instructions/symbiotic_development.instructions.md) para detalles técnicos y patrones colaborativos.

## Guía rápida de instalación
1. Clona el repositorio:
	```powershell
	git clone https://github.com/MrKaizen7/n8nation.git
	```
2. Instala dependencias:
	```powershell
	cd tools/ai-copilot
	pip install -r requirements.txt
	```
3. Configura variables de entorno:
	- Copia `.env.example` a `.env` y agrega tu `GOOGLE_API_KEY`.
4. Inicializa la base de conocimiento:
	```powershell
	python process_docs.py
	python embed_and_store.py
	```
5. Ejecuta el copilot:
	```powershell
	python enhanced_copilot.py
	```
6. Actualiza el conocimiento:
	```powershell
	python knowledge_updater.py --force
	# O vía API: python update_webhook.py
	```
7. Prueba la demo:
	```powershell
	python demo_copilot.py
	```

## Workflow de desarrollo
- Usa `python enhanced_copilot.py` para desarrollo principal.
- Ejecuta `python ai-copilot/demo_copilot.py` para demos rápidas.
- Consulta y actualiza instrucciones en `.github/instructions/` y prompts en `.github/prompts/`.

## Tecnologías clave
- Python
- ChromaDB
- Google Gemini API
- Docker
- TypeScript (integraciones)

## Contribuir
¿Quieres aportar? Revisa [CONTRIBUTING.md](CONTRIBUTING.md) para guías y buenas prácticas.

## Licencia
Este proyecto está bajo la licencia [MIT](LICENSE).

---
¿Dudas, sugerencias o ideas? Únete a la comunidad y revisa [CHANGELOG.md](CHANGELOG.md) y [ROADMAP.md](docs/N8NATION_MASTER_PLAN.md) para novedades.
