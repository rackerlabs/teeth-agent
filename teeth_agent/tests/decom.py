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

import unittest

from teeth_agent import decom
from teeth_agent import errors


class TestDecomMode(unittest.TestCase):
    def setUp(self):
        self.agent_mode = decom.DecomMode()

    def test_decom_mode(self):
        self.assertEqual(self.agent_mode.name, 'DECOM')

    def _build_fake_drive_info(self):
        return {
            'drives': ['/dev/sda', '/dev/sdb'],
            'key': 'sekrit',
        }

    def test_validate_drive_info_success(self):
        drive_info = self._build_fake_drive_info()
        self.agent_mode._validate_drive_info(drive_info)

    def test_validate_drive_info_missing_field(self):
        for field in ['drives', 'key']:
            info = self._build_fake_drive_info()
            del info[field]

            self.assertRaises(errors.InvalidCommandParamsError,
                              self.agent_mode._validate_drive_info,
                              info)

    def test_validate_drive_info_invalid_drives(self):
        info = self._build_fake_drive_info()
        info['drives'] = 'not a list'
        self.assertRaises(errors.InvalidCommandParamsError,
                          self.agent_mode._validate_drive_info,
                          info)

    def test_validate_drive_info_empty_drives(self):
        info = self._build_fake_drive_info()
        info['drives'] = []
        self.assertRaises(errors.InvalidCommandParamsError,
                          self.agent_mode._validate_drive_info,
                          info)

    def test_validate_drive_info_invalid_key(self):
        info = self._build_fake_drive_info()
        info['key'] = ['not', 'a', 'string']
        self.assertRaises(errors.InvalidCommandParamsError,
                          self.agent_mode._validate_drive_info,
                          info)

    def test_validate_drive_info_empty_key(self):
        info = self._build_fake_drive_info()
        info['key'] = ''
        self.assertRaises(errors.InvalidCommandParamsError,
                          self.agent_mode._validate_drive_info,
                          info)
