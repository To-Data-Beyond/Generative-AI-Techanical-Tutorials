import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import parseaddr

def send_email(sender_email, recipient_emails, subject, message, *,
               smtp_host="127.0.0.1", smtp_port=8025, username=None,
               password=None, use_starttls=False, allow_remote=False):
    recipients = list(recipient_emails)
    if not recipients:
        raise ValueError("Provide at least one recipient")
    for address in [sender_email, *recipients]:
        if not isinstance(address, str) or any(c in address for c in "\r\n"):
            raise ValueError("Invalid address")
        if parseaddr(address)[1] != address or "@" not in address:
            raise ValueError("Provide bare email addresses")
    if any(c in subject for c in "\r\n"):
        raise ValueError("Invalid subject")
    local = smtp_host in {"127.0.0.1", "::1"}
    if not local and not (allow_remote and use_starttls and username and password):
        raise ValueError("Remote email requires explicit opt-in, TLS and credentials")
    if bool(username) != bool(password):
        raise ValueError("Provide both username and password")
    mail = EmailMessage()
    mail["From"], mail["To"], mail["Subject"] = sender_email, ", ".join(recipients), subject
    mail.set_content(message)
    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
        server.ehlo()
        if use_starttls:
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
        if username:
            server.login(username, password)
        refused = server.send_message(mail, from_addr=sender_email, to_addrs=recipients)
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)
    return len(recipients)

def main():
    parser = argparse.ArgumentParser(description="Send to a local SMTP capture by default; remote delivery requires explicit opt-in.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8025)
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--starttls", action="store_true")
    parser.add_argument("--sender", default="sender@example.invalid")
    parser.add_argument("--to", nargs="+", default=["recipient@example.invalid"])
    parser.add_argument("--subject", default="Automation example")
    parser.add_argument("--message", default="Hello from the local automation tutorial.")
    args = parser.parse_args()
    try:
        count = send_email(args.sender, args.to, args.subject, args.message,
            smtp_host=args.host, smtp_port=args.port,
            username=os.getenv("SMTP_USERNAME"), password=os.getenv("SMTP_PASSWORD"),
            use_starttls=args.starttls, allow_remote=args.allow_remote)
        print(f"Accepted by SMTP capture/server: {count} recipient(s)")
    except (OSError, ValueError, smtplib.SMTPException) as exc:
        parser.exit(1, f"Email delivery failed: {exc}\n")

if __name__ == "__main__":
    main()
