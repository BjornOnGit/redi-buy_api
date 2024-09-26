# RediBuy API 🚀

<!-- [![Build Status](https://github.com/BjornOnGit/redi-buy_api/workflows/CI/badge.svg)](https://github.com/BjornOnGit/redi-buy_api/actions) -->

## Description

RediBuy is an e-commerce API built using FastAPI. The platform supports a shopping cart, payments (integrated with Paystack), coupon management, and real-time recommendation engine using collaborative filtering.

## Features

- User Authentication
- Shopping Cart and Order Management
- Coupon Management System
- Collaborative Filtering for Product Recommendations
- Payment Integration with Paystack
- Invoice Generation via Celery and Redis

## Technology Stack

- **Backend**: FastAPI, Python
- **Database**: MongoDB, ODMantic
- **Task Queue**: Celery, Redis
- **Containerization**: Docker, Docker Compose
- **Payment Integration**: Paystack
- **Recommendation System**: Collaborative Filtering

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10
- Paystack API credentials
- MongoDB and Redis

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/redi-buy-api.git
   cd redi-buy-api
   ```

2. Create a `.env` file in the root directory and add your Paystack API credentials:

   ```bash
    MONGODB_URL="mongodb://localhost:27017/my_local_db"
    PAYSTACK_SECRET_KEY="your_secret_key"
    REDIS_URL="redis://localhost:6379/0"
    ```

3. Build and run the containers:

    ```bash
    docker-compose up --build
    ```

## API Documentation

The API documentation can be accessed through the `/docs` or `/redoc` endpoints.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

### Create an Order

```bash
curl -X POST "http://localhost:8000/orders" -H "Content-Type: application/json" -d '{"user_id": "60c74b", "items": [...]}'
```

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
