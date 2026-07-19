import asyncio
import logging
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.triggers import every, TriggerContext
from database import SessionLocal
from models import Shipment

logging.basicConfig(level=logging.INFO)

async def periodic_health_check(ctx: TriggerContext):
    """Scan for anomalies and log alerts every 60 seconds."""
    db = SessionLocal()
    try:
        delayed = db.query(Shipment).filter(Shipment.current_eta > Shipment.original_eta).count()
        if delayed > 0:
            logging.warning(f"[BACKGROUND AGENT ALERT] Detected {delayed} delayed shipments! Supply chain at risk.")
    except Exception as e:
        logging.error(f"Error in background check: {e}")
    finally:
        db.close()

timer_trigger = every(60, periodic_health_check)

config = LocalAgentConfig(
    system_instructions="You are a proactive background monitor scanning for anomalies.",
    triggers=[timer_trigger],
)

async def start_background_agent():
    try:
        async with Agent(config) as agent:
            # Keep the agent alive to let triggers run
            while True:
                await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logging.info("Background agent cancelled.")
