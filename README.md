# QR Code Generator - CS50X Final Project
## Video Demo:  https://youtu.be/mzJOk4rrCSk
## Description:
This project allows people to generate QR codes from text or url without having to log in. However users can create their accounts and log in in order to see all the qr codes that they generated before on their accounts.
## Understanding:
### `app.py`
I use Flask framework for this project. You can see that I import a lot of libraries at the top of this file, including `helpers.py` which is the file that include all the helpers function (apology, generate_qr, login_required) there. Moreover, I use cs50's SQL library to use `qrcode.db` as a database for this project. Thereafter are a bunch of routes. You may notice that some routes are decorated by `@login_required` (a function defined in `helpers.py`), which mean you need to login in order to access those routes.
#### `index`
This is the main page of the website, where users can insert their text or URLs and generate QR Codes. However, you get there via `POST`, you'll see the template `generated.html` that show you the generated QR Code and allow you to download it by clicking download on that page, then you'll get to the `download` route via `POST`.
You may notice that this route doesn't require users to login. That's because I allow users to generate and download qrcodes without logging in, but those QR Codes will not be collected in their accounts.
#### `download`
This route is for downloading the QR Code into users' devices by receiving file_path from the `generated.html`.
#### `history`
This route require users to login to access this route via `GET` to show QR Codes that they generated before, using `return render_template("history.html", histories=histories)`. I use `SELECT` function in `SQLite3` to read the data from the database to be shown in this route.
#### `delete`
In `history` route, users can delete QR Codes from their accounts on this page by clicking the delete button. Then they will get to `delete` route via post. This route is for deleting QR Codes from users' account and redirect to `history` again. However, those images will not be actually deleted from the database, they will be updated to value in `is_deleted` column in the database to `True`. I did this because I think users could accidentally delete them. So they can ask the support to backup those QR Code by taking a look at the database.
#### `register`
This route is for creating an account. Starting with checking for errors. Then, insert `username` and `hashed_password` (using `werkzeug.security` library) into the database. And redirect the user to the `login` route.
#### `login`
This route is for logging in to the existing account. Then, remember the user's id with `session["user_id"] = rows[0]["id"]`. And redirect the user to the `index` route.
#### `logout`
This route is for logging out, using `session.clear()` and redirect the user to the `index` route.
### `helpers.py`
This file includes helper functions that are used in the `app.py`
#### `generate_qr`
This function generates a QR Code, using python `qrcode` library. Then, creating file name, using `escape(url)` function to avoid having special character in file name and add universal unique identifier to the file name to make all the file name unique, and directory to store the QR Code. Finally, this function returns the file path to that QR Code.
#### `apology`
This function renders meme photo for apologizing user when there's an error.
#### `escape`
This function turns every special characters that are not allowed in file path to those are acceptable.
#### `login_required`
This function is a decorator in `Flask` that force users to log in before getting access to some certain routes.
### `static/`
This directory includes `favicon.png`, `styles.css` and `qrcodes/`, where I store all the QR Code files here.
### `templates`
Files in this directory are `html` templates for the whole website.
### `qrcode.db`
This is the database file for this project, using `SQLite3`.
### `requirements.txt`
This `.txt` file includes all the packages for this project.
## Contact Me:
[My LinkedIn profile](https://www.linkedin.com/in/chatrtham-chatramornrat-799690213/)

[My GitHub profile](https://github.com/chatrtham)