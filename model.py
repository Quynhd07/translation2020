from flask-sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# model definitions
# create party and sources first; they are foreign keys for other tables

class Party(db.Model):
    """optional: candidate's party"""

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_name = db.Column(db.String(30), nullable=False)

    # backref candidates and party 
    candidate = db.relationship('Candidate', backref='parties')

    def __repr__(self):
        """returns id and party name"""
        return f'<ID: {self.party_id} Party Name: {self.party_name}'



class Source(db.Model):
    """source of articles"""
    
    __tablename__ = 'sources'

    source_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    source_name = db.Column(db.String(30), nullable=False)

    # backref to Article 
    article = db.relationship('Article', backref='sources')

    def __repr__(self):
        """return id and source name"""
        return f'<ID: {self.source_id} Source: {self.source_name}>'



class Candidate(db.Model):
    """Leading presidential candidates"""

    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    candidate_name = db.Column(db.String(30), nullable=False)
    twitter_handle = db.Column(db.String(15), nullable=True)
    party_id = db.Column(db.Integer, db.Foreign_Key='parties.party_id', nullable=True)

    def __repr__(self):
        """returns id, name, and twitter handle"""
        return f'<ID: {self.candidate_id} Name: {self.candidate_name} Twitter: {self.twitter_handle}>'



class Article(db.Model):
    """article information"""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key= True)
    article_title = db.Column(db.String(300), nullable=False)
    source_id = db.Column(db.Integer, db.Foreign_Key=('sources.source_id'))
    # review DateTime from ratings lab
    article_date = db.Column(db.DateTime, nullable=False)
    article_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """returns id and title"""
        return f'<ID: {self.article_id} Title: {self.article_title}>'



class Candidate_article(db.Model):
    """association table for candidates and articles"""
    
    __tablename__ = "candidates_articles"

    candidate_article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    candidate_id = db.Column(db.Integer, db.Foreign_Key=('candidates.candidate_id'))
    article_id = db.Column(db.Integer, db.Foreign_Key=('articles.article_id'))

    # backref to Candidate and Article
    candidate = db.relationship('Candidate', backref='candidates_articles')
    article = db.relationship('Article', backref='candidates_articles')

    def __repr__(self):
        """returns all id's"""
        return f'<ID: {self.candidate_article_id} Candidate: {candidate_id} Article: {self.article_id}>'


