

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db_session import SessionLocal
from app.models import User, Tenant
from app.schemas import UserRegister, UserLogin, AskQuestion
from app.security import hash_password, verify_password
from app.jwt_handler import create_access_token, verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.rag_service import ask_question




app = FastAPI(
    title="GuardRail-RAG",
    description="Permission-aware, multi-tenant RAG API",
    version="0.1.0",
)

oauth2_scheme = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    token = credentials.credentials
    payload = verify_access_token(token)  

    if payload is None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

def check_tenant_access(
    current_user: dict,
    resource_tenant_id: int,
):
    if current_user["tenant_id"] != resource_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: different tenant",
        )


def check_admin_access(current_user: dict):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )



def get_db():
    with SessionLocal() as session:
        yield session


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "GuardRail-RAG",
    }

@app.get("/protected")
def protected_route(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "You accessed a protected endpoint!",
        "user": current_user,
    }


@app.get("/tenant-check/{resource_tenant_id}")
def tenant_check(
    resource_tenant_id: int,
    current_user: dict = Depends(get_current_user),
):
    check_tenant_access(current_user, resource_tenant_id)

    return {"message": "Tenant access granted"}

@app.get("/admin-only")
def admin_only(
    current_user: dict = Depends(get_current_user),
):
    check_admin_access(current_user)

    return {"message": "Welcome, admin!"}

@app.get("/me")
def get_my_identity(
    current_user: dict = Depends(get_current_user),
):
    return {
        "user_id": current_user["sub"],
        "tenant_id": current_user["tenant_id"],
        "role": current_user["role"],
    }


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    tenant = db.get(Tenant, user_data.tenant_id)

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    user = User(
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
        role="intern",
        tenant_id=user_data.tenant_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role,
    }


@app.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    password_is_valid = verify_password(
        user_data.password,
        user.password_hash,
    )

    

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
    user_id=user.id,
    tenant_id=user.tenant_id,
    role=user.role,
)

    return {
    "message": "Login successful",
    "access_token": access_token,
    "token_type": "bearer",
}


@app.post("/ask")
def ask_rag_question(
    request: AskQuestion,
    current_user: dict = Depends(get_current_user),
):
    print("DEBUG 1: /ask endpoint reached", flush=True)

    answer = ask_question(
        question=request.question,
        tenant_id=int(current_user["tenant_id"]),
        role=current_user["role"],
    )

    print("DEBUG 2: RAG answer generated", flush=True)

    return {"question": request.question, "answer": answer}

