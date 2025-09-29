# Guía Completa: Crear Temas Personalizados

## 🎯 Paso a Paso para Crear un Tema Custom

### 1. 📝 Definir tu Tema

Piensa en:
- **Nicho específico**: ¿Qué área te interesa? (ej: cocina vegana, fitness en casa, finanzas personales)
- **Audiencia objetivo**: ¿A quién va dirigido?
- **Tipo de contenido**: ¿Consejos, datos curiosos, comparaciones?
- **Tono**: ¿Educativo, divertido, motivacional?

### 2. 🔧 Configurar en `custom_themes.json`

Copia el template `_template` y personalízalo:

```json
{
  "mi_tema_fitness": {
    "es": {
      "channel_name": "Fit en Casa",
      "description": "Ejercicios caseros, rutinas efectivas y motivación fitness",
      "tags_base": ["fitness", "ejercicios", "casa", "rutinas", "viral"],
      "content_types": ["TOP_5", "RUTINAS", "EJERCICIOS_CASA"],
      "topics_pool": [
        "ejercicios para quemar grasa en casa",
        "rutinas de 10 minutos súper efectivas",
        "ejercicios que no necesitan equipo",
        "errores comunes al hacer ejercicio",
        "alimentos que potencian tu entrenamiento"
      ]
    }
  }
}
```

### 3. ✍️ Crear Prompts Específicos

Crea archivo `prompts/fitness_es.md`:

```markdown
# Prompts para Tema: Fitness Casero (Español)

## TOP_5 Prompt
Crea un guion para YouTube Short sobre "{topic}" de fitness casero.
- Título motivacional con emojis
- Hook: "¿Quieres resultados sin gym?"
- 5 ejercicios/consejos numerados
- Instrucciones claras y seguras
- CTA: "¡Sígueme para más rutinas!"
- Hashtags: #Shorts #Fitness #Casa #Ejercicios

ESTILO: Motivacional, seguro, inclusivo
DURACIÓN: 45-60 segundos
```

### 4. 🧪 Probar y Ajustar

1. **Ejecuta tu tema**:
```bash
CONTENT_THEME=mi_tema_fitness python main.py
```

2. **Revisa resultados**:
   - ¿El contenido es coherente?
   - ¿El tono es apropiado?
   - ¿La duración es correcta?

3. **Ajusta prompts** según necesidades

### 5. 📚 Documentar tu Tema

Crea archivo en `examples/mi_tema_fitness.md`:

```markdown
# Tema: Fitness Casero

## Descripción
Contenido motivacional sobre ejercicios que se pueden hacer en casa.

## Resultados Típicos
- Videos de 45-60 segundos
- Tono motivacional y positivo
- Instrucciones claras y seguras
- Engagement alto en audiencia fitness

## Mejores Topics
- "ejercicios para quemar grasa sin equipo"
- "rutina de abdominales en 10 minutos"
- "estiramientos para dolor de espalda"

## Tips Específicos
- Siempre incluir advertencias de seguridad
- Mencionar alternativas para diferentes niveles
- Usar terminología motivacional
```

## 🔥 Temas Populares para Inspiración

### 🎮 Gaming
- Trucos y secretos
- Reviews rápidos
- Curiosidades gaming
- Comparaciones

### 🍳 Cocina
- Recetas rápidas
- Tips de cocina
- Datos nutricionales
- Hacks culinarios

### 💰 Finanzas
- Consejos de ahorro
- Inversiones básicas
- Apps financieras
- Educación financiera

### 🎨 Arte/Creatividad
- Tutoriales rápidos
- Inspiración artística
- Técnicas creativas
- Herramientas digitales

### 🌱 Lifestyle
- Hábitos saludables
- Productividad
- Minimalismo
- Desarrollo personal

## ⚡ Tips Avanzados

### 1. Optimización por Audiencia
```json
"topics_pool_by_age": {
  "18-25": ["temas trending", "referencias pop"],
  "25-35": ["temas profesionales", "life hacks"],
  "35+": ["temas familiares", "salud", "finanzas"]
}
```

### 2. Variaciones Estacionales
```json
"seasonal_topics": {
  "verano": ["ejercicios de playa", "comida fresca"],
  "invierno": ["rutinas en casa", "comfort food"]
}
```

### 3. Personalización por País
```json
"es": {
  "country_variants": {
    "ES": "terminología española",
    "MX": "terminología mexicana", 
    "AR": "terminología argentina"
  }
}
```

## 🚀 Activar tu Tema Custom

### Opción 1: Variable de Entorno
```bash
CONTENT_THEME=mi_tema_fitness python main.py
```

### Opción 2: Código Python
```python
automation = YouTubeAutomation(
    language="es",
    theme="mi_tema_fitness"  # Tu tema custom
)
```

### Opción 3: Archivo .env
```env
CONTENT_THEME=mi_tema_fitness
```

## 🔍 Troubleshooting

**Problema**: El tema no se encuentra
- **Solución**: Verifica que esté en `custom_themes.json` con la sintaxis correcta

**Problema**: Contenido muy genérico
- **Solución**: Ajusta los prompts para ser más específicos

**Problema**: Duración incorrecta
- **Solución**: Modifica las instrucciones de duración en los prompts

**Problema**: Tono inadecuado
- **Solución**: Revisa y ajusta las instrucciones de estilo en prompts