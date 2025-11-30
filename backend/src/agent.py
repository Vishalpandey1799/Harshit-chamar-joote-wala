import logging
import json
import os
from datetime import datetime, date
from typing import Dict, Any, Optional, List

import asyncio
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("ecom_agent")
logging.basicConfig(level=logging.INFO)

load_dotenv(".env")

 

def load_catalog():
    try:
        with open("shared-data/catelog.json", "r") as f:
            return json.load(f)
    except:
        return []

CATALOG = load_catalog()
ORDERS_FILE = "shared-data/orders.json"


def save_catalog():
    with open("shared-data/catelog.json", "w") as f:
        json.dump(CATALOG, f, indent=2)


def load_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


 

def build_system_prompt() -> str:
    return """
You are a voice-based shopping assistant.
Use the provided tools to browse products, create orders, cancel orders, 
cancel individual items, or calculate totals.
Keep responses short and natural for voice.
"""


 

class EcomAgent(Agent):
    def __init__(self):
        super().__init__(instructions=build_system_prompt())

    # ------------------------------------------------------------
    # LIST PRODUCTS
    # ------------------------------------------------------------
    @function_tool
    async def list_products(self, ctx: RunContext, filters: Optional[Dict[str, Any]] = None):
        results = CATALOG

        if filters:
            if "category" in filters:
                results = [p for p in results if p.get("category") == filters["category"]]
            if "color" in filters:
                results = [p for p in results if p.get("color") == filters["color"]]
            if "max_price" in filters:
                results = [p for p in results if p.get("price") <= filters["max_price"]]

        return results

 
    @function_tool
    async def create_order(self, ctx: RunContext, line_items: List[Dict[str, Any]]):

        # Validate before modifying stock
        for item in line_items:
            pid = item.get("product_id")
            qty = item.get("quantity", 1)
            size = item.get("size")

            product = next((p for p in CATALOG if p["id"] == pid), None)
            if not product:
                return {"error": "Invalid product id"}

       
            if product.get("sizes") and not size:
                return {
                    "needs_size": True,
                    "product_id": pid,
                    "available_sizes": product.get("sizes", [])
                }

     
            if product.get("stock", 0) < qty:
                return {"error": f"Only {product['stock']} left in stock"}

        # Create order now
        order_id = os.urandom(8).hex()
        order_items = []
        total = 0

        for item in line_items:
            pid = item["product_id"]
            qty = item.get("quantity", 1)
            size = item.get("size")

            product = next((p for p in CATALOG if p["id"] == pid), None)

            # Deduct stock
            product["stock"] -= qty

            order_items.append({
                "product_id": pid,
                "name": product["name"],
                "quantity": qty,
                "unit_price": product["price"],
                "size": size,
                "currency": product.get("currency", "INR")
            })

            total += product["price"] * qty

        save_catalog()

        new_order = {
            "id": order_id,
            "items": order_items,
            "total": total,
            "currency": "INR",
            "created_at": datetime.utcnow().isoformat(),
            "status": "CONFIRMED"
        }

        all_orders = load_orders()
        all_orders.append(new_order)
        save_orders(all_orders)

        return new_order

 
    @function_tool
    async def cancel_order(self, ctx: RunContext, order_id: str):

        all_orders = load_orders()
        order = next((o for o in all_orders if o["id"] == order_id), None)

        if not order:
            return {"error": "Order not found"}

        if order.get("status") == "CANCELLED":
            return {"message": "Order is already cancelled"}

        # Restore stock
        for item in order["items"]:
            product = next((p for p in CATALOG if p["id"] == item["product_id"]), None)
            if product:
                product["stock"] += item["quantity"]

        save_catalog()

        order["status"] = "CANCELLED"
        save_orders(all_orders)

        return {
            "message": "Order cancelled and stock restored",
            "order_id": order_id
        }
 
 
    @function_tool
    async def cancel_order_item(
        self,
        ctx: RunContext,
        order_id: str,
        product_id: str
    ):
        all_orders = load_orders()
        order = next((o for o in all_orders if o["id"] == order_id), None)

        if not order:
            return {"error": "Order not found"}

        if order.get("status") == "CANCELLED":
            return {"error": "Order is already cancelled"}

        item = next((i for i in order["items"] if i["product_id"] == product_id), None)

        if not item:
            return {"error": "Product not found in this order"}

        # Restore stock for this one item
        qty = item["quantity"]
        product = next((p for p in CATALOG if p["id"] == product_id), None)

        if product:
            product["stock"] += qty
            save_catalog()

        # Remove item
        order["items"].remove(item)

        # Recalculate total
        order["total"] = sum(i["unit_price"] * i["quantity"] for i in order["items"])

        # If order empty → fully cancelled
        if len(order["items"]) == 0:
            order["status"] = "CANCELLED"

        save_orders(all_orders)

        return {
            "message": "Item removed from order",
            "order_id": order_id,
            "removed_product_id": product_id,
            "new_total": order["total"]
        }

   
    @function_tool
    async def get_total_spent(self, ctx: RunContext):

        orders = load_orders()
        confirmed = [o for o in orders if o.get("status") == "CONFIRMED"]

        total = sum(o["total"] for o in confirmed)

        return {
            "total_spent": total,
            "currency": "INR",
            "order_count": len(confirmed)
        }
 
    @function_tool
    async def get_total_today(self, ctx: RunContext):

        today = date.today()
        orders = load_orders()

        total = 0
        count = 0

        for o in orders:
            created = datetime.fromisoformat(o["created_at"]).date()
            if created == today and o.get("status") == "CONFIRMED":
                total += o["total"]
                count += 1

        return {
            "total_spent_today": total,
            "currency": "INR",
            "orders_today": count
        }


 

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    print(">>> [BOOT] E-commerce Agent starting...")

    vad = ctx.proc.userdata["vad"]

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=vad,
        preemptive_generation=True,
    )

    await ctx.connect()

    await session.start(
        agent=EcomAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm
        )
    )
