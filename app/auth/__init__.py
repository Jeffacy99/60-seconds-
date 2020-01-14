from flask import Blueprint
from flask import Flask
app =Flask (_name_)

auth = Blueprint('auth', __name__)
from . import views, forms

app.run(debug=True)
