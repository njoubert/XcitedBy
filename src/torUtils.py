import os
import os.path

import torConstants

def torStart(xcitedbyUser, numTorInstances):

    torExecutableAbsolutePath = "/Users/" + xcitedbyUser + "/.xcitedby/TorBrowser_en-US.app/Contents/MacOS/tor"
    torTmpAbsolutePath        = "/Users/" + xcitedbyUser + "/.xcitedby/tmp/tor/"
    torDataAbsoluteBasePath   = torTmpAbsolutePath + "data/"
    torPidAbsolutePath        = torTmpAbsolutePath + "pid/"

    for i in range(numTorInstances):
        torDataAbsolutePath = torDataAbsoluteBasePath + "tor%02d/" % i
        if not os.path.exists(torDataAbsolutePath):
            print "[TORUTILS MKDIR] " + torDataAbsolutePath
            os.makedirs(torDataAbsolutePath)

    if not os.path.exists(torPidAbsolutePath):
        print "[TORUTILS MKDIR] " + torPidAbsolutePath
        os.makedirs(torPidAbsolutePath)

    for i in range(numTorInstances):
        controlPort            = torConstants.TOR_BASE_CONTROL_PORT + i
        socksPort              = torConstants.TOR_BASE_SOCKS_PORT   + i
        torPidFileAbsolutePath = torPidAbsolutePath       + "tor%02d.pid" % i
        torDataAbsolutePath    = torDataAbsoluteBasePath + "tor%02d/"    % i

        command = \
            "%s --RunAsDaemon 1 --ControlPort %d --SocksPort %d --PidFile %s --DataDirectory %s" % \
            (torExecutableAbsolutePath, controlPort, socksPort, torPidFileAbsolutePath, torDataAbsolutePath)

        print "[TORUTILS COMMAND] " + command
        os.system(command)

def torStop():

    command = "killall tor"
    print "[TORUTILS COMMAND] " + command
    os.system(command)
