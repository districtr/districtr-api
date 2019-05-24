from .places import bp as places
from .plans import bp as plans, list_my_plans
from .register import bp as register_bp
from .requests import bp as place_requests
from .tokens import bp as tokens
from .users import bp as users


def register_blueprints(app):
    app.register_blueprint(plans, url_prefix="/plans")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(places, url_prefix="/places")
    app.register_blueprint(tokens, url_prefix="/tokens")
    app.register_blueprint(place_requests, url_prefix="/requests")
    app.register_blueprint(register_bp)
    app.add_url_rule("/user/plans/", "list_my_plans", list_my_plans)
