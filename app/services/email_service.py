import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    Servicio para envío de emails usando Gmail SMTP
    """
    
    @staticmethod
    def _send_email(to_email: str, subject: str, html_content: str) -> bool:
        """
        Método privado para enviar emails usando Gmail SMTP
        
        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            html_content: Contenido HTML del email
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.FROM_EMAIL
            message["To"] = to_email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Conectar al servidor SMTP de Gmail
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()  # Iniciar conexión segura
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(message)
            
            logger.info(f"Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str, username: str) -> bool:
        """
        Envía un email con el link para resetear la contraseña
        
        Args:
            to_email: Email del destinatario
            reset_token: Token de reseteo generado
            username: Nombre de usuario
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        # Construir el link de reseteo
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        # Contenido del email
        subject = "Recuperación de Contraseña - Notes App"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4F46E5; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #4F46E5; color: white !important; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                .warning {{ background-color: #FEF3C7; padding: 15px; border-left: 4px solid #F59E0B; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Recuperación de Contraseña</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{username}</strong>,</p>
                    
                    <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en DRCV NOTE.</p>
                    
                    <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">Restablecer Contraseña</a>
                    </div>
                    
                    <p>O copia y pega este enlace en tu navegador:</p>
                    <p style="word-break: break-all; color: #4F46E5;">{reset_link}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Importante:</strong>
                        <ul>
                            <li>Este enlace expirará en <strong>1 hora</strong></li>
                            <li>Solo puede ser usado <strong>una vez</strong></li>
                            <li>Si no solicitaste este cambio, ignora este email</li>
                        </ul>
                    </div>
                    
                    <p>Si tienes problemas, contacta a nuestro equipo de soporte.</p>
                    
                    <p>Saludos,<br><strong>El equipo de DRCV NOTE</strong></p>
                </div>
                <div class="footer">
                    <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(to_email, subject, html_content)
    
    @staticmethod
    def send_password_changed_confirmation(to_email: str, username: str) -> bool:
        """
        Envía un email de confirmación cuando la contraseña fue cambiada exitosamente
        
        Args:
            to_email: Email del destinatario
            username: Nombre de usuario
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        subject = "Contraseña Cambiada Exitosamente - Notes App"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #10B981; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }}
                .success {{ background-color: #D1FAE5; padding: 15px; border-left: 4px solid #10B981; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✓ Contraseña Actualizada</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{username}</strong>,</p>
                    
                    <div class="success">
                        <p><strong>Tu contraseña ha sido cambiada exitosamente.</strong></p>
                    </div>
                    
                    <p>Si realizaste este cambio, no necesitas hacer nada más. Ya puedes iniciar sesión con tu nueva contraseña.</p>
                    
                    <p><strong>⚠️ ¿No fuiste tú?</strong></p>
                    <p>Si no realizaste este cambio, tu cuenta podría estar comprometida. Por favor, contacta inmediatamente a nuestro equipo de soporte.</p>
                    
                    <p>Saludos,<br><strong>El equipo de Notes App</strong></p>
                </div>
                <div class="footer">
                    <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(to_email, subject, html_content)
