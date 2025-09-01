#!/usr/bin/env python3
# Generate message.hex for toy RSA Verilog testbench

N = 3233  # modulus
e = 17  # public exponent

# Message to encrypt
plaintext = "Welcome to Fractile!"
datafile = "./data/message.hex"

with open(datafile, "w") as f:
    for ch in plaintext:
        m = ord(ch)  # ASCII value
        c = pow(m, e, N)  # RSA encrypt: c = m^e mod N
        f.write(f"{c:X}\n")

print("Wrote", datafile, "with ciphertexts for:", plaintext)
