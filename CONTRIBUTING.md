# Contributing to n8nation

¡Gracias por tu interés en contribuir a n8nation! 🚀

## Código de Conducta

### Nuestros Valores
- **Colaboración:** Trabajamos juntos hacia objetivos comunes
- **Respeto:** Tratamos a todos los miembros con dignidad y profesionalismo
- **Transparencia:** Compartimos información abiertamente dentro de la comunidad
- **Calidad:** Nos esforzamos por entregar trabajo de alta calidad
- **Crecimiento:** Apoyamos el desarrollo personal y profesional de todos

### Comportamiento Esperado
- ✅ Comunicación respetuosa y constructiva
- ✅ Colaboración activa y apoyo mutuo
- ✅ Feedback honesto y útil
- ✅ Cumplimiento de compromisos y plazos
- ✅ Compartir conocimiento y experiencias

### Comportamiento Inaceptable
- ❌ Discriminación o acoso de cualquier tipo
- ❌ Lenguaje ofensivo o comportamiento despectivo
- ❌ Spam o autopromoción excesiva
- ❌ Compartir información confidencial de clientes
- ❌ Plagio o violación de derechos de autor

## Tipos de Contribuciones

### 1. Desarrollo de Workflows
**¿Qué puedes aportar?**
- Workflows de n8n (.json) para casos de uso específicos
- Optimizaciones de workflows existentes
- Integraciones innovadoras entre plataformas
- Soluciones para industrias específicas

**Proceso:**
1. Fork del repositorio
2. Crear branch: `feature/workflow-[nombre]`
3. Desarrollar y probar workflow
4. Documentar uso y configuración
5. Pull request con descripción detallada

### 2. Documentación
**¿Qué necesitamos?**
- Tutoriales paso a paso
- Traducción de contenido técnico
- Guías de mejores prácticas
- Casos de estudio y ejemplos

**Proceso:**
1. Identificar gap en documentación
2. Crear issue describiendo lo que planeas escribir
3. Escribir contenido siguiendo style guide
4. Review interno antes de publicación

### 3. Desarrollo de Herramientas
**Oportunidades:**
- Mejoras al script start-n8n.bat
- Herramientas de línea de comandos
- Extensiones para editores de código
- Utilidades para debugging de workflows

### 4. Community Management
**¿Cómo ayudar?**
- Responder preguntas en Telegram
- Moderar discusiones
- Organizar eventos virtuales
- Crear contenido para redes sociales

### 5. Testing y QA
**Actividades:**
- Probar workflows en diferentes entornos
- Reportar bugs y problemas
- Validar documentación
- Testing de nuevas features

## Sistema de Puntos y Compensación

### Cómo Funcionan los Puntos
n8nation usa un **sistema transparente de puntos** para reconocer y compensar contribuciones:

#### Puntos por Desarrollo de Proyectos
| Actividad | Puntos Base | Multiplicadores |
|-----------|-------------|-----------------|
| Workflow simple (1-5 nodes) | 100-300 | +50% si es innovador |
| Workflow complejo (5+ nodes) | 300-800 | +25% si incluye documentación |
| Integración nueva | 200-500 | +100% si es primera vez |
| Bug fix crítico | 150-400 | +25% si es urgente |
| Optimización performance | 100-300 | +50% si mejora >30% |

#### Puntos por Contribuciones Comunitarias
| Actividad | Puntos | Frecuencia |
|-----------|--------|------------|
| Tutorial detallado | 100-300 | Por tutorial |
| Respuesta útil en Telegram | 5-20 | Por respuesta |
| Moderación diaria | 20-50 | Por día |
| Referir nuevo colaborador | 100 | Por referido activo |
| Organizar evento | 200-500 | Por evento |

### Conversión de Puntos a Dinero
- **Proyectos pagados:** Puntos se convierten a porcentaje según quota y tarifa del proyecto
- **Pote comunitario:** Distribución basada en puntos totales
- **Bonos:** Reconocimiento especial por contribuciones excepcionales

### Transparencia
- Dashboard público con puntos de cada contributor
- Sistema auditabile con historial completo
- Proceso abierto de dispute resolution

## Proceso de Contribución

### Proyectos de Clientes

#### 1. Aplicación a Proyectos
```
1. Revisar proyectos disponibles en Telegram/Reddt
2. Evaluar si tienes las skills necesarias
3. Aplicar con propuesta de abordaje
4. Esperar selección del equipo
5. Participar en kickoff meeting
```

#### 2. Durante el Proyecto
```
1. Comunicación regular en canal de proyecto
2. Updates de progreso cada 2-3 días
3. Code review con otros team members
4. Testing conjunto antes de entrega
5. Documentación de trabajo realizado
```

#### 3. Entrega y Payment
```
1. Review final con cliente
2. Cálculo de puntos por contribución
3. Payment procesado según términos
4. Retrospective con equipo
5. Actualización de portfolio
```

### Proyectos de Comunidad

#### 1. Propuesta de Proyecto
```markdown
## Project Proposal: [TÍTULO]

**Problema que resuelve:**
[Descripción del problema]

**Solución propuesta:**
[Tu approach para resolverlo]

**Beneficio para comunidad:**
[Por qué es valioso]

**Recursos necesarios:**
[Tiempo, herramientas, colaboración]

**Timeline estimado:**
[Cuándo estaría listo]
```

#### 2. Desarrollo Colaborativo
- Trabajo en branches separados
- Daily standups opcionales
- Peer review obligatorio
- Testing en múltiples entornos

