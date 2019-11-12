from datetime import datetime
from datetime import timezone


from sqlalchemy.exc import IntegrityError


from app import utils
from app.models import referrals
from app.models import User
from app.models import Waitlist


def get_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


def get_user_by_email(email):
    return User.query.filter_by(email=email).one_or_none()


def get_waitlist_user(uuid):
    return Waitlist.query.filter_by(uuid=uuid).one_or_none()


def create_user(email):
    email = utils.normalize_email(email)
    user = User(email=email)
    user.save()

    waitlist_user = Waitlist(user.id)
    waitlist_user.save()

    return user


def verify_email(token):
    payload = utils.decode_jwt_token(token)
    user = get_user(payload['user_id'])
    if user is None:
        return

    if not user.email_confirmed:
        user.email_confirmed = True
        now = datetime.now(timezone.utc)
        user.email_confirmed_on = now
        user.save()

    if payload['referring_uuid'] is not None:
        refer(payload['referring_uuid'], user.waitlist.uuid)


def refer(referring_uuid, referred_uuid):
    referring_user = get_waitlist_user(referring_uuid)
    referred_user = get_waitlist_user(referred_uuid)
    try:
        referring_user.referred.append(referred_user)
        referring_user.score -= Waitlist.decrease_per_referral
        referring_user.save()
    except IntegrityError:
        pass


def get_waitlist_position(uuid):
    waitlist_user = get_waitlist_user(uuid)
    score = waitlist_user.score
    return Waitlist.query.filter(Waitlist.score <= score).count()


def get_completed_referrals(uuid):
    waitlist_user = get_waitlist_user(uuid)
    return waitlist_user.referred.filter(
        referrals.c.referring == waitlist_user.uuid).count()
