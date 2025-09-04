import random
import sympy

# RSA Key Generation

# Euclidean Algorithm
# gcd and modular inverse
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)   # gcd is b
    else:
        g, x, y = egcd(b % a, a)  # recursive step
        return (g, y - (b // a) * x, x)

# modular inverse of e mod phi
# d such that (d * e) % phi == 1
def mod_inverse(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('No modular inverse (e and phi not coprime)')
    else:
        return x % phi  # make sure d is positive

# Choose two prime numbers
p = 61
q = 53

# Compute n = p * q (the modulus)
n = p * q

# Compute Euler's totient
phi = (p - 1) * (q - 1)

# Choose a public exponent e
e = 17

# Compute the private exponent d
d = mod_inverse(e, phi)

print("Public key (e, n):", (e, n))
print("Private key (d, n):", (d, n))
