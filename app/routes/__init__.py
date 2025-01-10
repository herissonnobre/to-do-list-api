from app.routes.auth import auth_blueprint
from app.routes.tasks import tasks_blueprint


def register_blueprints(app):
    """

    :param app:
    """
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
