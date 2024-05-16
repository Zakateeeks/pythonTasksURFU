import imaplib
import email
import argparse
import getpass
from email.header import decode_header


def decode_str(s):
    """Decode a string."""
    return ' '.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part for part, encoding in decode_header(s))


def fetch_email_headers(server, user, password, ssl=False, start=1, end=None):
    """Fetch email headers."""
    if ssl:
        imap_server = imaplib.IMAP4_SSL(server)
    else:
        imap_server = imaplib.IMAP4(server)

    imap_server.login(user, password)
    imap_server.select('INBOX')

    if not end:
        end = start

    typ, data = imap_server.fetch(f'{start}:{end}', '(RFC822.HEADER)')
    if typ == 'OK':
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                headers = {
                    'To': decode_str(msg['To']),
                    'From': decode_str(msg['From']),
                    'Subject': decode_str(msg['Subject']),
                    'Date': decode_str(msg['Date']),
                    'Size': len(response_part[1])
                }
                print(headers)
    imap_server.close()
    imap_server.logout()


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
