"""
.. module: lemur
    :platform: Unix
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.

.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>


"""
from flask import jsonify

from lemur import factory

from lemur.users.views import mod as users_bp
from lemur.roles.views import mod as roles_bp
from lemur.auth.views import mod as auth_bp
from lemur.domains.views import mod as domains_bp
from lemur.elbs.views import mod as elbs_bp
from lemur.accounts.views import mod as accounts_bp
from lemur.authorities.views import mod as authorities_bp
from lemur.listeners.views import mod as listeners_bp
from lemur.certificates.views import mod as certificates_bp
from lemur.status.views import mod as status_bp

LEMUR_BLUEPRINTS = (
    users_bp,
    roles_bp,
    auth_bp,
    domains_bp,
    elbs_bp,
    accounts_bp,
    authorities_bp,
    listeners_bp,
    certificates_bp,
    status_bp
)

def create_app(config=None):
    app = factory.create_app(app_name=__name__, blueprints=LEMUR_BLUEPRINTS, config=config)
    configure_hook(app)
    return app


def configure_hook(app):
    """

    :param app:
    :return:
    """
    from flask.ext.principal import PermissionDenied
    from lemur.decorators import crossdomain
    if app.config.get('CORS'):
        @app.after_request
        @crossdomain(origin="http://localhost:3000", methods=['PUT', 'HEAD', 'GET', 'POST', 'OPTIONS', 'DELETE'])
        def after(response):
            return response

    @app.errorhandler(PermissionDenied)
    def handle_invalid_usage(error):
        response = {'message': 'You are not allow to access this resource'}
        response.status_code = 403
        return response





