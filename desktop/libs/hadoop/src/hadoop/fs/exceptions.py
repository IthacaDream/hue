#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

from desktop.lib.exceptions import StructuredException
from desktop.lib.rest.http_client import RestException

LOG = logging.getLogger(__name__)


class PermissionDeniedException(StructuredException):
  def __init__(self, msg, orig_exc=None):
    # TODO(todd) use orig_exc for something fun
    StructuredException.__init__(self,
      "PERMISSION_DENIED",
      msg)


class WebHdfsException(RestException):
  def __init__(self, error):
    RestException.__init__(self, error)

    try:
      json_body = json.loads(self._message)
    except ValueError:
      pass
    else:
      remote_exception = json_body.get('RemoteException', {})
      exception = remote_exception.get('exception')
      message = remote_exception.get('message', '')

      if exception:
        self.server_exc = exception
        self._message = "%s: %s" % (self.server_exc, message)
