import Meteorographica.data.twcr as twcr
twcr.fetch('prmsl',1903,version='2c')
twcr.fetch_observations(1903,version='2c')
