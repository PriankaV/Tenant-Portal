from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20))

    def __repr__(self):
        return f'<User {self.name}>'

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Property {self.address}>'
