#!/usr/bin/python
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



__all__ = ["HTTP_Request", "HTTP_Response"]

from .information import *
from .html import *

from thirdparty_libs.urllib3.util import parse_url
from core.main.commonstructures import get_unique_id
from os.path import basename
from re import findall

#------------------------------------------------------------------------------
class HTTP_Request (Information):
    """"""

    TYPE_HTTP      = 0
    TYPE_JSON      = 1
    TYPE_SOAP      = 2
    TYPE_VIEWSTATE = 3

    #----------------------------------------------------------------------
    def __init__(self, url, method='GET', post_data = None, cache = True, follow_redirects=False, cookie="", random_user_agent=False, request_type = 0):
        """Constructor"""
        # Set method
        self.__method = method.upper() if method.upper() in ['POST', 'GET', 'PUT'] else 'GET'

        # Set url
        self.__url = url
        self.__parsed_url = parse_url(url) if url != '' else None

        # Follow redirects
        self.__follow_redirects = follow_redirects

        # Set main headers
        self.__headers = {
            'User-Agent' : self.generate_user_agent() if random_user_agent else "Mozilla/5.0 (compatible, GoLismero/2.0 The Web Knife; +http://code.google.com/p/golismero)",
            'Accept-Language' : "en-US",
            'Accept' : self.__get_accept_type(),
        }

        # Cache?
        self.__cache = cache

        # Post data
        self.__post_data = post_data

        # Post data
        if self.__post_data:
            self.__headers.update(self.__get_content_type())

        # Get type of request
        self.__type = request_type

        # This vas specify if request has files attached
        self.__files_attached = False

    #----------------------------------------------------------------------
    #
    # Public functions
    #
    #----------------------------------------------------------------------
    def generate_user_agent(self):
        """Return a random user agent string"""
        from random import randint

        m_user_agents = [
            "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.5.22 Version/10.50",
            "Mozilla/6.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:2.0.0.0) Gecko/20061028 Firefox/3.0",
            "Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
            "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/13.0.1",
            "Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20120724 Debian Iceweasel/15.0",
            "Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9",
            "Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)",
            "Mozilla/4.0(compatible; MSIE 7.0b; Windows NT 6.0)",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+",
            "Mozilla/5.0 (PLAYSTATION 3; 3.55)",
            "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
            "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"

        ]

        # Get a random user-agent
        return m_user_agents[randint(0, len(m_user_agents) - 1)]


    def add_file_from_file(self, param_name, path_to_file):
        """Add file from path

        :param param_name: name of parameter in resquest
        :type param_name: str

        :param path_to_file: path to file to load.
        :type path_to_file: str
        """
        if all([path_to_file, param_name]):
            self.add_file_from_object(param_name, basename(path_to_file), open(path_to_file).read())


    #----------------------------------------------------------------------
    def add_file_from_object(self, param_name, file_name, obj):
        """Add file from a binary object.

        :param param_name: name of parameter in resquest
        :type param_name: str

        :param file_name: name of file to send
        :type file_name: str

        :param obj: binary object to send
        :type obj: binary data
        """
        if all([param_name, file_name, obj]):
            # Create dict, if not exits
            if not self.__post_data:
                self.__post_data = {}

            # Fix method, if is GET
            if self.__method == "GET":
                self.__method = "POST"

            # Add data
            self.__post_data[param_name] = (file_name, obj )

            # Set request to file attached
            self.__files_attached = True



    #----------------------------------------------------------------------
    #
    # Private functions
    #
    #----------------------------------------------------------------------
    def __get_accept_type(self, accept_type=None):
        """Get accepted types.

        Available types are: html, text, all.

        :type accetp_type: str
        :return: complete string for specified input accept type.
        """

        m_types = {
            "html": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text" : "text/plain",
            "all": "*/*"
        }

        # If type is in list
        if accept_type:
            if accept_type in m_types.keys():
                return m_types[accept_type]

        # Otherwise
        return m_types["all"]



    def __get_content_type(self):
        """Generate dict entry with content type info"""
        return { 'Content-Type' : "application/x-www-form-urlencoded; charset=UTF-8" }


    #----------------------------------------------------------------------
    #
    # Read/Write parameters
    #
    #----------------------------------------------------------------------
    # Hostname
    def __get_host(self):
        return self.__headers['Host']
    def __set_host(self, value):
        self.__headers['Host'] = value if not value else ''
        self.__parsed_url.hostname = self.__headers['Host']
    hostname = property(__get_host, __set_host)

    # User agent
    def __get_user_agent(self):
        return self.__headers['User-Agent']
    def __set_user_agent(self, value):
        self.__headers['User-Agent'] = value if not value else ''
    user_agent = property(__get_user_agent, __set_user_agent)

    # Accept language
    def __get_accept_language(self):
        return self.__headers['Accept-Language']
    def __set_accept_language(self, value):
        self.__headers['Accept-Language'] = value if not value else ''
    accept_language = property(__get_accept_language, __set_accept_language)

    # Content-type
    def __get_accept(self):
        return self.__headers['Accept']
    def __set_accept(self, value):
        self.__headers['Accept'] = value if not value else ''
    accept = property(__get_accept, __set_accept)

    # Referer
    def __get_referer(self):
        return self.__headers['Referer']
    def __set_referer(self, value):
        self.__headers['Referer'] = value if not value else ''
    referer = property(__get_referer, __set_referer)

    # Cookie
    def __get_cookie(self):
        return self.__headers['Cookie']
    def __set_cookie(self, value):
        self.__headers['Cookie'] = value if not value else ''
    cookie = property(__get_cookie, __set_cookie)

    # Content type
    def __get_content_type(self):
        return self.__headers['Content-Type'] if 'Content-Type' in self.__headers['Content-Type'] else None
    def __set_content_type(self, value):
        self.__headers['Content-Type'] = value if not value else ''
    content_type = property(__get_content_type, __set_content_type)


    # Post data
    def __get_post_data(self):
        return self.__post_data
    def __set_post_data(self, value):
            if self.__post_data:
                self.__post_data.update(value)
            else:
                self.__post_data = value

            # Set content type
            self.__headers.update(self.__set_content_type())
    post_data = property(__get_post_data, __set_post_data)

    # Raw headers
    def __get_raw_headers(self):
        return self.__headers
    def __set_raw_headers(self, value):
        if isinstance(value, dict):
            self.__headers.update(value)
    raw_headers = property(__get_raw_headers, __set_raw_headers)

    #----------------------------------------------------------------------
    #
    # Read only parameters
    #
    #----------------------------------------------------------------------
    def __get_url(self):
        """"""
        return self.__url
    url = property(__get_url)

    #----------------------------------------------------------------------
    def __get_parsed_url(self):
        """"""
        return self.__parsed_url
    parsed_url = property(__get_parsed_url)

    #----------------------------------------------------------------------
    def __get_method(self):
        """"""
        return self.__method
    method = property(__get_method)

    #----------------------------------------------------------------------
    def __get_is_cacheable(self):
        """"""
        return self.__cache
    is_cacheable = property(__get_is_cacheable)

    #----------------------------------------------------------------------
    def __get_request_type(self):
        """"""
        return self.__type
    request_type = property(__get_request_type)

    #----------------------------------------------------------------------
    def __get_follow_redirects(self):
        """"""
        return self.__follow_redirects
    follow_redirects = property(__get_follow_redirects)

    #----------------------------------------------------------------------
    def __get_files_attached(self):
        """"""
        return self.__files_attached
    files_attached = property(__get_files_attached)




