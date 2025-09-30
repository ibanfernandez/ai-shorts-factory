# AI Shorts Factory 🚀

> **Automatización completa para crear YouTube Shorts virales c## 🌐 Interfaz Web Moderna

### **Acceso Rápido a la Interfaz Web**

```bash
# 1. Instalar dependencias completas (REQUERIDAS)
pip install -r requirements.txt

# 2. Lanzar interfaz web
python simple_web_app.py

# 3. Abrir navegador en: http://localhost:5000
```

> **⚠️ IMPORTANTE**: La interfaz web necesita **TODAS** las dependencias principales porque utiliza los mismos módulos de IA, video y audio que el sistema CLI.

### **🎮 Funciones de la Interfaz Web**

#### **Pestaña 1: Generador de Videos**
- 🎯 **Selector de tipo**: TOP 5 o Curiosidades
- 📝 **Input personalizado**: Escribe cualquier tema
- ⚡ **Generación automática**: Un clic y listo
- 📊 **Progreso en tiempo real**: Barra de progreso con polling
- 🎨 **Diseño moderno**: Gradientes y animaciones

#### **Pestaña 2: Biblioteca de Videos**
- 📚 **Vista de galería**: Todos tus videos generados
- ▶️ **Reproductor integrado**: Ve videos sin salir de la interfaz
- 🗑️ **Gestión completa**: Eliminar videos directamente
- 📱 **Responsive**: Perfecto en móvil y desktop
- 🔄 **Actualización automática**: Se actualiza al generar nuevos videos

#### **Pestaña 3: Catálogo de Temas**
- 📂 **5 Categorías organizadas**:
  - 🌌 **Espacio y Ciencia**: Planetas, agujeros negros, galaxias
  - 🔮 **Misterios y Paranormal**: Lugares misteriosos, civilizaciones perdidas
  - 🦁 **Naturaleza y Animales**: Criaturas raras, superpoderes animales
  - 🤖 **Tecnología y Futuro**: IA, robots, inventos revolucionarios
  - 🏛️ **Historia y Cultura**: Batallas épicas, emperadores, tesoros
- 📝 **Lista de Curiosidades**: Datos sorprendentes listos para usar
- 🔥 **Selección rápida**: Clic en cualquier tema para usarlo

#### **📊 Dashboard de Estadísticas**
- 🎬 **Videos Totales**: Contador de videos generados
- ⚡ **Generaciones Activas**: Procesos en tiempo real
- 📋 **Temas Disponibles**: Catálogo completo de temas

### **💻 Tecnología Web Stack**

- **🌐 Flask 2.3.3**: Backend ligero y eficiente
- **🎨 Bootstrap 5**: Interfaz moderna y responsive
- **⚡ AJAX Polling**: Actualizaciones en tiempo real sin WebSocket
- **📱 Mobile-First**: Optimizado para todos los dispositivos
- **🎭 Font Awesome 6**: Iconografía profesional

### **🔧 Características Técnicas Web**

- **🔄 Progreso en tiempo real**: Polling cada 2 segundos
- **💾 Gestión de archivos**: Servir videos y thumbnails
- **🗃️ Base de datos en memoria**: Rápida y eficiente
- **🔒 Compatibilidad total**: Sin dependencias problemáticas
- **⚡ Arranque instantáneo**: Listo en segundos

## 🎬 Uso del Sistema

### **Opción 1: Línea de Comandos (Tradicional)**
```bash
# 1. Asegúrate de que Ollama esté ejecutándose
ollama serve  # En una terminal separada

# 2. Activar entorno (si no está activo)
.venv\Scripts\activate  # Windows

# 3. Ejecutar automación
python main.py

# ¡Tu primer Short estará en output/videos/!
```

### **Opción 2: Interfaz Web (Recomendado)**
```bash
# 1. Lanzar interfaz web
python simple_web_app.py

# 2. Abrir navegador: http://localhost:5000

# 3. ¡Usar la interfaz visual para todo!
```e interfaz web moderna y generación masiva optimizada**

## ✨ Características Principales

