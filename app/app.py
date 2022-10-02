import json
import os
from flask import Flask, render_template, flash, request, url_for, redirect, Markup, session
from flask_session import Session
import uuid

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def calculate_total(arr):
    total = 0
    for el in arr:
        total += int(float(el['price']))

    return total

@app.route('/')
@app.route('/', methods=(['POST']))
def main():
    filename = os.path.join(app.static_folder, 'data', 'products.json')

    with open(filename) as test_file:
        data = app.json.load(test_file)

        
    if request.method == 'POST':
        obj = eval(request.form['object'])
        if 'cart' not in session:
            session['cart'] = []
        aux_cart = session['cart']
        aux_cart.append(obj)
        session['cart'] = aux_cart
        

        message = Markup(f'<div class="popup" style="background-color:{obj["bgColor"]}" class="teste"><span class="popup-strong">{obj["name"]}</span><span class="popup-normal"> has been added to your cart.</span> </div>')
        flash(message)


    return render_template('main.html', data=data, cart_size=len(session['cart']))

@app.route('/cart/')
@app.route('/cart/', methods=(['POST']))
def cart():
    if request.method == 'POST':
        index = eval(request.form['index'])
        aux_cart = session['cart']
        del aux_cart[index-1]
        session['cart'] = aux_cart

    return render_template('cart.html', cart=session['cart'],  cart_size=len(session['cart']), total=calculate_total(session['cart']))


@app.route('/checkout/')
@app.route('/checkout/', methods=(['POST']))
def checkout():
    if request.method == 'POST':
        accepted = request.form.getlist('check')
        if 'on' in accepted and len(request.form['name'])>4 and len(request.form['email'])>4 and len(session['cart'])>0:
            id = uuid.uuid4().hex

            info_and_cart = [{
                'name': request.form['name'],
                'email': request.form['email'],
                'total': calculate_total(session['cart']),
                'order_id': id
            }]

            info_and_cart.append(session['cart'])

            with open(f'./orders/order_{id}.json', 'w') as f:
                json.dump(info_and_cart, f, indent=2)
                session['cart'] = []
                return redirect(url_for('main'))  
        else:
            message = Markup('<span>Please fill in all the <span class="flash-cart-strong">fields</span> and accept the <span class="flash-cart-strong">terms and conditions</span></span>.')
            flash(message)      

    return render_template('checkout.html', cart_size=len(session['cart']), total=calculate_total(session['cart']))