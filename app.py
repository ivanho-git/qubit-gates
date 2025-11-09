# app.py
import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Quantum Gate Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Sidebar: Theme Toggle + Info
# -----------------------------
st.sidebar.title("Settings")
theme_choice = st.sidebar.radio("Theme:", ["System (auto)", "Light", "Dark"], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick tips**")
st.sidebar.markdown("- Use **Apply** buttons to visualize.\n- Animations use small sleeps to display frames.")
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ — copy freely and modify.")

# -----------------------------
# CSS: adaptive or forced theme
# -----------------------------
def inject_css(theme):
    # theme = "system", "light", or "dark"
    if theme == "system":
        css = """
        <style>
        /* System preference (auto) */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #0e1117;
                --card-bg: #1e1e2e;
                --text-color: #ffffff;
                --subtext-color: #b5b5b5;
                --gradient1: #6a11cb;
                --gradient2: #2575fc;
                --accent: #8b5cf6;
                --shadow: rgba(0, 0, 0, 0.6);
            }
        }
        @media (prefers-color-scheme: light) {
            :root {
                --bg-color: #f5f7fa;
                --card-bg: #ffffff;
                --text-color: #000000;
                --subtext-color: #555555;
                --gradient1: #667eea;
                --gradient2: #764ba2;
                --accent: #667eea;
                --shadow: rgba(0, 0, 0, 0.15);
            }
        }
        /* common styles */
        body, .main {
            background: var(--bg-color) !important;
            color: var(--text-color) !important;
            transition: background 0.4s ease, color 0.4s ease;
        }
        .block-container {
            background: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-radius: 20px;
            box-shadow: 0 10px 30px var(--shadow);
            padding: 2rem;
        }
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, var(--gradient1), var(--gradient2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { text-align:center; color:var(--subtext-color); }
        .stTabs [data-baseweb="tab-list"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); border-radius: 12px; padding: 1rem; }
        .stTabs [data-baseweb="tab"] { background: var(--card-bg); color: var(--text-color); border-radius: 10px; font-weight:600; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)) !important; color: #fff !important; }
        .card, .info-box { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); transition: transform 0.3s ease; padding: 1rem; }
        .card:hover, .info-box:hover { transform: translateY(-5px); }
        .stButton>button { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white; font-weight:600; border-radius:12px; padding:0.8rem 1.5rem; border:none; text-transform:uppercase; }
        .gradient-box { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white !important; border-radius: 20px; padding:2rem; }
        .feature-box { background: linear-gradient(135deg,#f093fb,#f5576c); color: white !important; border-radius:15px; padding:2rem; box-shadow:0 10px 25px rgba(245,87,108,0.3); }
        [data-testid="stMetricValue"] { color: var(--accent); }
        .profile-card { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); text-align: center; padding: 1.2rem; }
        .profile-img { width:140px; height:140px; border-radius:50%; border:4px solid var(--gradient1); object-fit:cover; margin-bottom:1rem; }
        .profile-name { color: var(--accent); font-weight:700; font-size:1.2rem; }
        .profile-role { color: var(--gradient2); font-weight:600; }
        footer, #MainMenu { visibility: hidden; }
        </style>
        """
    elif theme == "light":
        css = """
        <style>
        :root {
            --bg-color: #f5f7fa;
            --card-bg: #ffffff;
            --text-color: #000000;
            --subtext-color: #555555;
            --gradient1: #667eea;
            --gradient2: #764ba2;
            --accent: #667eea;
            --shadow: rgba(0, 0, 0, 0.15);
        }
        body, .main {
            background: var(--bg-color) !important;
            color: var(--text-color) !important;
        }
        .block-container {
            background: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-radius: 20px;
            box-shadow: 0 10px 30px var(--shadow);
            padding: 2rem;
        }
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, var(--gradient1), var(--gradient2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { text-align:center; color:var(--subtext-color); }
        .stTabs [data-baseweb="tab-list"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); border-radius: 12px; padding: 1rem; }
        .stTabs [data-baseweb="tab"] { background: var(--card-bg); color: var(--text-color); border-radius: 10px; font-weight:600; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)) !important; color: #fff !important; }
        .card, .info-box { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); transition: transform 0.3s ease; padding:1rem; }
        .stButton>button { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white; font-weight:600; border-radius:12px; padding:0.8rem 1.5rem; border:none; text-transform:uppercase; }
        .gradient-box { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white !important; border-radius: 20px; padding:2rem; }
        .feature-box { background: linear-gradient(135deg,#f093fb,#f5576c); color: white !important; border-radius:15px; padding:2rem; box-shadow:0 10px 25px rgba(245,87,108,0.3); }
        [data-testid="stMetricValue"] { color: var(--accent); }
        .profile-card { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); text-align: center; padding:1.2rem; }
        .profile-img { width:140px; height:140px; border-radius:50%; border:4px solid var(--gradient1); object-fit:cover; margin-bottom:1rem; }
        footer, #MainMenu { visibility: hidden; }
        </style>
        """
    else:  # dark
        css = """
        <style>
        :root {
            --bg-color: #0e1117;
            --card-bg: #1e1e2e;
            --text-color: #ffffff;
            --subtext-color: #b5b5b5;
            --gradient1: #6a11cb;
            --gradient2: #2575fc;
            --accent: #8b5cf6;
            --shadow: rgba(0, 0, 0, 0.6);
        }
        body, .main {
            background: var(--bg-color) !important;
            color: var(--text-color) !important;
        }
        .block-container {
            background: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-radius: 20px;
            box-shadow: 0 10px 30px var(--shadow);
            padding: 2rem;
        }
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, var(--gradient1), var(--gradient2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { text-align:center; color:var(--subtext-color); }
        .stTabs [data-baseweb="tab-list"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); border-radius: 12px; padding: 1rem; }
        .stTabs [data-baseweb="tab"] { background: var(--card-bg); color: var(--text-color); border-radius: 10px; font-weight:600; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)) !important; color: #fff !important; }
        .card, .info-box { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); transition: transform 0.3s ease; padding:1rem; }
        .stButton>button { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white; font-weight:600; border-radius:12px; padding:0.8rem 1.5rem; border:none; text-transform:uppercase; }
        .gradient-box { background: linear-gradient(135deg, var(--gradient1), var(--gradient2)); color: white !important; border-radius: 20px; padding:2rem; }
        .feature-box { background: linear-gradient(135deg,#f093fb,#f5576c); color: white !important; border-radius:15px; padding:2rem; box-shadow:0 10px 25px rgba(245,87,108,0.3); }
        [data-testid="stMetricValue"] { color: var(--accent); }
        .profile-card { background: var(--card-bg); color: var(--text-color); border-radius: 15px; box-shadow: 0 10px 30px var(--shadow); text-align: center; padding:1.2rem; }
        .profile-img { width:140px; height:140px; border-radius:50%; border:4px solid var(--gradient1); object-fit:cover; margin-bottom:1rem; }
        footer, #MainMenu { visibility: hidden; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

inject_css("system" if theme_choice == "System (auto)" or theme_choice == "System (auto)" else ("light" if theme_choice == "Light" else "dark") if False else ("system" if theme_choice == "System (auto)" else ("light" if theme_choice == "Light" else "dark")))

# (The above is intentionally permissive: mapping selection names to our inject function.)
# Simpler mapping:
if theme_choice == "System (auto)":
    inject_css("system")
elif theme_choice == "Light":
    inject_css("light")
else:
    inject_css("dark")

# Animated Header
st.markdown('<h1 class="main-header">⚛ Quantum Gate Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the fascinating world of quantum computing with interactive visualizations</p>', unsafe_allow_html=True)

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Standard Gates",
    "🌀 Rotation Gates",
    "🔮 Faraday Rotator",
    "🔐 BB84 Protocol",
    "🧑‍🔬 About Us"
])

# --------------------------
# Tab 1: Standard Gates
# --------------------------
with tab1:
    st.markdown('<p class="section-header">Standard Quantum Gates</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Control Panel")
        original_bit = st.selectbox(
            "**Initial Qubit State:**",
            ["|0⟩", "|1⟩", "|+⟩", "|-⟩"],
            help="Choose the starting state of your qubit"
        )
        st.markdown("---")
        st.markdown("**Select Quantum Gate:**")
        gate_category = st.radio(
            "Gate Category:",
            ["⚡ Pauli Gates", "🌟 Hadamard & Phase", "🚀 Advanced Gates"],
            label_visibility="collapsed"
        )
        if gate_category == "⚡ Pauli Gates":
            gate = st.selectbox("", ["Identity", "X (NOT)", "Y", "Z"], label_visibility="collapsed")
        elif gate_category == "🌟 Hadamard & Phase":
            gate = st.selectbox("", ["H (Hadamard)", "S (Phase)", "T", "S† (S-dagger)", "T† (T-dagger)"], label_visibility="collapsed")
        else:
            gate = st.selectbox("", ["SX (√X)", "SY (√Y)", "RZ(π/2)"], label_visibility="collapsed")
        st.markdown("---")
        apply_button = st.button("🚀 Apply Gate", use_container_width=True)
        gate_info_dict = {
            "Identity": "No change - Identity operation",
            "X (NOT)": "Bit flip: |0⟩↔|1⟩ (Quantum NOT)",
            "Y": "Bit & phase flip combination",
            "Z": "Phase flip: |1⟩→-|1⟩",
            "H (Hadamard)": "Creates superposition states",
            "S (Phase)": "90° phase rotation (π/2)",
            "T": "45° phase rotation (π/4)",
            "S† (S-dagger)": "Inverse S gate (-π/2)",
            "T† (T-dagger)": "Inverse T gate (-π/4)",
            "SX (√X)": "Square root of X gate",
            "SY (√Y)": "Square root of Y gate",
            "RZ(π/2)": "Z-axis rotation by π/2"
        }
        st.markdown(f"""
        <div class="info-box">
        <h4>📖 Gate Information</h4>
        <p><strong>{gate}</strong></p>
        <p>{gate_info_dict.get(gate, "")}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quantum State Visualization")
        if apply_button:
            qc = QuantumCircuit(1)
            # initial states
            if original_bit == "|1⟩":
                qc.x(0)
            elif original_bit == "|+⟩":
                qc.h(0)
            elif original_bit == "|-⟩":
                qc.x(0)
                qc.h(0)
            # apply gate
            if gate != "Identity":
                if gate == "X (NOT)":
                    qc.x(0)
                elif gate == "Y":
                    qc.y(0)
                elif gate == "Z":
                    qc.z(0)
                elif gate == "H (Hadamard)":
                    qc.h(0)
                elif gate == "S (Phase)":
                    qc.s(0)
                elif gate == "T":
                    qc.t(0)
                elif gate == "S† (S-dagger)":
                    qc.sdg(0)
                elif gate == "T† (T-dagger)":
                    qc.tdg(0)
                elif gate == "SX (√X)":
                    qc.sx(0)
                elif gate == "SY (√Y)":
                    qc.sy(0)
                elif gate == "RZ(π/2)":
                    qc.rz(np.pi/2, 0)
            state = Statevector.from_instruction(qc)
            state_array = state.data
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("α (|0⟩)", f"{state_array[0]:.3f}")
            with col_b:
                st.metric("β (|1⟩)", f"{state_array[1]:.3f}")
            with col_c:
                st.metric("Phase", f"{np.angle(state_array[1]):.3f} rad")
            st.markdown("---")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("P(|0⟩)", f"{abs(state_array[0])**2:.4f}")
            with col_p2:
                st.metric("P(|1⟩)", f"{abs(state_array[1])**2:.4f}")
            st.markdown("---")
            # Bloch sphere
            fig = plot_bloch_multivector(state)
            st.pyplot(fig)
            plt.close()
            # Circuit diagram
            st.markdown("#### 🔧 Quantum Circuit")
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except Exception:
                st.code(qc.draw(output='text'), language='text')
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Tab 2: Rotation Gates
# --------------------------
with tab2:
    st.markdown('<p class="section-header">Rotation Gates with Animation</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎚️ Rotation Controls")
        initial_state = st.selectbox("**Initial State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"], key="rot_state")
        st.markdown("---")
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        angle_degrees = st.slider("**Rotation Angle (degrees):**", min_value=0, max_value=360, value=90, step=15)
        angle_radians = np.deg2rad(angle_degrees)
        st.markdown(f"""
        <div class="info-box">
        <h4>📐 Angle Information</h4>
        <p><strong>Degrees:</strong> {angle_degrees}°</p>
        <p><strong>Radians:</strong> {angle_radians:.4f} rad</p>
        <p><strong>In terms of π:</strong> {angle_degrees/180:.2f}π</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        animate = st.checkbox("🎬 Show rotation animation", value=False)
        if animate:
            num_steps = st.slider("Animation steps:", 5, 50, 20)
            animation_speed = st.slider("Animation speed (higher is faster):", 1, 10, 5)
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True, key="apply_rot")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Rotation Visualization")
        if apply_rotation:
            # create initial state
            initial_qc = QuantumCircuit(1)
            if initial_state == "|1⟩":
                initial_qc.x(0)
            elif initial_state == "|+⟩":
                initial_qc.h(0)
            elif initial_state == "|-⟩":
                initial_qc.x(0); initial_qc.h(0)
            initial_statevector = Statevector.from_instruction(initial_qc)
            if animate:
                angles = np.linspace(0, angle_radians, num_steps)
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                for i, current_angle in enumerate(angles):
                    rotation_qc = QuantumCircuit(1)
                    if rotation_axis == "X":
                        rotation_qc.rx(current_angle, 0)
                    elif rotation_axis == "Y":
                        rotation_qc.ry(current_angle, 0)
                    else:
                        rotation_qc.rz(current_angle, 0)
                    state = initial_statevector.evolve(rotation_qc)
                    state_array = state.data
                    fig = plot_bloch_multivector(state)
                    with animation_placeholder.container():
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Step", f"{i+1}/{num_steps}")
                        with col_b:
                            st.metric("Angle", f"{np.rad2deg(current_angle):.1f}°")
                        with col_c:
                            st.metric("Progress", f"{((i+1)/num_steps)*100:.0f}%")
                        st.pyplot(fig)
                        col_1, col_2 = st.columns(2)
                        with col_1:
                            st.metric("|α|²", f"{abs(state_array[0])**2:.3f}")
                        with col_2:
                            st.metric("|β|²", f"{abs(state_array[1])**2:.3f}")
                    plt.close()
                    progress_bar.progress((i + 1) / num_steps)
                    time.sleep(0.1 / animation_speed)
                progress_bar.empty()
                st.success("✅ Animation complete!")
            else:
                qc = QuantumCircuit(1)
                if initial_state == "|1⟩":
                    qc.x(0)
                elif initial_state == "|+⟩":
                    qc.h(0)
                elif initial_state == "|-⟩":
                    qc.x(0); qc.h(0)
                if rotation_axis == "X":
                    qc.rx(angle_radians, 0)
                elif rotation_axis == "Y":
                    qc.ry(angle_radians, 0)
                else:
                    qc.rz(angle_radians, 0)
                state = Statevector.from_instruction(qc)
                state_array = state.data
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("α (|0⟩)", f"{state_array[0]:.4f}")
                with col_b:
                    st.metric("β (|1⟩)", f"{state_array[1]:.4f}")
                st.markdown("---")
                fig = plot_bloch_multivector(state)
                st.pyplot(fig)
                plt.close()
                st.markdown("#### 🔧 Circuit Diagram")
                try:
                    circuit_fig = qc.draw(output='mpl', style='iqp')
                    st.pyplot(circuit_fig)
                    plt.close()
                except Exception:
                    st.code(qc.draw(output='text'), language='text')
        else:
            st.info("👆 Set your rotation parameters and click 'Apply Rotation'")
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Tab 3: Faraday Rotator
# --------------------------
with tab3:
    st.markdown('<p class="section-header">Faraday Rotator Simulator</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box" style="text-align: center;">
    <h4>🔬 About the Faraday Effect</h4>
    <p>
    The Faraday effect causes the polarization plane of light to rotate when passing through a medium 
    in a magnetic field. This phenomenon is used in optical isolators and magnetic field sensors.
    </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Physical Parameters")
        initial_polarization = st.radio("**Initial Polarization:**", ["Horizontal (|H⟩)", "Vertical (|V⟩)", "Diagonal (+45°)", "Anti-diagonal (-45°)"])
        st.markdown("---")
        verdet_constant = st.slider("**Verdet Constant (rad/T·m):**", min_value=1.0, max_value=100.0, value=50.0, step=1.0)
        magnetic_field = st.slider("**Magnetic Field (Tesla):**", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
        path_length = st.slider("**Path Length (meters):**", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
        faraday_angle = verdet_constant * magnetic_field * path_length
        faraday_angle_deg = np.rad2deg(faraday_angle) % 360
        st.markdown(f"""
        <div class="gradient-box">
        <h3>🧮 Faraday Rotation</h3>
        <h2>θ = {faraday_angle_deg:.1f}°</h2>
        <p>θ = V × B × L = {faraday_angle:.3f} rad</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        show_faraday_animation = st.checkbox("🎬 Animate propagation", value=True, key="faraday_anim")
        if show_faraday_animation:
            propagation_steps = st.slider("Steps:", 10, 50, 25, key="faraday_steps")
            animation_speed = st.slider("Speed:", 1, 10, 5, key="anim_speed")
        simulate_faraday = st.button("🔬 Run Simulation", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Polarization Evolution")
        if simulate_faraday:
            if initial_polarization == "Horizontal (|H⟩)":
                initial_angle = 0
            elif initial_polarization == "Vertical (|V⟩)":
                initial_angle = 90
            elif initial_polarization == "Diagonal (+45°)":
                initial_angle = 45
            else:
                initial_angle = -45
            if show_faraday_animation:
                angles_through_medium = np.linspace(0, faraday_angle_deg, propagation_steps)
                distances = np.linspace(0, path_length, propagation_steps)
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                for i, (rotation_angle, current_distance) in enumerate(zip(angles_through_medium, distances)):
                    current_pol_angle = initial_angle + rotation_angle
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                    ax1 = plt.subplot(121, projection='3d')
                    z = np.linspace(0, 2*np.pi, 100)
                    angle_rad = np.deg2rad(current_pol_angle)
                    Ex = np.cos(angle_rad) * np.sin(z)
                    Ey = np.sin(angle_rad) * np.sin(z)
                    ax1.plot(Ex, Ey, z, linewidth=2.5, alpha=0.8)
                    arrow_length = 1.2
                    ax1.quiver(0, 0, 0,
                               arrow_length * np.cos(angle_rad),
                               arrow_length * np.sin(angle_rad),
                               0,
                               color='red', arrow_length_ratio=0.3, linewidth=3)
                    ax1.set_xlabel('Ex (H)')
                    ax1.set_ylabel('Ey (V)')
                    ax1.set_zlabel('Propagation')
                    ax1.set_title(f'Light Wave\nDistance: {current_distance*100:.1f} cm', fontsize=11)
                    ax1.set_xlim([-1.5, 1.5]); ax1.set_ylim([-1.5, 1.5]); ax1.set_zlim([0, 2*np.pi])
                    ax1.view_init(elev=20, azim=45)
                    ax1.grid(True, alpha=0.3)
                    ax2.set_aspect('equal')
                    ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                    ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                    ax2.text(1.35, 0, 'H', fontsize=13, ha='left', va='center', fontweight='bold')
                    ax2.text(0, 1.35, 'V', fontsize=13, ha='center', va='bottom', fontweight='bold')
                    initial_rad = np.deg2rad(initial_angle)
                    ax2.arrow(0, 0, np.cos(initial_rad), np.sin(initial_rad), head_width=0.15, head_length=0.15, fc='blue', ec='blue', alpha=0.3, linewidth=2.5)
                    ax2.arrow(0, 0, np.cos(angle_rad), np.sin(angle_rad), head_width=0.15, head_length=0.15, fc='red', ec='red', alpha=1.0, linewidth=3.5)
                    if rotation_angle > 0:
                        arc_angles = np.linspace(initial_rad, angle_rad, 50)
                        arc_x = 0.5 * np.cos(arc_angles)
                        arc_y = 0.5 * np.sin(arc_angles)
                        ax2.plot(arc_x, arc_y, 'g--', linewidth=2.5, alpha=0.8)
                        ax2.text(0, -0.8, f'Rotation: {rotation_angle:.1f}°', fontsize=10, ha='center', color='green', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
                    ax2.set_xlim([-1.6, 1.6]); ax2.set_ylim([-1.6, 1.6])
                    ax2.set_title(f'Polarization Plane\nB = {magnetic_field:.1f} T', fontsize=11)
                    ax2.legend(loc='upper right', fontsize=9)
                    ax2.grid(True, alpha=0.3, linestyle='--')
                    plt.tight_layout()
                    with animation_placeholder.container():
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Distance", f"{current_distance*100:.1f} cm", f"{(current_distance/path_length)*100:.0f}%")
                        with col_b:
                            st.metric("Rotation", f"{rotation_angle:.1f}°")
                        with col_c:
                            st.metric("Polarization", f"{current_pol_angle:.1f}°")
                        st.pyplot(fig)
                    plt.close()
                    progress_bar.progress((i + 1) / propagation_steps)
                    time.sleep(0.1 / animation_speed)
                progress_bar.empty()
                st.success(f"✅ Polarization rotated from {initial_angle}° to {initial_angle + faraday_angle_deg:.1f}°")
                # Quantum state representation
                st.markdown("---")
                st.markdown("#### ⚛️ Quantum State Representation")
                qc_initial = QuantumCircuit(1)
                if initial_polarization == "Horizontal (|H⟩)":
                    pass
                elif initial_polarization == "Vertical (|V⟩)":
                    qc_initial.x(0)
                elif initial_polarization == "Diagonal (+45°)":
                    qc_initial.h(0)
                else:
                    qc_initial.x(0); qc_initial.h(0)
                initial_state = Statevector.from_instruction(qc_initial)
                rotation_qc = QuantumCircuit(1)
                # Note: Faraday rotation maps to relative phase between H and V; using RZ(2θ) as mapping
                rotation_qc.rz(2 * faraday_angle, 0)
                final_state = initial_state.evolve(rotation_qc)
                col1_vis, col2_vis = st.columns(2)
                with col1_vis:
                    st.markdown("**Initial State**")
                    fig = plot_bloch_multivector(initial_state)
                    st.pyplot(fig)
                    plt.close()
                with col2_vis:
                    st.markdown("**Final State**")
                    fig = plot_bloch_multivector(final_state)
                    st.pyplot(fig)
                    plt.close()
            else:
                # static visualization
                final_pol_angle = initial_angle + faraday_angle_deg
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                ax1 = plt.subplot(121, projection='3d')
                z = np.linspace(0, 2*np.pi, 100)
                angle_rad = np.deg2rad(final_pol_angle)
                Ex = np.cos(angle_rad) * np.sin(z)
                Ey = np.sin(angle_rad) * np.sin(z)
                ax1.plot(Ex, Ey, z, linewidth=2.5, alpha=0.8)
                arrow_length = 1.2
                ax1.quiver(0, 0, 0,
                           arrow_length * np.cos(angle_rad),
                           arrow_length * np.sin(angle_rad),
                           0,
                           color='red', arrow_length_ratio=0.3, linewidth=3)
                ax1.set_xlabel('Ex (H)'); ax1.set_ylabel('Ey (V)'); ax1.set_zlabel('Propagation')
                ax1.set_title(f'Final Light Wave\nAfter {path_length*100:.1f} cm', fontsize=11)
                ax1.set_xlim([-1.5, 1.5]); ax1.set_ylim([-1.5, 1.5]); ax1.set_zlim([0, 2*np.pi])
                ax1.view_init(elev=20, azim=45); ax1.grid(True, alpha=0.3)
                ax2.set_aspect('equal')
                ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                ax2.text(1.35, 0, 'H', fontsize=13, fontweight='bold')
                ax2.text(0, 1.35, 'V', fontsize=13, fontweight='bold')
                initial_rad = np.deg2rad(initial_angle)
                ax2.arrow(0, 0, np.cos(initial_rad), np.sin(initial_rad), head_width=0.15, head_length=0.15, fc='blue', ec='blue', alpha=0.3, linewidth=2.5)
                ax2.arrow(0, 0, np.cos(angle_rad), np.sin(angle_rad), head_width=0.15, head_length=0.15, fc='red', ec='red', linewidth=3.5)
                arc_angles = np.linspace(initial_rad, angle_rad, 50)
                arc_x = 0.5 * np.cos(arc_angles)
                arc_y = 0.5 * np.sin(arc_angles)
                ax2.plot(arc_x, arc_y, 'g--', linewidth=2.5, alpha=0.8)
                ax2.text(0, -0.8, f'Rotation: {faraday_angle_deg:.1f}°', fontsize=10, ha='center', color='green', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
                ax2.set_xlim([-1.6, 1.6]); ax2.set_ylim([-1.6, 1.6])
                ax2.set_title(f'Polarization Rotation\nB = {magnetic_field:.1f} T, L = {path_length*100:.1f} cm', fontsize=11)
                ax2.grid(True, alpha=0.3, linestyle='--')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                st.success(f"✅ Polarization rotated by {faraday_angle_deg:.1f}°")
        else:
            st.info("👆 Configure parameters and click 'Run Simulation'")
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Tab 4: BB84 Protocol
# --------------------------
with tab4:
    st.markdown('<p class="section-header">BB84 Quantum Key Distribution</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="gradient-box">
        <h1 style='font-size: 2.2rem; margin-bottom: 0.5rem;'>🔐 BB84 Protocol</h1>
        <p style='font-size: 1rem; opacity: 0.95; margin:0;'>The First Quantum Cryptography Protocol - Absolutely Secure Communication</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3 style="color: var(--gradient1) !important;">📚 What is BB84?</h3>
        <p style="color: var(--text-color);">
        <strong>BB84</strong> (Bennett–Brassard 1984) is the first quantum key distribution protocol.
        It allows two parties, Alice and Bob, to create a shared secret key with eavesdropping detection.
        </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3 style="color: var(--gradient1) !important;">🎯 Key Features</h3>
        <ul style="color: var(--text-color);">
            <li><strong>Unconditional Security:</strong> Based on quantum physics</li>
            <li><strong>Eavesdropping Detection:</strong> Measuring disturbs states</li>
            <li><strong>Photon Polarization:</strong> Uses polarized photons</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Steps summary
    st.markdown("""
    <div style='background: linear-gradient(135deg,#f5f7fa,#c3cfe2); padding:1.2rem; border-radius:12px;'>
        <h4 style='color: var(--gradient1);'>🔬 How Does BB84 Work?</h4>
        <p style='color: var(--text-color);'>Alice prepares random bits in two bases and sends photons to Bob. Bob measures randomly. They reconcile bases and check errors to detect eavesdropping.</p>
    </div>
    """, unsafe_allow_html=True)

    steps_col1, steps_col2 = st.columns(2)
    with steps_col1:
        st.markdown("""
        <div class="info-box">
        <h4>1️⃣ Quantum Transmission</h4>
        <p>Alice encodes random bits using rectilinear and diagonal bases and sends photons.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <h4>2️⃣ Random Measurement</h4>
        <p>Bob randomly chooses bases to measure photons and records results.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <h4>3️⃣ Basis Reconciliation</h4>
        <p>Alice & Bob publicly compare bases (not bit values) and keep matching ones.</p>
        </div>
        """, unsafe_allow_html=True)
    with steps_col2:
        st.markdown("""
        <div class="info-box">
        <h4>4️⃣ Error Checking</h4>
        <p>They reveal a subset of bits to estimate error rate. High error → eavesdropper suspected.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <h4>5️⃣ Privacy Amplification</h4>
        <p>Process remaining bits to reduce any partial info an eavesdropper might have.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <h4>6️⃣ Secure Key</h4>
        <p>Alice and Bob now share a secret key for encryption.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg,#fff3cd,#ffe8a1); padding:1rem; border-radius:12px;'>
        <h4 style='color:#856404;'>💡 The Two Bases</h4>
        <div style='display:flex; gap:1rem;'>
            <div style='background:white; padding:0.8rem; border-radius:8px; flex:1;'>
                <strong>Rectilinear (+):</strong><br> Horizontal (|0⟩) and Vertical (|1⟩)
            </div>
            <div style='background:white; padding:0.8rem; border-radius:8px; flex:1;
