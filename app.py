import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
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
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Standard Gates", "🌀 Rotation Gates & Animation", "🔮 Faraday Rotator", "🔐 BB84 Protocol"])

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
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except Exception as e:
                st.info("Circuit diagram visualization requires additional dependencies. Showing text version:")
                st.code(qc.draw(output='text'), language='text')

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
                
                # Create initial state vector
                initial_qc = QuantumCircuit(1)
                if initial_state == "|1>":
                    initial_qc.x(0)
                elif initial_state == "|+>":
                    initial_qc.h(0)
                elif initial_state == "|->":
                    initial_qc.x(0)
                    initial_qc.h(0)
                
                initial_statevector = Statevector.from_instruction(initial_qc)
                
                # Placeholder for animation
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                import time
                
                for i, current_angle in enumerate(angles):
                    # Create a new circuit for rotation only
                    rotation_qc = QuantumCircuit(1)
                    
                    # Apply rotation to get the rotation operator
                    if rotation_axis == "X":
                        rotation_qc.rx(current_angle, 0)
                    elif rotation_axis == "Y":
                        rotation_qc.ry(current_angle, 0)
                    else:
                        rotation_qc.rz(current_angle, 0)
                    
                    # Apply rotation to initial state
                    state = initial_statevector.evolve(rotation_qc)
                    
                    # Plot
                    fig = plot_bloch_multivector(state)
                    
                    with animation_placeholder.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"**Step {i+1}/{num_steps}** - Angle: {np.rad2deg(current_angle):.1f}° ({current_angle:.3f} rad)")
                        with col_b:
                            state_array = state.data
                            st.markdown(f"**|α|²={abs(state_array[0])**2:.3f}**")
                            st.markdown(f"**|β|²={abs(state_array[1])**2:.3f}**")
                        st.pyplot(fig)
                    
                    plt.close()
                    
                    # Update progress bar
                    progress_bar.progress((i + 1) / num_steps)
                    
                    # Small delay for smooth animation
                    time.sleep(0.1)
                
                progress_bar.empty()
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
                try:
                    circuit_fig = qc.draw(output='mpl', style='iqp')
                    st.pyplot(circuit_fig)
                    plt.close()
                except Exception as e:
                    st.info("Circuit diagram visualization requires additional dependencies. Showing text version:")
                    st.code(qc.draw(output='text'), language='text')

