#!/usr/bin/env python
# -*- coding: utf-8 -*-
from golismero.api.data.information.portscan import Portscan
from golismero.api.data.resource.email import Email
from golismero.api.data.resource.ip import IP
from golismero.api.data.vulnerability.malware.defaced import DefacedUrl, DefacedDomain, DefacedIP
from golismero.api.data.vulnerability.malware.malicious import MaliciousIP, MaliciousUrl, MaliciousDomain
from golismero.api.data.vulnerability.ssl.outdated_certificate import OutdatedCertificate

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/golismero
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

from collections import defaultdict
from requests import get
from traceback import format_exc
from warnings import warn

from golismero.api.config import Config
from golismero.api.data import Database
from golismero.api.data.information.auth import Password
from golismero.api.data.information.banner import Banner
from golismero.api.data.information.html import HTML
from golismero.api.data.information.http import HTTP_Request, HTTP_Response
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.url import Url
from golismero.api.data.vulnerability import Vulnerability
from golismero.api.data.vulnerability.ssl.invalid_certificate import InvalidCertificate
from golismero.api.data.vulnerability.suspicious.header import SuspiciousHeader
from golismero.api.logger import Logger
from golismero.api.net.web_utils import parse_url
from golismero.api.plugin import TestingPlugin, ImportPlugin


#------------------------------------------------------------------------------
class SpiderFootPlugin(TestingPlugin):


    #--------------------------------------------------------------------------
    def check_params(self):

        # Check the parameters.
        try:
            url = Config.plugin_args["url"]
            assert url, "Missing URL"
        except Exception, e:
            raise ValueError(str(e))

        # Connect to the scanner.
        try:
            get(url)
        except Exception, e:
            raise RuntimeError(
                "Cannot connect to SpiderFoot, reason: %s" % e)


    #--------------------------------------------------------------------------
    def get_accepted_info(self):
        return [Domain]


    #--------------------------------------------------------------------------
    def recv_info(self, info):
        raise NotImplementedError()


