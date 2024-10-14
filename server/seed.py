from faker import Faker
from models import db, Episode, Guest, Appearance
import random
from sqlalchemy.exc import SQLAlchemyError
from app import app


fake = Faker()

# Function to clear existing data from all tables
def clear_data():
    try:
        # Delete all entries in the reverse order of dependency
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        db.session.commit()
        print("Database cleared successfully!")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error while clearing database: {str(e)}")

# Function to seed Episode data
def seed_episodes():
    episodes = []
    for _ in range(50):
        episode = Episode(
            date=fake.date_time_this_decade(),  # Random date within the last decade
            number=random.randint(1, 1000)      # Random episode number between 1 and 1000
        )
        episodes.append(episode)
    return episodes

# Function to seed Guest data
def seed_guests():
    guests = []
    for _ in range(50):
        guest = Guest(
            name=fake.name(),                   # Random name
            occupation=fake.job()               # Random occupation
        )
        guests.append(guest)
    return guests

# Function to seed Appearance data
def seed_appearances(episodes, guests):
    appearances = []
    for _ in range(50):
        appearance = Appearance(
            rating=random.choice([1, 2, 3, 4, 5]),  # Random rating between 1 and 5
            episode_id=random.choice(episodes).id,  # Randomly associate with an episode
            guest_id=random.choice(guests).id       # Randomly associate with a guest
        )
        appearances.append(appearance)
    return appearances

# Main function to execute the seed
def run_seed():
    try:
        print("Seeding database...")

        # Clear existing data
        clear_data()

        # Seed Episodes
        episodes = seed_episodes()
        db.session.add_all(episodes)

        # Seed Guests
        guests = seed_guests()
        db.session.add_all(guests)

        # Commit so the Episode and Guest IDs are available for Appearance
        db.session.commit()

        # Seed Appearances using the episodes and guests created
        appearances = seed_appearances(episodes, guests)
        db.session.add_all(appearances)

        # Commit all changes to the database
        db.session.commit()

        print("Database seeding completed successfully!")
    except SQLAlchemyError as e:
        print(f"Error during seeding: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
       run_seed()