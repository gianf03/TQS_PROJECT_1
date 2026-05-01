from qiskit import QuantumCircuit
from utils import apply_pbox, q_split, q_merge
from KeyGenerator import KeyGenerator
from sbox import sbox1_gate, sbox2_gate

def build_sdes_oracle(plaintext_bin_str, ciphertext_bin_str):
    # GESTIONE QUBIT:
    # Qubits 0-9: Chiave in superposizione (10 qubit)
    # Qubits 10-17: Spazio di lavoro per il cifrato (8 qubit)
    # Qubits 18-25: Ancille per l'Espansione a 8 bit (8 qubit)
    # Qubits 26-29: Ancille per l'Output delle S-Box (4 qubit)
    # Qubit 30: Qubit di Fase per Grover (1 qubit)

    TOTAL_QUBITS = 31
    qc = QuantumCircuit(TOTAL_QUBITS, name="S-DES_Oracle")
    
    key_qubits = list(range(10))            # chiave di 10 bit
    work_text = list(range(10, 18))         # testo in chiaro di 8 bit
    ancillas = list(range(18, 26))          # bit di ancilla usati per espansione e quant'altro
    sbox_outs = list(range(26, 30))         # ciascuna S-box produce 2 bit di output, per un totale di 4 bit
    phase_qubit = 30
    
    key_gen = KeyGenerator()
    k1_idx, k2_idx = key_gen.get_subkeys_indices(key_qubits)   # generazione delle sottochiavi dalla master key
    
    # Permutazioni usate nella versione standard del S-DES
    IP_order = [1, 5, 2, 0, 3, 7, 4, 6]
    EP_order = [3, 0, 1, 2, 1, 2, 3, 0]
    SP_order = [1, 3, 2, 0]            
    LP_order = [3, 0, 2, 4, 6, 1, 7, 5]    

    # Creazione circuito che implementa la cifratura (da usare come building block nell'oracolo) 
    forward_qc = QuantumCircuit(TOTAL_QUBITS, name="S-DES_Forward")
            
    # Applicazione  della permutazione iniziale al plaintext e successiva divisione in due parti
    current_text = apply_pbox(work_text, IP_order)
    L, R = q_split(current_text)

    # Esecuzione delle due funzioni di round sul plaintext
    for round_num, k_idx in enumerate([k1_idx, k2_idx]):
        # 1. Espansione
        for i, r_idx in enumerate(EP_order):
            forward_qc.cx(R[r_idx], ancillas[i])
            
        # 2. XOR con chiave
        for i in range(8):
            forward_qc.cx(k_idx[i], ancillas[i])
            
        # 3. S-Box
        forward_qc.append(sbox1_gate, ancillas[0:4] + sbox_outs[0:2])
        forward_qc.append(sbox2_gate, ancillas[4:8] + sbox_outs[2:4])
        
        # 4. P4 (si applica la permutazione sui nuovi qubit di output)
        p4_out = apply_pbox(sbox_outs, SP_order)
        
        # 5. XOR con L
        for i in range(4):
            forward_qc.cx(p4_out[i], L[i])
            
        # 6. Pulizia degli ancilla (inversione delle porte usando gli stessi identici qubit usati all'inizio)
        forward_qc.append(sbox2_gate.inverse(), ancillas[4:8] + sbox_outs[2:4])
        forward_qc.append(sbox1_gate.inverse(), ancillas[0:4] + sbox_outs[0:2])
        
        for i in range(7, -1, -1):
            forward_qc.cx(k_idx[i], ancillas[i])
        for i in range(7, -1, -1):
            forward_qc.cx(R[EP_order[i]], ancillas[i])
            
        # 7. Swap finale
        if round_num == 0:
            L, R = R, L

    # Applicazione permutazione inversa
    final_text = apply_pbox(q_merge(L, R), LP_order)


    # Inizializzazione dei qubit del plaintext secondo il valore noto
    for i, bit in enumerate(plaintext_bin_str):
        if bit == '1':
            qc.x(work_text[i])
    
    qc.append(forward_qc.to_gate(), range(TOTAL_QUBITS))

    # Negazione dei qubit del ciphertext che devono essere '0' per abilitare il controllo MCX
    for i, bit in enumerate(ciphertext_bin_str):
        if bit == '0':
            qc.x(final_text[i])
            
    # Phase kickback: flip del qubit di fase se il ciphertext corrisponde al valore atteso
    qc.mcx(final_text, phase_qubit)
    
    # Ripristino dei qubit del ciphertext modificati in precedenza (undo)
    for i, bit in enumerate(ciphertext_bin_str):
        if bit == '0':
            qc.x(final_text[i])
            
    # Rollback
    qc.append(forward_qc.inverse().to_gate(), range(TOTAL_QUBITS))

    # Ripristino dei qubit del plaintext modificati in precedenza (undo)
    for i, bit in enumerate(plaintext_bin_str):
        if bit == '1':
            qc.x(work_text[i])

    fig1 = forward_qc.draw('mpl', fold=-1, scale=1)
    #fig1.savefig('forward.png', dpi=150, bbox_inches='tight')
    fig2 = qc.draw('mpl', fold=-1, scale=1)
    #fig2.savefig('oracle.png', dpi=150, bbox_inches='tight')

    return qc.to_gate()
