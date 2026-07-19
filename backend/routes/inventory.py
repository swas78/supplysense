"""
Inventory monitoring and forecasting endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import get_db
from models import (
    InventorySnapshot, DemandHistory, Forecast, Product, Warehouse
)
from datetime import datetime, timedelta
import statistics

router = APIRouter()

@router.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    """
    GET /api/inventory
    Returns: list of all SKUs with current stock per warehouse, risk level
    """
    # Get latest inventory snapshots
    snapshots = db.query(InventorySnapshot).all()
    
    result = []
    for snapshot in snapshots:
        # Compute risk level based on reorder point
        stock_status = "SAFE"
        if snapshot.stock_on_hand < snapshot.reorder_point:
            stock_status = "LOW"
        if snapshot.stock_on_hand < snapshot.reorder_point * 0.5:
            stock_status = "CRITICAL"
        
        result.append({
            "product_id": snapshot.product_id,
            "product_name": snapshot.product.name,
            "warehouse_id": snapshot.warehouse_id,
            "warehouse_name": snapshot.warehouse.name,
            "stock_on_hand": snapshot.stock_on_hand,
            "reorder_point": snapshot.reorder_point,
            "safety_stock": snapshot.safety_stock,
            "stock_status": stock_status,
            "recorded_at": snapshot.recorded_at.isoformat()
        })
    
    return {
        "status": "success",
        "count": len(result),
        "inventory": result
    }

@router.get("/inventory/{sku_id}/forecast")
def get_forecast(sku_id: str, db: Session = Depends(get_db)):
    """
    GET /api/inventory/{sku_id}/forecast
    Returns: shortage prediction + confidence + reasoning
    """
    product = db.query(Product).filter_by(id=sku_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get latest inventory across all warehouses
    inventory = db.query(InventorySnapshot).filter_by(product_id=sku_id).all()
    
    result = []
    for inv in inventory:
        # Get last 30 days of demand history
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == sku_id,
            DemandHistory.warehouse_id == inv.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        
        if not demand_records:
            continue
        
        units_sold = [d.units_sold for d in demand_records]
        avg_daily_demand = statistics.mean(units_sold)
        demand_variance = statistics.stdev(units_sold) if len(units_sold) > 1 else 0
        
        # Compute days-to-stockout
        if avg_daily_demand > 0:
            days_to_stockout = inv.stock_on_hand / avg_daily_demand
        else:
            days_to_stockout = 999
        
        # Confidence score: lower variance = higher confidence
        confidence_score = max(0.3, 1.0 - (demand_variance / (avg_daily_demand + 0.01)))
        
        # Risk level
        if days_to_stockout < 7:
            risk_level = "HIGH_RISK"
        elif days_to_stockout < 14:
            risk_level = "MEDIUM_RISK"
        else:
            risk_level = "LOW_RISK"
        
        reasoning = f"Based on {len(units_sold)} days of demand history. "
        if demand_variance > avg_daily_demand * 0.5:
            reasoning += "High variance indicates unpredictable demand."
        else:
            reasoning += "Demand is relatively stable."
        
        result.append({
            "sku_id": sku_id,
            "sku_name": product.name,
            "warehouse_id": inv.warehouse_id,
            "warehouse_name": inv.warehouse.name,
            "current_stock": inv.stock_on_hand,
            "daily_avg_demand": round(avg_daily_demand, 2),
            "demand_variance": round(demand_variance, 2),
            "days_to_stockout": round(days_to_stockout, 1),
            "risk_level": risk_level,
            "confidence_score": round(confidence_score, 2),
            "reasoning": reasoning
        })
    
    return {
        "status": "success",
        "sku_id": sku_id,
        "sku_name": product.name,
        "forecasts": result
    }

@router.get("/inventory/overstock")
def get_overstock(db: Session = Depends(get_db)):
    """
    GET /api/inventory/overstock
    Returns: products with excess stock, working capital impact
    """
    snapshots = db.query(InventorySnapshot).all()
    
    overstock_items = []
    for snapshot in snapshots:
        # Get last 30 days of demand
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
        
        # Demand-justified stock = avg_daily_demand * 14 days safety
        demand_justified_stock = avg_daily_demand * 14
        
        # Flag if current stock > demand-justified * 1.5
        if snapshot.stock_on_hand > demand_justified_stock * 1.5:
            excess_units = snapshot.stock_on_hand - int(demand_justified_stock)
            working_capital_tied_up = excess_units * snapshot.product.unit_price
            
            overstock_items.append({
                "product_id": snapshot.product_id,
                "product_name": snapshot.product.name,
                "warehouse_id": snapshot.warehouse_id,
                "warehouse_name": snapshot.warehouse.name,
                "current_stock": snapshot.stock_on_hand,
                "demand_justified_stock": round(demand_justified_stock),
                "excess_units": excess_units,
                "working_capital_tied_up": round(working_capital_tied_up, 2),
                "recommendation": "Consider reducing reorders or running a promotion to move excess inventory"
            })
    
    return {
        "status": "success",
        "count": len(overstock_items),
        "overstock_items": overstock_items
    }
