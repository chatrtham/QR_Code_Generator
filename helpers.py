import os
import qrcode
import uuid

from flask import redirect, render_template, session
from functools import wraps


def generate_qr(url):
    # Generate QR code
    img = qrcode.make(url)

    url = escape(url)
    # Create directory
    directory = "static/qrcodes/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save as file
    unique_id = uuid.uuid4()
    file_name = f"{url}_{unique_id}.png"
    file_path = os.path.join(directory, file_name)
    img.save(file_path, "PNG")

    return file_path


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=escape(message)), code


def escape(s):
    for old, new in [
        ("-", "--"),
        (" ", "-"),
        ("_", "__"),
        ("?", "~q"),
        ("%", "~p"),
        ("#", "~h"),
        ("/", "~s"),
        ('"', "''"),
    ]:
        s = s.replace(old, new)
    return s


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
