data={
	"informations": {
		"6cd9bff569ff5cc2a28625ee2b1e51ca": {
			"display_name": "Service Fingerprint",
			"links": ["be375163029d9f54c39a83174786c9f6"],
			"data_type": 1,
			"protocol": "SSL",
			"port": 443,
			"depth": 0,
			"data_subtype": 1302,
			"information_category": 4,
			"class": "ServiceFingerprint",
			"identity": "6cd9bff569ff5cc2a28625ee2b1e51ca",
			"name": "unknown"
		},
		"9a8590b1720d5d046b822959d78b4ca7": {
			"display_name": "Port Scan Results",
			"links": ["be375163029d9f54c39a83174786c9f6"],
			"data_type": 1,
			"timestamp": 1391114264.0,
			"ports": [["CLOSED",
			"TCP",
			554],
			["CLOSED",
			"TCP",
			1119],
			["CLOSED",
			"TCP",
			1755],
			["OPEN",
			"TCP",
			21],
			["CLOSED",
			"TCP",
			1935],
			["OPEN",
			"TCP",
			443],
			["OPEN",
			"TCP",
			80],
			["CLOSED",
			"TCP",
			53]],
			"depth": 0,
			"data_subtype": 1304,
			"address": "93.184.216.119",
			"information_category": 4,
			"class": "Portscan",
			"identity": "9a8590b1720d5d046b822959d78b4ca7"
		},
		"314657380c683955d125f2d340abcd5f": {
			"display_name": "Service Fingerprint",
			"links": ["be375163029d9f54c39a83174786c9f6"],
			"data_type": 1,
			"protocol": "TCP",
			"port": 80,
			"depth": 0,
			"data_subtype": 1302,
			"information_category": 4,
			"class": "ServiceFingerprint",
			"identity": "314657380c683955d125f2d340abcd5f",
			"name": "unknown"
		},
		"2cf4eeb5400144220cc97087633fc434": {
			"display_name": "Web Server Fingerprint",
			"links": ["606489619590839a1c0ad662bcdc0189"],
			"data_type": 1,
			"canonical_name": "unknown",
			"related": {
				
			},
			"depth": 0,
			"data_subtype": 1300,
			"version": "45BF",
			"others": {
				
			},
			"information_category": 4,
			"banner": "EOS (lax004/45BF)",
			"class": "WebServerFingerprint",
			"identity": "2cf4eeb5400144220cc97087633fc434",
			"name": "EOS (lax004"
		},
		"744f818a94ce1a7a8f7358ae1c9aba12": {
			"display_name": "Port Scan Results",
			"links": ["c2a54c7128318728b74cdda512be7015"],
			"data_type": 1,
			"timestamp": 1391114116.0,
			"ports": [],
			"depth": 0,
			"data_subtype": 1304,
			"address": "2606:2800:220:6d:26bf:1447:1097:aa7",
			"information_category": 4,
			"class": "Portscan",
			"identity": "744f818a94ce1a7a8f7358ae1c9aba12"
		},
		"0e001d64286040f29a4b03def58618f5": {
			"city": null,
			"region_code": null,
			"display_name": "Geolocation",
			"links": ["be375163029d9f54c39a83174786c9f6"],
			"data_type": 1,
			"areacode": null,
			"street_addr": "8636-8692 Northwest 120th Street, Potwin, KS 67123, USA",
			"zipcode": null,
			"longitude": -97.0,
			"metro_code": null,
			"latitude": 38.0,
			"depth": 0,
			"data_subtype": 1307,
			"region_name": null,
			"country_code": "US",
			"country_name": "United States",
			"information_category": 4,
			"class": "Geolocation",
			"identity": "0e001d64286040f29a4b03def58618f5",
			"accuracy": null
		}
	},
	"stats": {
		"informations": 6,
		"vulns_by_level": {
			"Middle": 2,
			"Low": 1
		},
		"vulns_by_type": {
			"Insecure SSL/TLS Algorithm": 1,
			"Invalid CN Field": 1,
			"Invalid SSL/TLS Certificate": 1
		},
		"resources": 39,
		"vulnerabilities": 3
	},
	"audit_scope": {
		"domains": ["example.com",
		"www.example.com"],
		"web_pages": ["http://www.example.com/"],
		"addresses": ["2606:2800:220:6d:26bf:1447:1097:aa7",
		"93.184.216.119"],
		"roots": ["*.example.com"]
	},
	"vulnerabilities": [{
		"edb": [],
		"mskb": [],
		"cisco": [],
		"links": ["bf609a63ec6b1d6267e5b5644eb5df63"],
		"ca": [],
		"sectrack": [],
		"glsa": [],
		"references": ["https://cwe.mitre.org/data/definitions/327.html"],
		"vu": [],
		"domain_id": "bf609a63ec6b1d6267e5b5644eb5df63",
		"risk": 0,
		"impact": 0,
		"display_name": "Insecure SSL/TLS Algorithm",
		"severity": 0,
		"osvdb": [],
		"usn": [],
		"mdvsa": [],
		"capec": [],
		"data_subtype": "ssl/insecure_algorithm",
		"cvss_score": null,
		"plugin_id": "testing/scan/sslscan",
		"cwe": ["CWE-327"],
		"bid": [],
		"dsa": [],
		"tool_id": null,
		"description": "An SSL/TLS certificate was found to be using an insecure algorithm. This may allow a strategically located attacker to snoop on network traffic, or perform a Man-In-The-Middle attack against unsuspecting users connecting to this host.",
		"data_type": 2,
		"xf": [],
		"cvss_base": "0.0",
		"cvss_vector": null,
		"plugin_name": "SSLScan",
		"false_positive": null,
		"class": "InsecureAlgorithm",
		"identity": "81bdd671efd51d8312b19d413d85ecdd",
		"custom_id": null,
		"level": "middle",
		"title": "Insecure SSL/TLS Algorithm",
		"solution": "Create a new certificate using only secure algorithms.",
		"nessus": [],
		"depth": 0,
		"algorithms": ["ECDHE-RSA-DES-CBC3-SHA",
		"DES-CBC3-SHA",
		"ECDHE-RSA-DES-CBC3-SHA",
		"DES-CBC3-SHA"],
		"vmsa": [],
		"ms": [],
		"sa": [],
		"cve": [],
		"rhsa": []
	},
	{
		"edb": [],
		"mskb": [],
		"cisco": [],
		"links": ["bf609a63ec6b1d6267e5b5644eb5df63"],
		"ca": [],
		"sectrack": [],
		"glsa": [],
		"references": ["https://cwe.mitre.org/data/definitions/327.html"],
		"vu": [],
		"common_name": "gp1.wac.edgecastcdn.net",
		"domain_id": "bf609a63ec6b1d6267e5b5644eb5df63",
		"risk": 0,
		"impact": 0,
		"display_name": "Invalid CN Field",
		"severity": 0,
		"osvdb": [],
		"usn": [],
		"mdvsa": [],
		"capec": [],
		"data_subtype": "ssl/invalid_common_name",
		"cvss_score": null,
		"plugin_id": "testing/scan/sslscan",
		"cwe": ["CWE-327"],
		"cvss_base": "0.0",
		"dsa": [],
		"tool_id": null,
		"description": "An invalid CN field was found in a SSL/TLS certificate. This may allow a strategically located attacker to snoop on network traffic, or perform a Man-In-The-Middle attack against unsuspecting users connecting to this host.",
		"data_type": 2,
		"xf": [],
		"bid": [],
		"cvss_vector": null,
		"plugin_name": "SSLScan",
		"false_positive": null,
		"class": "InvalidCommonName",
		"identity": "cf136dd675d37545121e3212aa38489e",
		"custom_id": null,
		"level": "middle",
		"title": "Invalid CN Field",
		"solution": "Create a new certificate with the correct CN field.",
		"nessus": [],
		"depth": 0,
		"vmsa": [],
		"ms": [],
		"sa": [],
		"cve": [],
		"rhsa": []
	},
	{
		"edb": [],
		"mskb": [],
		"cisco": [],
		"links": ["bf609a63ec6b1d6267e5b5644eb5df63"],
		"ca": [],
		"sectrack": [],
		"glsa": [],
		"references": ["https://cwe.mitre.org/data/definitions/327.html"],
		"vu": [],
		"domain_id": "bf609a63ec6b1d6267e5b5644eb5df63",
		"risk": 0,
		"impact": 0,
		"display_name": "Invalid SSL/TLS Certificate",
		"severity": 0,
		"osvdb": [],
		"usn": [],
		"mdvsa": [],
		"capec": [],
		"data_subtype": "ssl/invalid_certificate",
		"cvss_score": null,
		"plugin_id": "testing/scan/sslscan",
		"cwe": ["CWE-327"],
		"cvss_base": "0.0",
		"dsa": [],
		"tool_id": null,
		"description": "An invalid SSL/TLS certificate was found. This may allow a strategically located attacker to snoop on network traffic, or perform a Man-In-The-Middle attack against unsuspecting users connecting to this host.",
		"data_type": 2,
		"xf": [],
		"bid": [],
		"cvss_vector": null,
		"plugin_name": "SSLScan",
		"false_positive": null,
		"class": "InvalidCertificate",
		"identity": "8e3e7e7414a65360c6c2153b83517c83",
		"custom_id": null,
		"level": "low",
		"title": "Invalid SSL/TLS Certificate",
		"solution": "Create a new certificate.",
		"nessus": [],
		"depth": 0,
		"vmsa": [],
		"ms": [],
		"sa": [],
		"cve": [],
		"rhsa": []
	}],
	"summary": {
		"report_time": "2014-01-30 20:38:05.512860",
		"start_time": "2014-01-30 21:34:17.170099 UTC",
		"audit_name": "example",
		"stop_time": "2014-01-30 21:38:05.285127 UTC",
		"run_time": "0 days, 0 hours, 3 minutes and 48 seconds"
	},
	"supported_taxonomies": {
		"edb": "ExploitDB",
		"mskb": "Microsoft Knowledge Base",
		"cisco": "Cisco Security Advisory",
		"xf": "ISS X-Force",
		"osvdb": "OSVDB",
		"nessus": "Nessus Plugin",
		"usn": "Ubuntu Security Notice",
		"bid": "Bugtraq",
		"sectrack": "Security Tracker",
		"glsa": "Gentoo Linux Security Advisory",
		"mdvsa": "Mandriva Security Advisory",
		"vu": "CERT Vulnerability Note",
		"capec": "CAPEC",
		"vmsa": "VMWare Security Advisory",
		"ms": "Microsoft Advisory",
		"sa": "Secunia Advisory",
		"cve": "CVE",
		"cwe": "CWE",
		"ca": "CERT Advisory",
		"rhsa": "RedHat Security Advisory",
		"dsa": "Debian Security Advisory"
	},
	"version": "GoLismero 2.0.0b3",
	"report_type": "full",
	"resources": {
		"b77cff0b4bface41590d945a4bddcd25": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "password@example.com",
			"class": "Email",
			"identity": "b77cff0b4bface41590d945a4bddcd25"
		},
		"6111141b3f8d1adef003c894d951e377": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "anything@example.com",
			"class": "Email",
			"identity": "6111141b3f8d1adef003c894d951e377"
		},
		"4db6529d72f1c9370c9194154b821ca7": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "manoto4030@example.com",
			"class": "Email",
			"identity": "4db6529d72f1c9370c9194154b821ca7"
		},
		"f523cc4661fa22a31b3b5d5df2a2b6ae": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "ai_do@example.com",
			"class": "Email",
			"identity": "f523cc4661fa22a31b3b5d5df2a2b6ae"
		},
		"53c3d4de3d318701a1f5c013216244e0": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "mail@example.com",
			"class": "Email",
			"identity": "53c3d4de3d318701a1f5c013216244e0"
		},
		"e6e2b7e6bb1b1cf0db752dc3b09790a2": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "netko@example.com",
			"class": "Email",
			"identity": "e6e2b7e6bb1b1cf0db752dc3b09790a2"
		},
		"bdf721947961ffb518f8b78fd8ecc811": {
			"display_name": "Folder URL",
			"links": [],
			"data_type": 3,
			"url": "http://www.example.com/",
			"depth": -1,
			"data_subtype": 3,
			"class": "FolderUrl",
			"identity": "bdf721947961ffb518f8b78fd8ecc811"
		},
		"c8656844e6cfd3a6a7353b587c50ec63": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "example@example.com",
			"class": "Email",
			"identity": "c8656844e6cfd3a6a7353b587c50ec63"
		},
		"f332597400cc691d3379a51d9f39870c": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "sender@example.com",
			"class": "Email",
			"identity": "f332597400cc691d3379a51d9f39870c"
		},
		"26490a42728bf6ba41f76db701ba792d": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "pat@example.com",
			"class": "Email",
			"identity": "26490a42728bf6ba41f76db701ba792d"
		},
		"4ef8781d067ec3a08bc7889e4d876563": {
			"display_name": "Domain Name",
			"links": ["19aa7c8cbfeb9fa93e84e6c79774bbf7",
			"1b3c539141aef5ac69eeab464c89f5fe",
			"1f94704ac48e720c4d3cf9ba413cb5b7",
			"21ccc2b0ee8b816b37e0bf67e8767584",
			"26490a42728bf6ba41f76db701ba792d",
			"28edbb2873308eee1e59ff3df19e40d8",
			"29c37ad06f837286bac25ca5b2fbf64d",
			"3b8fdea296d6d9fbcde536d5e4570e54",
			"4a7c60d5ce17fbf823f71218c999dcb1",
			"4db6529d72f1c9370c9194154b821ca7",
			"50e26e1c1992fb50caef68cae1cb001b",
			"53c3d4de3d318701a1f5c013216244e0",
			"5afd8dbc40ce7dcafc114d1f6f34ea92",
			"6111141b3f8d1adef003c894d951e377",
			"7ca372c785b8147382ded3a8259365df",
			"a8cb2573a44fb377067a4984d6329c2f",
			"b6cf098de17e092e0c05f0b955bcc062",
			"b77cff0b4bface41590d945a4bddcd25",
			"bf1524a278d70a19bbe006189ff7f522",
			"c8656844e6cfd3a6a7353b587c50ec63",
			"d2ae59c82d0bdd2f260c9297b2115c99",
			"d4b4c8283fd022bd2f96a2a4b8b42d96",
			"d5f73e7f4e5d0fbb045706618d895bb8",
			"e1b6539743749726a75301734345d044",
			"e6e2b7e6bb1b1cf0db752dc3b09790a2",
			"ee9a6a067bede066751af3b7067215cb",
			"f332597400cc691d3379a51d9f39870c",
			"f40fb45e473e5fbdb8cea0b4c26104b0",
			"f523cc4661fa22a31b3b5d5df2a2b6ae",
			"f74264375c55f508b459173bfadf7129"],
			"data_type": 3,
			"hostname": "example.com",
			"depth": 0,
			"data_subtype": 4,
			"class": "Domain",
			"identity": "4ef8781d067ec3a08bc7889e4d876563"
		},
		"bf609a63ec6b1d6267e5b5644eb5df63": {
			"display_name": "Domain Name",
			"links": ["81bdd671efd51d8312b19d413d85ecdd",
			"8e3e7e7414a65360c6c2153b83517c83",
			"af8dfcef2c359e251e12119c4c26107d",
			"cf136dd675d37545121e3212aa38489e",
			"d24a0a776b88a2dab8bee36b20c430dd"],
			"data_type": 3,
			"hostname": "www.example.com",
			"depth": 0,
			"data_subtype": 4,
			"class": "Domain",
			"identity": "bf609a63ec6b1d6267e5b5644eb5df63"
		},
		"3b8fdea296d6d9fbcde536d5e4570e54": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "mozilla@example.com",
			"class": "Email",
			"identity": "3b8fdea296d6d9fbcde536d5e4570e54"
		},
		"7ca372c785b8147382ded3a8259365df": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "myname@example.com",
			"class": "Email",
			"identity": "7ca372c785b8147382ded3a8259365df"
		},
		"21ccc2b0ee8b816b37e0bf67e8767584": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "reply@example.com",
			"class": "Email",
			"identity": "21ccc2b0ee8b816b37e0bf67e8767584"
		},
		"4a7c60d5ce17fbf823f71218c999dcb1": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "john.doe@example.com",
			"class": "Email",
			"identity": "4a7c60d5ce17fbf823f71218c999dcb1"
		},
		"b6cf098de17e092e0c05f0b955bcc062": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "recipient@example.com",
			"class": "Email",
			"identity": "b6cf098de17e092e0c05f0b955bcc062"
		},
		"d2ae59c82d0bdd2f260c9297b2115c99": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "sample@example.com",
			"class": "Email",
			"identity": "d2ae59c82d0bdd2f260c9297b2115c99"
		},
		"29c37ad06f837286bac25ca5b2fbf64d": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "dbmaster@example.com",
			"class": "Email",
			"identity": "29c37ad06f837286bac25ca5b2fbf64d"
		},
		"19aa7c8cbfeb9fa93e84e6c79774bbf7": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "you@example.com",
			"class": "Email",
			"identity": "19aa7c8cbfeb9fa93e84e6c79774bbf7"
		},
		"bf1524a278d70a19bbe006189ff7f522": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "accounts@example.com",
			"class": "Email",
			"identity": "bf1524a278d70a19bbe006189ff7f522"
		},
		"1b3c539141aef5ac69eeab464c89f5fe": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "john@example.com",
			"class": "Email",
			"identity": "1b3c539141aef5ac69eeab464c89f5fe"
		},
		"28edbb2873308eee1e59ff3df19e40d8": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "postmaster@example.com",
			"class": "Email",
			"identity": "28edbb2873308eee1e59ff3df19e40d8"
		},
		"f40fb45e473e5fbdb8cea0b4c26104b0": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "support@example.com",
			"class": "Email",
			"identity": "f40fb45e473e5fbdb8cea0b4c26104b0"
		},
		"d69bbc149f9f680333492aeace90f603": {
			"display_name": "URL",
			"links": [],
			"data_type": 3,
			"url": "http://www.example.com/",
			"method": "GET",
			"depth": 0,
			"data_subtype": 1,
			"post_data": null,
			"class": "Url",
			"identity": "d69bbc149f9f680333492aeace90f603"
		},
		"d4b4c8283fd022bd2f96a2a4b8b42d96": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "name@example.com",
			"class": "Email",
			"identity": "d4b4c8283fd022bd2f96a2a4b8b42d96"
		},
		"50e26e1c1992fb50caef68cae1cb001b": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "virusalert@example.com",
			"class": "Email",
			"identity": "50e26e1c1992fb50caef68cae1cb001b"
		},
		"d24a0a776b88a2dab8bee36b20c430dd": {
			"display_name": "E-Mail Address",
			"links": ["bf609a63ec6b1d6267e5b5644eb5df63"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "user@www.example.com",
			"class": "Email",
			"identity": "d24a0a776b88a2dab8bee36b20c430dd"
		},
		"c2a54c7128318728b74cdda512be7015": {
			"display_name": "IP Address",
			"links": ["744f818a94ce1a7a8f7358ae1c9aba12"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 5,
			"address": "2606:2800:220:6d:26bf:1447:1097:aa7",
			"class": "IP",
			"identity": "c2a54c7128318728b74cdda512be7015"
		},
		"d5f73e7f4e5d0fbb045706618d895bb8": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "osoba@example.com",
			"class": "Email",
			"identity": "d5f73e7f4e5d0fbb045706618d895bb8"
		},
		"606489619590839a1c0ad662bcdc0189": {
			"display_name": "Base URL",
			"links": ["2cf4eeb5400144220cc97087633fc434"],
			"data_type": 3,
			"url": "http://www.example.com/",
			"depth": 0,
			"data_subtype": 2,
			"class": "BaseUrl",
			"identity": "606489619590839a1c0ad662bcdc0189"
		},
		"1f94704ac48e720c4d3cf9ba413cb5b7": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "winter@example.com",
			"class": "Email",
			"identity": "1f94704ac48e720c4d3cf9ba413cb5b7"
		},
		"5afd8dbc40ce7dcafc114d1f6f34ea92": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "nobody@example.com",
			"class": "Email",
			"identity": "5afd8dbc40ce7dcafc114d1f6f34ea92"
		},
		"e1b6539743749726a75301734345d044": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "steve@example.com",
			"class": "Email",
			"identity": "e1b6539743749726a75301734345d044"
		},
		"af8dfcef2c359e251e12119c4c26107d": {
			"display_name": "E-Mail Address",
			"links": ["bf609a63ec6b1d6267e5b5644eb5df63"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "abcd1234@www.example.com",
			"class": "Email",
			"identity": "af8dfcef2c359e251e12119c4c26107d"
		},
		"a8cb2573a44fb377067a4984d6329c2f": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "someone@example.com",
			"class": "Email",
			"identity": "a8cb2573a44fb377067a4984d6329c2f"
		},
		"ee9a6a067bede066751af3b7067215cb": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "bob@example.com",
			"class": "Email",
			"identity": "ee9a6a067bede066751af3b7067215cb"
		},
		"be375163029d9f54c39a83174786c9f6": {
			"display_name": "IP Address",
			"links": ["0e001d64286040f29a4b03def58618f5",
			"314657380c683955d125f2d340abcd5f",
			"6cd9bff569ff5cc2a28625ee2b1e51ca",
			"9a8590b1720d5d046b822959d78b4ca7"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 5,
			"address": "93.184.216.119",
			"class": "IP",
			"identity": "be375163029d9f54c39a83174786c9f6"
		},
		"f74264375c55f508b459173bfadf7129": {
			"display_name": "E-Mail Address",
			"links": ["4ef8781d067ec3a08bc7889e4d876563"],
			"data_type": 3,
			"depth": 0,
			"data_subtype": 6,
			"address": "foo@example.com",
			"class": "Email",
			"identity": "f74264375c55f508b459173bfadf7129"
		}
	}
}