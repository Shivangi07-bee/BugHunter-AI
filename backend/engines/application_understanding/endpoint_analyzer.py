import ast


class EndpointAnalyzer:

    def __init__(self, source_files, routes):
        self.source_files = source_files
        self.routes = routes

    def analyze(self):

        analysis = []

        for route in self.routes:

            filename = route["file"]

            handler = route["handler"]

            for file in self.source_files:

                if file.name != filename:
                    continue

                with open(file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                endpoint = {
                    **route,
                    "calls": [],
                    "models": []
                }

                for node in ast.walk(tree):

                    if isinstance(node, ast.FunctionDef):

                        if node.name != handler:
                            continue

                        for child in ast.walk(node):

                            if isinstance(child, ast.Call):

                                if isinstance(child.func, ast.Name):

                                    endpoint["calls"].append(
                                        child.func.id
                                    )

                                elif isinstance(child.func, ast.Attribute):

                                    endpoint["calls"].append(
                                        child.func.attr
                                    )

                            if isinstance(child, ast.Name):

                                if child.id[0].isupper():

                                    endpoint["models"].append(
                                        child.id
                                    )

                endpoint["calls"] = list(
                    set(endpoint["calls"])
                )

                endpoint["models"] = list(
                    set(endpoint["models"])
                )

                analysis.append(endpoint)

        return analysis