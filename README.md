# Appearances API

This Flask API manages TV show episodes, guests, and their appearances. It includes endpoints to retrieve and add data for episodes, guests, and their appearances.

## Prerequisites

- Python 3.x
- PostgreSQL
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- SQLAlchemy-Serializer
- Faker

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database:**
   Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your PostgreSQL credentials.

4. **Set up the database:**
   ```bash
   flask --app app db init

   flask --app app db migrate -m "Your migration message"

   flask --app app db upgrade

   ```

5. **Seed the database:**
   ```bash
   python3 seed.py
   ```

6. **Run the app:**
   ```bash
   python3 app.py
   ```

## API Endpoints

- **GET** `/episodes` — Retrieve all episodes.
- **GET** `/episodes/<int:id>` — Retrieve a specific episode by ID.
- **GET** `/guests` — Retrieve all guests.
- **POST** `/appearances` — Create a new appearance (requires `rating`, `episode_id`, and `guest_id`).

## Models Overview

- **Episode**: `id`, `date`, `number`
- **Guest**: `id`, `name`, `occupation`
- **Appearance**: `id`, `rating`, `episode_id`, `guest_id`

## Seeding the Database

Run `python3 seed.py` to generate random data for episodes, guests, and appearances using Faker.

