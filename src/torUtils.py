import os
import os.path

XCITEDBY_USER                = "mike"
TOR_EXECUTABLE_ABSOLUTE_PATH = "/Users/" + XCITEDBY_USER + "/xcitedby/TorBrowser_en-US.app/Contents/MacOS/tor"
TOR_TMP_ABSOLUTE_PATH        = "/Users/" + XCITEDBY_USER + "/xcitedby/tmp/tor/"
TOR_DATA_ABSOLUTE_BASE_PATH  = TOR_TMP_ABSOLUTE_PATH + "data/"
TOR_PID_ABSOLUTE_PATH        = TOR_TMP_ABSOLUTE_PATH + "pid/"
NUM_TOR_INSTANCES            = 4
TOR_BASE_CONTROL_PORT        = 8118
TOR_BASE_SOCKS_PORT          = 9050

def torStart():

    for i in range(NUM_TOR_INSTANCES):
        torDataAbsolutePath = TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/" % i
        if not os.path.exists(torDataAbsolutePath):
            print "[TORUTILS MKDIR] " + torDataAbsolutePath
            os.makedirs(torDataAbsolutePath)

    if not os.path.exists(TOR_PID_ABSOLUTE_PATH):
        print "[TORUTILS MKDIR] " + TOR_PID_ABSOLUTE_PATH
        os.makedirs(TOR_PID_ABSOLUTE_PATH)

    for i in range(NUM_TOR_INSTANCES):
        controlPort            = TOR_BASE_CONTROL_PORT + i
        socksPort              = TOR_BASE_SOCKS_PORT   + i
        torPidFileAbsolutePath = TOR_PID_ABSOLUTE_PATH       + "tor%02d.pid" % i
        torDataAbsolutePath    = TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/"    % i

        command = \
            "%s --RunAsDaemon 1 --ControlPort %d --SocksPort %d --PidFile %s --DataDirectory %s" % \
            (TOR_EXECUTABLE_ABSOLUTE_PATH, controlPort, socksPort, torPidFileAbsolutePath, torDataAbsolutePath)

        print "[TORUTILS COMMAND] " + command
        os.system(command)

def torStop():

    command = "killall tor"
    print "[TORUTILS COMMAND] " + command
    os.system(command)
