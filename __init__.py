from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateStaffForm, CreateProductForm, CreateCustomerForm, UpdatePassword
import shelve
from User import Staff, Product
from Customer import Customer
import hashlib
import matplotlib.pyplot as plt

app = Flask(__name__)

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat/')
def chat():
    return render_template('chat.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/createUser', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db.get('Staff', {})
            staff_id = max(staff_dict.keys(), default=0) + 1
            hashed_password = hash_password(create_staff_form.Password.data)

            staff = Staff(
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
                            create_customer_form.date_joined.data,
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
            product = staff_dict.get(key)
            staff_list.append(product)
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
    update_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']
        hashed_password = hash_password(update_staff_form.Password.data)

        Staff = staff_dict.get(id)
        Staff.set_Username(update_staff_form.Username.data)
        Staff.set_Email(update_staff_form.Email.data)
        Staff.set_PhoneNo(update_staff_form.PhoneNo.data)
        Staff.set_Password(hashed_password)

        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('home'))
    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        Staff = staff_dict.get(id)
        update_staff_form.Username.data = Staff.get_Username()
        update_staff_form.Email.data = Staff.get_Email()
        update_staff_form.PhoneNo.data = Staff.get_PhoneNo()
        update_staff_form.Password.data = Staff.get_Password()

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
                0
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



if __name__ == '__main__':
    app.run(debug=True)