- 🤖 **Generación de contenido automática** con Ollama (gratuito) o GPT-4 (premium)
- 🌐 **Interfaz web moderna** - Control total desde tu navegador
- 🎥 **Videos verticales (9:16)** perfectos para móvil y algoritmo de Shorts  
- 🗣️ **Síntesis de voz natural** con Edge TTS multiidioma
- 📱 **Formato ultra-optimizado**: 30-60 segundos de duración ideal
- 🔄 **Publicación automática** en YouTube con SEO optimizado
- 💰 **Dos modalidades**: 100% Gratuito con Ollama (IA local) o Premium con OpenAI
- 📊 **Dashboard en tiempo real** - Progreso, estadísticas y biblioteca de videos

## 🎯 ¿Por qué YouTube Shorts?

| Aspecto | Shorts (Ollama) | Shorts (OpenAI) | Videos Largos |
|---------|-----------------|-----------------|---------------|
| **Duración** | 30-60 segundos | 30-60 segundos | 8-15 minutos |
| **Costo por video** | $0.00 | $0.03-0.10 | $0.00-3.00 |
| **Tiempo de producción** | 3-5 minutos | 2-3 minutos | 30-60 minutos |
| **Volumen diario** | 10-30 videos | 15-50 videos | 1-3 videos |
| **Alcance algoritmo** | 🔥 Preferencial | 🔥 Preferencial | 📈 Estándar |
| **ROI** | 1-3 meses | 2-4 meses | 8-18 meses |

## 🚀 Instalación Rápida

### 1. **Requisitos Previos**
- ✅ **Python 3.9+** (recomendado 3.11 o superior)
- ✅ **Git** para clonar el repositorio
- ✅ **Al menos 8GB RAM** (para Ollama local) o clave OpenAI

### 2. **Descargar e Instalar**

```bash
# Clonar el proyecto
git clone https://github.com/ibanfernandez/ai-shorts-factory.git
cd ai-shorts-factory

# Crear entorno virtual (RECOMENDADO)
python -m venv .venv

# Activar entorno virtual
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat

# Actualizar pip (soluciona errores comunes)
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

### 3. **Configurar IA (OBLIGATORIO)**

**Opción A: 🆓 Ollama (100% Gratis)**
```bash
# 1. Instalar Ollama desde https://ollama.ai
# 2. Descargar modelo (requiere 8GB RAM):
ollama pull llama3.1:8b

# 3. Configurar en .env:
USE_OLLAMA=true
OLLAMA_MODEL=llama3.1:8b
```

**Opción B: 💳 OpenAI (De Pago)**
```bash
# Configurar en .env:
OPENAI_API_KEY=tu-clave-openai-aqui
USE_OLLAMA=false
```

### 4. **Configuración Mínima**

Crea el archivo `.env` (copia `.env.example`):
```env
# IA - ELIGE UNA OPCIÓN
USE_OLLAMA=true                    # 🆓 Ollama (local) 
# OPENAI_API_KEY=sk-tu-clave...    # 💳 OpenAI (pago)

# CONFIGURACIÓN BÁSICA
CONTENT_LANGUAGE=es                # es, en, pt, fr, it, de
CONTENT_THEME=curiosidades         # Ver temas disponibles abajo
```

### 5. **¡Crear tu Primer Short!**

```bash
# 1. Asegúrate de que Ollama esté ejecutándose
ollama serve  # En una terminal separada

# 2. Activar entorno (si no está activo)
.venv\Scripts\activate  # Windows

# 3. Ejecutar automación
python main.py

