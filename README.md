# hyre-me FastAPI 테스트 서버

라즈베리파이 자동 배포 FastAPI 테스트 API 프로젝트

## API 명세

- 기본 경로: `/api`
- 테스트 엔드포인트: `GET /api/test`
- 응답 예시:

```json
{
  "time": "2026-04-18T12:34:56+09:00",
  "message": "hello world!"
}
```

## 환경 변수

서버의 `/var/www/hyre-me/api/.env` 파일에 아래 값을 설정합니다.

```env
gemini_api_key=YOUR_REAL_KEY
```

## 로컬 실행

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## GitHub Actions 자동 배포

워크플로우 파일: `.github/workflows/deploy.yml`

`main` 브랜치에 push 될 때마다 서버의 `/var/www/hyre-me/api`로 코드 파일(`app`, `requirements.txt`)만 동기화합니다.

`systemd`, `nginx`, TLS 인증서, 방화벽, 서비스 재시작은 **서버 관리자 사전 설정/운영 항목**이며 GitHub Actions에서 수행하지 않습니다.

리포지토리 Secrets 설정값(예시):

- `SERVER_HOST`: `YOUR_SERVER_HOST`
- `SERVER_PORT`: `YOUR_SERVER_PORT`
- `SERVER_USER`: `YOUR_SERVER_USER`
- `SERVER_SSH_KEY` : `YOUR_SERVER_SSH_KEY`


## 1회 초기 설정 (디렉토리 및 권한 설정)

```bash
sudo mkdir -p /var/www/hyre-me/api
sudo chown -R deploy:deploy /var/www/hyre-me
```

## systemd 서비스

서버 관리자 계정에서 user systemd 서비스를 직접 생성합니다.

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/hyre-me-api.service <<'EOF'
[Unit]
Description=hyre-me FastAPI service
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/hyre-me/api
EnvironmentFile=-/var/www/hyre-me/api/.env
ExecStart=/var/www/hyre-me/api/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user enable hyre-me-api
systemctl --user restart hyre-me-api
```

상태 확인:

```bash
systemctl --user status hyre-me-api --no-pager
journalctl --user -u hyre-me-api -n 100 --no-pager
```

## Nginx 리버스 프록시

도메인:

- `hyre-me-api-test.pdj.kr`

백엔드 업스트림:

- `127.0.0.1:8001`

아래 작업은 서버 관리자가 사전에 설정:

```bash
sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
sudo tee /etc/nginx/sites-available/hyre-me-api-test.conf > /dev/null <<'EOF'
server {
  listen 80;
  listen [::]:80;
  server_name hyre-me-api-test.pdj.kr;

  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  server_name hyre-me-api-test.pdj.kr;

  ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
  ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_session_timeout 1d;
  ssl_session_cache shared:SSL:10m;

  client_max_body_size 20m;

  location / {
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 60s;

    proxy_pass http://127.0.0.1:8001;
  }
}
EOF

sudo ln -sfn /etc/nginx/sites-available/hyre-me-api-test.conf /etc/nginx/sites-enabled/hyre-me-api-test.conf
sudo rm -f /etc/nginx/sites-enabled/default

# Debian/Ubuntu는 보통 아래 snakeoil 인증서가 이미 존재함.
# 없으면 임시 self-signed 인증서 생성.
if [ ! -f /etc/ssl/certs/ssl-cert-snakeoil.pem ] || [ ! -f /etc/ssl/private/ssl-cert-snakeoil.key ]; then
  sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
    -subj "/CN=hyre-me-api-test.pdj.kr" \
    -keyout /etc/ssl/private/ssl-cert-snakeoil.key \
    -out /etc/ssl/certs/ssl-cert-snakeoil.pem
  sudo chmod 600 /etc/ssl/private/ssl-cert-snakeoil.key
fi

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
sudo systemctl status nginx --no-pager
```
