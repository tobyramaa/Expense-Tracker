from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from wtforms import FloatField

class CommaFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            raw = valuelist[0]
            if raw:
                raw = raw.replace(",", "")
            valuelist = [raw]
        super().process_formdata(valuelist)

class TransactionForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    amount = CommaFloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than zero")])
    type = RadioField("Type", choices=[("income", "Income"), ("expense", "Expense")], validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500, message="Description must be less than 255 characters")])
    submit = SubmitField("Add Transaction")