# ¡Tu primer Short estará en output/videos/!
```

## ⚠️ **Solución a Errores Comunes**

| Error | Solución |
|-------|----------|
| `No module named 'flask'` | `pip install -r requirements.txt` (NO simple_requirements.txt) |
| `No module named 'openai'` | `pip install -r requirements.txt` |
| `No module named 'moviepy'` | `pip install -r requirements.txt` - La web necesita TODAS las deps |
| `sqlite3 not found` | ✅ Solucionado (módulo built-in de Python) |
| `unknown command "generate"` | ✅ Solucionado - Ollama ahora usa `run` |
| `UnicodeEncodeError` | Normal en Windows - el sistema funciona |
| `Invalid argument filename` | ✅ Se corregirá automáticamente |
| `Ollama connection failed` | Ejecutar `ollama serve` en terminal separada |
| `Python not found` | Instalar Python 3.9+ desde python.org |
| Emojis no se ven | Normal en Windows PowerShell - funciona bien |
| Error al abrir web | Verificar que TODAS las dependencias estén instaladas |

**Idiomas disponibles:**
- 🇪🇸 `es` - Español (Voz: Alvaro/Elvira)
- 🇺🇸 `en` - English (Voice: Christopher/Jenny)  
- 🇧🇷 `pt` - Português (Voz: Antonio/Francisca)
- 🇫🇷 `fr` - Français (Voix: Henri/Denise)
- 🇮🇹 `it` - Italiano (Voce: Diego/Elsa)
- 🇩🇪 `de` - Deutsch (Stimme: Conrad/Katja)

## 🍹 **Temas Disponibles**

### **Categorías TOP 5** (En la interfaz web):
- 🌌 **Espacio y Ciencia**: Planetas extraños, agujeros negros, galaxias lejanas
- 🔮 **Misterios y Paranormal**: Lugares misteriosos, civilizaciones perdidas
- 🦁 **Naturaleza y Animales**: Criaturas raras, animales con superpoderes
- 🤖 **Tecnología y Futuro**: IA avanzada, robots, inventos revolucionarios
- 🏛️ **Historia y Cultura**: Batallas épicas, emperadores, tesoros perdidos

### **Curiosidades Generales**:
- 🔍 `curiosidades` - Datos increíbles y sorprendentes
- 💻 `tecnologia` - Gadgets e innovación
- 📚 `historia` - Secretos y misterios del pasado
- 🎬 `entretenimiento` - Películas, series y celebridades
- 🍕 `comida` - Recetas y datos gastronómicos
- ⚽ `deportes` - Estadísticas y curiosidades deportivas
- 🌍 `viajes` - Destinos y culturas del mundo
- 💰 `negocios` - Emprendimiento y finanzas
- 🎵 `musica` - Artistas, géneros y datos musicales
- 🔬 `ciencia` - Descubrimientos y experimentos





## 🤖 **Opciones de IA: Elige tu Modalidad**

### 🆓 **Modalidad Gratuita (Ollama)**
- **Ollama + Llama 3.1:8B** - IA local de alta calidad ✅ Gratis
- **Edge TTS** - Síntesis de voz multiidioma ✅ Gratis  
- **Ventajas**: $0 costo, privacidad total, sin límites
- **Ideal para**: Usuarios con hardware decente, presupuesto $0

### 💎 **Modalidad Premium (OpenAI)**
- **OpenAI GPT-4** - IA en la nube de máxima calidad 💳 De pago
- **Edge TTS** - Síntesis de voz multiidioma ✅ Gratis
- **Ventajas**: Velocidad extrema, sin configuración
- **Ideal para**: Usuarios que priorizan velocidad sobre costo

## 🛠️ Stack Tecnológico Completo

### **Core del Sistema**
- **Python 3.11+** - Base del sistema ✅ Gratuito
- **Edge TTS** - Síntesis de voz natural multiidioma ✅ Gratuito
- **PIL/Pillow** - Procesamiento de imágenes ✅ Gratuito
- **MoviePy** - Edición de video automatizada ✅ Gratuito
- **YouTube Data API** - Publicación automática ✅ Gratuito

### **Interfaz Web**
- **Flask 2.3.3** - Servidor web ligero ✅ Gratuito
- **Bootstrap 5** - Framework UI moderno ✅ Gratuito
- **AJAX/JavaScript** - Interactividad en tiempo real ✅ Gratuito

### **IA y Generación**
- **Ollama** - IA local gratuita ✅ Gratuito
- **OpenAI API** - IA premium en la nube 💳 Opcional

## 💡 Flujo de Trabajo Automático

1. **🧠 IA genera contenido** - Viral optimizado para Shorts en cualquier idioma
2. **🎤 Síntesis de voz** - Audio natural multiidioma con Edge TTS
3. **🖼️ Búsqueda de imágenes** - Imágenes relevantes automáticas
4. **🎬 Composición vertical** - Video 1080x1920 para móviles
5. **🎨 Thumbnail automático** - Miniatura atractiva generada
6. **📱 Publicación YouTube** - Upload con SEO optimizado
7. **🌐 Gestión web** - Control total desde la interfaz

## 📁 Estructura del Proyecto

```
ai-shorts-factory/
├── 📄 main.py                 # Punto de entrada línea de comandos
├── 🌐 simple_web_app.py       # Interfaz web moderna
├── ⚙️ setup.py                # Configuración inicial
├── 📦 requirements.txt        # Dependencias principales
├── 🌐 simple_requirements.txt # Dependencias web mínimas
├── 🔧 config/
│   ├── settings.py            # Configuración central
│   ├── localization.py        # Soporte multiidioma
│   └── shorts_config.py       # Configuración específica Shorts
├── 🧠 src/
│   ├── content_generator/     # IA para contenido viral
│   ├── video_creator/         # Creación de Shorts
│   └── youtube_publisher/     # Automatización YouTube
├── � templates/
│   └── simple_index.html      # Interfaz web moderna
├── 🎨 assets/                 # Recursos visuales
├── 📊 data/                   # Logs y datos
└── 🎬 output/                 # Shorts generados
    ├── videos/                # Videos finales
    └── temp/                  # Archivos temporales
