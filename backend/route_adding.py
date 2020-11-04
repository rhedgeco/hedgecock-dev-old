from sanic import Sanic

from backend.ice_cream_or_pickle.ice_cream_or_pickle import IceCreamOrPickle


def add_routes(app: Sanic):
    app.add_route(IceCreamOrPickle.as_view(), '/ice_cream_or_pickle')