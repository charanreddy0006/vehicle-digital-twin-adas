import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AutoTwin ADAS",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main-title {font-size: 2.3rem; font-weight: 800; margin-bottom: 0;}
.sub-title {color: #777; margin-top: 0;}
.status {font-weight: 700;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚗 AutoTwin Command Center</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Vehicle Digital Twin • Sensor Fusion • ADAS Simulation</div>', unsafe_allow_html=True)

run_files = sorted(Path("data/runs").glob("*/summary.json"), reverse=True)
if not run_files:
    st.warning("No simulation runs found.")
    st.code("python -m autotwin.cli --scenario emergency_braking --duration 15")
    st.stop()

selected = st.sidebar.selectbox(
    "Simulation Run",
    run_files,
    format_func=lambda p: p.parent.name
)
run_dir = selected.parent
summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
df = pd.read_csv(run_dir / "telemetry.csv")
events_path = run_dir / "events.json"
events = json.loads(events_path.read_text(encoding="utf-8")) if events_path.exists() else []

st.sidebar.markdown("---")
st.sidebar.markdown("### System")
st.sidebar.success("SIMULATION ONLINE")
st.sidebar.caption(f"Scenario: {summary['scenario']}")
st.sidebar.caption(f"Version: {summary['version']}")

# KPI row
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Speed", f"{df['speed_kmh'].iloc[-1]:.1f} km/h")
c2.metric("Max Speed", f"{summary['max_speed_kmh']:.1f} km/h")
c3.metric("Distance", f"{summary['distance_m']:.0f} m")
c4.metric("Battery", f"{summary['final_battery_soc']*100:.1f}%")
c5.metric("Safety Events", summary["events"])

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Vehicle", "📡 Perception", "🛡️ ADAS", "📋 Run Report"]
)

with tab1:
    st.subheader("Vehicle Dynamics")

    left, right = st.columns(2)

    with left:
        fig = px.line(df, x="timestamp", y="speed_kmh", title="Vehicle Speed")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.line(
            df,
            x="timestamp",
            y=["throttle", "brake"],
            title="Throttle / Brake Commands",
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        fig = px.line(df, x="timestamp", y="battery_soc", title="Battery SOC")
        fig.update_yaxes(tickformat=".0%")
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.line(
            df,
            x="timestamp",
            y="acceleration_ms2",
            title="Longitudinal Acceleration",
        )
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Sensor & Perception Layer")

    sensor_names = ["Radar", "Camera", "Ultrasonic", "IMU", "GPS", "Wheel Speed"]
    cols = st.columns(6)
    for col, name in zip(cols, sensor_names):
        col.metric(name, "ONLINE")

    st.markdown("### Fused Object Perception")

    if len(df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["closest_object_m"].replace(999.0, None),
            mode="lines",
            name="Closest fused object",
        ))
        fig.update_layout(
            title="Closest Detected Object",
            xaxis_title="Time (s)",
            yaxis_title="Distance (m)",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

        fig = px.line(
            df,
            x="timestamp",
            y="fused_objects",
            title="Fused Object Count",
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("ADAS Safety Layer")

    counts = {
        "FCW": int(summary["fcw_events"]),
        "AEB": int(summary["aeb_events"]),
        "LDW": int(summary["ldw_events"]),
        "BSD": int(summary["bsd_events"]),
    }

    cols = st.columns(4)
    for col, (name, count) in zip(cols, counts.items()):
        col.metric(name, count)

    st.markdown("### ADAS Activation Timeline")
    adas_df = df[["timestamp", "fcw", "aeb", "ldw", "bsd"]].copy()
    adas_long = adas_df.melt(
        id_vars="timestamp",
        var_name="module",
        value_name="active"
    )
    adas_long["module"] = adas_long["module"].str.upper()

    fig = px.line(
        adas_long,
        x="timestamp",
        y="active",
        color="module",
        title="ADAS Module Activity",
    )
    fig.update_yaxes(range=[-0.05, 1.05], dtick=1)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Safety Event Log")
    if events:
        event_df = pd.DataFrame(events)
        st.dataframe(
            event_df[
                ["timestamp", "module", "level", "message", "value", "recommended_action"]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No safety events recorded for this run.")

with tab4:
    st.subheader("Simulation Report")

    report_cols = st.columns(3)
    report_cols[0].write("**Scenario**")
    report_cols[0].write(summary["scenario"])
    report_cols[1].write("**Duration**")
    report_cols[1].write(f"{summary['duration_s']} s")
    report_cols[2].write("**Final Mode**")
    report_cols[2].write(summary["final_mode"])

    st.json(summary)

    st.markdown("### Telemetry Preview")
    st.dataframe(df.tail(100), use_container_width=True, hide_index=True)

    st.download_button(
        "Download Telemetry CSV",
        data=(run_dir / "telemetry.csv").read_bytes(),
        file_name=f"{run_dir.name}_telemetry.csv",
        mime="text/csv",
    )
