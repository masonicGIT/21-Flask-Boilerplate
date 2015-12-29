from flask.ext.wtf import Form
from wtforms import TextField, IntegerField
from wtforms.validators import (Required, ValidationError, NumberRange, Length)

class Send(Form):

    ''' Wallet send form. '''

    address = TextField(validators=[Required(), Length(min=26)], description='Address')
    amount = IntegerField(validators=[Required(), NumberRange(min=5000, max=2100000000000000)], description='Amount')
