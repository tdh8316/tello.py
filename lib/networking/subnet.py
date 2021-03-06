import socket

import netaddr
import netifaces


def get_subnets():
    """
    Look through the server's internet connection and
    returns subnet addresses and server ip
    :return: list[str]: subnets
             list[str]: addr_list
    """
    subnets = []
    addr_list = []
    ifaces = netifaces.interfaces()
    for this_iface in ifaces:
        addrs = netifaces.ifaddresses(this_iface)

        if socket.AF_INET not in addrs:
            continue
        # Get ipv4 stuff
        ip_info = addrs[socket.AF_INET][0]
        address = ip_info["addr"]
        netmask = ip_info["netmask"]
        # limit range of search. This will work for router subnets
        if netmask != "255.255.255.0":
            continue

        # Create IP object and get the network details
        # Note CIDR is a networking term, describing the IP/subnet address format
        cidr = netaddr.IPNetwork("{}/{}".format(address, netmask))
        network = cidr.network
        subnets.append((network, netmask))
        addr_list.append(address)

    return subnets, addr_list
