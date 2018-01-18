#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `XenaChassisShell
"""

import sys
import unittest

from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession
from shellfoundry.releasetools.test_helper import create_autoload_resource

xena_chassis = {'xena-chassis': {'address': '176.22.65.114',
                                 'password': 'h8XUgX3gyjY0vKMg0wQxKg==',
                                 'modules': 11}}


class TestXenaChassisShell(unittest.TestCase):

    session = None

    def setUp(self):
        self.session = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')

    def tearDown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def testHelloWorld(self):
        pass

    def test_xena_chassis(self):
        self._get_inventory('xena-chassis', xena_chassis['xena-chassis'])

    def _get_inventory(self, name, properties):
        attributes = [AttributeNameValue('Xena Chassis Shell 2G.Password', properties['password'])]
        resource = create_autoload_resource(self.session, 'Xena Chassis Shell 2G', properties['address'], name,
                                            attributes)
        self.session.AutoLoad(resource.Name)
        resource_details = self.session.GetResourceDetails(resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(resource.Name)


if __name__ == '__main__':
    sys.exit(unittest.main())
