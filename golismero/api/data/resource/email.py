#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Email address type.
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

__all__ = ["Email"]

from . import Resource
from .domain import Domain
from .. import identity
from ...net.web_utils import DecomposedURL, is_in_scope


#------------------------------------------------------------------------------
class Email(Resource):
    """
    Email address.
    """

    resource_type = Resource.RESOURCE_EMAIL


    #----------------------------------------------------------------------
    def __init__(self, address, name = None):
        """
        :param address: Email address.
        :type address: str

        :param name: Optional real life name associated with this email.
        :type name: str | None
        """

        # Email address.
        # TODO: sanitize the email addresses using a regular expression
        self.__address = address

        # Real name.
        self.__name = name

        # Parent constructor.
        super(Email, self).__init__()


    #----------------------------------------------------------------------
    def __str__(self):
        return self.address


    #----------------------------------------------------------------------
    def __repr__(self):
        return "<Email address=%r name=%r>" % (self.address, self.name)


    #----------------------------------------------------------------------
    def is_in_scope(self):
        return is_in_scope(self.domain)


    #----------------------------------------------------------------------
    @identity
    def address(self):
        """
        :return: Email address.
        :rtype: str
        """
        return self.__address


    #----------------------------------------------------------------------
    @property
    def name(self):
        """
        :return: Real name.
        :rtype: str | None
        """
        return self.__name


    #----------------------------------------------------------------------
    @property
    def url(self):
        """
        :return: mailto:// URL for this email address.
        :rtype: str
        """
        return "mailto://" + self.__address


    #----------------------------------------------------------------------
    @property
    def hostname(self):
        """
        :return: Host name for this email address.
        :rtype: str
        """
        return self.__address.split("@", 1)[1].strip().lower()


    #----------------------------------------------------------------------

    @property
    def discovered_resources(self):
        return [Domain(self.hostname)]
