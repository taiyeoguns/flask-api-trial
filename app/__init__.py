import connexion
from flask import Blueprint, redirect

from app.extensions import cache, db, migrate
from config import Config

app_bp = Blueprint("app", __name__)


@app_bp.route("/")
def index():
    return redirect(f"{Config.API_VERSION}/docs/")


def create_app(cfg=Config):
    app = connexion.FlaskApp(
        __name__, specification_dir="../openapi", options={"swagger_url": "/docs"}
    )

    # get flask app object
    flask_app = app.app

    # load config
    flask_app.config.from_object(cfg)

    # initialize extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    cache.init_app(flask_app)

    with flask_app.app_context():
        from app import models  # noqa

    # register blueprints
    flask_app.register_blueprint(app_bp)

    # add api spec to connexion
    app.add_api("v1.yml", base_path="/v1")

    return app


flask_app = create_app().app
