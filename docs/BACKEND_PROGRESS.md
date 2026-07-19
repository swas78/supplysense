# SupplySense Backend - Build Progress

## ✅ COMPLETED (Phase 0-1)

### Phase 0: Shared Setup
- [x] FastAPI skeleton created (`main.py`)
- [x] Database configuration (`database.py`)
- [x] CORS middleware configured
- [x] Project structure established

### Phase 1a: Database Schema
All 14 tables created with relationships:
- [x] `suppliers` - supplier data + reliability metrics
- [x] `warehouses` - warehouse locations
- [x] `products` - product/SKU catalog
- [x] `inventory_snapshots` - current stock per product/warehouse
- [x] `demand_history` - historical daily demand
- [x] `purchase_orders` - supplier orders with tracking
- [x] `shipments` - shipment tracking with ETAs
- [x] `shipment_events` - shipment status updates
- [x] `external_signals` - weather, news, promo data
- [x] `forecasts` - prediction engine outputs
- [x] `anomalies` - detected demand anomalies
- [x] `customer_orders` - pending customer orders
- [x] `chat_logs` - chat conversation history
- [x] `allocation_decisions` - inventory allocation output
- [x] `procurement_suggestions` - procurement recommendations
- [x] `recommendations` - action recommendations
- [x] `dealer_messages` - LLM-generated supplier messages

### Phase 1b: Seeding Script
Comprehensive seed_data.py generates:
- [x] 5 suppliers with varied reliability profiles
- [x] 3 warehouses in different locations
- [x] 8 products with different categories
- [x] Current inventory snapshots with intentional low/overstock items
- [x] 90 days of synthetic demand history
  - Includes seasonal patterns
  - Includes promotional spikes
  - Realistic variance per product/warehouse
- [x] 12 historical purchase orders (mix of on-time/late)
- [x] 10 shipments with realistic tracking
- [x] 1 deliberately delayed in-transit shipment (for demo trigger)
- [x] 13 pending customer orders (3+ on the low-stock product for cascade demo)
- [x] External signals (weather, promo data)

---

## ✅ COMPLETED (Phase 2: Prediction Engine)

### Phase 2a: Inventory Monitoring
**Endpoint: `GET /api/inventory`**
- [x] Returns all SKUs with current stock per warehouse
- [x] Includes reorder point + safety stock levels
- [x] Color-coded stock status (SAFE, LOW, CRITICAL)

### Phase 2b: Shortage Prediction (Core ML)
**Endpoint: `GET /api/inventory/{sku_id}/forecast`**
- [x] Days-to-stockout calculation
  - Formula: `current_stock / rolling_avg_daily_demand(30 days)`
- [x] Confidence score based on demand variance
  - `confidence = 1.0 - (stdev / mean)`
  - Lower variance = higher confidence
- [x] Risk level classification (HIGH/MEDIUM/LOW)
  - HIGH: < 7 days
  - MEDIUM: 7-14 days
  - LOW: > 14 days
- [x] Reasoning text explaining forecast
- [x] Per-warehouse forecasts

### Phase 2c: Overstock Detection
**Endpoint: `GET /api/inventory/overstock`**
- [x] Identifies products with excess stock
- [x] Calculates demand-justified stock levels
- [x] Flags items where stock > 1.5x demand-justified
- [x] Estimates working capital tied up
- [x] Provides reorder reduction recommendations

### Phase 2d: Anomaly Detection
**Endpoint: `GET /api/anomalies`**
- [x] Z-score based anomaly detection
- [x] Detects both spikes (z > 2) and drops (z < -2)
- [x] Likely cause attribution:
  - Promotion flag
  - Weather/external events
  - Unknown
- [x] Severity classification (HIGH/MEDIUM)
- [x] Last 7 days scanned for recent anomalies
- [x] Sorted by z-score magnitude

### Phase 2e: Shipment Delay Detection
**Endpoint: `GET /api/shipments/delays`**
- [x] Lists all shipments with current_eta > original_eta
- [x] Includes supplier name, product, quantity
- [x] Shows original vs. current ETA
- [x] Calculates delay_days
- [x] Links to destination warehouse

### Phase 2f: Cascade Impact Simulator
**Endpoint: `GET /api/shipments/{id}/impact`**
- [x] Traces delay → affected products → affected warehouses
- [x] Calculates how long current stock will last
- [x] Finds at-risk pending customer orders
- [x] Calculates total at-risk order value (₹)
- [x] Generates human-readable summary
- [x] Returns structured cascade chain

**Response structure:**
```json
{
  "shipment_id": "...",
  "cascade": {
    "affected_products": [...],
    "affected_warehouses": [...],
    "at_risk_orders": [...],
    "total_at_risk_order_value": 87500,
    "summary": "This 4-day delay puts 2 pending orders at risk..."
  }
}
```

### Phase 2g: Demo Trigger Endpoint
**Endpoint: `POST /api/simulate/trigger-delay?shipment_id=xyz&delay_days=4`**
- [x] Manually triggers shipment delay for live demo
- [x] Updates shipment status to "delayed"
- [x] Recalculates cascade impact instantly
- [x] Returns immediate cascade response
- [x] Can be called with or without shipment_id (defaults to first in-transit)

---

## ✅ COMPLETED (Phase 3-4)

### Phase 3: Demo Trigger
- [x] `/api/simulate/trigger-delay` endpoint ready for live demo

### Phase 4: Weather API Integration (Stub)
- [x] `external_signals` table created
- [x] Seed data includes weather/promo signals
- [x] Ready for OpenWeatherMap API integration
- [x] Anomaly detector checks external signals for cause attribution

---

