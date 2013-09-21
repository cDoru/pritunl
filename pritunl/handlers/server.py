from pritunl.constants import *
from pritunl.organization import Organization
import pritunl.utils as utils
from pritunl import server
import flask

def _network_not_valid():
    return utils.jsonify({
        'error': NETWORK_NOT_VALID,
        'error_msg': NETWORK_NOT_VALID_MSG,
    }, 400)

def _interface_not_valid():
        return utils.jsonify({
            'error': INTERFACE_NOT_VALID,
            'error_msg': INTERFACE_NOT_VALID_MSG,
        }, 400)

def _port_not_valid():
        return utils.jsonify({
            'error': PORT_NOT_VALID,
            'error_msg': PORT_NOT_VALID_MSG,
        }, 400)

@server.app.route('/server', methods=['POST'])
@server.app.route('/server/<server_id>', methods=['PUT'])
def server_put_post(server_id=None):
    name = flask.request.json['name'].encode()
    network = flask.request.json['network'].encode()
    interface = flask.request.json['interface'].encode()
    port = flask.request.json['port'].encode()
    protocol = flask.request.json['protocol'].encode().lower()

    network = network.split('/')
    if len(network) != 2:
        return _network_not_valid()

    address = network[0].split('.')
    if len(address) != 4:
        return _network_not_valid()
    for i, value in enumerate(address):
        try:
            address[i] = int(value)
        except ValueError:
            return _network_not_valid()
    if address[0] != 10:
        return _network_not_valid()

    if address[1] > 254 or address[1] < 0 or \
            address[2] > 254 or address[2] < 0:
        return _network_not_valid()

    if address[3] != 0:
        return _network_not_valid()

    try:
        subnet = int(network[1])
    except ValueError:
        return _network_not_valid()

    if subnet < 8 or subnet > 28:
        return _network_not_valid()

    if interface[:3] != 'tun':
        return _interface_not_valid()

    try:
        interface_num = int(interface[3:])
    except ValueError:
        return _interface_not_valid()

    if interface_num > 64:
        return _interface_not_valid()

    interface = interface[:3] + str(interface_num)

    try:
        port = int(port)
    except ValueError:
        return _port_not_valid()

    if port < 1 or port > 65535:
        return _port_not_valid()

    if protocol not in ['udp', 'tcp']:
        return utils.jsonify({
            'error': PROTOCOL_NOT_VALID,
            'error_msg': PROTOCOL_NOT_VALID_MSG,
        }, 400)

    return utils.jsonify({})