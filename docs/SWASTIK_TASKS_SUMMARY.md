# SupplySense Project — Complete Overview & Swastik's Task Breakdown

---

## **PROJECT OVERVIEW**

### **What is SupplySense?**
An AI-powered supply chain risk & inventory intelligence system that:
- Watches the entire supply chain 24/7
- Predicts problems before they happen (7-day lookahead)
- Recommends specific actions with reasoning & ₹ impact
- Lets operations teams ask questions in plain English instead of digging through dashboards
- Traces disruption cascades (delay → affected products → affected orders → ₹ impact)

**Tagline:** "A smart doctor for your supply chain"

---

## **ALL FEATURES IN THE PROJECT** (19 mandatory)

### **Data & Monitoring (3 features)**
1. **Multi-source data ingestion** — suppliers, warehouses, POs, inventory, logistics, external data (weather, news)
2. **Real-time inventory monitoring** — stock levels across warehouses, dashboard visibility
3. **Shipment delay detection** — with downstream business impact estimation

### **Prediction & Intelligence (3 features)**
4. **Shortage/overstock prediction** — using demand history + inventory trends, with confidence score
5. **Abnormal demand spike detection** — with cause attribution (seasonality, promo, external event, weather)
6. **Supplier reliability scoring** — delivery performance, lead time, quality, fulfillment rate history

### **Decision Support & Recommendations (4 features)**
7. **Alternate supplier/warehouse recommendations** — during disruption, with reasoning
8. **Recovery Resilience Score** — how fast a supplier bounces back after a miss
9. **Inventory allocation prioritization** — when stock is limited, rank which pending orders get it first
10. **Procurement recommendations** — what to reorder, how much, by when (from forecasted demand)

### **Reporting & Interface (3 features)**
11. **Cost-of-Delay Translator** — ₹ impact estimate on every risk flag
12. **Unified real-time dashboard** — 7-day lookahead + today's snapshot, all key metrics in one place
13. **Auto-generated executive summary** — plain-English LLM-generated report
14. **Natural language query interface** — agentic chat that chains reasoning across multiple data sources

### **Differentiating Factors (8 features)**
15. **Disruption Cascade Simulator** — trace delay → products → inventory → orders → customers
16. **Decision-Ready Intelligence** — every risk shows recommended action + cost of inaction
17. **7-Day Lookahead as default view** — anticipate, don't react
18. **Explainable recommendations** — show why (supplier comparison, reasoning text, confidence)
19. **Confidence scores on predictions** — build trust, not blind faith

**Additional (if time):**
- What-If Scenario Engine (simulate supplier failure, demand spike)
- Silent Stockout Radar (products trending toward stockout)
- Autonomous mitigation (auto-draft POs, stock transfers for approval)

---

## **ALL MANDATORY SCREENS** (12 total)

| Screen | Purpose |
|--------|---------|
| **Main Dashboard** | 7-day lookahead overview + today's snapshot + active disruption count |
| **Inventory Screen** | Stock per SKU/warehouse, shortage/overstock flags, confidence scores |
| **Overstock View** | Toggle on Inventory Screen — same layout, opposite direction |
| **Anomaly Feed** | Detected demand spikes with likely causes (promo/weather/unknown) |
| **Shipment Delay Screen** | Delayed shipments + cascade impact (which orders/customers affected) |
| **Supplier Risk Screen** | Ranked supplier scorecard, reliability scores, Recovery Resilience Score |
| **Recommendations Feed** | Active recommendations with reasoning, cost impact, dealer message generator |
| **Allocation Priority Screen** | Ranked pending orders for limited-stock SKUs, with priority reasoning |
| **Procurement Suggestions Screen** | What to reorder, how much, from whom, by when |
| **Executive Summary View** | Auto-generated plain-English report |
| **Chat/NLQ Screen** | Natural language query interface with reasoning trace |
| **Demo Trigger Control** | Button to trigger shipment delay (for live demo) |

---

## **TECH STACK**

| Component | Choice | Why |
|-----------|--------|-----|
| Backend | **FastAPI** (Python) | Fast to build, async support, great for ML/data work |
| Database | **PostgreSQL** | Relational data fits supply chain entities; easy parallel querying |
| Frontend | **Next.js 14** | Dashboard-friendly, matches team's usual stack |
| LLM | **Anthropic Claude** or OpenAI | Executive summaries, NLQ agent, dealer messages |
| External Data | **OpenWeatherMap API** (free tier) | Real live signal for demo credibility |
| Hosting (optional) | Localhost for dev; Render/Railway for backend if deployed | Keep it simple — local demo is fine |

