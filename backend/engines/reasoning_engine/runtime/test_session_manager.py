from pprint import pprint

from engines.reasoning_engine.runtime.session_manager import SessionManager

session = SessionManager("Demo Application")

session.complete_goal()

session.add_evidence()

session.add_evidence()

session.add_observation()

session.update_metadata(

    "language",

    "Python"

)

pprint(

    session.summary()

)