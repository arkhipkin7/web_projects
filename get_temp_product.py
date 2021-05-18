import sqlalchemy

from ..models.temp_product import TempProduct
from ..models.product import Product


class GetTempProduct(object):
    def __init__(self, request):
        self.request = request

    def get_product(self):
        request = self.request
        temp_product = request.dbsession.execute("INSERT INTO temp_products SELECT * FROM products")
        return temp_product

    def get_all_temp(self):
        request = self.request
        query = request.dbsession.query(TempProduct)
        return query.order_by(sqlalchemy.asc(TempProduct.id))

    def add_temp_product_in_basket(self):
        request = self.request
        session = request.session
        id_order = session['basket_list']
        products = request.dbsession.query(TempProduct).filter(TempProduct.id.in_(id_order)).all()
        return products
