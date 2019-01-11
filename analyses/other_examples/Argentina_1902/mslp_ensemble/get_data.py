#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1902,8,1)
for version in (['4.5.1']):
    twcr.fetch('prmsl',dte,version=version)
    twcr.fetch('air.2m',dte,version=version)
    twcr.fetch('tmp',dte,level=925,version=version)
    twcr.fetch_observations(dte,version=version)

