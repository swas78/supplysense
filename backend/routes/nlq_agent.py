"""
Natural Language Query agent with tool-calling and reasoning
Powered by Google Antigravity SDK
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from models import (
    ChatHistory, InventorySnapshot, Forecast, Supplier, Shipment, 
    CustomerOrder, PurchaseOrder, Anomaly, DemandHistory, Product, 
    Warehouse, Recommendation, DealerMessage, ProcurementSuggestion
)
from datetime import datetime, timedelta
from pydantic import BaseModel
import json
import statistics

from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

router = APIRouter()

class ChatMessage(BaseModel):
    user_query: str
    conversation_id: str = "default_session"

# Define Tools with descriptive docstrings
def get_inventory_status(product_id: str) -> str:
    """Get current inventory levels for a specific product across all warehouses.
    
    Args:
        product_id: The SKU/product ID to check.
    """
    db = next(get_db())
    inv = db.query(InventorySnapshot).filter_by(product_id=product_id).all()
    if not inv:
        return f"Product {product_id} not found in inventory."
    
    results = [{"warehouse_id": i.warehouse_id, "stock_on_hand": i.stock_on_hand} for i in inv]
    return json.dumps({"product_id": product_id, "warehouses": results})

def get_shortage_forecast(product_id: str) -> str:
    """Get shortage prediction and days until stockout for a product.
    
    Args:
        product_id: The SKU/product ID to forecast.
    """
    db = next(get_db())
    forecast = db.query(Forecast).filter_by(product_id=product_id).first()
    if forecast:
        return json.dumps({
            "product_id": product_id,
            "days_to_stockout": forecast.predicted_days_to_stockout,
            "confidence_score": forecast.confidence_score
        })
    return f"No forecast available for {product_id}."

def get_supplier_performance(supplier_id: str) -> str:
    """Get reliability score, recovery resilience, and on-time delivery rate for a supplier.
    
    Args:
        supplier_id: The supplier ID.
    """
    db = next(get_db())
    supplier = db.query(Supplier).filter_by(id=supplier_id).first()
    if supplier:
        return json.dumps({
            "supplier_id": supplier_id,
            "supplier_name": supplier.name,
            "reliability_score": supplier.reliability_score,
            "recovery_resilience_score": supplier.recovery_resilience_score,
            "on_time_rate": supplier.on_time_rate,
            "avg_lead_time_days": supplier.avg_lead_time_days
        })
    return f"Supplier {supplier_id} not found."

def get_shipment_status(status_filter: str = "all") -> str:
    """Get status and ETA of pending shipments.
    
    Args:
        status_filter: Filter by status: 'delayed', 'on_time', or 'all'. Defaults to 'all'.
    """
    db = next(get_db())
    query = db.query(Shipment)
    
    if status_filter == "delayed":
        query = query.filter(Shipment.current_eta > Shipment.original_eta)
    elif status_filter == "on_time":
        query = query.filter(Shipment.current_eta <= Shipment.original_eta)
        
    shipments = query.all()
    results = []
    for s in shipments:
        results.append({
            "shipment_id": s.id,
            "status": "delayed" if s.current_eta > s.original_eta else "on_time",
            "original_eta": s.original_eta.isoformat(),
            "current_eta": s.current_eta.isoformat()
        })
    
    return json.dumps({"count": len(results), "shipments": results})

def get_cascade_impact(shipment_id: str) -> str:
    """Get customer orders affected by a specific shipment delay (cascade analysis).
    
    Args:
        shipment_id: The shipment ID to analyze.
    """
    db = next(get_db())
    shipment = db.query(Shipment).filter_by(id=shipment_id).first()
    if not shipment:
        return f"Shipment {shipment_id} not found."
    
    po = shipment.purchase_order
    affected_orders = db.query(CustomerOrder).filter(
        CustomerOrder.product_id == po.product_id,
        CustomerOrder.warehouse_id == po.warehouse_id,
        CustomerOrder.status == "pending"
    ).all()
    
    total_value = sum(o.order_value for o in affected_orders)
    
    results = [{"order_id": o.id, "order_value": o.order_value} for o in affected_orders]
    return json.dumps({
        "shipment_id": shipment_id,
        "affected_customer_orders": len(results),
        "total_at_risk_value": total_value,
        "orders": results
    })

def get_anomalies(product_id: str = None) -> str:
    """Get demand anomalies and spikes with root cause attribution.
    
    Args:
        product_id: Optional product ID to filter anomalies.
    """
    db = next(get_db())
    query = db.query(Anomaly).filter(Anomaly.status == "active")
    if product_id:
        query = query.filter_by(product_id=product_id)
        
    anomalies = query.all()
    results = []
    for a in anomalies:
        results.append({
            "anomaly_id": a.id,
            "product_id": a.product_id,
            "anomaly_type": a.anomaly_type,
            "attributed_cause": a.attributed_cause,
            "confidence": a.confidence_score
        })
    return json.dumps({"count": len(results), "anomalies": results})

def get_allocation_priority(product_id: str) -> str:
    """Get priority ranking for pending orders when stock is limited.
    
    Args:
        product_id: The product ID to analyze allocation.
    """
    db = next(get_db())
    inv = db.query(InventorySnapshot).filter_by(product_id=product_id).first()
    if not inv:
        return f"Product {product_id} not found."
    
    pending = db.query(CustomerOrder).filter(
        CustomerOrder.product_id == product_id,
        CustomerOrder.status == "pending"
    ).all()
    
    total_demand = sum(o.quantity for o in pending)
    shortage = max(0, total_demand - inv.stock_on_hand)
    
    return json.dumps({
        "product_id": product_id,
        "available_stock": inv.stock_on_hand,
        "pending_orders": len(pending),
        "total_demand": total_demand,
        "shortage": shortage
    })

def get_overstock_status(product_id: str = None) -> str:
    """Get products with excess stock and their working capital impact.
    
    Args:
        product_id: Optional product ID to filter for a specific product.
    """
    db = next(get_db())
    query = db.query(InventorySnapshot)
    if product_id:
        query = query.filter_by(product_id=product_id)
        
    snapshots = query.all()
    overstock_items = []
    
    for snapshot in snapshots:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == snapshot.product_id,
            DemandHistory.warehouse_id == snapshot.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        
        if not demand_records:
            continue
            
        units_sold = [d.units_sold for d in demand_records]
        avg_daily_demand = statistics.mean(units_sold)
        demand_justified_stock = avg_daily_demand * 14
        
        if snapshot.stock_on_hand > demand_justified_stock * 1.5:
            excess = snapshot.stock_on_hand - int(demand_justified_stock)
            overstock_items.append({
                "product_id": snapshot.product_id,
                "warehouse_id": snapshot.warehouse_id,
                "current_stock": snapshot.stock_on_hand,
                "excess_units": excess
            })
            
    return json.dumps({"count": len(overstock_items), "overstock_items": overstock_items})

def get_7_day_lookahead() -> str:
    """Get aggregated metrics for the next 7 days, including high risk stockouts and delayed shipments."""
    db = next(get_db())
    now = datetime.utcnow()
    
    delayed_shipments = db.query(Shipment).filter(Shipment.current_eta > Shipment.original_eta).all()
    pending_orders = db.query(CustomerOrder).filter_by(status="pending").all()
    
    high_risk_skus = []
    inventory = db.query(InventorySnapshot).all()
    for inv in inventory:
        thirty_days_ago = now - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == inv.product_id,
            DemandHistory.warehouse_id == inv.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        if demand_records:
            avg_daily_demand = statistics.mean([d.units_sold for d in demand_records])
            if avg_daily_demand > 0:
                days_to_stockout = inv.stock_on_hand / avg_daily_demand
                if days_to_stockout < 7:
                    high_risk_skus.append({
                        "product_id": inv.product_id,
                        "days_to_stockout": round(days_to_stockout, 1)
                    })
                    
    return json.dumps({
        "high_risk_skus_next_7_days": len(high_risk_skus),
        "delayed_shipments_count": len(delayed_shipments),
        "pending_orders_count": len(pending_orders),
        "total_pending_order_value": sum(o.order_value for o in pending_orders)
    })

def get_procurement_recommendations(product_id: str) -> str:
    """Get reorder quantity recommendations for a product to prevent stockouts.
    
    Args:
        product_id: The product ID to reorder.
    """
    db = next(get_db())
    inv = db.query(InventorySnapshot).filter_by(product_id=product_id).first()
    if not inv:
        return f"Product {product_id} not found."
        
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    demand_records = db.query(DemandHistory).filter(
        DemandHistory.product_id == product_id,
        DemandHistory.date >= thirty_days_ago
    ).all()
    
    avg_daily_demand = statistics.mean([d.units_sold for d in demand_records]) if demand_records else 0
    target_stock = avg_daily_demand * 30 # 30 days of cover
    
    pending_po = db.query(PurchaseOrder).filter(
        PurchaseOrder.product_id == product_id,
        PurchaseOrder.status == "pending"
    ).all()
    
    incoming_stock = sum(po.quantity for po in pending_po)
    
    suggested_qty = max(0, int(target_stock - inv.stock_on_hand - incoming_stock))
    
    sugg = ProcurementSuggestion(
        product_id=product_id,
        suggested_quantity=suggested_qty,
        reasoning=f"Target stock: {target_stock}, On hand: {inv.stock_on_hand}, Incoming: {incoming_stock}"
    )
    db.add(sugg)
    db.commit()
    
    return json.dumps({
        "product_id": product_id,
        "suggested_quantity": suggested_qty,
        "incoming_stock": incoming_stock,
        "target_stock": target_stock
    })

def get_alternate_suppliers(product_id: str) -> str:
    """Get recommended alternate suppliers for a product based on reliability and recovery resilience.
    
    Args:
        product_id: The product ID to source.
    """
    db = next(get_db())
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        return f"Product {product_id} not found."
        
    suppliers = db.query(Supplier).order_by(
        desc(Supplier.reliability_score),
        Supplier.recovery_resilience_score
    ).all()
    
    top_suppliers = []
    for s in suppliers[:3]:
        top_suppliers.append({
            "supplier_id": s.id,
            "name": s.name,
            "reliability_score": s.reliability_score,
            "recovery_resilience_score": s.recovery_resilience_score,
            "on_time_rate": s.on_time_rate
        })
        
    rec = Recommendation(
        trigger_type="alternate_supplier",
        trigger_ref_id=product_id,
        recommended_action=f"Switch to {top_suppliers[0]['name'] if top_suppliers else 'None'}",
        reasoning_text=f"Top alternate supplier based on {top_suppliers[0]['reliability_score']} reliability" if top_suppliers else ""
    )
    db.add(rec)
    db.commit()
        
    return json.dumps({"alternate_suppliers": top_suppliers})

def draft_supplier_message(recommendation_id: str, template_type: str) -> str:
    """Draft a communication message to a supplier/dealer.
    
    Args:
        recommendation_id: The ID of the recommendation to base the message on.
        template_type: Type of message, e.g., 'delay_notice', 'expedite_request'
    """
    db = next(get_db())
    
    message = ""
    if template_type == "delay_notice":
        message = f"URGENT: Notice of expected delay. Please review recommendation {recommendation_id}."
    elif template_type == "expedite_request":
        message = f"URGENT: Please expedite our upcoming orders based on recommendation {recommendation_id}."
    else:
        message = f"General update regarding recommendation {recommendation_id}."
        
    dealer_msg = DealerMessage(
        recommendation_id=recommendation_id,
        template_type=template_type,
        generated_text=message,
        recipient="Supplier/Dealer"
    )
    db.add(dealer_msg)
    db.commit()
    
    return json.dumps({"status": "success", "drafted_message": message, "message_id": dealer_msg.id})

# --- NEW EXECUTION TOOLS ---
def dispatch_purchase_order(product_id: str, quantity: int) -> str:
    """Execute a purchase order for a given product and quantity.
    
    Args:
        product_id: The product ID to order.
        quantity: The number of units to order.
    """
    db = next(get_db())
    po = PurchaseOrder(
        product_id=product_id,
        supplier_id="SUP-001",
        warehouse_id="WH-001",
        quantity=quantity,
        status="pending",
        order_date=datetime.utcnow()
    )
    db.add(po)
    db.commit()
    return json.dumps({"status": "success", "message": f"Purchase order {po.id} for {quantity} units of {product_id} dispatched."})

def send_supplier_message(message_id: str) -> str:
    """Send an auto-drafted message to a supplier.
    
    Args:
        message_id: The ID of the drafted message.
    """
    db = next(get_db())
    msg = db.query(DealerMessage).filter_by(id=message_id).first()
    if msg:
        msg.status = "sent"
        db.commit()
        return json.dumps({"status": "success", "message": f"Message {message_id} sent successfully."})
    return json.dumps({"status": "error", "message": f"Message {message_id} not found."})


# Configure the agent
SYSTEM_INSTRUCTION = """
You are SupplySense AI, an autonomous enterprise agent responsible for monitoring supply chain health.
You can execute purchase orders, send emails, and spawn subagents for multi-step audits.
Always use your tools to fetch relevant data before answering a query.
When answering, be professional, concise, and highlight critical issues. Do not hallucinate data.
"""

tools = [
    get_inventory_status,
    get_shortage_forecast,
    get_supplier_performance,
    get_shipment_status,
    get_cascade_impact,
    get_anomalies,
    get_allocation_priority,
    get_overstock_status,
    get_7_day_lookahead,
    get_procurement_recommendations,
    get_alternate_suppliers,
    draft_supplier_message,
    dispatch_purchase_order,
    send_supplier_message
]

# Safety Guardrails
policies = [
    policy.deny(
        "dispatch_purchase_order",
        when=lambda args: int(args.get("quantity", 0)) > 10000,
        name="deny_large_orders",
    ),
    policy.allow_all()
]

@router.post("/chat/query")
async def process_nlq_query(message: ChatMessage, db: Session = Depends(get_db)):
    """
    POST /api/chat/query
    Takes a natural language query and returns an AI-reasoned answer via Google Antigravity SDK.
    """
    user_query = message.user_query
    
    # Store initial chat in database
    chat_msg = ChatHistory(
        user_query=user_query,
        bot_response="",
        reasoning_trace="",
        tools_called=[],
        created_at=datetime.utcnow()
    )
    db.add(chat_msg)
    db.commit()
    
    thoughts = []
    final_response = ""
    
    # Dynamic Agent Config with Persistence and Subagents
    agent_config = LocalAgentConfig(
        system_instructions=SYSTEM_INSTRUCTION,
        tools=tools,
        conversation_id=message.conversation_id,
        save_dir="/tmp/supplysense_agent_memory",
        capabilities=types.CapabilitiesConfig(enable_subagents=True),
        policies=policies
    )
    
    try:
        async with Agent(agent_config) as agent:
            response = await agent.chat(user_query)
            
            # Collect thoughts
            async for thought in response.thoughts:
                thoughts.append(thought)
            
            # Collect final answer
            final_response = await response.text()
            
    except Exception as e:
        final_response = f"Agent encountered an error: {str(e)}"
    
    # Update DB with final response
    chat_msg.bot_response = final_response
    chat_msg.reasoning_trace = json.dumps(thoughts)
    db.commit()
    
    return {
        "status": "success",
        "user_query": user_query,
        "intent": "autonomous_agent",
        "reasoning_trace": thoughts,
        "tools_available": [t.__name__ for t in tools],
        "response": final_response,
        "message_id": chat_msg.id,
        "conversation_id": message.conversation_id
    }

@router.get("/chat/history")
def get_chat_history(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent chat history"""
    messages = db.query(ChatHistory).order_by(
        ChatHistory.created_at.desc()
    ).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(messages),
        "history": [
            {
                "message_id": m.id,
                "user_query": m.user_query,
                "bot_response": m.bot_response,
                "created_at": m.created_at.isoformat()
            }
            for m in reversed(messages)
        ]
    }
