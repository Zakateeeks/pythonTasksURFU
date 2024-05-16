import socket
import ssl
import argparse
import getpass
from email.header import decode_header


def decode_str(s):
    """Decode a string."""
    return ' '.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part for part, encoding in decode_header(s))


def fetch_email_headers(server, user, password, ssl_enabled=False, start=1, end=None):
    """Fetch email headers."""
    if ssl_enabled:
        imap_server = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    else:
        imap_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    imap_server.connect((server, 993 if ssl_enabled else 143))

    # Send login command
    imap_server.sendall(bytes(f'LOGIN {user} {password}\r\n', 'utf-8'))

    # Receive response
    response = imap_server.recv(1024).decode('utf-8')
    if not response.startswith('* OK'):
        print("Login failed. Please check your credentials.")
        return

    # Send LIST command to get a list of available folders
    imap_server.sendall(b'LIST "" *\r\n')

    # Receive response
    response = imap_server.recv(4096).decode('utf-8')
    print(response)
    if not response.startswith('* LIST'):
        print("Failed to retrieve list of folders.")
        return

    # Check if INBOX is available
    if 'INBOX' not in response:
        print("INBOX folder not found.")
        return

    # Send SELECT command
    imap_server.sendall(b'SELECT INBOX\r\n')

    # Receive response
    response = imap_server.recv(1024).decode('utf-8')
    if not response.startswith('* OK'):
        print("Failed to select INBOX.")
        return

    if not end:
        end = start

    # Send FETCH command
    imap_server.sendall(bytes(f'FETCH {start}:{end} RFC822.HEADER\r\n', 'utf-8'))

    # Receive response
    response = imap_server.recv(4096).decode('utf-8')

    # Process response
    for line in response.splitlines():
        if line.startswith('To:'):
            to_header = line.split(':', 1)[1].strip()
        elif line.startswith('From:'):
            from_header = line.split(':', 1)[1].strip()
        elif line.startswith('Subject:'):
            subject_header = line.split(':', 1)[1].strip()
        elif line.startswith('Date:'):
            date_header = line.split(':', 1)[1].strip()
        elif line.startswith('RFC822.HEADER'):
            headers = {
                'To': decode_str(to_header),
                'From': decode_str(from_header),
                'Subject': decode_str(subject_header),
                'Date': decode_str(date_header),
                'Size': len(line.encode('utf-8'))
            }
            print(headers)

    imap_server.close()


def main():
    parser = argparse.ArgumentParser(description='Retrieve information about emails in a mailbox.')
    parser.add_argument('-s', '--server', required=True,
                        help='IMAP server address in the format address[:port] (default port is 143).')
    parser.add_argument('-u', '--user', required=True, help='Username.')
    parser.add_argument('--ssl', action='store_true', help='Use SSL.')
    parser.add_argument('-n', nargs='+', type=int, help='Range of emails. Format: N1 [N2]. Default is all emails.')
    args = parser.parse_args()

    password = getpass.getpass('Password: ')

    start = args.n[0] if args.n else 1
    end = args.n[1] if args.n and len(args.n) == 2 else None

    fetch_email_headers(args.server, args.user, password, args.ssl, start, end)


if __name__ == '__main__':
    main()
