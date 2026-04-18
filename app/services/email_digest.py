import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from html import escape

from dotenv import load_dotenv

load_dotenv()


def _summary_to_html(summary: str) -> str:
    lines = [line.strip() for line in summary.splitlines() if line.strip()]

    if not lines:
        return "<p>No summary available.</p>"

    items = []
    for line in lines:
        cleaned = line.removeprefix("-").removeprefix("*").strip()
        items.append(f"<li>{escape(cleaned)}</li>")

    return f"<ul>{''.join(items)}</ul>"


def _summary_to_text(summary: str) -> str:
    lines = [line.strip() for line in summary.splitlines() if line.strip()]

    if not lines:
        return "- No summary available."

    normalized = []
    for line in lines:
        cleaned = line.removeprefix("-").removeprefix("*").strip()
        normalized.append(f"- {cleaned}")

    return "\n".join(normalized)


def build_digest_email(articles):
    digest_date = datetime.now().strftime("%B %d, %Y")

    html_parts = [
        """
        <html>
          <body style="margin:0;padding:0;background-color:#f4f7fb;font-family:Arial,sans-serif;color:#1f2937;">
            <div style="max-width:720px;margin:0 auto;padding:32px 20px;">
              <div style="background:linear-gradient(135deg,#0f172a,#1d4ed8);padding:32px;border-radius:20px;color:#ffffff;">
                <p style="margin:0 0 8px;font-size:13px;letter-spacing:1px;text-transform:uppercase;opacity:0.8;">AI News Aggregator</p>
                <h1 style="margin:0;font-size:30px;line-height:1.2;">Your latest AI news digest</h1>
                <p style="margin:12px 0 0;font-size:16px;line-height:1.6;opacity:0.9;">
                  %d newly summarized article%s on %s.
                </p>
              </div>
        """
        % (len(articles), "" if len(articles) == 1 else "s", escape(digest_date))
    ]

    text_parts = [
        "AI News Aggregator",
        f"{len(articles)} newly summarized article{'' if len(articles) == 1 else 's'} on {digest_date}",
        "",
    ]

    for article in articles:
        title = escape(article.title)
        source = escape(article.source)
        url = escape(article.url)
        published_at = (
            article.published_at.strftime("%b %d, %Y")
            if article.published_at
            else "Unknown publish date"
        )

        html_parts.append(
            f"""
              <div style="background:#ffffff;margin-top:20px;padding:24px;border-radius:18px;border:1px solid #dbe4f0;box-shadow:0 8px 24px rgba(15,23,42,0.06);">
                <p style="margin:0 0 12px;font-size:12px;text-transform:uppercase;letter-spacing:0.8px;color:#2563eb;font-weight:700;">
                  {source} | {escape(published_at)}
                </p>
                <h2 style="margin:0 0 12px;font-size:22px;line-height:1.35;color:#111827;">{title}</h2>
                <div style="font-size:15px;line-height:1.7;color:#374151;">
                  {_summary_to_html(article.summary or "")}
                </div>
                <p style="margin:18px 0 0;">
                  <a href="{url}" style="display:inline-block;padding:12px 18px;background:#2563eb;color:#ffffff;text-decoration:none;border-radius:999px;font-weight:700;">
                    Read article
                  </a>
                </p>
              </div>
            """
        )

        text_parts.extend(
            [
                f"{article.title} ({article.source})",
                f"Published: {published_at}",
                _summary_to_text(article.summary or ""),
                f"Read more: {article.url}",
                "",
            ]
        )

    html_parts.append(
        """
              <p style="margin:24px 0 0;font-size:13px;line-height:1.6;color:#6b7280;text-align:center;">
                Generated automatically by your AI news pipeline.
              </p>
            </div>
          </body>
        </html>
        """
    )

    return "".join(html_parts), "\n".join(text_parts)


def send_digest_email(articles):
    if not articles:
        print("No newly summarized articles to email.")
        return False

    smtp_username = os.getenv("GMAIL_SENDER_EMAIL")
    smtp_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("DIGEST_RECIPIENT_EMAIL", smtp_username)

    missing_values = [
        name
        for name, value in {
            "GMAIL_SENDER_EMAIL": smtp_username,
            "GMAIL_APP_PASSWORD": smtp_password,
            "DIGEST_RECIPIENT_EMAIL or GMAIL_SENDER_EMAIL": recipient,
        }.items()
        if not value
    ]
    if missing_values:
        print(
            "Email digest skipped. Missing environment variables: "
            + ", ".join(missing_values)
        )
        return False

    html_body, text_body = build_digest_email(articles)

    message = EmailMessage()
    message["Subject"] = f"AI News Digest: {len(articles)} new article{'s' if len(articles) != 1 else ''}"
    message["From"] = smtp_username
    message["To"] = recipient
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(message)

    print(f"Email digest sent to {recipient}")
    return True
