"""
Test 1 — Correctness Verification
Ensures both implementations produce mathematically correct results.
"""

import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt as std_encrypt,
    decrypt as std_decrypt,
    encrypt_bytes as std_encrypt_bytes,
    decrypt_bytes as std_decrypt_bytes,
    mod_exp as std_mod_exp,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt as opt_encrypt,
    decrypt as opt_decrypt,
    encrypt_bytes as opt_encrypt_bytes,
    decrypt_bytes as opt_decrypt_bytes,
    mod_exp_sliding_window as opt_mod_exp,
    KeyCache,
)

SEP = "=" * 64
SUBSEP = "-" * 64

passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}  {detail}")
        failed += 1


def test_mod_exp_correctness():
    print(f"\n{SUBSEP}")
    print("Modular Exponentiation — correctness")
    print(SUBSEP)

    test_cases = [
        (2, 10, 1000, 24),
        (3, 13, 97, 61),
        (5, 117, 199, 50),
        (123456789, 987654321, 1000000007, 652541198),
        (2, 65537, 3233, 2790),  # small RSA-like
    ]

    for base, exp, mod, _ in test_cases:
        expected = pow(base, exp, mod)
        std = std_mod_exp(base, exp, mod)
        opt = opt_mod_exp(base, exp, mod)
        check(f"pow({base}^{exp} mod {mod}) std == pow()", std == expected, f"got {std}")
        check(f"pow({base}^{exp} mod {mod}) opt == pow()", opt == expected, f"got {opt}")


def test_large_mod_exp():
    print(f"\n{SUBSEP}")
    print("Large Modular Exponentiation (1024-bit)")
    print(SUBSEP)

    a = random.getrandbits(1024)
    b = random.getrandbits(1024)
    n = random.getrandbits(1024) | (1 << 1023) | 1
    expected = pow(a, b, n)

    std = std_mod_exp(a, b, n)
    opt = opt_mod_exp(a, b, n)
    check("1024-bit mod_exp standard", std == expected)
    check("1024-bit mod_exp optimized", opt == expected)


def test_standard_rsa_encrypt_decrypt():
    print(f"\n{SUBSEP}")
    print("Standard RSA — encrypt/decrypt integers")
    print(SUBSEP)

    priv, pub = std_gen(1024)
    for msg_val in [42, 12345, 2**128 - 1, random.getrandbits(256)]:
        ct = std_encrypt(pub, msg_val)
        pt = std_decrypt(priv, ct)
        check(f"msg={msg_val} roundtrip", pt == msg_val)


def test_optimized_rsa_encrypt_decrypt():
    print(f"\n{SUBSEP}")
    print("Optimized RSA — encrypt/decrypt integers")
    print(SUBSEP)

    priv, pub = opt_gen(1024)
    for msg_val in [42, 12345, 2**128 - 1, random.getrandbits(256)]:
        ct = opt_encrypt(pub, msg_val)
        pt = opt_decrypt(priv, ct)
        check(f"msg={msg_val} roundtrip", pt == msg_val)


def test_bytes_encrypt_decrypt():
    print(f"\n{SUBSEP}")
    print("Byte-level encrypt/decrypt with padding")
    print(SUBSEP)

    for label, gen, enc_fn, dec_fn in [
        ("Standard", std_gen, std_encrypt_bytes, std_decrypt_bytes),
        ("Optimized", opt_gen, opt_encrypt_bytes, opt_decrypt_bytes),
    ]:
        priv, pub = gen(1024)
        messages = [
            b"hello world",
            b"A" * 50,
            b"\x00\x01\x02\x03" * 20,
            os.urandom(100),
        ]
        for msg in messages:
            ct = enc_fn(pub, msg)
            pt = dec_fn(priv, ct)
            check(f"{label} bytes roundtrip (len={len(msg)})", pt == msg)


def test_key_cache():
    print(f"\n{SUBSEP}")
    print("KeyCache — reuse and regeneration")
    print(SUBSEP)

    cache = KeyCache(1024)
    priv1, pub1 = cache.get()
    priv2, pub2 = cache.get()
    check("cache returns same key", priv1["d"] == priv2["d"])

    priv3, pub3 = cache.regenerate()
    check("regenerate creates new key", priv1["d"] != priv3["d"])

    msg = random.getrandbits(512)
    ct = opt_encrypt(pub3, msg)
    pt = opt_decrypt(priv3, ct)
    check("new cached key works", pt == msg)


def test_cross_compatibility():
    print(f"\n{SUBSEP}")
    print("Cross-implementation: std encrypt, opt decrypt")
    print(SUBSEP)

    priv, pub = opt_gen(1024)
    msg = random.getrandbits(512)

    # Use standard mod_exp to encrypt, optimized to decrypt
    from standard_rsa.rsa import mod_exp
    ct = mod_exp(msg, pub["e"], pub["n"])
    pt = opt_decrypt(priv, ct)
    check("std encrypt -> opt decrypt", pt == msg)


def test_hybrid_correctness():
    print(f"\n{SUBSEP}")
    print("Hybrid RSA+AES — correctness")
    print(SUBSEP)

    for label, gen, hy_enc, hy_dec in [
        ("Standard", std_gen, None, None),   # will skip if not available
        ("Optimized", opt_gen, None, None),
    ]:
        if label == "Standard":
            from standard_rsa.rsa import hybrid_encrypt as she, hybrid_decrypt as shd
            hy_enc, hy_dec = she, shd
        else:
            from optimized_rsa.rsa import hybrid_encrypt as ohe, hybrid_decrypt as ohd
            hy_enc, hy_dec = ohe, ohd

        priv, pub = gen(1024)
        for size in [16, 64, 256, 1024]:
            data = os.urandom(size)
            envelope = hy_enc(pub, data)
            recovered = hy_dec(priv, envelope)
            check(f"{label} hybrid {size}B roundtrip", recovered == data)


def main():
    print(SEP)
    print("TEST 1 — CORRECTNESS VERIFICATION")
    print(SEP)

    test_mod_exp_correctness()
    test_large_mod_exp()
    test_standard_rsa_encrypt_decrypt()
    test_optimized_rsa_encrypt_decrypt()
    test_bytes_encrypt_decrypt()
    test_key_cache()
    test_cross_compatibility()
    test_hybrid_correctness()

    print(f"\n{SEP}")
    total = passed + failed
    print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    if failed:
        print("STATUS: SOME TESTS FAILED")
    else:
        print("STATUS: ALL TESTS PASSED")
    print(SEP)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
