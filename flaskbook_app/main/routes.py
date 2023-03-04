from flaskbook_app.extensions import db
from flask import Blueprint, request, render_template, redirect, url_for, flash

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("home.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/signup")
def signup():
    return render_template("signup.html")
