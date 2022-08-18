from app import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name
