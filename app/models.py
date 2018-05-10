from app import db

class Website(db.Model):
    """
    The websites to scrape.
    
    @website - websites where people buy and sell sex.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(), unique=True, nullable=False)  

    def __init__(self, website):
        self.website = website

        
class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String)

    def __init__(self, place):
        self.place = place

class AdUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    scraped = db.Column(db.Boolean)

    def __init__(self, url, scraped):
        self.url = url
        self.scraped = scraped


class AdInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    date_posted = db.Column(db.String)
    url = db.Column(db.String)
    phone_number_body = db.Column(db.String)
    phone_number_title = db.Column(db.String)
    
    def __init__(self,
                 title,
                 body,
                 date_posted,
                 url,
                 phone_number_body,
                 phone_number_title):
        self.title = title
        self.date_posted = date_posted
        self.url = url
        self.body = body
        self.phone_number_body = phone_number_body
        self.phone_number_title = phone_number_title
        
