#!/bin/bash

# SupplySense Backend Startup Script

echo "🚀 Starting SupplySense Backend..."

# Move to backend directory
cd backend || exit

echo "📦 Installing dependencies..."
pip3 install -q -r requirements.txt

echo "🗄️ Initializing database..."
python3 -c "from database import init_db; init_db(); print('✓ Database ready')"

echo "🌱 Seeding test data..."
python3 -c "
from database import SessionLocal, init_db
from seed_data import seed_all
init_db()
db = SessionLocal()
seed_all(db)
"

echo "✅ Setup complete!"
echo "📡 Starting API server..."
python3 main.py
