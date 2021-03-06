"""
Copyright 2013 Rackspace, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import mock
import unittest

from ironic_python_agent import hardware


class TestGenericHardwareManager(unittest.TestCase):
    def setUp(self):
        self.hardware = hardware.GenericHardwareManager()

    @mock.patch('os.listdir')
    @mock.patch('os.path.exists')
    @mock.patch('__builtin__.open')
    def test_list_network_interfaces(self,
                                     mocked_open,
                                     mocked_exists,
                                     mocked_listdir):
        mocked_listdir.return_value = ['lo', 'eth0']
        mocked_exists.side_effect = [False, True]
        mocked_open.return_value.read.return_value = '00:0c:29:8c:11:b1\n'
        interfaces = self.hardware.list_network_interfaces()
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].name, 'eth0')
        self.assertEqual(interfaces[0].mac_address, '00:0c:29:8c:11:b1')

    def test_get_os_install_device(self):
        self.hardware._cmd = mock.Mock()
        self.hardware._cmd.return_value = (
            'RO    RA   SSZ   BSZ   StartSec            Size   Device\n'
            'rw   256   512  4096          0    249578283616   /dev/sda\n'
            'rw   256   512  4096       2048      8587837440   /dev/sda1\n'
            'rw   256   512  4096  124967424        15728640   /dev/sda2\n'
            'rw   256   512  4096          0     31016853504   /dev/sdb\n'
            'rw   256   512  4096          0    249578283616   /dev/sdc\n', '')

        self.assertEqual(self.hardware.get_os_install_device(), '/dev/sdb')
        self.hardware._cmd.assert_called_once_with(['blockdev', '--report'])

    def test_list_hardwre_info(self):
        self.hardware.list_network_interfaces = mock.Mock()
        self.hardware.list_network_interfaces.return_value = [
            hardware.NetworkInterface('eth0', '00:0c:29:8c:11:b1'),
            hardware.NetworkInterface('eth1', '00:0c:29:8c:11:b2'),
        ]

        hardware_info = self.hardware.list_hardware_info()
        self.assertEqual(len(hardware_info), 2)
        self.assertEqual(hardware_info[0].type, 'mac_address')
        self.assertEqual(hardware_info[1].type, 'mac_address')
        self.assertEqual(hardware_info[0].id, '00:0c:29:8c:11:b1')
        self.assertEqual(hardware_info[1].id, '00:0c:29:8c:11:b2')
