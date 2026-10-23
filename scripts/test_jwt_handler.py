

from app.jwt_handler import create_access_token, verify_access_token

token = create_access_token(
    user_id=3,
    tenant_id=1,
    role="intern",
)

print("Token created successfully.")

payload = verify_access_token(token)

if payload is not None:
    print("Valid token: True")
    print("User ID:", payload["sub"])
    print("Tenant ID:", payload["tenant_id"])
    print("Role:", payload["role"])
else:
    print("Valid token: False")

invalid_payload = verify_access_token("this.is.not.a.valid.token")
print("Invalid token rejected:", invalid_payload is None)

