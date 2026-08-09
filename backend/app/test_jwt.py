from app.utils.security import create_access_token
from app.core.security import verify_token


token = create_access_token("123")

print("TOKEN:")
print(token)

print("\nDECODED TOKEN:")
print(verify_token(token))