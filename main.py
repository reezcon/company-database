from fastapi import FastAPI 

from user.apis import router as user_router
from roles.apis import router as roles_router
from camera.apis import router as camera_router
from department.apis import router as department_router

app = FastAPI(title="Company API")

app.include_router(user_router)
app.include_router(roles_router)
app.include_router(camera_router)
app.include_router(department_router)

@app.get("/")
async def root():
    return "Welcome"    