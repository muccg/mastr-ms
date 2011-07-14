#!/bin/bash

#
# Its a sample script, tested only to the point of running manage.py runserver_plus
#
# You need to have:
#   python header files 
#   postgres headers
#   ldap header
#   sasl header files

EGGS_DIR='eggs/'
EGGS_PATTERN='*.*' #this ignores dirs, but means egg names must contain a .
PIP_DOWNLOAD_CACHE='/tmp/'
export PIP_DOWNLOAD_CACHE

CONFIG_DIR=''
if [ $# -eq 1 ]
then
    CONFIG_DIR=$1
fi
EGGS_PATH="$EGGS_DIR$CONFIG_DIR/$EGGS_PATTERN"
if [ ! -d $EGGS_DIR$CONFIG_DIR ]
then
    echo "No such configuration path exists: $EGGS_PATH"
    echo "Perhaps try one of these:"
    cd $EGGS_DIR
    for arg in *
    do
        if [ -d $arg ]
        then
            echo "$arg"
        fi
    done
    cd ..
    exit
fi

echo "---+++---"
echo "Building for eggs in $EGGS_PATH"
if [ -f $EGGS_DIR$CONFIG_DIR/DEPENDENCIES ]
then
    cat $EGGS_DIR$CONFIG_DIR/DEPENDENCIES
fi    
echo "---+++---"

BASE_DIR=`basename ${PWD}`
PRE="virt_"
VPYTHON_DIR="$PRE$BASE_DIR"
VIRTUALENV='virtualenv-1.6.1'
VIRTUALENV_TARBALL='virtualenv-1.6.1.tar.gz'

# only install if we dont already exist
if [ ! -d $VPYTHON_DIR ]
then
    echo -e '\n\nNo virtual python dir, lets create one\n\n'

    # only install virtual env if its not hanging around
    if [ ! -d $VIRTUALENV ]
    then
        echo -e '\n\nNo virtual env, creating\n\n'
  
        # only download the tarball if needed
        if [ ! -f $VIRTUALENV_TARBALL ]
        then
            wget http://pypi.python.org/packages/source/v/virtualenv/$VIRTUALENV_TARBALL
        fi

        # build virtualenv
        tar zxvf $VIRTUALENV_TARBALL
        cd $VIRTUALENV
        python setup.py build
        cd ..

    fi
       
    # create a virtual python in the current directory
    python $VIRTUALENV/build/lib*/virtualenv.py --no-site-packages $VPYTHON_DIR

    # we use fab for deployments
    ./$VPYTHON_DIR/bin/pip install fabric

    # install Mercurial
    #./$VPYTHON_DIR/bin/easy_install mercurial

    # install all the eggs in this app
    ./$VPYTHON_DIR/bin/easy_install $EGGS_PATH --allow-hosts=None

    # now we are going to eggify app settings, so we can run it locally
    # we need to jump through a few legacy hoops to make this happen

    if [ -d tmp ]
        mkdir tmp
    then
        rm -Rf tmp
    fi
    cd tmp
    rm -rf ccgapps-settings 
    svn export svn+ssh://ccg.murdoch.edu.au/store/techsvn/ccg/ccgapps-settings
    # the directory has the wrong name, so create a sym link with the name we need
    ln -s ccgapps-settings appsettings
    # the setup.py is at the wrong level
    mv appsettings/setup.py .
    ../$VPYTHON_DIR/bin/python setup.py bdist_egg
    ../$VPYTHON_DIR/bin/easy_install dist/*.egg
    rm -rf appsettings ccgapps-settings 
    cd ..

    # hack activate to set some environment we need
    echo "PROJECT_DIRECTORY=`pwd`;" >>  $VPYTHON_DIR/bin/activate
    echo "export PROJECT_DIRECTORY " >>  $VPYTHON_DIR/bin/activate

fi

echo -e "\n\n What just happened?\n\n"
echo " * Python has been installed into $VPYTHON_DIR"
echo " * eggs from the eggs in this project ($EGGS_PATH) have been installed"
echo " * fabric is also installed"
echo " * and ccgapps-settings"


# tell the (l)user how to activate this python install
echo -e "\n\nTo activate this python install, type the following at the prompt:\n\nsource $VPYTHON_DIR/bin/activate\n"
echo -e "To exit your virtual python, simply type 'deactivate' at the shell prompt\n\n"
