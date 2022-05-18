# from decimal import Decimal
# from django.conf import settings
# from account.models import Worker_card
#
#
# class Cart(object):
#
#     def __init__(self, request):
#         """
#         Инициализируем корзину
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             # save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#
# def add(self, worker_card, quantity=1, update_quantity=False):
#     """
#     Добавить продукт в корзину или обновить его количество.
#     """
#     worker_card_id = str(Worker_card.id)
#     if worker_card_id not in self.cart:
#         self.cart[worker_card_id] = {'quantity': 0}
#     if update_quantity:
#         self.cart[worker_card_id]['quantity'] = quantity
#     else:
#         self.cart[worker_card_id]['quantity'] += quantity
#     self.save()
#
# def save(self):
#     # Обновление сессии cart
#     self.session[settings.CART_SESSION_ID] = self.cart
#     # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
#     self.session.modified = True
#
#
# def remove(self, worker_card):
#     """
#     Удаление товара из корзины.
#     """
#     worker_card_id = str(worker_card.id)
#     if worker_card_id in self.cart:
#         del self.cart[worker_card_id]
#         self.save()
#
#
# def __iter__(self):
#     """
#     Перебор элементов в корзине и получение продуктов из базы данных.
#     """
#     worker_card_ids = self.cart.keys()
#     # получение объектов product и добавление их в корзину
#     worker_cards = Worker_card.objects.filter(id__in=worker_card_ids)
#     for worker_card in worker_cards:
#         self.cart[str(worker_card.id)]['product'] = worker_card
#
#
#
# def __len__(self):
#     """
#     Подсчет всех товаров в корзине.
#     """
#     return sum(item['quantity'] for item in self.cart.values())
#
# def clear(self):
#     # удаление корзины из сессии
#     del self.session[settings.CART_SESSION_ID]
#     self.session.modified = True
