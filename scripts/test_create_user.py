
from app.db_session import SessionLocal
from app.models import User

with SessionLocal() as session:
    user = User(
        email="alice@example.com",
        password_hash="demo_hash_for_practice_only",
        role="intern",
        tenant_id=1,
    )

    session.add(user)
    session.commit()

    print("User saved successfully!")
