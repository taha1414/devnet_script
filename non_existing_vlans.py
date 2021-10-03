from genie.testbed import load
testbed = load('testbed1.yml')


dev = testbed.devices['dist-sw01']
dev.connect()


output1 = dev.parse('show interface switchport')
trunk_vlans_list=[data['trunk_vlans'] for intf, data in output1.items()]
trunk_vlans_list={intf:list(map(str, sum(((list(range(*[int(b) + c for c, b in enumerate(a.split('-'))])) if '-' in a else [int(a)]) for a in data['trunk_vlans'].split(',')), []))) for intf, data in output1.items() if data['trunk_vlans'] != "1-4094"}


output=dev.parse('show vlan')
vlans_list=[vlan for vlan in output['vlans']]


remove_vlans = {intf:list(set(data)-set(vlans_list)) for intf, data in trunk_vlans_list.items()}


for intf , data in remove_vlans.items():
    dev.configure(f'interface {intf}\nswitchport trunk allowed vlan remove ' + ','.join(map(str, data)))