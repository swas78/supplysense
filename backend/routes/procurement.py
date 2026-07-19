"""
Procurement recommendation generator
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import (
    Product, Forecast, Supplier, DemandHistory, InventorySnapshot,
    ProcurementSuggestion
)
from datetime import datetime, timedelta
import statistics

router = APIRouter()

@router.get("/procurement/suggestions")
def get_procurement_suggestions(db: Session = Depends(get_db)):
    """
    GET /api/procurement/suggestions
    Returns: What to reorder, how much, from whom, by when
    """
    suggestions = []
    
    # Get all forecasts showing shortages
    forecasts = db.query(Forecast).filter(
        Forecast.predicted_days_to_stockout < 14  # Focus on upcoming shortages
    ).all()
    
    for forecast in forecasts:
        product = db.query(Product).filter_by(id=forecast.product_id).first()
        if not product:
            continue
        
        # Get inventory snapshot for this product/warehouse
        inventory = db.query(InventorySnapshot).filter(
            InventorySnapshot.product_id == forecast.product_id,
            InventorySnapshot.warehouse_id == forecast.warehouse_id
        ).first()
        
        if not inventory:
            continue
        
        # Get average daily demand
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == forecast.product_id,
            DemandHistory.warehouse_id == forecast.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        
        if not demand_records:
            continue
        
        units_sold = [d.units_sold for d in demand_records]
        daily_demand = statistics.mean(units_sold)
        
        # Calculate suggested reorder quantity
        # = (days_to_stockout + 7 days safety buffer) * daily_demand + safety_stock
        suggested_qty = int((forecast.predicted_days_to_stockout + 14) * daily_demand + inventory.safety_stock)
        
        # Find best supplier for this product
        all_suppliers = db.query(Supplier).all()
        suitable_suppliers = [
            s for s in all_suppliers
            if product.category in [str(cat) for cat in s.product_categories]
        ]
        
        if not suitable_suppliers:
            continue
        
        best_supplier = max(suitable_suppliers, key=lambda s: s.reliability_score)
        
        # Calculate deadline to order
        # deadline = today + lead_time - 2 day buffer
        deadline = datetime.utcnow() + timedelta(
            days=best_supplier.avg_lead_time_days - 2
        )
        
        # Determine urgency
        if forecast.predicted_days_to_stockout < 3:
            urgency = "CRITICAL"
        elif forecast.predicted_days_to_stockout < 7:
            urgency = "HIGH"
        else:
            urgency = "MEDIUM"
        
        # Estimate cost
        estimated_cost = suggested_qty * product.unit_price
        
        # Build reasoning
        reasoning = (
            f"Stock will run out in {forecast.predicted_days_to_stockout:.1f} days. "
            f"Current stock: {inventory.stock_on_hand} units. "
            f"Daily demand: {daily_demand:.1f} units. "
            f"Recommend reorder {suggested_qty} units from {best_supplier.name} "
            f"({best_supplier.on_time_rate*100:.0f}% on-time, {best_supplier.avg_lead_time_days} day lead time). "
            f"Order deadline: {deadline.strftime('%Y-%m-%d')} to ensure arrival before stockout."
        )
        
        suggestion = {
            "product_id": forecast.product_id,
            "product_name": product.name,
            "warehouse_id": forecast.warehouse_id,
            "current_stock": inventory.stock_on_hand,
            "daily_demand": round(daily_demand, 2),
            "days_to_stockout": round(forecast.predicted_days_to_stockout, 1),
            "suggested_quantity": suggested_qty,
            "recommended_supplier_id": best_supplier.id,
            "recommended_supplier_name": best_supplier.name,
            "supplier_on_time_rate": round(best_supplier.on_time_rate, 2),
            "supplier_lead_time_days": best_supplier.avg_lead_time_days,
            "order_deadline": deadline.isoformat(),
            "urgency": urgency,
            "estimated_cost": round(estimated_cost, 2),
            "reasoning": reasoning,
            "confidence_score": round(forecast.confidence_score, 2)
        }
        
        # Store in database
        proc_sugg = ProcurementSuggestion(
            product_id=forecast.product_id,
            suggested_quantity=suggested_qty,
            suggested_supplier_id=best_supplier.id,
            by_date=deadline,
            reasoning=reasoning,
            created_at=datetime.utcnow()
        )
        db.add(proc_sugg)
        
        suggestions.append(suggestion)
    
    db.commit()
    
    # Sort by urgency (CRITICAL > HIGH > MEDIUM) and days to stockout
    urgency_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    suggestions = sorted(
        suggestions,
        key=lambda x: (urgency_order[x["urgency"]], x["days_to_stockout"])
    )
    
    return {
        "status": "success",
        "count": len(suggestions),
        "suggestions": suggestions
    }

@router.get("/procurement/suggestions/{product_id}")
def get_procurement_suggestion_for_product(product_id: str, db: Session = Depends(get_db)):
    """Get procurement suggestion for a specific product"""
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    suggestions = db.query(ProcurementSuggestion).filter_by(
        product_id=product_id
    ).order_by(ProcurementSuggestion.created_at.desc()).limit(1).all()
    
    if not suggestions:
        return {
            "status": "success",
            "product_id": product_id,
            "product_name": product.name,
            "suggestion": None
        }
    
    sugg = suggestions[0]
    supplier = db.query(Supplier).filter_by(id=sugg.suggested_supplier_id).first()
    
    return {
        "status": "success",
        "product_id": product_id,
        "product_name": product.name,
        "suggestion": {
            "product_id": sugg.product_id,
            "suggested_quantity": sugg.suggested_quantity,
            "supplier_id": sugg.suggested_supplier_id,
            "supplier_name": supplier.name if supplier else "Unknown",
            "by_date": sugg.by_date.isoformat(),
            "reasoning": sugg.reasoning,
            "created_at": sugg.created_at.isoformat()
        }
    }
