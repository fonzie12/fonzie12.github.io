from __future__ import annotations

import os
from typing import Any

import httpx

from app.config import NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL


def _fallback_story(image_analysis: dict[str, Any], chart: dict[str, Any], tone: str = "warm") -> dict[str, Any]:
    sign = chart.get("sun_sign", "Koç")
    mood = image_analysis.get("mood", "dengeli")
    summary = image_analysis.get("summary", "Semboller, hayatınızda dengeli ve güzel bir akış olduğunu anlatıyor.")

    return {
        "tone": tone,
        "headline": f"{sign} enerjisi güçlü bir duygusal değişime alan açıyor.",
        "summary": (
            f"Fincanınız istikrarlı bir değişimi, sessiz bir cesareti ve doğru zamanı anlatıyor. {summary} "
            f"{sign} doğanız, tanıdık ama her zamankinden daha derin hissettiren işaretlere güvenmenizi söylüyor. "
            "Önümüzdeki dönemde küçük görünen bir kararın hayatınızda büyük bir kapı açma ihtimali var. "
            "Sezgilerinizi dinlerken somut adımlar atmanız, bu güzel enerjiyi kalıcı bir sonuca dönüştürecek."
        ),
        "love": (
            "Anlamlı bir yakınlık beklediğinizden daha yoğun hissedilebilir. "
            "Fazla analiz etmek yerine kırılganlığınıza izin vermeniz bu bağı güçlendirecek. "
            "Geçmişten kalan bir konu yeniden gündeme gelirse, bu kez kendinizi daha açık ifade edeceksiniz. "
            "Kalbinizi korurken karşınızdaki kişinin çabasını da görmeye çalışmanız ilişkinin dengesini değiştirebilir. "
            "Bekarsanız, samimi bir sohbetin zamanla daha derin bir bağa dönüşme ihtimali yüksek görünüyor."
        ),
        "career": (
            "Kariyer fırsatları konuşmalar, doğru zamanlama ve gerektiğinde cesurca söz almanız sayesinde karşınıza çıkabilir. "
            "Uzun süredir emek verdiğiniz bir işin karşılığını görünür biçimde almaya başlayabilirsiniz. "
            "Çevrenizdeki bir kişinin önerisi veya desteği yeni bir kapı açabilir. "
            "Karar verirken yalnızca kısa vadeli kazanca değil, size öğreteceği becerilere de bakın. "
            "Kendinizi geri planda tutmayı bıraktığınızda yetenekleriniz daha kolay fark edilecek."
        ),
        "money": (
            "Sabırlı kaldığınızda ve duygusal kararları aceleyle vermediğinizde maddi akışınız daha dengeli hale gelecek. "
            "Yakın zamanda beklemediğiniz bir ödeme veya küçük bir kazanç moralinizi yükseltebilir. "
            "Bununla birlikte, bu parayı anlık bir hevesle harcamak yerine önceliklerinize ayırmanız faydalı olacak. "
            "Eski bir borç, abonelik veya gereksiz masraf kalemini kapatmak bütçenizde rahatlama sağlayabilir. "
            "Önümüzdeki dönemde düzenli birikim, büyük ve riskli hamlelerden daha çok işinize yarayacak."
        ),
        "health": (
            "Enerjiniz; daha sakin bir tempo, yeterli dinlenme ve üzerinize aldığınız gereksiz baskıları azaltmanızla güçlenecek. "
            "Zihniniz çok dolduğunda bedeninizin verdiği küçük sinyalleri görmezden gelmemeye çalışın. "
            "Uyku düzeninizi toparlamak ve gün içinde kısa molalar vermek size beklediğinizden fazla iyi gelebilir. "
            "Kendinize ayırdığınız zaman bir lüks değil, üretkenliğinizi koruyan temel bir ihtiyaç olacak. "
            "Bu yorum tıbbi tavsiye yerine kendinize daha şefkatli davranmanız için bir hatırlatma niteliğinde."
        ),
        "personal_message": (
            f"Falınızdaki genel hava {mood}. "
            "İçinizde büyüttüğünüz bir niyet artık daha görünür hale geliyor. "
            "Bu süreçte herkesin beklentisini karşılamaya çalışmak yerine kendi sesinizi duymanız önemli. "
            "Doğru olduğuna inandığınız şeye nazik ama kararlı adımlarla ilerleyin. "
            "Önünüzdeki değişim, kendinize verdiğiniz değeri artırdığınız ölçüde güzelleşecek."
        ),
        "burc_yorumu": (
            f"{sign} karakteri, bu süreçte kararlılık ve sezgisel karar alma gücünü öne çıkarıyor. "
            "Duygularınız daha net hale gelecek ve neyi gerçekten istediğinizi daha kolay fark edeceksiniz. "
            "Sabırsız davrandığınız anlarda bile içinizdeki güçlü yön size yeniden denge kazandıracak. "
            "Çevrenizdekiler sizin güven veren ve çözüm üreten tarafınıza daha çok ihtiyaç duyabilir. "
            f"Bu dönemin ana mesajı, {sign} doğanızı saklamadan ama esnekliğinizi de koruyarak ilerlemeniz."
        ),
    }


async def generate_fortune(image_analysis: dict[str, Any], chart: dict[str, Any], tone: str = "warm") -> dict[str, Any]:
    if NVIDIA_API_KEY:
        prompt = (
            "Sen şefkatli, samimi ve güven veren bir fal yorumcususun. "
            "Aşağıdaki görsel analizi ve doğum haritası verilerini kullanarak kullanıcıya kişisel, sıcak ve akıcı bir fal yorumunu Türkçe olarak üret. "
            "Her bölüm en az 5 tam cümleden oluşsun; aşk, kariyer, para, sağlık ve burç yorumu bölümlerini ayrıntılı yaz. "
            "Ek olarak 'love', 'career', 'money', 'health', 'burc_yorumu' alanları içeren JSON döndür."
            f"\n\nGörsel analizi: {image_analysis}\n\nDoğum haritası: {chart}"
        )

        payload = {
            "model": NVIDIA_MODEL,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
        }

        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(
                    f"{NVIDIA_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {NVIDIA_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                return {"tone": tone, "raw_response": text}
        except Exception:
            return _fallback_story(image_analysis, chart, tone=tone)

    return _fallback_story(image_analysis, chart, tone=tone)
