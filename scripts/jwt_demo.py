

import jwt

payload = {
    "sub": "user_001",
    "tenant_id": "alpha_corp",
    "role": "intern",
}

# Step 1: Create a signed token
token = jwt.encode(
    payload,
    "demo-secret-only",
    algorithm="HS256",
)

print("JWT:", token)

# Step 2: Decode and verify the token
decoded_payload = jwt.decode(
    token,
    "demo-secret-only",
    algorithms=["HS256"],
)

print("Decoded payload:", decoded_payload)
