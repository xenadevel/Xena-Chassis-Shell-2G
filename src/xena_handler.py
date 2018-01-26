
from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from xenamanager.xena_app import init_xena


class XenaHandler(object):

    def initialize(self, context, logger):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        self.logger = logger
        self.address = context.resource.address
        port = context.resource.attributes['Xena Chassis Shell 2G.Controller TCP Port']
        if not port:
            port = '22611'
        encripted_password = context.resource.attributes['Xena Chassis Shell 2G.Password']
        password = CloudShellSessionContext(context).get_api().DecryptPassword(encripted_password).Value

        self.xm = init_xena(self.logger, 'quali-shell')
        self.xm.session.add_chassis(self.address, int(port), password)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.resources = []
        self.attributes = []
        self.xm.session.inventory()
        self._get_chassis(self.xm.session.chassis_list[self.address])
        details = AutoLoadDetails(self.resources, self.attributes)
        return details

    def _get_chassis(self, chassis):

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Model Name',
                                                 attribute_value=chassis.c_info['c_model']))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Xena Chassis Shell 2G.Serial Number',
                                                 attribute_value=chassis.c_info['c_serialno']))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Xena Chassis Shell 2G.Server Description',
                                                 attribute_value=''))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Vendor',
                                                 attribute_value='Xena'))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Version',
                                                 attribute_value=chassis.c_info['c_versionno']))

        for module_id, module in chassis.modules.items():
            self._get_module(module_id, module)

    def _get_module(self, module_id, module):
        """ Get module resource and attributes. """

        relative_address = 'M' + str(module_id)
        model = 'Xena Chassis Shell 2G.GenericTrafficGeneratorModule'
        resource = AutoLoadResource(model=model, name='Module' + str(module_id), relative_address=relative_address)
        self.resources.append(resource)
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorModule.Model Name',
                                                 attribute_value=module.m_info['m_model']))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.Serial Number',
                                                 attribute_value=module.m_info['m_serialno']))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.Version',
                                                 attribute_value=module.m_info['m_versionno']))

        for port_id, port in module.ports.items():
            self._get_port(relative_address, port_id, port)

    def _get_port(self, card_relative_address, port_id, port):
        """ Get port resource and attributes. """

        relative_address = card_relative_address + '/P' + str(port_id)
        resource = AutoLoadResource(model='Xena Chassis Shell 2G.GenericTrafficGeneratorPort',
                                    name='Port' + str(port_id),
                                    relative_address=relative_address)
        self.resources.append(resource)
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorPort.Max Speed',
                                                 attribute_value=port.p_info['p_speed']))
