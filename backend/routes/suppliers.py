"""
Supplier scoring and reliability endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Supplier, PurchaseOrder, Product
from datetime import datetime, timedelta
import statistics

router = APIRouter()

@router.get("/suppliers/scores")
def get_supplier_scores(db: Session = Depends(get_db)):
    """
    GET /api/suppliers/scores
    Returns: All suppliers ranked by reliability score with recovery resilience
    
    Formula: reliability_score = 0.5*on_time_rate + 0.25*(1/lead_time_factor) + 0.25*quality_rate
    """
    suppliers = db.query(Supplier).all()
    
    result = []
    for supplier in suppliers:
        # Calculate reliability score if not already cached
        if supplier.reliability_score == 0.0:
            supplier.reliability_score = (
                0.5 * supplier.on_time_rate +
                0.25 * (1 - min(supplier.avg_lead_time_days / 30, 1)) +
                0.25 * supplier.quality_rate
            )
            db.add(supplier)
        
        # Determine risk level based on on-time rate
        if supplier.on_time_rate >= 0.90:
            risk_level = "LOW_RISK"
        elif supplier.on_time_rate >= 0.75:
            risk_level = "MEDIUM_RISK"
        else:
            risk_level = "HIGH_RISK"
        
        # Build reasoning text
        reasoning = (
            f"On-time delivery: {supplier.on_time_rate*100:.0f}%, "
            f"Lead time: {supplier.avg_lead_time_days:.0f} days, "
            f"Quality: {supplier.quality_rate*100:.0f}%"
        )
        
        # Recovery resilience interpretation
        recovery_text = f"Recovers in ~{supplier.recovery_resilience_score:.1f} days after a miss"
        if supplier.recovery_resilience_score <= 2:
            recovery_text += " (fast recovery)"
        elif supplier.recovery_resilience_score <= 3.5:
            recovery_text += " (moderate recovery)"
        else:
            recovery_text += " (slow recovery)"
        
        result.append({
            "supplier_id": supplier.id,
            "supplier_name": supplier.name,
            "reliability_score": round(supplier.reliability_score, 3),
            "on_time_rate": round(supplier.on_time_rate, 2),
            "avg_lead_time_days": supplier.avg_lead_time_days,
            "quality_rate": round(supplier.quality_rate, 2),
            "recovery_resilience_score": round(supplier.recovery_resilience_score, 1),
            "risk_level": risk_level,
            "reasoning": reasoning,
            "recovery_text": recovery_text,
            "product_categories": supplier.product_categories
        })
    
    db.commit()
    
    # Sort by reliability score (highest first)
    result = sorted(result, key=lambda x: x["reliability_score"], reverse=True)
    
    return {
        "status": "success",
        "count": len(result),
        "suppliers": result
    }

@router.get("/suppliers/{supplier_id}")
def get_supplier_details(supplier_id: str, db: Session = Depends(get_db)):
    """
    GET /api/suppliers/{supplier_id}
    Returns: Detailed supplier info + historical performance
    """
    supplier = db.query(Supplier).filter_by(id=supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Get historical performance from purchase orders
    pos = db.query(PurchaseOrder).filter_by(supplier_id=supplier_id).all()
    
    on_time_count = 0
    late_count = 0
    late_days = []
    
    for po in pos:
        if po.actual_delivery_date and po.expected_delivery_date:
            if po.actual_delivery_date <= po.expected_delivery_date:
                on_time_count += 1
            else:
                late_count += 1
                days_late = (po.actual_delivery_date - po.expected_delivery_date).days
                late_days.append(days_late)
    
    total_orders = on_time_count + late_count
    
    avg_late_days = statistics.mean(late_days) if late_days else 0
    
    return {
        "status": "success",
        "supplier": {
            "supplier_id": supplier.id,
            "supplier_name": supplier.name,
            "reliability_score": round(supplier.reliability_score, 3),
            "on_time_rate": round(supplier.on_time_rate, 2),
            "quality_rate": round(supplier.quality_rate, 2),
            "avg_lead_time_days": supplier.avg_lead_time_days,
            "recovery_resilience_score": round(supplier.recovery_resilience_score, 1),
            "product_categories": supplier.product_categories,
            "historical_performance": {
                "total_orders": total_orders,
                "on_time_orders": on_time_count,
                "late_orders": late_count,
                "on_time_percentage": round((on_time_count / total_orders * 100) if total_orders > 0 else 0, 1),
                "avg_late_days": round(avg_late_days, 1)
            }
        }
    }
