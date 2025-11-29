# app/routes.py
from app.utils import render_template
from app import config

def register_routes(app):
    """
    Registers all the application routes.
    """
    @app.route('/')
    def index(request):
        # Render the main page
        return render_template(
            'index.html',
            app_name=config.APP_NAME,
            app_version=config.APP_VERSION,
            status="System OK"
        ), {'Content-Type': 'text/html'}

    @app.route('/shutdown')
    def shutdown(request):
        # This is a simple way to allow shutting down the server.
        # In a real app, you'd want security around this.
        print("Shutdown requested from web.")
        app.shutdown()
        return "Server shutting down..."

    # Example of a JSON API endpoint
    @app.route('/api/status')
    def api_status(request):
        return {
            'app_name': config.APP_NAME,
            'version': config.APP_VERSION,
            'status': 'ok'
        }
