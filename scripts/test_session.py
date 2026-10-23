
from sqlalchemy import text

from app.db_session import SessionLocal

with SessionLocal() as session:
    result = session.execute(text("SELECT 1"))
    print(result.scalar())

print("SQLAlchemy session successful!")
