#!/usr/bin/env python

import IRData.cera20c as cera20c
import datetime

dte=datetime.datetime(1903,2,1)
cera20c.fetch('prmsl',dte)
