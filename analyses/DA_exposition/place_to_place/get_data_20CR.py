#!/usr/bin/env python

import IRData.twcr as twcr
import datetime
dte=datetime.datetime(1903,10,22)
twcr.fetch('prmsl',dte,version='2c')
twcr.fetch_observations(dte,version='2c')
