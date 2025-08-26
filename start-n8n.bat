@echo off
cd /d %~dp0

echo 🚀 Starting n8n via Docker Compose...
docker compose up -d

echo 🌐 Starting ngrok tunnel...
start "" ngrok.exe http --domain=*tu-dominio-fijo.ngrok-free.app* 5678

timeout /t 5 >nul

echo 🧠 Opening n8n in your browser...
start *https://tu-dominio-fijo.ngrok-free.app*

echo ✅ All done. You can close this window or leave it open to monitor.
echo.
echo ➡️ Need help or want to connect with the community?
echo ➡️ Join our Telegram Channel: https://t.me/tu_canal_de_telegram
echo ➡️ Join our Telegram Group: https://t.me/tu_grupo_de_telegram
echo ➡️ Check out the repository for more info: https://github.com/tu_usuario/tu_repositorio
echo.
pause
