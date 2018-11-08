#!/usr/bin/env python

import platform
import clr

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
  print("No hololens found - is it attached via microUSB?")
  exit(1)

uniqueId = devices[0].UniqueId
print(uniqueId)