# .enc References
```
SECRET_KEY=SOME_SECRET_KEY

DB_NAME=online_shop
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_ENGINE=django.db.backends.postgresql
```

API Endpoints

# Authentication

Method: POST
URL: ``` api/token/ ```
Description: Use the received access token

# Category Endpoints

## List Categories
Method: GET
URL: ```/api/categories/ ```

## Create Category
Method: POST
URL: ```/api/categories/ ```
Body:
```
{
  "name": "Electronics"
}
```


# Subcategory Endpoints

## List Subcategories
Method: GET
URL: ``` /api/subcategories/ ```

## Create Subcategory
Method: POST
URL: ``` /api/subcategories/ ```
Body:
```
{
  "name": "Laptops",
  "category": 1  // ID of the parent category
}
```


# Product Endpoints

## List Products
Method: GET
URL: ``` /api/products/ ```
Description: Use query params category={id}, subcategory=2 for filtration and page={number_of_pahe}, page_size={size} for pagination

## Create Product
Method: POST
URL: ``` /api/products/ ```
Body:
```
{
  "name": "iPhone 13",
  "category": 1,
  "subcategory": 1,
  "price": 999.99,
  "discount_percentage": 10.0,
  "stock": 100,
  "reserved": 4,
  "sold": 0
}
```

## Change Product Price
Method: PATCH
URL: ``` /api/products/{id}/change_price/ ```
Body:
```
{
  "price": 899.99
}
```

## Start Product Discount
Method: PATCH
URL: ``` /api/products/{id}/start_discount/ ```
Body:
```
{
  "discount": 15.0
}
```

# Reserve Product
Method: POST
URL: ``` /api/products/{id}/reserve/ ```
```
{
  "quantity": 5
}
```

## Cancel Product Reservation
Method: POST
URL: ``` /api/products/{id}/cancel_reserve/ ```
Body:
```
{
  "quantity": 2
}
```

## Sell Product
Method: POST
URL: ``` /api/products/{id}/sell/ ```
Body:
```
{
  "quantity": 3
}
```
## Delete Product
Method: DELETE
URL: ``` /api/products/{id}/ ```

## Sales Report
Method: GET
URL: api/products/sales_report?category={id}&subcategory={id}
Query Params: date_from, date_to, category, subcategory


## Add Category to Product
Method: PATCH
URL: ``` api/products/{id}/update_category/ ```
Body:
```
{
    "category": {id}
}
```

## Add Subcategory to Product
Method: PATCH
URL: ``` api/products/{id}/update_subcategory/ ```
Body:
```
{
    "subcategory": {id}
}
```