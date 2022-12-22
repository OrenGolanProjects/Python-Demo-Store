from flask import Flask, render_template, request, redirect
from Classes.processSetup import *

# =========== Init all objects ==================
app = Flask(__name__)

obj_db = database_mysql()
obj_db.create_connection_MYSQL()
obj_customer = customer()
obj_product = product()
obj_cart = cart()
obj_db_sqlit3 = database_sqlite3()
obj_db_sqlit3.create_connection_sqlite3()

bool_sqlite3 = False
# ===============================================
# Manual login
# username: "Matt Murdock"  pass:	"ErY7Fe8G"	role: admin
# username: "Steven Grant" pass:	"NGFx8DzC"	role: customer
# ===============================================


@app.route('/')
def home():
    return render_template("login.html", title="HOME", action="login", loginPage_title="Welcome Back! Please enter your details.", loginPage_header="Login To Your Account")


@app.route("/login", methods=["GET", "POST"])
def validate_customer():
    obj_customer.UserName = ""
    obj_customer.Password = ""
    if request.method == "POST":
        obj_customer.UserName = request.form["username"]
        obj_customer.Password = request.form["password"]
        if obj_customer.isSignUP:
            if "customer" in request.form:
                obj_customer.Role = "customer"
            else:
                obj_customer.Role = "admin"
            obj_db_sqlit3.tableName = "customers"
            obj_db_sqlit3.UserName = obj_customer.UserName
            obj_db_sqlit3.Password = obj_customer.Password
            obj_db_sqlit3.Role = obj_customer.Role
            obj_db_sqlit3.insert()
            obj_customer.__init__()
            return render_template("login.html", title="HOME", action="login", loginPage_title="Welcome Back! Please enter your details.", loginPage_header="Login To Your Account")
        if bool_sqlite3:
            obj_customer.getCustomer(
                obj_db_sqlit3.databaseconnection, bool_sqlite3)
        else:
            obj_customer.getCustomer(obj_db.databaseConnection, bool_sqlite3)
    if obj_customer.isCustomerExists:
        return redirect("/store")
    else:
        if 'Sign-up' == request.form["commit"]:
            obj_customer.UserName = ""
            obj_customer.Password = ""
            obj_customer.isSignUP = True
            return redirect("/sign-up")

        else:
            return redirect("/loginError")


@ app.route("/loginError", methods=["GET", "POST"])
def invalid_login():
    if len(request.args) == 0:
        return render_template("invalid_login.html",
                               title="ERROR",
                               error_header="Login failed.",
                               error_description="The password or username you entered is incorrect.",
                               Login="Login")
    elif "login" in request.args:
        return redirect("/")
    else:
        return render_template("ThankYou.html",
                               title="Byebye",
                               thankyou_header="Bye Bye.",
                               thankyou_description="Dont be a stranger!")


@ app.route("/store", methods=["GET", "POST"])
def customer_choice():
    if request.method == "POST":
        counter_recores = 0
        for i in request.form:
            if int(request.form[i]) > 0:
                counter_recores = 1
                obj_cart.IdCustomer = obj_customer.Id  # DB customer ID
                obj_cart.IdProduct = i  # DB product ID
                obj_cart.Quantity = request.form[i]  # DB quantity

                if bool_sqlite3:
                    obj_cart.AddProductToCustomerTranscation(
                        obj_db_sqlit3.databaseconnection, bool_sqlite3)
                else:
                    obj_cart.AddProductToCustomerTranscation(
                        obj_db.databaseConnection, bool_sqlite3)

                if obj_cart.isInsertSucceeded == False:
                    return render_template("invalid_login.html",
                                           title="ERROR",
                                           error_header="Order Failed!",
                                           error_description="Please try order again..",
                                           Login="Login")

        if counter_recores == 0:
            return render_template("invalid_login.html",
                                   title="ERROR",
                                   error_header="No items in cart..",
                                   error_description="Click Store & Try again..",
                                   Login="Store"
                                   )
        return redirect("/role_check")
    else:
        if bool_sqlite3:
            obj_product.GetAppProducts(
                obj_db_sqlit3.databaseconnection, bool_sqlite3)
        else:
            obj_product.GetAppProducts(obj_db.databaseConnection, bool_sqlite3)
        return render_template("/store.html", title="SHOP", products=obj_product.products, role=str(obj_customer.Role))


@ app.route("/role_check", methods=["GET", "POST"])
def role_check():

    if str(obj_customer.Role).lower() == "admin":
        if bool_sqlite3 == True:
            obj_cart.GetCustomerGoldReport(
                obj_db_sqlit3.databaseconnection, bool_sqlite3)
        else:
            obj_cart.GetCustomerGoldReport(
                obj_db.databaseConnection, bool_sqlite3)
        return render_template("report.html", recoreds=obj_cart.goldCustomers, role=str(obj_customer.Role))
    else:
        # customer finish hes purches
        return render_template("/ThankYou.html", title="Byebye",
                               thankyou_header="Thank you for your order!",
                               thankyou_description="We hope to see you again.")


@ app.route("/exit", methods=["GET", "POST"])
def close():
    # admin wants to exist
    if request.method == "POST":
        return render_template("ThankYou.html",
                               title="Byebye",
                               thankyou_header="Bye Bye.",
                               thankyou_description="Until next time...")


@ app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    return render_template("login.html", title="sign-up", action="/sign_up", loginPage_title="You made the right decision!", loginPage_header="Please Enter Username & Password, welcome to the family!")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)
