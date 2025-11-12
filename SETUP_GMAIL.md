# Configuración de Gmail SMTP para Recuperación de Contraseña

## 📋 Pasos para Configurar Gmail SMTP

### 1. Activar Verificación en 2 Pasos

1. Ve a: https://myaccount.google.com/security
2. Busca **"Verificación en 2 pasos"**
3. Haz clic en **"Empezar"**
4. Sigue los pasos para activarla (necesitarás tu teléfono)

---

### 2. Generar App Password (Contraseña de Aplicación)

1. Ve a: https://myaccount.google.com/apppasswords
   - O busca "App Passwords" en la configuración de tu cuenta Google
2. Es posible que te pida iniciar sesión nuevamente
3. En "Select app" → Elige **"Mail"**
4. En "Select device" → Elige **"Other (Custom name)"**
5. Escribe: **"Notes App Backend"**
6. Haz clic en **"Generate"**
7. **⚠️ IMPORTANTE:** Copia la contraseña de 16 caracteres
   - Ejemplo: `abcd efgh ijkl mnop`
   - Solo se muestra una vez
   - Guárdala en un lugar seguro

---

### 3. Configurar Variables de Entorno

Crea o edita tu archivo `.env` (copia desde `.env.example`):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/notes_db

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=drcvcompany@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=drcvcompany@gmail.com
FRONTEND_URL=http://localhost:3000
```

**⚠️ Importante:**
- `SMTP_USER`: Tu email de Gmail completo
- `SMTP_PASSWORD`: La App Password de 16 caracteres (con o sin espacios)
- `FROM_EMAIL`: El mismo email (desde donde se enviarán los correos)
- `FRONTEND_URL`: URL de tu frontend donde está el formulario de reset

---

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Gmail SMTP usa librerías estándar de Python (`smtplib`), no necesitas instalar nada adicional.

---

### 5. Crear la Tabla en la Base de Datos

```bash
python create_tables.py
```

Esto creará la tabla `password_reset_tokens` en tu base de datos PostgreSQL.

---

### 6. Probar el Sistema

#### Iniciar el servidor:
```bash
uvicorn main:app --reload
```

#### Probar con el script de prueba:
```bash
python test_password_reset.py
```

O manualmente con cURL:

**1. Solicitar reseteo de contraseña:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@example.com"}'
```

**2. Validar token (usa el token del email):**
```bash
curl http://localhost:8000/api/v1/auth/validate-token/TOKEN_AQUI
```

**3. Resetear contraseña:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "TOKEN_AQUI",
    "new_password": "nuevaPassword123"
  }'
```

---

## 🔍 Verificar que Funciona

### En tu Email:

1. Revisa tu bandeja de entrada del email que usaste
2. Busca el email de "Recuperación de Contraseña"
3. Haz clic en el botón "Restablecer Contraseña"
4. Deberías ser redirigido a tu frontend con el token en la URL

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/forgot-password` | Solicitar reseteo (envía email) |
| GET | `/api/v1/auth/validate-token/{token}` | Validar si token es válido |
| POST | `/api/v1/auth/reset-password` | Cambiar contraseña con token |

---

## 🚨 Troubleshooting

### Error: "Username and Password not accepted"

**Causas posibles:**
1. No activaste la verificación en 2 pasos
2. Estás usando tu contraseña normal en lugar de la App Password
3. La App Password tiene espacios (quítalos o déjalos, ambos funcionan)

**Solución:**
- Verifica que la verificación en 2 pasos esté activa
- Genera una nueva App Password
- Copia la contraseña exactamente como aparece

---

### Error: "SMTPAuthenticationError"

**Solución:**
1. Verifica que `SMTP_USER` sea tu email completo
2. Verifica que `SMTP_PASSWORD` sea la App Password (no tu contraseña normal)
3. Intenta generar una nueva App Password

---

### No llega el email

**Solución:**
1. Revisa la carpeta de **SPAM/Correo no deseado**
2. Verifica que el email del usuario exista en tu base de datos
3. Revisa los logs del servidor para ver si hay errores
4. Verifica que tu conexión a internet funcione

---

### Error: "SMTPServerDisconnected"

**Solución:**
- Verifica que `SMTP_HOST=smtp.gmail.com` y `SMTP_PORT=587`
- Verifica tu conexión a internet
- Intenta reiniciar el servidor

---

### El email va a SPAM

**Solución:**
1. Marca el email como "No es spam"
2. Agrega el remitente a tus contactos
3. Para producción, considera usar un dominio propio con SPF/DKIM configurado

---

## 📈 Límites de Gmail SMTP

**Límites diarios:**
- ✅ **500 emails por día** (cuenta Gmail gratuita)
- ✅ **2,000 emails por día** (Google Workspace)
- ✅ Gratis permanentemente
- ✅ Sin costo adicional

**Si necesitas más:**
- Considera usar un servicio profesional como SendGrid, Mailgun, o Amazon SES
- O crear múltiples cuentas Gmail (no recomendado)

---

## 🔐 Seguridad

- ✅ Tokens expiran en 1 hora
- ✅ Tokens de un solo uso
- ✅ No revela si el email existe
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Email de confirmación al cambiar contraseña
- ✅ Conexión TLS/SSL segura con Gmail

---

## 💡 Tips de Producción

1. **Usa variables de entorno** - Nunca subas tu `.env` a Git
2. **Monitorea los logs** - Para detectar intentos de abuso
3. **Implementa rate limiting** - Máximo 3 intentos por hora por IP
4. **Considera un dominio propio** - Para mejor deliverability
5. **Backup de App Passwords** - Guarda la contraseña en un lugar seguro

---

## 🔄 Diferencias con SendGrid

| Característica | Gmail SMTP | SendGrid |
|----------------|------------|----------|
| Costo | Gratis | Gratis (100/día) |
| Límite diario | 500 emails | 100 emails |
| Configuración | Más simple | Más compleja |
| Deliverability | Buena | Excelente |
| Analytics | No | Sí |
| Producción | OK para MVP | Recomendado |

---

## 📚 Documentación Oficial

- Gmail SMTP: https://support.google.com/mail/answer/7126229
- App Passwords: https://support.google.com/accounts/answer/185833
- Python smtplib: https://docs.python.org/3/library/smtplib.html

---

## ✅ Checklist de Configuración

- [ ] Verificación en 2 pasos activada
- [ ] App Password generada
- [ ] Archivo `.env` configurado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Tabla `password_reset_tokens` creada
- [ ] Servidor iniciado (`uvicorn main:app --reload`)
- [ ] Email de prueba enviado y recibido
- [ ] Token validado correctamente
- [ ] Contraseña cambiada exitosamente

---

¡Listo! Tu sistema de recuperación de contraseña con Gmail SMTP está configurado. 🎉
