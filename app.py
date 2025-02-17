from flask import Flask, session, render_template, request
from flask_session import Session


import x

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################
@app.get("/")
def show_index():
    try:
        db, cursor = x.db()
        q = """SELECT u.user_pk, u.user_name, GROUP_CONCAT(p.user_phone ORDER BY p.user_phone) AS phones FROM users u LEFT JOIN users_phones p ON u.user_pk = p.user_fk GROUP BY u.user_pk"""
        cursor.execute(q)
        rows = cursor.fetchall()
        ic(rows)
        for row in rows:
            if row["phones"]:
                row["user_phones"] = row["phones"].split(",")
            else:
                row["user_phones"] = []
        ic(rows)
        return render_template("index.html", title="Home", rows=rows)
    except Exception as ex:
        return ex, 500
    finally:
        pass
    

##############################
@app.get("/contact-us")
def show_contact_us():
    return render_template("contact-us.html", title="Contact us")

##############################
@app.get("/about-us")
def show_about_us():
    return render_template("about-us.html", title="About us")

##############################
@app.get("/signup")
def show_signup():
    return render_template("signup.html", title="Signup us")

##############################
@app.get("/login")
def show_login():
    return render_template("login.html", title="Login us")

##############################
@app.post("/login")
def login():
    email = request.form.get("email", "")
    if email == "a":
        toast = render_template("_toast.html", status="ok", message="ok")
    else:
        toast = render_template("_toast.html", status="error", message="email invalid")

    return f"""
        <template mix-bottom="#toast_container">{toast}</template>
    """

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Page Not Found"), 404

##############################
@app.get("/api/v1/items")
def get_items():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM users"
        cursor.execute(q)
        rows = cursor.fetchall()
        ic(rows)
        return rows
    except Exception as ex:
        return ex, 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  



##############################
@app.delete("/api/v1/users/<user_id>")
def delete_user(user_id):
    try:
        db, cursor = x.db()
        q = "DELETE FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_id,))
        if cursor.rowcount != 1:
            raise Exception("user not found")
        db.commit()
        return f"User {user_id} deleted"
    except Exception as ex:
        return ex, 400
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  

##############################
@app.get("/users/<int:user_id>")
def show_user(user_id):
    try:
        db, cursor = x.db()
        # Retrieve user information
        q = """
            SELECT u.user_pk, u.user_name, p.user_phone
            FROM users u
            LEFT JOIN users_phones p ON u.user_pk = p.user_fk
            WHERE u.user_pk = %s
        """
        cursor.execute(q, (user_id,))
        rows = cursor.fetchall()

        if not rows:
            abort(404, description="User not found")

        # Process the data
        user = {
            "user_pk": rows[0]["user_pk"],
            "user_name": rows[0]["user_name"],
            "user_phones": [row["user_phone"] for row in rows if row["user_phone"]]
        }

        ic(user)
        return render_template("user_details.html", title=f"User {user['user_name']}", user=user)
    except Exception as ex:
        ic(ex)
        return "An error occurred while fetching the user details.", 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()
            
























# try:
#     ic(verification_key)
#     verification_key = x.validate_uuid4(verification_key)
#     user_verified_at = int(time.time())

#     db, cursor = x.db()
#     q = """ UPDATE users 
#             SET user_verified_at = %s 
#             WHERE user_verification_key = %s"""
#     cursor.execute(q, (user_verified_at, verification_key))
#     if cursor.rowcount != 1: x.raise_custom_exception("cannot verify account", 400)
#     db.commit()
#     return redirect(url_for("view_login", message="User verified, please login"))

# except Exception as ex:
#     ic(ex)
#     if "db" in locals(): db.rollback()
#     if isinstance(ex, x.CustomException): return ex.message, ex.code    
#     if isinstance(ex, x.mysql.connector.Error):
#         ic(ex)
#         return "Database under maintenance", 500        
#     return "System under maintenance", 500  
# finally:
#     if "cursor" in locals(): cursor.close()
#     if "db" in locals(): db.close()    






