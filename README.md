# TQS-PROJECT-1

## Descrizione
Il repository contiene il primo progetto del corso [TECNOLOGIE QUANTISTICHE PER LA SICUREZZA](https://docenti.unisa.it/030400/didattica?anno=2025&id=524113&cId=10000-2025&pId=N0*N0*S2).

In particolare si è scelto di comparare un [Known Plaintext Attack](https://en.wikipedia.org/wiki/Known-plaintext_attack) classico con la controparte quantistica realizzata con l'algoritmo di Grover.

Dato che questa tipologia di attacco richiede fin troppe risorse computazionali per essere efficace, si è deciso di attaccare l'algoritmo S-DES, una versione semplificata del DES nato in ambito accademico.

### Strumenti utilizzati
Sono state utilizzate le seguenti librerie:
- [sdes](https://pypi.org/project/sdes/): per effettuare la cifratura e la cifratura dei testi;
- [Qiskit](https://quantum.cloud.ibm.com/docs/en/guides): per la scrittura dei circuiti quantistici;
- [Qiskit Aer](https://qiskit.github.io/qiskit-aer/): per la simulazione di modelli quantistici con o senza rumore.

## Istruzioni

Si consiglia di creare un'ambiente dedicato per evitare conflitti durante l'installazione delle dipendenze.

In particolare, consigliamo di creare un'ambiente virtuale con [venv](https://docs.python.org/3/library/venv.html) utilizzando il comando seguente:

```
python -m venv ./<NOME-AMBIENTE>
```

Successivamente sarà possibile entrare nell'ambiente:

```
source ./<NOME-AMBIENTE>/bin/activate
```

Adesso possiamo clonare il progetto:

```
git clone https://github.com/gianf03/TQS_PROJECT_1.git
```

Infine, entriamo nella cartella del progetto:

```
cd TQS_PROJECT_1/
```

### Dipendenze
Le dipendenze possono essere installate facilmente con:

```
pip install -r requirements.txt
```

### Utilizzo
Per un attacco classico:

```
python classic_key_recovery_attack
```

Per calcolare la distribuzione delle chiavi:

```
python average_key_for_plain_cipher_couple.py
```

Per un attacco quantistico:

```
python QUANTUM/attack.py
```

Ovviamente è possibile modificare il codice sorgente dei vari programmi per modificare la coppia _plaintext_ - _ciphertext_.

## Licensa
Tutto il progetto è distribuito sotto licenza [MIT](https://mit-license.org/).