from pathlib import Path
from sanic import Sanic, response

from routing.route_adding import add_routes

app = Sanic('hedgecock_dev')

main_dir = Path('.')
add_routes(app)


if __name__ == "__main__":
    print('Serving at http://localhost/')
    app.run(host="0.0.0.0", port=80)