---

## **DATABASE SCHEMA** (14 tables total)

**Swastik owns 13 tables:**
1. `suppliers` — supplier data with reliability metrics
2. `warehouses` — warehouse locations
3. `products` (SKUs) — product catalog with margins
4. `inventory_snapshots` — current stock per product/warehouse
5. `demand_history` — historical daily demand per product/warehouse
6. `purchase_orders` — POs from suppliers (on-time/late records)
7. `shipments` — shipment tracking with ETAs, delays
8. `shipment_events` — individual shipment status updates
9. `external_signals` — weather, news, promo flags
10. `forecasts` — output: predicted days-to-stockout + confidence
11. `anomalies` — output: detected spikes with likely cause
12. `chat_logs` — conversation history for the NLQ agent
13. `customer_orders` — pending customer orders (raw ingested data)

**Tanishka owns 4 tables:**
- `recommendations` — output: suggested actions with reasoning
- `dealer_messages` — output: LLM-generated supplier/dealer messages
- `allocation_decisions` — output: priority ranking for limited stock
- `procurement_suggestions` — output: generated reorder suggestions

---

## **API ENDPOINTS** (15 total)

**Swastik owns 8 endpoints:**
- `GET /api/inventory` — stock levels per SKU/warehouse
- `GET /api/inventory/{sku_id}/forecast` — shortage prediction + confidence
- `GET /api/inventory/overstock` — overstock detection
- `GET /api/anomalies` — demand spikes with causes
- `GET /api/shipments/delays` — delayed shipments
- `GET /api/shipments/{id}/impact` — cascade impact tracing
- `POST /api/simulate/trigger-delay` — manual demo trigger
- `POST /api/chat` — agentic NLQ with tool-calling

**Tanishka owns 6 endpoints:**
- `GET /api/suppliers/scores` — reliability + Recovery Resilience scores
- `GET /api/recommendations` — recommended actions
- `POST /api/recommendations/{id}/message` — generate dealer message
- `GET /api/allocation/{product_id}` — priority ranking for orders
- `GET /api/procurement/suggestions` — reorder suggestions
- `GET /api/summary/executive` — LLM-generated summary

**Joint:**
- `GET /api/dashboard/overview` — aggregates both tracks

---

## **USER STORIES** (10 total)

1. **7-Day Lookahead** — Open dashboard, immediately see what breaks next week (not just today)
2. **Cascade Tracing** — When shipment is delayed, see exactly which orders/products it threatens
3. **Explainable Recommendations** — Supplier recommendation shows why (reliability %, lead time, Recovery Score)
4. **Financial Stakes** — Know the rupee cost of ignoring a risk
5. **Agentic Chat** — Ask "what's causing today's biggest disruption?" and get a synthesized answer across multiple data sources
6. **Auto-Drafted Messages** — System drafts supplier/dealer outreach; you don't have to write it
7. **Overstock Awareness** — Know when you're sitting on too much stock (working capital drain)
8. **Demand Anomaly Explanation** — When demand spikes/drops, system tells you why (not just that it happened)
9. **Allocation Priority** — When stock is limited, system ranks which pending orders should get it first + why
10. **Procurement Suggestions** — Get reorder suggestions generated from actual forecasts (not manual math)

---

---

# **SWASTIK'S COMPLETE TASK BREAKDOWN**

## **HIGH-LEVEL RESPONSIBILITY**
You own the **data layer**, **prediction engine**, and **NLQ chat agent** — basically everything that powers the analytics/intelligence side of SupplySense.

**Effort split:**
- 13 database tables
- 8 API endpoints (including the hardest one: the chat agent)
- 9 core features
- 6 frontend screens (Inventory, Overstock, Anomalies, Shipment Delays, Chat, Dashboard lead)

---

## **BACKEND TASKS — IN BUILD ORDER**

### **Phase 0: Shared Setup (do together, ~20 min)**
- [ ] Create FastAPI + PostgreSQL skeleton
- [ ] Agree on DB naming conventions, ID strategy (UUID vs. serial)
- [ ] Agree on API response format (JSON structure, error handling)
- [ ] Set up basic project structure (migrations, models, services)

---

