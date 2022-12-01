Hello 🐍

# Installation

Install Avvy package as follows:

`pip install avvy`


You will also need to have web3.py installed:

`pip install web3`

# Usage

## Setup

```python3
from avvy import AvvyClient
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
avvy = AvvyClient(w3)
```

## Forward Resolution

For example, using a .avax domain to find an 0x address:

```python3
evm_address = avvy.name('avvydomains.avax').resolve(avvy.RECORDS.EVM)
```

# Development

## Building Client Common

Set `AVVY_CLIENT_COMMON` environment variable if you want to reference a custom instance of client common.

Run `python3 build.py` to build dependencies.
