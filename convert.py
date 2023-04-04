#!/usr/bin/python3.8

import yaml 
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

proxyFile="sub_merge_yaml.yml"

def yaml_loader(file_name):
	d=open(file_name,"r")
	yload = yaml.load(d,Loader=Loader)
	d.close()
	return yload

read_proxy_file_yaml = yaml_loader(proxyFile)

#config
y={}
y['port'] = 7890
y['socks-port'] = 7891
y['allow-lan'] = True
y['mode'] = "Rule"
y['external-controller'] = "0.0.0.0:9090"
y['log-level'] = "debug"

y['dns'] = {
	'enables': True,
	'nameserver': ['8.8.8.8','1.1.1.1'],
	'fallback': ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']
}

y['proxies'] = read_proxy_file_yaml['proxies']

all_names = [ i['name'] for i in y['proxies'] ]

y['proxy-groups'] = [
	{
		'name': 'All Proxies',
		'type': 'select',
		'proxies': all_names
	},
	{
		'name': 'Auto Best',
		'url': 'http://t.me',
		'type': 'url-test',
		'interval': 900,
		'tolerance': 50,
		'proxies': all_names
	},
	{
		'name': 'Direct',
		'type': 'select',
		'proxies': ['DIRECT']
	},
	{
		'name': 'BLOCK',
		'type': 'select',
		'proxies': ['REJECT']
	},
]

y['rules'] = [
	'GEOIP,IR,Direct',
	'DOMAIN-SUFFIX,ir,Direct',
	'MATCH,All Proxies'
]

#write it
with open("conf.yaml","w") as f:
	f.write( yaml.dump(y) )