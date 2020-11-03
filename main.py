from pathlib import Path
from sanic import Sanic, response

from backend.route_adding import add_routes

app = Sanic('hedgecock_dev')

main_dir = Path('.')
frontend_dir = Path('./frontend')
app.static('/', str(frontend_dir))


@app.route('/')
async def index(request):
    return await response.file(str(frontend_dir / 'index.html'))

add_routes(app)

if __name__ == "__main__":
    print('Serving at http://localhost/')
    app.run(host="0.0.0.0", port=80)
