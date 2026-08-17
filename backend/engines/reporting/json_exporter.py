import json
import os


class JsonExporter:
    """
    Exports the BugHunter AI report as JSON.
    """

    def __init__(self, report):

        self.report = report

    # --------------------------------------------------

    def export(
        self,
        output_directory="reports",
        filename="BugHunter_Report.json"
    ):

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        output_path = os.path.join(
            output_directory,
            filename
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.report,
                file,
                indent=4,
                default=str
            )

        return output_path