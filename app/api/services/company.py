from __future__ import annotations

import random

COMPANIES = [
    "네이버",
    "카카오",
    "라인",
    "쿠팡",
    "배달의민족",
    "삼성",
    "LG",
    "하이닉스",
    "토스",
    "당근마켓",
]


def get_random_company() -> str:
    """기업명 리스트에서 랜덤하게 하나의 기업을 선택해서 반환합니다."""
    return random.choice(COMPANIES)
