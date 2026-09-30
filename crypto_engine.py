def des_encrypt(plaintext, key):
    '''
    Kemal's workspace
    Expected Input: string (plaintext), 16-char hex string (key)
    Expected Output: 16-char hex string (ciphertext)
    '''
    # TODO: implement DES encryption library here 
    return "aaaaa" # (dummy output for now)

def des_decrypt(ciphertext, key):
    '''
    Kemal's workspace
    Expected Input: 16-char hex string (ciphertext), 16-char hex string (key)
    Expected Output: string (plaintext)
    '''
    # TODO: implement DES decryption library here
    return "bbbbbb" # (dummy output for now)

# ===== KEY SCHEDULE (Pana) START =====
# DES key schedule reference implementation (FIPS 46-3 tables).
_KS_PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4,
]
_KS_PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32,
]
_KS_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def _ks_permute(bits, table):
    return "".join(bits[i - 1] for i in table)


def _ks_rotl(bits, n):
    return bits[n:] + bits[:n]


def get_key_schedule(key):
    original_64 = format(int(key, 16), "064b")
    pc_1 = _ks_permute(original_64, _KS_PC1)

    c, d = [pc_1[:28]], [pc_1[28:]]
    round_keys = []
    for r in range(16):
        c.append(_ks_rotl(c[r], _KS_SHIFTS[r]))
        d.append(_ks_rotl(d[r], _KS_SHIFTS[r]))
        round_keys.append(_ks_permute(c[r + 1] + d[r + 1], _KS_PC2))

    return {
        "original_64": original_64,
        "pc_1": pc_1,
        # Combine C0 and D0 into a single readable string for the UI
        "c0_d0": f"{c[0]}  (C0)\n{d[0]}  (D0)", 
        "c": c,
        "d": d,
        "shifts": list(_KS_SHIFTS),
        "round_keys": [format(int(k, 2), "012X") for k in round_keys], 
        "round_keys_binary": round_keys, 
    }
# ===== KEY SCHEDULE (Pana) END =====

def calculate_brute_force(keys_per_second):
    '''
    Abby's workspace (Security Feature)
    Expected Input: integer (keys per second guessed by attacker)
    Expected Output: string (time to crack)
    '''
    # TODO: Implement 2^56 math calculation here
    return "10 minutes" # (dummy output for now)