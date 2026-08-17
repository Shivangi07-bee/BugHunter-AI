import requests


class SessionManager:
    """
    Manages HTTP sessions for BugHunter AI.

    Responsibilities:
    - Maintain cookies
    - Maintain headers
    - Reuse authenticated sessions
    - Reset investigation sessions
    """

    def __init__(self):

        self.session = requests.Session()

    # --------------------------------------------------

    def get_session(self):

        return self.session

    # --------------------------------------------------

    def set_header(self, key, value):

        self.session.headers[key] = value

    # --------------------------------------------------

    def remove_header(self, key):

        self.session.headers.pop(key, None)

    # --------------------------------------------------

    def update_headers(self, headers):

        self.session.headers.update(headers)

    # --------------------------------------------------

    def clear_headers(self):

        self.session.headers.clear()

    # --------------------------------------------------

    def set_cookie(self, name, value):

        self.session.cookies.set(name, value)

    # --------------------------------------------------

    def clear_cookies(self):

        self.session.cookies.clear()

    # --------------------------------------------------

    def reset(self):

        self.session.close()

        self.session = requests.Session()