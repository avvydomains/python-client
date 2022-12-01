import os
import json

client_common_dir = os.environ.get('AVVY_CLIENT_COMMON', 'client-common')

# write contracts.json
contracts_dir = f'{client_common_dir}/contracts'
files = os.listdir(contracts_dir)
chains = {}
for ff in files:
	with open(f'{contracts_dir}/{ff}') as f:
		chain_data = json.loads(f.read())
	chain_id = ff.replace('.json', '')
	chains[chain_id] = chain_data
with open('avvy/contracts.py', 'w') as f:
	f.write('contract_data = ' + str(chains))

# write records.json
with open(f'{client_common_dir}/records/records.json') as f:
	records = json.loads(f.read())
with open('avvy/records.py', 'w') as f:
	f.write('record_data = ' + str(records))
