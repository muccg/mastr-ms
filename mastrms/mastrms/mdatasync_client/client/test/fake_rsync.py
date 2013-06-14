#!/usr/bin/env python

import os
import os.path
import sys
import tempfile
import pipes
import signal
import cPickle as pickle
import argparse
import shutil

__all__ = ["FakeRsync"]

class FakeRsync(object):
    """
    FakeRsync is a context manager which puts a stub rsync command in
    the PATH and captures the arguments which were supplied to it.
    """
    OPTS_FILE_ENV = "FAKE_RSYNC_OPTS_FILE"
    CAPTURE_FILE_ENV = "FAKE_RSYNC_CAPTURE_FILE"
    MY_PATH = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, results=None, retcode=0, stdoutdata=None, do_copy=False,
                 exit_callback=None):
        self.capture_file = tempfile.NamedTemporaryFile()
        self.opts_file = tempfile.NamedTemporaryFile()
        self.opts = { "retcode": retcode,
                      "stdoutdata": stdoutdata,
                      "do_copy": do_copy }
        if results is None:
            self.results = []
        else:
            self.results = results
        self.exit_callback = exit_callback

    def __enter__(self):
        self.initial_path = os.environ["PATH"]
        os.environ["PATH"] = "%s:%s" % (self.MY_PATH, self.initial_path)
        os.environ[self.OPTS_FILE_ENV] = self.opts_file.name
        os.environ[self.CAPTURE_FILE_ENV] = self.capture_file.name
        pickle.dump(self.opts, self.opts_file)
        self.opts_file.flush()
        self.sig_child_old = signal.signal(signal.SIGCHLD, self.sig_child)

    def sig_child(self, signal, frame):
        # read the capture file when the fake rsync subprocess exits
        result = self.collect_data()
        self.call_exit_callback(result)

    def __exit__(self, type, value, traceback):
        os.environ["PATH"] = self.initial_path
        del os.environ[self.OPTS_FILE_ENV]
        del os.environ[self.CAPTURE_FILE_ENV]
        signal.signal(signal.SIGCHLD, self.sig_child_old)

    def collect_data(self):
        self.capture_file.seek(0)
        data = self.capture_file.read()
        if data:
            self.results.append(pickle.loads(data))
            return self.results[-1]
        return None

    def call_exit_callback(self, result):
        if self.exit_callback:
            self.exit_callback(result)

def fake_rsync_capture(opts_filename, capture_filename):
    opts = pickle.load(open(opts_filename))
    result = command_line_args_info(sys.argv)
    if opts["do_copy"]:
        fake_rsync_copy(result)
    pickle.dump(result, open(capture_filename, "w"))
    if opts["stdoutdata"] is not None:
        sys.stdout.write(opts["stdoutdata"])
    return opts["retcode"]

def parse_fake_rsync_args(argv):
    """
    Looks at the files passed on the rsync command line and stores
    them for use by test assert statements.
    """
    parser = argparse.ArgumentParser(prog='rsync')
    parser.add_argument("src", nargs="+")
    parser.add_argument("dst")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-z", action="store_true")
    parser.add_argument("--itemize-changes", action="store_true")
    parser.add_argument("--from0", action="store_true")
    parser.add_argument("--include-from")
    parser.add_argument("--log-file")
    return parser.parse_args(argv[1:])

def command_line_args_info(argv):
    args = parse_fake_rsync_args(argv)

    def source_files(srcdirs):
        for srcdir in srcdirs:
            for root, dirs, files in os.walk(srcdir):
                for filename in files:
                    yield (srcdir, os.path.join(os.path.relpath(root, srcdir), filename))

    def get_include_files(include_file, from0):
        splitchar = "\0" if from0 else "\n"
        if include_file:
            return open(include_file).read().split(splitchar)
        return None

    return {
        "argv": argv,
        "args": vars(args),
        "source_files": sorted(source_files(args.src)),
        "include_files": get_include_files(args.include_from, args.from0),
        }

def fake_rsync_copy(info):
    "This actually copies files... am I implementing too much rsync yet?"
    destdir = info["args"]["dst"].split(":")[1]
    logfilename = info["args"].get("log_file", None)
    dirnames_written = set()
    with open(logfilename if logfilename else "/dev/null", "w") as logfile:
        # [11:45:50] DEBUG: rsync output is:
        # .d          ./
        # .d          runs/
        # .d          runs/2013/
        # .d          runs/2013/5/
        # .d          runs/2013/5/3/
        # cd+++++++++ runs/2013/5/3/pbqc_3-15.d/
        # <f+++++++++ runs/2013/5/3/pbqc_3-15.d/0
        # <f+++++++++ runs/2013/5/3/pbqc_3-15.d/1
        # <f+++++++++ runs/2013/5/3/pbqc_3-15.d/2
        # <f+++++++++ runs/2013/5/3/pbqc_3-15.d/3
        # <f+++++++++ runs/2013/5/3/pbqc_3-15.d/4

        logfile.write("Fake rsync\n")
        #sys.stdout.write(".d          ./\n")
        for (dirname, filename) in info["source_files"]:
            src = os.path.join(dirname, filename)
            dst = os.path.join(destdir, filename)

            logfile.write("Copying %s -> %s\n" % (src, dst))

            changed = not os.path.exists(dst) or open(src).read() != open(dst).read()

            if dirname not in dirnames_written:
                sys.stdout.write("cd          %s\n" % dirname)
                dirnames_written.add(dirname)
            if changed:
                sys.stdout.write("<f+++++++++ %s\n" % filename)
            else:
                sys.stdout.write(".f          %s\n" % filename)

            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            shutil.copyfile(src, dst)
        logfile.write("Finished\n")

def main():
    capture_filename = os.environ.get(FakeRsync.CAPTURE_FILE_ENV, None)
    opts_filename = os.environ.get(FakeRsync.OPTS_FILE_ENV, None)

    if opts_filename and capture_filename:
        return fake_rsync_capture(opts_filename, capture_filename)
    else:
        print "fake rsync is meant to be run through the FakeRsync context manager."
        return 1

if __name__ == "__main__":
    sys.exit(main())
