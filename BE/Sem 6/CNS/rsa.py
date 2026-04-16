import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_numbers():
    p, q = 0, 0
    while q ==0 or p == 0:
        num = random.randint(1, 100)
        if is_prime(num):
            if p == 0:
                p = num
            else:
                q = num
    return p, q

def calc_e(phi):
    e = random.randint(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi)
    return e

def calc_d(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

def encrypt(message, public_key):
    n, e = public_key
    return (message ** e) % n

def decrypt(encrypted, private_key):
    n, d = private_key
    return (encrypted ** d) % n


def main():
    p,q = generate_prime_numbers()
    print("Generated prime numbers: ", p, q)
    n = p * q
    print("Generated n: ", n)
    eufn = (p - 1) * (q - 1)
    print("Generated eufn: ", eufn)
    e = calc_e(eufn)
    print("Generated e: ", e)
    d = calc_d(e, eufn)
    print("Generated d: ", d)
    public_key = (n, e)
    private_key = (n, d)

    print("Public key: ", public_key)
    print("Private key: ", private_key)

    message = int(input("Enter a message to encrypt (integer): "))
    encrypted = encrypt(message, public_key)
    decrypted = decrypt(encrypted, private_key)
    print("Encrypted message: ", encrypted)
    print("Decrypted message: ", decrypted)

main()