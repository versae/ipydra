import easywebdav

from flask.ext.wtf import TextField

from ipydra import DAV_URI
from ipydra.forms import LoginForm as BaseLoginForm


if not DAV_URI:
    LoginForm = BaseLoginForm
else:
    dav_host, dav_path = DAV_URI.split("/", 1)

    class LoginForm(BaseLoginForm):
        password = TextField('Password')

        def validate(self):
            is_valid = super(LoginForm, self).validate()
            if is_valid:
                webdav = easywebdav.connect(
                    dav_host,
                    username=self.username.data,
                    password=self.password.data
                )
                try:
                    webdav.ls(dav_path)
                except:
                    is_valid = False
            return is_valid
