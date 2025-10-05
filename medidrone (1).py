# triage.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# ------------------------------
# Function: AI Triage Simulation
# ------------------------------
def show_triage():
    st.title("AI Triage System & Drone Simulation")

    # Severity Selection
    severity = st.selectbox("Select patient severity:", ["Low", "Medium", "High"])

    # Assign priority based on severity
    priority_map = {"Low": "Normal Priority", "Medium": "Normal Priority", "High": "Launch Immediately"}
    priority = priority_map[severity]

    st.subheader(f"Assigned Priority: {priority}")

    # Map simulation
    st.subheader("Drone Route Simulation")
    # Coordinates: start, patient, base (example locations)
    start = [12.9716, 77.5946]      # Drone base
    patient = [12.9750, 77.6050]    # Patient location
    end = [12.9716, 77.5946]        # Return to base

    # Create folium map
    m = folium.Map(location=start, zoom_start=14)
    folium.Marker(start, tooltip="Drone Base", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(patient, tooltip="Patient", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(end, tooltip="Return Base", icon=folium.Icon(color="blue")).add_to(m)

    # Draw route
    folium.PolyLine([start, patient, end], color="purple", weight=5, opacity=0.8).add_to(m)

    st_folium(m, width=700, height=400)

    # Fake flight steps animation
    st.subheader("Drone Flight Status")
    steps = ["Taking Off", "En Route", "Delivered", "Returning"]
    status_text = st.empty()

    for step in steps:
        status_text.text(f"Drone Status: {step}")
        time.sleep(1.5)
    status_text.text("Drone Status: Completed ✅")


# --------------------------------------
# Function: Doctor–Patient Consultation
# --------------------------------------
def show_consultation():
    st.title("Telecommunication Module: Doctor–Patient Interaction")

    # Video Consultation Simulation
    st.subheader("Video Consultation")
    sample_video = "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
    st.video(sample_video)

    # Chat Simulation
    st.subheader("Chat with Doctor")
    user_message = st.text_area("Type your message here:")
    if st.button("Send"):
        if user_message.strip() == "":
            st.warning("Please type a message!")
        else:
            # Fake doctor response
            responses = {
                "hello": "Hello! How are you feeling today?",
                "fever": "I see. Please take rest and stay hydrated.",
                "pain": "Can you describe the severity of the pain?",
            }
            user_lower = user_message.lower()
            reply = "Doctor: " + responses.get(user_lower, "Doctor: Thank you for the info. We'll guide you further.")
            st.text_area("Chat History", value=f"You: {user_message}\n{reply}", height=150)


# --------------------------------------
# Optional: Run standalone in Streamlit
# --------------------------------------
if __name__ == "__main__":
    st.sidebar.title("MediDrone AI")
    option = st.sidebar.selectbox("Select Module", ["Triage Module", "Telecommunication Module"])
    if option == "Triage Module":
        show_triage()
    else:
        show_consultation()



import streamlit as st
import random
import time

# --- Initialize session state ---
if "control_mode" not in st.session_state:
    st.session_state.control_mode = "AUTO"
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- Helper functions ---
def detect_birds():
    """Simulate AI bird detection with random chance"""
    if random.random() < 0.3:  # 30% chance of bird appearing
        distance = random.randint(5, 50)  # meters
        return {"present": True, "distance": distance}
    return {"present": False}

def assess_threat(bird):
    """Decide threat level based on distance"""
    if not bird["present"]:
        return "NONE"
    if bird["distance"] > 20:
        return "MONITOR"
    elif bird["distance"] > 10:
        return "AVOID"
    else:
        return "EMERGENCY"

def plan_maneuver(level):
    """Pick avoidance maneuver"""
    options = {
        "AVOID": random.choice(["Climb +2m", "Sidestep Right", "Hover"]),
        "EMERGENCY": random.choice(["Abort Mission", "Return-To-Home", "Descend Rapidly"]),
    }
    return options.get(level, "Continue Mission")

def log_event(event):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {event}")

# --- Streamlit UI ---
st.title("🚁 Drone Bird Avoidance Simulation")

st.sidebar.header("Control Panel")
if st.sidebar.button("Switch to AUTO Mode"):
    st.session_state.control_mode = "AUTO"
    log_event("Operator switched to AUTO mode")

if st.sidebar.button("Switch to REMOTE Mode"):
    st.session_state.control_mode = "REMOTE"
    log_event("Operator switched to REMOTE mode")

play_sound = st.sidebar.checkbox("Enable Sound Deterrent", value=True)

st.write(f"**Current Control Mode:** {st.session_state.control_mode}")

# --- Simulation step ---
if st.button("Run Simulation Step"):
    bird = detect_birds()
    threat = assess_threat(bird)

    if st.session_state.control_mode == "REMOTE":
        log_event("REMOTE control active — operator is flying")
        st.success("REMOTE: Operator in control, no AI action")
    else:
        if threat == "NONE":
            log_event("No bird detected — continuing mission")
            st.info("AUTO: No bird detected. Drone continues mission.")
        elif threat == "MONITOR":
            log_event(f"Bird detected at safe distance ({bird['distance']}m). Monitoring.")
            st.warning(f"AUTO: Bird detected at {bird['distance']}m — monitoring.")
        elif threat == "AVOID":
            maneuver = plan_maneuver("AVOID")
            log_event(f"Bird nearby ({bird['distance']}m) — executing avoidance: {maneuver}")
            st.error(f"AUTO: Avoidance maneuver triggered → {maneuver}")
            if play_sound:
                st.write("🔊 Sound deterrent activated")
        elif threat == "EMERGENCY":
            maneuver = plan_maneuver("EMERGENCY")
            log_event(f"EMERGENCY! Bird very close ({bird['distance']}m) — {maneuver}")
            st.error(f"AUTO: EMERGENCY action → {maneuver}")
            if play_sound:
                st.write("🔊 Sound deterrent activated (emergency)")

# --- Telemetry log ---
st.subheader("📋 Drone Telemetry Log")
for entry in reversed(st.session_state.logs[-10:]):  # show last 10 logs
    st.write(entry)



# app.py
# Mini test app to run only Yuva's diagnostics module

import streamlit as st
from diagnostics import show_diagnostics

st.set_page_config(page_title="MediDrone — Diagnostics Test", layout="centered")

st.sidebar.title("MediDrone Prototype (Test Mode)")
page = st.sidebar.radio("Choose Module", ["Diagnostics"])

if page == "Diagnostics":
    show_diagnostics()



# vitals_streamlit.py
"""
Streamlit-friendly Biosensor Vitals Simulator
- ECG waveform (synthetic)
- SpO₂ values (random)
- Body temperature values (random)
- Real-time plotting without blocking loops
"""

import streamlit as st
import numpy as np
from scipy.signal import convolve
import time
from collections import deque
import math
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# -------------------------
# Helper functions
# -------------------------
def make_beat_template(fs=250):
    t = np.linspace(-0.5, 0.8, int(1.3 * fs), endpoint=False)
    beat = np.zeros_like(t)
    def gauss(center, width, amp):
        return amp * np.exp(-0.5 * ((t - center)/width)**2)
    beat += gauss(-0.18, 0.03, 0.08)
    beat += gauss(-0.02, 0.005, -0.05)
    beat += gauss(0.0, 0.006, 1.0)
    beat += gauss(0.03, 0.006, -0.12)
    beat += gauss(0.32, 0.05, 0.25)
    beat = beat / np.max(np.abs(beat))
    return beat, t

def generate_ecg_chunk(hr_bpm, duration_s, fs, beat_template, noise_std=0.01, beat_jitter=0.02):
    n_samples = int(duration_s * fs)
    t = np.arange(n_samples)/fs
    avg_rr = 60.0/hr_bpm
    window_len = duration_s + 2.0
    Nbig = int(window_len*fs)
    impulses = np.zeros(Nbig)
    offset = random.uniform(0, avg_rr)
    beat_time = -1.0 + offset
    while beat_time < window_len:
        idx = int(round((beat_time + 1.0) * fs))
        if 0 <= idx < Nbig:
            impulses[idx] = 1.0
        beat_time += avg_rr*(1.0 + random.uniform(-beat_jitter, beat_jitter))
    ecg_big = convolve(impulses, beat_template, mode='same')
    start_idx = int(1.0*fs)
    ecg = ecg_big[start_idx:start_idx + n_samples]
    baseline = 0.02*np.sin(2*np.pi*0.2*t + random.uniform(0,2*math.pi))
    ecg = ecg + baseline + np.random.normal(0, noise_std, size=ecg.shape)
    return t, ecg

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Vitals Monitoring Simulator", layout="wide")
st.title("Vitals Monitoring Simulator — ECG, SpO₂, Body Temp")

# Auto-refresh every 200 ms
st_autorefresh(interval=200, key="vitals_refresh")

# -------------------------
# Controls
# -------------------------
col_ctrl, col_display = st.columns([1,3])
with col_ctrl:
    st.header("Controls")
    fs = st.slider("Sampling rate (Hz)", 125, 1000, 250, step=25)
    buffer_seconds = st.slider("ECG buffer (seconds shown)", 5, 30, 10)
    hr = st.slider("Heart rate (bpm)", 40, 140, 72)
    noise_level = st.slider("ECG noise level (std dev)", 0.0, 0.05, 0.01, step=0.001)
    beat_jitter = st.slider("Beat interval jitter (±fraction)", 0.0, 0.1, 0.02, step=0.005)
    spo2_baseline = st.slider("SpO₂ baseline (%)", 85, 100, 97)
    temp_baseline = st.slider("Body temp baseline (°C)", 35.0, 39.0, 36.6, step=0.1)
    run_sim = st.checkbox("Run simulation", value=True)

with col_display:
    st.header("Live signals")
    ecg_placeholder = st.empty()
    spo2_placeholder = st.empty()
    temp_placeholder = st.empty()
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    spo2_metric = metric_col1.empty()
    temp_metric = metric_col2.empty()
    hr_metric = metric_col3.empty()

# -------------------------
# Initialize buffers
# -------------------------
if "ecg_buffer" not in st.session_state:
    max_len = int(buffer_seconds*fs)
    st.session_state.ecg_buffer = deque([0.0]*max_len, maxlen=max_len)
    st.session_state.time_buffer = deque(np.linspace(-buffer_seconds,0,max_len,endpoint=False), maxlen=max_len)
    st.session_state.spo2_buffer = deque([spo2_baseline]*60, maxlen=60)
    st.session_state.temp_buffer = deque([temp_baseline]*60, maxlen=60)
    st.session_state.last_update = time.time()

beat_template, _ = make_beat_template(fs=fs)
expected_len = int(buffer_seconds*fs)
if st.session_state.ecg_buffer.maxlen != expected_len:
    st.session_state.ecg_buffer = deque([0.0]*expected_len, maxlen=expected_len)
    st.session_state.time_buffer = deque(np.linspace(-buffer_seconds,0,expected_len,endpoint=False), maxlen=expected_len)

# -------------------------
# Update buffers (one chunk per refresh)
# -------------------------
if run_sim:
    chunk_duration = 0.15
    _, ecg_chunk = generate_ecg_chunk(hr, chunk_duration, fs, beat_template, noise_level, beat_jitter)
    for s in ecg_chunk:
        st.session_state.ecg_buffer.append(s)
    last_time = st.session_state.time_buffer[-1] if st.session_state.time_buffer else 0.0
    for _ in ecg_chunk:
        last_time += 1.0/fs
        st.session_state.time_buffer.append(last_time)
    times = np.array(st.session_state.time_buffer)
    times = times - times[-1]
    st.session_state.time_buffer = deque(times, maxlen=st.session_state.time_buffer.maxlen)

    now = time.time()
    if now - st.session_state.last_update >= 1.0:
        st.session_state.last_update = now
        prev_spo2 = st.session_state.spo2_buffer[-1]
        new_spo2 = prev_spo2 + np.random.normal(0,0.15)
        new_spo2 += (spo2_baseline - new_spo2)*0.02
        new_spo2 = float(np.clip(new_spo2,80,100))
        st.session_state.spo2_buffer.append(new_spo2)

        prev_temp = st.session_state.temp_buffer[-1]
        new_temp = prev_temp + np.random.normal(0,0.01)
        new_temp += (temp_baseline - new_temp)*0.01
        new_temp = float(np.clip(new_temp,35.0,39.0))
        st.session_state.temp_buffer.append(new_temp)

# -------------------------
# Plotting
# -------------------------
# ECG
fig_ecg = go.Figure()
fig_ecg.add_trace(go.Scatter(x=np.array(st.session_state.time_buffer), y=np.array(st.session_state.ecg_buffer), mode='lines'))
fig_ecg.update_layout(title=f"ECG (last {buffer_seconds}s)", xaxis_title="Time (s)", yaxis_title="Amplitude", xaxis=dict(range=[-buffer_seconds,0]), height=300)
ecg_placeholder.plotly_chart(fig_ecg, use_container_width=True)

# SpO2
spo2_arr = np.array(st.session_state.spo2_buffer)
spo2_times = np.linspace(-len(spo2_arr)+1, 0, len(spo2_arr))
fig_spo2 = go.Figure()
fig_spo2.add_trace(go.Scatter(x=spo2_times, y=spo2_arr, mode='lines+markers'))
fig_spo2.update_layout(title="SpO₂ (last 60s)", yaxis=dict(range=[80,100]), height=250)
spo2_placeholder.plotly_chart(fig_spo2, use_container_width=True)

# Temp
temp_arr = np.array(st.session_state.temp_buffer)
temp_times = np.linspace(-len(temp_arr)+1,0,len(temp_arr))
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=temp_times, y=temp_arr, mode='lines+markers'))
fig_temp.update_layout(title="Body Temp (last 60s)", yaxis=dict(range=[35,39]), height=250)
temp_placeholder.plotly_chart(fig_temp, use_container_width=True)

# Metrics
spo2_metric.metric("SpO₂ (%)", f"{st.session_state.spo2_buffer[-1]:.1f}")
temp_metric.metric("Temp (°C)", f"{st.session_state.temp_buffer[-1]:.2f}")
hr_metric.metric("HR (bpm)", f"{hr}")



import streamlit as st
import time

# Set page title and icon
st.set_page_config(page_title="Medicine Dispenser", page_icon="💊")

st.title("💊 Smart Medicine Dispenser")
st.write("Click a medicine button to dispense:")

# List of medicines
medicines = ["Paracetamol", "Amoxicillin", "Ibuprofen", "Cetirizine", "Metformin"]

# Loop through medicines and create buttons
for med in medicines:
    if st.button(med):
        # Show spinner for 2 seconds to simulate dispensing
        with st.spinner(f"Dispensing {med}..."):
            time.sleep(2)
        # Show success message with emoji
        st.success(f"✅ Dispensing {med} 💊")
        # Fun animation
        st.balloons()