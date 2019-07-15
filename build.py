import os
import shutil
import git
import jinja2

def createBranchFolder(branchPath):
    if os.path.isdir(branchPath):
        shutil.rmtree(branchPath)
    os.mkdir(branchPath)

    dockerPath = os.path.join(branchPath, "docker")
    os.mkdir(dockerPath)

    dockerMoodlePath = os.path.join(dockerPath, "moodle")
    os.mkdir(dockerMoodlePath)

def addStaticFile(assetPath, branchPath, fileName, outputName=None):
    if outputName is None:
        outputName = fileName

    filePath = os.path.join(assetPath, fileName)
    shutil.copyfile(filePath, os.path.join(branchPath, outputName))


def addTemplatedFile(assetPath, branchPath, templateName, templateData):
    templateLoader = jinja2.FileSystemLoader(searchpath=assetPath)
    templateEnv = jinja2.Environment(loader=templateLoader, trim_blocks=True, lstrip_blocks=True)
    template = templateEnv.get_template("{0}.j2".format(templateName))
    outputPath = os.path.join(branchPath, templateName)

    with open(outputPath, 'w') as f:
            f.write(template.render(templateData))


def buildBranch(ubuntuVersion, db):
    branchName = "{0}-{1}".format(ubuntuVersion['name'], db['name'])
    print("Building {0}".format(branchName))

    dirName = os.path.dirname(__file__)
    branchPath = os.path.join(dirName, "build/{0}".format(branchName))
    dockerMoodlePath = os.path.join(branchPath, "docker/moodle")

    createBranchFolder(branchPath)

    assetPath = os.path.join(dirName, 'assets')

    addStaticFile(assetPath, branchPath, 'README.md')
    addStaticFile(assetPath, branchPath, 'control')
    os.chmod(os.path.join(branchPath, 'control'), 0o775)

    addStaticFile(assetPath, branchPath, 'gitignore', '.gitignore')
    addStaticFile(assetPath, dockerMoodlePath, 'nginx.conf')
    addStaticFile(assetPath, dockerMoodlePath, 'xdebug.ini')

    packages = ['curl', 'locales', 'nginx', 'vim']
    packages += ubuntuVersion['packages']
    packages += db['packages'][ubuntuVersion['name']]
    packages.sort()

    addTemplatedFile(
        assetPath,
        dockerMoodlePath,
        'Dockerfile',
        {
            'imageTag': ubuntuVersion['imageTag'],
            'packages': packages,
            'xdebugPath': ubuntuVersion['xdebugPath'],
        }
    )

    addTemplatedFile(
        assetPath,
        dockerMoodlePath,
        'entrypoint.sh',
        {
            'fpmService': ubuntuVersion['fpmService'],
        }
    )

    addTemplatedFile(
        assetPath,
        dockerMoodlePath,
        'nginx-site',
        {
            'fpmSock': ubuntuVersion['fpmSock'],
        }
    )

    addTemplatedFile(
        assetPath,
        branchPath,
        'docker-compose.yml',
        {
            'db': db['name']
        }
    )


ubuntuVersions = [
    {
        'name':         '1404',
        'imageTag':     '14.04',
        'fpmService':   'php5-fpm',
        'fpmSock':      '/var/run/php5-fpm.sock',
        'xdebugPath':   '/etc/php5/mods-available/xdebug.ini',
        'packages':     [
            'php5',
            'php5-cli',
            'php5-curl',
            'php5-fpm',
            'php5-gd',
            'php5-intl',
            'php5-ldap',
            'php5-xdebug',
            'php5-xmlrpc',
            'php-soap',
        ],
    },

    {
        'name':         '1604',
        'imageTag':     '16.04',
        'fpmService':   'php7.0-fpm',
        'fpmSock':      '/var/run/php/php7.0-fpm.sock',
        'xdebugPath':   '/etc/php/7.0/mods-available/xdebug.ini',
        'packages':     [
            'php',
            'php-cli',
            'php-curl',
            'php-fpm',
            'php-gd',
            'php-intl',
            'php-ldap',
            'php-mbstring',
            'php-mysql',
            'php-soap',
            'php-xdebug',
            'php-xmlrpc',
            'php-xml',
            'php-zip',
        ],
    },

    {
        'name':         '1804',
        'imageTag':     '18.04',
        'fpmService':   'php7.2-fpm',
        'fpmSock':      '/var/run/php/php7.2-fpm.sock',
        'xdebugPath':   '/etc/php/7.2/mods-available/xdebug.ini',
        'packages': [
            'php',
            'php-cli',
            'php-curl',
            'php-fpm',
            'php-gd',
            'php-intl',
            'php-ldap',
            'php-mbstring',
            'php-mysql',
            'php-soap',
            'php-xdebug',
            'php-xmlrpc',
            'php-xml',
            'php-zip',
        ],
    },
]

databases = [
    {
        'name': 'mysql',
        'packages': {
            '1404': ['php5-mysql'],
            '1604': ['php-mysql'],
            '1804': ['php-mysql'],
        },
    },
    {
        'name': 'psql',
        'packages': {
            '1404': ['php5-pgsql'],
            '1604': ['php-pgsql'],
            '1804': ['php-pgsql'],
        },
    },
]

for ubuntuVersion in ubuntuVersions:
    for db in databases:
        buildBranch(ubuntuVersion, db)
