
from app.security import hash_password, verify_password

password = "MyStrongPassword123!"

# Generate a password hash
hashed_password = hash_password(password)
print("Password hashed successfully!")

# Verify the correct password
print("Correct password:", verify_password(password, hashed_password))

# Verify an incorrect password
print("Wrong password:", verify_password("WrongPassword123!", hashed_password))
