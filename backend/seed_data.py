"""
Seed realistic test data for SupplySense demo
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import random
import math

from models import (
    Supplier, Warehouse, Product, InventorySnapshot, DemandHistory,
    PurchaseOrder, Shipment, ShipmentEvent, ExternalSignal, CustomerOrder
)

def seed_suppliers(db: Session):
    """Create suppliers with varied reliability profiles"""
    suppliers_data = [
        {
            "name": "Supplier A",
            "product_categories": ["electronics", "components"],
            "avg_lead_time_days": 10,
            "on_time_rate": 0.71,
            "quality_rate": 0.92,
        },
        {
            "name": "Supplier B",
            "product_categories": ["electronics", "components"],
            "avg_lead_time_days": 5,
            "on_time_rate": 0.96,
            "quality_rate": 0.98,
        },
        {
            "name": "Supplier C",
            "product_categories": ["components", "raw_materials"],
            "avg_lead_time_days": 14,
            "on_time_rate": 0.82,
            "quality_rate": 0.88,
        },
        {
            "name": "Supplier D",
            "product_categories": ["raw_materials"],
            "avg_lead_time_days": 7,
            "on_time_rate": 0.60,  # Bad reliability
            "quality_rate": 0.85,
        },
        {
            "name": "Supplier E",
            "product_categories": ["electronics"],
            "avg_lead_time_days": 6,
            "on_time_rate": 0.88,
            "quality_rate": 0.95,
        },
    ]
    
    suppliers = []
    for data in suppliers_data:
        supplier = Supplier(**data)
        # Compute reliability score: w1*on_time + w2*(1/lead_time) + w3*quality
        supplier.reliability_score = (
            0.5 * supplier.on_time_rate +
            0.25 * (1 - min(supplier.avg_lead_time_days / 30, 1)) +
            0.25 * supplier.quality_rate
        )
        # Recovery resilience: on average, how fast do they bounce back? (simulated)
        # Suppliers with bad on_time have high recovery resilience (recover fast)
        if supplier.on_time_rate < 0.70:
            supplier.recovery_resilience_score = 2.0  # Days to recover
        elif supplier.on_time_rate < 0.85:
            supplier.recovery_resilience_score = 3.5
        else:
            supplier.recovery_resilience_score = 1.5  # Good suppliers recover faster
        
        db.add(supplier)
        suppliers.append(supplier)
    
    db.commit()
    return suppliers

def seed_warehouses(db: Session):
    """Create warehouses in different locations"""
    warehouses_data = [
        {
            "name": "Warehouse 1",
            "location": "Delhi",
            "capacity_units": 15000,
        },
        {
            "name": "Warehouse 2",
            "location": "Mumbai",
            "capacity_units": 12000,
        },
        {
            "name": "Warehouse 3",
            "location": "Bangalore",
            "capacity_units": 10000,
        },
    ]
    
    warehouses = []
    for data in warehouses_data:
        warehouse = Warehouse(**data)
        db.add(warehouse)
        warehouses.append(warehouse)
    
    db.commit()
    return warehouses

def seed_products(db: Session):
    """Create product SKUs"""
    products_data = [
        {"name": "Widget A", "category": "electronics", "unit_margin": 0.35, "unit_price": 500},
        {"name": "Widget B", "category": "electronics", "unit_margin": 0.40, "unit_price": 800},
        {"name": "Component X", "category": "components", "unit_margin": 0.25, "unit_price": 200},
        {"name": "Component Y", "category": "components", "unit_margin": 0.30, "unit_price": 150},
        {"name": "Raw Material P", "category": "raw_materials", "unit_margin": 0.15, "unit_price": 100},
        {"name": "Raw Material Q", "category": "raw_materials", "unit_margin": 0.20, "unit_price": 120},
        {"name": "Assembly M1", "category": "electronics", "unit_margin": 0.45, "unit_price": 1200},
        {"name": "Assembly M2", "category": "electronics", "unit_margin": 0.40, "unit_price": 1500},
    ]
    
    products = []
    for data in products_data:
        product = Product(**data)
        db.add(product)
        products.append(product)
    
    db.commit()
    return products

def seed_inventory(db: Session, products, warehouses):
    """Create current inventory snapshots"""
    for product in products:
        for warehouse in warehouses:
            snapshot = InventorySnapshot(
                product_id=product.id,
                warehouse_id=warehouse.id,
                stock_on_hand=random.randint(50, 500),
                reorder_point=100,
                safety_stock=150,
                recorded_at=datetime.utcnow()
            )
            db.add(snapshot)
    
    # Override one product to be deliberately low (for shortage demo)
    low_product = products[0]  # Widget A
    low_wh = warehouses[1]  # Warehouse 2
    low_snapshot = db.query(InventorySnapshot).filter_by(
        product_id=low_product.id,
        warehouse_id=low_wh.id
    ).first()
    if low_snapshot:
        low_snapshot.stock_on_hand = 80  # Below reorder point
    
    # Override one product to be deliberately high (for overstock demo)
    high_product = products[3]  # Component Y
    high_wh = warehouses[0]  # Warehouse 1
    high_snapshot = db.query(InventorySnapshot).filter_by(
        product_id=high_product.id,
        warehouse_id=high_wh.id
    ).first()
    if high_snapshot:
        high_snapshot.stock_on_hand = 1500  # Way above demand-justified
    
    db.commit()

def seed_demand_history(db: Session, products, warehouses):
    """Create 3 months of synthetic demand history"""
    today = datetime.utcnow()
    start_date = today - timedelta(days=90)
    
    for product in products:
        for warehouse in warehouses:
            base_demand = random.randint(15, 40)  # Base daily demand
            
            for day_offset in range(90):
                date = start_date + timedelta(days=day_offset)
                
                # Add seasonal spike at certain days (Q4-like pattern)
                if 60 <= day_offset <= 75:
                    daily_demand = int(base_demand * 1.5)
                else:
                    daily_demand = base_demand + random.randint(-5, 10)
                
                daily_demand = max(1, daily_demand)
                
                is_promo = False
                # Promo days for Widget A
                if product.name == "Widget A" and 20 <= day_offset <= 25:
                    daily_demand = int(daily_demand * 2.5)
                    is_promo = True
                
                history = DemandHistory(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    date=date,
                    units_sold=daily_demand,
                    is_promo_flag=is_promo
                )
                db.add(history)
    
    db.commit()

def seed_purchase_orders(db: Session, suppliers, products, warehouses):
    """Create historical purchase orders (mix of on-time and late)"""
    now = datetime.utcnow()
    po_data = []
    
    for i in range(12):
        supplier = random.choice(suppliers)
        product = random.choice(products)
        warehouse = random.choice(warehouses)
        
        # Create orders across the past 60 days
        days_ago = random.randint(1, 60)
        expected_delivery = now - timedelta(days=days_ago) + timedelta(days=supplier.avg_lead_time_days)
        
        # Simulate on-time vs. late based on supplier reliability
        if random.random() < supplier.on_time_rate:
            actual_delivery = expected_delivery
        else:
            # Late delivery: add 1-7 days
            actual_delivery = expected_delivery + timedelta(days=random.randint(1, 7))
        
        po = PurchaseOrder(
            supplier_id=supplier.id,
            product_id=product.id,
            warehouse_id=warehouse.id,
            quantity=random.randint(100, 500),
            expected_delivery_date=expected_delivery,
            actual_delivery_date=actual_delivery,
            status="delivered"
        )
        db.add(po)
        po_data.append(po)
    
    db.commit()
    return po_data

def seed_shipments(db: Session, purchase_orders):
    """Create shipments from POs"""
    shipments = []
    now = datetime.utcnow()
    
    for po in purchase_orders[:8]:  # Shipments for some of the POs
        shipment = Shipment(
            purchase_order_id=po.id,
            carrier_name=random.choice(["FedEx", "UPS", "DHL", "Local Courier"]),
            current_status="delivered",
            original_eta=po.expected_delivery_date,
            current_eta=po.actual_delivery_date,
        )
        db.add(shipment)
        shipments.append(shipment)
    
    # Create one in-transit shipment (for demo trigger)
    if purchase_orders:
        demo_po = purchase_orders[0]
        demo_shipment = Shipment(
            purchase_order_id=demo_po.id,
            carrier_name="Premium Express",
            current_status="in_transit",
            original_eta=now + timedelta(days=3),
            current_eta=now + timedelta(days=3),
        )
        db.add(demo_shipment)
        shipments.append(demo_shipment)
    
    db.commit()
    return shipments

def seed_customer_orders(db: Session, products, warehouses):
    """Create pending customer orders (some will be at-risk when we trigger demo)"""
    now = datetime.utcnow()
    
    # Widget A (low stock) should have multiple pending orders
    widget_a = [p for p in products if p.name == "Widget A"][0]
    
    for i in range(3):
        order = CustomerOrder(
            customer_id=f"CUST_{i:03d}",
            product_id=widget_a.id,
            warehouse_id=warehouses[1].id,  # Warehouse 2 (the low-stock one)
            quantity=random.randint(100, 200),
            required_by_date=now + timedelta(days=random.randint(2, 7)),
            order_value=widget_a.unit_price * random.randint(100, 200),
            status="pending"
        )
        db.add(order)
    
    # Add some more random pending orders
    for i in range(10):
        product = random.choice(products)
        warehouse = random.choice(warehouses)
        order = CustomerOrder(
            customer_id=f"CUST_{random.randint(100, 999):03d}",
            product_id=product.id,
            warehouse_id=warehouse.id,
            quantity=random.randint(50, 300),
            required_by_date=now + timedelta(days=random.randint(1, 14)),
            order_value=product.unit_price * random.randint(50, 300),
            status="pending"
        )
        db.add(order)
    
    db.commit()

def seed_external_signals(db: Session):
    """Create some mock external signals (weather, promos)"""
    now = datetime.utcnow()
    
    signals = [
        {
            "signal_type": "weather",
            "location": "Delhi",
            "description": "Heavy rain expected",
            "severity": "high",
            "fetched_at": now - timedelta(hours=2)
        },
        {
            "signal_type": "weather",
            "location": "Mumbai",
            "description": "Clear skies",
            "severity": "low",
            "fetched_at": now - timedelta(hours=1)
        },
        {
            "signal_type": "promo",
            "location": "All",
            "description": "Flash sale on Electronics - 48h",
            "severity": "medium",
            "fetched_at": now
        },
    ]
    
    for sig in signals:
        signal = ExternalSignal(**sig)
        db.add(signal)
    
    db.commit()

def seed_all(db: Session):
    """Run all seed functions in order"""
    print("🌱 Seeding database...")
    
    # Clear existing data
    db.query(InventorySnapshot).delete()
    db.query(DemandHistory).delete()
    db.query(CustomerOrder).delete()
    db.query(Shipment).delete()
    db.query(ShipmentEvent).delete()
    db.query(PurchaseOrder).delete()
    db.query(ExternalSignal).delete()
    db.query(Product).delete()
    db.query(Warehouse).delete()
    db.query(Supplier).delete()
    db.commit()
    
    suppliers = seed_suppliers(db)
    print(f"✓ Seeded {len(suppliers)} suppliers")
    
    warehouses = seed_warehouses(db)
    print(f"✓ Seeded {len(warehouses)} warehouses")
    
    products = seed_products(db)
    print(f"✓ Seeded {len(products)} products")
    
    seed_inventory(db, products, warehouses)
    print(f"✓ Seeded inventory snapshots")
    
    seed_demand_history(db, products, warehouses)
    print(f"✓ Seeded 90 days of demand history")
    
    po_data = seed_purchase_orders(db, suppliers, products, warehouses)
    print(f"✓ Seeded {len(po_data)} purchase orders")
    
    shipments = seed_shipments(db, po_data)
    print(f"✓ Seeded {len(shipments)} shipments")
    
    seed_customer_orders(db, products, warehouses)
    print(f"✓ Seeded customer orders")
    
    seed_external_signals(db)
    print(f"✓ Seeded external signals")
    
    print("✅ Database seeding complete!")
