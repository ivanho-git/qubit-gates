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

# Enhanced CSS with dark mode support
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background adapts to theme */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Content container with theme-aware background */
    .block-container {
        padding: 2rem 3rem;
        background: color-mix(in srgb, var(--background-color) 95%, transparent);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem auto;
        backdrop-filter: blur(10px);
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-color);
        opacity: 0.8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Tabs Styling - theme aware */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: color-mix(in srgb, var(--background-color) 90%, var(--primary-color) 10%);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: color-mix(in srgb, var(--background-color) 95%, transparent);
        border-radius: 10px;
        color: var(--text-color);
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
    
    /* Info Boxes - dark mode compatible */
    .info-box {
        background: color-mix(in srgb, var(--background-color) 90%, #667eea 10%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: var(--text-color);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .info-box h3, .info-box h4, .info-box p, .info-box ul, .info-box li {
        color: var(--text-color) !important;
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
    
    /* Card Styling - theme aware */
    .card {
        background: color-mix(in srgb, var(--background-color) 95%, transparent);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin: 1rem 0;
        border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
        transform: translateY(-5px);
    }
    
    /* Gradient Boxes - always light text */
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
    
    .feature-box h4, .feature-box p {
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
    
    /* Expander - theme aware */
    .streamlit-expanderHeader {
        background: color-mix(in srgb, var(--background-color) 90%, #667eea 10%);
        border-radius: 10px;
        font-weight: 600;
        color: #667eea;
    }
    
    /* Profile cards - theme aware */
    .profile-card {
        background: color-mix(in srgb, var(--background-color) 95%, transparent);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
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
        color: var(--text-color);
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Warning/Info colored boxes - theme aware */
    .warning-box {
        background: color-mix(in srgb, var(--background-color) 85%, #ffc107 15%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .warning-box h4 {
        color: #ff9800 !important;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .info-highlight {
        background: color-mix(in srgb, var(--background-color) 85%, #17a2b8 15%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #0c5460;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .info-highlight h4 {
        color: #17a2b8 !important;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .success-box {
        background: color-mix(in srgb, var(--background-color) 85%, #28a745 15%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #155724;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .success-box h4 {
        color: #28a745 !important;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Ensure all text in colored boxes is readable */
    .warning-box p, .warning-box ul, .warning-box li,
    .info-highlight p, .info-highlight ul, .info-highlight li,
    .success-box p, .success-box ul, .success-box li {
        color: var(--text-color) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .block-container {
            padding: 1rem;
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
                elif gate == "SX (√X)":
                    qc.sx(0)
                elif gate == "SY (√Y)":
                    qc.sy(0)
                elif gate == "RZ(π/2)":
                    qc.rz(np.pi/2, 0)
            
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
            st.markdown("#### 🔧 Quantum Circuit")
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except:
                st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<p class="section-header">Rotation Gates with Animation</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
                
                st.markdown("#### 🔧 Circuit Diagram")
                try:
                    circuit_fig = qc.draw(output='mpl', style='iqp')
                    st.pyplot(circuit_fig)
                    plt.close()
                except:
                    st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Set your rotation parameters and click 'Apply Rotation'")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<p class="section-header">Faraday Rotator Simulator</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
    <h4>🔬 About the Faraday Effect</h4>
    <p>
    The Faraday effect causes the polarization plane of light to rotate when passing through a medium 
    in a magnetic field. This quantum phenomenon is fundamental to optical isolators and magnetic field sensors.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Physical Parameters")
        
        initial_polarization = st.radio(
            "**Initial Polarization:**",
            ["Horizontal (|H⟩)", "Vertical (|V⟩)", "Diagonal (+45°)", "Anti-diagonal (-45°)"]
        )
        
        st.markdown("---")
        
        verdet_constant = st.slider(
            "**Verdet Constant (rad/T·m):**",
            min_value=1.0,
            max_value=100.0,
            value=50.0,
            step=1.0
        )
        
        magnetic_field = st.slider(
            "**Magnetic Field (Tesla):**",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        
        path_length = st.slider(
            "**Path Length (meters):**",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
        
        faraday_angle = verdet_constant * magnetic_field * path_length