## 🔄 IN PROGRESS / TODO

### Phase 5: Chat/NLQ Agent
**Endpoint: `POST /api/chat?question={user_question}`**

**Current Status:**
- [x] Route created with placeholder
- [x] ChatLog model for persistence
- [x] Chat history endpoint (`GET /api/chat-history`)
- [ ] Full Claude/OpenAI integration with tool-calling
- [ ] Tool definitions for LLM:
  - [ ] `get_inventory_status(sku_id)`
  - [ ] `get_shipment_delays()`
  - [ ] `get_anomalies()`
  - [ ] `get_supplier_score(supplier_id)` (calls Tanishka's endpoint)
  - [ ] `get_recommendations()` (calls Tanishka's endpoint)
  - [ ] `get_cascade_impact(shipment_id)`
- [ ] LLM prompt engineering for reasoning chain
- [ ] Reasoning trace generation
- [ ] Response streaming (optional)

**Example questions the agent should handle:**
1. "What's causing today's biggest disruption?"
2. "Which products will stock out in the next 7 days?"
3. "How many customer orders are at risk right now?"

### Phase 6: Dashboard Aggregation
**Endpoint: `GET /api/dashboard/overview`**

**Current Status:**
- [x] Basic implementation created
- [ ] 7-day lookahead view as default
- [ ] Today's snapshot as secondary
- [ ] Integration with recommendations (from Tanishka's track)
- [ ] "Active disruption" card count
- [ ] Risk metrics aggregation

---

## 📊 TESTING & VERIFICATION NEEDED

### Backend Endpoint Testing (to do before frontend)
- [ ] Test `/api/inventory` - returns all SKUs
- [ ] Test `/api/inventory/{sku_id}/forecast` - shortage prediction works
- [ ] Test `/api/inventory/overstock` - overstock detection works
- [ ] Test `/api/anomalies` - detects seeded demand spikes
- [ ] Test `/api/shipments/delays` - returns delayed shipments
- [ ] Test `/api/shipments/{id}/impact` - cascade impact accurate
- [ ] Test `/api/simulate/trigger-delay` - triggers demo scenario
- [ ] Test `/api/seed` - database seeding endpoint
- [ ] Test `/api/chat` - placeholder response
- [ ] Test `/api/dashboard/overview` - aggregation works

### Seeded Data Verification
- [ ] Widget A (low stock) in Warehouse 2: 80 units (should predict ~6 days to stockout)
- [ ] Component Y (overstock) in Warehouse 1: 1500 units (should be flagged as overstock)
- [ ] 90-day demand history includes seasonal spike (days 60-75)
- [ ] 90-day demand history includes promo spike for Widget A (days 20-25)
- [ ] In-transit shipment ready for demo trigger
- [ ] 3 pending orders on Widget A in Warehouse 2 (for cascade demo)

---

## 🚀 HOW TO RUN

### Quick Start
```bash
bash run.sh
```

This will:
1. Install dependencies from requirements.txt
2. Initialize database
3. Seed test data
4. Start FastAPI server on http://localhost:8000

### Manual Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from database import init_db; init_db()"

# Seed data
python -c "from database import SessionLocal; from seed_data import seed_all; seed_all(SessionLocal())"

# Start server
python main.py
```

### Access API
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Seed endpoint: POST http://localhost:8000/api/seed

---

## 📝 NEXT STEPS (Swastik's remaining work)

### Immediate (Phase 5)
1. Implement full Chat/NLQ agent with Claude/OpenAI
   - Set up anthropic SDK
   - Define tool functions
   - Wire tools to endpoints
   - Test reasoning chain

2. Test all prediction endpoints thoroughly
   - Verify forecast accuracy
   - Check confidence scores
   - Validate cascade impact calculations

3. Prepare Postman collection with example requests

### Before Frontend Integration
1. Ensure all 8 Swastik endpoints return proper data
2. Create API response documentation
3. Test endpoint responses with sample queries
4. Stub Tanishka's endpoints if her track isn't ready

---

## 📦 PROJECT STRUCTURE

```
supplysense/
├── main.py                 # FastAPI app entrypoint
├── models.py              # SQLAlchemy models (14 tables)
├── database.py            # DB config + session mgmt
├── seed_data.py           # Comprehensive seeding script
├── routes/
│   ├── __init__.py
│   ├── inventory.py       # Phases 2a-2c endpoints
│   ├── shipments.py       # Phases 2d-2g + anomalies
│   ├── chat.py            # Phase 5 (chat agent)
│   ├── dashboard.py       # Phase 6 (dashboard aggregation)
│   └── seed.py            # Seeding endpoint
├── requirements.txt       # Python dependencies
├── run.sh                 # Startup script
└── BACKEND_PROGRESS.md    # This file
```

---

## ⚡ PERFORMANCE NOTES

- SQLite is used for development (can switch to PostgreSQL for prod)
- All queries are reasonably optimized with indexes on key columns
- Forecast calculation uses last 30 days of data (tunable)
- Anomaly detection uses z-score threshold of 2.0 (tunable)
- Chat agent will support streaming responses (not implemented yet)

---

## 🎯 SUCCESS CRITERIA (Current Status)

- [x] All 13 Swastik-owned tables created
- [x] Seeding script generates realistic test data
- [x] All Phase 2 prediction endpoints implemented
- [x] Demo trigger endpoint ready
- [ ] Chat agent fully integrated with Claude
- [ ] All endpoints verified to work with real data
- [ ] Postman collection created
- [ ] Frontend can integrate with these endpoints

---

**Last Updated:** Phase 4 complete, Phase 5-6 in progress
**Next Milestone:** Full chat agent + frontend integration testing
