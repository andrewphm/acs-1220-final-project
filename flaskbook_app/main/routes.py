from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user



main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    return render_template("home.html")