```

## 🎬 Ejemplos de Uso

### **Básico Web - Interfaz Gráfica**
```bash
# IMPORTANTE: Instalar TODAS las dependencias primero
pip install -r requirements.txt

# Luego lanzar la interfaz web
python simple_web_app.py
# Abrir http://localhost:5000 y usar la interfaz
```

### **Básico CMD - Un Short Automático**
```bash
python main.py
```

### **Avanzado - Personalizado con Python**
```python
from main import YouTubeAutomation

# Crear automatización con idioma y tema personalizados
automation = YouTubeAutomation(
    language="en",        # Cambiar idioma
    theme="tecnologia"    # Cambiar tema
)

# Generar contenido viral automáticamente
result = await automation.create_and_publish_video(
    topic="most innovative AI gadgets 2024",
    content_type="TOP_5"
)
```

## 📊 Configuración para Shorts

```python
# Configuración optimizada en config/settings.py
VIDEO_CONFIG = {
    "resolution": (1080, 1920),  # Vertical 9:16
    "duration": 45,              # 30-60 segundos
    "fps": 30,                   # Fluido para móvil
    "format": "mp4",            # Compatible universal
    "quality": "high"           # Balance tamaño/calidad
}
```

## 💰 Análisis de Costos Shorts

### 🎯 **DOS OPCIONES DE IA** - Tú eliges tu presupuesto

| Servicio | Opción Gratuita | Opción de Pago |
|----------|-----------------|------------------|
| **IA para contenido** | Ollama (local) ✅ $0 | OpenAI 💳 $9-30/mes |
| **Síntesis de voz** | Edge TTS ✅ $0 | Edge TTS ✅ $0 |
| **YouTube API** | ✅ $0/mes | ✅ $0/mes |
| **Video/Imágenes** | ✅ $0/mes | ✅ $0/mes |
| **Hosting** | ✅ $0/mes | ✅ $0/mes |
| **Interfaz Web** | ✅ $0/mes | ✅ $0/mes |

### 🆓 **Opción 100% Gratuita (Ollama)**
| Aspecto | Detalles |
|---------|----------|
| **Costo por Short** | **$0.00** |
| **Costo mensual** | **$0.00** 🎉 |
| **Velocidad** | Rápida (depende de hardware) |
| **Calidad** | Excelente para Shorts |
| **Requisitos** | 8GB+ RAM, CPU moderna |
| **Privacidad** | 100% local, datos seguros |
| **Límites** | Sin límites de uso |

### 💳 **Opción Premium (OpenAI)**
| Aspecto | Detalles |
|---------|----------|
| **Costo por Short** | $0.03-0.10 |
| **Costo mensual** | $9-30 (según uso) |
| **Velocidad** | Ultra rápida |
| **Calidad** | Premium, más sofisticada |
| **Requisitos** | Solo conexión internet |
| **Disponibilidad** | 24/7 sin configuración |
| **Límites** | Según plan de OpenAI |

### 📊 Comparación Anual con Competencia

| Solución | Con Ollama | Con OpenAI | Competencia |
|----------|------------|------------|-------------|
| **AI Shorts Factory** | **$0/año** 🎉 | $108-360/año | - |
| **N8N Cloud** | - | - | $681/año + APIs |
| **Zapier Pro** | - | - | $588/año + APIs |
| **Make.com** | - | - | $468/año + APIs |

**Ahorro real:**
- Con Ollama: **100% gratuito** vs $468-681/año
- Con OpenAI: **40-84% más económico** vs competencia

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
# Configuración de Contenido
CONTENT_LANGUAGE=es           # Idioma: es, en, pt, fr, it, de
CONTENT_THEME=curiosidades    # Tema: curiosidades, tecnologia, historia
TTS_VOICE=es-ES-AlvaroNeural  # Voz personalizada (opcional)

# Core IA
OPENAI_API_KEY=sk-...
USE_OLLAMA=true              # Para usar Ollama gratuito

# YouTube (opcional)
YOUTUBE_CLIENT_ID=tu_client_id
YOUTUBE_CLIENT_SECRET=tu_secret

# Optimización Shorts
TARGET_DURATION=45

# Web Interface (opcional)
WEB_HOST=0.0.0.0            # Para acceso remoto
WEB_PORT=5000               # Puerto personalizado
```

