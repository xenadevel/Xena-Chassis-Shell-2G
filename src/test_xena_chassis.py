"""
Tests for `XenaChassisDriver`
"""

import pytest
import time

from cloudshell.api.cloudshell_api import AttributeNameValue
from cloudshell.traffic.tg import XENA_CHASSIS_MODEL
from shellfoundry.releasetools.test_helper import (create_session_from_deployment, create_init_command_context,
                                                   create_autoload_resource)

from xena_driver import XenaChassisDriver


@pytest.fixture()
def model():
    yield XENA_CHASSIS_MODEL


@pytest.fixture()
def dut():
    yield ('176.22.65.117', '22611')


@pytest.fixture()
def session():
    yield create_session_from_deployment()


@pytest.fixture()
def context(session, model, dut):
    address, port = dut
    attributes = {model + '.Controller TCP Port': port,
                  model + '.Password': 'h8XUgX3gyjY0vKMg0wQxKg=='}
    init_context = create_init_command_context(session, 'CS_TrafficGeneratorChassis', model, address, attributes,
                                               'Resource')
    yield init_context


@pytest.fixture()
def driver(context):
    driver = XenaChassisDriver()
    driver.initialize(context)
    print(driver.logger.handlers[0].baseFilename)
    yield driver


@pytest.fixture()
def resource(session, model, dut):
    address, port = dut
    attributes = [AttributeNameValue(model + '.Controller TCP Port', port),
                  AttributeNameValue(model + '.Password', 'h8XUgX3gyjY0vKMg0wQxKg==')]
    resource = create_autoload_resource(session, 'CS_TrafficGeneratorChassis', model, address, 'test-xena',
                                        attributes)
    time.sleep(2)
    yield resource
    session.DeleteResource(resource.Name)


def test_autoload(driver, context):
    inventory = driver.get_inventory(context)
    print('\n')
    for r in inventory.resources:
        print('{}, {}, {}'.format(r.relative_address, r.model, r.name))
    print('\n')
    for a in inventory.attributes:
        print('{}, {}, {}'.format(a.relative_address, a.attribute_name, a.attribute_value))


def test_autoload_session(session, resource):
    session.AutoLoad(resource.Name)
    session.GetResourceDetails(resource.Name)
    print('Done')
