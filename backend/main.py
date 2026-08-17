from engines.application_understanding.repository_loader import RepositoryLoader
from engines.application_understanding.project_profiler import ProjectProfiler
from engines.application_understanding.route_discovery import RouteDiscovery
from engines.application_understanding.endpoint_analyzer import EndpointAnalyzer


def main():

    loader = RepositoryLoader("../sample_projects/shopping_app")

    files = loader.load_repository()

    root_files = loader.get_root_files()

    profiler = ProjectProfiler(files, root_files)

    profile = profiler.build_profile()

    print("\n========== PROJECT PROFILE ==========\n")

    for key, value in profile.items():
        print(f"{key:20}: {value}")

    # OUTSIDE the for loop
    route_engine = RouteDiscovery(files)

    routes = route_engine.discover_routes()

    print("\nRoutes Found\n")

    for route in routes:
        print(route)

    analysis = EndpointAnalyzer(
        files,
        routes
    ).analyze()

    print("\nEndpoint Analysis\n")

    for endpoint in analysis:

        print(endpoint)


if __name__ == "__main__":
    main()