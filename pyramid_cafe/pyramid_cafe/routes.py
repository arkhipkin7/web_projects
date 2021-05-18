def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Для всех
    config.add_route('home_page', '/')
    config.add_route('list_products', '/list')
    config.add_route('list_temp_products', '/list_temp')

    # Авторизация
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('sign_up', '/signup')

    # Для пользователя
    config.add_route('add_product', '/order/{id}')
    config.add_route('basket', '/basket')
    config.add_route('checkout', '/checkout')
    config.add_route('my_basket', '/my_basket')

    # Для админа
    config.add_route('basket_list', '/basket_list')
    config.add_route('delete_basket', '/delete/{id}')
    config.add_route('info_about_users', '/info_about_users')
    config.add_route('search', '/search/{uuid}')
