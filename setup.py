#!/usr/bin/env python3
"""
Script de configuración inicial para YouTube IA Automate.
Configura el entorno, verifica dependencias y prepara APIs.
"""

import os
import sys
import json
from pathlib import Path
import subprocess
import argparse
from typing import Dict, List

def print_banner():
    """Imprime el banner de bienvenida."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    YouTube IA Automate                       ║
║              Setup & Configuration Tool                      ║
║                                                              ║
║  🤖 Automatización completa para canales de YouTube         ║
║  📺 TOP 10 y Curiosidades en Español                        ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version() -> bool:
    """Verifica la versión de Python."""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_dependencies() -> bool:
    """Instala las dependencias necesarias."""
    
    print("\n📦 Instalando dependencias...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print("💡 Intenta ejecutar: pip install -r requirements.txt")
        return False

def setup_environment_file() -> bool:
    """Configura el archivo .env."""
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    if not env_example.exists():
        print("❌ Error: .env.example no encontrado")
        return False
    
    try:
        # Copiar ejemplo a .env
        with open(env_example, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo .env creado desde .env.example")
        print("📝 Edita .env con tus credenciales de API")
        return True
        
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def create_directories() -> bool:
    """Crea los directorios necesarios."""
    
    directories = [
        "data",
        "output",
        "output/videos",
        "output/temp",
        "assets",
        "assets/images",
        "assets/audio",
        "config"
    ]
    
    print("\n📁 Creando directorios...")
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directorios creados")
    return True

def setup_api_guide() -> None:
    """Muestra guía para configurar APIs."""
    
    guide = """
🔧 CONFIGURACIÓN DE APIs NECESARIAS

1. OPENAI API (Obligatorio)
   • Ve a: https://platform.openai.com/api-keys
   • Crea una nueva API key
   • Añádela como OPENAI_API_KEY en .env
   • Costo estimado: $10-30/mes

2. YOUTUBE API (Obligatorio para subir)
   • Ve a: https://console.developers.google.com/
   • Habilita YouTube Data API v3
   • Crea credenciales OAuth 2.0
   • Descarga el archivo JSON como 'config/youtube_credentials.json'

3. ELEVENLABS (Opcional - TTS premium)
   • Ve a: https://elevenlabs.io
   • Obtén tu API key
   • Añádela como ELEVENLABS_API_KEY en .env
   • Alternativa gratuita: Edge TTS (incluido)

4. UNSPLASH (Opcional - imágenes)
   • Ve a: https://unsplash.com/developers
   • Crea una aplicación
   • Obtén Access Key y Secret Key
   • Alternativa: imágenes generadas automáticamente

📚 Documentación completa: README.md
    """
    
    print(guide)

def validate_setup() -> Dict[str, bool]:
    """Valida la configuración actual."""
    
    print("\n🔍 Validando configuración...")
    
    checks = {
        ".env exists": Path(".env").exists(),
        "data directory": Path("data").exists(),
        "output directory": Path("output").exists(),
        "config directory": Path("config").exists(),
        "requirements.txt": Path("requirements.txt").exists(),
        "main.py": Path("main.py").exists()
    }
    
    # Verificar variables de entorno básicas
    if checks[".env exists"]:
        try:
            with open(".env", 'r') as f:
                env_content = f.read()
                checks["OPENAI_API_KEY configured"] = "OPENAI_API_KEY=" in env_content and "your-" not in env_content
        except:
            checks["OPENAI_API_KEY configured"] = False
    
    # Mostrar resultados
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
    
    return checks

def run_test() -> bool:
    """Ejecuta una prueba básica del sistema."""
    
    print("\n🧪 Ejecutando prueba básica...")
    
    try:
        # Importar módulos principales
        sys.path.append("src")
        
        # Test básico de configuración
        from config.settings import settings
        print(f"✅ Configuración cargada: {settings.PROJECT_ROOT}")
        
        # Test de generador de contenido (requiere API key)
        if settings.OPENAI_API_KEY and "your-" not in settings.OPENAI_API_KEY:
            from content_generator.ai_generator import ContentGenerator
            print("✅ Generador de contenido disponible")
        else:
            print("⚠️  OpenAI API key no configurada - configura para usar generación de IA")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def interactive_setup():
    """Configuración interactiva paso a paso."""
    
    print("\n🔧 CONFIGURACIÓN INTERACTIVA\n")
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Crear directorios", create_directories),
        ("Configurar .env", setup_environment_file),
        ("Instalar dependencias", install_dependencies),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        
        if not step_func():
            print(f"❌ Fallo en: {step_name}")
            return False
        
        input("   Presiona Enter para continuar...")
    
    # Mostrar guía de APIs
    setup_api_guide()
    
    # Validación final
    validation = validate_setup()
    
    success_count = sum(validation.values())
    total_checks = len(validation)
    
    print(f"\n📊 RESUMEN: {success_count}/{total_checks} configuraciones correctas")
    
    if success_count >= total_checks - 2:  # Permitir algunas opcionales
        print("🎉 ¡Configuración completada! Puedes ejecutar:")
        print("   python main.py")
    else:
        print("⚠️  Configuración incompleta. Revisa los errores arriba.")
    
    return True

def main():
    """Función principal del setup."""
    
    parser = argparse.ArgumentParser(description="Setup para YouTube IA Automate")
    parser.add_argument("--mode", choices=["interactive", "quick", "validate"], 
                       default="interactive", help="Modo de configuración")
    parser.add_argument("--skip-deps", action="store_true", 
                       help="Omitir instalación de dependencias")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.mode == "interactive":
        interactive_setup()
    
    elif args.mode == "quick":
        print("🚀 Configuración rápida...")
        check_python_version()
        create_directories()
        setup_environment_file()
        
        if not args.skip_deps:
            install_dependencies()
        
        validate_setup()
        setup_api_guide()
    
    elif args.mode == "validate":
        validation = validate_setup()
        
        if all(validation.values()):
            print("\n✅ Todo configurado correctamente")
            run_test()
        else:
            print("\n❌ Configuración incompleta")
            setup_api_guide()

if __name__ == "__main__":
    main()