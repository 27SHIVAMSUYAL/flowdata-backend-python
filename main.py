from fastapi import FastAPI
from routes.studentRoutes import router as studentRouter
from routes.adminRoutes import router as adminRouter
from routes.userRoutes import router as userRouter
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(studentRouter)
app.include_router(adminRouter)
app.include_router(userRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Students API"}
