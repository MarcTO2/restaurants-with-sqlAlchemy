from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review, Base

engine = create_engine('sqlite:///restaurant.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create example restaurants
restaurant1 = Restaurant(name="Tasty Bites", price=2500)
restaurant2 = Restaurant(name="Spice Haven", price=2800)

# Create example customers
customer1 = Customer(first_name="John", last_name="Doe")
customer2 = Customer(first_name="Alice", last_name="Smith")

# Create reviews
review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer2)

# Add objects to the session
session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2])

# Commit changes to the database
session.commit()
session.close()


