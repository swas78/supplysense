# SupplySense Backend — Complete Implementation Plan (Remaining Work)

**Current Status:** Phase 4 Complete (8/19 features, 8/15 endpoints)
**Goal:** 19/19 features, 15/15 endpoints fully working

---

## 📋 BREAKDOWN OF REMAINING WORK

### **Phase 5: Swastik's Work (Chat/NLQ Agent + Enhancements)**

#### 5a. Chat/NLQ Agent with LLM Tool-Calling (4-5 hours)
**Endpoint:** `POST /api/chat`

**What needs to be done:**
1. Set up Anthropic Claude API
2. Define tools that the LLM can call:
   - `get_inventory_status(sku_id)` → calls `/api/inventory/{sku_id}/forecast`
   - `get_all_inventory()` → calls `/api/inventory`
   - `get_delayed_shipments()` → calls `/api/shipments/delays`
   - `get_shipment_impact(shipment_id)` → calls `/api/shipments/{id}/impact`
   - `get_anomalies()` → calls `/api/anomalies`
   - `get_supplier_scores()` → calls Tanishka's endpoint (stub for now)
   - `get_recommendations()` → calls Tanishka's endpoint (stub for now)
3. Implement tool-calling loop:
   - User asks question
   - LLM decides which tools to call
   - Execute tools
   - Return results to LLM
   - LLM synthesizes answer
4. Store reasoning trace
5. Return answer + tools_used + reasoning_steps

**Example conversation:**
```
User: "What's causing today's biggest disruption?"

LLM reasoning:
  1. Call get_delayed_shipments() → Finds Supplier A delayed 4 days
  2. Call get_shipment_impact(shipment_001) → Gets cascade impact (2 orders, ₹87.5K)
  3. Call get_inventory_status(widget_a) → Gets 3.2 days to stockout
  4. Call get_anomalies() → Gets promo spike on Jan 20-25

LLM synthesizes:
"Your biggest disruption is a 4-day delay from Supplier A affecting Widget A.
 This puts 2 customer orders at risk (₹87,500 value) because Widget A stock
 will run out in 3.2 days. The root cause: a promotional campaign on Jan 20-25
 doubled demand, depleting safety stock below normal levels."
```

**Implementation:**
```python
# routes/chat.py - Full implementation

import anthropic
import json
from typing import Any

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def define_tools():
    """Define all available tools for the LLM"""
    return [
        {
            "name": "get_inventory_status",
            "description": "Get current inventory and shortage forecast for a specific SKU",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sku_id": {"type": "string", "description": "Product SKU ID"}
                },
                "required": ["sku_id"]
            }
        },
        {
            "name": "get_all_inventory",
            "description": "Get inventory status for all products across all warehouses",
            "input_schema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_delayed_shipments",
            "description": "Get list of currently delayed shipments",
            "input_schema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_shipment_impact",
            "description": "Get cascade impact of a specific shipment delay",
            "input_schema": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string"}
                },
                "required": ["shipment_id"]
            }
        },
        {
            "name": "get_anomalies",
            "description": "Get detected demand anomalies and their causes",
            "input_schema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_supplier_scores",
            "description": "Get supplier reliability scores and recovery resilience",
            "input_schema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_recommendations",
            "description": "Get active recommendations for mitigation actions",
            "input_schema": {"type": "object", "properties": {}}
        }
    ]

async def execute_tool(tool_name: str, tool_input: dict, db: Session):
    """Execute a tool by calling the appropriate API endpoint"""
    # Implementation: Call your own endpoints
    # This is internal, not HTTP calls
    pass

async def chat_agent_impl(question: str, db: Session):
    """Full tool-calling chat agent implementation"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    tools = define_tools()
    messages = [{"role": "user", "content": question}]
    reasoning_steps = []
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        
        # If LLM wants to call tools
        if response.stop_reason == "tool_use":
            assistant_content = response.content
            messages.append({"role": "assistant", "content": assistant_content})
            
            tool_results = []
            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    
                    # Execute the tool
                    result = await execute_tool(tool_name, tool_input, db)
                    
                    reasoning_steps.append({
                        "tool": tool_name,
                        "input": tool_input,
                        "result": result
                    })
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })
            
            messages.append({"role": "user", "content": tool_results})
        else:
            # LLM is done; extract answer
            final_answer = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    final_answer += block.text
            
            # Save to database
            chat_log = ChatLog(
                question=question,
                answer=final_answer,
                tools_used=json.dumps([s["tool"] for s in reasoning_steps]),
                reasoning_steps=json.dumps(reasoning_steps),
                created_at=datetime.utcnow()
            )
            db.add(chat_log)
            db.commit()
            
            return {
                "answer": final_answer,
                "tools_used": [s["tool"] for s in reasoning_steps],
                "reasoning_steps": reasoning_steps
            }
```

