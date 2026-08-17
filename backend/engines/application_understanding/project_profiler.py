from pathlib import Path


class ProjectProfiler:

    def __init__(self, source_files, root_files):
        self.source_files = source_files
        self.root_files = root_files

    def build_profile(self):

        profile = {
            "project_name": "",
            "language": "Unknown",
            "framework": "Unknown",
            "entry_point": "Unknown",
            "requirements": False,
            "package_json": False,
            "docker": False,
            "source_files": len(self.source_files)
        }

        if self.source_files:
            profile["project_name"] = self.source_files[0].parent.name

        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".go": "Go",
            ".cs": "C#"
        }

        counts = {}

        for file in self.source_files:
            ext = file.suffix
            counts[ext] = counts.get(ext, 0) + 1

        if counts:
            dominant = max(counts, key=counts.get)
            profile["language"] = extensions.get(dominant, "Unknown")

        possible_entry = {
            "app.py",
            "main.py",
            "server.js",
            "index.js"
        }

        for file in self.source_files:
            if file.name in possible_entry:
                profile["entry_point"] = file.name
                break

        profile["requirements"] = (
            "requirements.txt" in self.root_files
        )

        profile["package_json"] = (
            "package.json" in self.root_files
        )

        profile["docker"] = (
            "Dockerfile" in self.root_files
        )

        return profile