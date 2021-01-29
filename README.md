# Abacies APP

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/arunjohn96/Abacies.git
$ cd app
```
Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p path/to/python/x.x env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`
Here you will be able to access `DRF Browsable API Root Page`, where all the API's are listed.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```

## API Doc

#### Product List APIs
View list of all Products present in Products table
```sh
GET - http://localhost:8000/products/
```
Create a new Product using  `Product ID`, `Product Name`, `Quantity` & `Unit Price` in the Products table
```sh
POST - http://localhost:8000/products/   

payload:    {
            "product_id": null,
            "name": "",
            "quantity": null,
            "unit_price": null
            }
```

#### Product Details APIs
Get the details of a product
```sh
GET - http://localhost:8000/products/{pk}/
```
Update the product details
```sh
PUT - http://localhost:8000/products/{pk}/   

payload:    {
            "product_id": 100100502,
            "name": "100502 Product 100502",
            "quantity": 24803,
            "unit_price": "12383.00"
            }
```
Delete a product from the Products table
```sh
DELETE - http://localhost:8000/products/{pk}/
```

#### Purchase List APIs
View list of all records available in the Purchase Transactions Table
```sh
GET - http://localhost:8000/purchases/
```
Create a new record in Purchase Transactions table using `Product Id`, `Purchase ID` & `Purchased Quantity`
```sh
POST - http://localhost:8000/purchases/   

payload:    {
            "product_id": null,
            "purchase_id": "",
            "purchased_quantity": null
            }
```

#### Purchase Details APIs
Get Details of a Purchase record in Purchase Transactions Table
```sh
GET - http://localhost:8000/purchases/{pk}/
```
Update `Purchase Quantity` of existing record in Purchase Transactions table
```sh
PUT - http://localhost:8000/purchases/{pk}/

payload:    {
            "purchase_quantity": 2001,
            }
```
Delete a record in Purchase Transactions table
```sh
DELETE - http://localhost:8000/purchases/{pk}/
```

#### CSV DATA APIs
In settings.py, set location of csv file to `CSV_FILE_PATH` variable
Create products from CSV Data if the products doesnt exist in DB
```sh
POST - http://localhost:8000/import/csv/products/
```
Create Purchase Transactions and deduct stock from Products table using CSV data
```sh
POST - http://localhost:8000/import/csv/purchase_transactions/
```

#### Refill Stock Count API
Refill stock count in Products Table by giving `Product ID` & `Refill Count`
```sh
POST - http://localhost:8000/refill/

payload     {
            "product_id": 105001,
            "refill_count": 1500,
            }
```
