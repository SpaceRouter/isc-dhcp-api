#!/usr/bin/env python

from bottle import route, run, request, response
import json
import os
import subprocess

DHCPD_LEASES    = os.environ['DHCPD_LEASES']
DHCPD_CONF      = os.environ['DHCPD_CONF']

def enable_cors(fn):
  def _enable_cors(*args, **kwargs):
      response.content_type = 'application/json'
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
      response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if request.method != 'OPTIONS':
          # actual request; reply with the actual response
          return fn(*args, **kwargs)

  return _enable_cors

@route('/dhcp/leases')
@enable_cors
def index():
    free, fixed, staging = parse_dhcp_leases()
    response.status = 200
    return json.dumps({'free': free, 'fixed': fixed, 'staging': staging})

@route('/dhcp/scope')
@enable_cors
def scope():
    scope = parse_dhcp_scope()
    response.status = 200
    return json.dumps({'scope': scope})

@route('/dhcp/addfix', method=['POST','OPTIONS'])
@enable_cors
def add_fix():
    data = request.json
    hostname = data['hostname']
    mac = data['mac']
    ip = data['ip']

    add_fix(hostname, mac, ip)
    restart_dhcpd()
    response.status = 200
    return json.dumps({'status': True})

@route('/dhcp/deletefix', method=['POST','OPTIONS'])
@enable_cors
def delete_fix():
    data = request.json
    hostname = data['hostname']
    mac = data['mac']

    delete_fix(hostname, mac)
    restart_dhcpd()
    response.status = 200
    return json.dumps({'status': True})

@route('/dhcp/restart', method=['POST','OPTIONS'])
@enable_cors
def restart_dhcp():
    restart_dhcpd()
    response.status = 200
    return json.dumps({'status': True})

def parse_dhcp_leases():
    free = []
    fixed = []
    staging = []

    with open(DHCPD_LEASES, 'r') as f:
        for line in f:
            if line.startswith('lease'):
                lease_ip = line.split(' ')[1]
                item = read_lease(f, lease_ip)
                if item['binding'] == 'active':
                    staging.append(item)
                else:
                    free.append(item)

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
                        item["ip"] = ws[3].replace(';\n', '')
                fixed.append(item)

    return free, fixed, staging

def parse_dhcp_scope():
    scope = []

    with open(DHCPD_CONF, 'r') as f:
        for line in f:
            if line.startswith('subnet'):
                item = dict(scope=line.split(' ')[1])
                for l in f:
                    if l.startswith('}'):
                        break
                    ws = l.split(' ')
                    if ws[2] in 'range':
                        item["start"] = ws[3]
                        item["end"] = ws[4].replace(';\n', '')
                    elif ws[3] in 'subnet-mask':
                        item["subnet-mask"] = ws[4].replace(';\n', '')
                    elif ws[3] in 'broadcast-address':
                        item["broadcast-address"] = ws[4].replace(';\n', '')
                    elif ws[3] in 'domain-name':
                        item["domain-name"] = ws[4].replace('"', '').replace(';\n', '')
                    elif ws[3] in 'domain-name-servers':
                        item["domain-name-servers"] = ws[4].replace(';\n', '')
                scope.append(item)

    return scope

def read_lease(f, ip):
    d = dict()
    for l in f:
        if l.startswith('}'):
            break
        ws = l.split(' ')
        d['ip'] = ip
        if ws[2] in 'starts':
            d['starts'] = ws[4] + ' ' + ws[5].replace(';\n', '')
        elif ws[2] in 'ends':
            d['ends'] = ws[4] + ' ' + ws[5].replace(';\n', '')
        elif ws[2] in 'binding':
            d['binding'] = ws[4].replace(';\n', '')
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
    p = subprocess.Popen('systemctl restart dhcpd', shell=True, cwd='.', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    (stdout, stdin, stderr) = (p.stdout, p.stdin, p.stderr)
    if stderr:
        return False
    return True

run(host='0.0.0.0', port=8080, debug=False)
