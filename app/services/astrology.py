from __future__ import annotations

import math
from datetime import datetime
from typing import Any

ZODIAC_SIGNS = [
    ("Oğlak", (12, 22), (1, 19)),
    ("Kova", (1, 20), (2, 18)),
    ("Balık", (2, 19), (3, 20)),
    ("Koç", (3, 21), (4, 19)),
    ("Boğa", (4, 20), (5, 20)),
    ("İkizler", (5, 21), (6, 20)),
    ("Yengeç", (6, 21), (7, 22)),
    ("Aslan", (7, 23), (8, 22)),
    ("Başak", (8, 23), (9, 22)),
    ("Terazi", (9, 23), (10, 22)),
    ("Akrep", (10, 23), (11, 21)),
    ("Yay", (11, 22), (12, 21)),
]

PLANETS = [
    "Güneş",
    "Ay",
    "Merkür",
    "Venüs",
    "Mars",
    "Jüpiter",
    "Satürn",
    "Uranüs",
    "Neptün",
    "Plüton",
]


def _to_month_day(value: str):
    month, day = [int(part) for part in value.split("-")]
    return month, day


def zodiac_for_date(date_value: datetime) -> str:
    month = date_value.month
    day = date_value.day

    for sign_name, start, end in ZODIAC_SIGNS:
        start_month, start_day = start
        end_month, end_day = end
        if (month, day) >= (start_month, start_day):
            if (month, day) <= (end_month, end_day):
                return sign_name
    return "Capricorn"


def _hash_degree(seed: str, planet: str) -> float:
    total = sum(ord(ch) for ch in f"{seed}:{planet}")
    return (total % 360) + 1


def _planet_sign_and_house(degree: float) -> tuple[str, str]:
    signs = [
        "Koç",
        "Boğa",
        "İkizler",
        "Yengeç",
        "Aslan",
        "Başak",
        "Terazi",
        "Akrep",
        "Yay",
        "Oğlak",
        "Kova",
        "Balık",
    ]
    sign_index = int(degree // 30) % len(signs)
    house_index = int(degree // 30) % 12 + 1
    return signs[sign_index], f"{house_index}. Ev"


def _safe_format(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y %H:%M")
    return str(value)


def build_astrology_report(payload: dict[str, Any]) -> dict[str, Any]:
    birth_date = payload.get("birth_date") or "2000-01-01"
    birth_time = payload.get("birth_time") or "12:00"
    city = payload.get("city") or "Belirtilmedi"
    has_birth_date = bool(payload.get("birth_date", "").strip())

    parsed_date = datetime.fromisoformat(birth_date) if isinstance(birth_date, str) else datetime.strptime(str(birth_date), "%Y-%m-%d")
    dob = parsed_date
    sun_sign = zodiac_for_date(dob)
    ascendant = "Koç" if dob.day % 12 else "Aslan"
    moon_sign = "Yengeç" if dob.month % 2 else "Balık"

    summary = (
        f"Doğum tarihi girilmediği için genel bir {sun_sign} enerjisi yorumu hazırlanıyor. "
        f"Bu harita, duygusal sezgi ({moon_sign}) ve yükselen karakter ({ascendant}) açısından dengeli ve akıcı bir yol sunar."
        if not has_birth_date
        else (
            f"Doğum haritanız, özünüzde {sun_sign} karakteri taşıdığınızı ve duygusal dünyanızda {moon_sign} etkisinin öne çıktığını gösteriyor. "
            f"Yükseleniniz {ascendant}; bu yerleşimler özgüven, sezgi ve sosyal çekim gücünün dengeli bir karışımını anlatıyor."
        )
    )

    planet_positions = []
    for planet in PLANETS:
        degree = _hash_degree(f"{dob:%Y-%m-%d} {birth_time}", planet)
        sign, house = _planet_sign_and_house(degree)
        planet_positions.append(
            {
                "name": planet,
                "degree": round(degree, 1),
                "sign": sign,
                "house": house,
            }
        )

    return {
        "birth_details": {
            "date": _safe_format(dob) if has_birth_date else "Belirtilmedi",
            "time": birth_time,
            "city": city,
        },
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "ascendant": ascendant,
        "planet_positions": planet_positions,
        "summary": summary,
    }
