**Points**

+ Some points are not fully covered due to time constraints
+ Better permissions logic should be implemented
+ Analytics is not implemented, howere in case we implement it it should run on slave DB to not load our Master Database
+ Pagination is not implemented
+ API calls from Swagger UI not working due to JWT issue in header. Could go with drf_spectacular instead of drf-yasg which provices JWT and openapiv3 instead of v2. But not changing now due to time constraint. Adding POSTMAN collection for API testing. You can USE SWAGGER UI for auth toen and endpoints View.
+ Database tables and system architecture are added in the images.
+ Basic doker file added, it can be opimized a lot


***Assumptions***

    + Some businees logic quesions are added with tag 'NOTE'
    + Products price we cannot change after making it active.
    + If we require product price change after making it active, we need more colums in order_items (product_price_at_order_time) to get rid of disterpencies in future.


**Deployment and usage**

+ cd ecommerce_project
+ docker build -t rohit_ecommerce .
+ docker run -p 8000:8000 rohit_ecommerce
+ Admin Interface: http://127.0.0.1:8000/admin
+ Swagger UI Interface: http://127.0.0.1:8000/docs/
+ Can use Postman Collection to hit API Endpoints