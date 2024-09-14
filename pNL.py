import os
import requests
import subprocess

# Define the interface names
interfaces = ['eth1mac0', 'eth1mac1', 'eth1mac2']
# Define the URL template, 'ipaddr' is the part that will be replaced
url_template = '...wlan_user_ip=ipaddr...'

def get_interface_ip(interface):
    try:
        result = subprocess.check_output(f"ifconfig {interface} | grep 'inet addr'", shell=True).decode()
        ip_addr = result.split()[1].split(':')[1]
        return ip_addr
    except Exception as e:
        print(f"Failed to get IP address for interface {interface}: {e}")
        return None

def ping_ip(interface, target_ip='8.8.8.8'):
    try:
        result = subprocess.run(f"ping -I {interface} -c 3 {target_ip}", shell=True, stdout=subprocess.PIPE)
        return result.returncode == 0  # Return True if ping is successful
    except Exception as e:
        print(f"Ping failed for interface {interface}: {e}")
        return False

def access_url_with_ip(interface, ip):
    url = url_template.replace('ipaddr', ip)
    try:
        response = requests.get(url)
        print(f"Accessed URL: {url}, returned status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to access URL for interface {interface}: {e}")

for interface in interfaces:
    print(f"Checking interface {interface}")
    if not ping_ip(interface):
        print(f"Interface {interface} cannot ping 8.8.8.8, attempting to access URL")
        ip = get_interface_ip(interface)
        if ip:
            access_url_with_ip(interface, ip)
        else:
            print(f"Failed to get IP for interface {interface}, skipping URL access")
    else:
        print(f"Interface {interface} can successfully ping 8.8.8.8")