with tab3:
    st.markdown("### 🔮 Faraday Rotator Simulator")
    st.markdown("""
    The Faraday effect causes the polarization plane of light to rotate when passing through a medium 
    in a magnetic field. Here we simulate this quantum mechanically with polarization states mapped to qubits.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ⚙️ Faraday Rotator Settings")
        
        # Polarization settings
        st.markdown("**Initial Polarization:**")
        initial_polarization = st.radio(
            "Choose polarization:",
            ["Horizontal (|H⟩)", "Vertical (|V⟩)", "Diagonal (+45°)", "Anti-diagonal (-45°)"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Magnetic field strength (proportional to rotation)
        st.markdown("**Magnetic Field & Material:**")
        verdet_constant = st.slider(
            "Verdet Constant (rad/T·m):",
            min_value=1.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
            help="Material property determining rotation strength"
        )
        
        magnetic_field = st.slider(
            "Magnetic Field Strength (Tesla):",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        
        path_length = st.slider(
            "Path Length (meters):",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
        
        # Calculate Faraday rotation angle
        faraday_angle = verdet_constant * magnetic_field * path_length
        faraday_angle_deg = np.rad2deg(faraday_angle) % 360
        
        st.markdown(f"""
        <div class="info-box">
        <b>Faraday Rotation:</b><br>
        θ = V × B × L<br>
        θ = {faraday_angle:.3f} rad<br>
        θ = {faraday_angle_deg:.1f}°
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Animation controls
        st.markdown("**Visualization:**")
        show_faraday_animation = st.checkbox("Animate light propagation", value=True, key="faraday_anim")
        
        if show_faraday_animation:
            propagation_steps = st.slider("Propagation steps:", 10, 50, 25, key="faraday_steps")
            animation_speed = st.slider("Animation speed:", 1, 10, 5, key="anim_speed")
        
        simulate_faraday = st.button("🔬 Run Faraday Rotator", use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Polarization Evolution")
        
        if simulate_faraday:
            # Determine initial angle
            if initial_polarization == "Horizontal (|H⟩)":
                initial_angle = 0
            elif initial_polarization == "Vertical (|V⟩)":
                initial_angle = 90
            elif initial_polarization == "Diagonal (+45°)":
                initial_angle = 45
            else:  # Anti-diagonal
                initial_angle = -45
            
            if show_faraday_animation:
                # Create animation
                angles_through_medium = np.linspace(0, faraday_angle_deg, propagation_steps)
                distances = np.linspace(0, path_length, propagation_steps)
                
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                import time
                
                for i, (rotation_angle, current_distance) in enumerate(zip(angles_through_medium, distances)):
                    # Current polarization angle
                    current_pol_angle = initial_angle + rotation_angle
                    
                    # Create polarization visualization
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                    
                    # Left plot: 3D view of light wave with rotating polarization
                    ax1 = plt.subplot(121, projection='3d')
                    
                    # Create light wave propagating along z
                    z = np.linspace(0, 2*np.pi, 100)
                    
                    # Electric field components (rotating polarization)
                    angle_rad = np.deg2rad(current_pol_angle)
                    Ex = np.cos(angle_rad) * np.sin(z)
                    Ey = np.sin(angle_rad) * np.sin(z)
                    
                    # Plot the wave
                    ax1.plot(Ex, Ey, z, 'b-', linewidth=2, label='E-field')
                    
                    # Plot polarization vector at the front
                    arrow_length = 1.2
                    ax1.quiver(0, 0, 0, 
                              arrow_length * np.cos(angle_rad), 
                              arrow_length * np.sin(angle_rad), 
                              0,
                              color='red', arrow_length_ratio=0.3, linewidth=3,
                              label=f'Polarization: {current_pol_angle:.1f}°')
                    
                    ax1.set_xlabel('Ex (Horizontal)', fontsize=10)
                    ax1.set_ylabel('Ey (Vertical)', fontsize=10)
                    ax1.set_zlabel('Propagation →', fontsize=10)
                    ax1.set_title(f'Light Wave in Medium\nDistance: {current_distance*100:.1f} cm', fontsize=12, fontweight='bold')
                    ax1.set_xlim([-1.5, 1.5])
                    ax1.set_ylim([-1.5, 1.5])
                    ax1.set_zlim([0, 2*np.pi])
                    ax1.legend(loc='upper right')
                    ax1.view_init(elev=20, azim=45)
                    
                    # Right plot: Top-down view showing polarization rotation
                    ax2.set_aspect('equal')
                    
                    # Draw reference axes
                    ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3, label='Horizontal')
                    ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3, label='Vertical')
                    ax2.text(1.3, 0, 'H', fontsize=12, ha='left', va='center')
                    ax2.text(0, 1.3, 'V', fontsize=12, ha='center', va='bottom')
                    
                    # Draw initial polarization (faded)
                    initial_rad = np.deg2rad(initial_angle)
                    ax2.arrow(0, 0, 
                             np.cos(initial_rad), 
                             np.sin(initial_rad), 
                             head_width=0.15, head_length=0.15, 
                             fc='blue', ec='blue', alpha=0.3, linewidth=2,
                             label=f'Initial: {initial_angle}°')
                    
                    # Draw current polarization
                    ax2.arrow(0, 0, 
                             np.cos(angle_rad), 
                             np.sin(angle_rad), 
                             head_width=0.15, head_length=0.15, 
                             fc='red', ec='red', alpha=1.0, linewidth=3,
                             label=f'Current: {current_pol_angle:.1f}°')
                    
                    # Draw rotation arc
                    if rotation_angle > 0:
                        arc_angles = np.linspace(np.deg2rad(initial_angle), angle_rad, 50)
                        arc_x = 0.5 * np.cos(arc_angles)
                        arc_y = 0.5 * np.sin(arc_angles)
                        ax2.plot(arc_x, arc_y, 'g--', linewidth=2, alpha=0.7)
                        ax2.text(0, -0.7, f'Rotation: {rotation_angle:.1f}°', 
                                fontsize=11, ha='center', color='green', fontweight='bold')
                    
                    ax2.set_xlim([-1.5, 1.5])
                    ax2.set_ylim([-1.5, 1.5])
                    ax2.set_title(f'Polarization Plane (Top View)\nMagnetic Field: {magnetic_field:.1f} T', 
                                 fontsize=12, fontweight='bold')
                    ax2.legend(loc='upper right', fontsize=9)
                    ax2.grid(True, alpha=0.3)
                    ax2.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
                    ax2.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
                    
                    plt.tight_layout()
                    
                    with animation_placeholder.container():
                        col_a, col_b, col_c = st.columns([2, 2, 2])
                        with col_a:
                            st.metric("Distance", f"{current_distance*100:.1f} cm", f"+{(current_distance/path_length)*100:.0f}%")
                        with col_b:
                            st.metric("Rotation", f"{rotation_angle:.1f}°", f"{(rotation_angle/faraday_angle_deg)*100:.0f}%")
                        with col_c:
                            st.metric("Polarization", f"{current_pol_angle:.1f}°")
                        
                        st.pyplot(fig)
                    
                    plt.close()
                    progress_bar.progress((i + 1) / propagation_steps)
                    time.sleep(0.1 / animation_speed)
                
                progress_bar.empty()
                st.success(f"✅ Light polarization rotated from {initial_angle}° to {initial_angle + faraday_angle_deg:.1f}° ({faraday_angle_deg:.1f}° rotation)")
                
                # Also show quantum state
                st.markdown("---")
                st.markdown("### ⚛️ Quantum State Representation")
                
                # Map to quantum state
                qc_initial = QuantumCircuit(1)
                if initial_polarization == "Horizontal (|H⟩)":
                    pass
                elif initial_polarization == "Vertical (|V⟩)":
                    qc_initial.x(0)
                elif initial_polarization == "Diagonal (+45°)":
                    qc_initial.h(0)
                else:
                    qc_initial.x(0)
                    qc_initial.h(0)
                
                initial_state = Statevector.from_instruction(qc_initial)
                
                # Apply rotation
                rotation_qc = QuantumCircuit(1)
                rotation_qc.rz(2 * faraday_angle, 0)
                final_state = initial_state.evolve(rotation_qc)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Initial State**")
                    fig = plot_bloch_multivector(initial_state)
                    st.pyplot(fig)
                    plt.close()
                with col2:
                    st.markdown("**Final State**")
                    fig = plot_bloch_multivector(final_state)
                    st.pyplot(fig)
                    plt.close()
                
            else:
                # Static visualization - show final state
                final_pol_angle = initial_angle + faraday_angle_deg
                
                # Create static visualization
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                # Left: 3D wave
                ax1 = plt.subplot(121, projection='3d')
                z = np.linspace(0, 2*np.pi, 100)
                angle_rad = np.deg2rad(final_pol_angle)
                Ex = np.cos(angle_rad) * np.sin(z)
                Ey = np.sin(angle_rad) * np.sin(z)
                
                ax1.plot(Ex, Ey, z, 'b-', linewidth=2, label='E-field')
                arrow_length = 1.2
                ax1.quiver(0, 0, 0, 
                          arrow_length * np.cos(angle_rad), 
                          arrow_length * np.sin(angle_rad), 
                          0,
                          color='red', arrow_length_ratio=0.3, linewidth=3,
                          label=f'Polarization: {final_pol_angle:.1f}°')
                
                ax1.set_xlabel('Ex (Horizontal)', fontsize=10)
                ax1.set_ylabel('Ey (Vertical)', fontsize=10)
                ax1.set_zlabel('Propagation →', fontsize=10)
                ax1.set_title(f'Final Light Wave\nAfter {path_length*100:.1f} cm', fontsize=12, fontweight='bold')
                ax1.set_xlim([-1.5, 1.5])
                ax1.set_ylim([-1.5, 1.5])
                ax1.set_zlim([0, 2*np.pi])
                ax1.legend()
                ax1.view_init(elev=20, azim=45)
                
                # Right: Polarization comparison
                ax2.set_aspect('equal')
                ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                ax2.text(1.3, 0, 'H', fontsize=12)
                ax2.text(0, 1.3, 'V', fontsize=12)
                
                # Initial
                initial_rad = np.deg2rad(initial_angle)
                ax2.arrow(0, 0, np.cos(initial_rad), np.sin(initial_rad), 
                         head_width=0.15, head_length=0.15, 
                         fc='blue', ec='blue', alpha=0.3, linewidth=2,
                         label=f'Initial: {initial_angle}°')
                
                # Final
                ax2.arrow(0, 0, np.cos(angle_rad), np.sin(angle_rad), 
                         head_width=0.15, head_length=0.15, 
                         fc='red', ec='red', linewidth=3,
                         label=f'Final: {final_pol_angle:.1f}°')
                
                # Arc
                arc_angles = np.linspace(initial_rad, angle_rad, 50)
                arc_x = 0.5 * np.cos(arc_angles)
                arc_y = 0.5 * np.sin(arc_angles)
                ax2.plot(arc_x, arc_y, 'g--', linewidth=2, alpha=0.7)
                ax2.text(0, -0.7, f'Faraday Rotation: {faraday_angle_deg:.1f}°', 
                        fontsize=11, ha='center', color='green', fontweight='bold')
                
                ax2.set_xlim([-1.5, 1.5])
                ax2.set_ylim([-1.5, 1.5])
                ax2.set_title(f'Polarization Rotation\nB = {magnetic_field:.1f} T, L = {path_length*100:.1f} cm', 
                             fontsize=12, fontweight='bold')
                ax2.legend(loc='upper right')
                ax2.grid(True, alpha=0.3)
                ax2.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
                ax2.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                
                this is now a **proper Faraday rotator** where you can clearly see the light's polarization plane rotating as it propagates through the magnetic medium! The 3D wave and 2D polarization diagrams make it much easier to understand what's actually happening physically. 🌟

