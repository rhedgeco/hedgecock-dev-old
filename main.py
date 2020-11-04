from pathlib import Path
from sanic import Sanic, response

from backend.route_adding import add_routes
from backend.templating.template_router import \
    define_frontend_routes_with_templates

app = Sanic('hedgecock_dev')

main_dir = Path('.')
frontend_dir = Path('./frontend')
template_dir = Path('./templates')
define_frontend_routes_with_templates(app, frontend_dir, template_dir)

add_routes(app)

if __name__ == "__main__":
    print('Serving at http://localhost/')
    app.run(host="0.0.0.0", port=80)
