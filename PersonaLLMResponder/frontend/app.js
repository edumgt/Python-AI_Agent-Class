async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

const el = (id) => document.getElementById(id);

(async function init() {
  const meta = await fetchJson('/v1/project/meta');
  el('metaBox').textContent = JSON.stringify(meta, null, 2);
})();

el('saveBtn').addEventListener('click', async () => {
  const payload = {
    persona_id: el('personaId').value || null,
    name: el('name').value,
    role: el('role').value,
    tone: el('tone').value,
    speaking_rules: el('rules').value.split(',').map((v) => v.trim()).filter(Boolean),
  };
  const out = await fetchJson('/v1/persona/upsert', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  el('personaBox').textContent = JSON.stringify(out, null, 2);
  el('askPersonaId').value = out.persona_id;
  el('personaId').value = out.persona_id;
});

el('askBtn').addEventListener('click', async () => {
  const payload = {
    persona_id: el('askPersonaId').value,
    question: el('question').value,
    context: el('context').value,
    use_llm: el('useLlm').checked,
  };
  const out = await fetchJson('/v1/persona/answer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  el('answerBox').textContent = JSON.stringify(out, null, 2);
});
