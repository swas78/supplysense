"""
Dashboard overview endpoint (aggregation layer)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (
    InventorySnapshot, DemandHistory, Shipment, Supplier, CustomerOrder, Product
)
from datetime import datetime, timedelta
import statistics

router = APIRouter()

@router.get("/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    """
    GET /api/dashboard/overview
    Returns: 7-day lookahead + today's snapshot aggregated data
    """
    now = datetime.utcnow()
    seven_days_from_now = now + timedelta(days=7)
    
    # Get all inventory snapshots
    inventory = db.query(InventorySnapshot).all()
    
    high_risk_skus = []
    medium_risk_skus = []
    low_risk_skus = []
    
    for inv in inventory:
        # Get demand forecast
        thirty_days_ago = now - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == inv.product_id,
            DemandHistory.warehouse_id == inv.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        
        if not demand_records:
            continue
        
        units_sold = [d.units_sold for d in demand_records]
        avg_daily_demand = statistics.mean(units_sold)
        
        if avg_daily_demand > 0:
            days_to_stockout = inv.stock_on_hand / avg_daily_demand
        else:
            days_to_stockout = 999
        
        sku_info = {
            "product_id": inv.product_id,
            "product_name": inv.product.name,
            "warehouse_name": inv.warehouse.name,
            "current_stock": inv.stock_on_hand,
            "days_to_stockout": round(days_to_stockout, 1),
            "reorder_point": inv.reorder_point
        }
        
        if days_to_stockout < 7:
            high_risk_skus.append(sku_info)
        elif days_to_stockout < 14:
            medium_risk_skus.append(sku_info)
        else:
            low_risk_skus.append(sku_info)
    
    # Get delayed shipments
    delayed_shipments = db.query(Shipment).filter(
        Shipment.current_eta > Shipment.original_eta
    ).all()
    
    delay_count = len(delayed_shipments)
    
    # Get pending customer orders
    pending_orders = db.query(CustomerOrder).filter_by(status="pending").all()
    total_pending_value = sum(o.order_value for o in pending_orders)
    
    # Get average supplier reliability
    suppliers = db.query(Supplier).all()
    avg_supplier_ontime = (
        statistics.mean([s.on_time_rate for s in suppliers])
        if suppliers else 0
    )
    
    # Build response
    return {
        "status": "success",
        "timestamp": now.isoformat(),
        "dashboard": {
            "view_type": "7_day_lookahead",
            "metrics": {
                "high_risk_skus_count": len(high_risk_skus),
                "medium_risk_skus_count": len(medium_risk_skus),
                "delayed_shipments_count": delay_count,
                "pending_orders_count": len(pending_orders),
                "total_pending_order_value": round(total_pending_value, 2),
                "avg_supplier_ontime_rate": round(avg_supplier_ontime, 2)
            },
            "skus_at_risk_next_7_days": {
                "high_risk": high_risk_skus[:5],  # Top 5
                "medium_risk": medium_risk_skus[:5],
                "count_high": len(high_risk_skus),
                "count_medium": len(medium_risk_skus)
            },
            "disruptions": {
                "delayed_shipments": delay_count,
                "at_risk_orders": len([o for o in pending_orders if o.status == "at_risk"]),
                "status": "ACTIVE" if delay_count > 0 else "STABLE"
            },
            "today_snapshot": {
                "current_high_risk": len([s for s in high_risk_skus if s["days_to_stockout"] <= 1]),
                "current_delayed": delay_count,
                "critical_alerts": len(high_risk_skus)
            }
        }
    }
