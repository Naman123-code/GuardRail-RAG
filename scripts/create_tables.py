from app.database import engine
from app.models import Base, Tenant

Base.metadata.create_all(engine)

print("Tables created successfully!") 