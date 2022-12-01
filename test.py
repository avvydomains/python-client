from web3 import Web3
from avvy import AvvyClient, exceptions
from avvy.client import Name
import unittest


REVERSE_TEST_PUBKEY = '0x650197C550B00fdD74C0F533cAf877dD39F79270'
REVERSE_TEST_PUBKEY_NOT_SET = '0x18f4Cc86D27655A6C907B79ed65a82085D5D1A43'


class ClientTestCase(unittest.TestCase):
	def _build_client(self):
		w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
		return AvvyClient(w3, 31337)
	
	def test_registrant(self):
		client = self._build_client()
		registrant = client.name('avvy-client-common-testing.avax').registrant()
		self.assertEqual(registrant[:2], '0x')
	
	def test_registrant_does_not_exist(self):
		client = self._build_client()
		registrant = client.name('avvy-client-common-doesnt-exist.avax').registrant()
		self.assertEqual(registrant, None)
		
	def test_records_loaded(self):
		client = self._build_client()
		self.assertEqual(client.RECORDS.EVM, 3)
	
	def test_name_domain_two_labels(self):
		name = Name(None, 'test.avax')
		self.assertEqual(name.domain, 'test.avax')
	
	def test_name_domain_three_labels(self):
		name = Name(None, 'sub.test.avax')
		self.assertEqual(name.domain, 'test.avax')
	
	def test_name_uppercase(self):
		name = Name(None, 'SUB.TEST.AVAX')
		self.assertEqual(name.domain, 'test.avax')
		self.assertEqual(name.name, 'sub.test.avax')
	
	def test_name_hash(self):
		client = self._build_client()
		_hash = client.utils.name_hash('avvy-client-common-testing.avax')
		self.assertEqual(_hash, 5009886810970053750228119498024191690423831754312784118430229935127343039646)
	
	def test_name_hash_cache(self):
		client = self._build_client()
		_hash = client.utils.name_hash('avvy-client-common-testing.avax')
		self.assertEqual(_hash, 5009886810970053750228119498024191690423831754312784118430229935127343039646)
		_hash = client.utils.name_hash('avvy-client-common-testing.avax')
		self.assertEqual(_hash, 5009886810970053750228119498024191690423831754312784118430229935127343039646)
	
	def test_standard_record(self):
		client = self._build_client()
		address = client.name('avvy-client-common-testing.avax').resolve(client.RECORDS.X_CHAIN)
		self.assertEqual(address, 'x-avax13fd740ykwc5peewmkcgu8r9nmnhns5gpdrgfjy')
	
	def test_standard_record_uppercase(self):
		client = self._build_client()
		address = client.name('avvy-client-common-testing.avax'.upper()).resolve(client.RECORDS.X_CHAIN)
		self.assertEqual(address, 'x-avax13fd740ykwc5peewmkcgu8r9nmnhns5gpdrgfjy')
	
	def test_custom_record(self):
		client = self._build_client()
		address = client.name('avvy-client-common-testing.avax').resolve('CUSTOM_KEY')
		self.assertEqual(address, 'CUSTOM_VALUE')
	
	def test_resolve_expired(self):
		client = self._build_client()
		with self.assertRaises(client.exceptions.DomainExpiredException):
			client.name('avvy-client-common-expired.avax').resolve(client.RECORDS.X_CHAIN)
	
	def test_resolve_no_resolver(self):
		client = self._build_client()
		with self.assertRaises(client.exceptions.ResolverNotSetException):
			client.name('avvy-client-common-no-resolver.avax').resolve(client.RECORDS.X_CHAIN)
	
	def test_hash_reverse_revealed(self):
		domain = 'avvy-client-common-testing.avax'
		client = self._build_client()
		_hash = client.utils.name_hash(domain)
		name = client.hash(_hash).lookup()
		self.assertEqual(name.name, domain)
	
	def test_hash_reverse_not_revealed(self):
		client = self._build_client()
		_hash = 1
		name = client.hash(_hash).lookup()
		self.assertEqual(name, None)
	
	def test_reverse_resolve(self):
		client = self._build_client()
		_hash = client.reverse(client.RECORDS.EVM, REVERSE_TEST_PUBKEY)
		expected = client.utils.name_hash('avvy-client-common-reverse.avax')
		self.assertEqual(_hash.hash, expected)
	
	def test_reverse_resolve_fetch_preimage(self):
		client = self._build_client()
		_hash = client.reverse(client.RECORDS.EVM, REVERSE_TEST_PUBKEY)
		name = _hash.lookup()
		self.assertEqual(name.name, 'avvy-client-common-reverse.avax')
	
	def test_reverse_resolve_no_resolver(self):
		client = self._build_client()
		with self.assertRaises(client.exceptions.ReverseResolutionNotSupportedException):
			client.reverse(client.RECORDS.X_CHAIN, REVERSE_TEST_PUBKEY)
	
	def test_reverse_resolve_not_found(self):
		client = self._build_client()
		_hash = client.reverse(client.RECORDS.EVM, REVERSE_TEST_PUBKEY_NOT_SET)
		self.assertEqual(_hash, None)
		

		

if __name__ == '__main__':
	unittest.main()
