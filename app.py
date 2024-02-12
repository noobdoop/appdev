from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, session, abort
from chat import get_response

import shelve


# Phil
from Forms import CreateStaffForm, CreateProductForm, CreateCustomerForm, UpdatePassword, Feedback_Form, UpdateUserForm
from User import Staff, Product
from Customer import Customer, Feedback
import hashlib
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt

# Kiefer
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = Flask(__name__)
count_id = 0


data = [
    {
        "id": 1,
        "name": "Bouncy Castle",
        "image_url": "/static/Images/bouncycastle.png",
        "price": 40,
        "description": "A fun bouncy castle for kids to enjoy! \nDimension: 280*305*230cm \nMaximum: 6kids x 35 kg",
        "rating": 5,
        "reviews": [
            {"user": "bob", "comment": "very fun for my kids", "rating": 5},
            {"user": "jane", "comment": "bouncy bouncy", "rating": 4}
        ]
    },
    {
        "id": 2,
        "name": "Dollhouse",
        "image_url": "/static/Images/dollhouse.png",
        "price": 20,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 3,
        "name": "Remote-Controlled Car",
        "image_url": "/static/Images/car.png",
        "price": 15,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 4,
        "name": "Beyblade",
        "image_url": "/static/Images/beyblade.png",
        "price": 10,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
{
        "id": 5,
        "name": "Trampoline",
        "image_url": "/static/Images/trampoline.png",
        "price": 25,
        "description": "A fun bouncy castle for kids to enjoy!",
        "rating": 5
    },
    {
        "id": 6,
        "name": "Hula Hoop",
        "image_url": "/static/Images/hulahoop.png",
        "price": 3,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 7,
        "name": "Inflatable Soccer & Basketball Arena",
        "image_url": "/static/Images/soccer.png",
        "price": 60,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 8,
        "name": "Skateboard",
        "image_url": "/static/Images/skateboard.png",
        "price": 10,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
            "id": 9,
            "name": "VROOOOM",
            "image_url": "/static/Images/minicar.png",
            "price": 27,
            "description": "A beautiful dollhouse for imaginative play.",
            "rating":5
    }
]

with shelve.open('products.db', 'c') as db:
    # Loop through each product and store it in the shelve database
    for product in data:
        product_id = str(product["id"])  # Convert the ID to a string to use it as the key
        db[product_id] = {
            "id": product["id"],
            "name": product["name"],
            "image_url": product["image_url"],
            "price": product["price"],
            "description": product["description"],
            "rating": product["rating"]
        }


def retrieve_products():
    with shelve.open('products.db', 'r') as db:
        products = [db[key] for key in db.keys()]
    return products

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()


app.config[
    'STRIPE_PUBLIC_KEY'] = 'pk_test_51OWdR4EqxlVLyyvpqYj6CLNTjvL6wWKZfNLKxDgQ0fmkjxeLdYFEp3S8v808jaSrGJSOqgUb9PPlcmmP3N8oUEE500EzVKfI03'
app.config[
    'STRIPE_SECRET_KEY'] = 'sk_test_51OWdR4EqxlVLyyvptiGROn5mhsGVa0lUyiPavERmaT6Cugb8nNgvpHVekctBE5XoU0ZHPOwIl2QzN0TJdyWAcOcA00bi5psGUh'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

app.config["SECRET_KEY"] = "kdnioh12890ehksadnasnd8"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

create_database(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))



@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User with that email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
    return render_template("sign_up.html")

app.secret_key = 'WHENIWASAYOUNGBOYMYFATHERTOLDME'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_db = shelve.open('')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return redirect(url_for('base'))

            else:
                flash('Incorrect password.', category='error')
        else:
            flash('User with that email does not exist.', category='error')

    return render_template("login.html")


# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)
#         else:
#             return function()
#
#     return wrapper
#
#
# google_ClientID = "137590171650-k9mdg4pb75ove2p39ed62fg24b22fvs8.apps.googleusercontent.com"
# clients_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
#
# flow = Flow.from_client_secrets_file(
#     client_secrets_file=clients_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
#             "openid"],
#     redirect_uri="http://127.0.0.1:5000/callback"
# )
#
#
# @app.route("/glogin")
# def google_login():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)
#
#
# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!
#
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=google_ClientID
#     )
#
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/protected-area")
#
#
# @app.route("/glogout")
# def google_logout():
#     session.clear()
#     return redirect("/")
#
#
# @app.route('/google-login')
# def index():
#     return "<a href='/glogin'><button>Login</button></a>"
#
#
# @app.route('/protected-area')
# @login_is_required
# def protected_area():
#     return "<a href='/glogout'><button>Logout</button></a>"


