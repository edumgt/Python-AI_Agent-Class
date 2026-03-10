async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

function byId(id) {
  return document.getElementById(id);
}

(async function init() {
  const meta = await fetchJson('/v1/project/meta');
  byId('metaBox').textContent = JSON.stringify(meta, null, 2);
})();

byId('createBtn').addEventListener('click', async () => {
  const payload = {
    name: byId('name').value,
    base_voice: byId('baseVoice').value,
    style_tags: byId('styleTags').value.split(',').map((v) => v.trim()).filter(Boolean),
  };
  const out = await fetchJson('/v1/voice/profiles', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  byId('profileBox').textContent = JSON.stringify(out, null, 2);
  byId('trainProfileId').value = out.profile_id;
  byId('synthProfileId').value = out.profile_id;
});

byId('trainBtn').addEventListener('click', async () => {
  const payload = {
    profile_id: byId('trainProfileId').value,
    recordings_count: Number(byId('recordings').value),
    total_minutes: Number(byId('minutes').value),
    noise_level: Number(byId('noise').value),
    pronunciation_score: Number(byId('pron').value),
    emotion_score: Number(byId('emo').value),
  };
  const out = await fetchJson('/v1/voice/train', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  byId('trainBox').textContent = JSON.stringify(out, null, 2);
});

byId('synthBtn').addEventListener('click', async () => {
  const payload = {
    profile_id: byId('synthProfileId').value,
    text: byId('synthText').value,
    style_strength: Number(byId('strength').value),
  };
  const out = await fetchJson('/v1/voice/synthesize', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  byId('synthBox').textContent = JSON.stringify(out, null, 2);
});
