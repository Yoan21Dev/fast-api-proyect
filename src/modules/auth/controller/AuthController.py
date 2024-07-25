from fastapi import APIRouter ,requests ,Request
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.modules.auth.service.AuthService import authenticate_user,get_users_db,create_token
from datetime import timedelta
from fastapi.responses import HTMLResponse, RedirectResponse
authRouter = APIRouter()

@authRouter.post("/auth-login")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    
    users_db = await get_users_db()
    user = authenticate_user(users_db, form_data.username, form_data.password)
    
    access_token_expire = timedelta(minutes=30)
    
    access_token_jwt = create_token({"sub":user.username},access_token_expire)
    
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

# Ruta de autenticación
@authRouter.post("/auth-login-view")
async def loginView(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    users_db = await get_users_db()
    user = authenticate_user(users_db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expire = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expire)
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=access_token_jwt, httponly=True)
    
    return response