@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1OWddGEqxlVLyyvpiZlRQreW',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


@app.route('/thanks')
def thanks():
    return render_template('paymentThanks.html')


@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data']['0']['description'])

    return {}


@app.route("/form", methods=["GET", "POST"])
def form():
    formRequest = request.form
    with shelve.open("form.db") as db:
        db.update(formRequest)
    print(formRequest)
    return render_template("forms.html")


@app.route('/payment')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    products = retrieve_products()
    return render_template('shop.html', products=products)

@app.route('/productpage/<int:product_id>')
def product_page(product_id):
    products = retrieve_products()
    # Find the product by its ID
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        return render_template('productpage.html', product=product)
    else:
        return render_template('error.html', message="Product not found")

@app.route('/search')
def search():
    products = retrieve_products()
    query = request.args.get('query')

    if query:
        # Filter products based on the search query
        filtered_products = [product for product in products if query.lower() in product['name'].lower()]

        if not filtered_products:
            # If no results found, set a message and return it with the template
            return render_template('shop.html', products=products, query=query)

        # Return the filtered products if there are matches
        return render_template('shop.html', products=filtered_products)

    # Return all products if no query is provided
    return render_template('shop.html', products=products)


@app.route('/get_products')
def get_products():
    products = retrieve_products()
    return jsonify(products)

