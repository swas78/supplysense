# SupplySense Backend API - Complete Endpoint Reference

## Base URL
```
http://localhost:8000/api
```

## API Documentation (Swagger UI)
```
http://localhost:8000/docs
```

---

## 1. DATA INGESTION & INVENTORY MONITORING

### Get Inventory Status (All Products)
```
GET /api/inventory
```
Returns: Stock levels per warehouse for all products

**Response:**
```json
{
  "status": "success",
  "warehouses": [
    {
      "warehouse_id": "wh1",
      "warehouse_name": "Mumbai Central",
      "products": [
        {
          "product_id": "p1",
          "product_name": "Circuit Board",
          "stock_on_hand": 450,
          "safety_stock": 100,
          "status": "HEALTHY"
        }
      ]
    }
  ]
}
```

---

## 2. SHORTAGE PREDICTION & FORECASTING

### Get Shortage Forecast
```
GET /api/inventory/{sku_id}/forecast
```
Returns: Days to stockout with confidence score

**Example:**
```
GET /api/inventory/p1/forecast
```

**Response:**
```json
{
  "status": "success",
  "product_id": "p1",
  "product_name": "Circuit Board",
  "warehouse_id": "wh1",
  "current_stock": 450,
  "daily_demand": 125.5,
  "predicted_days_to_stockout": 3.6,
  "confidence_score": 0.87,
  "reasoning": "Based on 30-day demand average (125.5 units/day), current stock will deplete on 2024-01-23",
  "recommendation": "URGENT: Reorder within 24 hours"
}
```

### Get Overstock Detection
```
GET /api/inventory/overstock
```
Returns: Products with excess inventory and working capital impact

**Response:**
```json
{
  "status": "success",
  "overstocked_products": [
    {
      "product_id": "p2",
      "product_name": "Cable Set",
      "warehouse_id": "wh2",
      "current_stock": 2000,
      "safe_stock": 300,
      "excess_units": 1700,
      "excess_value_inr": 170000,
      "days_to_move": 13.6,
      "status": "CRITICAL_OVERSTOCK"
    }
  ]
}
```

---

## 3. ANOMALY DETECTION

### Get Demand Anomalies
```
GET /api/anomalies
```
Returns: Demand spikes/drops with root cause attribution

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "anomalies": [
    {
      "anomaly_id": "anom1",
      "product_id": "p1",
      "product_name": "Circuit Board",
      "warehouse_id": "wh1",
      "anomaly_type": "SPIKE",
      "magnitude": 2.3,
      "date": "2024-01-18",
      "normal_demand": 125.5,
      "actual_demand": 289,
      "attributed_cause": "Promotional Campaign",
      "confidence_score": 0.91,
      "reasoning": "Demand spiked 2.3x above average. Correlates with marketing email sent on 2024-01-17"
    }
  ]
}
```

---

## 4. SHIPMENT DELAY DETECTION

### Get Delayed Shipments
```
GET /api/shipments/delays
```
Returns: Pending and delayed shipments with ETA updates

**Response:**
```json
{
  "status": "success",
  "total_shipments": 10,
  "on_time": 8,
  "delayed": 2,
  "shipments": [
    {
      "shipment_id": "ship1",
      "product_id": "p1",
      "supplier_name": "Supplier A",
      "original_eta": "2024-01-20",
      "current_eta": "2024-01-24",
      "delay_days": 4,
      "status": "DELAYED",
      "reasoning": "Port delays due to customs clearance"
    }
  ]
}
```

---

## 5. DISRUPTION CASCADE SIMULATOR ⭐

### Get Cascade Impact of Shipment Delay
```
GET /api/shipments/{shipment_id}/impact
```
Returns: All customer orders affected by a specific shipment delay

**Example:**
```
GET /api/shipments/ship1/impact
```

**Response:**
```json
{
  "status": "success",
  "shipment_id": "ship1",
  "product_id": "p1",
  "product_name": "Circuit Board",
  "supplier": "Supplier A",
  "delay_days": 4,
  "cascade_analysis": {
    "affected_customer_orders": 5,
    "total_at_risk_value": 125000,
    "affected_orders": [
      {
        "order_id": "co1",
        "customer_id": "cust1",
        "order_value": 25000,
        "required_by_date": "2024-01-22",
        "days_until_required": 1,
        "status": "AT_RISK"
      }
    ],
    "impact_summary": "5 customer orders (₹125,000) will be unfulfilled if this 4-day delay happens",
    "business_impact": {
      "revenue_at_risk": 125000,
      "customer_satisfaction_impact": "CRITICAL",
      "estimated_churn_risk": 0.15
    }
  }
}
```

---

## 6. SUPPLIER SCORING & PERFORMANCE

### Get All Supplier Scores
```
GET /api/suppliers/scores
```
Returns: All suppliers ranked by reliability score with recovery resilience

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "suppliers": [
    {
      "supplier_id": "sup2",
      "supplier_name": "Supplier B",
      "reliability_score": 0.927,
      "on_time_rate": 0.96,
      "avg_lead_time_days": 5,
      "quality_rate": 0.98,
      "recovery_resilience_score": 2.1,
      "risk_level": "LOW_RISK",
      "reasoning": "On-time delivery: 96%, Lead time: 5 days, Quality: 98%",
      "recovery_text": "Recovers in ~2.1 days after a miss (fast recovery)"
    }
  ]
}
```

