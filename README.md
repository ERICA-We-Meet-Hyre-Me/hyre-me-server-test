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
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## GitHub Actions 자동 배포

워크플로우 파일: `.github/workflows/deploy.yml`

`main` 브랜치에 push 될 때마다 자동 배포됩니다.

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

서비스 파일은 레포에서 관리합니다.

- `deploy/systemd/hyre-me-api.service`
- 배포 시 `/etc/systemd/system/hyre-me-api.service`로 복사됨

상태 확인:

```bash
sudo systemctl status hyre-me-api --no-pager
```
