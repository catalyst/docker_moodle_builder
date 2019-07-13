import os
from shutil import copyfile, rmtree

def buildBranch(distro, db):
    branchName = "{0}-{1}".format(distro, db)
    print("Building {0}".format(branchName))

    # Create new branch folder
    dirName = os.path.dirname(__file__)
    branchFolder = os.path.join(dirName, "build/{0}".format(branchName))

    if os.path.isdir(branchFolder):
        rmtree(branchFolder)
    os.mkdir(branchFolder)

    #figure out asset path
    assetPath = os.path.join(dirName, "assets")

    # Copy in static README
    readmePath = os.path.join(assetPath, "static/README.md")
    copyfile(readmePath, os.path.join(branchFolder, "README.md"))


ubuntuDistributions = ['1404', '1604', '1804']
databases = ['mysql', 'psql']

for distro in ubuntuDistributions:
    for db in databases:
        buildBranch(distro, db)
