# dbt-sdk-python
A Python implementation of DBT API SDK (ported from [dbt-sdk-php](https://bitbucket.org/faithcomesbyhearing/dbt-sdk-php))

## Requirements

 - Python 3 (Recommended 3.6+)

## Installation

```bash

sudo python3 -m pip install dbtsdk

```

## Usage

Below are the steps neccessary to get you started with the DBT SDK.

### 1. Sign up for an API Key

Before you can start using the DBT SDK, you will need to sign up for an API Key at [https://www.digitalbibleplatform.com](https://www.digitalbibleplatform.com).  

### 2. (Optional) Add your API key to your environment

It's best not to hard code your API key in your script file. Instead, save it to your environment and let Python read it from there.

#### On Windows:

```batch

setx DBT_API_KEY "<your api key>"

```

#### On Mac and Linux:

```bash

export DBT_API_KEY=<your api key>

```

To make this environment persist between reboots, add this line to your `.bash_profile` file instead.

### 2. Include the SDK file

In your Python script, import the package.

```python

from dbtsdk import Dbt

```

### 3. Create an instance of the object

When creating the object, pass the API key.

```python

import os

api_key = os.environ['DBT_API_KEY']
dbt = Dbt.Dbt(api_key)

```

### 4. Retrieve volume information

For an example of the usual work flows, as well as examples of retrieving and displaying text, audio, and video, download the [sample code](https://github.com/Nilpo/dbt-sdk-python/blob/master/sample.py).

## API Documentation

Documentation for the underlying REST API can be found in the [Digital Bible Platform Developer Documentation](http://digitalbibleplatform.com/docs).

## License

dbt-sdk-python is available under the MIT license. See the LICENSE file for more info.