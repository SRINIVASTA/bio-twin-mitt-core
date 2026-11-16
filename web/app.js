let anomaly = false;
const t2Series = new Array();
const speSeries = new Array();

function getCanvas(primaryId, fallbackId) {
  return document.getElementById(primaryId) || document.getElementById(fallbackId);
}

function drawSeries(primaryId, fallbackId, series, uclVal, lineColor) {
  const canvas = getCanvas(primaryId, fallbackId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width || 500;
  const h = canvas.height || 170;
  const maxVal = 10.0;

  ctx.clearRect(0, 0, w, h);

  ctx.strokeStyle = '#21262d';
  ctx.lineWidth = 1;
  for (let g = 1; g <= 4; g++) {
    const gy = (h / 5) * g;
    ctx.beginPath();
    ctx.moveTo(0, gy);
    ctx.lineTo(w, gy);
    ctx.stroke();
  }

  const uclY = h - (uclVal / maxVal) * h;
  ctx.strokeStyle = '#f85149';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, uclY);
  ctx.lineTo(w, uclY);
  ctx.stroke();

  if (series.length < 2) return;
  ctx.strokeStyle = lineColor;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  const stepX = w / 19;
  series.forEach(function(val, idx) {
    const x = idx * stepX;
    const y = h - (Math.min(val, maxVal) / maxVal) * h;
    if (idx === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function triggerFault() {
  anomaly = true;
  document.getElementById('banner').className = 'status-banner alarm';
  document.getElementById('banner').textContent = '🔴 CRITICAL GxP STATUS ALARM: PROCESS SHIFT & RESIDUAL EXCURSION BREACH DETECTED';
  document.getElementById('agentOutput').innerHTML =
    '<h3>🤖 Groq Autonomous LLM Diagnostic Hub — [BATCH ANOMALY REPORT]</h3>' +
    '<p><strong>Diagnostic Classification:</strong> Unmodeled Disturbance (Dual T² &amp; SPE Excursion)</p>' +
    '<p><strong>Probable Root-Cause Analysis:</strong> Agitation drive failure or mechanical coupling slip causing RPM to exceed the 130.0 upper limit (~158 RPM), introducing unmodeled shear stress not captured by the baseline PCA model.</p>' +
    '<p><strong>Immediate SOP Corrective Actions:</strong> 1) Manually verify agitator shaft coupling integrity and motor current draw. 2) Inspect agitation_rpm control loop PID parameters against the 110.0–130.0 CPP range.</p>';
  tick(true);
}

function resetNormal() {
  anomaly = false;
  document.getElementById('banner').className = 'status-banner';
  document.getElementById('banner').textContent = '🟢 GOLDEN ENVELOPE VALIDATED: ALL CPPs WITHIN STATISTICAL CONTROL LIMITS';
  document.getElementById('agentOutput').innerHTML =
    '<h3>🤖 Groq Autonomous LLM Diagnostic Hub</h3>' +
    '<p><strong>Status:</strong> Process restored to Golden Envelope. Hotelling T² and SPE metrics are back inside statistical control limits.</p>';
  tick(true);
}

function tick(force) {
  const toggle = document.getElementById('streamToggle');
  if (!force && toggle && !toggle.checked) return;

  const now = new Date().toLocaleTimeString('en-GB');
  const temp = (25.0 + (Math.random() - 0.5) * 0.1).toFixed(2);
  const ph = (6.48 + (Math.random() - 0.5) * 0.06).toFixed(2);
  const rpm = anomaly ? (158 + Math.random() * 6).toFixed(2) : (120 + (Math.random() - 0.5) * 3).toFixed(2);
  const air = (250 + (Math.random() - 0.5) * 2).toFixed(2);
  const feed = (0.50 + (Math.random() - 0.5) * 0.02).toFixed(2);
  const t2 = anomaly ? (8.2 + Math.random() * 0.8).toFixed(2) : (2.2 + Math.random() * 0.4).toFixed(2);
  const spe = anomaly ? (6.1 + Math.random() * 0.7).toFixed(2) : (1.4 + Math.random() * 0.3).toFixed(2);

  document.getElementById('k-temp').textContent = temp + ' °C';
  document.getElementById('k-ph').textContent = ph;
  document.getElementById('k-rpm').textContent = rpm + ' RPM';
  document.getElementById('k-air').textContent = air + ' L/m';
  document.getElementById('k-feed').textContent = feed + ' kg/hr';

  t2Series.push(Number(t2));
  speSeries.push(Number(spe));
  if (t2Series.length > 20) {
    t2Series.shift();
    speSeries.shift();
  }

  drawSeries('t2Canvas', 't2Chart', t2Series, 6.0, '#58a6ff');
  drawSeries('speCanvas', 'speChart', speSeries, 4.5, '#3fb950');

  const tbody = document.getElementById('auditBody');
  if (tbody) {
    const row = document.createElement('tr');
    const statusText = anomaly ? 'CRITICAL_DUAL_BREACH' : 'GOLDEN_ENVELOPE_VALIDATED';
    const statusClass = anomaly ? 'tag-breach' : 'tag-ok';
    row.innerHTML =
      '<td>' + now + '</td>' +
      '<td class="' + statusClass + '">' + statusText + '</td>' +
      '<td>' + temp + '</td>' +
      '<td>' + ph + '</td>' +
      '<td>' + rpm + '</td>' +
      '<td>' + t2 + '</td>' +
      '<td>' + spe + '</td>';
    tbody.prepend(row);
    if (tbody.rows.length > 8) tbody.deleteRow(8);
  }
}

window.addEventListener('DOMContentLoaded', function() {
  for (let i = 0; i < 8; i++) tick(true);
  setInterval(function() { tick(false); }, 1500);
});
