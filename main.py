from pathlib import Path
from sanic import Sanic, response

from backend.frontend_updater import FrontendUpdater
from backend.route_adding import add_routes

app = Sanic('hedgecock_dev')

main_dir = Path('.')
frontend_dir = Path('./frontend')
app.static('/', str(frontend_dir))


@app.route('/')
async def index(request):
    return await response.file(str(frontend_dir / 'index.html'))

add_routes(app)

frontend_updater = FrontendUpdater(main_dir, frontend_dir)
app.add_route(frontend_updater.update_frontend, '/api/update_frontend',
              methods=['POST'])

if __name__ == "__main__":
    print('Serving at http://localhost/')
    app.run(host="0.0.0.0", port=80)
