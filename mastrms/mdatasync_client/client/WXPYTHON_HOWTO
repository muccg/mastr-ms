This is a guide on how to build the wxPython egg for this project. 


To build a wxPython egg is a pain in the rear. wxPython doesn't seem to adhere to the normal methods of module building - running 
setup.py with the appropriate (default) args should do the trick - but it doesn't. So I built an egg by hand: here's how.

On ubuntu 10.10, (and likely others) you will need to apt-get the following packages.

libgstreamer0.10-dev
libgstreamermm-0.10-2
libgstreamermm-0.10-dev
libgconf2-dev
libx11-dev
libxtst-dev

Now you are ready to even think about building.

First I got into the target virtual environment for the project I was adding this too (mastr) - so I had activated virt_madas.

Download the tarball, unpack (somewhere)
cd wxPython-src-2.9.1.1/wxPython
python build-wxpython.py --build_dir=../bld

This will use the python from the virtual environment you are in to do the building, which is what we want.

When it was done it said:
- Set your PYTHONPATH variable to /home/bpower/Downloads/wxPython-src-2.9.1.1/wxPython.
- Set your (DY)LD_LIBRARY_PATH to /home/bpower/Downloads/wxPython-src-2.9.1.1/bld/lib
- Run python demo/demo.py

so then I did
python setup.py WX_CONFIG="../bld/wx-config" build_ext
and then
python setup.py WX_CONFIG="../bld/wx-config" bdist_egg

The egg it builds (in the dist dir) won't have the compiled gtk libs inside it - I guess you are expected to install those on your system. We don't want to do that - I want to open up the egg and push the libs inside it, and then add an LD_LIBRARY_PATH export to the virtual env that will be able to find those libs at runtime.

I opened up that egg with unzip, and copied all the libraries from ../bld/lib (you don't need the wx dir, just everything starting with lib* in the ../bld/lib dir). Just into the root of the 'egg'.
Then I zipped it all back up again, and that was the egg I put into my config dir.

THEN, in the ENVIRONMENT file in that dir, I made sure I set an LD_LIBRARY_PATH that would resolve the lib deps.
Like this: 
echo "export LD_LIBRARY_PATH=$PWD/$VPYTHON_DIR/lib/python2.6/site-packages/wxPython-2.9.1.1-py2.6-linux-x86_64.egg" >> $VPYTHON_DIR/bin/activate

Now, when you bootstrap, you get all this goodness. wxPython works. No libraries have been 'installed' on your system.

