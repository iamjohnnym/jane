from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    company = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    domain_access = db.Column(db.String(124))
    email = db.Column(db.String(100), index=True)
    passwd = db.Column(db.String(64))
    sudoer = db.Column(db.String(64))
    shell = db.Column(db.String(64))
    created = db.Column(db.String(64), index=True)
    active = db.Column(db.String, index=True, default="Active")

#    def __repr__(self):
#        return '<User %r' % (self.username)

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(64), unique=True)
    usage = db.Column(db.Integer)
    created = db.Column(db.DateTime, index=True)
    active = db.Column(db.String, index=True, default="Active")
    
    
    def __repr__(self):
        return '<Domain %r' % (self.domain)

#class System(db.Model):
#    pass
