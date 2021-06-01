from bottle import route, run, request
import json
import os
import sys
import subprocess

DHCPD_LEASES = '/var/lib/dhcp/dhcpd.leases'
DHCPD_CONF = '/etc/dhcp/dhcpd.conf'
#DHCPD_LEASES = '/dhcp/dhcpd.leases'
#DHCPD_CONF = '/dhcp/dhcpd.conf'

@route('/addfix', method='POST')
def add_fix():
    hostname = request.forms.get('hostname')
    mac = request.forms.get('mac')
    ip = request.forms.get('ip')
    add_fix(hostname, mac, ip)
    restart_dhcpd()
    return json.dumps({'status': 'true'})

@route('/deletefix', method='POST')
def delete_fix():
    host = request.forms.get('hostname')
    mac = request.forms.get('mac')
    delete_fix(host, mac)
    restart_dhcpd()
    return json.dumps({'status': 'true'})

@route('/restart', method='POST')
def restart_dhcp():
    restart_dhcpd()
    return json.dumps({'status': 'true'})

@route('/data.json')
def index():
    free, fixed, staging = parse_dhcp_leases()
    return json.dumps({'free': free, 'fixed': fixed, 'staging': staging})

def parse_dhcp_leases():
    free = dict()
    fixed = dict()
    staging = dict()

    with open(DHCPD_LEASES, 'r') as f:
        for line in f:
            if line.startswith('lease'):
                item = read_lease(f)
                if item['binding'] == 'active':
                    staging[line.split(' ')[1]] = item
                else:
                    free[line.split(' ')[1]] = item

    with open(DHCPD_CONF, 'r') as f:
        for line in f:
            if line.startswith('host'):
                ip = ""
                item = dict(binding='fixed', hostname=line.split(' ')[1])
                for l in f:
                    if l.startswith('}'):
                        break
                    ws = l.split(' ')
                    if ws[2] in 'hardware':
                        item["mac"] = ws[4].replace(';\n', '')
                    elif ws[2] in 'fixed-address':
                        ip = ws[3].replace(';\n', '')
                fixed[ip] = item

    return free, fixed, staging

def read_lease(f):
    d = dict()
    d['has_name'] = False
    for l in f:
        if l.startswith('}'):
            break
        ws = l.split(' ')
        if ws[2] in 'starts':
            d['starts'] = ws[4] + ' ' + ws[5].replace(';\n', '')
        elif ws[2] in 'ends':
            d['ends'] = ws[4] + ' ' + ws[5].replace(';\n', '')
        elif ws[2] in 'binding':
            d['binding'] = ws[4].replace(';\n', '')
            if d['binding'] == 'active':
                d['state'] = True
            else:
                d['state'] = False
        elif ws[2] in 'hardware':
            d['mac'] = ws[4].replace(';\n', '')
        elif ws[2] in 'client-hostname':
            d['hostname'] = ws[3].replace(';\n', '').replace('"', '')
    return d

def read_dhcpd_conf():
    lines = []
    with open(DHCPD_CONF, 'r') as f:
        lines = f.readlines()
    return lines

def write_dhcpd_conf(lines):
    with open(DHCPD_CONF, 'w') as f:
        f.writelines(lines)

def add_fix(host, mac, ip):
    lines = read_dhcpd_conf()
    lines.append('host ' + host + ' {\n')
    lines.append('  hardware ethernet ' + mac + ';\n')
    lines.append('  fixed-address ' + ip + ';\n')
    lines.append('}\n')
    write_dhcpd_conf(lines)
    return

def delete_fix(host, mac):
    lines = read_dhcpd_conf()
    for i, line in enumerate(lines):
        if line.startswith('host'):
            if line.split(' ')[1] == host:
                val = lines[i+1].split(' ')[4].replace(';\n', '')
                if val == mac:
                    del lines[i:i+4]
    write_dhcpd_conf(lines)
    return

def restart_dhcpd():
    p = subprocess.Popen('systemctl restart dhcpd', shell=True,
                         cwd='.',
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         close_fds=True)
    (stdout, stdin, stderr) = (p.stdout, p.stdin, p.stderr)
    if stderr:
        return False
    return True

run(host='0.0.0.0', port=8080, debug=False)
