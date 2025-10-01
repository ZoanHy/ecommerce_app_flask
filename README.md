# E-Commerce Flask Application

This is a full-featured e-commerce web application built with Flask, SQLite, and Bootstrap.

## Features

### Authentication & User Management

- User Registration (`/register`)
- User Login (`/login`)
- User Logout (`/logout`)
- Account Management (`/account`)
  - View and update user profile information

### Product Management

- Product Listing on Homepage (`/`)
  - Display all available products
  - Product grid view with images and details
- My Products Management (`/my-product`)
  - Add new products
  - Edit existing products
  - Delete products
  - Image upload functionality
    - Supported formats: PNG, JPG, JPEG, GIF
    - Max file size: 1MB

### Shopping Features

- Shopping Cart Functionality
  - Add products to cart
  - Update quantities
  - Remove items
  - Calculate total price
- Product Details View
- Checkout Process

### Additional Pages

- Blog (`/blog`)
- Blog Detail (`/blog-detail`)
- Contact Us (`/contact-us`)
- Shop Page (`/shop`)
- Error Page (404 handling)

## Project Structure

```
ec_app/
├── app.py                 # Main application entry point
├── db_config.py          # Database configuration
├── schema.sql           # Database schema
├── routes/              # Route handlers
│   ├── account.py      # Account management
│   ├── home.py         # Homepage and main features
│   ├── login.py        # Authentication
│   ├── logout.py       # Logout functionality
│   ├── my_product.py   # Product management
│   └── register.py     # User registration
├── static/             # Static files (CSS, JS, Images)
├── templates/          # HTML templates
└── uploads/           # Product image uploads
```

## Technologies Used

- Flask (Python web framework)
- SQLite (Database)
- Bootstrap (Frontend framework)
- jQuery
- HTML5 & CSS3

## Key Features Details

### Home Page

- Product showcase
- Dynamic cart counter
- Featured products display

### Product Management

- CRUD operations for products
- Image upload with validation
- Product categorization

### User Features

- Secure authentication
- Session management
- User profile management

### Shopping Cart

- Session-based cart system
- Real-time price calculation
- Quantity management

## Template Structure

The application uses a modular template structure with:

- Base layout (`layout/main.html`)
- Header (`layout/header.html`)
- Footer (`layout/footer.html`)
- Slider (`layout/slider.html`)
