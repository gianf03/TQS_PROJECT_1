from qiskit import QuantumCircuit
from qiskit_aer import Aer
import math


# =========================================================
# ORACLE CORRETTO: PHASE FLIP SULLA CHIAVE GIUSTA
# =========================================================
def grover_oracle_secret_key(secret_key: str):
    """
    Oracle Grover standard:
    applica fase -1 SOLO allo stato |secret_key⟩
    """

    n = len(secret_key)
    qc = QuantumCircuit(n + 1, name="Grover_Oracle")

    # ----------------------------
    # STEP 1: portiamo |secret_key> a |111...1>
    # con X dove il bit è 0
    # ----------------------------
    for i, bit in enumerate(secret_key):
        if bit == "0":
            qc.x(i)

    # ----------------------------
    # STEP 2: multi-controlled Z
    # (flip fase sullo stato target)
    # ----------------------------
    qc.h(n)                      # ancilla -> |-> per phase kickback
    qc.mcx(list(range(n)), n)   # controlla tutti i qubit
    qc.h(n)

    # ----------------------------
    # STEP 3: undo X (ripristino base states)
    # ----------------------------
    for i, bit in enumerate(secret_key):
        if bit == "0":
            qc.x(i)

    return qc


# =========================================================
# DIFFUSER
# =========================================================
def diffuser(n):
    qc = QuantumCircuit(n)

    qc.h(range(n))
    qc.x(range(n))

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    qc.x(range(n))
    qc.h(range(n))

    return qc


# =========================================================
# GROVER ATTACK
# =========================================================
def grover_attack(secret_key):

    n = len(secret_key)
    qc = QuantumCircuit(n + 1, n)

    # 1. superposizione
    qc.h(range(n))

    # ancilla |-> per phase kickback
    qc.x(n)
    qc.h(n)

    oracle = grover_oracle_secret_key(secret_key)
    diff = diffuser(n)

    iterations = int(math.pi / 4 * math.sqrt(2 ** n))

    for _ in range(iterations):
        qc.append(oracle.to_gate(), range(n + 1))
        qc.append(diff.to_gate(), range(n))

    qc.measure(range(n), range(n))

    return qc


# =========================================================
# RUN SIMULAZIONE
# =========================================================
def run():
    secret_key = "1101010011"  # 10 bit S-DES key

    qc = grover_attack(secret_key)

    backend = Aer.get_backend("aer_simulator")
    compiled = transpile(qc, backend)

    result = backend.run(compiled, shots=1024).result()
    counts = result.get_counts()

    print("\n=== RISULTATO GROVER ===")
    print(counts)


if __name__ == "__main__":
    run()