# Copyright 2014 Rackspace, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pecan
from pecan import rest
from wsme import types
from wsmeext import pecan as wsme_pecan

from teeth_agent.api.controllers.v1 import base


class AgentStatus(base.APIBase):
    mode = types.text
    started_at = base.MultiType(float)
    version = types.text

    @classmethod
    def from_agent_status(cls, status):
        instance = cls()
        for field in ('mode', 'started_at', 'version'):
            setattr(instance, field, getattr(status, field))
        return instance


class StatusController(rest.RestController):
    """Controller for getting agent status."""

    @wsme_pecan.wsexpose(AgentStatus)
    def get_all(self):
        agent = pecan.request.agent
        status = agent.get_status()
        return AgentStatus.from_agent_status(status)
