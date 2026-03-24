from cryptography.hazmat.primitives import serialization
import json

with open('e:/kriyora/model_try/backend/google-credentials.json', 'r') as f:
    data = json.load(f)

key_str = data['private_key']
print(f"Key starts with: {key_str[:50]}")
print(f"Key ends with: {key_str[-50:]}")

try:
    serialization.load_pem_private_key(key_str.encode(), password=None)
    print("SUCCESS: Key is valid PEM!")
except Exception as e:
    print(f"ERROR: {e}")
    # Let's try to add newlines every 64 chars
    header = "-----BEGIN PRIVATE KEY-----\n"
    footer = "\n-----END PRIVATE KEY-----\n"
    content = key_str.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    # Remove any existing newlines/spaces in content
    content = "".join(content.split())
    # Add newlines every 64 chars
    formatted_content = "\n".join(content[i:i+64] for i in range(0, len(content), 64))
    new_key = header + formatted_content + footer
    print("Trying formatted key...")
    try:
        serialization.load_pem_private_key(new_key.encode(), password=None)
        print("SUCCESS with formatting!")
        # If success, I should use this.
    except Exception as e2:
        print(f"STILL ERROR: {e2}")
