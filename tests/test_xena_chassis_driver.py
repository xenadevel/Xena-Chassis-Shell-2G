#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `XenaChassisDriver`
"""

import sys
import logging
import unittest

from shellfoundry.releasetools.test_helper import create_autoload_context_2g

from driver import XenaChassisDriver

address = '176.22.65.114'
port = '22611'
password = 'h8XUgX3gyjY0vKMg0wQxKg=='


class TestXenaChassisDriver(unittest.TestCase):

    def setUp(self):
        self.context = create_autoload_context_2g(model='Xena Chassis Shell 2G', address=address, port=port,
                                                  password=password)
        self.driver = XenaChassisDriver()
        self.driver.initialize(self.context)
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def tearDown(self):
        pass

    def testHelloWorld(self):
        pass

    def testAutoload(self):
        self.inventory = self.driver.get_inventory(self.context)
        for r in self.inventory.resources:
            print r.relative_address, r.model, r.name
        for a in self.inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    sys.exit(unittest.main())
