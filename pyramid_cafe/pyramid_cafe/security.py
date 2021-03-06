from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User


class AuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user:
            return user.id


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id:
        user = request.dbsession.query(User).get(user_id)
        return user


def get_root(_id, request):
    if _id:
        user = request.dbsession.query(User).get(_id)
        return [user.status]


def includeme(config):
    settings = config.get_settings()
    authn_policy = AuthenticationPolicy(settings['auth.secret'], callback=get_root, hashalg='sha512', )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
