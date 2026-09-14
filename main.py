from flask import Flask, render_template_string,request, redirect, url_for, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tere_website_ka_secret_key_2026"

# Dummy Database - yaha apna data change kar sakta hai
PRODUCTS = [
    {"id": 1, "name": "Custom Alloy Wheel Showpiece", "price": 499, "desc": "Hand-painted tyre showpiece - Black & White"},
    {"id": 2, "name": "Husky Dance Toy", "price": 299, "desc": "Cute dancing husky for desk"},
    {"id": 3, "name": "Custom Name Plate", "price": 899,  "desc": "Personalized 3D name plate"},
]

ORDERS = []
MESSAGES = []

# HTML + CSS + JS - Sab ek hi file me taki tujhe tension na ho
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My 3rd Website - Official</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI', sans-serif}
        body{background:#0f0f0f;color:#fff;overflow-x:hidden}
        nav{display:flex;justify-content:space-between;align-items:center;padding:20px 5%;background:#1a1a1a;position:sticky;top:0;z-index:100}
        nav h1{color:#00ff88} nav a{color:#fff;margin-left:20px;text-decoration:none;font-weight:600}
        nav a:hover{color:#00ff88}
        .hero{height:80vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:linear-gradient(135deg,#000,#222)}
        .hero h2{font-size:3.5rem;margin-bottom:10px} .hero span{color:#00ff88}
        .hero p{color:#aaa;margin:20px 0;max-width:600px}
        .btn{padding:12px 30px;background:#00ff88;color:#000;border:none;border-radius:30px;font-weight:bold;cursor:pointer;transition:0.3s;text-decoration:none;display:inline-block}
        .btn:hover{transform:scale(1.05);box-shadow:0 0 20px #00ff88}
        .section{padding:60px 5%}
        .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-top:30px}
        .card{background:#1e1e1e;padding:20px;border-radius:15px;text-align:ce8nter;transition:0.3s;border:1px solid #333}
        .card:hover{transform:translateY(-10px);border-color:#00ff88}
        .card .icon{font-size:50px;margin-bottom:10px}
        .card h3{margin:10px 0} .price{color:#00ff88;font-weight:bold;font-size:1.2rem}
        .contact-form{max-width:500px;margin:30px auto;background:#1e1e1e;padding:30px;border-radius:15px}
        .contact-form input,.contact-form textarea{width:100%;padding:12px;margin:10px 0;background:#111;border:1px solid #333;color:#fff;border-radius:8px}
        footer{text-align:center;padding:30px;background:#1a1a1a;color:#777;margin-top:40px}
        .cart-badge{background:red;color:#fff;padding:2px 8px;border-radius:50%;font-size:12px}
        @media(max-width:600px){.hero h2{font-size:2rem}}
    </style>
</head>
<body>
    <nav>
        <h1>3RD WEBSITE</h1>
        <div>
            <a href="/">Home</a>
            <a href="#products">Products</a>
            <a href="#contact">'Contact</a>
            <a href="/admin">Admin ({{ orders|length }})</a>
        </div>
    </nav>

    <div class="hero">
        <h2>Welcome to My <span>3rd Website</span></h2>
        <p>Ye mera teesra aur sabse best website hai. Yaha custom showpiece, toys aur creative cheeze milengi.</p>
        <a href="#products" class="btn">Explore Now</a>
        <p 
        style="margin-top:20px;color:#555">Made in ramgarh,jharkhand</p>
    </div>

    <div class="section" id="products">
        <h2 style="font-size:2.5rem">Our Products</h2>
        <p style="color:#aaa">Tere haath ke bane showpieces jaisa collection</p>
        <div class="grid">
            {% for p in products %}
            <div class="card">
                <h3>{{ p.name }}</h3>
                <p style="color:#999;font-size:0.9rem">{{ p.desc }}</p>
                <p class="price">₹{{ p.price }}</p>
                <br>::
                <form method="post" action="/buy/{{ p.id }}">
                    <button class="btn" type="submit">Buy Now</button>
                </form>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="section" id="contact" style="background:#111">
        <h2 style="text-align:center;font-size:2.5rem">Contact Us</h2>
        <div class="contact-form">
            <form method="post" action="/contact">
                <input type="text" name="name" placeholder="Tera Naam" required>
                <input type="email" name="email" placeholder="Email" required>
                <textarea name="msg" rows="4" placeholder="Message likh bhai..." required></textarea>
                <button class="btn" style="width:100%" type="submit">Send Message</button>
            </form>
            {% if success %}<p style="color:#00ff88;text-align:center;margin-top:15px">{{ success }}</p>{% endif %}
        </div>
    </div>

    <footer>
        <p>© 2026 My 3rd Website | Built with Flask in Python | Patna</p>
        <p style="font-size:12px;margin-top:10px">Total Orders: {{ orders|length }} | Messages: {{ messages|length }}</p>
    </footer>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<h2 style="font-family:sans-serif;padding:20px">Admin Panel - Orders & Messages</h2>
<a href="/">Back to Home</a><hr>
<h3>Orders ({{ orders|length }})</h3>
{% for o in orders %}
<p>{{ o.time }} - {{ o.product }} - Rs.{{ o.price }}</p>
{% endfor %}
<hr>
<h3>Messages ({{ messages|length }})</h3>
{% for m in messages %}
<p><b>{{ m.name }} ({{ m.email }})</b>: {{ m.msg }} - <i>{{ m.time }}</i></p>
{% endfor %}
"""

@app.route("/")
def home():
    return render_template_string(MAIN_TEMPLATE, products=PRODUCTS, orders=ORDERS, messages=MESSAGES, success=request.args.get('msg'))

@app.route("/buy/<int:pid>", methods=["POST"])
def buy(pid):
    product = next((p for p in PRODUCTS if p["id"]==pid), None)
    if product:
        ORDERS.append({"product": product["name"], "price": product["price"], "time": datetime.now().strftime("%d-%m-%Y %H:%M")})
    return redirect(url_for('home', msg=f"Order placed for {product['name']}!"))

@app.route("/contact", methods=["POST"])
def contact():
    MESSAGES.append({
        "name": request.form['name'],
        "email": request.form['email'],
        "msg": request.form['msg'],
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    return redirect(url_for('home', msg="Message bhej diya! Jaldi reply karunga."))

@app.route("/admin")
def admin():
    return render_template_string(ADMIN_TEMPLATE, orders=ORDERS, messages=MESSAGES)

@app.route("/api/products")
def api():
    return jsonify(PRODUCTS)

if __name__ == "__main__":
    print("Bhai tera 3rd website chal raha hai: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
