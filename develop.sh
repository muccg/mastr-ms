#!/bin/sh
#
# Script to control Mastrms in dev and test
#

TOPDIR=$(cd `dirname $0`; pwd)

# break on error
set -e

ACTION=$1

PORT='8000'

PROJECT_NAME='mastrms'
VIRTUALENV="${TOPDIR}/virt_${PROJECT_NAME}"
AWS_DOCKER_INSTANCE='ccg_syd_nginx_staging'
AWS_RPM_INSTANCE='aws_syd_mastrms_staging'

# A lot of tests need a database and/or X display to run. So the full
# test suite TEST_LIST and the tests which don't need a database or X
# are in NOSE_TEST_LIST, because they can be run outside the django
# test runner.
TEST_LIST="mastrms.repository.tests mastrms.mdatasync_server.test"
NOSE_TEST_LIST="mdatasync_client.test.tests:DataSyncServerTests mdatasync_client.test.tests:MSDataSyncAPITests mdatasync_client.test.tests:MSDSImplTests"


usage() {
    echo ""
    echo "Usage ./develop.sh (start|runtests|lettuce|selenium)"
    echo "Usage ./develop.sh (pythonlint|jslint)"
    echo "Usage ./develop.sh (ci_docker_staging|docker_staging_selenium|ci_rpm_staging|docker_rpm_staging_selenium)"
    echo "Usage ./develop.sh (dockerbuild_unstable)"
    echo "Usage ./develop.sh (rpmbuild|rpm_publish)"
    echo ""
}


# ssh setup, make sure our ccg commands can run in an automated environment
ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    . /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging-2014.pem
}


activate_virtualenv() {
    . ${VIRTUALENV}/bin/activate
}


settings() {
    export DJANGO_SETTINGS_MODULE="${PROJECT_NAME}.settings"
}


make_virtualenv() {
    # check requirements
    which virtualenv > /dev/null
    if [ ! -e ${VIRTUALENV} ]; then
        virtualenv ${VIRTUALENV}
    fi

    activate_virtualenv

    pip install docker-compose
    pip install 'flake8>=2.0,<2.1'
    pip install 'closure-linter==2.3.13'
}


# build RPMs
rpmbuild() {
    mkdir -p data/rpmbuild
    chmod o+rwx data/rpmbuild

    make_virtualenv

    docker-compose --project-name mastr-ms -f docker-compose-rpmbuild.yml up
}


# publish rpms to testing repo
rpm_publish() {
    time ccg publish_testing_rpm:data/rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,release=6
}


# copy a version from testing repo to release repo
rpm_release() {
    if [ -z "$1" ]; then
        echo "rpm_release requires an rpm filename argument"
        usage
        exit 1
    fi

    time ccg release_rpm:$1,release=6
}


# puppet up staging which will install the latest rpm
ci_rpm_staging() {
    ccg ${AWS_RPM_INSTANCE} boot
    ccg ${AWS_RPM_INSTANCE} puppet
    ccg ${AWS_RPM_INSTANCE} shutdown:120
}


# lint using flake8
pythonlint() {
    make_virtualenv
    flake8 ${PROJECT_NAME} --ignore=E501 --count
}


jslint() {
    make_virtualenv
    JSFILES="mastrms/mastrms/app/static/js/*.js mastrms/mastrms/app/static/js/repo/*.js"
    OPTS="--exclude_files=mastrms/mastrms/app/static/js/swfobject.js,mastrms/mastrms/app/static/js/repo/prototype.js"
    DISABLE="--disable 0131,0200,0210,0217,0220,0110,120"
    for JS in $JSFILES
    do
        gjslint ${OPTS} ${DISABLE} $JS
    done
}


start() {
    mkdir -p data/dev
    chmod o+rwx data/dev

    make_virtualenv

    docker-compose --project-name mastr-ms -f docker-compose.yml up
}

runtests() {
    mkdir -p data/tests
    chmod o+rwx data/tests

    make_virtualenv

    # clean up containers from past runs
    ( docker-compose --project-name ${PROJECT_NAME} -f docker-compose-test.yml rm --force || exit 0 )
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-test.yml build # --no-cache
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-test.yml up
}


lettuce() {
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    make_virtualenv
 
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-lettuce.yml rm --force
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-lettuce.yml build
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-lettuce.yml up
}


selenium() {
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    make_virtualenv
 
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-selenium.yml rm --force
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-selenium.yml build
    docker-compose --project-name ${PROJECT_NAME} -f docker-compose-selenium.yml up
}


clean() {
    find ${PROJECT_NAME} -name "*.pyc" -exec rm -rf {} \;
}


purge() {
    rm -rf ${VIRTUALENV}
    rm *.log
}


case ${ACTION} in
runtests)
    runtests
    ;;
lettuce)
    lettuce
    ;;
selenium)
    selenium
    ;;
pythonlint)
    pythonlint
    ;;
jslint)
    jslint
    ;;
start)
    start
    ;;
rpmbuild)
    rpmbuild
    ;;
rpm_publish)
    ci_ssh_agent
    rpm_publish
    ;;
ci_rpm_staging)
    ci_ssh_agent
    ci_rpm_staging
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
