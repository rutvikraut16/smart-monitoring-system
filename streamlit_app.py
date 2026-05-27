import streamlit as st
import random
import time

st.set_page_config(page_title="Smart Monitoring System", layout="wide")

# ── Thresholds ─────────────────────────────────────────
THRESHOLDS = {
    "temp":  70,
    "hum":   80,
    "pres":  1020,
    "cpu":   80,
}

# ── CSS for red glow effect ────────────────────────────
st.markdown("""
<style>
.metric-normal {
    background-color: #1a1f2e;
    border: 1px solid #2a3550;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    transition: all 0.4s ease;
}
.metric-danger {
    background-color: rgba(220, 38, 38, 0.15);
    border: 1px solid rgba(220, 38, 38, 0.6);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 0 18px rgba(220, 38, 38, 0.35);
    transition: all 0.4s ease;
}
.metric-label {
    font-size: 11px;
    letter-spacing: 2px;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value-normal {
    font-size: 32px;
    font-weight: 700;
    color: #00f5a0;
    font-family: monospace;
}
.metric-value-danger {
    font-size: 32px;
    font-weight: 700;
    color: #f87171;
    font-family: monospace;
}
.metric-threshold {
    font-size: 10px;
    color: #475569;
    margin-top: 4px;
    font-family: monospace;
}
.metric-status-ok   { font-size: 10px; color: #00f5a0; margin-top: 4px; font-family: monospace; }
.metric-status-warn { font-size: 10px; color: #f87171; margin-top: 4px; font-family: monospace; }

.feed-item-normal { font-family: monospace; font-size: 12px; color: #94a3b8; padding: 3px 0; }
.feed-item-alert  { font-family: monospace; font-size: 12px; color: #f87171; padding: 3px 0; }

div[data-testid="stMetric"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("## ⬡ Smart Monitoring System")
st.caption("Live sensor feed — updates every 2 seconds")

# ── Layout placeholders ────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
box_temp = col1.empty()
box_hum  = col2.empty()
box_pres = col3.empty()
box_cpu  = col4.empty()

st.divider()

chart_col1, chart_col2 = st.columns(2)
chart_col1.markdown("**Temperature History**")
chart_col2.markdown("**CPU Load History**")
temp_chart = chart_col1.empty()
cpu_chart  = chart_col2.empty()

chart_col3, chart_col4 = st.columns(2)
chart_col3.markdown("**Humidity History**")
chart_col4.markdown("**Pressure History**")
hum_chart  = chart_col3.empty()
pres_chart = chart_col4.empty()

st.divider()
alert_area = st.empty()
st.markdown("**Live Feed Log**")
feed_area  = st.empty()

# ── History buffers ────────────────────────────────────
temp_hist = []
cpu_hist  = []
hum_hist  = []
pres_hist = []
feed_log  = []

# ── Helper: build metric card HTML ────────────────────
def metric_card(label, value, unit, threshold, is_danger):
    card_class  = "metric-danger"  if is_danger else "metric-normal"
    value_class = "metric-value-danger" if is_danger else "metric-value-normal"
    status_class = "metric-status-warn" if is_danger else "metric-status-ok"
    status_text  = "DANGER" if is_danger else "NORMAL"
    return f"""
    <div class="{card_class}">
      <div class="metric-label">{label}</div>
      <div class="{value_class}">{value}{unit}</div>
      <div class="metric-threshold">Threshold: {threshold}{unit}</div>
      <div class="{status_class}">{'⚠ ' if is_danger else '● '}{status_text}</div>
    </div>
    """

# ── Main loop ──────────────────────────────────────────
while True:
    temp = random.randint(20, 100)
    hum  = random.randint(30, 90)
    pres = random.randint(995, 1025)
    cpu  = random.randint(10, 95)
    ts   = time.strftime("%H:%M:%S")

    temp_danger = temp > THRESHOLDS["temp"]
    hum_danger  = hum  > THRESHOLDS["hum"]
    pres_danger = pres > THRESHOLDS["pres"]
    cpu_danger  = cpu  > THRESHOLDS["cpu"]

    # Metric cards with red glow on danger
    box_temp.markdown(metric_card("Temperature", temp, "°C",  THRESHOLDS["temp"],  temp_danger), unsafe_allow_html=True)
    box_hum.markdown( metric_card("Humidity",    hum,  "%",   THRESHOLDS["hum"],   hum_danger),  unsafe_allow_html=True)
    box_pres.markdown(metric_card("Pressure",    pres, " hPa",THRESHOLDS["pres"],  pres_danger), unsafe_allow_html=True)
    box_cpu.markdown( metric_card("CPU Load",    cpu,  "%",   THRESHOLDS["cpu"],   cpu_danger),  unsafe_allow_html=True)

    # Chart history (last 20 points)
    temp_hist.append(temp); cpu_hist.append(cpu)
    hum_hist.append(hum);   pres_hist.append(pres)
    for h in [temp_hist, cpu_hist, hum_hist, pres_hist]:
        if len(h) > 20: h.pop(0)

    temp_chart.line_chart({"Temp (°C)":    temp_hist})
    cpu_chart.line_chart( {"CPU (%)" :     cpu_hist})
    hum_chart.line_chart( {"Humidity (%)": hum_hist})
    pres_chart.line_chart({"Pressure (hPa)": pres_hist})

    # Alert banner
    alerts = []
    if temp_danger: alerts.append(f"Temp {temp}°C > {THRESHOLDS['temp']}°C")
    if hum_danger:  alerts.append(f"Humidity {hum}% > {THRESHOLDS['hum']}%")
    if pres_danger: alerts.append(f"Pressure {pres} > {THRESHOLDS['pres']} hPa")
    if cpu_danger:  alerts.append(f"CPU {cpu}% > {THRESHOLDS['cpu']}%")

    if alerts:
        alert_area.error("⚠ ALERTS: " + " | ".join(alerts))
    else:
        alert_area.success(f"[{ts}] All systems normal")

    # Feed log
    any_danger = temp_danger or hum_danger or pres_danger or cpu_danger
    status = "ALERT" if any_danger else "OK"
    msg = f"[{ts}] T={temp}°C  H={hum}%  P={pres}hPa  CPU={cpu}%  [{status}]"
    feed_log.insert(0, (msg, any_danger))
    if len(feed_log) > 15: feed_log.pop()

    feed_html = "".join([
        f'<div class="{"feed-item-alert" if danger else "feed-item-normal"}">{m}</div>'
        for m, danger in feed_log
    ])
    feed_area.markdown(feed_html, unsafe_allow_html=True)

    time.sleep(2)