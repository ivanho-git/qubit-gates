import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

st.title("Qubit Gate Simulator")

# Select original qubit
original_bit = st.selectbox("Select the original qubit:", ["|0>", "|1>"])

# Select gate
gate = st.selectbox("Select a gate to apply:", ["No Gate", "X", "Y", "Z", "H"])

# Apply gate button
if st.button("Apply Gate"):
    # Initialize qubit
    qc = QuantumCircuit(1)
    if original_bit == "|1>":
        qc.x(0)  # set qubit to |1>

    # Apply gate only if it's not "No Gate"
    if gate != "No Gate":
        if gate == "X":
            qc.x(0)
        elif gate == "Y":
            qc.y(0)
        elif gate == "Z":
            qc.z(0)
        elif gate == "H":
            qc.h(0)

    # Get statevector
    state = Statevector.from_instruction(qc)

    # Plot Bloch sphere
    fig = plot_bloch_multivector(state)
    st.pyplot(fig)
