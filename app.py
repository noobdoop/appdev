from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

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
    app.run()