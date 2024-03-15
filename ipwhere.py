"""Brightsign Takehome Task.

Given an IP address, look up its physical location in lat/long.
"""

import os
import sys
from urllib.request import urlopen
from urllib.error import (HTTPError, URLError)
import ipaddress
import json
import argparse

# Constant strings (keys and URL elements)
BASE_URL = "api.ipstack.com"
ACCESS_KEY = "access_key"
IP = "ip"
LATITUDE = "latitude"
LONGITUDE = "longitude"
STATUS = "status"
ERROR = "error"
INFO = "info"

# env var for IPStack access key
IPSTACK_ACCESS_KEY = "ipstack_access_key"


class Ip2LatLong:
    """Convert an IP address to lat/long."""

    def __init__(self):
        """Initialise the object."""

    def create_error(self, ip_address, msg):
        """Create an error message as a dict.

        Args:
            ip_address (str): IP address
            msg (str): Error message

        Returns dict:
            {"ipaddress": <ip_address>, # str
             "error": <error message> # str
             "status": False # bool
            }

        """
        result = {
            IP: ip_address,
            ERROR: msg,
            STATUS: False
        }
        return result

    def ip_to_lat_long(self, ip_address, access_key=None):
        """Given an IP address, return the lat/long.

        Args:
            ip_address (str): IP address (IPV4 or IPV6)
            access_key (str): The IPstack access key
                defaults to object's stored value

        Returns:
            lat, long as a JSON str:
                {"ip": <ipaddress>, # str
                 "latitude": <latitude>, # float
                 "longitude": <longitude>, # float
                 "status": True # bool
                }

                If there is an error, an error field is returned in JSON instead:
                    {"ip": <ip_address>, # str
                     "error": <error message> # str
                     "status": False # bool
                    }

        """
        if access_key is None:
            access_key = os.getenv(IPSTACK_ACCESS_KEY, None)
            if access_key is None:
                error = self.create_error(
                    ip_address,
                    f"Error: no access key for IPStack given (also checked env {IPSTACK_ACCESS_KEY})"
                )
                return json.dumps(error)

        try:
            # Not interested in the IP address object, just the validation.
            _ = ipaddress.ip_address(ip_address)
        except ValueError as exc:
            # Not a valid IPV4 or IPV6 address
            msg = f"Error: ({ip_address}) is not a valid IP address"
            error = {
                IP: ip_address,
                ERROR: msg
            }
            return json.dumps(error)

        url = f"http://{BASE_URL}/{ip_address}?{ACCESS_KEY}={access_key}"
        try:
            # Comment out the real urlopen to avoid using up free requests.
            # pass
            response = urlopen(url)
        except (HTTPError, URLError) as exc:
            error = self.create_error(
                ip_address,
                f"Error: {str(exc)}"
            )
            return json.dumps(error)

        else:
            try:
                # For testing without a connection:
                # to avoid using up free requests,
                # populate the dict from dummy data.
                # json_data = json.dumps(
                #     {'ip': '1.1.1.1',
                #      'latitude': 42.0,
                #      'longitude': 42.0
                #     }
                # )
                # The real line to decode the response.
                json_data = response.read().decode('utf-8', 'replace')
            except Exception as exc:
                error = self.create_error(
                    ip_address,
                    f"Error: accessing or decoding response {str(exc)}"
                )
                return json.dumps(error)

        rslt = json.loads(json_data)
        if ERROR in rslt:
            if INFO in rslt[ERROR]:
                msg = rslt[ERROR][INFO]
            else:
                msg = "Unknown error in response from IPStack."
            error = self.create_error(ip_address, msg)
            return json.dumps(error)

        result = {}
        for k in [IP, LATITUDE, LONGITUDE]:
            result[k] = rslt.get(k, None)
            if result[k] is None:
                error = self.create_error(
                    ip_address,
                    f"Error: response is missing {k}"
                )
                return json.dumps(error)

        result[STATUS] = True

        return json.dumps(result)


# Create an argparse variant that prints the help on a parsing error
class MyParser(argparse.ArgumentParser):
    """Redefine the error method to write out the help message."""

    def error(self, message):
        """Write out the help on parse error, and exit."""
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    PARSER = MyParser(
        description=(
            "Look up the physical location of an IP address, " +
            "returning lat/long, using the IPStack API")
    )
    PARSER.add_argument(
        "-i", "--ip_address", required=True,
        help="IP address in IPV4 or IPV6 notation"
    )
    PARSER.add_argument(
        "-a", "--access_key",
        help=f"IPStack API access key (defaults to env var {IPSTACK_ACCESS_KEY}"
    )

    ARGS = PARSER.parse_args()

    IP_2_LAT_LONG = Ip2LatLong()

    RESULT = IP_2_LAT_LONG.ip_to_lat_long(ARGS.ip_address, ARGS.access_key)

    print(RESULT)
