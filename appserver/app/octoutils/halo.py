import cloudpassage
import os

class Halo(object):
    def __init__(self):
        self.halo_key = os.getenv("HALO_API_KEY")
        self.halo_secret = os.getenv("HALO_API_SECRET_KEY")
        self.session = cloudpassage.HaloSession(self.halo_key,
                                                self.halo_secret)
        self.server = cloudpassage.Server(self.session)
        self.group = cloudpassage.ServerGroup(self.session)

    def list_all_servers(self):
        return self.server.list_all()

    def list_all_groups(self):
        return self.group.list_all()
