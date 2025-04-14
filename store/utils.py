import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart : ', cart)
    items = []
    order = {'get_cart_total' : 0, 'get_cart_items' : 0, 'shipping' : False}
    
    for i in cart:
        try:
            quantity_of_row = cart[i]['quantity']
            product = Product.objects.get(id=i)
            total_of_row = product.price * quantity_of_row
            order['get_cart_total'] += total_of_row
            order['get_cart_items'] += quantity_of_row

            item = {
                'product' : {
                    'id' : product.id,
                    'name' : product.name,
                    'price' : product.price,
                    'imageURL' : product.imageURL,
                    },
                    'quantity' : quantity_of_row,
                    'get_total' : total_of_row
                    }   
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass 

    cartItems = order['get_cart_items']
    return {'items': items, 'order': order , 'cartItems': cartItems}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
    return{'items': items, 'order': order , 'cartItems': cartItems}



def guestOrder(request,data):
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])
        print('User is not logged in')

    return customer,order

