import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings, FRONTEND_DIR
from app.database import engine, get_db, Base
from app.models.user import AdminUser
from app.auth import hash_password, verify_password

# Initialize database tables (MySQL or SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,   # Pure traditional web application (no API docs)
    redoc_url=None
)

# Mount static assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

templates = Jinja2Templates(directory=str(FRONTEND_DIR))

def seed_initial_admin():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        if not db.query(AdminUser).first():
            default_admin = AdminUser(
                full_name="Jamuna Rajbanshi",
                email="admin@salestrack.ai",
                password_hash=hash_password("admin123"),
                role="Super Admin"
            )
            db.add(default_admin)
            db.commit()
            print("[AUTH] Initial default admin seeded: admin@salestrack.ai / admin123")
    except Exception as e:
        print("[AUTH] Seed error:", e)
    finally:
        db.close()

seed_initial_admin()

def get_current_user(request: Request, db: Session) -> AdminUser | None:
    """Retrieves authenticated admin from session cookie."""
    user_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not user_id:
        return None
    try:
        return db.query(AdminUser).filter(AdminUser.id == int(user_id)).first()
    except (ValueError, TypeError):
        return None

# ==============================================================================
# Traditional Web Routes (HTML Forms & Server-Side Rendering - No API)
# ==============================================================================

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    
    success_msg = "Account created successfully! Please sign in." if request.query_params.get("registered") == "1" else None
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None, "success": success_msg}
    )

@app.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.strip().lower()
    user = db.query(AdminUser).filter(AdminUser.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password. Please try again.", "success": None},
            status_code=400
        )

    # Authentication successful -> Set session cookie and redirect to protected dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=str(user.id),
        httponly=True,
        max_age=86400 * 7  # 7 days
    )
    return response

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"error": None, "success": None}
    )

@app.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    full_name = full_name.strip()
    email = email.strip().lower()

    # Form Validations
    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Passwords do not match. Please re-enter.", "success": None},
            status_code=400
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Password must be at least 6 characters long.", "success": None},
            status_code=400
        )

    # Check if admin email already exists in database
    existing_user = db.query(AdminUser).filter(AdminUser.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "An administrator with this email already exists.", "success": None},
            status_code=400
        )

    # Hash password and persist in database
    hashed_pw = hash_password(password)
    new_admin = AdminUser(
        full_name=full_name,
        email=email,
        password_hash=hashed_pw,
        role="Admin"
    )
    db.add(new_admin)
    db.commit()

    # Redirect to login with success indicator
    return RedirectResponse(url="/login?registered=1", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def protected_dashboard(request: Request, db: Session = Depends(get_db)):
    """Protected Admin Dashboard — only accessible when authenticated."""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user}
    )

@app.get("/logout")
def logout():
    """Logs out admin and destroys session cookie."""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key=settings.SESSION_COOKIE_NAME)
    return response
