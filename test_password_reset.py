"""
Script de prueba para el sistema de recuperación de contraseña
Ejecutar: python test_password_reset.py
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_password_reset_flow():
    """
    Prueba completa del flujo de recuperación de contraseña
    """
    print("=" * 60)
    print("TEST: Sistema de Recuperación de Contraseña")
    print("=" * 60)
    
    # 1. Solicitar reseteo de contraseña
    print("\n1️⃣  Solicitando reseteo de contraseña...")
    email = input("Ingresa el email del usuario: ")
    
    response = requests.post(
        f"{BASE_URL}/auth/forgot-password",
        json={"email": email}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code != 200:
        print("❌ Error al solicitar reseteo")
        return
    
    print("✅ Solicitud enviada. Revisa tu email.")
    
    # 2. Validar token
    print("\n2️⃣  Validando token...")
    token = input("Ingresa el token del email (o presiona Enter para saltar): ")
    
    if token:
        response = requests.get(f"{BASE_URL}/auth/validate-token/{token}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code != 200:
            print("❌ Token inválido o expirado")
            return
        
        print("✅ Token válido")
        
        # 3. Resetear contraseña
        print("\n3️⃣  Reseteando contraseña...")
        new_password = input("Ingresa la nueva contraseña (mínimo 8 caracteres): ")
        
        response = requests.post(
            f"{BASE_URL}/auth/reset-password",
            json={
                "token": token,
                "new_password": new_password
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Contraseña actualizada exitosamente")
            print("📧 Deberías recibir un email de confirmación")
        else:
            print("❌ Error al actualizar contraseña")
    
    print("\n" + "=" * 60)
    print("Test completado")
    print("=" * 60)

def test_forgot_password_only():
    """
    Prueba solo el endpoint de forgot-password
    """
    print("\n🧪 Test: Forgot Password")
    email = input("Email: ")
    
    response = requests.post(
        f"{BASE_URL}/auth/forgot-password",
        json={"email": email}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_validate_token():
    """
    Prueba solo el endpoint de validación de token
    """
    print("\n🧪 Test: Validate Token")
    token = input("Token: ")
    
    response = requests.get(f"{BASE_URL}/auth/validate-token/{token}")
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_reset_password():
    """
    Prueba solo el endpoint de reset password
    """
    print("\n🧪 Test: Reset Password")
    token = input("Token: ")
    new_password = input("Nueva contraseña: ")
    
    response = requests.post(
        f"{BASE_URL}/auth/reset-password",
        json={
            "token": token,
            "new_password": new_password
        }
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("\n🔐 Test de Recuperación de Contraseña")
    print("\nOpciones:")
    print("1. Test completo (flujo completo)")
    print("2. Solo forgot-password")
    print("3. Solo validate-token")
    print("4. Solo reset-password")
    
    opcion = input("\nSelecciona una opción (1-4): ")
    
    if opcion == "1":
        test_password_reset_flow()
    elif opcion == "2":
        test_forgot_password_only()
    elif opcion == "3":
        test_validate_token()
    elif opcion == "4":
        test_reset_password()
    else:
        print("Opción inválida")
