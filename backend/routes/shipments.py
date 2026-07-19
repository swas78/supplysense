"""
Shipment tracking and anomaly detection endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
from models import (
    Shipment, Anomaly, DemandHistory, InventorySnapshot,
    CustomerOrder, Product, ExternalSignal, PurchaseOrder, Supplier
)
from datetime import datetime, timedelta
import statistics

router = APIRouter()

@router.get("/anomalies")
def get_anomalies(db: Session = Depends(get_db)):
    """
    GET /api/anomalies
    Returns: detected demand spikes/drops with likely causes
    """
    # Get last 30 days of demand data
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    demand_records = db.query(DemandHistory).filter(
        DemandHistory.date >= thirty_days_ago
    ).all()
    
    anomalies_result = []
    
    # Group by product and warehouse
    product_wh_demands = {}
    for record in demand_records:
        key = (record.product_id, record.warehouse_id)
        if key not in product_wh_demands:
            product_wh_demands[key] = []
        product_wh_demands[key].append(record)
    
    # Detect anomalies using z-score
    for (product_id, warehouse_id), records in product_wh_demands.items():
        if len(records) < 10:
            continue
        
        units_sold_list = [r.units_sold for r in records]
        mean = statistics.mean(units_sold_list)
        stdev = statistics.stdev(units_sold_list) if len(units_sold_list) > 1 else 1
        
        # Check recent days for anomalies
        for record in records[-7:]:  # Last 7 days
            z_score = (record.units_sold - mean) / (stdev + 0.01)
            
            if abs(z_score) > 2.0:  # Anomaly threshold
                anomaly_type = "SPIKE" if z_score > 0 else "DROP"
                
                # Determine likely cause
                likely_cause = "Unknown"
                if record.is_promo_flag:
                    likely_cause = "Promotion"
                else:
                    # Check external signals on this date
                    signals = db.query(ExternalSignal).filter(
                        ExternalSignal.fetched_at >= record.date - timedelta(hours=2),
                        ExternalSignal.fetched_at <= record.date + timedelta(hours=2)
                    ).all()
                    if signals:
                        likely_cause = "Weather/External Event"
                
                severity = "HIGH" if abs(z_score) > 3.0 else "MEDIUM"
                
                product = db.query(Product).filter_by(id=product_id).first()
                
                anomalies_result.append({
                    "anomaly_id": f"anom_{product_id[:8]}_{warehouse_id[:8]}_{record.date.timestamp()}",
                    "product_id": product_id,
                    "product_name": product.name if product else "Unknown",
                    "detected_at": datetime.utcnow().isoformat(),
                    "date_of_spike": record.date.isoformat(),
                    "anomaly_type": anomaly_type,
                    "units_sold": record.units_sold,
                    "expected_units": int(mean),
                    "z_score": round(z_score, 2),
                    "likely_cause": likely_cause,
                    "severity": severity
                })
    
    return {
        "status": "success",
        "count": len(anomalies_result),
        "anomalies": sorted(anomalies_result, key=lambda x: x["z_score"], reverse=True)
    }

@router.get("/shipments/delays")
def get_delayed_shipments(db: Session = Depends(get_db)):
    """
    GET /api/shipments/delays
    Returns: list of delayed shipments with current ETA vs original ETA
    """
    shipments = db.query(Shipment).all()
    
    delayed = []
    for shipment in shipments:
        if shipment.current_eta > shipment.original_eta:
            delay_days = (shipment.current_eta - shipment.original_eta).days
            
            po = shipment.purchase_order
            supplier = db.query(Supplier).filter_by(id=po.supplier_id).first()
            product = db.query(Product).filter_by(id=po.product_id).first()
            
            delayed.append({
                "shipment_id": shipment.id,
                "supplier_id": supplier.id if supplier else None,
                "supplier_name": supplier.name if supplier else "Unknown",
                "product_id": po.product_id,
                "product_name": product.name if product else "Unknown",
                "quantity": po.quantity,
                "original_eta": shipment.original_eta.isoformat(),
                "current_eta": shipment.current_eta.isoformat(),
                "delay_days": delay_days,
                "destination_warehouse": po.warehouse_id,
                "carrier": shipment.carrier_name,
                "status": shipment.current_status
            })
    
    return {
        "status": "success",
        "count": len(delayed),
        "delayed_shipments": delayed
    }

@router.get("/shipments/{shipment_id}/impact")
def get_cascade_impact(shipment_id: str, db: Session = Depends(get_db)):
    """
    GET /api/shipments/{id}/impact
    Returns: cascade impact - which products, warehouses, orders affected
    """
    shipment = db.query(Shipment).filter_by(id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    po = shipment.purchase_order
    supplier = db.query(Supplier).filter_by(id=po.supplier_id).first()
    product = db.query(Product).filter_by(id=po.product_id).first()
    warehouse = db.query(InventorySnapshot).filter_by(
        product_id=po.product_id,
        warehouse_id=po.warehouse_id
    ).first()
    
    delay_days = (shipment.current_eta - shipment.original_eta).days
    
    # Step 1: Affected products
    affected_products = [{
        "product_id": po.product_id,
        "product_name": product.name if product else "Unknown",
        "shipment_quantity": po.quantity
    }]
    
    # Step 2: Affected warehouses
    affected_warehouses = []
    if warehouse:
        # Estimate how long current stock will last
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        demand_records = db.query(DemandHistory).filter(
            DemandHistory.product_id == po.product_id,
            DemandHistory.warehouse_id == po.warehouse_id,
            DemandHistory.date >= thirty_days_ago
        ).all()
        
        if demand_records:
            units_sold = [d.units_sold for d in demand_records]
            avg_daily_demand = statistics.mean(units_sold)
            stock_will_last_days = warehouse.stock_on_hand / avg_daily_demand if avg_daily_demand > 0 else 999
        else:
            avg_daily_demand = 0
            stock_will_last_days = 999
        
        affected_warehouses.append({
            "warehouse_id": po.warehouse_id,
            "warehouse_name": f"Warehouse {po.warehouse_id[:8]}",
            "current_stock": warehouse.stock_on_hand,
            "avg_daily_demand": round(avg_daily_demand, 2),
            "stock_will_last_days": round(stock_will_last_days, 1)
        })
    
    # Step 3: At-risk customer orders
    at_risk_orders = db.query(CustomerOrder).filter(
        CustomerOrder.product_id == po.product_id,
        CustomerOrder.warehouse_id == po.warehouse_id,
        CustomerOrder.status == "pending"
    ).all()
    
    at_risk_order_data = []
    total_at_risk_value = 0
    
    for order in at_risk_orders:
        order_data = {
            "order_id": order.id,
            "customer_id": order.customer_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "required_by_date": order.required_by_date.isoformat(),
            "order_value": round(order.order_value, 2),
            "days_until_required": (order.required_by_date - datetime.utcnow()).days
        }
        at_risk_order_data.append(order_data)
        total_at_risk_value += order.order_value
    
    # Summary
    num_at_risk_orders = len(at_risk_order_data)
    num_at_risk_units = sum(o["quantity"] for o in at_risk_order_data)
    
    summary = f"This {delay_days}-day delay puts {num_at_risk_orders} pending orders at risk of stockout. "
    summary += f"{num_at_risk_units} units at risk. Total value: ₹{total_at_risk_value:,.0f}."
    
    return {
        "status": "success",
        "shipment_id": shipment_id,
        "supplier_name": supplier.name if supplier else "Unknown",
        "delay_days": delay_days,
        "cascade": {
            "affected_products": affected_products,
            "affected_warehouses": affected_warehouses,
            "at_risk_orders": at_risk_order_data,
            "total_at_risk_order_value": round(total_at_risk_value, 2),
            "summary": summary
        }
    }

@router.post("/simulate/trigger-delay")
def trigger_demo_delay(
    shipment_id: str = None,
    delay_days: int = 4,
    db: Session = Depends(get_db)
):
    """
    POST /api/simulate/trigger-delay?shipment_id=xyz&delay_days=4
    Triggers a shipment delay for demo purposes
    """
    # If no shipment specified, find the in-transit one
    if not shipment_id:
        shipment = db.query(Shipment).filter(
            Shipment.current_status == "in_transit"
        ).first()
        if not shipment:
            shipment = db.query(Shipment).first()
    else:
        shipment = db.query(Shipment).filter_by(id=shipment_id).first()
    
    if not shipment:
        raise HTTPException(status_code=404, detail="No shipment found to delay")
    
    # Update shipment
    old_eta = shipment.current_eta
    shipment.current_eta = shipment.original_eta + timedelta(days=delay_days)
    shipment.current_status = "delayed"
    db.commit()
    
    po = shipment.purchase_order
    supplier = db.query(Supplier).filter_by(id=po.supplier_id).first()
    
    # Get cascade impact
    impact = get_cascade_impact(shipment.id, db)
    
    return {
        "status": "delay_triggered",
        "shipment_id": shipment.id,
        "supplier_name": supplier.name if supplier else "Unknown",
        "old_eta": old_eta.isoformat(),
        "new_eta": shipment.current_eta.isoformat(),
        "delay_days": delay_days,
        "affected_orders": impact["cascade"]["at_risk_orders"].__len__(),
        "total_at_risk_value": impact["cascade"]["total_at_risk_order_value"],
        "message": "Demo delay triggered successfully"
    }