#------------------------------------------------------------------------------
class HTTP_Response (Information):
    """
    This class contain all info fo HTTP response
    """

    #----------------------------------------------------------------------
    def __init__(self, raw_response, request_time, request):
        """Constructor"""

        super(HTTP_Response, self).__init__(Information.INFORMATION_HTTP_RESPONSE)

        # URL from response was requested
        self.__from_request = request

        # HTML code of response
        self.__raw_data = raw_response.data if raw_response.data != None else ""
        # HTTP response code
        self.__http_response_code = raw_response.status
        # HTTP response reason
        self.__http_response_code_reason = raw_response.reason
        # HTTP headers
        self.__http_headers = dict(raw_response.headers)
        # HTTP headers in raw format
        self.__http_headers_raw = ''.join(["%s: %s\n" % (k,v) for k,v in raw_response.headers.items()])
        # Request time
        self.__request_time = request_time
        # Generate information object
        self.__information = self.__get_type_by_raw(self.__http_headers, self.__raw_data)
        # Wrapper for cookie
        self.__cookie = None

        #
        # Counters
        #
        # Total number of words of body response
        self.__word_count = None
        # Total number of lines of body response
        self.__lines_count = None
        # Total number of characters of body response
        self.__char_count = None

    #----------------------------------------------------------------------
    def __get_raw(self):
        """"""
        return self.__raw_data
    raw_data = property(__get_raw)

    #----------------------------------------------------------------------
    def __get_cookie(self):
        """"""
        return self.__request.cookie
    cookie = property(__get_cookie)

    #----------------------------------------------------------------------
    def __get_http_response_code(self):
        """"""
        return self.__http_response_code
    http_code = property(__get_http_response_code)

    #----------------------------------------------------------------------
    def __get_http_response_reason(self):
        """"""
        return self.__http_response_code_reason
    http_reason = property(__get_http_response_reason)

    #----------------------------------------------------------------------
    def __get_http_headers(self):
        """"""
        return self.__http_headers
    http_headers = property(__get_http_headers)

    #----------------------------------------------------------------------
    def __get_http_raw_headers(self):
        """"""
        return self.__http_headers_raw
    http_headers_raw = property(__get_http_raw_headers)

    #----------------------------------------------------------------------
    def __get_request_time(self):
        """"""
        return self.__request_time
    request_time = property(__get_request_time)

    #----------------------------------------------------------------------
    def __get_information(self):
        """"""
        return self.__information
    information = property(__get_information)

    #----------------------------------------------------------------------
    def __get_type_by_raw(self, headers, data):
        """
        Get an information type from a raw object
        """
        m_return_content = None
        if headers:
            if "content-type" in headers.keys():
                m_content_type = headers["content-type"]

                # Select the type
                if m_content_type.startswith('text/html'):
                    m_return_content = HTML(data)

        return m_return_content


    #----------------------------------------------------------------------
    def __get_char_count(self):
        """"""
        if not self.__char_count:
            self.__char_count = len(self.__raw_data)

        return self.__char_count

    char_count = property(__get_char_count)
    """Number of chars of body response"""

    #----------------------------------------------------------------------
    def __get_lines_count(self):
        """"""
        if not self.__lines_count:
            self.__lines_count = len(findall("\S+", self.__raw_data))

        return self.__lines_count

    lines_count = property(__get_lines_count)
    """Number of lines of body response"""

    #----------------------------------------------------------------------
    def __get_words_count(self):
        """"""
        if not self.__word_count:
            self.__word_count = self.__raw_data.count('\n')
        return self.__word_count

    words_count = property(__get_words_count)
    """Number of words of body response"""

    #----------------------------------------------------------------------
    def __get_from_request(self):
        """"""
        return self.__from_request
    from_request = property(__get_from_request)
