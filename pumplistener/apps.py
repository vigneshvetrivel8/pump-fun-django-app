# import threading
# from django.apps import AppConfig

# class PumplistenerConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'pumplistener'

#     def ready(self):
#         """
#         This method is called when Django starts.
#         We start our listener in a new daemon thread.
#         """
#         from . import listener  # Import your listener module

#         # Ensure this code runs only once, not in the reloader process
#         import os
#         if os.environ.get('RUN_MAIN', None) != 'true':
#             # Create a thread to run our listener
#             # The `daemon=True` part ensures the thread will exit when the main Django process exits
#             listener_thread = threading.Thread(
#                 target=listener.run_listener_in_new_loop, 
#                 daemon=True
#             )
#             listener_thread.start()
#             print("🚀 Started pump.fun listener thread.")

####################################################################################################################
# pumplistener/apps.py

from django.apps import AppConfig

class PumplistenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pumplistener'

# --- DELETE EVERYTHING ELSE THAT WAS HERE ---
# (Specifically, delete the "ready(self)" method that starts the thread)