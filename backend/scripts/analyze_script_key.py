with open('e:/kriyora/model_try/backend/tmp_fix_creds.py', 'r') as f:
    content = f.read()

import re
match = re.search(r'private_key = """(.*?)"""', content, re.DOTALL)
if match:
    key = match.group(1).strip()
    print(f"Key length: {len(key)}")
    print(f"Starts with: {repr(key[:100])}")
    print(f"Ends with: {repr(key[-100:])}")
    
    # Check for literal \n
    if "\\n" in key:
        print("Literal \\n found!")
    else:
        print("No literal \\n found.")
else:
    print("Private key not found in script.")
