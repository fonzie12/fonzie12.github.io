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

Açık adres: http://localhost:8000

## GitHub Pages ve üretim

Frontend için hedef adres: `https://fonzie12.github.io`.

GitHub Pages yalnızca statik frontend çalıştırdığı için FastAPI backend'i ayrı bir serviste yayınlayın. Bu proje için hazır `render.yaml` dosyası Render üzerinde backend oluşturur.

1. Projeyi `fonzie12.github.io` repository'sine gönderin.
2. Repository Settings > Pages bölümünde kaynak olarak GitHub Actions seçin.
3. Render'da bu repository'yi bağlayıp `render.yaml` servisini deploy edin.
4. GitHub repository Variables bölümüne `ASTROFAL_API_URL` adıyla Render backend adresini ekleyin.
5. Yeni push sonrasında frontend `https://fonzie12.github.io` adresinde backend'e bağlanır.

API adresi yerelde boş bırakıldığında frontend `http://localhost:8000/api/fortune` adresini kullanır.

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
