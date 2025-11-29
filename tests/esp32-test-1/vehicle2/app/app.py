# app/app.py
from microdot import MicroDot

def create_app():
    """
    Application factory for creating the MicroDot app instance.
    """
    app = MicroDot()

    # Import and register routes
    from app import routes
    routes.register_routes(app)
    
    # You can initialize other components here, e.g.:
    # from app import database
    # database.init_app(app)

    return app
