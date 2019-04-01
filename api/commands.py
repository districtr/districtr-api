from .models import User, db


def make_admin(user_email):
    user = User.by_email(user_email)
    if not user.has_role("admin"):
        user.add_role("admin")
        db.session.commit()
