# AI Shorts Factory 🚀

> **Automatización completa para crear YouTube Shorts virales con IA - Multiidioma y multitemática, optimizado para cualquier tipo de contenido**

## ✨ Características Principales

- 🤖 **Generación de contenido automática** con Ollama (gratuito) o GPT-4 (premium)
- 🎥 **Videos verticales (9:16)** perfectos para móvil y algoritmo de Shorts  
- 🗣️ **Síntesis de voz natural** con Edge TTS multiidioma
- 📱 **Formato ultra-optimizado**: 30-60 segundos de duración ideal
- 🔄 **Publicación automática** en YouTube con SEO optimizado
- 💰 **Dos modalidades**: 100% Gratuito con Ollama (IA local) o Premium con OpenAI

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

### 1. Clonar y Configurar

```bash
git clone https://github.com/ibanfernandez/ai-shorts-factory.git
cd ai-shorts-factory
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configurar Idioma y Tema

Crear archivo `.env`:
```env
# 🎯 ELECCIÓN DE IA (elige una opción):

# Opción 1: 100% GRATUITO con Ollama (IA local)
# Instala Ollama desde: https://ollama.ai
# Luego ejecuta: ollama pull llama3.1:8b
USE_OLLAMA=true

# Opción 2: OpenAI (de pago, más rápido)
# OPENAI_API_KEY=tu_clave_openai_aqui
# USE_OLLAMA=false

# ⚙️ CONFIGURACIÓN BÁSICA
CONTENT_LANGUAGE=es  # es, en, pt, fr, it, de
CONTENT_THEME=curiosidades  # curiosidades, tecnologia, historia

# 🚫 OPCIONAL - Funciones extra
# YOUTUBE_CLIENT_ID=para_subida_automatica
# UNSPLASH_ACCESS_KEY=para_mas_imagenes
```

**Idiomas disponibles:**
- 🇪🇸 `es` - Español (Voz: Alvaro/Elvira)
- 🇺🇸 `en` - English (Voice: Christopher/Jenny)  
- 🇧🇷 `pt` - Português (Voz: Antonio/Francisca)
- 🇫🇷 `fr` - Français (Voix: Henri/Denise)
- 🇮🇹 `it` - Italiano (Voce: Diego/Elsa)
- 🇩🇪 `de` - Deutsch (Stimme: Conrad/Katja)

**Temas disponibles:**
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

### 🎨 **Crear Temas Personalizados**

¿Quieres un nicho específico? ¡Crea tu propio tema!

**Ejemplos de temas custom**:
- 🎮 `gaming` - Trucos, reviews, curiosidades gaming
- 🏃 `fitness` - Ejercicios caseros, rutinas, nutrición
- 🍳 `cocina` - Recetas rápidas, tips culinarios
- 💰 `finanzas` - Ahorro, inversiones, apps financieras
- 🎨 `arte` - Tutoriales, técnicas, inspiración creativa

**Pasos para crear tu tema**:

1. **Configura tu tema** en `templates/custom_themes.json`:
```json
{
  "mi_tema": {
    "es": {
      "channel_name": "Mi Canal Viral",
      "description": "Tu descripción aquí",
      "tags_base": ["tag1", "tag2", "viral"],
      "content_types": ["TOP_5", "MI_FORMATO"],
      "topics_pool": ["tema 1", "tema 2", "tema 3"]
    }
  }
}
```

2. **Crea prompts específicos** en `templates/prompts/mi_tema_es.md`

3. **Activa tu tema**:
```bash
CONTENT_THEME=mi_tema python main.py
```

> **📚 Guía completa**: Ver `templates/examples/guia_temas_personalizados.md` para instrucciones detalladas

### 3a. OPCIÓN GRATUITA: Instalar Ollama (Recomendado)

```bash
# 1. Descargar Ollama para Windows
# Visita: https://ollama.ai/download/windows

# 2. Instalar el modelo (una sola vez)
ollama pull llama3.1:8b

# 3. Verificar instalación
ollama list

# 4. ¡Ya tienes IA gratuita!
```

**Requisitos recomendados para Ollama:**
- **Mínimo**: 8GB RAM + CPU moderna (funciona en cualquier PC reciente)
- **Recomendado**: 16GB+ RAM + GPU NVIDIA/AMD (mayor velocidad)
- **Óptimo**: 32GB+ RAM + GPU dedicada (máximo rendimiento)
- **Modelo recomendado**: Llama 3.1:8B (balance perfecto calidad/velocidad)
- **Costo**: $0 para siempre

> **💡 Ejemplo real**: Con Ryzen 2600x + GTX 1660Ti + 16GB RAM obtienes generación ultra rápida

### 3b. OPCIÓN DE PAGO: Usar OpenAI

Si prefieres OpenAI, simplemente agrega tu API key al `.env`.

### 4. ¡Crear tu primer Short!

```bash
python main.py
```

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

## � Stack Tecnológico Común

- **Python 3.11+** - Base del sistema ✅ Gratuito
- **Edge TTS** - Síntesis de voz natural multiidioma ✅ Gratuito
- **PIL/Pillow** - Procesamiento de imágenes ✅ Gratuito
- **MoviePy** - Edición de video automatizada ✅ Gratuito
- **YouTube Data API** - Publicación automática ✅ Gratuito

## 💡 Flujo de Trabajo Automático

1. **🧠 IA genera contenido** - Viral optimizado para Shorts en cualquier idioma
2. **🎤 Síntesis de voz** - Audio natural multiidioma con Edge TTS
3. **🖼️ Búsqueda de imágenes** - Imágenes relevantes automáticas
4. **🎬 Composición vertical** - Video 1080x1920 para móviles
5. **🎨 Thumbnail automático** - Miniatura atractiva generada
6. **📱 Publicación YouTube** - Upload con SEO optimizado

## 📁 Estructura del Proyecto

```
ai-shorts-factory/
├── 📄 main.py              # Punto de entrada principal
├── ⚙️ setup.py             # Configuración inicial
├── 📦 requirements.txt     # Dependencias
├── 🔧 config/
│   └── settings.py         # Configuración central
├── 🧠 src/
│   ├── content_generator/  # IA para contenido viral
│   ├── video_creator/      # Creación de Shorts
│   └── youtube_publisher/  # Automatización YouTube
├── 🎨 templates/           # Plantillas de contenido
├── 📱 assets/              # Recursos visuales
└── 🎬 output/              # Shorts generados
```

## 🎬 Ejemplos de Uso

### Básico - Un Short Automático
```bash
python main.py
```

### Avanzado - Personalizado
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

# YouTube (opcional)
YOUTUBE_CLIENT_ID=tu_client_id
YOUTUBE_CLIENT_SECRET=tu_secret

# Optimización Shorts
TARGET_DURATION=45
```

## 🚦 Consideraciones de Uso

### ✅ Incluido
- ✅ Contenido 100% original generado por IA
- ✅ Optimización para algoritmo de Shorts
- ✅ SEO automático multiidioma
- ✅ Cumplimiento términos YouTube
- ✅ Escalabilidad ilimitada

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

## 🔄 Roadmap

- [x] **v1.0** - Generación básica de Shorts
- [x] **v1.1** - Optimización para algoritmo
- [ ] **v1.2** - Analytics integrado  
- [ ] **v1.3** - A/B testing automático
- [ ] **v2.0** - Integración TikTok/Instagram

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

**Desarrollado para creators que quieren escalar su contenido con IA 🚀**