### **Phase 1: Database Schema & Seeding** (Swastik solo, ~2-3 hours)

#### **Step 1a: Create all 13 tables** (migrations/models)
```
suppliers
warehouses
products
inventory_snapshots
demand_history
purchase_orders
shipments
shipment_events
external_signals
forecasts (output table)
anomalies (output table)
chat_logs (output table)
customer_orders
```

**Key fields to include:**
- `suppliers`: id, name, product_categories[], avg_lead_time_days, on_time_rate, quality_rate, reliability_score (computed), recovery_resilience_score (computed)
- `products`: id, name, category, unit_margin, unit_price
- `inventory_snapshots`: product_id, warehouse_id, stock_on_hand, reorder_point, safety_stock, recorded_at
- `demand_history`: product_id, warehouse_id, date, units_sold, is_promo_flag (for anomaly cause)
- `shipments`: purchase_order_id, carrier_name, current_status (in_transit/delayed/delivered), original_eta, current_eta, delay_days
- `forecasts`: product_id, warehouse_id, predicted_days_to_stockout, confidence_score, generated_at
- `anomalies`: product_id, detected_at, anomaly_type (spike/drop), likely_cause (promo/weather/unknown), severity
- `customer_orders`: id, product_id, warehouse_id, quantity, required_by_date, order_value (for cost-of-delay), status

#### **Step 1b: Write seed script** (~800 lines, core demo data)
Generate realistic test data:

**Suppliers (5-8):**
- Mix of good (95% on-time), mediocre (75%), and bad but fast recovery (60% on-time, recovers in 2 days)
- Vary lead times (3-14 days)
- Assign product categories each can supply

**Warehouses (2-3):**
- Different locations (for weather API lookup)
- Different capacities

**Products (15-20 SKUs):**
- Vary by category, margin, price
- Include 1-2 that are deliberately overstocked (for allocation demo)
- Include 1-2 that will have predicted shortages

**Demand history (3-6 months):**
- Daily sales per product/warehouse
- Bake in 1 seasonal pattern (e.g., spike in Q4)
- Bake in 1 promo spike (flag with `is_promo_flag = true`)
- Add realistic variance

**Purchase orders (10-15):**
- Mix of on-time and late deliveries
- Reference real suppliers + products
- Some marked as "delivered," some "pending"

**Shipments (5-10):**
- One clearly delayed (reserved for demo trigger)
- Mix of delivered and in-transit

**Customer orders (5-10):**
- Pending orders with various required dates
- One SKU with multiple pending orders (for allocation demo)
- Order values for cost-of-delay calc

---

### **Phase 2: Prediction Engine** (Swastik solo, ~3 hours)

#### **Step 2a: Inventory monitoring endpoint**
```
GET /api/inventory
→ Returns: list of all SKUs with current stock per warehouse, reorder_point, safety_stock
```

**Implementation:**
- Query `inventory_snapshots` (latest recorded_at per product/warehouse)
- Include warehouse name, product name, stock level
- Return as JSON list

#### **Step 2b: Shortage prediction (core ML)**
```
GET /api/inventory/{sku_id}/forecast
→ Returns: predicted_days_to_stockout, confidence_score, reasoning
```

**Formula (keep it simple for hackathon):**
```
days_to_stockout = current_stock / rolling_avg_daily_demand (last 30 days)
confidence_score = 1.0 - (demand_variance / mean_demand)  // higher variance = lower confidence
```

**Logic:**
- Query inventory_snapshots for current stock
- Query demand_history for last 30 days
- Compute rolling avg + variance
- If days_to_stockout < 7, mark as "HIGH_RISK" (red)
- If 7-14, mark as "MEDIUM_RISK" (yellow)
- If >14, mark as "LOW_RISK" (green)
- Return all three + reasoning text

**Response shape:**
```json
{
  "sku_id": "abc123",
  "sku_name": "Widget A",
  "current_stock": 150,
  "daily_avg_demand": 25,
  "days_to_stockout": 6.0,
  "risk_level": "HIGH_RISK",
  "confidence_score": 0.78,
  "reasoning": "Based on 30 days of demand history. High variance due to seasonal variation."
}
```

#### **Step 2c: Overstock detection**
```
GET /api/inventory/overstock
→ Returns: products with excess stock, working capital impact
```

**Logic:**
- For each SKU/warehouse, compute "demand-justified stock" = (avg_daily_demand * safety_stock_days)
- If current_stock > demand_justified_stock * 1.5, flag as overstock
- Return excess_units + estimated working capital tied up

