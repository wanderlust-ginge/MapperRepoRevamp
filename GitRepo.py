class GitRepo:
    def __init__(self, project, host="git@github.com", organization="Starcounter"):
        self.host = host
        self.organization = organization
        self.project = project

    def __init__(self, host="git@github.com", organization="Starcounter"):
        self.host = host
        self.organization = organization
        self.project = ""

    def SetProject(self, project):
        self.project = project

    def GitPath(self):
        return self.host + ":" + self.organization + "/" + self.project