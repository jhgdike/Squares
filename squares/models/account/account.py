from squares.ext import db


def _make_password(password):
    return password


class Account(db.Model):
    """Account System."""
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    @classmethod
    def add(cls, username, password):
        password = _make_password(password)
        rs = cls(username=username, password=password)
        db.session.add(rs)
        db.session.commit()
        return rs

    def change_password(self, password):
        self.password = _make_password(password)
        db.session.commit()

    @classmethod
    def get(cls, id):
        return Account.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, name):
        return Account.query.filter_by(username=name).first()

    def check_password(self, password):
        return self.password == _make_password(password)

    @classmethod
    def check(cls, username, password):
        rs = cls.get_by_name(username)
        if rs and rs.check_password(password):
            return True
        return False

    @classmethod
    def login(cls, username):
        pass

    def logout(self):
        pass
