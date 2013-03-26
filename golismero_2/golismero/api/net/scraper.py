#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
# URL scraping API
#-----------------------------------------------------------------------

__license__="""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com
  Mario Vilas | mvilas@gmail.com

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

__all__ = ["is_link", "extract_from_text", "extract_from_html"]

from BeautifulSoup import BeautifulSoup
from urlparse import urldefrag, urljoin, urlparse

import re

#
# TODO: a generic "extract" function that uses the appropriate helper
#       function to extract URLs, based on the content-type header.
#


#----------------------------------------------------------------------
# URL detection regex, by John Gruber.
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
_re_url = re.compile("""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""", re.I)


#----------------------------------------------------------------------
def is_link(url, base_url):
    """
    Determines if an URL is a link to another resource.

    :param url: URL to test.
    :type url: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :returns: bool -- True if the URL points to another page or resource, False otherwise.
    """

    # URLs that point to the same page in a different fragment are not links.
    if urldefrag(url)[0] == base_url:
        return False

    # Scripting and data URLs are not links.
    scheme = urlparse(url)[0]
    if not scheme:
        scheme = ""
    scheme = scheme.lower()
    if scheme.endswith("://"):
        scheme = scheme[:-3]
    if scheme in ("javascript", "vbscript", "data"):
        return False

    # All other URLs are links.
    return True


#----------------------------------------------------------------------
def extract_from_text(text, base_url, only_links = True):
    """
    Extract URLs from text.

    :param text: Text.
    :type text: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :param only_links: If True, only extract links to other resources. If False, extract all URLs.
    :type only_links: bool

    :returns: set(str) -- Extracted URLs.
    """

    # Set where the URLs will be collected.
    result = set()
    add_result = result.add

    # Remove the fragment from the base URL.
    base_url = urldefrag(base_url)[0]

    # Look for URLs using a regular expression.
    for url in _re_url.findall(text):

        # Canonicalize the URL.
        url = urljoin(base_url, url.strip())

        # Discard URLs that are not links to other pages or resources.
        if not only_links or is_link(url, base_url = base_url):

            # Add the URL to the set.
            add_result(url)

    # Return the set of collected URLs.
    return result


#----------------------------------------------------------------------
def extract_from_html(raw_html, base_url, only_links = True):
    """
    Extract URLs from HTML.

    Implementation notes:

    - The current implementation is fault tolerant, meaning it will try
      to extract URLs even if the HTML is malformed and browsers wouldn't
      normally see those links. This may therefore result in some false
      positives.

    - HTML5 tags are supported, including tags not currently supported by
      any major browser.

    :param raw_html: Raw HTML data.
    :type raw_html: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :param only_links: If True, only extract links to other resources. If False, extract all URLs.
    :type only_links: bool

    :returns: set(str) -- Extracted URLs.
    """

    # Set where the URLs will be collected.
    result = set()
    add_result = result.add

    # Remove the fragment from the base URL.
    base_url = urldefrag(base_url)[0]

    # Parse the raw HTML.
    bs = BeautifulSoup(raw_html,
                       convertEntities = BeautifulSoup.ALL_ENTITIES)

    # Some sets of tags and attributes to look for.
    href_tags = {"a", "link", "area"}
    src_tags = {"form", "script", "img", "iframe", "frame", "embed", "source", "track"}
    param_names = {"movie", "href", "link", "src", "url", "uri"}

    # Iterate once through all tags...
    for tag in bs.findAll():

        # Get the tag name, case insensitive.
        name = tag.name.lower()

        # Extract the URL from each tag that has one.
        url = None
        if name in href_tags:
            url = tag.get("href", None)
        elif name in src_tags:
            url = tag.get("src", None)
        elif name == "param":
            name = tag.get("name", "").lower().strip()
            if name in param_names:
                url = tag.get("value", None)
        elif name == "object":
            url = tag.get("data", None)
        elif name == "applet":
            url = tag.get("code", None)
        elif name == "meta":
            name = tag.get("name", "").lower().strip()
            if name == "http-equiv":
                p = tag.get("content", "").find(";")
                if p >= 0:
                    url = content[ p + 1 : ]
        elif name == "base":
            url = tag.get("href", None)
            if url is not None:  # update the base url
                base_url = urljoin(base_url, url.strip(), allow_fragments = False)

        # If we found an URL in this tag...
        if url is not None:

            # Canonicalize the URL.
            url = urljoin(base_url, url.strip())

            # Discard URLs that are not links to other pages or resources.
            if not only_links or is_link(url, base_url = base_url):

                # Add the URL to the set.
                add_result(url)

    # Return the set of collected URLs.
    return result
