from collections import Counter

from order.models import Order,OrderItem


def recommend_products(product, response_num=5):
    '''
    How this recommendation works
        -> By using the product parameter we will get all orders that contain that products
        -> By using that orders will filter all products from OrderItem table and exclude the given product
        -> sort the list of queryset based on the no of times the product get repeated
        -> Then we return the top frequently brought together products to the view
        -> return recommended_products[:response_num] here we are actually return top response_num products 
            -> for eg: if response_num=5 then we will return top 5 most repeated products
    '''
    order_ids = OrderItem.objects.filter(product=product).values_list('order__id', flat=True)
    orders = Order.objects.filter(id__in=order_ids)

    # Retrieve all order items except for the given product
    other_order_items = OrderItem.objects.filter(order__in=orders).exclude(product=product)
    products = [item.product for item in other_order_items]
    recommended_products = []
    queryset_counts = Counter(products)
    
    # Sort the unique querysets based on their occurrences in descending order
    sorted_querysets = sorted(queryset_counts.keys(), key=lambda x: queryset_counts[x], reverse=True)

    for queryset in sorted_querysets:
        recommended_products.append(queryset)

    return recommended_products[:response_num]

