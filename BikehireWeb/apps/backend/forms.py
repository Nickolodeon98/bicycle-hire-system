from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from wtforms import Form


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='Please enter the right email '),InputRequired(message='Please enter email')])
    password = StringField(validators=[Length(6,22,message='Enter the right password')])
    remember = IntegerField()
