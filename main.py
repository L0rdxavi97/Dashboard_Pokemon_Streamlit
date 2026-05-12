import streamlit as st
import pandas as pd
import plotly.express as px


# COMANDO: streamlit run main.py


# CONFIGURACIÓN DE LA PÁGINA
# set_page_config es la PRIMERA llamada a Streamlit del script.
# Aquí definimos el título que aparece en la pestaña del navegador, el icono
# y el layout "wide" para aprovechar todo el ancho de la pantalla.
st.set_page_config(
    page_title="Dashboard Pokémon Kanto",
    page_icon="👾",
    layout="wide",
)


# CARGA DE DATOS
# Leemos el CSV que contiene la información de los 151 Pokémon.
# la ruta relativa es "data/pokemon_gen1.csv".
datos_pokemon = pd.read_csv("data/pokemon_gen1.csv")

# Normalizamos los nombres: primera letra en mayúscula
# para que el selector y las etiquetas se vean bien.
datos_pokemon['name'] = datos_pokemon['name'].str.capitalize()


# CABECERA DE LA APLICACIÓN
st.title("👾 Dashboard Pokémon: 1ª Generación")
st.markdown("Análisis interactivo de los 151 Pokémon originales.")
st.divider()   # línea horizontal decorativa que separa secciones


# SELECTOR DE POKÉMON (widget de control principal)
# Extraemos la lista de nombres únicos del DataFrame para poblar el desplegable.
# Cuando el usuario cambia la selección, Streamlit re-ejecuta todo el script
# desde arriba automáticamente, por lo que todos los gráficos y métricas
# de abajo se actualizan de forma reactiva sin código extra.
lista_pokemon = datos_pokemon['name'].unique()

seleccion = st.selectbox(
    "Selecciona un Pokémon para ver su análisis:",
    lista_pokemon
)

# Filtramos el DataFrame para quedarnos solo con la fila del Pokémon elegido.
pokemon_info = datos_pokemon[datos_pokemon['name'] == seleccion].iloc[0]


# SECCIÓN DINÁMICA: IMAGEN + GRÁFICO DE ESTADÍSTICAS
# Dividimos el espacio horizontal en dos columnas con proporciones [1, 2]:
#   col_img   → ocupa 1 parte (imagen del Pokémon)
#   col_stats → ocupa 2 partes (gráfico de barras con sus stats)
col_img, col_stats = st.columns([1, 2])

# --- Columna izquierda: imagen del Pokémon ---
with col_img:
    # La URL de la imagen viene directamente del CSV (columna 'sprite_url').
    # use_container_width=True hace que la imagen se adapte al ancho de la columna.
    st.image(
        pokemon_info['sprite_url'],
        caption=f"Artwork oficial de {seleccion}",
        width='stretch'
    )

# --- Columna derecha: gráfico de barras horizontales con las stats ---
with col_stats:
    st.subheader("Estadísticas de Combate")

    # Lista con los nombres de las columnas de estadísticas en el CSV
    stats_cols = [
        'stat_hp',
        'stat_attack',
        'stat_defense',
        'stat_sp_attack',
        'stat_sp_defense',
        'stat_speed'
    ]

    # Extraemos los valores numéricos del Pokémon seleccionado para cada stat
    valores = [pokemon_info[col] for col in stats_cols]

    # Convertimos los nombres de columna a etiquetas legibles
    nombres_stats = [s.replace('_', ' ').upper() for s in stats_cols]

    # Creamos el gráfico de barras horizontal con Plotly Express:
    #   - x=valores      → longitud de cada barra (valor de la stat)
    #   - y=nombres_stats → etiqueta de cada barra
    #   - orientation='h' → barras horizontales (más fácil de comparar labels largos)
    #   - color=valores   → colorea cada barra según su valor numérico
    #   - color_continuous_scale='Viridis' → paleta de colores degradada (azul→verde→amarillo)
    fig_stats = px.bar(
        x=valores,
        y=nombres_stats,
        orientation='h',
        labels={'x': 'Puntos', 'y': 'Estadística'},
        color=valores,
        color_continuous_scale='Viridis',
        template="plotly_dark"   # fondo oscuro, más limpio visualmente
    )

    # Fijamos el eje X entre 0 y 255
    # Esto garantiza que la escala sea siempre la misma al cambiar de Pokémon,
    # permitiendo una comparación visual justa entre distintos Pokémon.
    fig_stats.update_xaxes(range=[0, 255])

    st.plotly_chart(fig_stats, width='stretch')


# MÉTRICAS DE COMPARACIÓN VS LA MEDIA DE KANTO
st.divider()
st.subheader(f"Rendimiento de {seleccion} vs La Media de Kanto")

# Calculamos la media de cada estadística sobre todos los 151 Pokémon.
medias_globales = datos_pokemon[stats_cols].mean()

# Creamos 4 columnas para las 4 métricas que vamos a mostrar
m1, m2, m3, m4 = st.columns(4)

# st.metric muestra: nombre de la métrica, valor actual y un "delta" (diferencia).
# El delta se colorea automáticamente en verde si es positivo y rojo si es negativo,
# lo que permite ver de un vistazo si el Pokémon supera o no la media.
# Usamos :.1f para mostrar el delta con un decimal de precisión.

m1.metric(
    "Puntos de Vida (HP)",
    pokemon_info['stat_hp'],
    # delta vs media
    f"{pokemon_info['stat_hp'] - medias_globales['stat_hp']:.1f}"
)
m2.metric(
    "Ataque",
    pokemon_info['stat_attack'],
    f"{pokemon_info['stat_attack'] - medias_globales['stat_attack']:.1f}"
)
m3.metric(
    "Defensa",
    pokemon_info['stat_defense'],
    f"{pokemon_info['stat_defense'] - medias_globales['stat_defense']:.1f}"
)
m4.metric(
    "Velocidad",
    pokemon_info['stat_speed'],
    f"{pokemon_info['stat_speed'] - medias_globales['stat_speed']:.1f}"
)


# DISTRIBUCIONES GENERALES (gráficos estáticos sobre toda la generación)
# Estos dos gráficos NO dependen del Pokémon seleccionado: muestran información
# global de los 151 Pokémon y sirven como contexto para interpretar mejor
# la ficha individual de arriba.
st.divider()
col_izq, col_der = st.columns(2)

# --- Gráfico izquierdo: histograma de tipos ---
with col_izq:
    # Cuenta cuántos Pokémon hay de cada tipo primario y los muestra como barras.
    # color="type_primary" asigna un color distinto a cada tipo automáticamente.
    fig_tipos = px.histogram(
        datos_pokemon,
        x="type_primary",
        title="Distribución de Tipos en Kanto",
        color="type_primary"
    )
    st.plotly_chart(fig_tipos, width='stretch')

# --- Gráfico derecho: dispersión Ataque vs Defensa ---
with col_der:
    # Scatter plot donde cada punto es un Pokémon.
    # Permite identificar visualmente los Pokémon más ofensivos, más defensivos
    # o equilibrados. Al pasar el ratón sobre un punto, hover_name muestra el nombre.
    fig_scatter = px.scatter(
        datos_pokemon,
        x="stat_attack",
        y="stat_defense",
        color="type_primary",   # colorea por tipo para detectar patrones por tipo
        hover_name="name",      # tooltip con el nombre al hacer hover
        title="Relación Ataque vs Defensa"
    )
    st.plotly_chart(fig_scatter, width='stretch')
