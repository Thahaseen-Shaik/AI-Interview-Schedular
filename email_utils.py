import os
import re
import smtplib
import ssl
from email.message import EmailMessage

import requests
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.example")


def _first_env(*names, default=""):
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default


def _normalize_password_like_value(value):
    return re.sub(r"\s+", "", value or "")


RESEND_API_KEY = _first_env("RESEND_API_KEY", default="")
RESEND_FROM = _first_env("RESEND_FROM", default="AI Interview <onboarding@resend.dev>")
RESEND_REPLY_TO = _first_env("RESEND_REPLY_TO", "SMTP_USER", default="")
RESEND_API_URL = _first_env("RESEND_API_URL", default="https://api.resend.com/emails")
SMTP_HOST = _first_env("SMTP_HOST", default="")
SMTP_PORT = int(_first_env("SMTP_PORT", default="587") or "587")
SMTP_USERNAME = _first_env("SMTP_USERNAME", "SMTP_USER", default="")
SMTP_PASSWORD = _normalize_password_like_value(_first_env("SMTP_PASSWORD", "SMTP_PASS", "MAIL_PASSWORD", default=""))
SMTP_FROM = _first_env("SMTP_FROM", "SMTP_USERNAME", "SMTP_USER", default="")
SMTP_REPLY_TO = _first_env("SMTP_REPLY_TO", "SMTP_USER", default="")
SMTP_USE_TLS = _first_env("SMTP_USE_TLS", default="true").lower() not in {"0", "false", "no", "off"}
SMTP_USE_SSL = _first_env("SMTP_USE_SSL", "SMTP_SECURE", default="false").lower() in {"1", "true", "yes", "on"}


def _build_interview_message(to_email, candidate_name, interview_time, interview_link):
    compatibility_link = (
        interview_link.replace("/interview?", "/system-check?")
        if "/interview?" in interview_link
        else interview_link
    )
    start_link = interview_link if "mode=" in interview_link else f"{interview_link}&mode=start"
    subject = f"AI Interview Invitation - {candidate_name}"
    text = (
        f"Hello {candidate_name},\n\n"
        f"You have been invited for an AI Interview.\n"
        f"Time: {interview_time}\n\n"
        f"System Compatibility Check: {compatibility_link}\n"
        f"Start Interview: {start_link}\n"
    )
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; margin: auto; }}
            .header {{ background-color: #4A90E2; color: white; padding: 10px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 20px; }}
            .button {{ display: inline-block; padding: 10px 20px; color: white; background-color: #4A90E2; text-decoration: none; border-radius: 5px; margin-top: 15px; }}
            .button-secondary {{ display: inline-block; padding: 10px 20px; color: white; background-color: #10b981; text-decoration: none; border-radius: 5px; margin-top: 10px; }}
            .checklist {{ margin-top: 14px; padding-left: 18px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>Interview Invitation</h1></div>
            <div class="content">
                <p>Hello {candidate_name},</p>
                <p>You have been invited for an AI Interview.</p>
                <p><strong>Time:</strong> {interview_time}</p>
                <p>Please use the link below to join the interview at the scheduled time.</p>
                <p><strong>Before joining, please make sure:</strong></p>
                <ul class="checklist">
                    <li>Your camera is working and permission is allowed</li>
                    <li>Your microphone is enabled and unmuted</li>
                    <li>You use a supported browser like Chrome or Edge</li>
                    <li>You keep a stable internet connection during the interview</li>
                </ul>
                <p>When you open the interview, you will first see a System Compatibility Check page for camera, microphone, speaker, and internet support.</p>
                <p>After that, you can wait for the scheduled time and start the interview when it opens.</p>
                <p>Note that you won't be able to join before or significantly after the slot.</p>
                <a href="{compatibility_link}" class="button">System Compatibility Check</a>
                <br>
                <a href="{start_link}" class="button-secondary">Start Interview</a>
                <p>Good luck!</p>
            </div>
        </div>
    </body>
    </html>
    """

    return {
        "from": RESEND_FROM,
        "to": to_email,
        "subject": subject,
        "html": html,
        "text": text,
        "reply_to": RESEND_REPLY_TO or None,
    }


def _build_smtp_message(message):
    email_message = EmailMessage()
    email_message["Subject"] = message["subject"]
    email_message["From"] = SMTP_FROM or SMTP_USERNAME or RESEND_FROM
    email_message["To"] = message["to"]
    if SMTP_REPLY_TO or message.get("reply_to"):
        email_message["Reply-To"] = SMTP_REPLY_TO or message.get("reply_to")
    email_message.set_content(message["text"])
    email_message.add_alternative(message["html"], subtype="html")
    return email_message


def _success(provider):
    return {"ok": True, "provider": provider, "error": "", "details": ""}


def _failure(provider, error, details=""):
    return {
        "ok": False,
        "provider": provider,
        "error": error,
        "details": details or "",
    }


def _skipped(provider="none", error="Email provider is not configured.", details=""):
    return {
        "ok": None,
        "provider": provider,
        "error": error,
        "details": details or "",
    }


def _send_single_message(message):
    if RESEND_API_KEY:
        payload = {
            "from": message["from"],
            "to": [message["to"]],
            "subject": message["subject"],
            "html": message["html"],
            "text": message["text"],
        }
        if message.get("reply_to"):
            payload["reply_to"] = message["reply_to"]

        try:
            response = requests.post(
                RESEND_API_URL,
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "AI-Interview-Scheduler/1.0",
                },
                json=payload,
                timeout=30,
            )
            if response.status_code < 400:
                return _success("resend")
            details = response.text.strip()
            error = f"Resend rejected the message ({response.status_code})."
            print(f"[ERROR] Resend failed: {response.status_code} {details}")
            return _failure("resend", error, details)
        except Exception as exc:
            error = "Failed to send email via Resend."
            print(f"[ERROR] {error} {exc}")
            return _failure("resend", error, str(exc))

    if SMTP_HOST:
        try:
            smtp_message = _build_smtp_message(message)
            if SMTP_USE_SSL:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
                    if SMTP_USERNAME:
                        server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.send_message(smtp_message)
            else:
                context = ssl.create_default_context()
                with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                    if SMTP_USE_TLS:
                        server.starttls(context=context)
                    if SMTP_USERNAME:
                        server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.send_message(smtp_message)
            return _success("smtp")
        except Exception as exc:
            error = "Failed to send email via SMTP."
            print(f"[ERROR] {error} {exc}")
            return _failure("smtp", error, str(exc))

    print("[INFO] No email provider configured. Email delivery skipped.")
    print(f"Link: {message['to']}")
    return _skipped()


def send_interview_email(to_email, candidate_name, interview_time, interview_link):
    message = _build_interview_message(to_email, candidate_name, interview_time, interview_link)
    return _send_single_message(message)


def send_bulk_interview_emails(recipients):
    all_ok = True
    last_failure = None
    sent_any = False
    for recipient in recipients:
        message = _build_interview_message(
            recipient["to_email"],
            recipient["candidate_name"],
            recipient["interview_time"],
            recipient["interview_link"],
        )
        result = _send_single_message(message)
        if result.get("ok") is True:
            sent_any = True
        elif result.get("ok") is False:
            all_ok = False
            last_failure = result
    if all_ok and sent_any:
        return _success("bulk")
    if not sent_any and not RESEND_API_KEY and not SMTP_HOST:
        print("[INFO] No email provider configured. Email delivery skipped.")
        for recipient in recipients:
            print(f"Link: {recipient['to_email']}")
        return _skipped(details="No email provider is configured.")
    return last_failure or _failure("bulk", "One or more emails failed to send.")
