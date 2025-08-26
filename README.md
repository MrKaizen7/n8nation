Configuración Local de N8N con Docker y Ngrok
¡Bienvenido a la Configuración Local de N8N! Este repositorio ofrece una solución sencilla y con un solo clic para ejecutar n8n en un contenedor de Docker y exponerlo a internet con una URL persistente de Ngrok. ¡Di adiós a la frustración de tener que cambiar las URL de tus webhooks!

¿Por Qué Usar Esta Configuración?
URL Persistente: Tu URL de webhook se mantiene igual cada vez que ejecutas el script, lo que la hace perfecta para el desarrollo y las pruebas.

Automatización: Un solo archivo .bat se encarga de iniciar tu contenedor de Docker y crear el túnel de Ngrok.

Entorno Limpio: Todo se ejecuta dentro de un contenedor de Docker, manteniendo el entorno de tu máquina local limpio y libre de conflictos de dependencias.

Requisitos Previos
Antes de empezar, asegúrate de tener lo siguiente instalado:

Docker

Ngrok

Empezando
1. Clona el Repositorio
Clona este repositorio en tu máquina local:

git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

2. Configura Tus Archivos
Abre los archivos docker-compose.yml y start-n8n.bat y reemplaza los valores de marcador de posición con tu propia información.

docker-compose.yml
Reemplaza estos valores:

tu_correo@ejemplo.com

tu_password

tu_licencia_key

https://tu-dominio-fijo.ngrok-free.app/

start-n8n.bat
Reemplaza este valor:

tu-dominio-fijo.ngrok-free.app

3. Ejecuta el Script
Una vez que tus archivos estén configurados, simplemente ejecuta el archivo start-n8n.bat.

start-n8n.bat

Esto iniciará automáticamente tu contenedor de Docker de n8n, creará el túnel de Ngrok y abrirá tu instancia de n8n en tu navegador web predeterminado.

Comunidad
¡Únete a nuestra comunidad para hacer preguntas, compartir tus flujos de trabajo y conectar con otros usuarios de n8n! Esta comunidad es principalmente para usuarios de habla hispana.

Canal de Telegram: https://t.me/tu_canal_de_telegram

Grupo de Telegram: https://t.me/tu_grupo_de_telegram
