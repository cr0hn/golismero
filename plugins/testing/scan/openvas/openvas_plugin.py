#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run the OpenVas scanner.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/cr0hn/golismero/
Golismero project mail: golismero.project<@>gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from golismero.api.config import Config
from golismero.api.data.resource.ip import IP
from golismero.api.plugin import TestingPlugin

from threading import Event
from functools import partial

# Import the OpenVAS libraries from the plugin data folder.
# FIXME the library should go to thirdparty_libs once it's published!
import os, sys
cwd = os.path.abspath(os.path.split(__file__)[0])
cwd = os.path.join(cwd, ".")
sys.path.insert(0, cwd)

from openvas_lib import VulnscanManager


#------------------------------------------------------------------------------
class OpenVas(TestingPlugin):
    """
    Run the OpenVas scanner.
    """


    #----------------------------------------------------------------------
    def get_accepted_info(self):
        return [IP]


    #----------------------------------------------------------------------
    def recv_info(self, info):

        # Synchronization object to wait for completion.
        m_event = Event()

        # Get the config.
        m_user      = Config.plugin_config.get("user", "admin")
        m_password  = Config.plugin_config.get("password", "admin")
        m_host      = Config.plugin_config.get("host", "127.0.0.1")
        m_port      = Config.plugin_config.get("port", "9390")
        m_timeout   = Config.plugin_config.get("timeout", "30")
        m_profile   = Config.plugin_config.get("profile", "Full and fast")

        # Sanitize the port and timeout.
        try:
            m_port = int(m_port)
        except Exception:
            m_port = 9390
        if m_timeout.lower().strip() in ("inf", "infinite", "none"):
            m_timeout = None
        else:
            try:
                m_timeout = int(m_timeout)
            except Exception:
                m_timeout = None

        # Get the target address.
        m_target    = info.address

        #---------------- XXX DEBUG -----------------
        m_host      = "192.168.0.208"
        m_target    = "8.8.0.0/24" #"192.168.0.194"
        m_profile   = "empty"
        #---------------- XXX DEBUG -----------------

        # Connect to the scanner.
        m_scanner = VulnscanManager(m_host, m_user, m_password, m_port, m_timeout)

        # Launch the scanner.
        m_scan_id = m_scanner.launch_scan(
            m_target,
            profile = m_profile,
            callback_end = partial(lambda x: x.set(), m_event),
            callback_progress = partial(self.update_status_step, text="openvas status scan")
        )

        try:

            # Wait for completion.
            m_event.wait()

            # Get the scan results.
            m_openvas_results = m_scanner.get_results(m_scan_id)

            # Convert the scan results to the GoLismero data model.
            #
            # XXX TODO
            #

        finally:

            # Clean up.
            m_scanner.delete_scan(m_scan_id)
