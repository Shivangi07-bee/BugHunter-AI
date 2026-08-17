from pprint import pprint

from engines.reasoning_engine.runtime.investigation_history import InvestigationHistory

history = InvestigationHistory()

history.record(

    "Repository Loaded"

)

history.record(

    "Workflow Built"

)

history.record(

    "Authentication Hypothesis Generated"

)

history.record(

    "Attack Plan Created"

)

history.record(

    "Reflection Completed"

)

pprint(

    history.summary()

)