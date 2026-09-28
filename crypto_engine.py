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

def get_key_schedule(key):
    '''
    Pana's workspace (visualizer)
    Expected Input: 16-char hex string (key)
    Expected Output: Dictionary containing all intermediate steps
    '''
    # TODO: Implement key schedule step extraction here
    return {
        "original_64": "...",
        "pc_1": "...",
        "c0_d0": "...",
        "round_keys": ["K1...", "K2...", "...K16"]
    }

def calculate_brute_force(keys_per_second):
    '''
    Abby's workspace (Security Feature)
    Expected Input: integer (keys per second guessed by attacker)
    Expected Output: string (time to crack)
    '''
    # TODO: Implement 2^56 math calculation here
    return "10 minutes" # (dummy output for now)