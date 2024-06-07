import threading
import socket
from pysnmp.hlapi import *
from helper import create_pdf, print_pdf
from smtp import send_report
# snmpwalk -v1 -Ont -c public 10.10.20.30

# 1.define printers across the network


def discover_printers():
    printers = []

    def discover_printer(ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                printers.append(ip)
        except (socket.timeout, socket.error):
            pass

    threads = []
    for i in range(27, 69):
        ip = f"10.10.20.{i}"
        thread = threading.Thread(target=discover_printer, args=(ip, 9100))
        threads.append(thread)
        thread.start()
        # print(threads)

    return printers


network_printers = discover_printers()
print("Network Printers:", network_printers)


def define_printer(array11):
    printers_formatted = {}
    for printer in array11:
        if printer == '10.10.20.30':
            printers_formatted[printer] = 'SOMETHING'
        else:
            print('not mentioned')
            pass
    return printers_formatted


print(define_printer(network_printers))

# 2.retrieve information from the printers (cartridge, etc .. )
# SNMP


printers_raw = define_printer(network_printers)


def printer_info(ip_address, community='public', port=161, printer_list={}):
    oid1 = '1.3.6.1.2.1.43.12.1.1.4.1.1'  # black
    oid2 = '1.3.6.1.2.1.43.12.1.1.4.1.2'  # cyan
    oid3 = '1.3.6.1.2.1.43.12.1.1.4.1.3'  # magenta
    oid4 = '1.3.6.1.2.1.43.12.1.1.4.1.4'  # yellow

    oid5 = '1.3.6.1.2.1.25.3.2.1.3.1'  # (name of a printer)

    oid6 = '1.3.6.1.2.1.43.11.1.1.9.1.1'  # black_level
    oid7 = '1.3.6.1.2.1.43.11.1.1.9.1.2'  # cyan_level
    oid8 = '1.3.6.1.2.1.43.11.1.1.9.1.3'  # magenta_level
    oid9 = '1.3.6.1.2.1.43.11.1.1.9.1.4'  # yellow_level

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip_address, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid1)),
               ObjectType(ObjectIdentity(oid2)),
               ObjectType(ObjectIdentity(oid3)),
               ObjectType(ObjectIdentity(oid4)),
               ObjectType(ObjectIdentity(oid5)),
               ObjectType(ObjectIdentity(oid6)),
               ObjectType(ObjectIdentity(oid7)),
               ObjectType(ObjectIdentity(oid8)),
               ObjectType(ObjectIdentity(oid9)),
               )
    )

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus}")
    else:
        printer_list_result = {}
        for name, val in varBinds:
            printer_list_result[name.prettyPrint()] = val.prettyPrint()
        printer_list[ip_address] = printer_list_result


dict_printers = {}

for printer in printers_raw:
    printer_info(printer, printer_list=dict_printers)

snmpv2_decode = {
    'SNMPv2-SMI::mib-2.43.12.1.1.4.1.1': 'Cartridge Color',
    'SNMPv2-SMI::mib-2.43.12.1.1.4.1.2': 'Cartridge Color',
    'SNMPv2-SMI::mib-2.43.12.1.1.4.1.3': 'Cartridge Color',
    'SNMPv2-SMI::mib-2.43.12.1.1.4.1.4': 'Cartridge Color',
    'SNMPv2-SMI::mib-2.25.3.2.1.3.1': 'Printer Name',
    'SNMPv2-SMI::mib-2.43.11.1.1.9.1.1': 'Level of Black Cartridge',
    'SNMPv2-SMI::mib-2.43.11.1.1.9.1.2': 'Level of Cyan Cartridge',
    'SNMPv2-SMI::mib-2.43.11.1.1.9.1.3': 'Level of Magenta Cartridge',
    'SNMPv2-SMI::mib-2.43.11.1.1.9.1.4': 'Level of Yellow Cartridge'
}

for ip, inner_dict in dict_printers.items():
    updated_inner_dict = {}
    for oid, value in inner_dict.items():
        new_key = snmpv2_decode.get(oid, oid)
        updated_inner_dict[new_key] = value
    dict_printers[ip] = updated_inner_dict

print(dict_printers)


# 3.generate PDF


def generate_pdf(dict_printers):
    toner_low_found = False
    printer_info_list = []

    for ip, inner_dict in dict_printers.items():
        for key, value in inner_dict.items():
            if isinstance(value, str) and value.isdigit() and int(value) <= 15:
                printer_model = inner_dict.get('Printer Name')
                if ip == 'SOMETHING':
                    ip = 'SOMETHING'
                print(f'Replace toner for {ip}: {key} is low ({value}) printer name is {printer_model}.')
                toner_low_found = True
                # break
                array = [printer_model, ip, key, "O. Narbayov"]
                printer_info_list.append(array)
                print(printer_info_list)

    if toner_low_found:
        create_pdf('report.pdf', printer_info_list)
        print_pdf('report.pdf', "HP_LaserJet_500_color_M551_15E8B4_")
        send_report('report.pdf')

    else:
        print("All systems are working!")


# # Пример использования
generate_pdf(dict_printers)



