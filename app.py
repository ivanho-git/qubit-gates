import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(page_title="Qubit Gate Simulator", page_icon="⚛️", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚛️ Quantum Gate Simulator</p>', unsafe_allow_html=True)

# Create tabs for different modes
tab1, tab2 = st.tabs(["🎯 Standard Gates", "🌀 Rotation Gates & Animation"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ Controls")
        
        # Select original qubit
        original_bit = st.selectbox("**Initial Qubit State:**", ["|0>", "|1>", "|+>", "|->"])
        
        st.markdown("---")
        
        # Select gate with categories
        st.markdown("**Select Gate:**")
        gate_category = st.radio(
            "Gate Category:",
            ["Pauli Gates", "Hadamard & Phase", "Advanced Gates"],
            label_visibility="collapsed"
        )
        
        if gate_category == "Pauli Gates":
            gate = st.selectbox("Gate:", ["No Gate", "X (NOT)", "Y", "Z"], label_visibility="collapsed")
        elif gate_category == "Hadamard & Phase":
            gate = st.selectbox("Gate:", ["H (Hadamard)", "S (Phase)", "T", "S† (S-dagger)", "T† (T-dagger)"], label_visibility="collapsed")
        else:
            gate = st.selectbox("Gate:", ["SX (√X)", "SY (√Y)", "SWAP (root)"], label_visibility="collapsed")
        
        st.markdown("---")
        
        # Apply gate button
        apply_button = st.button("🚀 Apply Gate", use_container_width=True)
        
        # Display gate information
        st.markdown("### 📖 Gate Info")
        gate_info = {
            "No Gate": "Identity operation - qubit unchanged",
            "X (NOT)": "Bit flip: |0>↔|1>",
            "Y": "Bit & phase flip",
            "Z": "Phase flip: |1>→-|1>",
            "H (Hadamard)": "Creates superposition",
            "S (Phase)": "90° phase rotation",
            "T": "45° phase rotation",
            "S† (S-dagger)": "Inverse of S gate",
            "T† (T-dagger)": "Inverse of T gate",
            "SX (√X)": "Square root of X gate",
            "SY (√Y)": "Square root of Y gate",
            "SWAP (root)": "Square root of SWAP"
        }
        
        st.markdown(f'<div class="info-box">{gate_info.get(gate, "")}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Bloch Sphere Visualization")
        
        if apply_button:
            # Initialize qubit
            qc = QuantumCircuit(1)
            
            # Set initial state
            if original_bit == "|1>":
                qc.x(0)
            elif original_bit == "|+>":
                qc.h(0)
            elif original_bit == "|->":
                qc.x(0)
                qc.h(0)
            
            # Apply gate
            if gate != "No Gate":
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
                elif gate == "SWAP (root)":
                    # For single qubit, apply a custom rotation
                    qc.rz(np.pi/2, 0)
            
            # Get statevector
            state = Statevector.from_instruction(qc)
            
            # Display state coefficients
            state_array = state.data
            st.markdown(f"**State Vector:** α|0⟩ + β|1⟩")
            st.markdown(f"- α (amplitude for |0⟩): `{state_array[0]:.4f}`")
            st.markdown(f"- β (amplitude for |1⟩): `{state_array[1]:.4f}`")
            st.markdown(f"- Probabilities: |0⟩: `{abs(state_array[0])**2:.4f}`, |1⟩: `{abs(state_array[1])**2:.4f}`")
            
            # Plot Bloch sphere
            fig = plot_bloch_multivector(state)
            st.pyplot(fig)
            plt.close()
            
            # Show circuit
            st.markdown("### 🔧 Circuit Diagram")
            circuit_fig = qc.draw(output='mpl', style='iqp')
            st.pyplot(circuit_fig)
            plt.close()

with tab2:
    st.markdown("### 🌀 Rotation Gates with Animation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 🎚️ Rotation Controls")
        
        # Initial state
        initial_state = st.selectbox("**Initial State:**", ["|0>", "|1>", "|+>", "|->"], key="rot_state")
        
        st.markdown("---")
        
        # Rotation axis
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        
        # Angle control
        angle_degrees = st.slider(
            "**Rotation Angle (degrees):**",
            min_value=0,
            max_value=360,
            value=90,
            step=15
        )
        
        angle_radians = np.deg2rad(angle_degrees)
        
        st.markdown(f"**Angle in radians:** `{angle_radians:.4f}` rad")
        st.markdown(f"**Angle in terms of π:** `{angle_degrees/180:.2f}π`")
        
        st.markdown("---")
        
        # Animation controls
        st.markdown("#### 🎬 Animation")
        animate = st.checkbox("Show rotation animation", value=False)
        
        if animate:
            num_steps = st.slider("Animation steps:", 5, 50, 20)
        
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True, key="apply_rot")
    
    with col2:
        st.markdown("### 📊 Rotation Visualization")
        
        if apply_rotation:
            if animate:
                # Create animation frames
                angles = np.linspace(0, angle_radians, num_steps)
                
                # Placeholder for animation
                animation_placeholder = st.empty()
                
                for i, current_angle in enumerate(angles):
                    qc = QuantumCircuit(1)
                    
                    # Set initial state
                    if initial_state == "|1>":
                        qc.x(0)
                    elif initial_state == "|+>":
                        qc.h(0)
                    elif initial_state == "|->":
                        qc.x(0)
                        qc.h(0)
                    
                    # Apply rotation
                    if rotation_axis == "X":
                        qc.rx(current_angle, 0)
                    elif rotation_axis == "Y":
                        qc.ry(current_angle, 0)
                    else:
                        qc.rz(current_angle, 0)
                    
                    # Get statevector and plot
                    state = Statevector.from_instruction(qc)
                    fig = plot_bloch_multivector(state)
                    
                    with animation_placeholder.container():
                        st.markdown(f"**Step {i+1}/{num_steps}** - Angle: {np.rad2deg(current_angle):.1f}°")
                        st.pyplot(fig)
                    
                    plt.close()
                
                st.success("✅ Animation complete!")
                
            else:
                # Static rotation
                qc = QuantumCircuit(1)
                
                # Set initial state
                if initial_state == "|1>":
                    qc.x(0)
                elif initial_state == "|+>":
                    qc.h(0)
                elif initial_state == "|->":
                    qc.x(0)
                    qc.h(0)
                
                # Apply rotation
                if rotation_axis == "X":
                    qc.rx(angle_radians, 0)
                elif rotation_axis == "Y":
                    qc.ry(angle_radians, 0)
                else:
                    qc.rz(angle_radians, 0)
                
                # Get statevector
                state = Statevector.from_instruction(qc)
                state_array = state.data
                
                # Display state information
                st.markdown(f"**Final State Vector:**")
                st.markdown(f"- α (|0⟩): `{state_array[0]:.4f}`")
                st.markdown(f"- β (|1⟩): `{state_array[1]:.4f}`")
                
                # Plot Bloch sphere
                fig = plot_bloch_multivector(state)
                st.pyplot(fig)
                plt.close()
                
                # Show circuit
                st.markdown("### 🔧 Circuit Diagram")
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Qiskit and Streamlit | Visualizing quantum states on the Bloch sphere</p>
    </div>
""", unsafe_allow_html=True)
