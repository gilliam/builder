# Copyright 2013 Johan Rydberg.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import sys

from gevent import pywsgi, monkey, socket
monkey.patch_all(thread=False, time=False)

from xdura.api import API
from xdura.builder import Builder


def main(options):
    # check config:
    if not os.path.exists(options['BUILD_SCRIPT']):
        sys.exit("BUILD_SCRIPT does not exist")
    format = '%(levelname)-8s %(name)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=format)

    builder = Builder(logging.getLogger('builder'),
                      options['BUILD_SCRIPT'])
    environ = {'SERVER_NAME': options.get('SERVER_NAME', socket.getfqdn()),
               'SERVER_PORT': options['PORT']}
    app = API(logging.getLogger('api'), environ, 
              options['IMAGE_DIR'], builder)
    logging.info("Start serving requests on port %d" % (
            int(options['PORT']),))
    return pywsgi.WSGIServer(('', int(options['PORT'])), app)


def _start():
    main(os.environ).serve_forever()

if __name__ == '__main__':
    _start()
