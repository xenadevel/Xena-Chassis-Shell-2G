
from cloudshell.traffic.tg import TgChassisDriver

from xena_handler import XenaHandler


class XenaChassisDriver(TgChassisDriver):

    def __init__(self):
        self.handler = XenaHandler()

    def initialize(self, context):
        super(self.__class__, self).initialize(context)

    def cleanup(self):
        pass

    def get_inventory(self, context):
        return super(self.__class__, self).get_inventory(context)
