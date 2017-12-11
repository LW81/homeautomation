#!/usr/bin/env python3

import sys
import os
import argparse
import logging
from subprocess import call

###
# Statics
###
# all we need for the plugs
dictPLUGS = {"turm": "10101 1", "kugel": "10101 2", "kiste": "10101 3", "bad": "10101 4", "ball": "10101 5","leuchtbox": "00000 3"}
dictPLUGSCENES = {"haus": ["turm", "kugel", "kiste", "bad", "ball"],
                  "wohnzimmer": ["ball", "kugel", "turm", "kiste"]}
dictPLUGSTATE = {"ON": 1, "OFF": 0}
# the dictDEVICES dictionary holds any additional device and their ON OFF commands
dictDEVICES = {"diskstation": {"ON": "wakeonlan 00:11:32:2A:6E:33"}}


###
# Functions
###
def build_command(device, state):
    # This returns the command to run to trigger the desired state on the provided device
    # initialize command as this is required by the for loop
    command = ""

    if device in dictPLUGS.keys():
        command = "send %s %s" % (dictPLUGS[device], dictPLUGSTATE[state])

    if device in dictPLUGSCENES.keys():
        if state == "ON":
            lstPlugs=dictPLUGSCENES[device]
        else:
            lstPlugs=reversed(dictPLUGSCENES[device])

        for plug in lstPlugs:
            command += "send %s %s ;" % (dictPLUGS[plug], dictPLUGSTATE[state])


    if (device in dictDEVICES.keys() and state in dictDEVICES[device].keys()):
            command = dictDEVICES[device][state]

    return command


def run_command(command):
    # This runs the command that is handed over and returns the RC

    # Setting up /dev/null
    devnull = open(os.devnull, 'w')

    returnCode = call(command, shell=True, stdout=devnull, stderr=devnull)

    return returnCode


def main(argv):
    try:
        ###
        # Setting up logging (specify format and set loglevel to info so we see something)
        ###
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        logfileName = "ha.log"
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-7.7s]  %(message)s")
        logging.getLogger().setLevel(logging.INFO)
        rootLogger = logging.getLogger()

        fileHandler = logging.FileHandler("{0}/{1}".format(dname, logfileName))
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

        ###
        # Setting up the Parser and parse what we have
        ###
        parser = argparse.ArgumentParser(description='This is a Home Automation Trigger')
        # Adding our two argumets
        parser.add_argument("device", help="Specify name of the device you want to control",
                            choices=(list(dictPLUGS.keys())
                                     + list(dictPLUGSCENES.keys())
                                     + list(dictDEVICES.keys())))
        parser.add_argument("state", help="Specify state to be set",
                            choices=list(dictPLUGSTATE.keys()))
        # and parsing them
        args = parser.parse_args()

        # So here we go
        # First we get the command
        logging.info("Building command to set device: %s to state: %s" % (args.device, args.state))

        command = build_command(args.device, args.state)

        # Check if we got back something useful
        if command:
            # Now we run it
            logging.info("Executing command: %s" % command)

            returnCode = run_command(command)

            # Very basic checking if everything went well
            if returnCode != 0:
                logging.error("Execution of command returned error code: %d" % returnCode)
                return returnCode
            else:
                logging.info("Command executed succesfully.")
                return 0
        else:
            logging.warn("Setting device %s to state %s is not supported."
                         % (args.device, args.state))
            return 1
    except Exception as e:
        logging.exception("ERROR: %sn" % str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
