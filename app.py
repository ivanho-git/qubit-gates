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

# === CSS Styling ===
st.markdown("""<style>
/* (Your full CSS block remains unchanged — keep everything you already have here) */
</style>""", unsafe_allow_html=True)

# Animated Header
st.markdown('<h1 class="main-header">⚛️ Quantum Gate Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the fascinating world of quantum computing with interactive visualizations</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Standard Gates",
    "🌀 Rotation Gates",
    "🔮 Faraday Rotator",
    "🔐 BB84 Protocol",
    "👥 About Us"
])

# ========== TAB 1 ==========
with tab1:
    st.markdown('<p class="section-header">Standard Quantum Gates</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Control Panel")
        original_bit = st.selectbox("**Initial Qubit State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"])
        st.markdown("---")
        st.markdown("**Select Quantum Gate:**")
        gate_category = st.radio("Gate Category:", ["⚡ Pauli Gates", "🌟 Hadamard & Phase", "🚀 Advanced Gates"], label_visibility="collapsed")
        
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
    
    with col2:
        st.subheader("📊 Quantum State Visualization")
        
        if apply_button:
            qc = QuantumCircuit(1)
            if original_bit == "|1⟩":
                qc.x(0)
            elif original_bit == "|+⟩":
                qc.h(0)
            elif original_bit == "|-⟩":
                qc.x(0)
                qc.h(0)
            
            if gate != "Identity":
                if gate == "X (NOT)": qc.x(0)
                elif gate == "Y": qc.y(0)
                elif gate == "Z": qc.z(0)
                elif gate == "H (Hadamard)": qc.h(0)
                elif gate == "S (Phase)": qc.s(0)
                elif gate == "T": qc.t(0)
                elif gate == "S† (S-dagger)": qc.sdg(0)
                elif gate == "T† (T-dagger)": qc.tdg(0)
                elif gate == "SX (√X)": qc.sx(0)
                elif gate == "SY (√Y)": qc.sy(0)
                elif gate == "RZ(π/2)": qc.rz(np.pi/2, 0)
            
            state = Statevector.from_instruction(qc)
            state_array = state.data
            
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("α (|0⟩)", f"{state_array[0]:.3f}")
            with col_b: st.metric("β (|1⟩)", f"{state_array[1]:.3f}")
            with col_c: st.metric("Phase", f"{np.angle(state_array[1]):.3f} rad")
            
            st.markdown("---")
            col_p1, col_p2 = st.columns(2)
            with col_p1: st.metric("P(|0⟩)", f"{abs(state_array[0])**2:.4f}")
            with col_p2: st.metric("P(|1⟩)", f"{abs(state_array[1])**2:.4f}")
            
            st.markdown("---")
            fig = plot_bloch_multivector(state)
            st.pyplot(fig)
            plt.close()
            
            st.markdown("**🔧 Quantum Circuit**")
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except:
                st.code(qc.draw(output='text'), language='text')
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")

# ========== TAB 2 (Rotation Gates) ==========
with tab2:
    st.markdown('<p class="section-header">Rotation Gates with Animation</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎚️ Rotation Controls")
        initial_state = st.selectbox("**Initial State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"], key="rot_state")
        st.markdown("---")
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        angle_degrees = st.slider("**Rotation Angle (degrees):**", 0, 360, 90, 15)
        angle_radians = np.deg2rad(angle_degrees)
        
        st.markdown(f"""
        <div class="info-box">
        <h4>📐 Angle Information</h4>
        <p><strong>Degrees:</strong> {angle_degrees}°</p>
        <p><strong>Radians:</strong> {angle_radians:.4f} rad</p>
        <p><strong>In terms of π:</strong> {angle_degrees/180:.2f}π</p>
        </div>
        """, unsafe_allow_html=True)
        
        animate = st.checkbox("🎬 Show rotation animation", value=False)
        if animate:
            st.slider("Animation steps:", 5, 50, 20)
            st.slider("Animation speed:", 1, 10, 5)
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True, key="apply_rot")
    
    with col2:
        st.subheader("📊 Rotation Visualization")
        if apply_rotation:
            st.info("Rotation visualization coming soon...")

# ====== TAB 3 & TAB 4 placeholders ======
with tab3:
    st.markdown('<p class="section-header">Faraday Rotator</p>', unsafe_allow_html=True)
    st.info("This section is under development.")

with tab4:
    st.markdown('<p class="section-header">BB84 Quantum Key Distribution</p>', unsafe_allow_html=True)
    st.info("This section is under development.")

# ========== TAB 5: ABOUT US ==========
with tab5:
    st.markdown('<p class="section-header">Meet the Team</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <p style="font-size:1.2rem; color:#000;">
        We are a passionate team of quantum computing enthusiasts dedicated to making quantum mechanics interactive and fun through this simulator.
        </p>
    </div>
    """, unsafe_allow_html=True)

    team_members = [
        {"name": "🧠 Srijan Dey", "role": "Project Lead & Quantum Developer", "img": "image1.png", "bio": "Leads the quantum logic and system design behind this simulator."},
        {"name": "💻 Ibhan Mukherjee", "role": "UI/UX Designer & Streamlit Engineer", "img": "image2.png", "bio": "Designs the elegant visuals, layout, and front-end flow of the app."},
        {"name": "⚙️ Anirban Das", "role": "Backend & Qiskit Integration", "img": "image3.png", "bio": "Ensures seamless integration between Qiskit backend and visualization modules."},
        {"name": "📊 Priya Sharma", "role": "Data Visualization & Research", "img": "image4.png", "bio": "Creates Bloch sphere visualizations and quantum gate documentation."},
        {"name": "🧩 Riya Ghosh", "role": "Testing & Optimization", "img": "image5.png", "bio": "Performs app testing, optimization, and deployment readiness."}
    ]

    for i in range(0, len(team_members), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(team_members):
                member = team_members[i + j]
                with col:
                    st.markdown(f"""
                    <div class="gradient-box" style="padding:2rem; text-align:center;">
                        <img src="{member['img']}" style="width:150px; height:150px; border-radius:50%; margin-bottom:1rem; border:4px solid white;">
                        <h3>{member['name']}</h3>
                        <p><strong>{member['role']}</strong></p>
                        <p>{member['bio']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="margin-top:2rem; margin-bottom:2rem;">
    <div style="text-align:center;">
        <h3>🚀 Our Mission</h3>
        <p style="font-size:1.1rem; color:#000;">To make quantum computing concepts intuitive, visual, and accessible to everyone.</p>
    </div>
    """, unsafe_allow_html=True)