**Response shape:**
```json
{
  "sku_id": "xyz789",
  "sku_name": "Widget B",
  "current_stock": 500,
  "demand_justified_stock": 200,
  "excess_units": 300,
  "working_capital_tied_up": 15000,
  "recommendation": "Consider reducing reorders or increasing promotions"
}
```

#### **Step 2d: Anomaly detection**
```
GET /api/anomalies
→ Returns: detected demand spikes/drops with likely causes
```

**Logic:**
- Z-score anomaly detection on daily demand
- If |z-score| > 2, flag as anomaly
- Assign likely cause:
  - If `is_promo_flag = true` on that date → "Promotion"
  - If `external_signals` has weather/news on that date → "Weather/External event"
  - Otherwise → "Unknown"
- Rank by severity (how far from normal)

**Response shape:**
```json
{
  "anomaly_id": "anom_001",
  "sku_id": "abc123",
  "sku_name": "Widget A",
  "detected_at": "2024-01-15",
  "date_of_spike": "2024-01-14",
  "anomaly_type": "SPIKE",
  "units_sold": 120,
  "expected_units": 25,
  "z_score": 3.8,
  "likely_cause": "Promotion",
  "severity": "HIGH"
}
```

#### **Step 2e: Shipment delay detection**
```
GET /api/shipments/delays
→ Returns: list of delayed shipments with current ETA vs. original ETA
```

**Logic:**
- Query `shipments` where current_eta > original_eta
- Include purchase_order details (supplier, product, quantity)
- Calculate delay_days = current_eta - original_eta

**Response shape:**
```json
[
  {
    "shipment_id": "ship_001",
    "supplier_name": "Supplier A",
    "product_name": "Widget A",
    "quantity": 500,
    "original_eta": "2024-01-20",
    "current_eta": "2024-01-24",
    "delay_days": 4,
    "destination_warehouse": "Warehouse 2"
  }
]
```

#### **Step 2f: Cascade impact simulator (the hardest part)**
```
GET /api/shipments/{id}/impact
→ Returns: which products, warehouses, orders, customers are affected by this delay
```

**Logic (trace the chain):**
1. Get the delayed shipment → find which products + quantity
2. Query `inventory_snapshots`: which warehouses are these products low in?
3. Query `customer_orders`: which pending orders depend on low stock of these products in those warehouses?
4. Calculate at-risk order value + delay impact
5. Return the cascade chain

**Response shape:**
```json
{
  "shipment_id": "ship_001",
  "supplier_name": "Supplier A",
  "delay_days": 4,
  "cascade": {
    "affected_products": [
      {
        "product_id": "abc123",
        "product_name": "Widget A",
        "shipment_quantity": 500
      }
    ],
    "affected_warehouses": [
      {
        "warehouse_id": "wh_02",
        "warehouse_name": "Warehouse 2",
        "current_stock": 100,
        "stock_will_last_days": 4
      }
    ],
    "at_risk_orders": [
      {
        "order_id": "ord_001",
        "customer_id": "cust_A",
        "product_id": "abc123",
        "quantity": 200,
        "required_by_date": "2024-01-23",
        "order_value": 50000
      },
      {
        "order_id": "ord_002",
        "customer_id": "cust_B",
        "product_id": "abc123",
        "quantity": 150,
        "required_by_date": "2024-01-25",
        "order_value": 37500
      }
    ],
    "total_at_risk_order_value": 87500,
    "summary": "This delay puts 2 pending orders at risk of stockout. 350 units at risk. Total value: ₹87,500."
  }
}
```

#### **Step 2g: Write to output tables**
When any of steps 2b-2d run, write results to:
- `forecasts` (from 2b)
- `anomalies` (from 2d)
- Cascade impact doesn't get written; it's computed on-demand in 2f

---

### **Phase 3: Demo Trigger Endpoint** (Swastik solo, ~30 min)

```
POST /api/simulate/trigger-delay
Body: { shipment_id: string, delay_days: number }
→ Side effect: marks shipment as delayed, re-triggers 2b-2d, returns updated data instantly
```

