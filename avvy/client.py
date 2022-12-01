from .contracts import contract_data
from .records import record_data
from .exceptions import *
import time


class Name:
	def __init__(self, client, name):
		self.client = client
		self.name = name.lower()
		self.domain = self._get_domain(name).lower()
	
	def _get_domain(self, name):
		"""
		Takes a name with an arbitrary number of labels
		and returns the second-level domain (i.e. 2 labels)
		"""
		split = name.split('.')
		return split[len(split) - 2] + '.' + split[len(split) - 1]
	
	def _get_resolver(self):
		"""
		Returns the resolver for this domain.
		"""
		domain_hash = self.client.utils.name_hash(self.domain)
		_hash = self.client.utils.name_hash(self.name)
		resolver_registry = self.client.load_contract('ResolverRegistryV1')
		try:
			address, dataset_id = resolver_registry.functions.get(domain_hash, _hash).call()
		except Exception as e:
			if 'ResolverRegistry: resolver not set' in str(e):
				raise ResolverNotSetException()
			raise e
		resolver = self.client.load_contract('PublicResolverV1', address)
		return [resolver, dataset_id]
	
	def _resolve_standard(self, key):
		_hash = self.client.utils.name_hash(self.name)
		resolver, dataset_id = self._get_resolver()
		return resolver.functions.resolveStandard(dataset_id, _hash, key).call()
	
	def _resolve_custom(self, key):
		_hash = self.client.utils.name_hash(self.name)
		resolver, dataset_id = self._get_resolver()
		return resolver.functions.resolve(dataset_id, _hash, key).call()
	
	def get_expiry(self):
		_hash = self.client.utils.name_hash(self.domain)
		domain_contract = self.client.load_contract('Domain')
		return domain_contract.functions.getDomainExpiry(_hash).call()
	
	def is_expired(self):
		expiry = self.get_expiry()
		now = int(time.time())
		return now >= expiry
	
	def resolve(self, key):
		if self.is_expired():
			raise DomainExpiredException()

		if type(key) == int:
			return self._resolve_standard(key)

		elif type(key) == str:
			return self._resolve_custom(key)

		raise InvalidKeyException('Resolution key must be a string or an integer')


class Hash:
	def __init__(self, client, _hash):
		self.client = client
		self.hash = _hash
	
	def lookup(self):
		rainbow_table = self.client.load_contract('RainbowTableV1')
		try:
			input_signals = rainbow_table.functions.lookup(self.hash).call()
		except Exception as e:
			if 'RainbowTableV1: entry not found' in str(e):
				return None
			raise e
		domain = self.client.utils.decode_name_hash_input_signals(input_signals)
		return Name(self.client, domain)


class Records:
	def __init__(self):
		for record in record_data['records']:
			setattr(self, record['name'], record['key'])


class Utils:
	def __init__(self, client):
		self.client = client

	def bits_to_num(self, bits):
		return int(bits, 2)
	
	def num_to_bits(self, n, fill):
		return bin(n)[2:].zfill(fill)
	
	def _prep_preimage_signal(self, chars): 
		bits_arr = [self.num_to_bits(c, 8) for c in chars][::-1]
		bits = ''.join(bits_arr)
		return self.bits_to_num(bits)
	
	def name_hash_iteration(self, _hash, label):
		chars = [ord(c) for c in label]
		while len(chars) < 62:
			#chars = [0] + chars
			chars += [0] 
		pair = [chars[:31], chars[31:]]
		_input = [_hash] + [self._prep_preimage_signal(p) for p in pair]
		return self.client.poseidon(_input)
	
	def name_hash(self, name):
		labels = name.split('.')
		labels.reverse()
		_hash = 0
		for label in labels:
			_hash = self.name_hash_iteration(_hash, label)
		return _hash
	
	def _decode_magic(self, pair):
		char_arrays = ["".join(self.num_to_bits(i, 248)) for i in pair]
		bits = char_arrays[0] + char_arrays[1]
		final = ""
		for i in range(0, len(bits), 8):
			__next = self.bits_to_num(bits[i:i + 8])
			if __next != 0:
				final += chr(__next)
		return final[::-1]
	
	def decode_name_hash_input_signals(self, signals):
		unf = []
		for i in range(len(signals)):
			if i % 2 == 0:
				unf.append((signals[i], signals[i + 1]))
		arr = [self._decode_magic(i) for i in unf]
		return ".".join(arr[::-1])


class Client:
	def __init__(self, w3, chain_id=None):
		if chain_id is None: chain_id = 43114
		self.w3 = w3
		self.chain_id = chain_id
		self.utils = Utils(self)
		self.RECORDS = Records()
		self.poseidon_cache = {}
	
	def load_contract(self, contract_name, address=None):
		chain = contract_data[str(self.chain_id)]
		contract = chain['contracts'][contract_name]
		if address is None:
			address = contract['address']
		abi = contract['abi']
		return self.w3.eth.contract(
			address=address,
			abi=abi
		)
	
	def poseidon(self, triad):

		# pre-cache for "avax" TLD
		if triad == [0, 2019653217, 0]:
			return 4272832630669137235923015693490068373911885005413996126751674003559469537065

		cache_key = '_'.join([str(t) for t in triad])
		if cache_key in self.poseidon_cache:
			return self.poseidon_cache[cache_key]

		contract = self.load_contract('Poseidon')
		output = contract.functions.poseidon(triad).call()
		self.poseidon_cache[cache_key] = output
		return output
	
	def clear_poseidon_cache(self):
		self.poseidon_cache = {}
	
	def name(self, name):
		return Name(self, name)
		
	def hash(self, _hash):
		return Hash(self, _hash)
	
	def reverse(self, key, value):
		""" 
		Takes a given Standard Key (e.g. EVM) and a value,
		and attempts to find the related name.
		"""
		pass
