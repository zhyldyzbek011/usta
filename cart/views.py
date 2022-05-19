# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
# from account.models import Worker_card
# from .cart import Cart
# from .forms import CartAddCardForm
#
#
# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     worker_card = get_object_or_404(Worker_card, id=worker_card_id)
#     form = CartAddCardForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(worcer_card=worker_card,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('cart:cart_detail')