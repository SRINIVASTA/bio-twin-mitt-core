# src/mitt_core/infrastructure/notifier.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

class EnterpriseNotificationService:
    """
    Production-grade notification middleware handling regular cron-style digests
    and automated operational tracking summaries over validated SMTP channels.
    """
    
    @st.cache_data(ttl=60)
    def build_summary_table(latest_parameters: dict) -> str:
        """Generates a clean HTML table displaying current parameter statuses."""
        rows = "".join([
            f"<tr><td style='padding: 8px; border-bottom: 1px solid #ddd;'><b>{k}</b></td>"
            f"<td style='padding: 8px; border-bottom: 1px solid #ddd; text-align: right;'>{v:.3f}</td></tr>"
            for k, v in latest_parameters.items()
        ])
        return f"<table style='width: 100%; border-collapse: collapse;'>{rows}</table>"

    @staticmethod
    def dispatch_hybrid_alert(report_markdown: str, alarm_type: str, latest_parameters: dict, is_emergency: bool = False, time_to_breach: float = None) -> bool:
        """
        Routes either routine digests or immediate trajectory breach warnings to stakeholders.
        """
        try:
            # Check for secrets block presence matching your working schema parameters
            if "gmail" not in st.secrets:
                st.error("⚠️ Notification Layer Failed: [gmail] config block missing from secrets.toml.")
                return False
                
            gmail_secrets = st.secrets["gmail"]
            
            # 👇 FIXED MAPS: Adjusted to use your proven, working secrets keys
            email_sender = gmail_secrets["username"]
            app_password = gmail_secrets["app_password"]
            
            # Use recipients array if present, fallback cleanly to your sender if not declared
            recipient_list = gmail_secrets.get("RECIPIENTS", [email_sender])
            if isinstance(recipient_list, str):
                recipient_list = [e.strip() for e in recipient_list.split(",") if e.strip()]

            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            # Assemble cross-platform multipart container
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = ", ".join(recipient_list)
            
            # Structural assignment depending on whether an override or periodic ticket triggered
            if is_emergency:
                time_context = f"within {time_to_breach:.1f} mins" if time_to_breach else "Imminent"
                msg['Subject'] = f"🚨 GxP CRITICAL BOUNDARY RISK: {alarm_type} Anomaly Expected {time_context}!"
                banner_color = "#f8d7da"
                text_color = "#721c24"
                border_color = "#dc2626"
                header_title = "🔮 Predictive Early-Intervention Emergency Overrides"
                sub_text = "CRITICAL ACTION REQUIRED: The forecasting engine has identified an immediate boundary collapse trajectory."
            else:
                msg['Subject'] = f"📝 [MANUAL SNAPSHOT] {alarm_type}"
                banner_color = "#f0fdf4" if "STABLE" in alarm_type else "#fff5f5"
                text_color = "#166534" if "STABLE" in alarm_type else "#991b1b"
                border_color = "#16a34a" if "STABLE" in alarm_type else "#dc2626"
                header_title = "📋 Manual Process Performance Summary Snapshot"
                sub_text = "Continuous automated telemetry analytics insight transmission packet."

            param_table = EnterpriseNotificationService.build_summary_table(latest_parameters)
            
            body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
                <div style="background-color: {banner_color}; padding: 15px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid {border_color};">
                    <h2 style="color: {text_color}; margin: 0; font-size: 18px;">{header_title}</h2>
                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #475569;">{sub_text}</p>
                </div>
            """

            if is_emergency and time_to_breach is not None:
                body += f"""
                <p style="font-size: 15px;"><strong>Estimated Window Remaining Before Boundary Cross:</strong> 
                   <span style="color: #d9534f; font-weight: bold; background-color: #ffeef0; padding: 4px 8px; border-radius: 4px;">
                     {time_to_breach:.2f} Minutes
                   </span>
                </p>
                """

            body += f"""
                <h3 style="color: #1e293b; margin-top: 15px;">📋 Snapshot Parameters Metrics:</h3>
                {param_table}
                
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;" />
                <h3 style="color: #1e293b;">🤖 Digital Twin AI Diagnostics & SOP Actions:</h3>
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; font-family: monospace; white-space: pre-wrap; font-size: 13px; border-radius: 4px; color: #334155;">
{report_markdown}
                </div>
                <p style="font-size: 11px; color: #94a3b8; text-align: center; margin-top: 25px;">
                    <em>This message was systematically compiled by bio-twin-mitt-core hybrid alert infrastructure.</em>
                </p>
              </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))

            # Establish explicit connection matching your working code structures
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() 
            server.login(email_sender, app_password)
            server.sendmail(email_sender, recipient_list, msg.as_string())
            server.quit()
            
            return True

        except Exception as e:
            # Force the raw network error to pop up right on your active dashboard screen if it slips
            st.error(f"🚨 SMTP Transmission Layer Faulted: {str(e)}")
            return False
