from app import utils
from app.extensions import db


class BaseModel(object):
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(BaseModel, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_on = db.Column(db.DateTime(timezone=True))
    waitlist = db.relationship('Waitlist', uselist=False, back_populates='user')

    def __init__(self, email):
        self.email = email


referrals = db.Table(
    'referral',
    db.Column('referring', db.String(8), db.ForeignKey('waitlist.uuid')),
    db.Column('referred', db.String(8), db.ForeignKey('waitlist.uuid')),
    db.PrimaryKeyConstraint('referring', 'referred', name='referrals_pk')
)


class Waitlist(BaseModel, db.Model):
    __tablename__ = 'waitlist'

    initial_score = 65231
    decrease_per_referral = 10

    uuid = db.Column(db.String(8), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='waitlist')
    score = db.Column(db.Integer)
    referred = db.relationship(
        'Waitlist',
        secondary=referrals,
        primaryjoin=(referrals.c.referring == uuid),
        secondaryjoin=(referrals.c.referred == uuid),
        backref=db.backref('referral', lazy='dynamic'), lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id
        self.set_uuid()
        self.set_initial_score()

    def set_uuid(self):
        uuid = utils.generate_simple_uuid(8)
        while db.session.query(Waitlist).filter_by(uuid=uuid).one_or_none():
            uuid = utils.generate_simple_uuid(8)
        self.uuid = uuid

    def set_initial_score(self):
        self.score = self.initial_score + db.session.query(Waitlist).count() + 1
