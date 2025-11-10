import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Quantum Gate Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED UI & DARK MODE COMPATIBLE CSS ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* --- Root Variables for Theming --- */
    :root {
        --glow-primary: #667eea;
        --glow-secondary: #764ba2;
        --card-bg-color: rgba(255, 255, 255, 0.05);
        --card-border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Adjust for Streamlit's Dark Theme */
    [data-theme="dark"] {
        --card-bg-color: rgba(40, 40, 60, 0.4);
        --card-border-color: rgba(102, 126, 234, 0.3);
    }

    /* --- Global & Body --- */
    * {
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background: #0f0c29;
        background: -webkit-linear-gradient(to right, #24243e, #302b63, #0f0c29);
        background: linear-gradient(to right, #24243e, #302b63, #0f0c29);
        background-attachment: fixed;
    }
    
    /* --- Headers --- */
    .main-header {
        font-size: 3.8rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #a26cf5, #667eea, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        animation: fadeIn 1s ease-in-out;
        text-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }
    .subtitle {
        text-align: center;
        color: var(--text-color);
        opacity: 0.8;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
        animation: fadeIn 1.5s ease-in-out;
    }

    /* --- Glassmorphism Card Style --- */
    .glass-card {
        background: var(--card-bg-color);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid var(--card-border-color);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        margin-bottom: 1rem;
    }
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 40px 0 rgba(0, 0, 0, 0.3), 0 0 40px 10px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5);
    }

    /* --- Tabs with Glow Effect --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border: none;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: var(--card-bg-color);
        backdrop-filter: blur(5px);
        border-radius: 12px;
        color: var(--text-color) !important;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0 2rem;
        border: 1px solid var(--card-border-color);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        color: white !important;
        transform: translateY(-4px);
        border-color: var(--glow-primary);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--glow-primary), var(--glow-secondary)) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
        animation: pulse-glow 2s infinite alternate;
    }
    @keyframes pulse-glow {
        from { box-shadow: 0 0 15px -5px var(--glow-primary), 0 0 30px -10px var(--glow-secondary); }
        to { box-shadow: 0 0 25px 0px var(--glow-primary), 0 0 40px -5px var(--glow-secondary); }
    }
    
    /* --- Buttons with Glow --- */
    .stButton>button {
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: white;
        background: linear-gradient(135deg, var(--glow-primary), var(--glow-secondary));
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, var(--glow-secondary), var(--glow-primary));
    }
    
    /* --- Custom Form Controls --- */
    label[data-testid="stWidgetLabel"] {
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    .stSlider [data-baseweb="slider"] > div {
        background: linear-gradient(135deg, var(--glow-primary), var(--glow-secondary));
    }
    .stSlider [data-testid="stThumbValue"] {
        border: 2px solid var(--glow-primary);
        background: var(--background-color);
    }
    
    /* --- Profile Cards --- */
    .profile-card {
        background: var(--card-bg-color);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid var(--card-border-color);
        text-align: center;
        height: 100%;
        transition: all 0.4s ease;
    }
    .profile-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.3);
        border-color: var(--glow-primary);
    }
    .profile-img {
        width: 140px; height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid var(--glow-primary);
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4);
    }
    .profile-name {
        font-size: 1.5rem; font-weight: 700;
        color: var(--glow-primary); margin-bottom: 0.25rem;
    }
    .profile-role {
        font-size: 1.1rem; font-weight: 600;
        color: var(--glow-secondary); margin-bottom: 1rem;
    }
    
    /* --- Hide Streamlit Branding --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    </style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---

st.markdown('<h1 class="main-header">⚛ Quantum Gate Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the fascinating world of quantum computing with interactive visualizations</p>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Standard Gates", "🌀 Rotation Gates", "🔮 Faraday Rotator", "🔐 BB84 Protocol", "🧑‍🔬 About Us"
])

# --- TAB 1: STANDARD GATES ---
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.markdown("### 🎛️ Control Panel")
        original_bit = st.selectbox("**Initial Qubit State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"])
        gate_category = st.radio("**Gate Category:**", ["⚡ Pauli Gates", "🌟 Hadamard & Phase"])
        
        if gate_category == "⚡ Pauli Gates":
            gate = st.selectbox("Select Pauli Gate:", ["Identity", "X (NOT)", "Y", "Z"])
        else:
            gate = st.selectbox("Select Hadamard & Phase Gate:", ["H (Hadamard)", "S (Phase)", "T", "S† (S-dagger)", "T† (T-dagger)"])
        
        apply_button = st.button("🚀 Apply Gate", use_container_width=True)
        
    with col2:
        st.markdown("### 📊 Quantum State Visualization")
        if apply_button:
            qc = QuantumCircuit(1)
            if original_bit == "|1⟩": qc.x(0)
            elif original_bit == "|+⟩": qc.h(0)
            elif original_bit == "|-⟩": qc.x(0); qc.h(0)
            
            gate_map = {"X (NOT)": qc.x, "Y": qc.y, "Z": qc.z, "H (Hadamard)": qc.h, "S (Phase)": qc.s, "T": qc.t, "S† (S-dagger)": qc.sdg, "T† (T-dagger)": qc.tdg}
            if gate != "Identity": gate_map[gate](0)
            
            state = Statevector.from_instruction(qc)
            st.metric("P(|0⟩)", f"{abs(state.data[0])**2:.4f}")
            st.metric("P(|1⟩)", f"{abs(state.data[1])**2:.4f}")
            fig = plot_bloch_multivector(state)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: ROTATION GATES ---
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.markdown("### 🎚️ Rotation Controls")
        initial_state = st.selectbox("**Initial State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"], key="rot_state")
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        angle_degrees = st.slider("**Rotation Angle (°):**", 0, 360, 90, 15)
        animate = st.checkbox("🎬 Show rotation animation")
        if animate:
            num_steps = st.slider("Animation steps:", 5, 50, 20)
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True)

    with col2:
        st.markdown("### 📊 Rotation Visualization")
        if apply_rotation:
            angle_radians = np.deg2rad(angle_degrees)
            initial_qc = QuantumCircuit(1)
            if initial_state == "|1⟩": initial_qc.x(0)
            elif initial_state == "|+⟩": initial_qc.h(0)
            elif initial_state == "|-⟩": initial_qc.x(0); initial_qc.h(0)
            initial_sv = Statevector.from_instruction(initial_qc)

            if animate:
                import time
                placeholder = st.empty()
                progress = st.progress(0)
                for i, angle in enumerate(np.linspace(0, angle_radians, num_steps)):
                    rot_qc = QuantumCircuit(1)
                    if rotation_axis == "X": rot_qc.rx(angle, 0)
                    elif rotation_axis == "Y": rot_qc.ry(angle, 0)
                    else: rot_qc.rz(angle, 0)
                    state = initial_sv.evolve(rot_qc)
                    fig = plot_bloch_multivector(state)
                    with placeholder.container():
                        st.pyplot(fig)
                    plt.close()
                    progress.progress((i + 1) / num_steps)
                    time.sleep(0.05)
                st.success("✅ Animation complete!")
            else:
                qc = initial_qc.copy()
                if rotation_axis == "X": qc.rx(angle_radians, 0)
                elif rotation_axis == "Y": qc.ry(angle_radians, 0)
                else: qc.rz(angle_radians, 0)
                state = Statevector.from_instruction(qc)
                fig = plot_bloch_multivector(state)
                st.pyplot(fig)
                plt.close()
        else:
            st.info("👆 Set your rotation parameters and click 'Apply Rotation'.")
    st.markdown('</div>', unsafe_allow_html=True)
    
# --- TAB 3: FARADAY ROTATOR ---
with tab3:
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align:center; color: var(--glow-primary);">🔮 Faraday Rotator & BB84</h2>
        <p style="text-align:center; opacity: 0.8;">Demonstrating how a Faraday Rotator's non-reciprocal rotation can be used to precisely align photon polarization for Quantum Key Distribution.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    align_col1, align_col2 = st.columns([1, 2], gap="large")
    with align_col1:
        st.markdown("### ⚙️ Alignment Controls")
        material = st.selectbox("Select Material:", ["Flint Glass (V=50)", "TGG Crystal (V=134)", "Custom"])
        V_align = {"Flint Glass (V=50)": 50.0, "TGG Crystal (V=134)": 134.0}.get(material, 50.0)
        if material == "Custom":
            V_align = st.slider("Custom Verdet Constant (rad/T·m):", 1.0, 200.0, 50.0, 1.0)
        
        B_align = st.slider("Magnetic Field B (Tesla):", 0.0, 1.0, 0.25, 0.01, key="b_align")
        L_align = st.slider("Path Length L (m):", 0.01, 0.1, 0.05, 0.001, key="l_align")
        initial_angle_align = st.slider("Initial Photon Polarization Angle (°):", 0, 180, 22, 1)
        run_alignment = st.button("🚀 Run Basis Alignment", use_container_width=True)

    with align_col2:
        st.markdown("### 📊 Basis Alignment Visualization")
        if run_alignment:
            theta_faraday = V_align * B_align * L_align
            theta_faraday_deg = np.rad2deg(theta_faraday)
            final_angle = (initial_angle_align + theta_faraday_deg) % 360
            
            bb84_bases = {"H": 0, "V": 90, "D": 45, "A": 135}
            
            def find_nearest_basis(angle, bases):
                return min(bases.items(), key=lambda item: min(abs(angle - item[1]), abs(angle - (item[1] + 180))) % 180)

            nearest_basis_name, nearest_basis_angle = find_nearest_basis(final_angle, bb84_bases)
            alignment_error = min(abs(final_angle - nearest_basis_angle), abs(final_angle - (nearest_basis_angle + 180))) % 180

            fig_align, ax1 = plt.subplots(figsize=(8, 8))
            ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5)
            ax1.set_aspect('equal'); ax1.grid(True, alpha=0.2)
            
            # Draw basis vectors
            for name, angle in bb84_bases.items():
                rad = np.deg2rad(angle)
                ax1.arrow(0, 0, 1.2*np.cos(rad), 1.2*np.sin(rad), head_width=0.08, length_includes_head=True, fc='gray', ec='gray', alpha=0.4)
                ax1.text(1.4*np.cos(rad), 1.4*np.sin(rad), f'|{name}⟩', ha='center', va='center', alpha=0.6)

            # Draw polarizations
            init_rad = np.deg2rad(initial_angle_align)
            ax1.arrow(0, 0, np.cos(init_rad), np.sin(init_rad), head_width=0.1, length_includes_head=True, fc='cyan', ec='cyan', lw=2, label=f'Initial: {initial_angle_align:.1f}°')
            final_rad = np.deg2rad(final_angle)
            ax1.arrow(0, 0, np.cos(final_rad), np.sin(final_rad), head_width=0.1, length_includes_head=True, fc='magenta', ec='magenta', lw=3, label=f'Final: {final_angle:.1f}°')
            ax1.legend(loc='upper right')
            st.pyplot(fig_align); plt.close()

            m1, m2, m3 = st.columns(3)
            m1.metric("Faraday Rotation", f"{theta_faraday_deg:.2f}°")
            m2.metric("Nearest BB84 Basis", f"|{nearest_basis_name}⟩")
            m3.metric("Alignment Error", f"{alignment_error:.2f}°")
        else:
            st.info("👆 Adjust parameters to see how the Faraday rotator aligns a photon to a BB84 basis.")
    st.markdown('</div>', unsafe_allow_html=True)
    
# --- TAB 4: BB84 PROTOCOL ---
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
        <h2 style="text-align:center; color: var(--glow-primary);">🔐 The BB84 Protocol</h2>
        <p style="text-align:center; opacity: 0.8;">Discover the first quantum cryptography protocol that guarantees secure communication by leveraging the laws of physics.</p>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.info("**Unconditional Security:** Security is based on physics (the uncertainty principle & no-cloning theorem), not computational difficulty.", icon="🛡️")
    c2.info("**Eavesdropper Detection:** Any attempt by an intruder to measure the photons will disturb their state, introducing detectable errors.", icon="🔍")

    st.markdown("""
    <div class="feature-box" style="text-align: center; margin-top: 2rem;">
        <h2 style='font-size: 2.2rem;'>🧪 Ready to Experience BB84 in Action?</h2>
        <p style='font-size: 1.2rem; margin-bottom: 2rem;'>Try our interactive BB84 simulator and see quantum key distribution working in real-time!</p>
        <a href="https://bb84.srijan.dpdns.org/" target="_blank" style="text-decoration: none;">
            <button class="custom-link-button">🚀 ENTER THE SIMULATION LAB</button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
# --- TAB 5: ABOUT US ---
with tab5:
    st.markdown('<h2 style="text-align:center; color: var(--glow-primary);">🧑‍🔬 Meet The Team</h2>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The innovators dedicated to making quantum concepts accessible to all.</p>", unsafe_allow_html=True)
    
    team_cols = st.columns(5, gap="large")
    team_members = [
        {"name": "ABHINAV SUNEESH", "role": "DFS Researcher", "img": "https://github.com/ivanho-git/qubit-gates/blob/main/abhinav.jpeg?raw=true"},
        {"name": "IBHAN MUKHERJEE", "role": "Eavesdropper Analyst", "img": "https://github.com/ivanho-git/qubit-gates/blob/main/ibhann.jpeg?raw=true"},
        {"name": "HARI ASHWIN", "role": "Qubits & Gates Expert", "img": "https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0032.jpg?raw=true"},
        {"name": "SRIJAN GUCHHAIT", "role": "BB84 Protocol Architect", "img": "https://github.com/ivanho-git/qubit-gates/blob/main/gucci.jpeg?raw=true"},
        {"name": "OM THAVARI", "role": "Faraday Rotator Tech", "img": "https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0008.jpg?raw=true"}
    ]

    for i, member in enumerate(team_members):
        with team_cols[i]:
            st.markdown(f"""
            <div class="profile-card">
                <img src="{member['img']}" class="profile-img">
                <p class="profile-name">{member['name']}</p>
                <p class="profile-role">{member['role']}</p>
            </div>
            """, unsafe_allow_html=True)