### Get Supplier Details
```
GET /api/suppliers/{supplier_id}
```
Returns: Detailed supplier info with historical performance

**Example:**
```
GET /api/suppliers/sup2
```

**Response:**
```json
{
  "status": "success",
  "supplier": {
    "supplier_id": "sup2",
    "supplier_name": "Supplier B",
    "reliability_score": 0.927,
    "on_time_rate": 0.96,
    "quality_rate": 0.98,
    "avg_lead_time_days": 5,
    "recovery_resilience_score": 2.1,
    "product_categories": ["electronics", "components"],
    "historical_performance": {
      "total_orders": 12,
      "on_time_orders": 11,
      "late_orders": 1,
      "on_time_percentage": 91.7,
      "avg_late_days": 2.0
    }
  }
}
```

---

## 7. RECOMMENDATIONS ENGINE

### Get Active Recommendations
```
GET /api/recommendations
```
Returns: All active recommendations with cost impact and reasoning

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "recommendations": [
    {
      "recommendation_id": "rec1",
      "trigger_type": "shipment_delay",
      "trigger_ref_id": "ship1",
      "problem": "Supplier A delay (4 days) affecting Circuit Board",
      "current_supplier": "Supplier A",
      "recommended_action": "Switch to Supplier B",
      "reasoning_text": "Supplier A is 4 days late. Supplier B has 96% on-time rate (vs 71%), lead time 5 days (vs 10), recovery resilience 2.1 days. Risk of 5 orders unfulfilled (₹125,000).",
      "estimated_cost_impact_inr": 125000,
      "confidence_score": 0.92,
      "status": "active"
    }
  ]
}
```

### Get Recommendation Details
```
GET /api/recommendations/{rec_id}
```
Returns: Full recommendation with generated dealer message

**Example:**
```
GET /api/recommendations/rec1
```

**Response:**
```json
{
  "status": "success",
  "recommendation": {
    "id": "rec1",
    "trigger_type": "shipment_delay",
    "recommended_action": "Switch to Supplier B for expedited fulfillment",
    "reasoning_text": "...",
    "estimated_cost_impact_inr": 125000,
    "confidence_score": 0.92,
    "status": "active",
    "created_at": "2024-01-19T10:30:00"
  },
  "message": {
    "text": "EXPEDITE REQUEST\n\nDear Supplier Partner,\n\nWe are requesting expedited fulfillment...",
    "recipient": "Supplier B"
  }
}
```

### Generate Dealer Message
```
POST /api/recommendations/{rec_id}/message
```
Generates auto-drafted supplier/dealer message for execution

**Response:**
```json
{
  "status": "success",
  "message": "EXPEDITE REQUEST\n\nDear Supplier Partner,\n\n...",
  "recipient": "Supplier B",
  "message_id": "msg1"
}
```

---

## 8. INVENTORY ALLOCATION PRIORITY

### Get Allocation Priority for Product
```
GET /api/allocation/{product_id}
```
Returns: Ranked pending orders with allocation priority when stock is limited

**Example:**
```
GET /api/allocation/p1
```

**Response:**
```json
{
  "status": "success",
  "product_id": "p1",
  "product_name": "Circuit Board",
  "available_stock": 450,
  "total_pending_demand": 750,
  "shortage": 300,
  "allocation_plan": [
    {
      "order_id": "co1",
      "customer_id": "cust1",
      "requested_quantity": 100,
      "allocated_quantity": 100,
      "priority_rank": 1,
      "priority_score": 92.5,
      "status": "FULFILLED",
      "required_by_date": "2024-01-22",
      "days_until_required": 1,
      "order_value": 25000,
      "reasoning": "Due in 1 days (URGENT) | Order value: ₹25,000 | Quantity: 100 units"
    }
  ],
  "summary": "Available stock: 450 units | Total demand: 750 units | Shortage: 300 units. Fulfilled: 3, Partial: 1, Unfulfilled: 1. Prioritized by: order value (40%), delivery urgency (40%), order size (20%)."
}
```

---

## 9. PROCUREMENT SUGGESTIONS

### Get Procurement Suggestions
```
GET /api/procurement/suggestions
```
Returns: What to reorder, how much, from whom, by when

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "suggestions": [
    {
      "product_id": "p1",
      "product_name": "Circuit Board",
      "warehouse_id": "wh1",
      "current_stock": 450,
      "daily_demand": 125.5,
      "days_to_stockout": 3.6,
      "suggested_quantity": 1800,
      "recommended_supplier_id": "sup2",
      "recommended_supplier_name": "Supplier B",
      "supplier_on_time_rate": 0.96,
      "supplier_lead_time_days": 5,
      "order_deadline": "2024-01-19",
      "urgency": "CRITICAL",
      "estimated_cost": 180000,
      "reasoning": "Stock will run out in 3.6 days. Current stock: 450 units. Daily demand: 125.5 units. Recommend reorder 1800 units from Supplier B (96% on-time, 5 day lead time). Order deadline: 2024-01-19 to ensure arrival before stockout.",
      "confidence_score": 0.87
    }
  ]
}
```

