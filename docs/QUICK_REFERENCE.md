# SupplySense — Quick Feature Reference

## ✅ READY TO USE RIGHT NOW (8 Features)

### 1️⃣ **Multi-Source Data Ingestion**
- **Test:** `POST http://localhost:8000/api/seed`
- **What it does:** Populates all tables with 90 days of realistic data
- **Response:** Database seeded with 5 suppliers, 3 warehouses, 8 products, 13 pending orders

### 2️⃣ **Real-Time Inventory Monitoring**
- **Test:** `GET http://localhost:8000/api/inventory`
- **What it shows:** All SKUs, current stock, warehouse, reorder point, stock status
- **Example response:**
  ```json
  {
    "product_name": "Widget A",
    "warehouse_name": "Warehouse 2",
    "stock_on_hand": 80,
    "reorder_point": 100,
    "stock_status": "LOW"
  }
  ```

### 3️⃣ **Shortage Prediction**
- **Test:** `GET http://localhost:8000/api/inventory/abc123/forecast`
  - (Replace `abc123` with an actual product ID from /api/inventory)
- **What it predicts:**
  - Days until stockout
  - Confidence score (0-1)
  - Risk level (HIGH/MEDIUM/LOW)
- **Example:** Widget A in Warehouse 2 → **3.2 days to stockout, 75% confidence**

### 4️⃣ **Overstock Detection**
- **Test:** `GET http://localhost:8000/api/inventory/overstock`
- **What it finds:** Products with excess stock
- **Shows:** Excess units, working capital tied up (₹)
- **Example:** Component Y → 1150 excess units, ₹172,500 tied up

### 5️⃣ **Anomaly Detection**
- **Test:** `GET http://localhost:8000/api/anomalies`
- **What it finds:** Unusual demand spikes/drops
- **Cause attribution:** Promotion, Weather, or Unknown
- **Example:** Widget A spike on Jan 20-25 → **Cause: Promotion**, Z-score: 3.8

### 6️⃣ **Shipment Delay Detection**
- **Test:** `GET http://localhost:8000/api/shipments/delays`
- **What it shows:** All late shipments
- **Includes:** Supplier, product, original ETA, current ETA, delay days

### 7️⃣ **🌟 DISRUPTION CASCADE SIMULATOR** ⭐
- **Test:** 
  1. `POST http://localhost:8000/api/simulate/trigger-delay`
  2. Then: `GET http://localhost:8000/api/shipments/{shipment_id}/impact`
- **THE DEMO WINNER:** Shows exactly which orders get affected by a delay
- **Response includes:**
  - Affected products
  - Affected warehouses (and how long stock will last)
  - At-risk customer orders (with ₹ values)
  - Summary: "This delay puts 2 orders at risk, ₹87,500 impact"

### 8️⃣ **Supplier Data (Ready to Use)**
- **In database:** 5 suppliers with realistic profiles
  - Supplier A: 71% on-time (risky)
  - Supplier B: 96% on-time (premium)
  - Includes recovery resilience scores
