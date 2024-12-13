# Standard Store API

This is an API for a standard store, developed in Python using the FastAPI framework. The application follows the **MVC (Model-View-Controller)** design pattern and is connected to a **PostgreSQL database**.

## Features
- **FastAPI**: The API is built using the FastAPI framework for high performance and easy development.
- **MVC Architecture**: The application uses the MVC pattern for better separation of concerns.
- **PostgreSQL Database**: The API is connected to a PostgreSQL database for data storage.
- **Alembic Migrations**: Database migrations are managed using Alembic to ensure version control and smooth updates.
- **Docker Integration**: The application is configured to run with Docker for easy deployment and containerization.

## Models

The project includes the following key models:
- **User**: Represents the users of the store.
- **Order**: Represents customer orders in the system.
- **OrderItem**: Represents the items within an order.
- **Product**: Represents the products available in the store.

## Installation

1. Clone the repository:

    Using SSH:
    ```bash
    git clone git@github.com:MrBubliKK/candy_shop.git
    ```

    Using HTTPS:
    ```bash
    git clone https://github.com/MrBubliKK/candy_shop.git
    ```

2. Navigate to the project directory:
    ```bash
    cd <repository_directory>
    ```

3. Build and run with Docker:
    ```bash
    docker-compose up --build
    ```

## Usage

Once the application is running, you can access the API at `http://localhost:8000`.

## Database Migrations

To manage database migrations, Alembic is used. You can apply migrations using the following command:

```bash
alembic upgrade head
