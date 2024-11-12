import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iihc_website_portal.settings')
application = get_asgi_application()



# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from website_portal.consumers import YourConsumer  

# # Set the default settings module for the Django application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iihc_website_portal.settings')

# # Create the Django ASGI application
# django_asgi_app = get_asgi_application()

# # Define the routing for different protocols
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,  # Handle HTTP requests with the Django ASGI application
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             [
#                 path("ws/somepath/", YourConsumer.as_asgi()),  # Define WebSocket path and consumer
#                 # Add more WebSocket paths here as needed
#             ]
#         )
#     ),
# })