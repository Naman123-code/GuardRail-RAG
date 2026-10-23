from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError 

hasher = PasswordHasher()

password = "MyDemoPassword123!"

# Convert the password into a secure hash
password_hash = hasher.hash(password)

print("Stored hash:", password_hash)

# Verify the correct password
print("Correct password:", hasher.verify(password_hash, password)) 

try:
    hasher.verify(password_hash, "WrongPassword123!")
    print("Wrong password accepted")
except VerifyMismatchError:
    print("Wrong password rejected")