with tab4:
    st.markdown("### 🔐 BB84 Quantum Key Distribution Protocol")
    
    # Create an attractive hero section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h1 style='color: white; text-align: center; margin-bottom: 1rem; font-size: 2.5rem;'>
                🔐 BB84 Protocol
            </h1>
            <p style='color: white; text-align: center; font-size: 1.2rem; opacity: 0.95;'>
                The First Quantum Cryptography Protocol - Absolutely Secure Communication
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Introduction section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3>📚 What is BB84?</h3>
        <p>
        <strong>BB84</strong> (Bennett-Brassard 1984) is the first and most famous quantum key distribution protocol. 
        It allows two parties, Alice and Bob, to generate a shared secret key that is provably secure against 
        any eavesdropper, even one with unlimited computing power.
        </p>
        <p>
        The security comes from the fundamental laws of quantum mechanics - any attempt to measure or intercept 
        the quantum states will inevitably disturb them, alerting Alice and Bob to the presence of an eavesdropper.
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
    
    # How it works section
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 5px solid #667eea;'>
        <h3 style='color: #667eea; margin-bottom: 1rem;'>🔬 How Does BB84 Work?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Protocol steps
    steps_col1, steps_col2 = st.columns(2)
    
    with steps_col1:
        st.markdown("""
        <div class="info-box">
        <h4>1️⃣ Quantum Transmission</h4>
        <p>Alice encodes random bits using two different bases (rectilinear and diagonal) and sends photons to Bob.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>2️⃣ Random Measurement</h4>
        <p>Bob randomly chooses bases to measure the received photons, recording the results.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>3️⃣ Basis Reconciliation</h4>
        <p>Alice and Bob publicly compare their bases (not the bit values) and keep only matching measurements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="info-box">
        <h4>4️⃣ Error Checking</h4>
        <p>They sacrifice some bits to check for eavesdropping. High error rate indicates interference.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>5️⃣ Privacy Amplification</h4>
        <p>The remaining bits are processed to remove any partial information an eavesdropper might have.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>6️⃣ Secure Key</h4>
        <p>Alice and Bob now share an identical, secret key for encrypting communications!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Polarization bases explanation
    st.markdown("""
    <div style='background-color: #fff3cd; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 2rem;'>
        <h4 style='color: #856404; margin-bottom: 1rem;'>💡 The Two Bases</h4>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
            <div>
                <strong style='color: #856404;'>Rectilinear Basis (+):</strong><br>
                Horizontal (|0⟩) and Vertical (|1⟩) polarizations
            </div>
            <div>
                <strong style='color: #856404;'>Diagonal Basis (×):</strong><br>
                +45° (|0⟩) and -45° (|1⟩) polarizations
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Why it's secure section
    st.markdown("""
    <div style='background-color: #d1ecf1; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #0c5460; margin-bottom: 2rem;'>
        <h4 style='color: #0c5460; margin-bottom: 1rem;'>🛡️ Why is BB84 Unbreakable?</h4>
        <p style='margin-bottom: 0.5rem;'><strong>Heisenberg Uncertainty Principle:</strong> Measuring a quantum state in the wrong basis disturbs it.</p>
        <p style='margin-bottom: 0.5rem;'><strong>No-Cloning Theorem:</strong> It's impossible to create identical copies of unknown quantum states.</p>
        <p style='margin-bottom: 0;'><strong>Observable Disturbance:</strong> Any eavesdropping attempt introduces detectable errors in the transmission.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-world applications
    st.markdown("""
    <div style='background-color: #d4edda; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #155724; margin-bottom: 2rem;'>
        <h4 style='color: #155724; margin-bottom: 1rem;'>🌍 Real-World Applications</h4>
        <ul style='margin-bottom: 0;'>
            <li><strong>Banking & Finance:</strong> Securing high-value financial transactions</li>
            <li><strong>Government Communications:</strong> Protecting classified information</li>
            <li><strong>Quantum Internet:</strong> Building the foundation for quantum networks</li>
            <li><strong>Satellite QKD:</strong> China's Micius satellite demonstrated space-based BB84</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action - Interactive simulator
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 3rem 2rem; 
                border-radius: 15px; 
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
        <h2 style='color: white; margin-bottom: 1rem; font-size: 2rem;'>
            🧪 Ready to Experience BB84 in Action?
        </h2>
        <p style='color: white; font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.95;'>
            Try our interactive BB84 simulator and see quantum key distribution working in real-time!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 ENTER THE SIMULATION LAB", use_container_width=True, type="primary"):
            st.markdown("""
                <meta http-equiv="refresh" content="0; url=https://bb84.srijan.dpdns.org/" />
            """, unsafe_allow_html=True)
            st.markdown("""
                <script>
                    window.open('https://bb84.srijan.dpdns.org/', '_blank');
                </script>
            """, unsafe_allow_html=True)
            st.success("🎉 Opening BB84 Simulation Lab in a new tab...")
            st.markdown("[Click here if the page doesn't open automatically](https://bb84.srijan.dpdns.org/)")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Additional resources
    with st.expander("📖 Learn More About BB84"):
        st.markdown("""
        ### Further Reading
        
        - **Original Paper:** Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
        - **Key Concepts:** Quantum mechanics, photon polarization, basis reconciliation, privacy amplification
        - **Modern Implementations:** Commercial QKD systems are now available with distances up to 100+ km
        
        ### Historical Context
        
        BB84 was proposed by Charles Bennett and Gilles Brassard in 1984, making it one of the earliest applications 
        of quantum mechanics to information theory. It laid the foundation for the entire field of quantum cryptography.
        
        ### Recent Achievements
        
        - **2017:** China's Micius satellite achieved intercontinental quantum key distribution
        - **2020:** Commercial quantum networks deployed in major cities worldwide
        - **2023:** Record-breaking QKD distances achieved with trusted node networks
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Qiskit and Streamlit | Visualizing quantum states on the Bloch sphere</p>
    </div>
""", unsafe_allow_html=True)
