# Quantum Circuit Lab

A **pure-Python quantum circuit state-vector simulator** built from first principles with complex linear algebra. Includes Hadamard, Pauli X/Y/Z, phase S/T, controlled-NOT, Bell states, GHZ states, probability distributions and reproducible measurement histograms.

## Usage
Python 3.10+; no third-party packages necessary.

```bash
python main.py --demo bell --shots 1024
python main.py --demo ghz --qubits 4
python -m unittest discover -s tests -v
```

The state vector stores complex amplitudes of 2^n computational basis states, with qubit 0 as the least-significant bit. Probabilities are the amplitude magnitudes squared. Measurement sampling does not collapse the stored state and is appropriate for repeating circuit shots.

## Engineering scope
- Single-qubit gates, CNOT entanglement, and circuit operation history
- Simulated probabilities and reproducible sampling with random seeds
- Unit tests verifying normalization, Bell states, GHZ states, and invalid inputs
- Maximum 14 qubits to bound memory/time

This is a pedagogical ideal-state simulator, not real quantum-hardware execution or a noisy channel model.

MIT licensed.