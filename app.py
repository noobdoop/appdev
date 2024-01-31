from flask import Flask, render_template, request, jsonify, url_for, redirect

from chat import get_response

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

@app.route('/contactus')
def contact():
    return render_template('contactus.html')

@app.route('/stickGame')
def maze():
    return render_template('stickGame.html')

# chatbot stuff
@app.route("/predict", methods= ["POST"])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@app.route('/get_conversation_data', methods=['GET'])
def get_conversation_data():
    with shelve.open('conversation_data.db') as db:
        conversation_data = db.get('conversation', {})
        message_data = conversation_data.get('message', {})
        latest_msg_id = max(message_data.keys()) if message_data else 0
        conversation_data['msgID'] = latest_msg_id
    return jsonify(conversation_data)

@app.route('/delete_conversation_data', methods=['POST'])
def delete_conversation_data():
    msg_id_to_delete = request.form.get('msgID')
    with shelve.open('conversation_data.db', writeback=True) as db:
        if 'conversation' in db and 'message' in db['conversation']:
            message_data = db['conversation']['message']

            try:
                msg_id_to_delete = int(msg_id_to_delete)
            except ValueError:
                return "Invalid message ID provided."

            if msg_id_to_delete in message_data:
                del message_data[msg_id_to_delete]
                print(f"Conversation Data with ID {msg_id_to_delete} Deleted")

                remaining_msg_ids = list(message_data.keys())
                remaining_msg_ids.sort()
                for i, msg_id in enumerate(remaining_msg_ids, start=1):
                    if msg_id != i:
                        message_data[i] = message_data.pop(msg_id)
                print("Remaining Message IDs After Shift:", list(message_data.keys()))

                return "Conversation data deleted successfully"

    print(f"No conversation data found with ID {msg_id_to_delete} to delete")
    return "Failed to delete conversation data. Message ID not found."


# feedback form stuff
def get_feedback_data():
    with shelve.open('feedback_db') as db:
        return db.get('feedbacks', [])

@app.route('/get_feedback_data')
def get_feedback_data_route():
    feedbacks = get_feedback_data()
    return jsonify(feedbacks)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        # Retrieve feedback data from JSON request
        feedback_data = request.json

        # Save feedback data to Shelve database
        with shelve.open('feedback_db', writeback=True) as db:
            if 'feedbacks' not in db:
                db['feedbacks'] = []

            db['feedbacks'].append(feedback_data)

        print("Feedback data saved:", feedback_data)
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Error submitting feedback: {str(e)}")
        return jsonify({"status": "error"})


@app.route('/feedback')
def display_feedback():
    # Retrieve feedback data from Shelve database
    with shelve.open('feedback_db') as db:
        feedbacks = db.get('feedbacks', [])

    return render_template("feedback.html", feedbacks=feedbacks)

@app.route('/delete_feedback/<int:index>')
def delete_feedback(index):
    try:
        with shelve.open('feedback_db', writeback=True) as db:
            if 'feedbacks' in db and 0 < index <= len(db['feedbacks']):
                del db['feedbacks'][index - 1]
                return redirect(url_for('display_feedback'))

        return jsonify({"status": "error", "message": "Invalid index for deletion"})

    except Exception as e:
        print(f"Error deleting feedback: {str(e)}")
        return jsonify({"status": "error"})


# Game Stuff

if __name__ == "__main__":
    app.run(debug=True)
