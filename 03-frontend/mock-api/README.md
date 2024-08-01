---
# HBnB Evolution Application

This project is a place management application based on Flask, which includes functionalities for managing users, cities, countries, reviews, and amenities. The application can be run in a Dockerized environment using Gunicorn as the application server.

## Project Structure

### Models

- **BaseModel**: Abstract class defining common attributes and methods.
- **City**: Represents a city.
- **DataManager**: Manages data persistence.
- **Review**: Represents a review.
- **Place**: Represents a place.
- **User**: Represents a user.

### Endpoints

#### Users
- **POST /users**: Create a new user.
- **GET /users**: Retrieve a list of all users.
- **GET /users/{user_id}**: Retrieve details of a specific user.
- **PUT /users/{user_id}**: Update an existing user.
- **DELETE /users/{user_id}**: Delete a user.

#### Cities
- **POST /cities**: Create a new city.
- **GET /cities**: Retrieve a list of all cities.
- **GET /cities/{city_id}**: Retrieve details of a specific city.
- **PUT /cities/{city_id}**: Update an existing city.
- **DELETE /cities/{city_id}**: Delete a city.

#### Reviews
- **POST /places/{place_id}/reviews**: Create a new review for a specific place.
- **GET /users/{user_id}/reviews**: Retrieve all reviews written by a specific user.
- **GET /places/{place_id}/reviews**: Retrieve all reviews for a specific place.
- **GET /reviews/{review_id}**: Retrieve details of a specific review.
- **PUT /reviews/{review_id}**: Update an existing review.
- **DELETE /reviews/{review_id}**: Delete a review.

#### Amenities
- **POST /amenities**: Create a new amenity.
- **GET /amenities**: Retrieve a list of all amenities.
- **GET /amenities/{amenity_id}**: Retrieve details of a specific amenity.
- **PUT /amenities/{amenity_id}**: Update an existing amenity.
- **DELETE /amenities/{amenity_id}**: Delete an amenity.

#### app
##### get every endpoint from a flask image
- *app.register_blueprint(user_manager_blueprint)
- *app.register_blueprint(country_city_manager_blueprint)
- *app.register_blueprint(amenity_blueprint)
- *app.register_blueprint(place_manager_blueprint)
- *app.register_blueprint(review_manager_blueprint)

### UML Diagram

#### Class Diagram

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +id: String
        +created_at: DateTime
        +updated_at: DateTime
        +save(): void
        +to_dict(): dict
    }

    class City {
        +name: String
        +country_code: String
    }

    class DataManager {
        -storage: dict
        +load_countries(): void
        +save(entity: BaseModel): void
        +get(entity_id: String, entity_type: String): BaseModel
        +update(entity: BaseModel): void
        +delete(entity_id: String, entity_type: String): void
    }

    class Review {
        +place_id: String
        +user_id: String
        +rating: int
        +comment: String
    }

    class Place {
        +name: String
        +description: String
        +address: String
        +city_id: String
        +latitude: float
        +longitude: float
        +host_id: String
        +number_of_rooms: int
        +number_of_bathrooms: int
        +price_per_night: float
        +max_guests: int
        +amenity_ids: list
    }

    class User {
        +email: String
        +password: String
    }

    class Amenity {
        +name: String
    }

    class FlaskApp {
        +register_blueprint(user_manager_blueprint): void
        +register_blueprint(country_city_manager_blueprint): void
        +register_blueprint(amenity_blueprint): void
        +register_blueprint(place_manager_blueprint): void
        +register_blueprint(review_manager_blueprint): void
        +run(): void
    }

    class UserManager {
        +create_user(): void
        +get_users(): void
        +get_user(user_id: String): void
        +update_user(user_id: String): void
        +delete_user(user_id: String): void
    }

    class ReviewManager {
        +create_review(place_id: String): void
        +get_user_reviews(user_id: String): void
        +get_place_reviews(place_id: String): void
        +get_review(review_id: String): void
        +update_review(review_id: String): void
        +delete_review(review_id: String): void
    }

    class PlaceManager {
        +create_place(): void
        +get_places(): void
        +get_place(place_id: String): void
        +update_place(place_id: String): void
        +delete_place(place_id: String): void
    }

    class CountryCityManager {
        +get_countries(): void
        +get_country(country_code: String): void
        +get_cities_by_country(country_code: String): void
        +create_city(): void
        +get_cities(): void
        +get_city(city_id: String): void
        +update_city(city_id: String): void
        +delete_city(city_id: String): void
    }

    class AmenityManager {
        +create_amenity(): void
        +get_amenities(): void
        +get_amenity(amenity_id: String): void
        +update_amenity(amenity_id: String): void
        +delete_amenity(amenity_id: String): void
    }

    BaseModel <|-- City
    BaseModel <|-- Review
    BaseModel <|-- Place
    BaseModel <|-- User
    BaseModel <|-- Amenity

    DataManager --> BaseModel : manages

    FlaskApp --> user_manager
    FlaskApp --> country_city_manager
    FlaskApp --> amenity_manager
    FlaskApp --> place_manager
    FlaskApp --> review_manager

    user_manager ..> UserManager
    country_city_manager ..> CountryCityManager
    amenity_manager ..> AmenityManager
    place_manager ..> PlaceManager
    review_manager ..> ReviewManager

```

#### Deployment Diagram

```mermaid
stateDiagram-v2
    state Docker {
        state Container {
            [*] --> FlaskApplication
            FlaskApplication --> Gunicorn
            Gunicorn --> Flask
            Flask --> Blueprints
            state Blueprints {
                user_manager_blueprint
                country_city_manager_blueprint
                amenity_blueprint
                place_manager_blueprint
                review_manager_blueprint
            }
        }
    }

    state HostMachine {
        state Volumes {
            DataVolume : /app/data
        }
    }

    Docker --> HostMachine
```

## Unit Tests

### User Tests

File: `tests/test_user_endpoints.py`

### City Tests

File: `tests/test_country_city_endpoints.py`

### Review Tests

File: `tests/test_review_endpoints.py`

## Dockerization

### `Dockerfile`

```dockerfile
# Use an Alpine Linux base image with Python
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application source code
COPY . /app/

# Expose the port the application will run on
EXPOSE $PORT

# Create a volume for data persistence
VOLUME /app/data

# Configure Gunicorn as the application server
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} api.review_manager:app"]
```

### Building and Running the Docker Container

#### Build the image

```sh
docker build -t holberton_hbnb .
```

#### Run the container

```sh
docker run -d -p 8000:8000 --name holberton_hbnb_container -v $(pwd)/data:/app/data -e PORT=8000 holberton_hbnb
```

### Verification

To verify that your application is working correctly, open a web browser and navigate to `http://localhost:8000`. You can also use tools like `curl` or Postman to make requests to your endpoints and verify that they are responding correctly.

#### Example `curl` command

```sh
curl http://localhost:8000/places
```
## BUGS

N/A

## Author
Nelson Betancourt Aponte
---