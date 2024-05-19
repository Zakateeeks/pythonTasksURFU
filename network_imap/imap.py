import argparse
import getpass
import re
import selectors
import socket
import ssl
from email.header import decode_header


def decode_str(encoded_header):
    """Decode a MIME-encoded string.

    Args:
        encoded_header (str): The MIME-encoded string.

    Returns:
        str: The decoded string.
    """
    decoded_parts = []
    for part, encoding in decode_header(encoded_header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)


def create_socket(server, ssl_enabled):
    """Create and connect a socket to the server.

    Args:
        server (str): The server address.
        ssl_enabled (bool): Whether to use SSL.

    Returns:
        socket.socket: The connected socket.
    """
    port = 993 if ssl_enabled else 143
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if ssl_enabled:
        context = ssl.create_default_context()
        imap_server = context.wrap_socket(raw_socket, server_hostname=server)
    else:
        imap_server = raw_socket
    try:
        imap_server.connect((server, port))
    except Exception as e:
        raise ConnectionError(f"Error connecting to {server}:{port} - {e}")
    return imap_server


def login_to_server(imap_server, user, password):
    """Login to the IMAP server.

    Args:
        imap_server (socket.socket): The connected socket.
        user (str): Username.
        password (str): Password.

    Returns:
        bool: True if login successful, else False.
    """
    login_command = f'A01 LOGIN "{user}" "{password}"\r\n'
    imap_server.sendall(login_command.encode())
    response = imap_server.recv(1024).decode()
    return 'OK' in response


def list_folders(imap_server):
    """List folders in the IMAP server.

    Args:
        imap_server (socket.socket): The connected socket.

    Returns:
        bool: True if folder list retrieval successful, else False.
    """
    imap_server.sendall(b'A02 LIST "" *\r\n')
    response = imap_server.recv(4096).decode()
    return 'LIST' in response


def select_inbox(imap_server):
    """Select the INBOX folder.

    Args:
        imap_server (socket.socket): The connected socket.

    Returns:
        bool: True if INBOX selection successful, else False.
    """
    imap_server.sendall(b'A03 SELECT INBOX\r\n')
    response = imap_server.recv(1024).decode()
    return 'INBOX' in response


def fetch_data(imap_server, command):
    """Fetch data from the IMAP server based on the provided command.

    Args:
        imap_server (socket.socket): The connected socket.
        command (str): The IMAP command to fetch data.

    Returns:
        str: The response data.
    """
    selector = selectors.DefaultSelector()
    selector.register(imap_server, selectors.EVENT_READ)
    imap_server.sendall(command.encode())
    data = b''
    while True:
        events = selector.select(timeout=1)
        for key, mask in events:
            data += key.fileobj.recv(4096)
            if not data:
                break
        if not events:
            break
    return data.decode()


def parse_fetch_response(data):
    """Parse the fetch response from the IMAP server.

    Args:
        data (str): The fetch response data.

    Returns:
        list: List of email details extracted from the response.
    """
    if ' NO ' in data:
        raise ValueError("Error fetching emails")

    msgs = []
    for line in data.split('*'):
        if "FETCH" not in line:
            continue
        matches = re.findall('([^"]+)', decode_str(line))
        if matches:
            numb = line[1] + line[2]
            date = matches[1]
            them = matches[3]
            name = matches[5]
            domain = f'{matches[7]}@{matches[9]}'
            msgs.append([numb, date[:26], them, name, domain])
    return msgs


def fetch_email_headers(server, user, password, ssl_enabled=True,
                        start='1', end='*'):
    """Fetch email headers from the server.

    Args:
        server (str): The server address.
        user (str): The username.
        password (str): The password.
        ssl_enabled (bool): Whether SSL is enabled.
        start (str): The starting email index.
        end (str): The ending email index.
    """
    try:
        imap_server = create_socket(server, ssl_enabled)
    except ConnectionError as e:
        print(e)
        return

    if not login_to_server(imap_server, user, password):
        print("Login failed. Please check your credentials or enable IMAP.")
        return

    if not list_folders(imap_server):
        print("Failed to retrieve list of folders.")
        return

    if not select_inbox(imap_server):
        print("Failed to select INBOX.")
        return

    data = fetch_data(imap_server, f'A04 FETCH {start}:{end} (ENVELOPE)\r\n')
    msgs = parse_fetch_response(data)

    data = fetch_data(imap_server, f'A05 FETCH {start}:{end}'
                                   f' (RFC822.SIZE)\r\n')
    for i, subj in enumerate(data.split('*')):
        if ' OK ' not in subj:
            for field in msgs[i]:
                print(field)
            print(subj[subj.find('SIZE') + 5:-3] + ' bytes')
            print()

    imap_server.sendall(b'A06 LOGOUT\r\n')
    response = imap_server.recv(1024).decode('utf-8')
    print(f"Logout response: {response}")  # Debug print


def main():
    parser = argparse.ArgumentParser(description='Retrieve information about emails '
                                                 'in a mailbox.')
    parser.add_argument('-s', '--server', required=True,
                        help='IMAP server address in the format address[:port]'
                             ' (default port is 143).')
    parser.add_argument('-u', '--user', required=True, help='Username.')
    parser.add_argument('--ssl', action='store_true', default=True, help='Use SSL.')
    parser.add_argument('-n', nargs='+', type=int, help='Range of emails. Format:'
                                                        ' N1 [N2]. Default is all emails.')
    args = parser.parse_args()

    password = getpass.getpass('Password: ')

    start = args.n[0] if args.n else '1'
    end = args.n[1] if args.n and len(args.n) == 2 else '*'

    fetch_email_headers(args.server, args.user, password, args.ssl, start, end)


if __name__ == '__main__':
    main()
