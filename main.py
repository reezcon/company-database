from fastapi import FastAPI 
from engine.engine import Base, get_connection

from user.apis import router as user_router
from roles.apis import router as roles_router
from camera.apis import router as camera_router
from department.apis import router as department_router
from userCamera.apis import router as userCamera_router

Base.metadata.create_all(bind=get_connection())

app = FastAPI(title="Company API")

app.include_router(user_router)
app.include_router(roles_router)
app.include_router(camera_router)
app.include_router(department_router)
app.include_router(userCamera_router)

@app.get("/")
async def root():
    return "Welcome"    