
from cloudshell.traffic.tg import TgChassisHandler

from cloudshell.shell.core.driver_context import AutoLoadResource, AutoLoadAttribute

from trafficgenerator.tgn_utils import ApiType
from xenavalkyrie.xena_app import init_xena

from xena_data_model import Xena_Chassis_Shell_2G, GenericTrafficGeneratorModule, GenericTrafficGeneratorPort


class XenaHandler(TgChassisHandler):

    def initialize(self, context, logger):
        """
        :param InitCommandContext context:
        """
        resource = Xena_Chassis_Shell_2G.create_from_context(context)
        super(self.__class__, self).initialize(resource, logger)

    def load_inventory(self, context):
        """
        :param InitCommandContext context:
        """

        self.get_connection_details(context)
        port = self.resource.controller_tcp_port
        if not port:
            port = '22611'

        self.xm = init_xena(ApiType.socket, self.logger, 'quali-cs')
        self.xm.session.add_chassis(self.address, int(port), self.password)
        self.xm.session.inventory()

        self._load_chassis(self.xm.session.chassis_list[self.address])
        return self.resource.create_autoload_details()

    def _load_chassis(self, chassis):

        self.resource.vendor = 'Xena'
        self.resource.model_name = chassis.c_info['c_model']
        self.resource.version = chassis.c_info['c_versionno']
        self.resource.serial_number = chassis.c_info['c_serialno']

        for module_id, module in chassis.modules.items():
            self._load_module(module_id, module)

    def _load_module(self, module_id, module):
        """ Get module resource and attributes. """

        gen_module = GenericTrafficGeneratorModule('Module{}'.format(module_id))
        self.resource.add_sub_resource('M{}'.format(module_id), gen_module)
        gen_module.model_name = module.m_info['m_model']
        gen_module.serial_number = module.m_info['m_serialno']
        gen_module.version = module.m_info['m_versionno']

        for port_id, port in module.ports.items():
            self._load_port(gen_module, port_id, port)

    def _load_port(self, gen_module, port_id, port):
        """ Get port resource and attributes. """

        gen_port = GenericTrafficGeneratorPort('Port{}'.format(port_id))
        gen_module.add_sub_resource('P{}'.format(port_id), gen_port)
        gen_port.max_speed = int(port.p_info['p_speed'])
