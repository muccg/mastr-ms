#!/bin/bash
#
# Script to control Mastrms in dev and test
#

# break on error
set -e 

ACTION="$1"

PORT='8000'

PROJECT_NAME='mastrms'
AWS_BUILD_INSTANCE='rpmbuild-centos6-aws'
TARGET_DIR="/usr/local/src/${PROJECT_NAME}"
CLOSURE="/usr/local/closure/compiler.jar"
MODULES="MySQL-python==1.2.3 psycopg2==2.4.6 Werkzeug flake8"
PIP_OPTS="-v -M --download-cache ~/.pip/cache"


function usage() {
    echo ""
    echo "Usage ./develop.sh (test|lint|jslint|dropdb|start|install|clean|purge|pipfreeze|pythonversion|ci_remote_build|ci_rpm_publish|ci_remote_destroy)"
    echo ""
}


function settings() {
    export DJANGO_SETTINGS_MODULE="${PROJECT_NAME}.settings"
}


# ssh setup, make sure our ccg commands can run in an automated environment
function ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging.pem
}


# build RPMs on a remote host from ci environment
function ci_remote_build() {
    time ccg ${AWS_BUILD_INSTANCE} boot
    time ccg ${AWS_BUILD_INSTANCE} puppet
    time ccg ${AWS_BUILD_INSTANCE} shutdown:50

    EXCLUDES="('bootstrap'\, '.hg*'\, 'virt*'\, '*.log'\, '*.rpm')"
    SSH_OPTS="-o StrictHostKeyChecking\=no"
    RSYNC_OPTS="-l"
    time ccg ${AWS_BUILD_INSTANCE} rsync_project:local_dir=./,remote_dir=${TARGET_DIR}/,ssh_opts="${SSH_OPTS}",extra_opts="${RSYNC_OPTS}",exclude="${EXCLUDES}",delete=True
    time ccg ${AWS_BUILD_INSTANCE} build_rpm:centos/${PROJECT_NAME}.spec,src=${TARGET_DIR}

    mkdir -p build
    ccg ${AWS_BUILD_INSTANCE} getfile:rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,build/
}


# publish rpms 
function ci_rpm_publish() {
    time ccg ${AWS_BUILD_INSTANCE} publish_rpm:build/${PROJECT_NAME}*.rpm,release=6
}


# destroy our ci build server
function ci_remote_destroy() {
    ccg ${AWS_BUILD_INSTANCE} destroy
}


# lint using flake8
function lint() {
    source virt_${PROJECT_NAME}/bin/activate
    flake8 ${PROJECT_NAME} --ignore=E501 --count
}


# lint js, assumes closure compiler
function jslint() {
    JSFILES="mastrms/mastrms/app/static/js/*.js mastrms/mastrms/app/static/js/repo/*.js"
    for JS in $JSFILES
    do
        java -jar ${CLOSURE} --js $JS --js_output_file output.js --warning_level DEFAULT --summary_detail_level 3
    done
}


# run the tests using django-admin.py
function djangotests() {
    source virt_${PROJECT_NAME}/bin/activate
    virt_${PROJECT_NAME}/bin/django-admin.py test ${PROJECT_NAME} --noinput
}


function nosetests() {
    source virt_${PROJECT_NAME}/bin/activate
    virt_${PROJECT_NAME}/bin/nosetests --with-xunit --xunit-file=tests.xml -v -w tests
}


function nose_collect() {
    source virt_${PROJECT_NAME}/bin/activate
    virt_${PROJECT_NAME}/bin/nosetests -v -w tests --collect-only
}


function dropdb() {
    echo "todo"
}


function installapp() {
    # check requirements
    which virtualenv >/dev/null

    echo "Install ${PROJECT_NAME}"
    virtualenv --system-site-packages virt_${PROJECT_NAME}
    pushd ${PROJECT_NAME}
    ../virt_${PROJECT_NAME}/bin/pip install ${PIP_OPTS} -e .
    popd
    virt_${PROJECT_NAME}/bin/pip install ${PIP_OPTS} ${MODULES}
}


# django syncdb, migrate and collect static
function syncmigrate() {
    echo "syncdb"
    virt_${PROJECT_NAME}/bin/django-admin.py syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> syncdb-develop.log
    echo "migrate"
    virt_${PROJECT_NAME}/bin/django-admin.py migrate --settings=${DJANGO_SETTINGS_MODULE} 1> migrate-develop.log
    echo "collectstatic"
    virt_${PROJECT_NAME}/bin/django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> collectstatic-develop.log
}


# start runserver
function startserver() {
    virt_${PROJECT_NAME}/bin/django-admin.py runserver_plus ${port}
}


function pythonversion() {
    virt_${PROJECT_NAME}/bin/python -V
}


function pipfreeze() {
    echo "${PROJECT_NAME} pip freeze"
    virt_${PROJECT_NAME}/bin/pip freeze
    echo '' 
}


function clean() {
    find ${PROJECT_NAME} -name "*.pyc" -exec rm -rf {} \;
}


function purge() {
    rm -rf virt_${PROJECT_NAME}
    rm *.log
}


function runtest() {
    #nosetests
    djangotests
}



case ${ACTION} in
pythonversion)
    pythonversion
    ;;
pipfreeze)
    pipfreeze
    ;;
test)
    settings
    runtest
    ;;
lint)
    lint
    ;;
jslint)
    jslint
    ;;
syncmigrate)
    settings
    syncmigrate
    ;;
start)
    settings
    startserver
    ;;
install)
    settings
    installapp
    ;;
ci_remote_build)
    ci_ssh_agent
    ci_remote_build
    ;;
ci_remote_destroy)
    ci_ssh_agent
    ci_remote_destroy
    ;;
ci_rpm_publish)
    ci_ssh_agent
    ci_rpm_publish
    ;;
dropdb)
    dropdb
    ;;
clean)
    settings
    clean
    ;;
purge)
    settings
    clean
    purge
    ;;
*)
    usage
esac
