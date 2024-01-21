from flask import Flask, render_template, url_for

app = Flask(__name__)
#temp database
products = [
    {
        "id": 1,
        "name": "Bouncy Castle",
        "image_url": "/static/Images/bouncycastle.png",
        "price": 45,
        "description": "A fun bouncy castle for kids to enjoy!",
        "rating": 5
    },
    {
        "id": 2,
        "name": "Dollhouse",
        "image_url": "/static/Images/dollhouse.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 3,
        "name": "Remote-Controlled Car",
        "image_url": "/static/Images/car.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 4,
        "name": "Beyblade",
        "image_url": "/static/Images/beyblade.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
{
        "id": 5,
        "name": "Trampoline",
        "image_url": "/static/Images/trampoline.png",
        "price": 45,
        "description": "A fun bouncy castle for kids to enjoy!",
        "rating": 5
    },
    {
        "id": 6,
        "name": "Hula Hoop",
        "image_url": "/static/Images/hulahoop.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 7,
        "name": "Inflatable Soccer and Basketball Arena",
        "image_url": "/static/Images/soccer.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
    {
        "id": 8,
        "name": "Skateboard",
        "image_url": "/static/Images/skateboard.png",
        "price": 25,
        "description": "A beautiful dollhouse for imaginative play.",
        "rating": 4
    },
]
@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

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