### Get Procurement Suggestion for Product
```
GET /api/procurement/suggestions/{product_id}
```
Returns: Latest procurement suggestion for a specific product

**Example:**
```
GET /api/procurement/suggestions/p1
```

---

## 10. EXECUTIVE SUMMARY & DASHBOARDS

### Get Executive Summary
```
GET /api/executive-summary
```
Returns: High-level KPIs, financial impact, cost-of-delay translator

**Response:**
```json
{
  "status": "success",
  "summary": "Supply chain health: MODERATE RISK. 2 supplier delays affecting 1 SKU. 2 products trending toward stockout in <7 days. ₹125,000 in pending orders at risk. Potential revenue loss if not resolved: ₹1,250. 2 active mitigation recommendations pending execution.",
  "kpis": {
    "active_issues": {
      "delayed_shipments": 2,
      "shortage_forecasts": 2,
      "active_anomalies": 1,
      "active_recommendations": 2,
      "inventory_at_risk": 1
    },
    "financial_impact": {
      "pending_orders_value": 125000,
      "potential_revenue_loss": 1250,
      "cost_of_delay_per_day": 1250,
      "cost_of_delay_per_hour": 52.08
    },
    "timeline": {
      "estimated_recovery_days": 3.2,
      "recovery_eta": "2024-01-22T14:30:00"
    }
  },
  "cost_of_delay_translator": {
    "narrative": "If current delays aren't resolved: ₹52.08/hour or ₹1,250/day in lost revenue. Over 7 days: ₹8,750. This assumes 2 recommendations are NOT executed.",
    "hourly_cost": 52.08,
    "daily_cost": 1250,
    "weekly_cost": 8750,
    "recommendation_impact": "Executing 2 recommendations could reduce this by 40-60%"
  }
}
```

### Get Dashboard Snapshot
```
GET /api/dashboard/snapshot
```
Returns: Lightweight snapshot for dashboard widget

**Response:**
```json
{
  "status": "success",
  "health_status": "WARNING",
  "status_color": "ORANGE",
  "metrics": {
    "delayed_shipments": 2,
    "shortage_forecasts": 2,
    "pending_orders_at_risk": 5,
    "total_at_risk_value": 125000
  },
  "last_updated": "2024-01-19T14:30:00"
}
```

