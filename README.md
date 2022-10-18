# The Southern California Plate Boundary Region

<a href="https://github.com/sceccode/scpbr.git"><img src="https://github.com/sceccode/scpbr/wiki/images/scpbr_logo.png"></a>

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub repo size](https://img.shields.io/github/repo-size/sceccode/scpbr)
[![scpbr-ci Actions Status](https://github.com/SCECcode/scpbr/workflows/scpbr-ci/badge.svg)](https://github.com/SCECcode/scpbr/actions)
[![scpbr-ucvm-ci Actions Status](https://github.com/SCECcode/scpbr/workflows/scpbr-ucvm-ci/badge.svg)](https://github.com/SCECcode/scpbr/actions)

## Description

The Southern California Plate Boundary Region
2019

## Table of Contents
1. [Software Documentation](https://github.com/SCECcode/scpbr/wiki)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [Credits](#credit)
6. [License](#license)

## Installation

This package is intended to be installed as part of the UCVM framework,
version 22.7.0 or higher. 

This package can also be installed standalone.

$ aclocal
$ autoconf
$ automake --add-missing
$ ./configure --prefix=/dir/to/install
$ make
$ make install

## Usage

### UCVM

As part of [UCVM](https://github.com/SCECcode/ucvm) installation, use 'scpbr' as the model.

### scpbr_query

ASCII query interface(C api) accepts points from stdin with format (lat, lon, dep (m)) and write
data material p roperties to stdout.

## Support
Support for SCPBR is provided by the Southern California Earthquake Center
(SCEC) Research Computing Group.  Users can report issues and feature requests
using SCPBR' github-based issue tracking link below. Developers will also
respond to emails sent to the SCEC software contact listed below.
1. [SCPBR Github Issue Tracker](https://github.com/SCECcode/scpbr/issues)
2. Email Contact: software@scec.usc.edu

## Credits

## Contributing
We welcome contributions to the SCPBR, please contact us at software@scec.usc.edu.

## License
This software is distributed under the BSD 3-Clause open-source license.
Please see the [LICENSE.txt](LICENSE.txt) file for more information.
