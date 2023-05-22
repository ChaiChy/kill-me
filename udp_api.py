import socket
import ipaddress
import struct

# port number for udp receive and transfer
rx_port = 3207
tx_port = 6969

# multicast stuff
MCAST_GRP = '239.255.255.250'
MCAST_PORT = 4242


def get_local_ip():

    try:
        # Create a temporary socket to connect to a remote host
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(('8.8.8.8', 80))  # Connect to a known external host

        # Get the local IP address from the connected socket
        local_ip = temp_socket.getsockname()[0]

        # Close the temporary socket
        temp_socket.close()
        return local_ip

    except socket.error:
        return None


def find_stm32():

    local_ip = get_local_ip()
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    # UDP datagram rx socket 
    rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rx_socket.bind((MCAST_GRP, MCAST_PORT))
    rx_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    rx_socket.settimeout(30)

    try:
        payload, sender_info = rx_socket.recvfrom(10)

        # sender_info is a list that contains the sender's ip and the port ip used for delivery
        stm32_ip = sender_info[0]
        return stm32_ip

    except socket.timeout:
        # no gud
        return None

    finally:
        rx_socket.close()


# probably don't need this
def get_broadcast_address(local_ip):

    subnet_mask = '255.255.255.0'
    network = ipaddress.IPv4Address(f'{local_ip}/{subnet_mask}', strict=False)
    return network.broadcast_address

def send_udp(target_ip: str, payload: int):

    if target_ip is not None:
        tx_socket = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

        try:
            tx_socket.sendto(payload, (target_ip, tx_port))
            tx_socket.close()
            return 'message was fired'
        except socket.error:
            return 'error firing message'
        finally:
            tx_socket.close()

    return 'network not found'













