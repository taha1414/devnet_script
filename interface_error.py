
from genie.testbed import load
testbed = load('testbed1.yml')
import csv

dev = testbed.devices['dist-sw01']
dev.connect(log_stdout=False)

output = dev.parse('show interface')

interface_file = "interface.csv"
report_fields = ['Interface', 'CRC', 'input_error', 'output_error']

modify_output = {intf:[data.get('counters').get('in_crc_errors'), data.get('counters').get('in_errors'), data.get('counters').get('out_errors')] for intf, data in output.items() if data.get('counters') != None}
modify_output = {intf:data for intf, data in modify_output.items() if data[0] != None}


threshold_output ={intf:data for intf, data in modify_output.items() if data[0]>0 or data[1]>0 or data[2]>0}


with open(interface_file,'w') as f:
    writer = csv.DictWriter(f, report_fields)
    writer.writeheader()

    for intf, data in threshold_output.items():
        writer.writerow({
            'Interface': intf,
            'CRC': data[0],
            'input_error': data[1],
            'output_error': data[2]
        })



# table_data = []

# for intf, data in output.items():
#          counters = data.get('counters')
#          if counters:
#              table_row=[]
#              if 'in_crc_errors' in counters:
#                  table_row.append(intf)
#                  table_row.append(str(counters['in_crc_errors']))
#              else:
#                  table_row.append(intf)
#                  table_row.append('N/A')
#              table_data.append(table_row)

# print(tabulate(table_data, headers=['Interface', 'CRC Errors Counter'], tablefmt='orgtbl'))
