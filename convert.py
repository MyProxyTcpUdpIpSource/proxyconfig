#!/usr/bin/python3.8

import re
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


y['proxy-groups'] = [
	{
		'name': 'All Proxies',
		'type': 'select',
		'proxies': []
	},
	{
		'name': 'Auto Best',
		'url': 'http://t.me',
		'type': 'url-test',
		'interval': 900,
		'tolerance': 50,
		'proxies': []
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

proxy_groups={}

for each_proxy in y['proxies'] :
	p_type = each_proxy['type']
	p_4byteName = re.findall( '[^0-9a-zA-z\-\.\_]+' , each_proxy['name'] )[0]
	group_name = f"{p_type} {p_4byteName}"

	if ( not (group_name in proxy_groups) ):

		proxy_groups[ group_name ] = {
			'name': group_name ,
			'type': 'select' ,
			'proxies' : []
		}

		y['proxy-groups'][0]['proxies'].append( group_name )
		y['proxy-groups'][1]['proxies'].append( group_name )

		y['proxy-groups'].append( proxy_groups[ group_name ] )

	proxy_groups[ group_name ]["proxies"].append( each_proxy['name'] )



y['rules'] = [
	'GEOIP,IR,Direct',
	'DOMAIN-SUFFIX,ir,Direct',
	'MATCH,All Proxies'
]

#write it
with open("conf.yaml","w") as f:
	f.write( yaml.dump(y) )

