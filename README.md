
# Brightsign Take Home Task
## by Shaun Griffith

A simple command line interface to the IPStack API.

## Description

ipwhere: given an IP address and an API access key, return the lattitude/longitude.

ipwhere.py uses the IPStack API, and standard Python modules.

## Getting Started

### Dependencies

* `ipwhere` is developed and tested on Python 3.10.12, but should be compatible with older Python 3 versions.
* * `urllib` had some changes back around 3.3 (?), so earlier versions of Python may fail (untested).

### Installing

* `ipwhere` is hosted on GitHub for user `qm64`.
* Use any of the GitHub or `git` methods for downloading the script.
* There is no other installation needed.

### Configuration

* IPStack requires an API access key.
* * Go to https://ipstack.com/ to get a free access key.
* The access key can be set in a shell environment variable.
	```
	export ipstack_access_key=your_access_key
	```
* * (The access key can also be specified at runtime, on the command line.)

### Execution

* From the command line:
	```
	python3 ipwhere.py -a your_access_key -i some_ip_address
	```
* * The access key can also be specified in a shell env variable, ipstack_access_key
* Typical result:
	```
	python3 ipwhere.py -a your_access_key -i 1.1.1.1
	{"ip": "1.1.1.1", "latitude": -37.7036018371582, "longitude": 145.18063354492188, "status": true}
	```

* Command line help:
	```
	python3 ipwhere.py -h
	usage: ipwhere.py [-h] -i IP_ADDRESS [-a ACCESS_KEY]

	Look up the physical location of an IP address, returning lat/long, using the IPStack API

	options:
	  -h, --help            show this help message and exit
	  -i IP_ADDRESS, --ip_address IP_ADDRESS
	                        IP address in IPV4 or IPV6 notation
	  -a ACCESS_KEY, --access_key ACCESS_KEY
	                        IPStack API access key (defaults to env var ipstack_access_key
	```

### Security

IPStack uses an access key to limit requests, and charges for more than minimal use. Access keys in general may also be required to restrict access to private information. (For `ipwhere`, this is public information.)

The following is a discussion of secrets for command line processes in general:
* Secrets are not secure when given on the command line, as it may be observed from process data.
* Using an env var is also not secure, as other processes may have access to the env var.
* Further, env vars are typically populated from a bash startup file, such as `.bashrc` or an alias file. While these may be unreadable except by the owner, there is still the potential to leak the secret.
* Secrets manager: a secrets manager can authenticate the caller, and share the secret over an encrypted channel.
* * Linux has a keyring, which is securely designed as a secrets manager. Other OSs and clouds have their own versions of this.
* * HTTPS can also be used with a simple API for authentication and secret sharing.
* https://smallstep.com/blog/command-line-secrets/ provides a low-tech solution if the process reads the secret from a file. Through some (accidental?) bash magic, the env var can be set on the command line, and read as if through a file on disk, and be nearly as secure as a secret manager.
* All of these methods require a bit more work, and sometimes extra dependencies.

## Authors

Created by Shaun Griffith, shaun.griffith.1964@gmail.com, in fulfillment of a take home task.
