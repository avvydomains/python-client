Hello 🐍

# Installation

Install Avvy package as follows:

`pip install avvy`


You will also need to have web3.py installed:

`pip install web3`

# Usage

## Quick Start

```python3
from avvy import AvvyClient
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
avvy = AvvyClient(w3)

# use forward resolution to convert a .avax domain into an 0x address
evm_address = avvy.name('avvydomains.avax').resolve(avvy.RECORDS.EVM)
print(f'avvydomains.avax forward resolves to {evm_address}')

# use reverse resolution to convert an 0x address into a .avax domain
_hash = avvy.reverse(avvy.RECORDS.EVM, '0x9BC4e7C1Fa4Ca66f6B2F4B6F446Dad80Ec541983')
name = _hash.lookup()
print(f'0x9BC4e7C1Fa4Ca66f6B2F4B6F446Dad80Ec541983 reverse resolves to {name.name}')
```

## Names

Names represent .avax domains, or subdomains. You can create one as follows:

```python3
name = avvy.name('avvydomains.avax')
```

#### Has the name been minted?

```python3
name.is_minted() # returns bool
```

#### When does the name expire?

```python3
name.get_expiry() # returns unix timestamp, int
```

#### Is the name expired?

```python3
name.is_expired() # returns bool
```

#### Who is the registrant of the domain?

```python3
name.registrant() # returns str or None
```

- If the domain has been minted, this returns the 0x address of the registrant.
- If the domain is minted & expired, this returns the 0x address of the previous registrant (no longer active registration).
- If the domain has not been minted, this will return `None`.

#### Forward Resolution

If you want to find data points that have been set on a domain, you want to use forward resolution.

```python3
evm_address = name.resolve(avvy.RECORDS.EVM) # returns str or None
```

- If the user has set the record on the domain, this will return the record
- If the lookup fails for any reason, this will return None. Lookups can fail for a number of reasons, including:
  - Resolver is not set
  - Record was not set
  - Domain is expired

The same method can be used to look up custom data:

```python3
custom_value = name.resolve('CUSTOM_KEY')
```

## Hashes

At the smart-contract level, .avax names are represented as hashes (large integers). 

#### Convert a .avax name into it's hash value

```python3
hash_num = avvy.utils.name_hash('avvydomains.avax') # returns int
```

#### Convert a hash value to a .avax name

```python3
avvy.hash(hash_num).lookup() # returns a Name object or None
```

- If we are able to convert the hash to a .avax name, this will return an instance of `Name`
- If we are not able to convert the hash to a .avax name, this will return None. 
- We can only convert the hash to a .avax name if someone knowing the .avax name (preimage) has published the name to the RainbowTable contract.

## Reverse Resolution

Use Reverse Resolution to convert a value into a .avax name (e.g. going from an 0x address to a .avax name).

```python3
# returns a Hash object or None
_hash = name.reverse(avvy.RECORDS.EVM, '0x9BC4e7C1Fa4Ca66f6B2F4B6F446Dad80Ec541983') 
```

- If we are able to reverse the data type / value, this returns an instance of `Hash`.
- If the data type provided does not support reverse resolution, this will return None.
- If the value provided does not have a reverse record set, this will return None.

After retrieving the Hash, users can find the name via `_hash.lookup()`

## Records

Standard Records exist in the system as numbers. We maintain a list of these records in the [Client Common repository](https://github.com/avvydomains/client-common/blob/master/records/records.json).

The list of these records is available to the user as a `dict` via `avvy.RECORDS._LIST`.

Standard record keys can be accessed via `avvy.RECORDS.{KEY}`, replacing `{KEY}` with the name of the record (e.g. `avvy.RECORDS.EVM`, `AVVY.RECORDS.X_CHAIN`, etc.

## Direct Contract Access

To interact directly with Avvy contracts:

```python3
# returns an instance of a Web3.py contract
w3_contract = avvy.load_contract(contract_name)
```

In some cases, you might want to load the ABI with a different address:

```python3
w3_contract = avvy.load_contract('PublicResolverV1', resolver_address)
```

# Have Questions?

Join us in `#technical-chat` channel of the [Avvy Domains Discord](https://discord.gg/mn5un9mUqq) for technical support.
