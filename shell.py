#!/usr/bin/env python

import clr

clr.AddReference("Microsoft.Tools.Connectivity")
from Microsoft.Tools.Connectivity import *

deviceDiscoveryService = DeviceDiscoveryService()
deviceDiscoveryService.Start()
uniqueId = deviceDiscoveryService.DevicesDiscovered()[0].UniqueId
print(uniqueId)