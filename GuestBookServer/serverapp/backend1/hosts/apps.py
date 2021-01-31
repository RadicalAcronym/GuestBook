from django.apps import AppConfig


class HostsConfig(AppConfig):
    name = 'hosts'


# Not sure SignatureStitcher does
class SignatureStitcher(AppConfig):
    name = 'myapps'
    label = 'SignatureStitcher'

    def ready(self):
        import numpy as np

        self.test_string = np.array([1,2,3,4])

        print('finished with setting up SignatureStitcher')


