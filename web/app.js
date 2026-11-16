let anomaly = false;
const labels = new Array();
const t2Data = new Array();
const speData = new Array();
const uclT2 = new Array();
const uclSpe = new Array();

const chartOpts = {
  responsive: true,
  animation: false,
  scales: {
    x: { ticks: { color: '#8b949e', maxTicksLimit: 6 }, grid: { color: '#21262d' } },
    y: { ticks: { color: '#8b949e' }, grid: { color: '#21262d' }, min: 0, max: 10 }
  },
  plugins: { legend: { labels: { color: '#e6edf3', boxWidth: 12 } } }
};

const t2Chart = new Chart(document.getElementById('t2Chart'), {
  type: 'line',
  data: {
    labels: labels,
    datasets: new Array(
      { label: 'T2_VALUE', data: t2Data, borderColor: '#58a6ff', tension: 0.25, pointRadius: 2 },
      { label: 'Upper Control Limit', data: uclT2, borderColor: '#f85149', borderDash: new Array(5, 5), pointRadius: 0 }
    )
  },
  options: chartOpts
});

const speChart = new Chart(document.getElementById('speChart'), {
  type: 'line',
  data: {
    labels: labels,
    datasets: new Array(
      { label: 'SPE_VALUE', data: speData, borderColor: '#3fb950', tension: 0.25, pointRadius: 2 },
      { label: 'Upper Control Limit', data: uclSpe, borderColor: '#f85149', borderDash: new Array(5, 5), pointRadius: 0 }
    )
  },
  options: chartOpts
});

function triggerFault() {
  anomaly = true;
  document.getElementById('banner').className = 'status-banner alarm';
  document.getElementById('banner').textContent = '🔴 CRITICAL GxP STATUS ALARM: PROCESS SHIFT & RESIDUAL EXCURSION BREACH DETECTED';
  document.getElementById('agentOutput').innerHTML = `
    <h3>🤖 Groq Autonomous LLM Diagnostic Hub — [BATCH ANOMALY REPORT]</h3>
    <p><strong>Diagnostic Classification:</strong> Unmodeled Disturbance (Dual T² &amp; SPE Excursion)</p>
    <p><strong>Probable Root-Cause Analysis:</strong> Agitation drive failure or mechanical coupling slip causing RPM to exceed the 130.0 upper limit (~158 RPM), introducing unmodeled shear stress not captured by the baseline PCA model.</p>
    <p><strong>Immediate SOP Corrective Actions:</strong> 1) Manually verify agitator shaft coupling integrity and motor current draw. 2) Inspect agitation_rpm control loop PID parameters against the 110.0–130.0 CPP range.</p>
  `;
}

function resetNormal() {
  anomaly = false;
  document.getElementById('banner').className = 'status-banner';
  document.getElementById('banner').textContent = '🟢 GOLDEN ENVELOPE VALIDATED: ALL CPPs WITHIN STATISTICAL CONTROL LIMITS';
  document.getElementById('agentOutput').innerHTML = `
    <h3>🤖 Groq Autonomous LLM Diagnostic Hub</h3>
    <p><strong>Status:</strong> Process restored to Golden Envelope. Hotelling T² and SPE metrics are back inside statistical control limits.</p>
  `;
}

function tick() {
  if (!document.getElementById('streamToggle').checked) return;

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

  labels.push(now);
  t2Data.push(Number(t2));
  speData.push(Number(spe));
  uclT2.push(6.0);
  uclSpe.push(4.5);

  if (labels.length > 15) {
    labels.shift();
    t2Data.shift();
    speData.shift();
    uclT2.shift();
    uclSpe.shift();
  }
  t2Chart.update();
  speChart.update();

  const tbody = document.getElementById('auditBody');
  const row = document.createElement('tr');
  const statusText = anomaly ? 'CRITICAL_DUAL_BREACH' : 'GOLDEN_ENVELOPE_VALIDATED';
  const statusClass = anomaly ? 'tag-breach' : 'tag-ok';
  row.innerHTML = `
    <td>${now}</td>
    <td class="${statusClass}">${statusText}</td>
    <td>${temp}</td>
    <td>${ph}</td>
    <td>${rpm}</td>
    <td>${t2}</td>
    <td>${spe}</td>
  `;
  tbody.prepend(row);
  if (tbody.rows.length > 8) tbody.deleteRow(8);
}

for (let i = 0; i < 6; i++) tick();
setInterval(tick, 1800);
