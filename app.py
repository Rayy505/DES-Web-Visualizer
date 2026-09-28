from flask import Flask, render_template, request, jsonify
import re
import crypto_engine

app = Flask(__name__)

# --- 1. VALIDATION HELPERS ---
def is_valid_hex(s):
    """Check if string contains only valid hex characters"""
    return bool(re.match(r'^[0-9a-fA-F]+$', s))

def validate_des_input(text, key, is_encrypting=True):
    """Handles Requirement 4: Input Validation"""
    if not text:
        return "❌ Error: Text field cannot be empty."
    if not key:
        return "❌ Error: Key field cannot be empty."
    if len(key) != 16:
        return f"❌ Error: Key must be exactly 16 hex characters (You entered {len(key)})."
    if not is_valid_hex(key):
        return "❌ Error: Key contains invalid characters (Only 0-9 and A-F allowed)."
    
    # If decrypting, ciphertext must also be valid hex
    if not is_encrypting and not is_valid_hex(text):
         return "❌ Error: Ciphertext must be hexadecimal."
         
    return None # None means validation passed

# --- 2. SERVING THE FRONTEND ---
@app.route('/')
def index():
    # This serves templates/index.html to the browser
    return render_template('index.html')

# --- 3. API ENDPOINTS ---
@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext', '').strip()
    key = data.get('key', '').strip()

    # Run Validation
    error_msg = validate_des_input(plaintext, key, is_encrypting=True)
    if error_msg:
        return jsonify({"error": error_msg}), 400

    # Hand off to Crypto Dev 1
    ciphertext = crypto_engine.des_encrypt(plaintext, key)
    
    return jsonify({
        "ciphertext": ciphertext,
        "key_order": "K1 -> K2 -> K3 -> ... -> K16" # Requirement 4
    })

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext', '').strip()
    key = data.get('key', '').strip()

    # Run Validation
    error_msg = validate_des_input(ciphertext, key, is_encrypting=False)
    if error_msg:
        return jsonify({"error": error_msg}), 400

    # Hand off to Crypto Dev 1
    plaintext = crypto_engine.des_decrypt(ciphertext, key)
    
    return jsonify({
        "plaintext": plaintext,
        "key_order": "K16 -> K15 -> K14 -> ... -> K1" # Requirement 4
    })

@app.route('/api/key-schedule', methods=['POST'])
def api_key_schedule():
    data = request.get_json()
    key = data.get('key', '').strip()

    if len(key) != 16 or not is_valid_hex(key):
        return jsonify({"error": "❌ Error: Invalid key format."}), 400

    # Hand off to Crypto Dev 2
    schedule_data = crypto_engine.get_key_schedule(key)
    
    return jsonify(schedule_data)

@app.route('/api/security-calc', methods=['POST'])
def api_security():
    data = request.get_json()
    speed = data.get('keys_per_second')
    
    if not str(speed).isdigit() or int(speed) <= 0:
        return jsonify({"error": "❌ Error: Please enter a valid number."}), 400

    # Hand off to Crypto Dev 3
    result = crypto_engine.calculate_brute_force(int(speed))
    
    return jsonify({"time_to_crack": result})

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=5000)