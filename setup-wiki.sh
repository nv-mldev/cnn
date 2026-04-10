#!/bin/bash
set -euo pipefail

echo "=== Step 1: MkDocs systemd service ==="
cat > /etc/systemd/system/mkdocs-wiki.service <<'SVC'
[Unit]
Description=MkDocs Wiki Server
After=network.target

[Service]
User=nithin
WorkingDirectory=/home/nithin/projects/cnn
ExecStart=/home/nithin/.local/bin/mkdocs serve --dev-addr=0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
SVC

systemctl daemon-reload
systemctl enable --now mkdocs-wiki
echo "MkDocs service started."

echo "=== Step 2: Nginx reverse proxy ==="
apt install -y apache2-utils nginx

cat > /etc/nginx/sites-available/wiki <<'NGX'
server {
    listen 80;
    server_name _;

    auth_basic "Wiki";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGX

ln -sf /etc/nginx/sites-available/wiki /etc/nginx/sites-enabled/

echo "=== Step 3: Set wiki password ==="
echo "Enter a password for the wiki:"
htpasswd -c /etc/nginx/.htpasswd nithin

echo "=== Step 4: Test and reload nginx ==="
nginx -t
systemctl reload nginx

echo "=== Done! ==="
echo "Wiki is live at http://$(hostname -I | awk '{print $1}')/"
