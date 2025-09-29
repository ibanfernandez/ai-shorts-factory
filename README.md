# AI Shorts Factory 🚀

> **Automatización completa para crear YouTube Shorts virales con IA - Multiidioma y multitemática, optimizado para cualquier tipo de contenido**

## ✨ Características Principales

- 🤖 **Generación de contenido automática** con GPT-4 optimizado para Shorts
- 🎥 **Videos verticales (9:16)** perfectos para móvil y algoritmo de Shorts  
- 🗣️ **Síntesis de voz natural** con Edge TTS multiidioma
- 📱 **Formato ultra-optimizado**: 30-60 segundos de duración ideal
- 🔄 **Publicación automática** en YouTube con SEO optimizado
- 💰 **Ultra económico**: $5-15/mes vs $681/año de alternativas cloud

## 🎯 ¿Por qué YouTube Shorts?

| Formato | Shorts | Videos Largos |
|---------|--------|---------------|
| **Duración** | 30-60 segundos | 8-15 minutos |
| **Costo por video** | $0.10-0.50 | $2-5 |
| **Tiempo de producción** | 5 minutos | 30-60 minutos |
| **Volumen diario** | 5-15 videos | 1-3 videos |
| **Alcance algoritmo** | 🔥 Preferencial | 📈 Estándar |
| **ROI** | 3-6 meses | 12-24 meses |

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
# IA y APIs
OPENAI_API_KEY=tu_clave_openai_aqui

# Configuración de contenido
CONTENT_LANGUAGE=es  # es, en, pt, fr, it, de
CONTENT_THEME=curiosidades  # curiosidades, tecnologia, historia
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

> **💡 Tip**: Puedes crear temas personalizados modificando los prompts en `templates/`

### 3. ¡Crear tu primer Short!

```bash
python main.py
```

## 🛠 Tecnologías

- **Python 3.11+** - Base del sistema
- **OpenAI GPT-4** - Generación de contenido viral
- **Edge TTS** - Síntesis de voz natural multiidioma
- **PIL/Pillow** - Procesamiento de imágenes optimizado
- **YouTube Data API** - Publicación automática

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

### Costos Mensuales (Producción 10 Shorts/día)
- **OpenAI GPT-4**: $5-10
- **APIs opcionales**: $0-5  
- **Hosting**: $0 (GitHub)
- **Total**: **$5-15/mes**

### Comparación con Competencia
- **Esta solución**: $16/año
- **N8N Cloud**: $681/año
- **Zapier Pro**: $588/año
- **Ahorro**: **97% más económico**

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

### ⚠️ Requisitos
- Clave OpenAI (GPT-4 recomendado)
- Python 3.11+ instalado
- Conexión a internet estable

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