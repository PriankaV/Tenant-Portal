from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# User Model (Existing)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20))

    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f'<User {self.username}>'

# Property Model (Existing)
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Property {self.address}>'

# Tenant Model
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    move_in_date = db.Column(db.Date, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('tenants', lazy=True))
    property = db.relationship('Property', backref=db.backref('tenants', lazy=True))

    def __repr__(self):
        return f'<Tenant {self.user.name}>'

# Lease Model
class Lease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    rent_amount = db.Column(db.Float)
    tenant = db.relationship('Tenant', backref=db.backref('leases', lazy=True))
    property = db.relationship('Property', backref=db.backref('leases', lazy=True))

    def __repr__(self):
        return f'<Lease {self.id} for Property {self.property_id}>'

# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('lease.id'), nullable=False)
    due_date = db.Column(db.Date)
    payment_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))  # e.g., "Paid", "Due", "Overdue"
    lease = db.relationship('Lease', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.id} for Lease {self.lease_id}>'

# Maintenance Request Model
class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pending")
    request_date = db.Column(db.Date, default=datetime.utcnow)
    tenant = db.relationship('Tenant', backref=db.backref('requests', lazy=True))

    def __repr__(self):
        return f'<MaintenanceRequest {self.id} by Tenant {self.tenant_id}>'

# Document Model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('lease.id'), nullable=False)
    document_name = db.Column(db.String(100))
    document_path = db.Column(db.String(255))
    upload_date = db.Column(db.Date, default=datetime.utcnow)
    lease = db.relationship('Lease', backref=db.backref('documents', lazy=True))

    def __repr__(self):
        return f'<Document {self.document_name} for Lease {self.lease_id}>'
