# from delete_views import delete_routes
# from patch_views import patch_routes
# from post_views import post_routes
from get_views import get_routes 

def init_app(app):
    get_routes(app)
    # post_routes(app)
    # patch_routes(app)
    # delete_routes(app)
