import requests
import sys
import getopt
import os
import platform
import subprocess
import time

# obtener el fabricante por MAC usando la API 
def consulta_mac(mac):
    url = f'https://api.maclookup.app/v2/macs/{mac}'
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000)  # Tiempo de respuesta en milisegundos

    if response.status_code == 200:
        data = response.json()
        if 'company' in data and data['company']:  # Verifica que 'company' no sea vacio
            print(f"MAC address: {mac}")
            print(f"Fabricante: {data['company']}")
        else:
            print(f"MAC address: {mac}")
            print("Fabricante: NOT FOUND")
    else:
        print("Error al conectar con la API")
    
    print(f"Tiempo de respuesta: {response_time}ms")

# obtener las MACs del ARP y consultar el fabricante
def mostrar_arp():
    if platform.system() == "Windows":
        command = "arp -a"
    else:
        command = "arp"

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        # Procesar las MAC encontradas en la salida de ARP
        arp_output = result.stdout
        macs = extraer_macs(arp_output)
        if macs:
            for mac in macs:
                consulta_mac(mac)
        else:
            print("No se encontraron direcciones MAC en la tabla ARP.")
    else:
        print("Error al ejecutar el comando arp.")

# extraer las MAC del arp
def extraer_macs(arp_output):
    import re
    macs = re.findall(r'([0-9A-Fa-f]{2}(?:[:-][0-9A-Fa-f]{2}){5})', arp_output)
    return macs

# manejo de argumentos y ejecuta las funciones
def main(argv):
    mac_address = ''
    arp = False
    
    try:
        opts, args = getopt.getopt(argv, "ha:m:", ["help", "arp", "mac="])
    except getopt.GetoptError:
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
            sys.exit()
        elif opt in ('-m', '--mac'):
            mac_address = arg
        elif opt in ('-a', '--arp'):
            arp = True
    
    if mac_address:
        consulta_mac(mac_address)
    elif arp:
        mostrar_arp()
    else:
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')

if __name__ == "__main__":
    main(sys.argv[1:])
