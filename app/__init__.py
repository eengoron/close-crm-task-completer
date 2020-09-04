from flask import Flask

from .methods import setup_integration_webhooks

app = Flask(__name__)

from app import routes
setup_integration_webhooks()

if __name__ == '__main__':
    app.run(use_reloader=False, debug=True)
