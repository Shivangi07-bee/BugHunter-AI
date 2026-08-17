from engines.workflow_engine.relationship_builder import RelationshipBuilder

endpoint_metadata = [

    {
        "path": "/login",
        "method": "POST",
        "handler": "login",
        "models": ["User"],
        "calls": [
            "authenticate",
            "generate_token"
        ]
    },

    {
        "path": "/profile",
        "method": "GET",
        "handler": "profile",
        "models": ["User"],
        "calls": [
            "verify_token",
            "get_user"
        ]
    },

    {
        "path": "/logout",
        "method": "POST",
        "handler": "logout",
        "models": ["Session"],
        "calls": [
            "delete_session"
        ]
    }

]

builder = RelationshipBuilder(endpoint_metadata)

edges = builder.build_relationships()

for edge in edges:
    print(edge)