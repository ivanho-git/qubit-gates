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

# Dark Mode Compatible CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-color);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 1rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0 2rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Info Boxes - Dark Mode Compatible */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .info-box h3 {
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 0.8rem;
        color: #667eea !important;
    }
    
    .info-box h4 {
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #764ba2 !important;
    }
    
    /* Gradient Boxes */
    .gradient-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .gradient-box h1, .gradient-box h2, .gradient-box h3, .gradient-box p {
        color: white !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 2rem 0 1rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        display: block;
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0.5rem auto;
        border-radius: 2px;
    }
    
    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
    }
    
    .feature-box h4, .feature-box p, .feature-box h2 {
        color: white !important;
    }
    
    /* Custom link button */
    .custom-link-button {
        display: inline-block;
        width: 100%;
        padding: 1.2rem 2rem;
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        border-radius: 15px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .custom-link-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(245, 87, 108, 0.6);
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }
    
    /* Profile Cards - Dark Mode Compatible */
    .profile-card {
        background: rgba(102, 126, 234, 0.05);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100%;
    }
    
    .profile-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
    }
    
    .profile-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-left: auto;
        margin-right: auto;
    }
    
    .profile-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.25rem;
    }
    
    .profile-role {
        font-size: 1.1rem;
        font-weight: 600;
        color: #764ba2;
        margin-bottom: 1rem;
    }
    
    .profile-bio {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Content boxes with transparent backgrounds */
    .content-box {
        background: rgba(102, 126, 234, 0.05);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .content-box h4 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Animated Header
st.markdown('<h1 class="main-header">⚛ Quantum Gate Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the fascinating world of quantum computing with interactive visualizations</p>', unsafe_allow_html=True)

# Create tabs with icons
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Standard Gates",
    "🌀 Rotation Gates",
    "🔮 Faraday Rotator",
    "🔐 BB84 Protocol",
    "🧑‍🔬 About Us"
])