@app.route('/repair')
def repair():
    return render_template('repair.html')

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/snake')
def snake():
    return render_template('snake.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contact():
    create_feedback_form = Feedback_Form(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db.get('Feedback', {})
            feedback = Feedback(
                create_feedback_form.Name.data,
                create_feedback_form.Email.data,
                create_feedback_form.PhoneNo.data,
                create_feedback_form.Feedback_type.data,
                create_feedback_form.Feedback.data,
            )
            # Use the Name as the key in the feedback_dict
            feedback_dict[create_feedback_form.Name.data] = feedback
            db['Feedback'] = feedback_dict
        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()
        return redirect(url_for('display_feedback'))
    else:
        print(create_feedback_form.errors)

    return render_template('contactus.html', form=create_feedback_form)



@app.route('/stickGame')
def stickGame():
    return render_template('stickGame.html')

# chatbot stuff
@app.route("/predict", methods= ["POST"])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


# feedback form stuff
def get_feedback_data():
    with shelve.open('feedback_db') as db:
        return db.get('feedbacks', [])

@app.route('/feedback')
def display_feedback():
    feedback_list = []
    db = shelve.open('feedback.db', 'r')

    try:
        feedback_dict = db.get('Feedback', {})
        for key in feedback_dict:
            feedback = feedback_dict[key]
            feedback_list.append(feedback)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
    return render_template('feedback.html', count=len(feedback_list), feedback_list=feedback_list)

@app.route('/delete_feedback/<name>', methods=['POST', 'GET'])
def delete_feedback(name):
    if request.method == 'POST':
        feedback_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedback_dict = db.get('Feedback', {})

        if name in feedback_dict:
            feedback_dict.pop(name)

        db['Feedback'] = feedback_dict
        db.close()

        return redirect(url_for('display_feedback'))


# PHIL
def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


@app.route('/createUser', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db.get('Staff', {})
            staff_id = max(staff_dict.keys(), default=0) + 1
            global count_id
            count_id+=1
            hashed_password = hash_password(create_staff_form.Password.data)

            staff = Staff(
                count_id,
                staff_id,
                create_staff_form.Username.data,
                create_staff_form.Email.data,
                create_staff_form.PhoneNo.data,
                hashed_password  # Store the hashed password
            )

            staff_dict[staff_id] = staff
            db['Staff'] = staff_dict
        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()
        return redirect(url_for('retrieve_users'))
    else:
        print(create_staff_form.errors)

    return render_template('createUser.html', form=create_staff_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')
        hashed_password = hash_password(create_customer_form.Password.data)

        customer_id = 1  # Initialize customer_id before the try block

        try:
            customers_dict = db['Customers']
            customer_id = max(customers_dict.keys(), default=0) + 1
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer(customer_id, create_customer_form.Username.data,
                            create_customer_form.gender.data, create_customer_form.Email.data,
                            create_customer_form.PhoneNo.data,
                            create_customer_form.address.data, hashed_password)
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)

@app.route('/retrieveUsers')
def retrieve_users():
    staff_list = []
    db = shelve.open('staff.db', 'r')

    try:
        staff_dict = db.get('Staff', {})
        for key in staff_dict:
            staff = staff_dict.get(key)
            staff_list.append(staff)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
    return render_template('retrieveUsers.html', count=len(staff_list), staff_list=staff_list)

@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_staff_form = UpdateUserForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        Staff = staff_dict.get(id)
        Staff.set_Username(update_staff_form.Username.data)
        Staff.set_Email(update_staff_form.Email.data)
        Staff.set_PhoneNo(update_staff_form.PhoneNo.data)

        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        Staff = staff_dict.get(id)
        update_staff_form.Username.data = Staff.get_Username()
        update_staff_form.Email.data = Staff.get_Email()
        update_staff_form.PhoneNo.data = Staff.get_PhoneNo()

        return render_template('updateUser.html', form=update_staff_form, id=id)


@app.route('/updatePasssword/<int:id>/', methods=['GET', 'POST'])
def update_password(id):
    update_staff_password_form = UpdatePassword(request.form)
    if request.method == 'POST' and update_staff_password_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']
        check_hash = hash_password(update_staff_password_form.Password.data)
        new_hashed = hash_password(update_staff_password_form.New_Password.data)

        Staff = staff_dict.get(id)
        if Staff.get_hashed_password() == check_hash:
            Staff.set_hashed_password(new_hashed)

            db['Staff'] = staff_dict
            db.close()

        return redirect(url_for('home'))

    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        Staff = staff_dict.get(id)
        update_staff_password_form.Password.data = Staff.get_Password()

        return render_template('updatePassword.html', form=update_staff_password_form, id=id)

@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        product_dict = {}
        db = shelve.open('product.db', 'w')
        product_dict = db['Product']

        Product = product_dict.get(id)
        Product.set_Name(update_product_form.Name.data)
        Product.set_Description(update_product_form.Description.data)
        Product.set_Price(update_product_form.Price.data)

        db['Product'] = product_dict
        db.close()

        return redirect(url_for('sales'))
    else:
        product_dict = {}
        db = shelve.open('product.db', 'r')
        product_dict = db['Product']
        db.close()

        Product = product_dict.get(id)
        update_product_form.Name.data = Product.get_Name()
        update_product_form.Description.data = Product.get_Description()
        update_product_form.Price.data = Product.get_Price()

        return render_template('updateProduct..html', form=update_product_form, id=id)





@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']

    staff_dict.pop(id)

    db['Staff'] = staff_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route('/deleteCustomer/<int:id>', methods=['POST']) #HELP
def delete_customer(id):
    customer_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('retrieve_customers'))



@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        db = shelve.open('product.db', 'c')  # Use 'c' to open the shelve in read/write mode

        try:
            product_dict = db.get('Product', {})
            product_id = max(product_dict.keys(), default=0) + 1

            product = Product(
                product_id,
                create_product_form.Name.data,
                create_product_form.Description.data,
                create_product_form.Price.data,
                5,
                0,
            )

            product_dict[product_id] = product
            db['Product'] = product_dict  # Correct the key name to 'Product'
        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()
        return redirect(url_for('sales'))  # Change the target route to 'sales' instead of 'retrieve_users'

    return render_template('createProduct.html', form=create_product_form, id=id)
@app.route('/sales')
def sales():
    product_list = []
    db = shelve.open('product.db', 'r')

    try:
        product_dict = db.get('Product', {})
        for key in product_dict:
            product = product_dict.get(key)
            product.calculate_overall_sales()  # Calculate overall sales for each product
            product_list.append(product)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

    return render_template('sales.html', product_list=product_list)




@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    product_dict = {}
    db = shelve.open('product.db', 'w')
    product_dict = db['Product']

    product_dict.pop(id)

    db['Product'] = product_dict
    db.close()

    return redirect(url_for('sales'))


# Kiefer




if __name__ == "__main__":
    app.run(debug=True)
