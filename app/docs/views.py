from flask import Blueprint, render_template

apiary = Blueprint('apiary', __name__, template_folder='templates')


@apiary.route('/')
def index():
    return render_template('index.html')
