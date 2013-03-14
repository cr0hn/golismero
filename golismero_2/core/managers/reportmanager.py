#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Author: Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com

Golismero project site: http://code.google.com/p/golismero/
Golismero project mail: golismero.project@gmail.com

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

__all__ = ["ReportManager"]

from .priscillapluginmanager import *


#------------------------------------------------------------------------------
class ReportManager (object):
    """This class manages the generation of reports."""


    #----------------------------------------------------------------------
    def __init__(self, config):

        # Load plugins
        self.__reporters = PriscillaPluginManager().load_plugins(
            config.enabled_plugins, config.disabled_plugins,
            category = "report")


    #----------------------------------------------------------------------
    def generate_reports(self, config, results):
        """
        Call appropiate plugins (user selected) and generate the reports.

        :param config: configuration of audit.
        :type config: GlobalParams.

        :param results: iterable with results.
        :type results: iterable.
        """

        # Check None
        if not config.output_formats:
            return

        # Get user selected report types
        m_selected_reporters = filter(lambda x: x.report_type in config.output_formats, self.__reporters.itervalues())

        # Generate report
        map(lambda p: p.generate_report(config, results), m_selected_reporters)
