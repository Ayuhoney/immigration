from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from app.routes import auth, upload, user_info

# Create FastAPI instance
app = FastAPI(
    title="Immigration Backend API",
    description="API for immigration services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(user_info.router)

@app.get("/")
async def root():
    return {"message": "Immigration Backend API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Service is running"}
