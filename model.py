from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# model definitions
# create user and article first to reference association table 

class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    """user's session"""
    __tablename__ = "users"

    # user_session = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_session = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_language = db.Column(db.String(2), nullable=True)
    # TODO: set visits

    def __repr__(self):
        return f'<session: {self.user_session} lang: {self.user_language}'

    def serialize(self):
        return {"user_session": self.user_session,
                "user_language": self.user_language}


class Article(ModelMixin, db.Model):
    """article info"""
    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_heading = db.Column(db.String(400), nullable=False)
    article_url = db.Column(db.String(600), nullable=False)
    # article_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<id: {self.article_id} heading: {self.article_heading}>'


class User_article(ModelMixin, db.Model):
    """association table between Article and User"""
    __tablename__ = "users_articles"

    user_article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_session = db.Column(db.Integer, db.ForeignKey('users.user_session'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'), nullable=False)

    user = db.relationship('User', backref='users_articles')
    article = db.relationship('Article', backref='users_articles')

    def __repr__(self):
        return f'<id: {self.user_article_id} session: {self.user_session} article: {self.article_id}>'


def connect_to_db(app, uri="postgresql:///translation2020"):
    """Connect the database to Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")