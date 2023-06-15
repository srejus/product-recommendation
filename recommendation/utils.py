import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from order.models import Order,OrderItem


def recommend_products(user,response_num=5):
    # Retrieve all orders for the given user
    orders = Order.objects.all()
    user_orders = orders.filter(customer=user)

    # Retrieve all orders except for the user's orders
    other_orders = orders.exclude(customer=user)

    # Create a dataframe to store the orders data
    orders_data = []
    for order in other_orders:
        orders_data.append([order.total_amount, order.rating])
    orders_df = pd.DataFrame(orders_data, columns=['total_amount', 'rating'])

    # Normalize the order data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(orders_df)

    # Create a dataframe for the user's orders
    user_orders_data = []
    for order in user_orders:
        user_orders_data.append([order.total_amount, order.rating])
    user_orders_df = pd.DataFrame(user_orders_data, columns=['total_amount', 'rating'])
    
    # Normalize the user's order data
    normalized_user_data = scaler.transform(user_orders_df)

    # Calculate the cosine similarity between the user's orders and all other orders
    similarities = cosine_similarity(normalized_user_data, normalized_data)

    # Get the indices of the most similar orders
    similar_indices = similarities.argsort()[0][::-1]

    # Recommend the top 5 products to the user
    recommended_orders = []
    for index in similar_indices[:response_num]:
        order = other_orders[int(index)]
        recommended_orders.append(order)

    recommended_order_ids = [order.id for order in recommended_orders]
    recommended_order_items = OrderItem.objects.filter(order__id__in = recommended_order_ids)
    recommended_products = [item.product for item in recommended_order_items]
    
    return recommended_products


def calculate_accuracy(actual_products, recommended_products):
    correct_predictions = 0
    for product in recommended_products:
        if product in actual_products:
            correct_predictions += 1

    accuracy = correct_predictions / len(recommended_products) * 100
    return accuracy

