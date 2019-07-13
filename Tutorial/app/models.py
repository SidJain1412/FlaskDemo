from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Adding a table for followers for users
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )


# When making changes to models, you must migrate again
# No need to remake the entire table and drop existing entries
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # Users that a user has followed
    # Followers can be added like `user1.followed.append(user2)`
    # Removed like `user1.followed.remove(user2)`
    followed = db.relationship(
        'User', secondary=followers,
        # .c is to access column
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generating random avatar for a user through gravatar
    # We send gravatar a MD5 hash of the user's email
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # Boolean, whether following or not
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def folowed_posts(self):
        # First we join on the followers table (as it is our association)
        # We are making a temporary table through this join
        # We see the posts where user_id is same as followed id for a follower
        # Now we filter where follower_id is same as user id
        # Then we sort on descending timestamp
        # This `followed` has all posts by the people a user follows
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.followed_id == self.id)
        # But it doesn't have user's own posts
        # User's own posts:
        own = Post.query.filter_by(user_id==self.id)
        # Returning union of own and following posts, sorted by timestamp
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # Not calling the datetime.utcnow function, but naming it
    # This is because default gets executed, not assigned
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
