from pyramid.view import view_config, forbidden_view_config, view_defaults
from pyramid.security import (
    remember,
    forget
)
from pyramid.httpexceptions import HTTPFound

from ..models import User, Basket

from ..Algorithms.get_product import GetProduct
from ..Algorithms.get_basket import GetBasket
from ..Algorithms.get_temp_product import GetTempProduct


# Базовые страницы
@view_defaults(route_name='home_page')
class ViewHome:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home_page', renderer='/templates/home_page.jinja2')
    def home(self):
        return {}

    # Список продуктов
    @view_config(route_name='list_products', renderer='/templates/product_list.jinja2')
    def list_products(self):
        request = self.request
        products = GetProduct(request).get_all()
        return {"products": products}

    @view_config(route_name='list_temp_products', renderer='/templates/temp_product_list.jinja2')
    def list_temp_product(self):
        request = self.request
        temp_products = GetTempProduct(request).get_all_temp()
        return {'temp_products': temp_products}


# Авторизация и регистрация
@view_defaults()
class LogInOut:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', renderer='/templates/login.jinja2')
    def login(self):
        login = ''
        message = ''
        request = self.request
        next_url = request.params.get('next', request.referrer)

        # если юзер авторизовался
        if next_url == request.route_url('login'):
            next_url = request.route_url('home_page')
        # Возвращаем на home_page
        if not next_url:
            next_url = request.route_url('home_page')

        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user = request.dbsession.query(User).filter_by(name=login).first()
            # Если юзер есть в БД
            if user is not None and user.check_password(password):
                headers = remember(request, user.id)
                return HTTPFound(location=next_url, headers=headers)
            message = 'LogIn is Invalid'
        return {'message': message,
                'url': request.route_url('login'),
                'next_url': next_url,
                'login': login
                }

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        next_url = request.route_url('login')
        return HTTPFound(location=next_url, headers=headers)

    @forbidden_view_config()
    def forbidden_view(self):
        request = self.request
        next_url = request.route_url('login', _query={'next': request.url})
        return HTTPFound(location=next_url)

    @view_config(route_name='sign_up', renderer='/templates/sign_up.jinja2')
    def sign_up(self):
        request = self.request
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            status = request.params['status']
            user = User(name=login, status=status)
            user.set_password(password)
            request.dbsession.add(user)
            request.session.flash('Registration completed successfully')
            return HTTPFound(location=request.route_url('login'))
        return {}


# View для админа
@view_defaults()
class ViewAdmin:
    def __init__(self, request):
        self.request = request

    # Посмотреть все заказы(Админ)
    @view_config(route_name='basket_list', renderer='/templates/basket_list.jinja2', permission='admin')
    def basket_list(self):
        baskets = GetBasket(self.request).get_all()
        return {'baskets': baskets}

    # Удалить заказ
    @view_config(route_name='delete_basket', permission='admin')
    def delete_basket(self):
        request = self.request
        id_basket = int(request.matchdict['id'])
        GetBasket(request).delete(id_basket)
        request.session.flash('Basket Removed')
        return HTTPFound(location=request.route_url('basket_list'))

    @view_config(route_name='info_about_users', renderer='/templates/info_about_users.jinja2', permission='admin')
    def info_about_users(self):
        orders = GetBasket(self.request).get_by_month()
        return {'orders': orders}

    @view_config(route_name='search', renderer='/templates/search.jinja2', permission='admin')
    def search(self):
        uuid = self.request.matchdict['uuid']
        result_search = self.request.dbsession.query(Basket).filter_by(qrcode=uuid).all()
        return {'result_search': result_search}


# View для программиста
@view_defaults(route_name='add_product')
class ViewDeveloper:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='my_basket', renderer='/templates/my_basket.jinja2', permission='developer')
    def my_basket(self):
        my_baskets = GetBasket(self.request).get_user_basket()
        return {'my_baskets': my_baskets}

    # Добавить продукт в корзину
    @view_config(route_name='add_product', permission='developer')
    def add_product(self):
        request = self.request
        session = request.session
        id_order = int(request.matchdict['id'])
        if 'basket_list' in session:
            session['basket_list'].append(id_order)
        else:
            session['basket_list'] = [id_order]
        return HTTPFound(location=request.route_url('list_products'))

    # Офрмление заказа
    @view_config(route_name='checkout', permission='developer')
    def checkout(self):
        request = self.request
        if 'form.submitted' in request.params:
            price = request.params['price']
            data = request.params['data']
            GetBasket(request).add(data, price)
            del request.session['basket_list']
            return HTTPFound(location=request.route_url('basket'))
        return HTTPFound(location=request.route_url('home_page'))

    # Корзина
    @view_config(route_name='basket', renderer='/templates/basket.jinja2', permission='developer')
    def basket(self):
        request = self.request
        session = request.session
        basket_body = ''
        _sum = 0

        GetTempProduct(request).get_product()

        if 'basket_list' in session:
            products = GetTempProduct(request).add_temp_product_in_basket()
            for product in products:
                basket_body += product.name + ' '
                _sum = _sum + product.price
            return {'basket_body': basket_body,
                    '_sum': _sum,
                    'products': products,
                    }
        else:
            return HTTPFound(location=request.route_url('home_page'))
