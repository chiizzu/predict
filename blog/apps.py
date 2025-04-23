from django.apps import AppConfig
import threading, asyncio

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    def ready(self):
        from .update import main

        def start_socket_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())

        threading.Thread(target=start_socket_loop, daemon=True).start()