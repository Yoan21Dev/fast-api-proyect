from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import FastAPI, Request, Form, Depends, HTTPException,APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from src.modules.cars.scheme.SchemeCar import CarCreate
from src.modules.user.service.UserService import UserService
from src.modules.user.scheme.UserScheme import CreateUser,User
from src.modules.cars.service.CarService import CarService
from src.database.models import User as UserMaster
from src.modules.auth.service.AuthService import get_user_current, get_user_disabled_current

viewRouter = APIRouter()
# Configurar Jinja2 para manejar las plantillas HTML
templates = Jinja2Templates(directory="src\\modules\\views\\templates")
userService = UserService()
carService = CarService()

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

@viewRouter.post('/create-car')
async def create_car(request: Request,
    name: str = Form(...),
    model: str = Form(...),
    mark: str = Form(...),
    year: int = Form(...),
    price: float = Form(...),
    color: str = Form(...),
    state: str = Form(...),
    user: User = Depends(get_user_current)
    ):
    
    car_data = CarCreate(
        name=name,
        model=model,
        mark=mark,
        year=year,
        price=price,
        color=color,
        state=state,
        created_by_user_id=user.id
        )
    await carService.create_car(car_data)


# Ruta de dashboard (nueva plantilla)
@viewRouter.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    
    token: Optional[str] = request.cookies.get("access_token")

    if not token:
        return RedirectResponse(url="/", status_code=302)
    cars = await carService.get_all_cars()
    context = {"request": request, "token": token, 'cars': cars}
    return templates.TemplateResponse("dashboard.html", context)

@viewRouter.get("/user-perfil", response_class=HTMLResponse)
async def perfil(request:Request,  user: User = Depends(get_user_current)):
    
    return  templates.TemplateResponse("perfil.html", {"request": request, "user": user})

@viewRouter.post("/buy-car")
async def buy_car(request: Request, user: UserMaster = Depends(get_user_current)):
    data = await request.json()
    car_id = data.get("car_id")
    
    if not car_id:
        raise HTTPException(status_code=400, detail="Car ID is required")
    
    success = await carService.buy_car(user_id=user.id, car_id=int (car_id))
    
    if success:
        return JSONResponse(content={"message": "Compra realizada con éxito"})
    else:
        raise HTTPException(status_code=500, detail="Error al realizar la compra")
