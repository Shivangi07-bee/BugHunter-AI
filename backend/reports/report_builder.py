from dataclasses import asdict, is_dataclass


class ReportBuilder:

    def build(self, workspace):

        report = {}

        for key, value in workspace.__dict__.items():

            if is_dataclass(value):
                report[key] = asdict(value)

            elif isinstance(value, list):

                report[key] = []

                for item in value:

                    if is_dataclass(item):
                        report[key].append(asdict(item))
                    else:
                        report[key].append(item)

            else:

                report[key] = value

        return report