import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Mailtrap SMTP credentials — set via environment variables or defaults below
SMTP_HOST = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = int(os.getenv("SMTP_PORT", "2525"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@urbanserve.com")


def send_booking_confirmation(
    to_email: str,
    to_name: str,
    provider_name: str,
    service_name: str,
    scheduled_at: str,
    booking_id: int,
) -> None:
    subject = f"Booking Confirmed — {service_name} with {provider_name}"

    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:auto;padding:24px;border:1px solid #e5e7eb;border-radius:12px;">
      <div style="text-align:center;margin-bottom:24px;">
        <span style="font-size:32px">🏙️</span>
        <h2 style="color:#4f46e5;margin:8px 0 0">UrbanServe</h2>
      </div>

      <h3 style="color:#111827">Hi {to_name},</h3>
      <p style="color:#6b7280">Your booking has been confirmed! Here are the details:</p>

      <div style="background:#f9fafb;border-radius:8px;padding:16px;margin:16px 0;">
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:6px 0;color:#6b7280;width:40%">Booking ID</td><td style="color:#111827;font-weight:600">#{booking_id}</td></tr>
          <tr><td style="padding:6px 0;color:#6b7280">Service</td><td style="color:#111827;font-weight:600">{service_name}</td></tr>
          <tr><td style="padding:6px 0;color:#6b7280">Provider</td><td style="color:#111827;font-weight:600">{provider_name}</td></tr>
          <tr><td style="padding:6px 0;color:#6b7280">Scheduled At</td><td style="color:#111827;font-weight:600">{scheduled_at}</td></tr>
          <tr><td style="padding:6px 0;color:#6b7280">Status</td><td><span style="background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:99px;font-size:12px;font-weight:600">Confirmed</span></td></tr>
        </table>
      </div>

      <p style="color:#6b7280;font-size:14px;">Thank you for using UrbanServe. If you need to cancel or reschedule, please contact support.</p>

      <div style="margin-top:24px;text-align:center;color:#9ca3af;font-size:12px;">
        © 2026 UrbanServe — All rights reserved.
      </div>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
