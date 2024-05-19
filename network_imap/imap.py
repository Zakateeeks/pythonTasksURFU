import socket
import ssl
import argparse
import getpass
from email.header import decode_header

def decode_str(encoded_header):
    """Decode a MIME-encoded string."""
    decoded_parts = []
    for part, encoding in decode_header(encoded_header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)

def fetch_email_headers(server, user, password, ssl_enabled=True, start=1, end=None):
    """Fetch email headers from the server."""
    port = 993 if ssl_enabled else 143

    # Create socket and wrap it with SSL if needed
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if ssl_enabled:
        context = ssl.create_default_context()
        imap_server = context.wrap_socket(raw_socket, server_hostname=server)
    else:
        imap_server = raw_socket

    try:
        imap_server.connect((server, port))
    except Exception as e:
        print(f"Error connecting to {server}:{port} - {e}")
        return

    # Login
    login_command = f'A01 LOGIN "{user}" "{password}"\r\n'
    imap_server.sendall(login_command.encode())
    response = imap_server.recv(1024).decode()
    print(f"Login response: {response}")  # Debug print
    if 'OK' not in response:
        print("Login failed. Please check your credentials or enable IMAP.")
        return

    # List folders
    imap_server.sendall(b'A02 LIST "" "*"\r\n')
    response = imap_server.recv(4096).decode()
    print(f"List response: {response}")  # Debug print
    if 'LIST' not in response:
        print("Failed to retrieve list of folders.")
        return

    # Check INBOX availability
    if 'INBOX' not in response:
        print("INBOX folder not found.")
        return

    # Select INBOX
    imap_server.sendall(b'A03 SELECT INBOX\r\n')
    response = imap_server.recv(1024).decode('utf-8')
    print(f"Select response: {response}")  # Debug print
    if 'OK' not in response:
        print("Failed to select INBOX.")
        return

    # Fetch emails
    if not end:
        end = start
    fetch_command = f'A04 FETCH {start}:{end} (RFC822.HEADER)\r\n'
    imap_server.sendall(fetch_command.encode('utf-8'))
    response = imap_server.recv(4096).decode('utf-8')
    print(f"Fetch response: {response}")  # Debug print

    # Process headers
    headers = {}
    for line in response.splitlines():
        if line.startswith('To:'):
            headers['To'] = decode_str(line.split(':', 1)[1].strip())
        elif line.startswith('From:'):
            headers['From'] = decode_str(line.split(':', 1)[1].strip())
        elif line.startswith('Subject:'):
            headers['Subject'] = decode_str(line.split(':', 1)[1].strip())
        elif line.startswith('Date:'):
            headers['Date'] = decode_str(line.split(':', 1)[1].strip())
        elif 'RFC822.HEADER' in line:
            headers['Size'] = len(line.encode('utf-8'))
            print(headers)

    # Logout
    imap_server.sendall(b'A05 LOGOUT\r\n')
    response = imap_server.recv(1024).decode('utf-8')
    print(f"Logout response: {response}")  # Debug print

def main():
    parser = argparse.ArgumentParser(description='Retrieve information about emails in a mailbox.')
    parser.add_argument('-s', '--server', required=True, help='IMAP server address in the format address[:port] (default port is 143).')
    parser.add_argument('-u', '--user', required=True, help='Username.')
    parser.add_argument('--ssl', action='store_true', default=True, help='Use SSL.')
    parser.add_argument('-n', nargs='+', type=int, help='Range of emails. Format: N1 [N2]. Default is all emails.')
    args = parser.parse_args()

    password = getpass.getpass('Password: ')

    start = args.n[0] if args.n else 1
    end = args.n[1] if args.n and len(args.n) == 2 else None

    fetch_email_headers(args.server, args.user, password, args.ssl, start, end)

if __name__ == '__main__':
    main()