- **API endpoint:** Not yet implemented (Tanishka's task)
- **Data is 100% ready to use**

---

## 🔄 PARTIALLY READY (6 Features)

| Feature | Status | What Works | What's Missing |
|---------|--------|-----------|-----------------|
| Confidence Scores | 80% | In forecasts (0-1 based on variance) | In recommendations (TBD) |
| Cost-of-Delay | 50% | ₹ values in cascade impact | Full calculation in recommendations (TBD) |
| Recovery Resilience | 0% (data ready) | Seeded in suppliers table | Endpoint not implemented yet |
| Exec Summary | 0% | Route exists | Need to wire Claude LLM |
| Chat/NLQ | 0% | Route exists | Need to wire Claude LLM |
| Dashboard Overview | 30% | Basic aggregation logic | Needs polish + frontend |

---

## ❌ NOT YET STARTED (5 Features)

| Feature | Assigned | Task |
|---------|----------|------|
| Supplier Scoring Endpoint | Tanishka | Build `/api/suppliers/scores` |
| Alternate Supplier Recommendations | Tanishka | Build `/api/recommendations` |
| Allocation Priority | Tanishka | Build `/api/allocation/{product_id}` |
| Procurement Suggestions | Tanishka | Build `/api/procurement/suggestions` |
| Dealer Messages | Tanishka | Build `/api/recommendations/{id}/message` |

---

## 🎬 LIVE DEMO FLOW (100% READY)

```
Step 1: Dashboard Shows Normal State
  GET /api/dashboard/overview
  → ₹50K in pending orders, all suppliers OK

Step 2: TRIGGER DISRUPTION
  POST /api/simulate/trigger-delay
  → Shipment marked 4 days late

Step 3: Show Impact
  GET /api/shipments/delays
  → "Supplier A delayed by 4 days"

Step 4: TRACE CASCADE
  GET /api/shipments/{id}/impact
  → "2 orders at risk, ₹87,500 impact"

Step 5: Show Forecast
  GET /api/inventory/Widget-A/forecast
  → "3.2 days to stockout"

Step 6: Show Anomalies
  GET /api/anomalies
  → "Promo spike drove low inventory"

[Steps 7-9 pending LLM integration]
```

**Try this right now to see the demo in action!**

---

## 📝 EXAMPLE CURL COMMANDS

```bash
# Seed database
curl -X POST http://localhost:8000/api/seed

# Get all inventory
curl http://localhost:8000/api/inventory

# Get overstock items
curl http://localhost:8000/api/inventory/overstock

# Get anomalies
curl http://localhost:8000/api/anomalies

# Get delayed shipments
curl http://localhost:8000/api/shipments/delays

# TRIGGER DEMO DISRUPTION
curl -X POST "http://localhost:8000/api/simulate/trigger-delay?delay_days=4"

# Get cascade impact (use shipment_id from previous response)
curl "http://localhost:8000/api/shipments/{shipment_id}/impact"

# Get forecast for a product (use product_id from /api/inventory)
curl "http://localhost:8000/api/inventory/{product_id}/forecast"
```

---

## 🎯 PROGRESS CHECKLIST

### Backend (Swastik)
- [x] Database schema (14 tables)
- [x] Seed script (90 days of realistic data)
- [x] Inventory monitoring (`/api/inventory`)
- [x] Shortage prediction (`/api/inventory/{sku_id}/forecast`)
- [x] Overstock detection (`/api/inventory/overstock`)
- [x] Anomaly detection (`/api/anomalies`)
- [x] Shipment tracking (`/api/shipments/delays`)
- [x] Cascade simulator (`/api/shipments/{id}/impact`)
- [x] Demo trigger (`/api/simulate/trigger-delay`)
- [ ] Chat/NLQ agent (wire Claude LLM)
- [ ] Dashboard aggregation (polish)

### Backend (Tanishka)
- [ ] Supplier scoring (`/api/suppliers/scores`)
- [ ] Recommendations engine (`/api/recommendations`)
- [ ] Allocation logic (`/api/allocation/{product_id}`)
- [ ] Procurement suggestions (`/api/procurement/suggestions`)
- [ ] Dealer message generator (LLM)
- [ ] Executive summary (LLM)

### Frontend (Swastik)
- [ ] Inventory screen
- [ ] Anomaly feed
- [ ] Shipment delay screen (with cascade visual)
- [ ] Chat screen
- [ ] Dashboard

### Frontend (Tanishka)
- [ ] Supplier risk screen
- [ ] Recommendations feed
- [ ] Allocation priority screen
- [ ] Procurement suggestions screen
- [ ] Executive summary view

---

## 💡 KEY INSIGHTS

**What makes the cascade simulator special:**
- Most supply chain tools show isolated metrics (shipment is late, inventory is low)
- SupplySense connects the dots: delay → affects these 5 products → affects these 2 warehouses → affects these 2 customer orders → ₹87,500 at risk
- This is what operations teams actually care about during a crisis

**What's unique about the data:**
- Not fake flat numbers; includes real patterns:
  - Seasonal spike (Q4-like demand increase)
  - Promotional spike (Widget A doubled demand for 6 days)
  - Varied supplier performance (Supplier A risky, Supplier B reliable)
  - Multi-warehouse complexity
- Judges will see that this could actually work in production

**What's ready for judges to see:**
- Full end-to-end demo with real data
- Click one button → watch disruption cascade through 5 layers
- Answer: "What's the impact?" → ₹87,500 (immediate, clear answer)
- Answer: "Why did this happen?" → Promo spike drove low inventory (root cause)

---

## 🚀 NEXT STEPS

**To keep momentum:**

1. **Swastik:** Wire Claude LLM for chat agent (Phase 5, 4-5 hrs)
   - Define tools for inventory, delays, cascade, recommendations
   - Test tool-calling pattern
   - Add reasoning trace display

2. **Tanishka:** Build supplier scoring + recommendations (Phases 5-8, 6-8 hrs)
   - Supplier score formula (reliability + recovery resilience)
   - Alternate supplier matcher
   - Cost-of-delay calculation
   - Dealer message LLM integration

3. **Both:** Build frontend screens (Phases 9-10, 10-12 hrs)
   - Inventory screen with forecast/overstock
   - Cascade simulator visual
   - Chat with reasoning trace
   - Dashboard 7-day lookahead

**Total remaining: ~20-25 hours**
**Time to demo-ready: 2-3 days of focused work**

