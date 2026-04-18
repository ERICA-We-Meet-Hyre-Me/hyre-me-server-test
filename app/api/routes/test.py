from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test_endpoint() -> dict[str, str]:
    now = datetime.now(timezone.utc).astimezone().isoformat()
    return {
        "time": now,
        "message": "hello world!",
    }
