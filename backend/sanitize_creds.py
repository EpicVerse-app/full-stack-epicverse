import json

with open('e:/kriyora/model_try/backend/google-credentials.json', 'r') as f:
    data = json.load(f)

key = data['private_key']
# Remove everything except the base64
content = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
# Remove all whitespace including \n, \r, \t, etc
content = "".join(content.split())
# Rebuild with standard \n every 64 chars
formatted = "-----BEGIN PRIVATE KEY-----\n"
for i in range(0, len(content), 64):
    formatted += content[i:i+64] + "\n"
formatted += "-----END PRIVATE KEY-----\n"

data['private_key'] = formatted

with open('e:/kriyora/model_try/backend/google-credentials.json', 'w') as f:
    json.dump(data, f, indent=2)

print("SUCCESS: Credentials re-formatted to single \n newline style.")
