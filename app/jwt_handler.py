
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


from jwt.exceptions import InvalidTokenError


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"


from datetime import datetime, timedelta, timezone


def create_access_token(user_id: int, tenant_id: int, role: str):
    payload = {
        "sub": str(user_id),
        "tenant_id": tenant_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        return payload
    except InvalidTokenError:
        return None

