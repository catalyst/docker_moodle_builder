# docker_moodle_builder

Python script that build various branches for https://github.com/catalyst/docker_moodle

## Budget update process - to be automated

    git config --global core.editor vim
    git config --global user.name "xxxxxxxxxx"
    git config --global user.email "xxxxxxxxx"

    cd 1804-psql
    git init
    git add .
    git checkout -b 1804-psql
    git commit -m "Build"
    git remote add origin git@github.com:catalyst/docker_moodle.git
    git push -u origin 1804-psql -f
