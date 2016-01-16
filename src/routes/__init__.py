import falcon

# falcon.API instances are callable WSGI apps
app = falcon.API()

from . import mapinfo

# things will handle all requests to the matching URL path
app.add_route('/maps-info', mapinfo.MapInfo)
