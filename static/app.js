const form = document.getElementById('fortune-form');
const resultEl = document.getElementById('result');
const loadingEl = document.getElementById('loading');
const submitButton = document.getElementById('submit-button');
const modeButtons = document.querySelectorAll('.mode-button');
const modeSections = document.querySelectorAll('.mode-section');
const apiBaseUrl = (window.ASTROFAL_API_URL || '').replace(/\/$/, '');

let selectedMode = 'both';

const modeLabels = {
  both: 'İkisini birlikte yorumla',
  birth: 'Burç falımı yorumla',
  cup: 'Kahve falımı yorumla',
};

function setMode(mode) {
  selectedMode = mode;
  modeButtons.forEach((button) => {
    button.classList.toggle('is-active', button.dataset.mode === mode);
  });
  modeSections.forEach((section) => {
    const isVisible = mode === 'both' || section.dataset.section === mode;
    section.classList.toggle('mode-hidden', !isVisible);
    section.querySelectorAll('input, select, textarea').forEach((field) => {
      field.disabled = !isVisible;
    });
  });
  submitButton.textContent = modeLabels[mode];
}

modeButtons.forEach((button) => {
  button.addEventListener('click', () => setMode(button.dataset.mode));
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);

  const hasBirthData = selectedMode !== 'cup' && !!(
    (formData.get('name') || '').toString().trim() ||
    (formData.get('birth_date') || '').toString().trim() ||
    ((formData.get('birth_time') || '').toString().trim() && formData.get('birth_time') !== '00:00') ||
    (formData.get('city') || '').toString().trim()
  );

  const hasImage = selectedMode !== 'birth' && !!(formData.get('file') && formData.get('file').size > 0);

  if (!hasBirthData && !hasImage) {
    resultEl.innerHTML = '<div class="card"><p>En az bir bölüm doldurmanız gerekiyor: doğum bilgileri veya kahve fincanı fotoğrafı.</p></div>';
    return;
  }

  loadingEl.classList.remove('hidden');
  resultEl.innerHTML = '';

  try {
    const response = await fetch(`${apiBaseUrl}/api/fortune`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const detail = errorData.detail;
      const message = typeof detail === 'string' ? detail : 'İstek başarısız oldu.';
      throw new Error(message);
    }

    const data = await response.json();
    const fortune = data.fortune || {};
    const chart = data.chart || {};
    const image = data.image_analysis || {};

    const birthInfo = chart.birth_details || {};
    const imageSummary = image.summary || 'Görsel analizi mevcut değil.';

    const imageMarkup = hasImage
      ? `
        <div class="card">
          <h3>Görsel analizi</h3>
          <p>${imageSummary}</p>
          <ul>
            ${(image.patterns || []).map((p) => `<li>${p}</li>`).join('')}
          </ul>
        </div>
      `
      : '';

    const chartMarkup = hasBirthData
      ? `
        <div class="card">
          <h3>Yıldız haritası</h3>
          <p><strong>Doğum tarihi:</strong> ${birthInfo.date || 'Belirtilmedi'}</p>
          <p><strong>Doğum saati:</strong> ${birthInfo.time || 'Belirtilmedi'}</p>
          <p><strong>Doğum yeri:</strong> ${birthInfo.city || 'Belirtilmedi'}</p>
          <p><strong>Güneş:</strong> ${chart.sun_sign || 'Belirlenmedi'}</p>
          <p><strong>Ay:</strong> ${chart.moon_sign || 'Belirlenmedi'}</p>
          <p><strong>Yükselen:</strong> ${chart.ascendant || 'Belirlenmedi'}</p>
        </div>
      `
      : '';

    resultEl.innerHTML = `
      ${imageMarkup}
      ${chartMarkup}

      <div class="card">
        <h3>Fal yorumu</h3>
        <p>${fortune.summary || 'Yorum hazırlanamadı.'}</p>
        <p><strong>Aşk:</strong> ${fortune.love || ''}</p>
        <p><strong>Kariyer:</strong> ${fortune.career || ''}</p>
        <p><strong>Para:</strong> ${fortune.money || ''}</p>
        <p><strong>Sağlık:</strong> ${fortune.health || ''}</p>
        <p><strong>Burç yorumu:</strong> ${fortune.burc_yorumu || ''}</p>
      </div>
    `;
  } catch (error) {
    resultEl.innerHTML = `<div class="card"><p>${error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.'}</p></div>`;
  } finally {
    loadingEl.classList.add('hidden');
  }
});
