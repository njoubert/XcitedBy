import os
import os.path

import torConstants

def torStart():

    for i in range(torConstants.NUM_TOR_INSTANCES):
        torDataAbsolutePath = torConstants.TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/" % i
        if not os.path.exists(torDataAbsolutePath):
            print "[TORUTILS MKDIR] " + torDataAbsolutePath
            os.makedirs(torDataAbsolutePath)

    if not os.path.exists(torConstants.TOR_PID_ABSOLUTE_PATH):
        print "[TORUTILS MKDIR] " + torConstants.TOR_PID_ABSOLUTE_PATH
        os.makedirs(torConstants.TOR_PID_ABSOLUTE_PATH)

    for i in range(torConstants.NUM_TOR_INSTANCES):
        controlPort            = torConstants.TOR_BASE_CONTROL_PORT + i
        socksPort              = torConstants.TOR_BASE_SOCKS_PORT   + i
        torPidFileAbsolutePath = torConstants.TOR_PID_ABSOLUTE_PATH       + "tor%02d.pid" % i
        torDataAbsolutePath    = torConstants.TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/"    % i

        command = \
            "%s --RunAsDaemon 1 --ControlPort %d --SocksPort %d --PidFile %s --DataDirectory %s" % \
            (torConstants.TOR_EXECUTABLE_ABSOLUTE_PATH, controlPort, socksPort, torPidFileAbsolutePath, torDataAbsolutePath)

        print "[TORUTILS COMMAND] " + command
        os.system(command)

def torStop():

    command = "killall tor"
    print "[TORUTILS COMMAND] " + command
    os.system(command)
