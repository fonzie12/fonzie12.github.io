# AstroFal

Yapay zeka destekli kahve fincanı falı web uygulaması prototipi.

## Özellikler
- Kahve fincanı görseli yükleme
- Doğum tarihi, saati ve yeri toplama
- Astroloji haritası özeti oluşturma
- Yapay zeka tabanlı fal yorumu üretme

## Yerelde çalıştırma

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Açık adres: http://localhost:8000/docs

## Ortam değişkenleri
Bir `.env` dosyası oluşturup şu bilgileri ekleyin:

```env
NVIDIA_API_KEY=your_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.2-90b-vision-instruct
```

## Geliştirme kuralı
- Her değişiklikten sonra proje, kullanıcı akışı baştan sona çalıştırılarak test edilmelidir.
- Sonuç kullanıcıya sunulmadan önce hata, tarayıcı konsolu ve API yanıtları kontrol edilmelidir.
- Bir bug veya hata bulunursa düzeltilmeden proje sunulmamalıdır.
