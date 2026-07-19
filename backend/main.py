"""
SupplySense - AI Supply Chain Risk & Inventory Intelligence
Backend FastAPI Application
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from database import init_db

import asyncio
from background_agent import start_background_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("✓ Database initialized")
    
    # Start background agent
    background_task = asyncio.create_task(start_background_agent())
    
    yield
    # Shutdown
    background_task.cancel()
    print("✓ Shutting down")

app = FastAPI(
    title="SupplySense API",
    description="AI Supply Chain Risk & Inventory Intelligence",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routes import (
    inventory, shipments, dashboard, seed, suppliers,
    recommendations, allocation, procurement, executive_summary, nlq_agent
)

app.include_router(inventory.router, prefix="/api")
app.include_router(shipments.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(seed.router, prefix="/api")
app.include_router(suppliers.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(allocation.router, prefix="/api")
app.include_router(procurement.router, prefix="/api")
app.include_router(executive_summary.router, prefix="/api")
app.include_router(nlq_agent.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "SupplySense API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
