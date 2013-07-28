import argparse
import torUtils

parser = argparse.ArgumentParser(description="script for launching TOR instances")
parser.add_argument("--xcitedbyUser", metavar="xcitedbyUser", action="store",
                    default="xcitedby", help="The username under which all temp files will be created. Defaults to xcitedby.")
parser.add_argument("--numTorInstances", dest="numTorInstances", type=int, action="store",
                   default=4,
                   help="The number of TOR instances to launch.")
commandLineArgs = parser.parse_args()

torUtils.torStart(commandLineArgs.xcitedbyUser, commandLineArgs.numTorInstances)
