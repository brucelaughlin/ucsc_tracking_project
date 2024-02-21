

 # Deactivate particles:


deactivate_elements(indices, reason)

self.deactivate_elements(self.elements.mass < 0.5, reason='vanished')

        ('age_seconds', {'dtype': np.float32,
                         'units': 's',
                         'seed': False,
                         'default': 0}),

#so:
self.elements.age_seconds    should be what we want..?

# seconds in 30 days : 86400 * 30 = 2592000
#self.deactivate_elements(self.elements.age_seconds > 2592000, reason='age > 30 days')


# seconds in 90 days : 86400 * 90 = 7776000
self.deactivate_elements(self.elements.age_seconds > 7776000, reason='age > 90 days')








