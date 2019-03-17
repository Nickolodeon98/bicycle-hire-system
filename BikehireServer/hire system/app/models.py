from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from app import constants

class BaseModel(object):

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Staff(BaseModel, db.Model):

    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), unique=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def to_dict(self):
        """convert object to dictionary"""
        staff_dict = {
            "staff_id": self.id,
            "name": self.name,
            "email": self.email,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return staff_dict

class User(BaseModel, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(20))
    orders = db.relationship("Order", backref="user")

    def __init__(self,*args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")

        super(User,self). __init__(*args,**kwargs)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def to_dict(self):
        """convert object to dictionary"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "email": self.email,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

class Location(BaseModel, db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    bike = db.relationship("Bike", backref="location")

    def to_dict(self):
        "convert to dictionary"
        d = {
            "lid": self.id,
            "lname":self.name
        }
        return d

class Bike(BaseModel,db.Model):
    __tablename__ = "bike"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, default=0) #rent fee per day
    index_image_url = db.Column(db.String(256), default="")
    images = db.relationship("BikeImage")
    orders = db.relationship("Order", backref="bike")

    def to_basic_dict(self):
        bike_dict = {
            "bike_id": self.id,
            "title": self.title,
            "price": self.price,
            "location_name": self.location.name,
            "img_url": constants.QINIU_URL_DOMAIN + self.index_image_url if self.index_image_url else "",
        }
        return bike_dict

    def to_full_dict(self):
        """"""
        bike_dict = {
            "bike_id": self.id,
            "title": self.title,
            "price": self.price,
            "location_name": Bike.location.name,
            "img_url": constants.QINIU_URL_DOMAIN + self.index_image_url if self.index_image_url else ""
        }

        # bike image
        img_urls = []
        for image in self.images:
            img_urls.append(constants.QINIU_URL_DOMAIN + image.url)
        bike_dict["img_urls"] = img_urls

        return bike_dict
class Order(BaseModel, db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bike.id"), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    bike_price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, default=0)
    status = db.Column(
        db.Enum(
            "PAID",
            "PICKED"
            "COMPLETE",
            "CANCELED",
        ),
        default="PAID", index=True)

    def to_dict(self):
        """"""
        order_dict = {
            "order_id": self.id,
            "user_name": self.user.name,
            "bike_name":self.bike_id,
            "price": self.bike_price,
            "location_name": self.bike.location_id,
            "amount": self.amount,
            "begin_date":self.begin_date,
            "end_date":self.end_date,
            "days":self.days,
            "status":self.status
        }
        return order_dict
class BikeImage(BaseModel, db.Model):
    """bike image"""

    __tablename__ = "bike_image"

    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey("bike.id"), nullable=False)
    url = db.Column(db.String(256), nullable=False)
