# combines the role of env and elementaltables

import os

class Env(object) :
    def __init__(self, envName) :
        self.envName = envName

    home = os.getcwd()
    baseRoot = f"{home}/spark-storage"
    def tempRoot(self) : return  f"{self.baseRoot}/temp/{self.envName}"
    def hdfsTempPath(self) : return f"file:{self.tempRoot()}"

    def hdfsRoot(self) : return f"{self.baseRoot}/{self.envName}"
    def hdfsPath(self) : return f"file:{self.hdfsRoot()}"

    def projectDir(self) : return "%s/code" % (self.home)
    def projectData(self) : return "%s/data/%s" % (self.home, self.envName)
    def projectTempData(self) : return "%s/temp" % self.projectData()
    


