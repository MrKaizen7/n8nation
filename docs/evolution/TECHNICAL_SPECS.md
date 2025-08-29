# Especificaciones Técnicas - n8nation

## Configuración del Entorno de Desarrollo

### Componentes Base

#### docker-compose.yml
```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=tu_correo@ejemplo.com
      - N8N_BASIC_AUTH_PASSWORD=tu_password
      - N8N_LICENSE_TENANT_ID=tu_license_key
      - WEBHOOK_URL=https://tu-dominio-fijo.ngrok-free.app/
      - N8N_SECURE_COOKIE=false
      - N8N_CORS_ORIGIN=*
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
volumes:
  n8n_data:
  postgres_data:
```

#### start-n8n.bat
```batch
@echo off
echo Iniciando n8nation Development Environment...
echo.

REM Verificar si Docker está corriendo
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está corriendo. Por favor, abre Docker Desktop primero.
    pause
    exit /b 1
)

REM Verificar si ngrok.exe existe
if not exist "ngrok.exe" (
    echo ❌ ngrok.exe no se encuentra en esta carpeta.
    echo Por favor, descarga ngrok.exe y ponlo en la misma carpeta que este script.
    pause
    exit /b 1
)

echo ✅ Iniciando contenedor de n8n...
docker-compose up -d

echo ✅ Esperando que n8n esté listo...
timeout /t 10

echo ✅ Iniciando túnel de Ngrok...
start /min ngrok http --domain=tu-dominio-fijo.ngrok-free.app 5678

echo ✅ Abriendo n8n en el navegador...
timeout /t 5
start https://tu-dominio-fijo.ngrok-free.app

echo.
echo ✅ All done. You can close this window or leave it open to monitor.
echo.
echo ➡️ Need help or want to connect with the community?
echo ➡️ Join our Telegram Channel: https://t.me/n8nation
echo ➡️ Join our Telegram Group: https://t.me/n8nation_chat  
echo ➡️ Check out the repository: https://github.com/MrKaizen7/n8n_local_docker_ngrok
echo.
pause
```

## Requisitos del Sistema

### Hardware Mínimo
- **RAM:** 4GB (recomendado 8GB)
- **Almacenamiento:** 2GB libres
- **Procesador:** Cualquier CPU de 64 bits

### Software Requerido
- **Docker Desktop:** Versión 4.0 o superior
- **Ngrok:** Cuenta gratuita o de pago
- **Sistema Operativo:** Windows 10/11, macOS, Linux

### Dependencias
- **PostgreSQL:** Incluido en docker-compose
- **Node.js:** Manejado dentro del contenedor
- **n8n:** Última versión estable

## Configuración de Ngrok

### Setup Inicial
1. Crear cuenta en [ngrok.com](https://ngrok.com)
2. Descargar ngrok.exe
3. Configurar authtoken:
   ```bash
   ngrok config add-authtoken TU_AUTHTOKEN
   ```

### Dominio Persistente
Para URL fija, configurar en ngrok.com:
- Ir a Cloud Edge > Domains  
- Crear dominio estático
- Usar formato: `tu-dominio-fijo.ngrok-free.app`

## Estructura del Proyecto

```
n8n_local_docker_ngrok/
├── docker-compose.yml          # Configuración de contenedores
├── start-n8n.bat              # Script de inicio
├── updaten8ncomposer.txt       # Guía de actualización
├── README.md                   # Documentación principal
├── N8NATION_MASTER_PLAN.md     # Plan estratégico
├── docs/                       # Documentación de evolución
│   ├── 01.md - 10.md          # Registro de conversaciones
└── LICENSE                     # Licencia MIT
```

## Comandos Útiles

### Docker
```bash
# Ver logs de n8n
docker-compose logs n8n

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Actualizar n8n
docker-compose pull && docker-compose up -d
```

### Troubleshooting
```bash
# Verificar puertos
netstat -an | findstr :5678

# Limpiar containers
docker system prune

# Ver estado de servicios
docker-compose ps
```

## Seguridad

### Configuración Básica
- **Autenticación:** Habilitada por defecto
- **HTTPS:** Forzado través de Ngrok
- **CORS:** Configurado para desarrollo local

### Mejores Prácticas
1. Cambiar credenciales por defecto
2. Usar variables de entorno para secretos
3. Regularmente actualizar n8n
4. Monitorear logs por actividad sospechosa

## Variables de Entorno

### Configurables
```env
N8N_BASIC_AUTH_USER=tu_correo@ejemplo.com
N8N_BASIC_AUTH_PASSWORD=tu_password_seguro
N8N_LICENSE_TENANT_ID=tu_license_key
WEBHOOK_URL=https://tu-dominio-fijo.ngrok-free.app/
```

### Opcionales
```env
N8N_ENCRYPTION_KEY=tu_clave_encriptacion
N8N_SECURE_COOKIE=false
N8N_CORS_ORIGIN=*
N8N_LOG_LEVEL=info
```

## Licencias y Cumplimiento

### Licencia MIT del Proyecto
- Uso libre para cualquier propósito
- Modificación y distribución permitidas
- Sin garantías implícitas

### Cumplimiento con n8n
- ✅ Uso personal y comercial permitido
- ✅ Venta de workflows (.json) permitida
- ✅ Consultoría y servicios permitidos
- ❌ Hosting como servicio (requiere licencia $50K)
- ❌ Redistribución embebida (requiere licencia $50K)

## Roadmap Técnico

### Versión 1.1
- [ ] Script para Linux/macOS
- [ ] Configuración automática de Ngrok
- [ ] Verificación de requisitos previos

### Versión 1.2  
- [ ] Integración con Docker Desktop API
- [ ] GUI simple para configuración
- [ ] Backup automático de workflows

### Versión 2.0
- [ ] Aplicación React para gestión
- [ ] API para gestión remota
- [ ] Integración con servicios cloud