---

### **Phase 6: Tanishka's Work (Supplier Scoring + Recommendations)**

#### 6a. Supplier Reliability Scoring Endpoint (2 hours)
**Endpoint:** `GET /api/suppliers/scores`

**What needs to be done:**
1. Fetch all suppliers from DB
2. Calculate reliability_score for each:
   - Formula: `0.5*on_time_rate + 0.25*(1/lead_time_factor) + 0.25*quality_rate`
3. Include recovery_resilience_score (already seeded)
4. Return ranked list with reasoning

**Response structure:**
```json
{
  "status": "success",
  "suppliers": [
    {
      "supplier_id": "sup_001",
      "supplier_name": "Supplier B",
      "reliability_score": 0.92,
      "on_time_rate": 0.96,
      "avg_lead_time_days": 5,
      "quality_rate": 0.98,
      "recovery_resilience_score": 1.5,
      "risk_level": "LOW_RISK",
      "reasoning": "Excellent on-time delivery (96%), short lead time (5 days), high quality (98%)"
    },
    {
      "supplier_id": "sup_002",
      "supplier_name": "Supplier A",
      "reliability_score": 0.71,
      "on_time_rate": 0.71,
      "avg_lead_time_days": 10,
      "quality_rate": 0.92,
      "recovery_resilience_score": 2.0,
      "risk_level": "MEDIUM_RISK",
      "reasoning": "Moderate on-time rate (71%), acceptable quality (92%), recovers quickly (2 days)"
    }
  ]
}
```

---

#### 6b. Alternate Supplier Recommendation (2-3 hours)
**Endpoint:** `GET /api/recommendations`

**What needs to be done:**
1. Detect disruptions:
   - Delayed shipments
   - Predicted shortages
   - Low supplier reliability
2. For each disruption, find alternate suppliers:
   - Check `product_categories` for substitutability
   - Score alternatives based on reliability
   - Prefer suppliers with faster lead times
3. Calculate cost-of-delay:
   - at_risk_order_value * (delay_days / 30)
4. Generate reasoning text
5. Store in `recommendations` table

**Response structure:**
```json
{
  "status": "success",
  "recommendations": [
    {
      "recommendation_id": "rec_001",
      "trigger_type": "shipment_delay",
      "trigger_ref_id": "ship_001",
      "problem": "Supplier A delayed 4 days, Widget A supply at risk",
      "recommended_action": "Switch to Supplier B for expedited restock",
      "reasoning_text": "Supplier B has 96% on-time rate vs Supplier A's 71%. Lead time: 5 days vs 10 days. Recovery resilience: 1.5 days (faster bounce-back).",
      "estimated_cost_impact_inr": 87500,
      "confidence_score": 0.92,
      "status": "active"
    }
  ]
}
```

---

#### 6c. Inventory Allocation Prioritization (2 hours)
**Endpoint:** `GET /api/allocation/{product_id}`

**What needs to be done:**
1. Get product + available stock
2. Get all pending orders for this product
3. Rank orders by priority:
   - Order value (higher = earlier)
   - Days until required (sooner = earlier)
   - Customer tier (premium = earlier)
4. Calculate fulfillment plan:
   - Which orders get fulfilled
   - Which get partial
   - Which go unfulfilled
5. Return ranking with reasoning

