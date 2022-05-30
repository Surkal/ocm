from flask import Flask, render_template, request
import logging

from .main import extract


app = Flask(__name__)

@app.route("/")
def index():
    page_number = request.args.get('page', 1)
    # Extract the data from OpenClassroom website
    courses, pagination = extract(page_number)
    data={
        'courses': courses,
        'current_page': page_number,
        'pagination': pagination,
    }
    return render_template('home.html', data=data)