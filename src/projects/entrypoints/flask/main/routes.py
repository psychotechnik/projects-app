from projects.entrypoints.flask.main import bp


@bp.route('/', methods=['GET'])
def index():
    return {"status": "ok"}
