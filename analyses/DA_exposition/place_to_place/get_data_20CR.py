#!/usr/bin/env python

import IRData.twcr as twcr
import datetime
dte=datetime.datetime(1903,10,22)
twcr.fetch('prmsl',dte,version='4.5.1')
twcr.fetch_observations(dte,version='4.5.1')
