from qiskit import QuantumCircuit
import numpy as np

# ==========================================
# 1. FUNZIONI DI ROUTING (Costo Quantistico: 0)
# ==========================================
def q_split(qubit_indices):
    mid = len(qubit_indices) // 2
    return qubit_indices[:mid], qubit_indices[mid:]

def q_merge(left, right):
    return left + right

def apply_pbox(qubit_indices, out_order):
    return [qubit_indices[i] for i in out_order]

def left_shift(lst, n):
    return lst[n:] + lst[:n]

class KeyGenerator:   # nel file vecchio la classe era QuantumKeyGenerator, ma non c'è nulla di quantistico qui
    def __init__(self):
        self.P10_order = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
        self.P8_order = [5, 2, 6, 3, 7, 4, 9, 8]
        self.LeftShift1_order = [1, 2, 3, 4, 0]

    def get_subkeys_indices(self, key_qubits):
        x = apply_pbox(key_qubits, self.P10_order)
        left, right = q_split(x)
        
        left = left_shift(left, 1)
        right = left_shift(right, 1)
        
        k1_indices = apply_pbox(q_merge(left, right), self.P8_order)
        
        left = left_shift(left, 2)
        right = left_shift(right, 2)
        
        k2_indices = apply_pbox(q_merge(left, right), self.P8_order)
        
        return k1_indices, k2_indices


def sbox1_optimized():
    qc = QuantumCircuit(6, name="SBox1_opt")

    # --- o0 = b0 ⊕ b1 ⊕ b2 ---
    qc.cx(0, 4)
    qc.cx(1, 4)
    qc.cx(2, 4)

    # --- o1 = (b1 AND b2) ⊕ b3 ⊕ b0 ---
    qc.ccx(1, 2, 5)   # b1 AND b2
    qc.cx(3, 5)
    qc.cx(0, 5)

    return qc.to_gate()


