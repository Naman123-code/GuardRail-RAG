
from app.schemas import UserRegister

user = UserRegister(
    email="alice@example.com",
    password="StrongPass123!",
    tenant_id=1,
)

print(user)
print("Schema validation successful!")
