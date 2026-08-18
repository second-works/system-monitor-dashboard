const REFRESH_INTERVAL_MS = 5000;

function formatUptime(totalSeconds) {
  const seconds = Math.max(0, Math.floor(Number(totalSeconds) || 0));
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  return `${days}d ${hours}h ${minutes}m ${remainingSeconds}s`;
}

function formatGigabytes(value) {
  return `${Number(value).toFixed(1)} GB`;
}

function formatPercent(value) {
  return `${Number(value).toFixed(1)}%`;
}

function formatSystemInfo(data) {
  return {
    cpu: formatPercent(data.cpu_percent),
    memoryPercent: formatPercent(data.memory.percent),
    memoryDetail: `${formatGigabytes(data.memory.used_gb)} / ${formatGigabytes(data.memory.total_gb)}`,
    diskPercent: formatPercent(data.disk.percent),
    diskDetail: `${formatGigabytes(data.disk.used_gb)} / ${formatGigabytes(data.disk.total_gb)}`,
    os: data.os,
    uptime: formatUptime(data.uptime_seconds),
  };
}

function renderSystemInfo(data) {
  const display = formatSystemInfo(data);
  document.querySelector("#cpu-value").textContent = display.cpu;
  document.querySelector("#memory-percent").textContent = display.memoryPercent;
  document.querySelector("#memory-detail").textContent = display.memoryDetail;
  document.querySelector("#disk-percent").textContent = display.diskPercent;
  document.querySelector("#disk-detail").textContent = display.diskDetail;
  document.querySelector("#os-value").textContent = display.os;
  document.querySelector("#uptime-value").textContent = display.uptime;
}

function setLoadingState(isLoading) {
  document.querySelector("#status-text").textContent = isLoading ? "Updating…" : "Live";
}

function setErrorState(hasError) {
  const errorPanel = document.querySelector("#error-panel");
  errorPanel.hidden = !hasError;
  document.querySelector("#status-text").textContent = hasError ? "Update failed" : "Live";
}

async function updateDashboard() {
  if (updateDashboard.inFlight) {
    return;
  }
  updateDashboard.inFlight = true;
  setLoadingState(true);

  try {
    const response = await fetch("/api/system", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`System API returned ${response.status}`);
    }
    const data = await response.json();
    renderSystemInfo(data);
    setErrorState(false);
    document.querySelector("#last-update").textContent = new Date().toLocaleTimeString();
  } catch (error) {
    setErrorState(true);
    console.error(error);
  } finally {
    updateDashboard.inFlight = false;
  }
}

if (typeof window !== "undefined") {
  window.SystemMonitorDashboard = { formatUptime, formatSystemInfo, updateDashboard };
  window.addEventListener("DOMContentLoaded", () => {
    updateDashboard();
    window.setInterval(updateDashboard, REFRESH_INTERVAL_MS);
  });
}
