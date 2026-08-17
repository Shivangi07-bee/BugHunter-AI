import re


class RouteDiscovery:

    def __init__(self, source_files):
        self.source_files = source_files

    def discover_routes(self):

        routes = []

        # Flask/FastAPI decorators
        route_pattern = re.compile(
            r'@app\.(get|post|put|delete|patch|route)\(\s*[\'"]([^\'"]+)[\'"]'
        )

        # Function name
        function_pattern = re.compile(
            r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        )

        for file in self.source_files:

            if file.suffix != ".py":
                continue

            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            i = 0

            while i < len(lines):

                line = lines[i]

                match = route_pattern.search(line)

                if not match:
                    i += 1
                    continue

                method = match.group(1).upper()
                path = match.group(2)

                authentication = False

                j = i + 1

                # Read decorators until function
                while j < len(lines):

                    current = lines[j].strip()

                    if current.startswith("@login_required"):
                        authentication = True

                    func = function_pattern.search(current)

                    if func:

                        handler = func.group(1)

                        routes.append({
                            "path": path,
                            "method": method,
                            "handler": handler,
                            "file": file.name,
                            "authentication": authentication
                        })

                        break

                    j += 1

                i = j + 1

        return routes