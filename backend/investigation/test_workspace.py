from workspace import Workspace


def test_workspace():

    ws = Workspace()

    ws.repository({"project": "Shopping App"})
    ws.routes([{"path": "/login"}])

    result = ws.build()

    assert result.repository["project"] == "Shopping App"

    assert len(result.routes) == 1