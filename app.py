from flask import Flask, render_template, request, jsonify
import shelve

app = Flask(__name__)


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
        ],
        "tags":['Kids','Large','Obstacle Course'],
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


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

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

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