---

## 11. NATURAL LANGUAGE QUERY (NLQ) AGENT

### Post NLQ Query
```
POST /api/chat/query
```
Takes natural language query and returns AI-reasoned answer with multi-step reasoning

**Request Body:**
```json
{
  "user_query": "Which products are at risk of stockout in the next 7 days?"
}
```

**Response:**
```json
{
  "status": "success",
  "user_query": "Which products are at risk of stockout in the next 7 days?",
  "intent": "shortage_analysis",
  "reasoning_trace": [
    "Step 1: Classifying query intent...",
    "Step 2: Intent detected: shortage_analysis",
    "Step 3: Selecting appropriate tools...",
    "Step 4: Executing tools and gathering data...",
    "Step 5: Synthesizing response with reasoning..."
  ],
  "tools_available": ["get_inventory_status", "get_shortage_forecast", "get_supplier_performance", "get_shipment_status", "get_cascade_impact", "get_anomalies", "get_allocation_priority"],
  "response": "Based on current demand patterns and inventory, 2 products are at risk of stockout within 7 days. Products most at risk: p1, p3. Recommend immediate reorder from high-reliability suppliers.",
  "message_id": "msg123"
}
```

### Example NLQ Queries
- "Which products are at risk of stockout?"
- "What's the impact of the Supplier A delay?"
- "Who are the best suppliers?"
- "How should we allocate inventory?"
- "What demand spikes are happening?"

### Get Chat History
```
GET /api/chat/history?limit=10
```
Returns: Recent chat messages and responses

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "history": [
    {
      "message_id": "msg1",
      "user_query": "Which products are at risk?",
      "bot_response": "2 products are at risk of stockout...",
      "created_at": "2024-01-19T10:30:00"
    }
  ]
}
```

---

## 12. SEED / DEMO DATA

### Initialize Demo Data
```
POST /api/seed
```
Seeds realistic test data for demo and testing

**Response:**
```json
{
  "status": "success",
  "message": "Database seeded successfully",
  "counts": {
    "suppliers": 5,
    "warehouses": 3,
    "products": 8,
    "demand_history": 720,
    "purchase_orders": 12,
    "shipments": 10,
    "customer_orders": 13,
    "external_signals": 5,
    "anomalies": 2,
    "forecasts": 8
  }
}
```

### Trigger Demo Scenario
```
POST /api/simulate/trigger-delay
```
Triggers a realistic demo disruption for live presentation

**Response:**
```json
{
  "status": "success",
  "scenario": "Supplier A 4-day delay on Circuit Board",
  "shipment_affected": "ship1",
  "product_affected": "p1",
  "customer_orders_at_risk": 5,
  "revenue_at_risk": 125000,
  "message": "Demo scenario triggered. Check GET /api/shipments/delays to see the impact"
}
```

---

## Error Responses

All endpoints return error responses in this format:

```json
{
  "status": "error",
  "message": "Description of the error",
  "detail": "Additional details if applicable"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Not found (product/supplier not found)
- `500` - Server error

---

## Testing the APIs

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Modify parameters if needed
5. Click "Execute"

### Using cURL

**Get all inventory:**
```bash
curl http://localhost:8000/api/inventory
```

**Get shortage forecast:**
```bash
curl http://localhost:8000/api/inventory/p1/forecast
```

**Post NLQ query:**
```bash
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"user_query":"Which products are at risk?"}'
```

**Trigger demo:**
```bash
curl -X POST http://localhost:8000/api/simulate/trigger-delay
```

---

## Phase Completion Status

✅ Phase 0 - Infrastructure Setup  
✅ Phase 1 - Database Schema & Seeding  
✅ Phase 2 - Data Monitoring & Prediction Engine  
✅ Phase 3 - Weather API Integration (stub)  
✅ Phase 4 - Demo Trigger Mechanism  
✅ Phase 5 - Supplier Scoring  
✅ Phase 6 - Recommendations Engine  
✅ Phase 7 - Allocation & Procurement  
✅ Phase 8 - Executive Summary & Dashboard  
✅ Phase 9 - Chat/NLQ Agent (with tool-calling architecture)  

**All 15 API endpoints fully functional and documented.**
