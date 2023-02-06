try:
    from .config import db
except:
    from  __main__ import db
from flask_login import UserMixin
import random, string
from datetime import datetime


def specific_string(length):  
    sample_string = 'abcdefghijklmnoprstuwxyzABCDEFGHIJKLMNOPRSTUWXYZ' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    # result = "BNihdoIHkjOhuxklEGwnJxBhLZjBUlyM"
    return result 


def unique_str(object, length, field):
    print(field)
    # print(dir(field))
    # return False
    while True:
        gen_str = specific_string(length)
        try:
            if field == "activate_string":
                qr = object.query.filter_by(activate_string=gen_str).all()

            elif field == "declaration_string":
                qr = object.query.filter_by(declaration_string=gen_str).all()

            elif field == "invitation_string":
                qr = object.query.filter_by(invitation_string=gen_str).all()

        except Exception as e:
            return False

        if len(qr)<1:
            print(gen_str)
            return gen_str
 

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    superadmin = db.Column(db.Boolean, default=False, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    login_parameter = db.Column(db.String(128), unique=True, nullable=True)
    # activate_string = db.Column(db.String(128), unique=True, default=specific_string(32))
    activate_string = db.Column(db.String(128), unique=True)
    info = db.Column(db.String(128), unique=True, nullable=True)
    
    added_by = db.Column(db.Integer, nullable=True, default=None)

    def __str__(self):
        return self.email


class Divisions(db.Model, UserMixin):
    __tablename__ = "divisions"
    id = db.Column(db.Integer, primary_key=True)
    division_name = db.Column(db.String(128))
    division_leader = db.Column(db.String(128))

    superadmin_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    event_id = db.Column(db.Integer, db.ForeignKey("event.id", ondelete="CASCADE"))
    
    superadmin = db.relationship("User", backref='divisions', lazy=True)
    event = db.relationship("Event", backref='divisions_events', lazy=True)
 

    def __str__(self):
        return self.division_name




class Event(db.Model, UserMixin):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    superadmin_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    date =  db.Column(db.Date)
    delcaration_deadline =  db.Column(db.Date)
    time =  db.Column(db.Time)

    address = db.Column(db.String(512))
    google_map_iframe = db.Column(db.String(512), nullable=True)
    google_map_link = db.Column(db.String(512), nullable=True)
    place_img = db.Column(db.String(512), nullable=True)

    superadmin = db.relationship("User", backref='event', lazy=True)

    declaration_mail_content = db.Column(db.String(2048), nullable=True)
    invitation_mail_content = db.Column(db.String(2048), nullable=True)

    image_link_header = db.Column(db.String(1024))
    image_link_footer = db.Column(db.String(1024))
    contact_to_organizators = db.Column(db.String(256))



    def __str__(self):
        return self.name


class Accompanying(db.Model):
    __tablename__ = "accompanying"

    id = db.Column(db.Integer, primary_key=True)


    
    first_name = db.Column(db.String(128), unique=False, nullable=True)
    last_name = db.Column(db.String(128), unique=False, nullable=True)
    email = db.Column(db.String(128), unique=False, nullable=True)
    invitation_string = db.Column(db.String(128), server_default="", unique=True)

    how_paid = db.Column(db.String(128), server_default="")


    event_id = db.Column(db.Integer, db.ForeignKey("event.id", ondelete="CASCADE"))
    event = db.relationship("Event", 
        backref='accompanying', 
        lazy=True
        )



class Participants(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))

    invitation_sent = db.Column(db.Boolean, default=False, nullable=False)

    declaration_sent = db.Column(db.Boolean, default=False, nullable=False)
    declarated = db.Column(db.Boolean, default=False, nullable=False)
    # declaration_string = db.Column(db.String(128), unique=True, default=specific_string(48))
    declaration_string = db.Column(db.String(128), unique=True)
    present = db.Column(db.Boolean, default=False, nullable=False)
    email_sent = db.Column(db.Boolean, default=False, nullable=False)
    invitation_string = db.Column(db.String(128), server_default="", unique=True)

    first_name_by_user = db.Column(db.String(128))
    last_name_by_user = db.Column(db.String(128))
    email_by_user = db.Column(db.String(128))
    
    canceled = db.Column(db.Boolean, default=False, nullable=False)
    is_vip = db.Column(db.Boolean, default=False, nullable=False)
    

    car_park = db.Column(db.Boolean,  default=False)
    personal_data = db.Column(db.Boolean,  default=False,  nullable=False)

    
    # accompanying_person = db.Column(db.Boolean,  default=False,  nullable=False)
    # accompanying_person_first_name = db.Column(db.String(128), unique=False, nullable=True)
    # accompanying_person_last_name = db.Column(db.String(128), unique=False, nullable=True)
    # accompanying_person_email = db.Column(db.String(128), unique=False, nullable=True)
    



    division_id = db.Column(db.Integer, db.ForeignKey("divisions.id", ondelete="CASCADE"))
    added_by_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id", ondelete="CASCADE"))
    accomapnying_id = db.Column(db.Integer, db.ForeignKey("accompanying.id", ondelete="CASCADE"))


    added_by = db.relationship("User", 
        backref='participants', 
        lazy=True
        )
    event = db.relationship("Event", 
        backref='participants', 
        lazy=True
        )
    division = db.relationship("Divisions", 
        backref='participants', 
        lazy=True
        )
    accompanying = db.relationship("Accompanying", 
        backref='participants', 
        lazy=True,
        uselist=False
        )


    def __str__(self):
        return self.email




class Enters(UserMixin,db.Model):
    __tablename__ = "enters"
    id = db.Column(db.Integer, primary_key=True)
    #user has entered meas that participant is in the building
    has_entered = db.Column(db.Boolean, default=True)
    date =  db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    participant_id = db.Column(db.Integer,db.ForeignKey("participants.id", ondelete="CASCADE"), nullable=True)
    accompanying_id = db.Column(db.Integer,db.ForeignKey("accompanying.id", ondelete="CASCADE"), nullable=True )
    recorded_by_id = db.Column(db.Integer,db.ForeignKey("user.id", ondelete="CASCADE") )
    event_id = db.Column(db.Integer,db.ForeignKey("event.id", ondelete="CASCADE") )

    participant = db.relationship("Participants", 
        backref='enters', 
        lazy=True
        )
    accompanying = db.relationship("Accompanying", 
        backref='enters', 
        lazy=True
        )

    recorded_by = db.relationship("User", 
        backref='enters', 
        lazy=True
        )
    event = db.relationship("Event", 
        backref='enters', 
        lazy=True
        )

