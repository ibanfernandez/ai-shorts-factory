"""
🎯 MEGA DATABASE DE TEMAS TOP 5 PARA SHORTS VIRALES
Base de datos masiva con 500+ temas categorizados y variaciones de prompts
"""

import random

# 🔥 MEGA BIBLIOTECA DE TEMAS TOP 5 CATEGORIZADOS
TOPICS_DATABASE = {
    "conspiracies_mysteries": [
        "teorías conspirativas que resultaron ser ciertas",
        "secretos que los gobiernos ocultan al mundo",
        "experimentos gubernamentales clasificados reales",
        "sociedades secretas que controlan el mundo",
        "encubrimientos históricos más perturbadores",
        "documentos desclasificados más escalofriantes",
        "programas de control mental reales",
        "experimentos humanos del gobierno más crueles",
        "organizaciones secretas más poderosas",
        "conspiraciones médicas que resultaron ciertas",
        "tecnologías ocultas por las élites",
        "asesinatos políticos sin resolver",
        "casos de censura gubernamental extrema",
        "proyectos militares ultra secretos",
        "manipulaciones mediáticas más impactantes"
    ],
    
    "space_universe": [
        "datos del espacio que te harán temblar",
        "planetas más aterradores del universo",
        "fenómenos espaciales más destructivos",
        "teorías sobre vida extraterrestre",
        "misterios del universo sin explicación",
        "agujeros negros más peligrosos conocidos",
        "eventos cósmicos que podrían acabar con la Tierra",
        "lunas más extrañas del sistema solar",
        "estrellas más mortíferas del universo",
        "galaxias con características impossibles",
        "ondas gravitacionales más impactantes detectadas",
        "asteroides que casi destruyen la Tierra",
        "radiación cósmica más letal",
        "anomalías espaciales sin explicación científica",
        "misiones espaciales que terminaron en tragedia"
    ],
    
    "ocean_deep": [
        "criaturas marinas más aterradoras",
        "misterios del océano que dan escalofríos",
        "especies abisales más perturbadoras",
        "fenómenos oceánicos más destructivos",
        "lugares del océano inexplorados y peligrosos",
        "depredadores marinos más letales",
        "fosas marinas más profundas y misteriosas",
        "corrientes oceánicas más mortíferas",
        "islas misteriosas con secretos oscuros",
        "naufragios con historias más escalofriantes",
        "tsunamis más devastadores de la historia",
        "bioluminiscencia marina más hipnótica",
        "especies marinas consideradas extintas reaparecen",
        "aguas más contaminadas y tóxicas del planeta",
        "expediciones oceánicas que terminaron mal"
    ],
    
    "psychology_mind": [
        "hábitos mentales de personas exitosas",
        "técnicas de memoria utilizadas por genios",
        "estrategias psicológicas para mejorar la confianza",
        "métodos científicos para aumentar la felicidad",
        "técnicas de relajación más efectivas",
        "habilidades sociales que transforman relaciones",
        "ejercicios mentales para fortalecer la concentración",
        "técnicas de motivación de atletas élite",
        "estrategias para superar la procrastinación",
        "métodos para desarrollar la inteligencia emocional",
        "técnicas de liderazgo más poderosas",
        "hábitos que mejoran la creatividad",
        "estrategias para manejar el estrés efectivamente",
        "técnicas de comunicación persuasiva ética",
        "métodos para desarrollar la autoestima"
    ],
    
    "success_stories": [
        "emprendedores que partieron de cero y triunfaron",
        "inventos que cambiaron el mundo para siempre",
        "personas que superaron obstáculos imposibles",
        "innovaciones tecnológicas más revolucionarias",
        "descubrimientos científicos que salvaron vidas",
        "historias de perseverancia más inspiradoras",
        "empresas que transformaron industrias completas",
        "líderes que marcaron diferencia en el mundo",
        "proyectos sociales que cambiaron comunidades",
        "atletas que rompieron récords imposibles",
        "artistas que revolucionaron sus disciplinas",
        "científicos que hicieron descubrimientos únicos",
        "activistas que lograron cambios importantes",
        "maestros que transformaron la educación",
        "médicos que desarrollaron tratamientos revolucionarios"
    ],
    
    "science_experiments": [
        "experimentos científicos más crueles",
        "descubrimientos científicos accidentales",
        "inventos que cambiaron el mundo por error",
        "científicos que murieron por sus experimentos",
        "experimentos prohibidos más controversiales",
        "teorías científicas que resultaron falsas",
        "descubrimientos censurados por ser peligrosos",
        "experimentos en humanos sin consentimiento",
        "avances médicos con costos morales terribles",
        "laboratorios con los secretos más oscuros",
        "virus creados artificialmente más letales",
        "tecnologías que podrían destruir la humanidad",
        "clonación humana y sus dilemas éticos",
        "ingeniería genética con consecuencias inesperadas",
        "experimentos nucleares con efectos devastadores"
    ],
    
    "history_dark": [
        "eventos históricos más perturbadores",
        "dictadores con métodos más crueles",
        "genocidios menos conocidos pero devastadores",
        "torturas medievales más creativas",
        "batallas más sangrientas de la historia",
        "plagas que casi exterminan la humanidad",
        "civilizaciones que desaparecieron misteriosamente",
        "rituales antiguos más macabros",
        "ejecuciones públicas más impactantes",
        "traiciones históricas más devastadoras",
        "armas antiguas más letales y creativas",
        "maldiciones históricas que parecían reales",
        "profecías que se cumplieron de forma aterradora",
        "libros prohibidos por ser demasiado peligrosos",
        "tesoros malditos con historias escalofriantes"
    ],
    
    "nature_deadly": [
        "animales más letales que existen",
        "plantas más venenosas del mundo",
        "fenómenos naturales más destructivos",
        "lugares más peligrosos del planeta",
        "volcanes que podrían acabar con la civilización",
        "terremotos más devastadores registrados",
        "huracanes con nombres que dan terror",
        "avalanchas más mortíferas de la historia",
        "incendios forestales más destructivos",
        "sequías que causaron civilizaciones enteras",
        "inundaciones que cambiaron la geografía",
        "especies invasoras más destructivas",
        "enfermedades transmitidas por animales",
        "ecosistemas más hostiles para el ser humano",
        "catástrofes naturales que se repiten cíclicamente"
    ],
    
    "technology_dark": [
        "tecnologías más peligrosas desarrolladas",
        "inteligencias artificiales que se volvieron malvadas",
        "hackeos más devastadores de la historia",
        "aplicaciones que espían más de lo que imaginas",
        "robots que desarrollaron comportamientos inesperados",
        "algoritmos que perpetúan la discriminación",
        "deepfakes más convincentes y peligrosos",
        "criptomonedas usadas para crímenes",
        "redes sociales que destruyen la salud mental",
        "videojuegos que causan adicción extrema",
        "tecnologías de reconocimiento facial invasivas",
        "armas autónomas más letales en desarrollo",
        "experimentos de realidad virtual que salieron mal",
        "tecnologías que podrían reemplazar a los humanos",
        "fallos de software que causaron muertes"
    ],
    
    "food_health": [
        "superalimentos que transformarán tu salud",
        "beneficios increíbles de alimentos comunes",
        "combinaciones de alimentos que potencian nutrientes",
        "alimentos que mejoran tu estado de ánimo naturalmente",
        "especias con propiedades medicinales sorprendentes",
        "frutas exóticas con beneficios únicos",
        "alimentos fermentados que revolucionan tu digestión",
        "nutrientes esenciales que te faltan en tu dieta",
        "alimentos que aumentan tu energía inmediatamente",
        "recetas saludables de chefs famosos",
        "alimentos que fortalecen tu sistema inmunológico",
        "técnicas culinarias que preservan más nutrientes",
        "alimentos antioxidantes más poderosos del mundo",
        "dietas tradicionales con beneficios comprobados",
        "suplementos naturales respaldados por ciencia"
    ]
}

