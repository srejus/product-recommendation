# product-recommendation

Django rest framework project to recommend product to the user based on the previous orders

## How to Setup the project


1. Clone the Repo with the command <br>
        git clone https://github.com/srejus/product-recommendation.git <br>
        cd product-recommendation <br>

2. Create a virtualenv and install the required libraries from requirements.txt file  
        pip install -r requirements.txt  
  
3. Run migrate command to create the db.sqlite3  
    python manage.py migrate  
  
4. Create a superuser to access the database admin page  
    python manage.py createsuperuser  
  
5. Make migrations for the product and order modules  
    python manage.py makemigrations  
    python manage.py migrate  
  
6. Import the postman collection that is also included in the repo to your postman and login with the login api  
    URL -  {{BASE_URL}}/api/token/  
    METHOD - POST  
  
7. Run the Bulk product import api to populate the product table with some product data (You can check the admin panel to see the data)  
    URL - {{BASE_URL}}/product/populate-products/  
    METHOD - POST  
      
8. Need to create new user from the admin page(http://127.0.0.1:8000/admin)  
9. Then Populate the Order table with some order data using the following API  
    URL - {{BASE_URL}}/order/populate-orders/  
    METHOD - POST  
  
    NOTE: Check the Example in the postman to know how to pass the no of orders needed to generate  
  
10. Use the recommendation API to get the list of Products that brough together  
    URL - {{BASE_URL}}/recommendation/1/ -> here 1 is the product id  
    METHOD - GET  


