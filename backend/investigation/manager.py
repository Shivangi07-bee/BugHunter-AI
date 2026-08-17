class WorkspaceManager:

    def __init__(self):

        self.sessions = {}

    def create(self, workspace):

        self.sessions[workspace.id] = workspace

        return workspace.id

    def get(self, workspace_id):

        return self.sessions.get(workspace_id)

    def delete(self, workspace_id):

        self.sessions.pop(workspace_id, None)

    def all(self):

        return list(self.sessions.values())