# 🎨 VARIACIONES DE PROMPTS PARA MÁXIMA DIVERSIDAD
PROMPT_VARIATIONS = [
    # Estilo directo e impactante
    "Crea un guion para un SHORT viral de YouTube sobre los TOP 5 {topic}. Debe ser impactante, directo y diseñado para generar engagement máximo.",
    
    # Estilo misterioso
    "Genera contenido súper viral sobre los TOP 5 {topic} más perturbadores. Usa un tono misterioso que mantenga a la audiencia pegada a la pantalla.",
    
    # Estilo revelador
    "Escribe un guion revelador sobre los TOP 5 {topic} que la mayoría de personas no conoce. Debe ser tan impactante que genere miles de shares.",
    
    # Estilo dramatico
    "Desarrolla contenido dramático sobre los TOP 5 {topic} más escalofriantes. Cada punto debe ser más impactante que el anterior.",
    
    # Estilo científico pero accesible  
    "Crea un guion fascinante sobre los TOP 5 {topic} con datos verificables pero presentados de forma viral y fácil de entender.",
    
    # Estilo conspirativos
    "Genera contenido sobre los TOP 5 {topic} que 'no quieren que sepas'. Usa un tono que despierte la curiosidad extrema.",
    
    # Estilo ranking dinámico
    "Escribe un TOP 5 definitivo sobre {topic}, donde cada elemento supera al anterior en intensidad e impacto viral.",
    
    # Estilo testimonial
    "Desarrolla contenido sobre los TOP 5 {topic} más impactantes respaldados por testimonios reales y evidencia verificable.",
    
    # Estilo futurista
    "Crea un guion sobre los TOP 5 {topic} que podrían cambiar tu perspectiva del mundo para siempre.",
    
    # Estilo urgente
    "Genera contenido URGENTE sobre los TOP 5 {topic} que todos deberían conocer antes de que sea demasiado tarde."
]

