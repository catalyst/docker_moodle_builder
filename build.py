import os
import shutil
import git

def buildBranch(distro, db, webServer):
    branchName = "{0}-{1}-{2}".format(distro, db, webServer)
    print("Building {0}".format(branchName))

    # Create new branch folder
    dirName = os.path.dirname(__file__)
    branchFolder = os.path.join(dirName, "build/{0}".format(branchName))

    if os.path.isdir(branchFolder):
        shutil.rmtree(branchFolder)
    os.mkdir(branchFolder)

    #figure out asset path
    assetPath = os.path.join(dirName, "assets")

    # Copy in static README
    readmePath = os.path.join(assetPath, "static/README.md")
    shutil.copyfile(readmePath, os.path.join(branchFolder, "README.md"))


ubuntuDistros = ['1404', '1604', '1804']
databases = ['mysql', 'psql']
webServers = ['nginx', 'apache']

for distro in ubuntuDistros:
    for db in databases:
        for webServer in webServers:
            buildBranch(distro, db, webServer)
