async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function parseValues(raw) {
  return raw
    .split(",")
    .map((v) => Number(v.trim()))
    .filter((v) => Number.isFinite(v));
}

document.getElementById("meta-btn").addEventListener("click", async () => {
  const box = document.getElementById("meta-box");
  box.textContent = "loading...";
  try {
    const data = await fetchJson("/v1/project/meta");
    box.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    box.textContent = String(error);
  }
});

document.getElementById("run-btn").addEventListener("click", async () => {
  const valuesRaw = document.getElementById("values").value;
  const note = document.getElementById("note").value || "frontend-run";
  const payload = {
    values: parseValues(valuesRaw),
    note,
  };

  const box = document.getElementById("run-box");
  box.textContent = "running...";
  try {
    const data = await fetchJson("/v1/project/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    box.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    box.textContent = String(error);
  }
});