**Response structure:**
```json
{
  "product_id": "prod_001",
  "product_name": "Widget A",
  "available_stock": 200,
  "total_pending_demand": 350,
  "shortage": 150,
  "allocation_plan": [
    {
      "order_id": "ord_001",
      "customer_id": "cust_A",
      "requested_quantity": 200,
      "allocated_quantity": 200,
      "priority_rank": 1,
      "priority_score": 95.5,
      "reasoning": "Order value: ₹50K (highest), Due: 2 days (urgent), SLA: Premium"
    },
    {
      "order_id": "ord_002",
      "customer_id": "cust_B",
      "requested_quantity": 150,
      "allocated_quantity": 0,
      "priority_rank": 2,
      "priority_score": 62.3,
      "reasoning": "Order value: ₹37.5K, Due: 4 days, SLA: Standard"
    }
  ],
  "summary": "200 units allocated. Order ORD_001 fulfilled completely. Order ORD_002 unfulfilled (wait for restock or switch to alternate supplier)."
}
```

---

#### 6d. Procurement Suggestions (1.5 hours)
**Endpoint:** `GET /api/procurement/suggestions`

**What needs to be done:**
1. Get all forecasts showing shortages
2. For each shortage:
   - Determine reorder quantity (days_to_stockout * avg_daily_demand + safety_stock)
   - Find best supplier (reliability + lead time)
   - Calculate deadline (today + lead_time - 2 days buffer)
3. Return ranked by urgency

**Response structure:**
```json
{
  "status": "success",
  "suggestions": [
    {
      "product_id": "prod_001",
      "product_name": "Widget A",
      "current_stock": 80,
      "daily_demand": 25,
      "days_to_stockout": 3.2,
      "suggested_quantity": 300,
      "recommended_supplier_id": "sup_002",
      "recommended_supplier_name": "Supplier B",
      "supplier_lead_time_days": 5,
      "deadline_to_order": "2024-01-18",
      "urgency": "CRITICAL",
      "reasoning": "Stock will run out in 3.2 days. Reorder 300 units (covers 12 days). Supplier B delivery in 5 days, deadline is Jan 18.",
      "estimated_cost": 150000
    }
  ]
}
```

---

#### 6e. Auto-Drafted Dealer Messages (LLM, 1.5 hours)
**Endpoint:** `POST /api/recommendations/{rec_id}/message`

**What needs to be done:**
1. Get recommendation details
2. Use Claude LLM to draft professional message
3. Message types:
   - Delay notice to customer
   - Expedite request to new supplier
   - Demand forecast update
4. Store in `dealer_messages` table

**Implementation:**
```python
@router.post("/recommendations/{rec_id}/message")
async def generate_dealer_message(rec_id: str, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter_by(id=rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Determine message type
    if rec.trigger_type == "shipment_delay":
        template = "expedite_to_supplier"
    else:
        template = "customer_communication"
    
    # Get context data
    # ...
    
    # Call Claude
    prompt = f"""
    Generate a professional {template} message.
    Problem: {rec.problem}
    Recommendation: {rec.recommended_action}
    
    Keep it under 150 words. Be professional and actionable.
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    message_text = response.content[0].text
    
    # Store in DB
    dealer_msg = DealerMessage(
        recommendation_id=rec_id,
        template_type=template,
        generated_text=message_text,
        recipient=rec.recipient,
        created_at=datetime.utcnow()
    )
    db.add(dealer_msg)
    db.commit()
    
    return {
        "status": "success",
        "message": message_text,
        "recipient": rec.recipient
    }
```

---

#### 6f. Executive Summary (LLM, 1.5 hours)
**Endpoint:** `GET /api/summary/executive`

**What needs to be done:**
1. Gather all data:
   - High-risk SKUs (shortages)
   - Overstock items
   - Delayed shipments
   - Active anomalies
   - Recommendations
2. Call Claude LLM
3. Generate plain-English summary with:
   - Top 3 risks
   - Financial impact
   - Mitigation strategies
   - Next steps

**Implementation:**
```python
@router.get("/summary/executive")
async def get_executive_summary(db: Session = Depends(get_db)):
    # Gather data
    high_risk = get_high_risk_skus(db)
    overstock = get_overstock_items(db)
    delays = get_delayed_shipments(db)
    anomalies = get_anomalies(db)
    recs = get_recommendations(db)
    
    # Build context
    context = f"""
    HIGH-RISK INVENTORY:
    {format_risk_list(high_risk)}
    
    OVERSTOCK ITEMS:
    {format_overstock_list(overstock)}
    
    DELAYED SHIPMENTS:
    {format_delays(delays)}
    
    ANOMALIES:
    {format_anomalies(anomalies)}
    
    RECOMMENDATIONS:
    {format_recommendations(recs)}
    """
    
    # Call Claude
    prompt = f"""
    Generate an executive summary of supply chain status for today.
    Include: top risks, financial impact, recommended actions, next steps.
    Keep to 3-4 paragraphs, written for a CFO.
    
    {context}
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary_text = response.content[0].text
    
    return {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary_text,
        "risk_count": len(high_risk),
        "overstock_count": len(overstock),
        "delayed_count": len(delays)
    }
```

