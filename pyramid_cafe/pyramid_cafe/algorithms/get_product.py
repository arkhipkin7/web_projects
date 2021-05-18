import sqlalchemy

from ..models.product import Product


class GetProduct(object):
    def __init__(self, request):
        self.request = request

    def get_all(self):
        request = self.request
        query = request.dbsession.query(Product)
        return query.order_by(sqlalchemy.asc(Product.id))
