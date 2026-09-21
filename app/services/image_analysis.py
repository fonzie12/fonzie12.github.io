from __future__ import annotations

from typing import Any


def analyze_uploaded_image(file: Any | None) -> dict[str, Any]:
    if file is None:
        return {
            "patterns": ["Görsel yüklenmedi; genel sembolik okuma kullanılıyor."],
            "mood": "Dengeli ve yeni duygusal sinyallere açık.",
            "symbols": ["çizgi", "çember", "denge yolu"],
            "summary": "Görsel okuma, önünüzde sakin ama enerjik bir yol olduğunu gösteriyor.",
        }

    filename = getattr(file, "filename", "coffee_cup")
    return {
        "patterns": [
            "Kıvrımlı çizgiler duygusal hareketi ve ilişkilerdeki değişimi gösteriyor.",
            "Merkezdeki şekil kişisel istikrara ve güçlü karar alma becerisine işaret ediyor.",
            "Yumuşak kenarlar, güvendiğiniz kişilerden gelecek desteğe açık olduğunuzu anlatıyor.",
        ],
        "mood": "Sıcak, düşünceli ve sosyal açıdan çekici.",
        "symbols": ["hilal", "çember", "iç denge"],
        "summary": f"'{filename}' fincan görüntüsü duygusal netliğin ve önemli bir dönüm noktasının güçlü işaretlerini taşıyor. Şekiller, ilişkilerde odaklanacağınız ve iç güveninizin artacağı bir döneme işaret ediyor.",
    }
