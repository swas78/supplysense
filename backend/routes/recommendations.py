"""
Recommendations engine - alternate suppliers, procurement, etc.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import (
    Shipment, Supplier, Product, Recommendation, CustomerOrder, 
    Forecast, DemandHistory, InventorySnapshot, DealerMessage, PurchaseOrder
)
from datetime import datetime, timedelta
import statistics
import json

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    """
    GET /api/recommendations
    Returns: Active recommendations for disruptions with reasoning + cost impact
    """
    recommendations = []
    
    # 1. Check for delayed shipments → recommend alternate suppliers
    delayed_shipments = db.query(Shipment).filter(
        Shipment.current_eta > Shipment.original_eta
    ).all()
    
    for shipment in delayed_shipments:
        po = shipment.purchase_order
        current_supplier = db.query(Supplier).filter_by(id=po.supplier_id).first()
        product = db.query(Product).filter_by(id=po.product_id).first()
        
        delay_days = (shipment.current_eta - shipment.original_eta).days
        
        # Get cascade impact to calculate cost
        at_risk_orders = db.query(CustomerOrder).filter(
            CustomerOrder.product_id == po.product_id,
            CustomerOrder.warehouse_id == po.warehouse_id,
            CustomerOrder.status == "pending"
        ).all()
        
        total_at_risk_value = sum(o.order_value for o in at_risk_orders)
        
        # Find alternate suppliers
        all_suppliers = db.query(Supplier).all()
        alternate_suppliers = [
            s for s in all_suppliers 
            if s.id != po.supplier_id and 
            po.product_id[:3] in [str(cat)[:3] for cat in s.product_categories]
        ]
        
        # Pick best alternate (highest reliability score)
        best_alternate = max(
            alternate_suppliers,
            key=lambda s: s.reliability_score,
            default=None
        )
        
        if best_alternate:
            reasoning = (
                f"Supplier {current_supplier.name} is {delay_days} days late. "
                f"{best_alternate.name} has {best_alternate.on_time_rate*100:.0f}% on-time rate "
                f"(vs {current_supplier.on_time_rate*100:.0f}%), "
                f"lead time {best_alternate.avg_lead_time_days} days (vs {current_supplier.avg_lead_time_days}), "
                f"recovery resilience {best_alternate.recovery_resilience_score:.1f} days. "
                f"Risk of {len(at_risk_orders)} orders unfulfilled (₹{total_at_risk_value:,.0f})."
            )
            
            rec = Recommendation(
                trigger_type="shipment_delay",
                trigger_ref_id=shipment.id,
                recommended_action=f"Switch to {best_alternate.name} for expedited fulfillment",
                reasoning_text=reasoning,
                estimated_cost_impact_inr=total_at_risk_value,
                confidence_score=0.92,
                status="active"
            )
            db.add(rec)
            
            recommendations.append({
                "recommendation_id": rec.id,
                "trigger_type": "shipment_delay",
                "trigger_ref_id": shipment.id,
                "problem": f"{current_supplier.name} delay ({delay_days} days) affecting {product.name}",
                "current_supplier": current_supplier.name,
                "recommended_action": f"Switch to {best_alternate.name}",
                "reasoning_text": reasoning,
                "estimated_cost_impact_inr": round(total_at_risk_value, 2),
                "confidence_score": 0.92,
                "status": "active"
            })
    
    # 2. Check for predicted shortages → recommend procurement
    forecasts = db.query(Forecast).filter(
        Forecast.predicted_days_to_stockout < 7
    ).all()
    
    for forecast in forecasts:
        product = db.query(Product).filter_by(id=forecast.product_id).first()
        
        # Find best supplier for this product
        all_suppliers = db.query(Supplier).all()
        suitable_suppliers = [
            s for s in all_suppliers
            if product.category in [str(cat) for cat in s.product_categories]
        ]
        
        best_supplier = max(
            suitable_suppliers,
            key=lambda s: s.reliability_score,
            default=None
        )
        
        if best_supplier:
            reasoning = (
                f"Product {product.name} will run out in {forecast.predicted_days_to_stockout:.1f} days. "
                f"Recommend reorder from {best_supplier.name} "
                f"({best_supplier.on_time_rate*100:.0f}% on-time, {best_supplier.avg_lead_time_days} day lead time)."
            )
            
            rec = Recommendation(
                trigger_type="shortage_predicted",
                trigger_ref_id=forecast.id,
                recommended_action=f"Reorder {product.name} from {best_supplier.name}",
                reasoning_text=reasoning,
                estimated_cost_impact_inr=10000,  # Rough estimate
                confidence_score=forecast.confidence_score,
                status="active"
            )
            db.add(rec)
            
            recommendations.append({
                "recommendation_id": rec.id,
                "trigger_type": "shortage_predicted",
                "trigger_ref_id": forecast.id,
                "problem": f"{product.name} shortage predicted in {forecast.predicted_days_to_stockout:.1f} days",
                "recommended_action": f"Reorder from {best_supplier.name}",
                "reasoning_text": reasoning,
                "estimated_cost_impact_inr": 10000,
                "confidence_score": round(forecast.confidence_score, 2),
                "status": "active"
            })
    
    db.commit()
    
    return {
        "status": "success",
        "count": len(recommendations),
        "recommendations": recommendations
    }

@router.post("/recommendations/{rec_id}/message")
def generate_dealer_message(rec_id: str, db: Session = Depends(get_db)):
    """
    POST /api/recommendations/{rec_id}/message
    Generates auto-drafted dealer/supplier message
    """
    rec = db.query(Recommendation).filter_by(id=rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Determine message type based on trigger
    if rec.trigger_type == "shipment_delay":
        # Message to alternate supplier requesting expedite
        template = f"""
