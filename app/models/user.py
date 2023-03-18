

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)


class Role(db.Model):
    pass
