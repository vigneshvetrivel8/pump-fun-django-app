# pumplistener/management/commands/run_pump_listener.py

import asyncio
import websockets
import json
import time
from django.core.management.base import BaseCommand

# --- CONFIGURATION ---
PUMPORTAL_WSS = "wss://pumpportal.fun/api/data"

async def pump_fun_listener():
    """
    Connects to the PumpPortal WebSocket and prints new token creation events.
    This is the core asynchronous logic.
    """
    print("🚀 Starting Pump.fun New Token Monitor (as a standalone worker)...")
    print(f"Connecting to WebSocket: {PUMPORTAL_WSS}")
    
    try:
        # Establish a persistent connection
        async with websockets.connect(PUMPORTAL_WSS) as websocket:
            print("✅ Successfully connected to WebSocket.")
            
            # Subscribe to the new token stream
            subscribe_message = {"method": "subscribeNewToken"}
            await websocket.send(json.dumps(subscribe_message))
            print("✅ Subscribed to new token stream. Waiting for launches...\n")

            # Loop forever, processing messages
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)

                    # Check for 'create' events and print details
                    if data and data.get('txType') == 'create':
                        print("=============================================")
                        print(f"🔥 New Token Creation Detected!")
                        print(f"   -> Name: {data.get('name', 'N/A')} (${data.get('symbol', 'N/A')})")
                        print(f"   -> Mint Address: {data.get('mint', 'N/A')}")
                        print(f"   -> Creator Invested: {data.get('solAmount', 0):.2f} SOL")
                        print(f"   -> Creator: {data.get('traderPublicKey', 'N/A')}")
                        print(f"   -> Link: https://pump.fun/{data.get('mint', '')}")
                        print("=============================================\n")

                except websockets.ConnectionClosed:
                    print("⚠️ WebSocket connection closed by server. Will attempt to reconnect...")
                    break # Exit the inner loop to trigger the reconnection logic in handle()
                except Exception as e:
                    print(f"💥 An error occurred while processing a message: {e}")

    except Exception as e:
        print(f"💥 Failed to connect to WebSocket: {e}")


class Command(BaseCommand):
    """
    Defines the Django management command `run_pump_listener`.
    """
    help = 'Runs the pump.fun WebSocket listener as a standalone background worker.'

    def handle(self, *args, **options):
        """
        The entry point for the management command.
        It runs the async listener in a resilient, looping manner.
        """
        self.stdout.write(self.style.SUCCESS("Starting the pump.fun listener loop..."))
        
        # This outer loop ensures that if the listener function ever exits
        # (e.g., due to a connection drop), it will wait and restart.
        while True:
            try:
                # Run the main asynchronous function
                asyncio.run(pump_fun_listener())
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Listener stopped manually."))
                break
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Listener crashed with a critical error: {e}"))
            
            self.stdout.write(self.style.NOTICE("Listener process finished. Reconnecting in 10 seconds..."))
            time.sleep(10)