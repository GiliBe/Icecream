# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor  # Changed this line
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
import os

from config import Config
from models import db, User, IceCream, Order, OrderItem

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter()
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Configure metrics
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter())
meter_provider = MeterProvider(metric_readers=[metric_reader])
meter = meter_provider.get_meter(__name__)

# Create counters and histograms
order_counter = meter.create_counter(
    name="ice_cream_orders",
    description="Number of ice cream orders",
    unit="1",
)

order_value_histogram = meter.create_histogram(
    name="order_value_distribution",
    description="Distribution of order values",
    unit="USD",
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Flask instrumentation (changed this line)
FlaskInstrumentor().instrument_app(app)

# Rest of the application code remains the same...
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    ice_creams = IceCream.query.all()
    return render_template('index.html', ice_creams=ice_creams)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/order', methods=['POST'])
@login_required
def place_order():
    with tracer.start_as_current_span("place_order") as span:
        # Create new order
        order = Order(user_id=current_user.id, total_amount=0)
        db.session.add(order)
        
        total_amount = 0
        for item in request.form:
            if item.startswith('quantity_'):
                ice_cream_id = int(item.split('_')[1])
                quantity = int(request.form[item])
                if quantity > 0:
                    ice_cream = IceCream.query.get(ice_cream_id)
                    if ice_cream.stock >= quantity:
                        order_item = OrderItem(
                            order=order,
                            ice_cream_id=ice_cream_id,
                            quantity=quantity,
                            price=ice_cream.price
                        )
                        db.session.add(order_item)
                        total_amount += quantity * ice_cream.price
                        ice_cream.stock -= quantity
                    else:
                        flash(f'Not enough stock for {ice_cream.name}')
                        return redirect(url_for('index'))

        order.total_amount = total_amount
        db.session.commit()

        # Record metrics
        order_counter.add(1)
        order_value_histogram.record(total_amount)
        
        span.set_attribute("order.id", order.id)
        span.set_attribute("order.amount", total_amount)
        
        flash('Order placed successfully!')
        return redirect(url_for('order_history'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    orders = Order.query.all()
    ice_creams = IceCream.query.all()
    users = User.query.all()
    return render_template('admin/dashboard.html', orders=orders, ice_creams=ice_creams, users=users)

@app.route('/admin/ice-cream/add', methods=['GET', 'POST'])
@login_required
def add_ice_cream():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))

    if request.method == 'POST':
        ice_cream = IceCream(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock'])
        )
        db.session.add(ice_cream)
        db.session.commit()
        flash('Ice cream added successfully!')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_ice_cream.html')

@app.route('/order-history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).all()
    return render_template('order_history.html', orders=orders)



# Additional routes and functionality for app.py

@app.route('/admin/ice-cream/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ice_cream(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    ice_cream = IceCream.query.get_or_404(id)
    
    if request.method == 'POST':
        ice_cream.name = request.form['name']
        ice_cream.description = request.form['description']
        ice_cream.price = float(request.form['price'])
        ice_cream.stock = int(request.form['stock'])
        
        db.session.commit()
        flash('Ice cream updated successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_ice_cream.html', ice_cream=ice_cream)

@app.route('/admin/ice-cream/delete/<int:id>', methods=['POST'])
@login_required
def delete_ice_cream(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    ice_cream = IceCream.query.get_or_404(id)
    db.session.delete(ice_cream)
    db.session.commit()
    
    flash('Ice cream deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/order/<int:id>')
@login_required
def view_order(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(id)
    return render_template('admin/order_view.html', order=order)

@app.route('/admin/order/<int:id>/status', methods=['POST'])
@login_required
def update_order_status(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'preparing', 'ready', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated successfully!')
    
    return redirect(url_for('view_order', id=id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
            
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/create-admin', methods=['GET', 'POST'])
def create_admin():
    # Check if any admin exists
    if User.query.filter_by(is_admin=True).first():
        flash('Admin user already exists!', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        # Get secret key from environment variable
        # admin_secret = os.getenv('ADMIN_SECRET_KEY', 'your-secret-key')
        
        # if request.form.get('secret_key') != admin_secret:
        #     flash('Invalid secret key!', 'error')
        #     return redirect(url_for('create_admin'))
            
        admin = User(
            username=request.form['username'],
            email=request.form['email'],
            password_hash=generate_password_hash(request.form['password']),
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('login'))
        
    return render_template('admin/create_admin.html')


# Add these routes to app.py

@app.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
def toggle_admin(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(id)
    
    # Prevent self-demotion
    if user.id == current_user.id:
        flash('Cannot change your own admin status', 'error')
        return redirect(url_for('manage_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    flash(f'Admin status updated for {user.username}', 'success')
    return redirect(url_for('manage_users'))
# Enhanced metrics
# from opentelemetry.sdk.metrics import Counter, Histogram
# from datetime import datetime, timedelta

# # Additional metrics
# stock_level_gauge = meter.create_up_down_counter(
#     name="ice_cream_stock_levels",
#     description="Current stock levels for each ice cream flavor",
#     unit="units",
# )

# order_processing_time = meter.create_histogram(
#     name="order_processing_time",
#     description="Time taken to process orders",
#     unit="seconds",
# )

# revenue_by_flavor = meter.create_counter(
#     name="revenue_by_flavor",
#     description="Revenue generated by each ice cream flavor",
#     unit="USD",
# )

#
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)