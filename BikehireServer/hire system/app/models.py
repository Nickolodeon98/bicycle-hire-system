from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash,check_password_hash

class BaseModel(object):

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Staff(BaseModel, db.Model):

    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(20), unique=True)
    avatar_url = db.Column(db.String(128))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

class Bike(BaseModel, db.Model):

    __tablename__ = "bike"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    image_url = db.Column(db.String(128))
    type = db.Column(db.String(32))
    price = db.Column(db.Integer, default=0)
    status = db.Column(
        db.Enum("available", "unavailable"),
        default="unavailable", index=True)
    orders = db.relationship("Order", backref="bike")

class User(BaseModel, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar_url = db.Column(db.String(128))
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

class Order(BaseModel, db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bike.id"), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    house_price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(
            "WAIT_PAYMENT",
            "PAID",
            "COMPLETE",
            "CANCELED",
        ),
        default="WAIT_ACCEPT", index=True)