with open('e:/kriyora/model_try/backend/tmp_fix_creds.py', 'r') as f:
    content = f.read()

import re
match = re.search(r'private_key = """(.*?)"""', content, re.DOTALL)
if match:
    key = match.group(1).strip()
    # Remove headers
    content = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    lines = content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) != 64 and i < len(lines)-1:
            print(f"Line {i+1} has length {len(line)}: {repr(line)}")
    print(f"Last line (Line {len(lines)}) has length {len(lines[-1].strip())}: {repr(lines[-1].strip())}")
else:
    print("Not found")
