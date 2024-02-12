import wtforms
from wtforms import Form, StringField, validators, RadioField, SelectField, TextAreaField, FileField
from wtforms.fields import EmailField, DateField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

class CreateStaffForm(Form):
    Username = StringField('Username: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    Email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    PhoneNo = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(), validators.Regexp('^\d+$', message='Phone number must only contain numeric digits.')])
    Password = wtforms.PasswordField('Password: ', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateCustomerForm(Form):
    Username = StringField('Username: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    Email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    PhoneNo = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(),
                                           validators.Regexp('^\d+$',
                                            message='Phone number must only contain numeric digits.')])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    Password = wtforms.PasswordField('Password: ', [validators.Length(min=1, max=150), validators.DataRequired()])

class UpdateUserForm(Form):
    Username = StringField('Username: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    Email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    PhoneNo = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(),
                                           validators.Regexp('^\d+$',
                                                             message='Phone number must only contain numeric digits.')])



class UpdatePassword(Form):
    Password = wtforms.PasswordField('Password: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    New_Password = wtforms.PasswordField(label='New Password:', validators=[
        validators.Length(min=1, max=20),
        validators.EqualTo('Confirm_Password', message='Passwords must match')
    ])
    Confirm_Password = wtforms.PasswordField(label='Confirm password:', validators=[
        validators.Length(min=1, max=20)
    ])

class CreateProductForm(Form):
    Name = StringField('Name of product: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    Price = StringField('Price', [
        validators.DataRequired(),
        validators.Regexp(r'^\d+(\.\d{1,2})?$', message='Invalid price format. Use up to 2 decimal places.')
    ])
    Description = StringField('Description: ', [validators.Length(min=50, max=1000), validators.DataRequired()])



class Feedback_Form(Form):
    Name = StringField('Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    Email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    PhoneNo = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(),
                                           validators.Regexp('^\d+$',
                                                             message='Phone number must only contain numeric digits.')])
    Feedback_type = SelectField('Feedback type: ', choices=[('Compliment'), ('Suggestion'), ('Issue')], default=('ComplimentZ'))
    Feedback = StringField('Feedback (Max 500 words): ', [validators.Length(min=10, max=500), validators.DataRequired()])
