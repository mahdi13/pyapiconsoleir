# pyapiconsoleir

Python ApiConsole Api Client

[![Build Status](https://app.travis-ci.com/mahdi13/pyapiconsoleir.svg?branch=master)](https://app.travis-ci.com/github/mahdi13/pyapiconsoleir)
[![Build Status](https://badge.fury.io/py/pyapiconsoleir.svg)](https://pypi.org/project/pyapiconsoleir/)
[![Build Status](https://pypip.in/d/pyapiconsoleir/badge.png)](https://pypi.org/project/pyapiconsoleir/)
[![codecov](https://codecov.io/gh/mahdi13/pyapiconsoleir/branch/master/graph/badge.svg)](https://codecov.io/gh/mahdi13/pyapiconsoleir)

Install using pypi:

```shell script
pip install pyapiconsoleir
```

## ApiConsole

Home Page: https://apiconsole.ir/

## Usage

Initialize api client:

```python
from pyapiconsoleir import ApiconsoleClient

api_client = ApiconsoleClient(consumer_key='MY-CONSUMER-KEY', consumer_secret='MY-CONSUMER-SECRET')

print(api_client.postalcode_to_address_v2('4313118369'))

```

