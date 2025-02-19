# E-Commerce API

This is a Django-based RESTful API for an e-commerce platform, providing authentication, product management, order handling, and cart functionalities.

## Features
- User authentication (register, login)
- Product and category management
- Order management (create, update, cancel, search)
- Cart management (add, edit, remove items, clear cart)
- API documentation using **drf-spectacular**

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/ecommerce-api.git
   cd ecommerce-api
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Authentication
| Endpoint                | Method | Description        |
|-------------------------|--------|--------------------|
| `/api/v1/users/register/` | POST   | Register a new user |
| `/api/v1/users/login/`    | POST   | Login user         |
| `/api/v1/users/`         | GET    | List all users     |
| `/api/v1/users/detail/<uuid:pk>/` | GET  | Retrieve user details |

### Product & Category
| Endpoint                      | Method | Description               |
|--------------------------------|--------|---------------------------|
| `/api/v1/category/`           | GET    | List all categories       |
| `/api/v1/category/`           | POST   | Create a new category     |
| `/api/v1/category/<uuid:pk>/`           | PUT   | Update a  category     |
| `/api/v1/category/<uuid:pk/`           | DELETE   | Delete a  category     |
| `/api/v1/products/`           | GET    | List all products         |
| `/api/v1/products/`           | POST   | Add a new product         |
| `/api/v1/products/<uuid:pk>/`           | PUT   | Update a  product     |
| `/api/v1/products/<uuid:pk/`           | DELETE   | Delete a  product     |



### Orders
| Endpoint                          | Method | Description             |
|------------------------------------|--------|-------------------------|
| `/api/v1/orders/create/`          | POST   | Create a new order      |
| `/api/v1/orders/`                 | GET    | List all orders        |
| `/api/v1/orders/<uuid:pk>/`       | GET    | Retrieve order details  |
| `/api/v1/orders/<uuid:pk>/edit/`  | PUT    | Update an order        |
| `/api/v1/orders/<uuid:pk>/cancel/`| POST   | Cancel an order        |
| `/api/v1/orders/search/`          | GET    | Search for an order    |

### Cart
| Endpoint                                    | Method | Description                    |
|--------------------------------------------|--------|--------------------------------|
| `/api/v1/carts/add/`                      | POST   | Add an item to the cart       |
| `/api/v1/carts/`                          | GET    | List cart items               |
| `/api/v1/carts/<uuid:pk>/clear/`         | POST   | Clear a specific cart         |
| `/api/v1/carts/session-clear/`           | POST   | Clear session cart            |
| `/api/v1/carts/item/<uuid:pk>/remove/`   | POST   | Remove an item from cart      |
| `/api/v1/carts/item/<uuid:pk>/edit/`     | PUT    | Edit an item in cart          |
| `/api/v1/carts/item/<uuid:product_id>/update/` | PUT   | Update session cart item |
| `/api/v1/carts/item/<uuid:product_id>/delete/` | DELETE | Remove session cart item |

---
### API Documentation
The API is documented using `drf-spectacular`. The schema can be accessed at:
- **Schema:** `/schema/`
- **Swagger UI:** `/`

## License
This project is licensed under the MIT License.

## Author
Developed by **Esezobor Osemen**

Happy coding! 🚀

