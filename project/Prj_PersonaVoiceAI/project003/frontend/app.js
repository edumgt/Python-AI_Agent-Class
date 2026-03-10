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

el('bootstrapBtn').addEventListener('click', async () => {
  const out = await fetchJson('/v1/knowledge/bootstrap', {method: 'POST'});
  el('knowledgeBox').textContent = JSON.stringify(out, null, 2);
});

el('listBtn').addEventListener('click', async () => {
  const out = await fetchJson('/v1/knowledge/list');
  el('knowledgeBox').textContent = JSON.stringify(out, null, 2);
});

el('answerBtn').addEventListener('click', async () => {
  const payload = {
    persona_name: el('persona').value,
    style: el('style').value,
    question: el('question').value,
    top_k: Number(el('topk').value),
  };
  const out = await fetchJson('/v1/custom/answer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  el('answerBox').textContent = JSON.stringify(out, null, 2);
});