#------------------------------------------------------------------------------
class SpiderFootImportPlugin(ImportPlugin):


    #--------------------------------------------------------------------------
    def is_supported(self, input_file):
        if input_file and input_file.lower().endswith(".csv"):
            with open(input_file, "rU") as fd:
                row = self.__parse_line(fd.readline())
                return row == [
                    "Updated", "Type", "Module", "Source", "Data"
                ]
        return False


    #--------------------------------------------------------------------------
    def import_results(self, input_file):
        try:
            with open(input_file, "rU") as fd:
                results = self.parse_results(fd)
            if results:
                Database.async_add_many(results)
        except Exception, e:
            fmt = format_exc()
            Logger.log_error(
                "Could not load file: %s" % input_file)
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(fmt)
        else:
            if results:
                data_count = len(results)
                vuln_count = sum(
                    1 for x in results
                    if x.is_instance(Vulnerability)
                )
                if vuln_count == 0:
                    vuln_msg = ""
                elif vuln_count == 1:
                    vuln_msg = " (1 vulnerability)"
                else:
                    vuln_msg = " (%d vulnerabilities)" % vuln_count
                Logger.log(
                    "Loaded %d %s%s from file: %s" %
                    (data_count, "results" if data_count != 1 else "result",
                     vuln_msg, input_file)
                )
            else:
                Logger.log_error("No results found in file: %s" % input_file)


    #--------------------------------------------------------------------------
    def parse_results(self, iterable):

        # Most of the data is extracted directly from each row in the CSV file.
        # Each data type from SpiderFoot is matched to a method in this class.
        # However, some of the data has to be reconstructed after parsing the
        # whole file, since a single row may not have enough information.

        # Variables.
        self.results = {}
        self.reconstruct_http_code = {}
        self.reconstruct_http_headers = {}
        self.reconstruct_http_data = {}
        self.reconstructed_http = {}
        self.strange_headers = defaultdict(set)
        self.port_scan = defaultdict(set)
        self.allow_external = Config.audit_scope.has_scope
        self.allow_subdomains = Config.audit_config.include_subdomains
        warn_data_lost = True

        # Make sure the file format is correct.
        assert self.__parse_line(iterable.next()) == [
            "Updated", "Type", "Module", "Source", "Data"
        ], "Unsupported file format!"

        # For each line...
        for line in iterable:
            try:

                # Parse the line into a row.
                row = self.__parse_line(line)
                if not row:
                    continue

                # Split the row into its columns.
                _, sf_type, sf_module, source, raw_data = row

                # Call the parser method for this data type, if any.
                method = getattr(self, "sf_" + sf_type, self.sf_null)
                partial_results = method(sf_module, source, raw_data)

                # If we have new data, add it to the results.
                self.__add_partial_results(partial_results)

            # On error, log the exception and move to the next row.
            except Exception, e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

        # Reconstruct the suspicious header vulnerabilities.
        for url, headers in self.strange_headers.iteritems():
            try:
                if url in self.reconstructed_http:
                    identity = self.reconstructed_http[url]
                    resp = self.results[identity]
                    for name, value in headers:
                        vulnerability = SuspiciousHeader(resp, name, value)
                        self.__add_partial_results((vulnerability,))
                elif warn_data_lost:
                    warn("Missing information in SpiderFoot results,"
                         " some data may be lost", RuntimeError)
                    warn_data_lost = False
            except Exception, e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)
            headers.clear()
        self.strange_headers.clear()

        # Check if we have incomplete HTTP information.
        if warn_data_lost and (
            self.reconstruct_http_code or
            self.reconstruct_http_headers or
            self.reconstruct_http_data
        ):
            warn("Missing information in SpiderFoot results,"
                 " some data may be lost", RuntimeError)
            warn_data_lost = False
        self.reconstruct_http_code.clear()
        self.reconstruct_http_headers.clear()
        self.reconstruct_http_data.clear()
        self.reconstructed_http.clear()

        # Reconstruct the port scans.
        for address, ports in self.port_scan:
            try:
                ip = IP(address)
                ps = Portscan(ip, (("OPEN", "TCP", port) for port in ports))
                self.__add_partial_results((ip, ps))
            except Exception, e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

        # Return the imported results.
        imported = self.results.values()
        self.results.clear()
        return imported


    #--------------------------------------------------------------------------
    def __parse_line(self, line):

        # Unfortunately we can't use a standard CSV parser, because the CSV
        # files generated by SpiderFoot are malformed (the control characters
        # inside fields are not properly escaped). Our custom parser assumes
        # there won't be any control character injection in any field but the
        # last one, all fields are surrounded by double quotes regardless of
        # their contents, and there's always the same number of fields.
        return [token[1:-1] for token in line.strip().split(",", 4)]


    #--------------------------------------------------------------------------
    def __add_partial_results(self, partial_results):
        if partial_results:
            try:
                iterator = iter(partial_results)
            except TypeError:
                iterator = [partial_results]
            for data in iterator:
                identity = data.identity
                if identity in self.results:
                    self.results[identity].merge(data)
                else:
                    self.results[identity] = data


    #--------------------------------------------------------------------------
    def __reconstruct_http(self, raw_url):
        url = Url(raw_url)
        req = HTTP_Request(
            method = "GET",
            url    = raw_url,
        )
        req.add_resource(url)
        resp = HTTP_Response(
            request = req,
            status  = self.reconstruct_http_code[raw_url],
            headers = eval(self.reconstruct_http_headers[raw_url]),
            data    = self.reconstruct_http_data[raw_url],
        )
        self.reconstructed_http[raw_url] = resp.identity
        del self.reconstruct_http_code[raw_url]
        del self.reconstruct_http_headers[raw_url]
        del self.reconstruct_http_data[raw_url]
        return url, req, resp


    #--------------------------------------------------------------------------
    def sf_null(self, sf_module, source, raw_data):
        pass


    #--------------------------------------------------------------------------
    def sf_URL_STATIC(self, sf_module, source, raw_data):
        return Url(raw_data)


    #--------------------------------------------------------------------------
    def sf_URL_FORM(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source, method="POST")


    #--------------------------------------------------------------------------
    def sf_URL_UPLOAD(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source, method="POST")


    #--------------------------------------------------------------------------
    def sf_URL_PASSWORD(self, sf_module, source, raw_data):
        url = Url(source)
        password = Password(raw_data)
        url.add_information(password)
        return url, password


    #--------------------------------------------------------------------------
    def sf_URL_JAVASCRIPT(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_URL_JAVA_APPLET(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_URL_FLASH(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_LINKED_URL_INTERNAL(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_LINKED_URL_EXTERNAL(self, sf_module, source, raw_data):
        if self.allow_external:
            return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_CO_HOSTED_SITE(self, sf_module, source, raw_data):
        if self.allow_external:
            return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_PROVIDER_JAVASCRIPT(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)


    #--------------------------------------------------------------------------
    def sf_INITIAL_TARGET(self, sf_module, source, raw_data):
        return Domain(raw_data)


    #--------------------------------------------------------------------------
    def sf_SUBDOMAIN(self, sf_module, source, raw_data):
        if self.allow_subdomains:
            return Domain(raw_data)


    #--------------------------------------------------------------------------
    def sf_AFFILIATE_DOMAIN(self, sf_module, source, raw_data):
        if self.allow_external:
            return Domain(raw_data)


    #--------------------------------------------------------------------------
    def sf_PROVIDER_DNS(self, sf_module, source, raw_data):
        try:
            return IP(raw_data)
        except ValueError:
            return Domain(raw_data)


    #--------------------------------------------------------------------------
    def sf_PROVIDER_MAIL(self, sf_module, source, raw_data):
        try:
            return IP(raw_data)
        except ValueError:
            return Domain(raw_data)


    #--------------------------------------------------------------------------
    def sf_SIMILARDOMAIN(self, sf_module, source, raw_data):
        ##return Domain(raw_data)
        pass  # ignoring, it produces too many false positives


    #--------------------------------------------------------------------------
    def sf_IP_ADDRESS(self, sf_module, source, raw_data):
        return IP(raw_data)


    #--------------------------------------------------------------------------
    def sf_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            return IP(raw_data)


    #--------------------------------------------------------------------------
    def sf_GEOINFO(self, sf_module, source, raw_data):
        # ignore, information is too primitive to be of any use
        pass


    #--------------------------------------------------------------------------
    def sf_EMAILADDR(self, sf_module, source, raw_data):
        return Email(raw_data)


    #--------------------------------------------------------------------------
    def sf_WEBSERVER_BANNER(self, sf_module, source, raw_data):
        parsed = parse_url(source)
        domain = Domain(parsed.host)
        banner = Banner(domain, raw_data, parsed.port)
        return domain, banner


    #--------------------------------------------------------------------------
    def sf_TCP_PORT_OPEN(self, sf_module, source, raw_data):
        ip, port = raw_data.split(":")
        ip = ip.strip()
        port = int(port.strip())
        self.port_scan[ip].add(port)


    #--------------------------------------------------------------------------
    def sf_HTTP_CODE(self, sf_module, source, raw_data):
        self.reconstruct_http_code[source] = raw_data
        if source in self.reconstruct_http_headers and \
                        source in self.reconstruct_http_data:
            return self.__reconstruct_http(source)


    #--------------------------------------------------------------------------
    def sf_WEBSERVER_HTTPHEADERS(self, sf_module, source, raw_data):
        self.reconstruct_http_headers[source] = raw_data
        if source in self.reconstruct_http_code and \
                        source in self.reconstruct_http_data:
            return self.__reconstruct_http(source)


    #--------------------------------------------------------------------------
    def sf_TARGET_WEB_CONTENT(self, sf_module, source, raw_data):
        url = Url(source)
        html = HTML(raw_data)
        url.add_information(html)
        self.reconstruct_http_data[source] = raw_data
        if source in self.reconstruct_http_code and \
                        source in self.reconstruct_http_headers:
            return (url, html) + self.__reconstruct_http(source)
        return url, html


    #--------------------------------------------------------------------------
    def sf_RAW_DATA(self, sf_module, source, raw_data):
        if sf_module in ("sfp_spider", "sfp_xref"):
            return self.sf_TARGET_WEB_CONTENT(sf_module, source, raw_data)


    #--------------------------------------------------------------------------
    def sf_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            if sf_module in ("sfp_dns", "sfp_ripe"):
                return self.sf_PROVIDER_DNS(sf_module, source, raw_data)
            if sf_module in ("sfp_crossref", "sfp_xref"):
                return self.sf_LINKED_URL_INTERNAL(sf_module, source, raw_data)


    #--------------------------------------------------------------------------
    def sf_AFFILIATE_WEB_CONTENT(self, sf_module, source, raw_data):
        if self.allow_external and sf_module == "sfp_crossref":
            return self.sf_TARGET_WEB_CONTENT(sf_module, source, raw_data)


    #--------------------------------------------------------------------------
    def sf_SSL_CERTIFICATE_MISMATCH(self, sf_module, source, raw_data):
        domain = Domain(parse_url(source).host)
        vulnerability = InvalidCertificate(  # XXX or is it InvalidCommonName?
            domain = domain,
            tool_id = sf_module,
        )
        return domain, vulnerability


    #--------------------------------------------------------------------------
    def sf_SSL_CERTIFICATE_EXPIRED(self, sf_module, source, raw_data):
        domain = Domain(parse_url(source).host)
        vulnerability = OutdatedCertificate(
            domain = domain,
            tool_id = sf_module,
        )
        return domain, vulnerability


    #--------------------------------------------------------------------------
    def sf_BLACKLISTED_IPADDR(self, sf_module, source, raw_data):
        ip = IP(source)
        vulnerability = MaliciousIP(
            ip = ip,
            tool_id = sf_module,
        )
        return ip, vulnerability


    #--------------------------------------------------------------------------
    def sf_BLACKLISTED_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = MaliciousIP(
                ip = ip,
                tool_id = sf_module,
            )
            return ip, vulnerability


    #--------------------------------------------------------------------------
    def sf_DEFACED(self, sf_module, source, raw_data):
        url = Url(source)
        vulnerability = DefacedUrl(
            url = url,
            tool_id = sf_module,
        )
        return url, vulnerability


    #--------------------------------------------------------------------------
    def sf_DEFACED_COHOST(self, sf_module, source, raw_data):
        if self.allow_external:
            url = Url(source)
            vulnerability = DefacedUrl(
                url = url,
                tool_id = sf_module,
            )
            return url, vulnerability


    #--------------------------------------------------------------------------
    def sf_DEFACED_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            domain = Domain(source)
            vulnerability = DefacedDomain(
                domain = domain,
                tool_id = sf_module,
            )
            return domain, vulnerability


    #--------------------------------------------------------------------------
    def sf_DEFACED_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = DefacedIP(
                ip = ip,
                tool_id = sf_module,
            )
            return ip, vulnerability


    #--------------------------------------------------------------------------
    def sf_MALICIOUS_SUBDOMAIN(self, sf_module, source, raw_data):
        domain = Domain(source)
        vulnerability = MaliciousDomain(
            domain = domain,
            tool_id = sf_module,
        )
        return domain, vulnerability


    #--------------------------------------------------------------------------
    def sf_MALICIOUS_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            domain = Domain(source)
            vulnerability = MaliciousDomain(
                domain = domain,
                tool_id = sf_module,
            )
            return domain, vulnerability


    #--------------------------------------------------------------------------
    def sf_MALICIOUS_COHOST(self, sf_module, source, raw_data):
        if self.allow_external:
            url = Url(source)
            vulnerability = MaliciousUrl(
                url = url,
                tool_id = sf_module,
            )
            return url, vulnerability


    #--------------------------------------------------------------------------
    def sf_MALICIOUS_IPADDR(self, sf_module, source, raw_data):
        ip = IP(source)
        vulnerability = MaliciousIP(
            ip = ip,
            tool_id = sf_module,
        )
        return ip, vulnerability


    #--------------------------------------------------------------------------
    def sf_MALICIOUS_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = MaliciousIP(
                ip = ip,
                tool_id = sf_module,
            )
            return ip, vulnerability


    #--------------------------------------------------------------------------
    def sf_WEBSERVER_STRANGEHEADER(self, sf_module, source, raw_data):
        name, value = raw_data.split(":")
        name = name.strip()
        value = value.strip()
        self.strange_headers[source].add((name, value))
