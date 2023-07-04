# Webservice-COPERT

## Description

The COPERT webservice consists of a Django API that calls the command line interface of a COPERT executable located in the project's root directory.
As a result, the functionality provided by COPERT can be exposed to the users of LEAD platform.

## Installation

In order to run the API a Windows machine with a Python installation is required.
The API has been tested with Python 3.11 and with the packages as described in the `requirements.txt` file.
The COPERT executable needs to be [downloaded](https://www.emisia.com/utilities/copert/download/).
Then the user must install COPERT in the project's root directory.
The web service has been tested with COPERT version 5.4.52.

## Usage

The COPERT webservice start by running

```
<path-of-your-python-installation>\python.exe manage.py runserver 0.0.0.0:8000
```

from the project's root path.

Then a user can send a `POST` request to the API to run a COPERT simulation.
A `cURL` example demostrating the required parameters is presented below.

```
curl --location --globoff '{{copert_webservice_url}}' \
    --form 'File=@"/path/to/file"' \
    --form 'keep="true"' \
    --form 'noevap="false"' \
    --form 'alt_country="HU"' \
    --form 'EB="true"' \
    --form 'EF="true"' \
    --form 'outputFile="json"'
```

where `copert_webservice_url` is the URL where the webservice has been deployed and the `/path/to/file` is the local directory of an XLSX file provided as input to the COPERT.

## Support

For any issues or questions please create a new issue on the repository.

## Roadmap

The API has been created for the LEAD Horizon-2020 project supporting COPERT v5.
Future developments will be based on newer versions of the model and taking into account the needs of each project.