#### 3. Release Process
- Merge a main branch
- Update documentation
- Announcement en comunidad
- Celebration y recognition 🎉

## Standards Técnicos

### Workflows de n8n
```json
{
  "name": "Descriptive Workflow Name",
  "nodes": [],
  "connections": {},
  "settings": {
    "executionOrder": "v1"
  },
  "staticData": {},
  "tags": ["category", "industry", "complexity-level"],
  "meta": {
    "description": "Clear description of what this workflow does",
    "author": "Your GitHub username",
    "version": "1.0.0",
    "requirements": ["List", "of", "required", "integrations"],
    "setupInstructions": "Step-by-step setup guide"
  }
}
```

### Documentation Standards
- **Headers:** Use consistent markdown headers
- **Code blocks:** Always specify language for syntax highlighting
- **Images:** Store in `/assets/` folder with descriptive names
- **Links:** Use relative links when possible

### Git Workflow
```bash
# 1. Fork y clone
git clone https://github.com/tu-usuario/n8n_local_docker_ngrok.git
cd n8n_local_docker_ngrok

# 2. Crear feature branch
git checkout -b feature/mi-nueva-feature

# 3. Hacer cambios y commits
git add .
git commit -m "feat: add workflow for Shopify to Slack integration"

# 4. Push y crear PR
git push origin feature/mi-nueva-feature
# Crear Pull Request en GitHub
```

### Commit Message Standards
Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new workflow for e-commerce automation
fix: resolve issue with webhook timeout
docs: update installation instructions
refactor: improve error handling in core workflow
test: add unit tests for API integration
```

## Review Process

### Code Review Checklist
- [ ] **Functionality:** Does it work as intended?
- [ ] **Documentation:** Is it properly documented?
- [ ] **Testing:** Has it been tested in multiple scenarios?
- [ ] **Style:** Follows project coding standards?
- [ ] **Security:** No sensitive data exposed?
- [ ] **Performance:** Efficient resource usage?

### Documentation Review
- [ ] **Clarity:** Easy to understand for target audience?
- [ ] **Completeness:** Covers all necessary information?
- [ ] **Accuracy:** Technical information is correct?
- [ ] **Examples:** Includes practical examples?
- [ ] **Language:** Grammar and spelling are correct?

## Getting Help

### Where to Ask Questions
1. **Technical Issues:** GitHub Issues
2. **General Questions:** @n8nation_chat (Telegram)
3. **Collaboration Opportunities:** Direct message @MrKaizen7
4. **Community Events:** @n8nation (Telegram channel)

### Mentorship Program
- **New Contributors:** Paired with experienced community member
- **Monthly Check-ins:** Progress review and goal setting
- **Skill Development:** Access to learning resources and workshops
- **Project Opportunities:** Guided introduction to collaborative projects

## Recognition and Growth

### Contributor Levels
```
🌱 Newcomer (0-100 points)
   - Getting started with first contributions
   - Access to mentorship program
   - Basic community privileges

🌿 Contributor (100-500 points)
   - Regular community participant
   - Can lead small projects
   - Eligible for community pot distributions

🌳 Core Member (500-2000 points)
   - Significant project contributions
   - Can mentor newcomers
   - Voting rights on community decisions

🏆 Community Leader (2000+ points)
   - Major impact on n8nation growth
   - Strategic decision involvement
   - Profit-sharing opportunities
```

### Achievement Badges
- 🥇 **First Contribution:** Your first merged PR
- 🔧 **Tool Builder:** Created useful development tool
- 📚 **Knowledge Sharer:** Multiple tutorials created
- 🤝 **Team Player:** Collaborated on 5+ projects
- 🌟 **Innovation Award:** Created groundbreaking workflow
- 👑 **Community Champion:** Outstanding community leadership

## Roadmap Participation

### How Decisions Are Made

n8nation operates under a **democratic governance model** where major decisions are made through community voting:

1. **Proposal** (3 days): Community member proposes new direction/feature
2. **Discussion** (7 days): Open debate in Telegram and GitHub  
3. **Refinement** (2 days): Proposal refined based on feedback
4. **Vote** (2 days): Weighted voting by contribution points
5. **Implementation**: Transparent execution of approved decisions

**What gets voted on:**
- Points system values (e.g., testing = 150 points?)
- Feature development priorities  
- Compensation policies and pote distribution
- Strategic partnerships and expansion

**Voting weight** is based on contribution history: recent activity (70%) + historical points (30%).

For complete details about our governance structure, voting procedures, and decision-making processes, see [Gobernanza Democrática](./N8NATION_MASTER_PLAN.md#gobernanza-democrática) in our Master Plan.

### Current Priority Areas
- [ ] **React App Development:** Build the central platform
- [ ] **AI/RAG Integration:** Workflow co-creation assistant
- [ ] **Mobile Experience:** Progressive Web App
- [ ] **Enterprise Features:** Advanced collaboration tools
- [ ] **International Expansion:** Multi-language support

---

## Quick Start Checklist

### Ready to Contribute? ✅
- [ ] Read and understand Code of Conduct
- [ ] Join @n8nation_chat Telegram group  
- [ ] Introduce yourself in the community
- [ ] Fork the repository
- [ ] Pick your first contribution type
- [ ] Read relevant technical standards
- [ ] Start with a small, manageable task
- [ ] Ask questions when you need help!

**¡Bienvenido a n8nation! Tu contribución hace la diferencia.** 🚀

---

*Esta guía es un documento vivo. Si tienes sugerencias para mejorarla, ¡crea un issue o propón cambios directamente!*
