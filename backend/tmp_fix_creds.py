import json

# Correctly formatted private key with actual newlines
private_key = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcJ1GEHDWNlQuC\n"
    "LYqBaGzwzJjWAX8LNut68TQIWZIBEakFuxKqovzGbcjgGq0BCKCAVwk11l67C7Hx\n"
    "tS2f9FqG6ksDaflOfmziuCvgC21y6MYdx+D6nYqGww4eb2uYXeQDimyKSdhj2bgF\n"
    "+d9cCyMTCXGU4KnvybybRRQNEjQ1dZvj8ansBxKz0Oc8pmiYYVfAIzRunRiGx442\n"
    "e70rTu6gxtw+lbSyU4xwIkI+JKjssN2BsL8k/jdJCNpfzUA2GKsL4DLuB3jGCbN5\n"
    "+L6cV4X1S1yPCkjj0Zm3ZxcM7ilgEl+awKOAHvexDHdt7Z4lu+N4XSFhYw9kT8br\n"
    "scR2gUObAgMBAAECggEAG3gxzPt9bc5sbTB5g8Qf3maTphWcYIMtxrKp/LtluF8X\n"
    "vptPrPLr+hELa3W9+Hm3F8xvCG9YdUZJobsq7OEfGo50EFenaoqOfjY0uJ6JvY4b\n"
    "NO69El2Yl1AR8ZeSzqQzJdiedR2EXpEf9mmYhnJCohwfi/qsZDsWdC6eXd3Tnd0f\n"
    "iaggEnPcv3hWDCW2G3KQodvkHF+GoQuiNNkmEoAU8sNmC+YWOtNCVeJmzV2xwrGW\n"
    "+Qw6nJOBt5ep5pdZKEmbUhTaiYnYqhFynZQIawNKBq6ZzcPKQV3jAj/kSN+0j3Ae\n"
    "ndEYc9+7FH23Koe/WIChb/nqPQRQX+kFJ3mLCmtuFQQKBgQD7zV8ngBiJ+j6I3Eq0\n"
    "gkAJjDaadleW+nF9kubd7C3rycB0JR2Gn72l09ufMo3+fuxLRkUTjbxUFko37ioh\n"
    "4TYZ4KEB9CZaip5X1nlagCtXawB8iN2/EY6PypT88tPhMCT8Ymbzm8oNVQ4GTFNY\n"
    "Xo4Ie3Dlh/IoTSxB0DiwNBrIWQKBgQDf0uDYfsJa3zr01sk+7H4tdtxtdxffSA9W\n"
    "NPH9OlhAkePx04xmT7tZJ6CcH5ved9kOSdiq8ISEuVFEXyX8UuDeMQse08Ho+Qay\n"
    "szFlueF5UiFz0ae3c0EF/0NZu88k8Us/GfyQmvVgy1oqribwasT0XIOeCVa9UTQB\n"
    "AYgolBrtEwKBgGMvT3cIvyHCf9V7KLYXxE++ele3m+LtvbygG+54tNH3A6b8Y7f+\n"
    "vj5OyGjaChKgPkWcZWNBZlic+xky6Ee2JZBl6iYR3PW3Oo4Q/nZGnEvv6x4i723u\n"
    "5YAAZVWJ9Snzw+3iePkmeZ1sznxunjnl7P6sWRkgxqNXWsKF2X6W16HpAoGBAMYa\n"
    "ifRUzYVMy4vlh53wCAYJjDQ/EpwH1btBhWXSfEY6Wnyx9zSfIX1Zu6gzuewAO9eP\n"
    "uPwjgcdPlwRjCuX4HRvMYMFaP+kKcMk+HVyiV1TgQseWK1IN6uF5+4yy1DcocqdZ\n"
    "QthirwiLNDVOixyEA+sc70mzjlhmRRcW2gLAg8yNAoGAcboAt0e3WUrPDcBKsquZ\n"
    "PVupdZqeAWgcLxh5r6UdvNjy1h8yNcnVch+TUSZIoHcs8Wc3ByNE7hitJaBsoNul\n"
    "maLVHHmQIAoWjXFlZlEjPyV+K8V13hEu9xtYHpQCXol5v8Hjk7QBrYyxAlVxsxSm\n"
    "ndEJXZgce+EA7s9Tlj/XbUEE=\n"
    "-----END PRIVATE KEY-----\n"
)

data = {
  "type": "service_account",
  "project_id": "kriyora-epicverse",
  "private_key_id": "cb5bda06e7a3ae71dfa14a5218a164c9b17e56b8",
  "private_key": private_key,
  "client_email": "kriyora-epicverse@kriyora-epicverse.iam.gserviceaccount.com",
  "client_id": "110596946541273524611",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kriyora-epicverse%40kriyora-epicverse.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

with open('google-credentials.json', 'w') as f:
    json.dump(data, f, indent=2)

print("SUCCESS: Full private key restored.")
