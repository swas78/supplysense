"""
Inventory allocation prioritization endpoint
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import (
    Product, InventorySnapshot, CustomerOrder, AllocationDecision
)
from datetime import datetime
import json

router = APIRouter()

@router.get("/allocation/{product_id}")
def get_allocation_priority(product_id: str, db: Session = Depends(get_db)):
    """
    GET /api/allocation/{product_id}
    Returns: Ranked pending orders with allocation priority when stock is limited
    """
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get all pending orders for this product
    pending_orders = db.query(CustomerOrder).filter(
        CustomerOrder.product_id == product_id,
        CustomerOrder.status == "pending"
    ).all()
    
    if not pending_orders:
        return {
            "status": "success",
            "product_id": product_id,
            "product_name": product.name,
            "message": "No pending orders",
            "allocation_plan": []
        }
    
    # Get total available stock across all warehouses
    inventory = db.query(InventorySnapshot).filter_by(product_id=product_id).all()
    total_available_stock = sum(inv.stock_on_hand for inv in inventory)
    
    # Calculate total pending demand
    total_pending_demand = sum(o.quantity for o in pending_orders)
    
    # Score each order by priority
    order_scores = []
    for order in pending_orders:
        # Priority factors (weighted)
        # 1. Order value (higher = higher priority) - 40%
        value_score = (order.order_value / max([o.order_value for o in pending_orders])) * 40 if pending_orders else 0
        
        # 2. Days until required (sooner = higher priority) - 40%
        days_until_required = (order.required_by_date - datetime.utcnow()).days
        urgency_score = max(0, (7 - days_until_required) / 7 * 40)  # 0-40 points
        
        # 3. Order size (larger = higher priority) - 20%
        size_score = (order.quantity / max([o.quantity for o in pending_orders])) * 20 if pending_orders else 0
        
        total_score = value_score + urgency_score + size_score
        
        order_scores.append({
            "order": order,
            "total_score": total_score,
            "value_score": value_score,
            "urgency_score": urgency_score,
            "size_score": size_score,
            "days_until_required": days_until_required
        })
    
    # Sort by total score (highest first)
    order_scores = sorted(order_scores, key=lambda x: x["total_score"], reverse=True)
    
    # Allocate stock based on ranking
    allocation_plan = []
    remaining_stock = total_available_stock
    
    for rank, item in enumerate(order_scores, 1):
        order = item["order"]
        
        # Allocate what we can
        allocated_qty = min(order.quantity, remaining_stock)
        remaining_stock -= allocated_qty
        
        # Determine status
        if allocated_qty >= order.quantity:
            status = "FULFILLED"
        elif allocated_qty > 0:
            status = "PARTIAL"
        else:
            status = "UNFULFILLED"
        
        # Build reasoning
        reasoning_parts = []
        if item["days_until_required"] <= 2:
            reasoning_parts.append(f"Due in {item['days_until_required']} days (URGENT)")
        else:
            reasoning_parts.append(f"Due in {item['days_until_required']} days")
        reasoning_parts.append(f"Order value: ₹{order.order_value:,.0f}")
        reasoning_parts.append(f"Quantity: {order.quantity} units")
        
        allocation_plan.append({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "requested_quantity": order.quantity,
            "allocated_quantity": allocated_qty,
            "priority_rank": rank,
            "priority_score": round(item["total_score"], 1),
            "status": status,
            "required_by_date": order.required_by_date.isoformat(),
            "days_until_required": item["days_until_required"],
            "order_value": round(order.order_value, 2),
            "reasoning": " | ".join(reasoning_parts)
        })
    
    # Calculate shortage
    shortage = max(0, total_pending_demand - total_available_stock)
    
    # Generate summary
    fulfilled_count = sum(1 for a in allocation_plan if a["status"] == "FULFILLED")
    partial_count = sum(1 for a in allocation_plan if a["status"] == "PARTIAL")
    unfulfilled_count = sum(1 for a in allocation_plan if a["status"] == "UNFULFILLED")
    
    summary = (
        f"Available stock: {total_available_stock} units | "
        f"Total demand: {total_pending_demand} units | "
        f"Shortage: {shortage} units. "
        f"Fulfilled: {fulfilled_count}, Partial: {partial_count}, "
        f"Unfulfilled: {unfulfilled_count}. "
        f"Prioritized by: order value (40%), delivery urgency (40%), order size (20%)."
    )
    
    # Store allocation decision
    alloc_decision = AllocationDecision(
        product_id=product_id,
        available_stock=total_available_stock,
        total_demand=total_pending_demand,
        ranking_json=json.dumps([
            {
                "order_id": a["order_id"],
                "priority_rank": a["priority_rank"],
                "priority_score": a["priority_score"],
                "allocated_qty": a["allocated_quantity"],
                "requested_qty": a["requested_quantity"],
                "status": a["status"]
            }
            for a in allocation_plan
        ]),
        created_at=datetime.utcnow()
    )
    db.add(alloc_decision)
    db.commit()
    
    return {
        "status": "success",
        "product_id": product_id,
        "product_name": product.name,
        "available_stock": total_available_stock,
        "total_pending_demand": total_pending_demand,
        "shortage": shortage,
        "allocation_plan": allocation_plan,
        "summary": summary
    }
