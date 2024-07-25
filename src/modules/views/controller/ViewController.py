from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import FastAPI, Request, Form, Depends, HTTPException,APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from src.modules.user.service.UserService import UserService
from src.modules.user.scheme.UserScheme import CreateUser

viewRouter = APIRouter()
# Configurar Jinja2 para manejar las plantillas HTML
templates = Jinja2Templates(directory="src\\modules\\views\\templates")
userService = UserService()
# Ruta para la vista web
@viewRouter.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = {"request": request, "message": "Hola desde FastAPI!"}
    
    return templates.TemplateResponse("index.html", context)



@viewRouter.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@viewRouter.post("/register")
async def register_user(request: Request, username: str = Form(...), confirm_password: str = Form(...), password: str = Form(...), full_name: str = Form(...), email: str = Form(...)):
    
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
    
    user_data = CreateUser(
        username=username,
        password=password,
        full_name=full_name,
        email=email,
        disabled=False
    )
    
    # Debugging
    print("User data:", user_data)
    
    user = await userService.create_user(user_data)
    
    # Debugging
    print("Created user:", user)
    
    return RedirectResponse(url="/", status_code=302)


# Ruta de dashboard (nueva plantilla)
@viewRouter.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    token: Optional[str] = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/", status_code=302)
    
    context = {"request": request, "token": token}
    return templates.TemplateResponse("dashboard.html", context)