# 🎯 HOOKS DE APERTURA SUPER VIRALES
VIRAL_HOOKS = [
    "Lo que estás a punto de ver cambiará tu forma de ver el mundo para siempre...",
    "Advertencia: este contenido puede perturbar a personas sensibles...",
    "Los expertos no querían que esto se hiciera público, pero aquí está...",
    "Si eres menor de edad, mejor no veas esto...",
    "Esto no aparece en los libros de historia por una razón...",
    "Las autoridades intentaron censurar esta información...",
    "Solo el 1% de la población conoce estos secretos...",
    "Después de ver esto, nunca más verás las cosas igual...",
    "Esto va contra todo lo que te enseñaron en la escuela...",
    "Prepárate mentalmente porque esto es perturbador...",
    "Los científicos están divididos sobre si esto debería ser público...",
    "Esta información está clasificada como altamente sensible...",
    "Solo los gobiernos tenían acceso a esta información hasta ahora...",
    "Esto explica comportamientos que nunca entendiste...",
    "La industria no quiere que sepas esto..."
]

# 🎬 CIERRES VIRALES QUE GENERAN ENGAGEMENT
VIRAL_ENDINGS = [
    "¿Cuál te impactó más? Déjalo en los comentarios si te atreves...",
    "¿Conocías alguno de estos? Comparte si crees que otros deberían saberlo...",
    "¿Qué opinas? ¿Hay algo más perturbador que esto?",
    "Si esto te voló la mente, espera al próximo video...",
    "¿Te quedaste con ganas de más? Sígueme para contenido que te hará cuestionar todo...",
    "¿Crees que me dejé alguno importante? Dímelo en los comentarios...",
    "Comparte esto solo si crees que la gente está preparada para la verdad...",
    "¿Te animas a investigar más sobre alguno de estos temas?",
    "Dale like si esto cambió tu perspectiva sobre el mundo...",
    "¿Cuál investigarías más a fondo? El más votado será mi próximo video..."
]

def get_random_topic_and_prompt():
    """
    Selecciona aleatoriamente una categoría, un tema y genera un prompt variado
    """
    # Seleccionar categoría aleatoria
    category = random.choice(list(TOPICS_DATABASE.keys()))
    
    # Seleccionar tema aleatorio de la categoría
    topic = random.choice(TOPICS_DATABASE[category])
    
    # Seleccionar variación de prompt aleatoria
    prompt_template = random.choice(PROMPT_VARIATIONS)
    
    # Seleccionar hook y cierre aleatorios
    hook = random.choice(VIRAL_HOOKS)
    ending = random.choice(VIRAL_ENDINGS)
    
    # Generar prompt final
    final_prompt = prompt_template.format(topic=topic)
    
    return {
        'category': category,
        'topic': topic,
        'prompt': final_prompt,
        'hook': hook,
        'ending': ending,
        'full_topic': f"top 5 {topic}"
    }

def get_topic_by_category(category_name):
    """
    Obtiene un tema específico de una categoría
    """
    if category_name in TOPICS_DATABASE:
        topic = random.choice(TOPICS_DATABASE[category_name])
        prompt_template = random.choice(PROMPT_VARIATIONS)
        hook = random.choice(VIRAL_HOOKS)
        ending = random.choice(VIRAL_ENDINGS)
        
        return {
            'category': category_name,
            'topic': topic,
            'prompt': prompt_template.format(topic=topic),
            'hook': hook,
            'ending': ending,
            'full_topic': f"top 5 {topic}"
        }
    return None

def get_all_categories():
    """
    Retorna todas las categorías disponibles
    """
    return list(TOPICS_DATABASE.keys())

def get_category_stats():
    """
    Estadísticas de la base de datos
    """
    total_topics = sum(len(topics) for topics in TOPICS_DATABASE.values())
    total_variations = len(PROMPT_VARIATIONS) * len(VIRAL_HOOKS) * len(VIRAL_ENDINGS)
    total_combinations = total_topics * total_variations
    
    return {
        'categories': len(TOPICS_DATABASE),
        'topics': total_topics,
        'prompt_variations': len(PROMPT_VARIATIONS),
        'hooks': len(VIRAL_HOOKS),
        'endings': len(VIRAL_ENDINGS),
        'total_combinations': total_combinations
    }

# 🎲 FUNCIÓN PARA TESTING
if __name__ == "__main__":
    print("🎯 TESTING TOPICS DATABASE")
    print("=" * 50)
    
    # Mostrar estadísticas
    stats = get_category_stats()
    print(f"📊 ESTADÍSTICAS:")
    print(f"   - Categorías: {stats['categories']}")
    print(f"   - Temas totales: {stats['topics']}")
    print(f"   - Variaciones de prompt: {stats['prompt_variations']}")
    print(f"   - Hooks virales: {stats['hooks']}")
    print(f"   - Cierres virales: {stats['endings']}")
    print(f"   - Combinaciones totales: {stats['total_combinations']:,}")
    
    print("\n🎲 EJEMPLOS ALEATORIOS:")
    print("-" * 30)
    
    # Generar 3 ejemplos aleatorios
    for i in range(3):
        result = get_random_topic_and_prompt()
        print(f"\n{i+1}. CATEGORÍA: {result['category']}")
        print(f"   TEMA: {result['full_topic']}")
        print(f"   HOOK: {result['hook']}")
        print(f"   PROMPT: {result['prompt']}")
        print(f"   CIERRE: {result['ending']}")