**Implementation:**
1. Find the shipment by ID
2. Update its current_eta = original_eta + delay_days
3. Re-run forecast + anomaly detection (in-memory; don't need DB writes for this demo flow)
4. Return the updated shipment + cascade impact
5. This is your single most important piece for live demo control

**Response:**
```json
{
  "status": "delay_triggered",
  "shipment_id": "ship_001",
  "new_delay_days": 4,
  "affected_orders": 2,
  "total_at_risk_value": 87500
}
```

---

### **Phase 4: Weather API Integration** (Swastik solo, ~1 hour)

```
Background task: Poll OpenWeatherMap API every 15 min
→ Store in external_signals table
→ Use in anomaly cause attribution
```

**Implementation:**
1. Get list of warehouse locations from DB
2. For each location, call `https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}`
3. Parse weather + severity
4. Store in `external_signals` (signal_type='weather', location, description, severity, fetched_at)
5. Use this data when assigning `likely_cause` in anomaly detection

**Simple example trigger:**
- Weather alerts for a warehouse location
- Anomaly detector checks: "Was there bad weather on the day this spike/drop happened?"
- If yes → mark as `likely_cause: "Weather"` instead of "Unknown"

---

### **Phase 5: Chat/NLQ Agent (Swastik solo — hardest piece, ~4-5 hours)**

```
POST /api/chat
Body: { question: string }
→ Returns: { answer: string, tools_used: string[], reasoning_steps: any[] }
```

**Why this is hardest:**
- LLM tool-calling agent pattern (Claude/OpenAI function calling)
- Must define tools as endpoints your own API exposes
- Agent decides which tools to call based on question
- Agent chains reasoning across inventory + shipments + suppliers + anomalies
- Must show reasoning trace (not just final answer)

**Tools to expose to the LLM:**
1. `get_inventory_status(sku_id: str)` → calls your `/api/inventory/{sku_id}/forecast`
2. `get_shipment_delays()` → calls your `/api/shipments/delays`
3. `get_anomalies()` → calls your `/api/anomalies`
4. `get_supplier_score(supplier_id: str)` → calls Tanishka's `/api/suppliers/scores` (stub with fake data if not ready)
5. `get_recommendations()` → calls Tanishka's `/api/recommendations` (stub if not ready)
6. `get_cascade_impact(shipment_id: str)` → calls your `/api/shipments/{id}/impact`

**Implementation pattern (using Anthropic SDK):**
```python
import anthropic

def chat_agent(question: str):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    tools = [
        {
            "name": "get_inventory_status",
            "description": "Get current inventory level and shortage forecast for a product",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sku_id": {"type": "string", "description": "The product SKU ID"}
                },
                "required": ["sku_id"]
            }
        },
        # ... define other tools similarly
    ]
    
    messages = [{"role": "user", "content": question}]
    reasoning_steps = []
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # or latest Claude model
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        
        # If the LLM wants to call a tool:
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    
                    # Call your own API
                    tool_result = call_my_api(tool_name, tool_input)
                    
                    reasoning_steps.append({
                        "tool": tool_name,
                        "input": tool_input,
                        "result": tool_result
                    })
                    
                    # Add tool result back to conversation
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(tool_result)
                            }
                        ]
                    })
        else:
            # LLM is done; extract final answer
            final_answer = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    final_answer += block.text
            
            return {
                "answer": final_answer,
                "tools_used": [s["tool"] for s in reasoning_steps],
                "reasoning_steps": reasoning_steps
            }
```

**Example conversation:**

User asks: *"What's causing today's biggest disruption?"*

Agent reasoning:
1. Calls `get_shipment_delays()` → finds a delayed shipment
2. Calls `get_cascade_impact(shipment_001)` → finds 2 at-risk orders
3. Calls `get_inventory_status(product_abc)` → sees stock at 100, will last 4 days
4. Calls `get_supplier_score(supplier_a)` → sees 71% on-time rate
5. Synthesizes answer: "Supplier A's shipment is delayed by 4 days. Widget A stock will run out in 4 days. 2 customer orders are at risk (₹87.5K value). Supplier A's reliability is concerning at 71% on-time."

Return:
```json
{
  "answer": "Your biggest disruption today is a delayed shipment from Supplier A. Widget A stock will run out in 4 days, putting 2 pending customer orders at risk (total value: ₹87,500). Supplier A has a 71% on-time delivery rate, which is below your average. I'd recommend switching to Supplier B (96% on-time) for urgent restocks.",
  "tools_used": ["get_shipment_delays", "get_cascade_impact", "get_inventory_status", "get_supplier_score"],
  "reasoning_steps": [ ... ]
}
```

**Store in `chat_logs` table:**
- question
- answer
- tools_used
- created_at

---

### **Phase 6: Midpoint Sync** (Swastik + Tanishka together, ~1 hour)

**Checklist (do NOT skip):**
- [ ] Trigger a delay via `/api/simulate/trigger-delay`
- [ ] Confirm forecasts update correctly
- [ ] Confirm cascade impact shows the right orders
- [ ] Confirm chat agent answers a question about this scenario correctly
- [ ] Confirm anomalies are detected with causes
- [ ] Tanishka: confirm `/api/recommendations` pulls real data
- [ ] Tanishka: confirm `/api/summary/executive` reflects real numbers
- [ ] Tanishka: confirm `/api/allocation/{product_id}` ranks orders correctly
- [ ] Tanishka: confirm `/api/procurement/suggestions` shows real suggestions
- [ ] Build `/api/dashboard/overview` together (simple aggregation)

---

## **FRONTEND TASKS — IN BUILD ORDER**

### **Phase 7: Frontend Setup** (Swastik + Tanishka together, ~20 min)
- [ ] Create Next.js 14 project
- [ ] Agree on folder structure, design tokens (colors, fonts, spacing)
- [ ] Create shared API client (wrapper around `fetch`)
- [ ] Set up Tailwind CSS or your preferred styling

---

### **Phase 8: Frontend Builds** (Swastik solo, ~4-5 hours)

#### **Screen 1: Inventory Screen** (1 hour)
```
GET /api/inventory
→ Display: table/grid with columns:
   - Product name
   - Current warehouse stock
   - Reorder point
   - Safety stock
   - Days to stockout (from forecast)
   - Confidence score (%)
   - Risk level (color-coded: red/yellow/green)
   - Overstock flag (toggle to Overstock View)
```

**Features:**
- Sortable by stock level, days-to-stockout, risk level
- Click product → drill down to forecast details
- Toggle between "Shortage View" and "Overstock View"

**Overstock View (same screen, different tab):**
```
GET /api/inventory/overstock
→ Display: excess units, working capital tied up, recommendation
```

#### **Screen 2: Anomaly Feed** (45 min)
```
GET /api/anomalies
→ Display: list of recent demand spikes/drops with:
   - Product name
   - Date detected
   - Type (SPIKE/DROP)
   - Actual vs. expected units
   - Likely cause (Promo/Weather/Unknown) — color-coded
   - Severity badge
```

#### **Screen 3: Shipment Delay Screen** (1.5 hours)
```
GET /api/shipments/delays + GET /api/shipments/{id}/impact
→ Display two sections:

A) List of delayed shipments:
   - Supplier name
   - Product(s)
   - Original ETA vs. Current ETA
   - Delay days (highlighted if > 3)

B) Cascade Simulator (when you click a shipment):
   - Affected products
   - Affected warehouses (current stock, days stock will last)
   - At-risk customer orders (order ID, customer, quantity, order value)
   - Summary: "This delay puts X orders at risk of stockout within Y days"
   - Visual flow chart showing: Delay → Products → Warehouses → Orders
```

**Key UI detail:**
- Cascade impact should have a clean flow visual (arrows, boxes)
- Color-code orders by urgency (required date closest to today = more urgent)

#### **Screen 4: Chat/NLQ Screen** (1.5 hours — hardest)
```
POST /api/chat
→ Display:
   - Chat history (past Q&A)
   - Input box (text field)
   - Submit button
   - Response area with:
     * Agent's answer (plain text)
     * Reasoning trace (expandable):
       - Tools called in order
       - Data pulled from each tool
       - Final synthesis
```

**UI challenge:**
- Make reasoning trace readable (not a wall of JSON)
- Show tools called with icons/labels
- Show intermediate results (what data agent pulled)
- Final answer in bold at top

**Example rendering:**
```
User: "What's causing today's biggest disruption?"

[Answer] ▼
"Your biggest disruption today is a delayed shipment from Supplier A..."

[Show Reasoning] ▼
  1. get_shipment_delays()
     → Found 1 delayed shipment (Supplier A, 4 days late)
  
  2. get_cascade_impact(shipment_001)
     → 2 pending orders at risk, ₹87.5K total value
  
  3. get_inventory_status(product_abc)
     → 100 units on hand, 4 days until stockout
  
  4. get_supplier_score(supplier_a)
     → 71% on-time delivery rate
```

#### **Screen 5: Dashboard + Demo Trigger** (1.5 hours)
```
GET /api/dashboard/overview (joint with Tanishka)
→ Display: 7-Day Lookahead by default
   - Overview cards:
     * Total at-risk order value (₹)
     * Pending orders
     * Suppliers at risk (yellow/red)
     * SKUs predicted to stock out (next 7 days)
   - Key metrics:
     * Warehouse utilization %
     * Average supplier on-time rate
     * Number of active anomalies
   - Disruption card (from Tanishka):
     * Shows active disruptions
     * Clickable → goes to Shipment Delay Screen
   
   [Toggle] Today's Snapshot (below the lookahead)
   - Current inventory status
   - Current shipment status
   - Today's anomalies

Demo Trigger Button:
   - Embedded in Dashboard header
   - Click → triggers POST /api/simulate/trigger-delay
   - Shows: "Delay triggered! Refresh to see impact"
```

**Key UI detail:**
- 7-day lookahead should be the prominent, default view
- Today's snapshot is secondary, collapsed/tabbed below
- Color scheme:
  - Red: HIGH_RISK (days-to-stockout < 7)
  - Yellow: MEDIUM_RISK (7-14 days)
  - Green: LOW_RISK (>14 days)

---

## **TESTING CHECKLIST**

Before moving to Tanishka's frontend:
- [ ] Every endpoint returns real data (not mocked)
- [ ] Dashboard refreshes correctly after demo trigger
- [ ] Chat answers match what's shown on detail screens
- [ ] Cascade impact is accurate (orders shown match actual pending orders)
- [ ] Confidence scores are between 0-1
- [ ] Anomalies show correct causes (weather matches external_signals dates)

---

## **TIMELINE ESTIMATE**

| Phase | Est. Hours | Total |
|-------|-----------|-------|
| Phase 0: Setup | 0.3 | 0.3 |
| Phase 1: DB + Seeding | 2.5 | 2.8 |
| Phase 2: Prediction engine (2b-2g) | 3.5 | 6.3 |
| Phase 3: Demo trigger | 0.5 | 6.8 |
| Phase 4: Weather API | 1 | 7.8 |
| Phase 5: Chat agent | 4.5 | 12.3 |
| Phase 6: Midpoint sync | 1 | 13.3 |
| Phase 7: Frontend setup | 0.3 | 13.6 |
| Phase 8: Frontend screens (1-5) | 5 | 18.6 |

**Total: ~18.5 hours** (realistic for one person working on core logic + basic UI)

---

## **SUCCESS CRITERIA (for your track)**

- [ ] All 13 tables created + seeded with realistic test data
- [ ] All 8 endpoints return correct data
- [ ] Demo trigger works: one click → shipment marked delayed → cascade updated instantly
- [ ] Chat agent can answer at least 3 sample questions:
  1. "What's causing today's biggest disruption?"
  2. "Which products will stock out in the next 7 days?"
  3. "How many customer orders are at risk right now?"
- [ ] All 5 frontend screens render real backend data (no mocks)
- [ ] Confidence scores shown on forecasts
- [ ] Cascade simulator visual is clear and accurate
- [ ] Chat reasoning trace is readable

---

## **KNOWN BLOCKERS & HOW TO HANDLE THEM**

1. **Chat agent hallucinates numbers**
   - Solution: Double-check LLM prompt. Add constraint: "Only use data from tool results; never make up numbers."

2. **Cascade impact takes too long to compute**
   - Solution: Pre-compute and cache for demo; compute on-demand for real use.

3. **Weather API quota exhausted**
   - Solution: Use a test city (e.g., always fetch for Mumbai); mock data as fallback.

4. **Anomaly detection too noisy**
   - Solution: Adjust z-score threshold (start at 2.5, tune down if needed).

5. **Forecasts show negative days-to-stockout**
   - Solution: Add max(days, 0) constraint; show "In Stock" if positive stock and negative days.

---

## **HANDOFF TO FRONTEND**

Once all backend endpoints are tested and working:
1. Create Postman collection with sample requests/responses
2. Write API documentation (even simple README with curl examples)
3. Give Tanishka the endpoint responses so she can build frontend in parallel
4. You can stub Tanishka's endpoints with fake data so her frontend doesn't block on her backend

This way, both of you can work in parallel without waiting on each other.

