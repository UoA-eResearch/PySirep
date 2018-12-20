#!/usr/bin/env python

import platform
import clr
import sys

arch, os = platform.architecture()
if arch != "32bit":
  print("This tool only works on 32-bit versions of Python. Sorry :(")
  exit(1)

clr.AddReference("Microsoft.Tools.Connectivity")
from Microsoft.Tools.Connectivity import *

deviceDiscoveryService = DeviceDiscoveryService()
deviceDiscoveryService.Start()
devices = list(deviceDiscoveryService.DevicesDiscovered())
if len(devices) == 0:
  print("No device found - is it attached via microUSB?")
  exit(1)

d = devices[0]
print(d.Address, d.Connection, d.Location, d.Name, d.OSVersion, d.UniqueId)
rd = RemoteDevice(d.UniqueId)
try:
  print("Trying to connect as SshRecoveryUser")
  rd.UserName = "SshRecoveryUser"
  rd.Connect()
except:
  print("Trying to connect as UpdateUser")
  rd.UserName = "UpdateUser"
  rd.Connect()

print("Connected!")

deviceUpdateUtilArgs = ["firmwareversion",
"manufacturer", "serialnumber", "buildbranch", "buildnumber", "buildtimestamp",
"oemdevicename", "uefiname", "buildrevision", "imageversion", "getbatterylevel", "isfirstbootcomplete", "securitystate"]
additionalDeviceUpdateUtilArgs = ["getinstalledpackages", "reboottouefi", "reboottomassstorage", "shutdown", "settime"]

for arg in deviceUpdateUtilArgs:
  resp = rd.RunCommand("C:\\Windows\\System32\\DeviceUpdateUtil.exe", arg)
  print("{}={}".format(arg, resp))

def handle_command(input):
  bits = input.split()
  command = bits[0]
  if len(bits) > 1:
    args = " ".join(bits[1:])
  else:
    args = ""

  if command == "disconnect" or command == "dc":
    rd.Disconnect()
    print("Disconnected")
  elif command == "connect" or command == "c":
    rd.Connect()
    print("Connected")
  elif command in additionalDeviceUpdateUtilArgs:
    resp = rd.RunCommand("C:\\Windows\\System32\\DeviceUpdateUtil.exe", input)
    resp = resp.replace(";", "\n")
    print(resp)
    if command == "shutdown":
      print("Bye!")
      rd.Disconnect()
      exit(0)
  elif command == "get":
    rd.GetFile(args, ".")
    print("Got!")
  elif command == "put":
    remote = bits[1]
    local = bits[2]
    rd.PutFile(remote, local)
    print("Put!")
  elif command == "ping":
    if rd.Ping():
      print("Pong!")
    else:
      print("Thunk")
  elif command == "quit" or command == "q" or command == "exit":
    print("Bye!")
    rd.Disconnect()
    exit(0)
  else:
    resp = rd.RunCommand("C:\\Windows\\System32\\cmd.exe", "/C " + input)
    print(resp)

if len(sys.argv) > 1:
  input = ' '.join(sys.argv[1:])
  handle_command(input)
else:
  #REPL
  while True:
    print("Type a command to run on the remote device")
    command = input()
    try:
      handle_command(command)
    except Exception as e:
      print(e)