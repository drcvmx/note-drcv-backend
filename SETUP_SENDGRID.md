# Configuración de SendGrid para Recuperación de Contraseña

## 📋 Pasos para Configurar SendGrid

### 1. Crear Cuenta en SendGrid (GRATIS)

1. Ve a: https://signup.sendgrid.com/
2. Completa el formulario de registro
3. Verifica tu email
4. Completa el cuestionario inicial (selecciona "Free" plan)

**Plan Gratuito:**
- ✅ 100 emails por día
- ✅ Permanente (no expira)
- ✅ No requiere tarjeta de crédito

---

### 2. Obtener tu API Key

1. Inicia sesión en SendGrid
2. Ve a **Settings** → **API Keys** (https://app.sendgrid.com/settings/api_keys)
3. Haz clic en **Create API Key**
4. Nombre: `notes-app-password-reset`
5. Permisos: Selecciona **Full Access** (o solo "Mail Send")
6. Haz clic en **Create & View**
7. **⚠️ IMPORTANTE:** Copia la API Key (solo se muestra una vez)

---

### 3. Verificar tu Email de Remitente

SendGrid requiere verificar el email desde el cual enviarás correos:

#### Opción A: Single Sender Verification (Más Fácil)

1. Ve a **Settings** → **Sender Authentication** → **Single Sender Verification**
2. Haz clic en **Create New Sender**
3. Completa el formulario:
   - **From Name:** Notes App
   - **From Email Address:** tu-email@gmail.com (o cualquier email que controles)
   - **Reply To:** (mismo email)
   - Completa los demás campos
4. Haz clic en **Create**
5. Revisa tu email y haz clic en el link de verificación

#### Opción B: Domain Authentication (Más Profesional)

Si tienes un dominio propio (ej: tudominio.com):
1. Ve a **Settings** → **Sender Authentication** → **Domain Authentication**
2. Sigue el wizard para configurar DNS records
3. Esto te permite enviar desde cualquier email @tudominio.com

---

### 4. Configurar Variables de Entorno

Crea o edita tu archivo `.env`:

```env
# SendGrid Email
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=tu-email-verificado@gmail.com
FRONTEND_URL=http://localhost:3000
```

**⚠️ Importante:**
- `SENDGRID_API_KEY`: La API Key que copiaste en el paso 2
- `FROM_EMAIL`: El email que verificaste en el paso 3
- `FRONTEND_URL`: URL de tu frontend (donde está el formulario de reset)

---

### 5. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará `sendgrid==6.11.0` y todas las demás dependencias.

---

### 6. Crear la Tabla en la Base de Datos

```bash
python create_tables.py
```

Esto creará la tabla `password_reset_tokens` en tu base de datos PostgreSQL.

---

### 7. Probar el Sistema

#### Iniciar el servidor:
```bash
uvicorn main:app --reload
```

#### Probar con cURL o Postman:

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

### En SendGrid Dashboard:

1. Ve a **Activity** → **Email Activity**
2. Deberías ver los emails enviados
3. Verifica el estado: "Delivered", "Opened", etc.

### En tu Email:

1. Revisa tu bandeja de entrada
2. Busca el email de "Recuperación de Contraseña"
3. Haz clic en el botón "Restablecer Contraseña"

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/forgot-password` | Solicitar reseteo |
| GET | `/api/v1/auth/validate-token/{token}` | Validar token |
| POST | `/api/v1/auth/reset-password` | Cambiar contraseña |

---

## 🚨 Troubleshooting

### Error: "The from email does not match a verified Sender Identity"

**Solución:** Verifica que el email en `FROM_EMAIL` esté verificado en SendGrid (paso 3).

### Error: "Forbidden"

**Solución:** Verifica que tu API Key tenga permisos de "Mail Send".

### No llega el email

**Solución:**
1. Revisa la carpeta de SPAM
2. Verifica en SendGrid Activity que se envió
3. Asegúrate de que el email del usuario existe en tu BD

### Error: "Invalid API Key"

**Solución:** Verifica que copiaste correctamente la API Key en el archivo `.env`.

---

## 💡 Tips de Producción

1. **Usa un dominio propio** para mejor deliverability
2. **Configura SPF, DKIM, DMARC** (SendGrid te ayuda con esto)
3. **Monitorea el Activity Feed** para ver bounces y spam reports
4. **Implementa rate limiting** para evitar abuso
5. **Considera actualizar al plan pago** si necesitas más de 100 emails/día

---

## 📈 Límites del Plan Gratuito

- ✅ 100 emails por día
- ✅ Permanente
- ✅ Email Activity por 30 días
- ✅ Soporte por email

**Si necesitas más:**
- Essentials: $19.95/mes → 50,000 emails/mes
- Pro: $89.95/mes → 100,000 emails/mes

---

## 🔐 Seguridad

- ✅ Tokens expiran en 1 hora
- ✅ Tokens de un solo uso
- ✅ No revela si el email existe
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Email de confirmación al cambiar contraseña

---

## 📚 Documentación Oficial

- SendGrid Docs: https://docs.sendgrid.com/
- SendGrid Python: https://github.com/sendgrid/sendgrid-python
- API Reference: https://docs.sendgrid.com/api-reference/mail-send/mail-send