---

### **Phase 7: Both Tracks - Dashboard Enhancement (1 hour)**

#### 7a. Complete Dashboard Aggregation
**Endpoint:** `GET /api/dashboard/overview`

Enhance with:
- 7-day lookahead view (default)
- Today's snapshot view
- Active disruption count
- Risk distribution
- Quick metrics summary

---

## 📊 IMPLEMENTATION SEQUENCE

### **CRITICAL PATH (Must do in order)**

1. **Tanishka Phase 6a: Supplier Scoring** (2h)
   - No dependencies
   - Unblocks recommendations

2. **Tanishka Phase 6b: Recommendations** (2-3h)
   - Depends on: Supplier scoring
   - Unblocks: Dealer messages, chat agent

3. **Tanishka Phase 6c: Allocation** (2h)
   - Depends on: Forecasts (already ready)
   - Independent of recommendations

4. **Tanishka Phase 6d: Procurement** (1.5h)
   - Depends on: Forecasts, supplier scoring
   - Independent of recommendations

5. **Swastik Phase 5a: Chat Agent** (4-5h)
   - Depends on: All above (calls them as tools)
   - Should start after steps 1-2 are done

6. **Tanishka Phase 6e: Dealer Messages** (1.5h)
   - Depends on: Recommendations

7. **Tanishka Phase 6f: Executive Summary** (1.5h)
   - Depends on: All above (aggregates them)

8. **Both Phase 7a: Dashboard Polish** (1h)
   - Depends on: Executive summary

---

## 🎯 TOTAL TIME ESTIMATE

| Phase | Owner | Hours | Total |
|-------|-------|-------|-------|
| 5a | Swastik | 4-5 | 4-5 |
| 6a | Tanishka | 2 | 2 |
| 6b | Tanishka | 2-3 | 2-3 |
| 6c | Tanishka | 2 | 2 |
| 6d | Tanishka | 1.5 | 1.5 |
| 5a (chat) | Swastik | 4-5 | 4-5 |
| 6e | Tanishka | 1.5 | 1.5 |
| 6f | Tanishka | 1.5 | 1.5 |
| 7a | Both | 1 | 1 |

**Total Backend Remaining: 18-21 hours**

---

## ✅ SUCCESS CRITERIA

### Phase 5 (Swastik - Chat Agent)
- [ ] Chat agent calls at least 3 tools successfully
- [ ] Reasoning trace shows all tools called
- [ ] Answer synthesizes data from multiple sources
- [ ] Test: "What's the biggest disruption?" → Returns correct answer

### Phase 6a (Supplier Scoring)
- [ ] All 5 suppliers scored
- [ ] Scores between 0-1
- [ ] Highest score = Supplier B (0.92+)
- [ ] Lowest score = Supplier D (0.60-0.70)

### Phase 6b (Recommendations)
- [ ] At least 1 recommendation generated for seeded delay
- [ ] Includes reasoning + cost impact
- [ ] Recommended supplier has higher score than original

### Phase 6c (Allocation)
- [ ] Widget A (limited stock) shows 2-3 orders
- [ ] Orders ranked by priority
- [ ] Some orders fulfilled, some unfulfilled

### Phase 6d (Procurement)
- [ ] Widget A shows as CRITICAL
- [ ] Suggested quantity covers demand + safety stock
- [ ] Recommended supplier has short lead time

### Phase 6e (Dealer Messages)
- [ ] Message is professional and actionable
- [ ] Under 150 words
- [ ] References specific product/supplier

### Phase 6f (Executive Summary)
- [ ] Summary includes top 3 risks
- [ ] Financial impact mentioned
- [ ] Actionable next steps
- [ ] 3-4 paragraphs, CFO-friendly tone

---

## 🚀 START IMPLEMENTING NOW

I'll start with Phase 6a (Supplier Scoring) since it has no dependencies, then move to 6b, 6c, 6d.

