from security import hash_password, verify_password

password = "1234"

hashed = hash_password(password)

print("Hash:", hashed)

print(
    "Correct Password:",
    verify_password("1234", hashed)
)

print(
    "Wrong Password:",
    verify_password("9999", hashed)
)