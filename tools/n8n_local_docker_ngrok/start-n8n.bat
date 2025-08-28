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
echo ➡️ Join our Telegram Channel: https://t.me/n8nation
echo ➡️ Join our Telegram Group: https://t.me/n8nation_chat
echo ➡️ Reddit: https://reddit.com/r/n8nation_
echo ➡️ Check out the repository: https://github.com/MrKaizen7/n8n_local_docker_ngrok
echo ➡️ Join N8Nation: See PROPOSAL.md for collaboration opportunities
echo.
pause
