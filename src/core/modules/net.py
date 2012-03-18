from socket import gaierror, timeout
from httplib import HTTPConnection, HTTPException, NotConnected, InvalidURL, UnknownProtocol, UnknownTransferEncoding, UnimplementedFileMode, IncompleteRead, ImproperConnectionState, BadStatusLine
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse
