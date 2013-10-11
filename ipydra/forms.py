from flask.ext.wtf import Form
from flask.ext.wtf import TextField


class LoginForm(Form):
    """ A simple login form for front end.
    """
    username = TextField('Username')

    def validate(self):
        if not self.username.data.isalnum():
            return False
        return True