with tab1:
    st.markdown('<p class="section-header">Standard Quantum Gates</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
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
            ["⚡ Pauli Gates", "🌟 Hadamard & Phase"],
            label_visibility="collapsed"
        )
        
        if gate_category == "⚡ Pauli Gates":
            gate = st.selectbox("", ["Identity", "X (NOT)", "Y", "Z"], label_visibility="collapsed")
        else:
            gate = st.selectbox("", ["H (Hadamard)", "S (Phase)", "T", "S† (S-dagger)", "T† (T-dagger)"], label_visibility="collapsed")
        
        st.markdown("---")
        apply_button = st.button("🚀 Apply Gate", use_container_width=True)
        
        # Gate information
        gate_info_dict = {
            "Identity": "No change - Identity operation",
            "X (NOT)": "Bit flip: |0⟩↔|1⟩ (Quantum NOT)",
            "Y": "Bit & phase flip combination",
            "Z": "Phase flip: |1⟩→-|1⟩",
            "H (Hadamard)": "Creates superposition states",
            "S (Phase)": "90° phase rotation (π/2)",
            "T": "45° phase rotation (π/4)",
            "S† (S-dagger)": "Inverse S gate (-π/2)",
            "T† (T-dagger)": "Inverse T gate (-π/4)"
        }
        
        st.markdown(f"""
        <div class="info-box">
        <h4>📖 Gate Information</h4>
        <p><strong>{gate}</strong></p>
        <p>{gate_info_dict.get(gate, "")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Quantum State Visualization")
        
        if apply_button:
            qc = QuantumCircuit(1)
            
            # Set initial state
            if original_bit == "|1⟩":
                qc.x(0)
            elif original_bit == "|+⟩":
                qc.h(0)
            elif original_bit == "|-⟩":
                qc.x(0)
                qc.h(0)
            
            # Apply gate
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
            
            state = Statevector.from_instruction(qc)
            state_array = state.data
            
            # Display state info
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
            st.markdown("**Quantum Circuit:**")
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except:
                st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")

with tab2:
    st.markdown('<p class="section-header">Rotation Gates with Animation</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎚️ Rotation Controls")
        
        initial_state = st.selectbox("**Initial State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"], key="rot_state")
        
        st.markdown("---")
        
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        
        angle_degrees = st.slider(
            "**Rotation Angle (degrees):**",
            min_value=0,
            max_value=360,
            value=90,
            step=15
        )
        
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
            animation_speed = st.slider("Animation speed:", 1, 10, 5)
        
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True, key="apply_rot")
    
    with col2:
        st.markdown("### 📊 Rotation Visualization")
        
        if apply_rotation:
            if animate:
                angles = np.linspace(0, angle_radians, num_steps)
                
                initial_qc = QuantumCircuit(1)
                if initial_state == "|1⟩":
                    initial_qc.x(0)
                elif initial_state == "|+⟩":
                    initial_qc.h(0)
                elif initial_state == "|-⟩":
                    initial_qc.x(0)
                    initial_qc.h(0)
                
                initial_statevector = Statevector.from_instruction(initial_qc)
                
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                import time
                
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
                    qc.x(0)
                    qc.h(0)
                
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
                
                st.markdown("**Circuit Diagram:**")
                try:
                    circuit_fig = qc.draw(output='mpl', style='iqp')
                    st.pyplot(circuit_fig)
                    plt.close()
                except:
                    st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Set your rotation parameters and click 'Apply Rotation'")

with tab3:
    st.markdown('<p class="section-header">Faraday Rotator Simulator</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
    <h4>🔬 About the Faraday Effect</h4>
    <p>
    The Faraday effect causes the polarization plane of light to rotate when passing through a medium 
    in a magnetic field. This quantum phenomenon is fundamental to optical isolators and magnetic field sensors.
    A key feature is its <strong>non-reciprocal nature</strong>: light rotating in one direction continues 
    rotating the same way on the return path, unlike normal optical rotators. This property makes it ideal 
    for <strong>aligning photon polarization</strong> to specific bases in quantum key distribution (BB84).
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔄 Non-Reciprocal vs Reciprocal Rotation Comparison")
    
    comp_col1, comp_col2 = st.columns([1, 2])
    
    with comp_col1:
        st.markdown("**Compare Rotator Types:**")
        V_comp = st.slider("Verdet Constant V (rad/T·m)", 1.0, 150.0, 50.0, step=1.0, key="v_comp")
        B_comp = st.slider("Magnetic Field B (Tesla)", 0.0, 1.0, 0.5, 0.01, key="b_comp")
        L_comp = st.slider("Material Length L (m)", 0.0, 0.1, 0.02, 0.005, key="l_comp")
        mode = st.selectbox("Rotator Type", ["Faraday Rotator (non-reciprocal)", "Normal Optical Rotator (reciprocal)"])
        
        theta_comp = V_comp * B_comp * L_comp
        st.markdown(f"""
        <div class="info-box">
        <h4>Rotation per pass</h4>
        <p style="font-size: 1.5rem; font-weight: bold; color: #667eea;">θ = {np.rad2deg(theta_comp):.2f}°</p>
        </div>
        """, unsafe_allow_html=True)
        
        animate_comp = st.checkbox("🎬 Animate rotation", value=True, key="comp_anim")
    
    with comp_col2:
        # Static view
        f_angle_final = theta_comp
        if "Faraday" in mode:
            b_angle_final = 2 * theta_comp # Final angle after round trip
        else:
            b_angle_final = 0 # Final angle after round trip is back to start
        
        fig_comp, ax_comp = plt.subplots(figsize=(6, 6))
        ax_comp.set_xlim(-1.5, 1.5)
        ax_comp.set_ylim(-1.5, 1.5)
        ax_comp.set_xlabel("Re(Eₓ)", fontsize=12, fontweight='bold')
        ax_comp.set_ylabel("Re(Eᵧ)", fontsize=12, fontweight='bold')
        ax_comp.set_title(f"Polarization Rotation - {mode}", fontsize=13, fontweight='bold', color='#667eea')
        ax_comp.grid(True, alpha=0.3)
        ax_comp.set_aspect('equal')
        
        # Initial State (0 degrees)
        ax_comp.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, 
                    fc='gray', ec='gray', lw=2.5, alpha=0.8, label='Initial (0°)')

        # Forward light
        fx, fy = np.cos(f_angle_final), np.sin(f_angle_final)
        ax_comp.arrow(0, 0, fx, fy, head_width=0.1, head_length=0.1, 
                    fc='blue', ec='blue', lw=2.5, alpha=0.8, label=f'Forward: {np.rad2deg(f_angle_final):.1f}°')
        
        # Backward light
        bx, by = np.cos(b_angle_final), np.sin(b_angle_final)
        ax_comp.arrow(0, 0, bx, by, head_width=0.1, head_length=0.1, 
                    fc='red', ec='red', lw=2.5, alpha=0.8, linestyle='--', label=f'Return: {np.rad2deg(b_angle_final):.1f}°')
        
        ax_comp.legend(loc='upper right', fontsize=10)
        st.pyplot(fig_comp)
        plt.close()

    st.markdown("---")
    
    st.markdown("""
    <div class="content-box">
        <h4>📚 What You're Seeing in the Simulation</h4>
        <p>This simulation shows what happens to light's polarization after it passes through a rotator, reflects off a mirror, and passes back through the same rotator.</p>
        <ul>
            <li><b>Faraday Rotator (Non-reciprocal):</b> The rotation <strong>doubles</strong> upon return. This is crucial for creating optical isolators.</li>
            <li><b>Normal Rotator (Reciprocal):</b> The rotation is <strong>cancelled out</strong> upon return, bringing the light back to its initial polarization.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # NEW SECTION: BB84 BASIS ALIGNMENT USING FARADAY ROTATOR
    # ========================================================================
    st.markdown("### 🎯 BB84 Basis Alignment with Faraday Rotator")
    st.markdown("""
    <div class="gradient-box">
        <h3>Polarization Control for Quantum Key Distribution</h3>
        <p>In BB84, photons must be precisely aligned to either the <strong>rectilinear basis</strong> (|H⟩, |V⟩) 
        or <strong>diagonal basis</strong> (|D⟩, |A⟩). The Faraday rotator provides active control to correct 
        polarization drift and ensure accurate basis preparation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control panel for basis alignment
    align_col1, align_col2 = st.columns([1, 2])
    
    with align_col1:
        st.markdown("### ⚙️ Alignment Controls")
        
        material = st.selectbox(
            "**Select Material:**",
            ["Flint Glass (V=50)", "Fused Silica (V=20)", "TGG Crystal (V=134)", "Custom"],
            key="material_select"
        )
        
        if material == "Flint Glass (V=50)":
            V_align = 50.0
        elif material == "Fused Silica (V=20)":
            V_align = 20.0
        elif material == "TGG Crystal (V=134)":
            V_align = 134.0
        else:
            V_align = st.slider("Custom Verdet Constant (rad/T·m):", 1.0, 200.0, 50.0, 1.0, key="v_custom")
        
        B_align = st.slider("**Magnetic Field B (Tesla):**", 0.0, 2.0, 0.5, 0.01, key="b_align")
        L_align = st.slider("**Path Length L (m):**", 0.01, 0.1, 0.02, 0.005, key="l_align")
        
        theta_faraday = V_align * B_align * L_align
        theta_faraday_deg = np.rad2deg(theta_faraday) % 360
        
        st.markdown(f"""
        <div class="gradient-box">
        <h3>🧮 Faraday Rotation</h3>
        <h2>θ = {theta_faraday_deg:.2f}°</h2>
        </div>
        """, unsafe_allow_html=True)
        
        initial_angle_align = st.slider("**Initial Photon Polarization Angle (°):**", 0, 180, 22, 1, key="initial_align")
        
        run_alignment = st.button("🚀 Run Basis Alignment", use_container_width=True, key="run_align")
    
    with align_col2:
        st.markdown("### 📊 Basis Alignment Visualization")
        
        if run_alignment:
            bb84_bases = {"H": 0, "V": 90, "D": 45, "A": 135}
            final_angle = (initial_angle_align + theta_faraday_deg) % 360
            
            def find_nearest_basis(angle, bases):
                min_diff = float('inf')
                nearest = None
                for name, basis_angle in bases.items():
                    diff = min(abs(angle - basis_angle), abs(angle - (basis_angle + 180))) % 180
                    if diff < min_diff:
                        min_diff = diff
                        nearest = (name, basis_angle)
                return nearest, min_diff
            
            nearest_basis, alignment_error = find_nearest_basis(final_angle, bb84_bases)
            
            fig_align, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [2, 1]})
            
            ax1.set_xlim(-1.5, 1.5)
            ax1.set_ylim(-1.5, 1.5)
            ax1.set_aspect('equal')
            ax1.set_title("BB84 Basis Alignment", fontsize=14, fontweight='bold', color='#667eea')
            ax1.grid(True, alpha=0.3)
            
            basis_colors = {"H": "blue", "V": "green", "D": "purple", "A": "orange"}
            for name, angle in bb84_bases.items():
                angle_rad = np.deg2rad(angle)
                x, y = 1.2 * np.cos(angle_rad), 1.2 * np.sin(angle_rad)
                ax1.arrow(0, 0, x, y, head_width=0.08, head_length=0.08, fc=basis_colors[name], ec=basis_colors[name], alpha=0.3, lw=2)
                ax1.text(1.4*x, 1.4*y, f'|{name}⟩\n{angle}°', ha='center', va='center', fontsize=10, fontweight='bold', color=basis_colors[name])
            
            init_rad = np.deg2rad(initial_angle_align)
            ax1.arrow(0, 0, 0.9*np.cos(init_rad), 0.9*np.sin(init_rad), head_width=0.12, head_length=0.12, fc='cyan', ec='cyan', alpha=0.5, lw=3, label=f'Initial: {initial_angle_align:.1f}°')
            
            final_rad = np.deg2rad(final_angle)
            ax1.arrow(0, 0, np.cos(final_rad), np.sin(final_rad), head_width=0.15, head_length=0.15, fc='red', ec='red', lw=4, label=f'Final: {final_angle:.1f}°')
            
            if theta_faraday_deg > 0:
                arc_angles = np.linspace(init_rad, final_rad, 50)
                arc_x = 0.6 * np.cos(arc_angles)
                arc_y = 0.6 * np.sin(arc_angles)
                ax1.plot(arc_x, arc_y, 'r--', lw=2.5, alpha=0.8)
            
            ax1.legend(loc='upper left', fontsize=9)
            ax1.set_xlabel("Horizontal Polarization", fontweight='bold')
            ax1.set_ylabel("Vertical Polarization", fontweight='bold')
            
            ax2.axis('off')
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            
            info_y = 0.9
            ax2.text(0.5, info_y, "Alignment Analysis", fontsize=16, fontweight='bold', ha='center', color='#667eea')
            
            info_y -= 0.15
            ax2.text(0.5, info_y, f"Nearest Basis: |{nearest_basis[0]}⟩", fontsize=13, ha='center', fontweight='bold', bbox=dict(boxstyle='round', facecolor=basis_colors[nearest_basis[0]], alpha=0.3))
            
            info_y -= 0.15
            alignment_quality = "Excellent" if alignment_error < 5 else "Good" if alignment_error < 15 else "Poor"
            color_quality = "#28a745" if alignment_error < 5 else "#ffc107" if alignment_error < 15 else "#dc3545"
            ax2.text(0.5, info_y, f"Alignment Error: {alignment_error:.2f}°", fontsize=12, ha='center', bbox=dict(boxstyle='round', facecolor=color_quality, alpha=0.3))
            
            info_y -= 0.1
            ax2.text(0.5, info_y, f"Quality: {alignment_quality}", fontsize=12, ha='center', fontweight='bold', color=color_quality)

            info_y -= 0.15
            ax2.text(0.1, info_y, "Physical Parameters:", fontsize=11, fontweight='bold')
            info_y -= 0.08
            ax2.text(0.1, info_y, f"• Rotation: {theta_faraday_deg:.2f}°", fontsize=10, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig_align)
            plt.close()
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Final Angle", f"{final_angle:.1f}°")
            with metric_col2:
                st.metric("Nearest Basis", f"|{nearest_basis[0]}⟩")
            with metric_col3:
                st.metric("Alignment Error", f"{alignment_error:.2f}°", delta=f"{alignment_quality}", delta_color="off")
            
            if alignment_error < 5:
                st.success(f"✅ Photon successfully aligned to |{nearest_basis[0]}⟩ basis!")
            elif alignment_error < 15:
                st.warning(f"⚠️ Photon reasonably aligned. Consider adjusting B field for better accuracy.")
            else:
                st.error(f"❌ Poor alignment. Significant B field adjustment needed.")

            st.markdown("---")
            st.markdown("**⚛️ Quantum State Representation on Bloch Sphere:**")
            
            qc_initial = QuantumCircuit(1)
            qc_initial.ry(2 * np.deg2rad(initial_angle_align), 0)
            
            rotation_qc = QuantumCircuit(1)
            rotation_qc.rz(2 * theta_faraday, 0)
            
            initial_state = Statevector.from_instruction(qc_initial)
            final_state = initial_state.evolve(rotation_qc)
            
            bloch_col1, bloch_col2 = st.columns(2)
            with bloch_col1:
                st.markdown("**Initial State**")
                fig_init = plot_bloch_multivector(initial_state)
                st.pyplot(fig_init)
                plt.close()
            with bloch_col2:
                st.markdown("**Final State**")
                fig_final = plot_bloch_multivector(final_state)
                st.pyplot(fig_final)
                plt.close()
        else:
            st.info("👆 Configure alignment parameters and click 'Run Basis Alignment'")

with tab4:
    st.markdown('<p class="section-header">BB84 Quantum Key Distribution</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gradient-box">
        <h1 style='font-size: 2.8rem; margin-bottom: 1rem;'>🔐 BB84 Protocol</h1>
        <p style='font-size: 1.3rem; opacity: 0.95;'>
            The First Quantum Cryptography Protocol - Absolutely Secure Communication
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3>📚 What is BB84?</h3>
        <p>
        <strong>BB84</strong> (Bennett-Brassard 1984) is the first and most famous quantum key distribution protocol. 
        It allows two parties, Alice and Bob, to generate a shared secret key that is provably secure against 
        any eavesdropper, even one with unlimited computing power.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3>🎯 Key Features</h3>
        <ul style="font-size: 1.05rem;">
            <li><strong>Unconditional Security:</strong> Based on quantum physics, not computational complexity</li>
            <li><strong>Eavesdropping Detection:</strong> Any interception attempt is detectable</li>
            <li><strong>Perfect Forward Secrecy:</strong> Each session uses a new quantum key</li>
            <li><strong>Photon Polarization:</strong> Uses quantum states of light particles</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='content-box'><h4>🔬 How Does BB84 Work?</h4></div>", unsafe_allow_html=True)
    
    steps_col1, steps_col2 = st.columns(2)
    with steps_col1:
        st.markdown("<div class='info-box'><h4>1️⃣ Quantum Transmission</h4><p>Alice encodes random bits using two different bases (rectilinear and diagonal) and sends photons to Bob.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><h4>2️⃣ Random Measurement</h4><p>Bob randomly chooses bases to measure the received photons, recording the results.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><h4>3️⃣ Basis Reconciliation</h4><p>Alice and Bob publicly compare their bases (not the bit values) and keep only matching measurements.</p></div>", unsafe_allow_html=True)
    with steps_col2:
        st.markdown("<div class='info-box'><h4>4️⃣ Error Checking</h4><p>They sacrifice some bits to check for eavesdropping. High error rate indicates interference.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><h4>5️⃣ Privacy Amplification</h4><p>The remaining bits are processed to remove any partial information an eavesdropper might have.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><h4>6️⃣ Secure Key</h4><p>Alice and Bob now share an identical, secret key for encrypting communications!</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='content-box' style='border-left-color: #ffc107;'>
        <h4 style='color: #ffc107;'>💡 The Two Bases</h4>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;'>
            <div style='background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 10px;'>
                <strong style='font-size: 1.1rem;'>Rectilinear Basis (+):</strong><br>
                <span>Horizontal (|0⟩) and Vertical (|1⟩) polarizations</span>
            </div>
            <div style='background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 10px;'>
                <strong style='font-size: 1.1rem;'>Diagonal Basis (×):</strong><br>
                <span>+45° (|0⟩) and -45° (|1⟩) polarizations</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='content-box' style='border-left-color: #17a2b8;'>
        <h4 style='color: #17a2b8;'>🛡️ Why is BB84 Unbreakable?</h4>
        <p style='margin-bottom: 0.8rem;'><strong>Heisenberg Uncertainty Principle:</strong> Measuring a quantum state in the wrong basis disturbs it.</p>
        <p style='margin-bottom: 0.8rem;'><strong>No-Cloning Theorem:</strong> It's impossible to create identical copies of unknown quantum states.</p>
        <p style='margin-bottom: 0;'><strong>Observable Disturbance:</strong> Any eavesdropping attempt introduces detectable errors in the transmission.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box" style="text-align: center; margin: 3rem 0;">
        <h2 style='font-size: 2.2rem; margin-bottom: 1rem;'>🧪 Ready to Experience BB84 in Action?</h2>
        <p style='font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.95;'>Try our interactive BB84 simulator and see quantum key distribution working in real-time!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <a href="https://bb84.srijan.dpdns.org/" target="_blank" style="text-decoration: none;">
                <button class="custom-link-button">🚀 ENTER THE SIMULATION LAB</button>
            </a>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

with tab5:
    st.markdown('<p class="section-header">Meet The Team</p>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The innovators dedicated to making quantum concepts accessible to all.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/abhinav.jpeg?raw=true" class="profile-img">
            <p class="profile-name">ABHINAV SUNEESH</p>
            <p class="profile-role">BB84 in DFS Researcher</p>
            <p class="profile-bio">Explores how BB84 operates within a Decoherence-Free Subspace to protect information from environmental noise.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/ibhann.jpeg?raw=true" class="profile-img">
            <p class="profile-name">IBHAN MUKHERJEE</p>
            <p class="profile-role">How To Catch the Thief?</p>
            <p class="profile-bio">The sneaky tester who tries to intercept the quantum key, showing how BB84 detects intrusions.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0032.jpg?raw=true" class="profile-img">
            <p class="profile-name">HARI ASHWIN</p>
            <p class="profile-role">Qubits and Gates Expert</p>
            <p class="profile-bio">The technical mind explaining how qubits are prepared, transmitted, and measured using quantum logic gates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    _, col4, col5, _ = st.columns([0.5, 1, 1, 0.5], gap="large")
    with col4:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/gucci.jpeg?raw=true" class="profile-img">
            <p class="profile-name">SRIJAN GUCHHAIT</p>
            <p class="profile-role">BB84 Idealist</p>
            <p class="profile-bio">Introduces the BB84 protocol and demonstrates how it works perfectly in an ideal, noise-free setting.</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0008.jpg?raw=true" class="profile-img">
            <p class="profile-name">OM THAVARI</p>
            <p class="profile-role">Faraday Rotator Technician</p>
            <p class="profile-bio">Manages optical components, ensuring polarization rotations are precise and consistent.</p>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; border-top: 2px solid rgba(102, 126, 234, 0.3); margin-top: 3rem;'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>Made By Engineers 👷🏻‍♂️ For Curiosity Not Just For Credits 😉</p>
        <p style='font-size: 0.9rem; opacity: 0.8;'>Visualizing quantum states on the Bloch sphere | Ibhan Mukherjee</p>
    </div>
""", unsafe_allow_html=True)