EXPEDITE REQUEST

Dear Supplier Partner,

We are requesting expedited fulfillment of the following:

Product: {rec.recommended_action.split()[-1]}
Quantity: [To be confirmed]
Delivery Target: {(datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d')}

Reason: Current supplier experiencing delays. This order is critical for customer fulfillment.

Urgency: HIGH
Expected Delivery: {(datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d')}

Please confirm availability and capacity within 2 hours.

Best regards,
Supply Chain Operations
        """
    else:
        # Message for standard procurement
        template = f"""
PURCHASE ORDER REQUEST

Dear Supplier Partner,

Please provide a quote for:

{rec.recommended_action}
Quantity: [To be calculated]
Requested Delivery: {(datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')}

We are targeting this timeline based on demand forecasts.

Please quote by EOD today.

Best regards,
Procurement Team
        """
    
    # Store message
    dealer_msg = DealerMessage(
        recommendation_id=rec_id,
        template_type="expedite_request" if rec.trigger_type == "shipment_delay" else "procurement_request",
        generated_text=template.strip(),
        recipient=rec.recommended_action.split()[-1],  # Extract supplier name
        created_at=datetime.utcnow()
    )
    db.add(dealer_msg)
    db.commit()
    
    return {
        "status": "success",
        "message": template.strip(),
        "recipient": rec.recommended_action.split()[-1],
        "message_id": dealer_msg.id
    }

@router.get("/recommendations/{rec_id}")
def get_recommendation_detail(rec_id: str, db: Session = Depends(get_db)):
    """Get details of a specific recommendation"""
    rec = db.query(Recommendation).filter_by(id=rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Get associated message if exists
    message = db.query(DealerMessage).filter_by(recommendation_id=rec_id).first()
    
    return {
        "status": "success",
        "recommendation": {
            "id": rec.id,
            "trigger_type": rec.trigger_type,
            "recommended_action": rec.recommended_action,
            "reasoning_text": rec.reasoning_text,
            "estimated_cost_impact_inr": rec.estimated_cost_impact_inr,
            "confidence_score": rec.confidence_score,
            "status": rec.status,
            "created_at": rec.created_at.isoformat()
        },
        "message": {
            "text": message.generated_text if message else None,
            "recipient": message.recipient if message else None
        } if message else None
    }
