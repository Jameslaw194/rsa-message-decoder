#!/usr/bin/env python3
# Generate message.hex for toy RSA Verilog testbench
import random

N = 3233  # modulus
e = 17  # public exponent

# Message to encrypt
random_plaintext = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@£$%^&*()-=_+'\"|,./<>?`~§±", k=20))
plaintext = "Welcome to Fractile!"
datafile = "./data/message.hex"

with open(datafile, "w") as f:
    for ch in random_plaintext:
        m = ord(ch)  # ASCII value
        c = pow(m, e, N)  # RSA encrypt: c = m^e mod N
        f.write(f"{c:X}\n")

print("Wrote", datafile, "with ciphertexts for:", random_plaintext)
