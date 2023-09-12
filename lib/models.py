from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy engine
engine = create_engine('sqlite:///restaurant.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the many-to-many association table
restaurant_customer_association = Table(
    'restaurant_customer_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurant.id')),
    Column('customer_id', Integer, ForeignKey('customer.id'))
)

# Define the Customer class
class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    restaurants = relationship("Restaurant", secondary=restaurant_customer_association, back_populates="customers")
    reviews = relationship("Review", back_populates="customer")

    def get_reviews(self):
        return self.reviews
    
    def get_restaurants(self):
        return self.restaurants
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def favorite_restaurant(self):
        favorite = None
        highest_rating = -1

        for review in self.reviews:
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite = review.restaurant

        return favorite
    
    def add_review(self, restaurant, rating):
        new_review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        self.reviews.append(new_review)
    
    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            self.reviews.remove(review)

    def __repr__(self):
        return f'FirstName={self.first_name}. LastName={self.last_name}'

# Define the Review class
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def get_customer(self):
        return self.customer
    
    def get_restaurant(self):
        return self.restaurant
    
    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars'

    def __repr__(self):
        return f'Rating={self.star_rating}'

# Define the Restaurant class
class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    customers = relationship("Customer", secondary=restaurant_customer_association, back_populates="restaurants")
    reviews = relationship("Review", back_populates="restaurant")

    def get_reviews(self):
        return self.reviews
    
    def get_customers(self):
        return self.customers
    
    @classmethod
    def fanciest(cls):
        return Session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        review_strings = []
        for review in self.reviews:
            review_str = f'Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars.'
            review_strings.append(review_str)
        return review_strings

    def __repr__(self):
        return f'Name={self.name}, Price={self.price}'
