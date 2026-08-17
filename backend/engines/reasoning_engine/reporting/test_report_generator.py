from pprint import pprint

from engines.reasoning_engine.reporting.report_generator import ReportGenerator

from engines.reasoning_engine.llm.reasoning_engine import (

    AIReasoningResult

)

runtime = {

    "repository":"Demo App",

    "workflow":"Authentication"

}

reasoning = AIReasoningResult(

    summary="Authentication investigated.",

    attack_analysis="Possible authentication weakness.",

    confidence=0.91,

    verdict="Potential High Risk",

    recommendations="Verify JWT validation."

)

generator = ReportGenerator(

    runtime,

    reasoning

)

report = generator.generate()

pprint(report)