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

import subprocess

from teeth_agent import base
from teeth_agent import errors


def _read_hdparm_output(process):
    output = p.communicate()[0]
    output = output.replace('\n', '')
    output = output.replace('\t', '')
    output = output.replace(' ', '')
    return output


def _check_for_frozen_drive(drive):
    # TODO(jimrollenhagen) does this require the key?
    p = subprocess.Popen('hdparm -I {}'.format(drive),
                         shell=True,
                         stdout=subprocess.PIPE)
    output = _read_hdparm_output(p)

    if 'notfrozen' not in output:
        raise errors.FrozenDriveError(drive)


def _secure_drive(drive, key):
    _check_for_frozen_drive(drive)

    cmd = 'hdparm --user-master u --security-set-pass {} {}'.format(key, drive)

    # TODO(jimrollenhagen) error checking
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.communicate()


def _erase_drive(drive, key):
    _check_for_frozen_drive(drive)

    cmd = 'hdparm --user-master u --security-erase {} {}'.format(key, drive)

    # TODO(jimrollenhagen) error checking
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.communicate()


class SecureDrivesCommand(base.AsyncCommandResult):
    def execute(self):
        drives = self.command_params['drives']
        key = self.command_params['key']

        for drive in drives:
            _secure_drive(drive, key)


class EraseDrivesCommand(base.AsyncCommandResult):
    def execute(self):
        drives = self.command_params['drives']
        key = self.command_params['key']

        for drive in drives:
            _erase_drive(drive, key)


class DecomMode(base.BaseAgentMode):
    def __init__(self):
        super(DecomMode, self).__init__('DECOM')
        self.command_map['secure_drives'] = self.secure_drives
        self.command_map['erase_drives'] = self.erase_drives

    def _validate_drive_info(self, drive_info):
        drives = drive_info.get('drives')
        if type(drives) != list or not drives:
            raise errors.InvalidCommandParamsError(
                'Parameter \'drives\' must be a list with at least one '
                'element.')

        key = drive_info.get('key')
        if not isinstance(key, basestring) or not key:
            raise errors.InvalidCommandParamsError(
                'Parameter \'drives\' must be a non-empty string.')

    def secure_drives(self, command_name, **command_params):
        self._validate_drives(command_params)
        return SecureDrivesCommand(command_name, command_params).start()

    def erase_drives(self, command_name, **command_params):
        self._validate_drives(command_params)
        return EraseDrivesCommand(command_name, command_params).start()
