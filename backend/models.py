"""
Database models for SupplySense
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    product_categories = Column(JSON, default=[])  # List of product category IDs
    avg_lead_time_days = Column(Float, default=7)
    on_time_rate = Column(Float, default=0.8)  # 0-1
    quality_rate = Column(Float, default=0.95)  # 0-1
    reliability_score = Column(Float, default=0.0)  # Computed
    recovery_resilience_score = Column(Float, default=0.0)  # Days to recover
    created_at = Column(DateTime, default=datetime.utcnow)
    
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    location = Column(String)  # For weather API lookup
    capacity_units = Column(Integer, default=10000)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    inventory_snapshots = relationship("InventorySnapshot", back_populates="warehouse")
    demand_history = relationship("DemandHistory", back_populates="warehouse")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    unit_margin = Column(Float, default=0.3)  # 30% margin
    unit_price = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    inventory_snapshots = relationship("InventorySnapshot", back_populates="product")
    demand_history = relationship("DemandHistory", back_populates="product")
    purchase_orders = relationship("PurchaseOrder", back_populates="product")
    forecasts = relationship("Forecast", back_populates="product")
    anomalies = relationship("Anomaly", back_populates="product")
    customer_orders = relationship("CustomerOrder", back_populates="product")
    

class AllocationDecision(Base):
    __tablename__ = "allocation_decisions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), index=True)
    available_stock = Column(Integer)
    total_demand = Column(Integer)
    ranking_json = Column(Text)  # JSON string of allocation ranking
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ProcurementSuggestion(Base):
    __tablename__ = "procurement_suggestions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), index=True)
    suggested_quantity = Column(Integer)
    suggested_supplier_id = Column(String, ForeignKey("suppliers.id"))
    by_date = Column(DateTime)
    reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_query = Column(Text)
    bot_response = Column(Text)
    reasoning_trace = Column(Text)
    tools_called = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), index=True)
    stock_on_hand = Column(Integer, default=0)
    reorder_point = Column(Integer, default=50)
    safety_stock = Column(Integer, default=100)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    product = relationship("Product", back_populates="inventory_snapshots")
    warehouse = relationship("Warehouse", back_populates="inventory_snapshots")

class DemandHistory(Base):
    __tablename__ = "demand_history"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), index=True)
    date = Column(DateTime, index=True)
    units_sold = Column(Integer, default=0)
    is_promo_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="demand_history")
    warehouse = relationship("Warehouse", back_populates="demand_history")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String, ForeignKey("suppliers.id"), index=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), index=True)
    quantity = Column(Integer, default=0)
    expected_delivery_date = Column(DateTime, index=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, delivered, delayed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    supplier = relationship("Supplier", back_populates="purchase_orders")
    product = relationship("Product", back_populates="purchase_orders")
    shipments = relationship("Shipment", back_populates="purchase_order")

class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), index=True)
    carrier_name = Column(String, default="Standard Carrier")
    current_status = Column(String, default="in_transit")  # in_transit, delayed, delivered
    original_eta = Column(DateTime, index=True)
    current_eta = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    purchase_order = relationship("PurchaseOrder", back_populates="shipments")
    shipment_events = relationship("ShipmentEvent", back_populates="shipment")

class ShipmentEvent(Base):
    __tablename__ = "shipment_events"
    
    id = Column(Integer, primary_key=True)
    shipment_id = Column(String, ForeignKey("shipments.id"), index=True)
    event_type = Column(String)  # delay_reported, in_transit_update, delivered
    event_timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    shipment = relationship("Shipment", back_populates="shipment_events")

class ExternalSignal(Base):
    __tablename__ = "external_signals"
    
    id = Column(Integer, primary_key=True)
    signal_type = Column(String, index=True)  # weather, news, promo
    location = Column(String, index=True)
    description = Column(String)
    severity = Column(String, default="medium")  # low, medium, high
    fetched_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=True)
    predicted_days_to_stockout = Column(Float, nullable=True)
    predicted_overstock_units = Column(Integer, nullable=True)
    confidence_score = Column(Float, default=0.5)  # 0-1
    risk_level = Column(String, default="LOW_RISK")  # HIGH_RISK, MEDIUM_RISK, LOW_RISK
    reasoning = Column(Text)
    generated_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    product = relationship("Product", back_populates="forecasts")

class Anomaly(Base):
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    anomaly_type = Column(String)  # SPIKE, DROP
    likely_cause = Column(String)  # Promotion, Weather, Unknown
    severity = Column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH
    z_score = Column(Float, nullable=True)
    expected_units = Column(Integer, nullable=True)
    actual_units = Column(Integer, nullable=True)
    
    product = relationship("Product", back_populates="anomalies")

class CustomerOrder(Base):
    __tablename__ = "customer_orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, index=True)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), index=True)
    quantity = Column(Integer, default=0)
    required_by_date = Column(DateTime, index=True)
    order_value = Column(Float, default=0.0)  # ₹ value
    status = Column(String, default="pending")  # pending, fulfilled, at_risk, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="customer_orders")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trigger_type = Column(String)  # shipment_delay, shortage_predicted
    trigger_ref_id = Column(String, index=True)  # ID of shipment/forecast that triggered it
    recommended_action = Column(String)  # e.g., "switch to Supplier B"
    reasoning_text = Column(Text)
    estimated_cost_impact_inr = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.5)
    status = Column(String, default="active")  # active, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

class DealerMessage(Base):
    __tablename__ = "dealer_messages"
    
    id = Column(Integer, primary_key=True)
    recommendation_id = Column(String, nullable=True)
    template_type = Column(String)  # delay_notice, expedite_request
    generated_text = Column(Text)
    recipient = Column(String)  # supplier/dealer name
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(Text)
    tools_used = Column(JSON, default=[])
    reasoning_steps = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)

