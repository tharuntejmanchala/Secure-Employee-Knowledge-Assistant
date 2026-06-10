# test_jwt.py

from security import create_access_token

token = create_access_token(
    {
        "email": "priya@gmail.com",
        "role": "HR"
    }
)

print(token)