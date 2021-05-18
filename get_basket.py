import datetime
import sqlalchemy
import pyqrcode
import uuid
import os
import dateutil.relativedelta

from ..models import Basket, User

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GetBasket(object):
    def __init__(self, request):
        self.request = request

    def get_all(self):
        request = self.request
        query = request.dbsession.query(Basket)
        return query.order_by(sqlalchemy.desc(Basket.datetime))

    def add(self, data, price):
        request = self.request
        basket = Basket(data=data, price=price, creator=request.user, datetime=datetime.datetime.now())
        request.dbsession.add(basket)
        request.dbsession.flush()
        request.dbsession.refresh(basket)
        basket_id = basket.id

        qr = str(uuid.uuid1())
        qrcode = pyqrcode.create(qr)

        # Путь к директории
        path = os.path.join(project_path, 'static') + '\\' + qr + '.svg'
        qrcode.svg(path, scale=2)

        basket = request.dbsession.query(Basket).filter_by(id=basket_id).one()
        basket.qrcode = qr

    def get_user_basket(self):
        baskets = self.request.dbsession.query(Basket).filter_by(creator=self.request.user).all()
        return baskets

    def delete(self, basket_id):
        request = self.request
        request.dbsession.query(Basket).filter_by(id=basket_id).delete()

    def get_by_month(self):
        today = datetime.datetime.today()
        end_month = today - dateutil.relativedelta.relativedelta(month=+1)
        base_query = self.request.dbsession.query(User.name, sqlalchemy.func.sum(Basket.price).label('sum')).join(
            Basket.creator).filter(Basket.datetime < today).filter(Basket.datetime > end_month).group_by(User.name)

        orders = [{'username': row[0], 'sum': row[1]}
                  for row in base_query.all()]
        return orders
