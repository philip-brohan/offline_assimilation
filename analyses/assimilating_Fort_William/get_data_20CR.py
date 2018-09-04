#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1903,1,1)
twcr.fetch('prmsl',dte,version='2c')
twcr.fetch_observations(dte,version='2c')