# YouTube (opcional)
YOUTUBE_CLIENT_ID=tu_client_id
YOUTUBE_CLIENT_SECRET=tu_secret

# Optimización Shorts
TARGET_DURATION=45
```

## 🚦 Consideraciones de Uso

### ✅ Incluido
- ✅ Contenido 100% original generado por IA
- ✅ Interfaz web moderna y responsive
- ✅ Optimización para algoritmo de Shorts
- ✅ SEO automático multiidioma
- ✅ Cumplimiento términos YouTube
- ✅ Escalabilidad ilimitada
- ✅ Gestión visual de biblioteca de videos

### ⚠️ Requisitos del Sistema

**Opción Gratuita (Ollama):**
- Python 3.11+ instalado
- 8GB+ RAM (16GB+ recomendado)
- ~10GB espacio en disco (para modelos IA)
- CPU moderna (cualquiera de los últimos 5 años)
- GPU opcional (acelera la generación)

**Opción de Pago (OpenAI):**
- Python 3.11+ instalado
- Clave OpenAI API (GPT-4 recomendado)
- Conexión a internet estable
- Requisitos mínimos de hardware

**Para Interfaz Web:**
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Puerto 5000 disponible (configurable)

## 🔄 Roadmap

- [x] **v1.0** - Generación básica de Shorts
- [x] **v1.1** - Optimización para algoritmo
- [x] **v1.2** - Interfaz web moderna
- [x] **v1.3** - Dashboard y gestión visual
- [ ] **v1.4** - Analytics integrado  
- [ ] **v1.5** - A/B testing automático
- [ ] **v2.0** - Integración TikTok/Instagram
- [ ] **v2.1** - API REST completa
- [ ] **v2.2** - Plantillas de video personalizables

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añade nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

### ⭐ ¿Te resulta útil? ¡Deja una estrella y comparte!

**🚀 Desarrollado para creators que quieren escalar su contenido con IA**

**📧 Soporte**: [GitHub Issues](https://github.com/ibanfernandez/ai-shorts-factory/issues)

**🌐 Demo**: Ejecuta `pip install -r requirements.txt && python simple_web_app.py` y ve a http://localhost:5000