# 👾 Dashboard Pokémon: 1ª Generación

Dashboard interactivo para explorar y analizar los 151 Pokémon de la región de Kanto, construido con **Streamlit** y **Plotly**.

---

## 🚀 Instalación y puesta en marcha

### 1. Clonar el repositorio

```bash
git clone https://github.com/L0rdxavi97/Dashboard_Pokemon_Streamlit.git
cd Dashboard_Pokemon_Streamlit
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Preparar los datos

El CSV con los datos de los 151 Pokémon debe estar en `data/pokemon_gen1.csv`. Si aún no existe, ejecúta el script de ingesta para generarlo desde la PokeAPI:

```bash
python pokeapi_batch.py
```

Esto descargará automáticamente los datos y creará el fichero `data/pokemon_gen1.csv`.

### 4. Lanzar el dashboard

```bash
streamlit run main.py
```

Se abrirá el navegador en `http://localhost:8501`.

---

## 📁 Estructura del proyecto

```
.
├── main.py                # Aplicación principal de Streamlit
├── pokeapi_batch.py       # Script de ingesta de datos desde la PokeAPI
├── requirements.txt       # Dependencias Python
├── data/
│   └── pokemon_gen1.csv   # Dataset generado (crear con pokeapi_batch.py)
└── README.md
```

---

## ✨ Funcionalidades

- **Selector de Pokémon** — elige cualquiera de los 151 para ver su ficha completa.
- **Artwork oficial** — imagen de alta calidad del Pokémon seleccionado.
- **Gráfico de estadísticas** — barras horizontales con HP, Ataque, Defensa, Ataque Especial, Defensa Especial y Velocidad, con escala fija (0–255) para facilitar la comparación.
- **Métricas vs la media de Kanto** — comparativa de HP, Ataque, Defensa y Velocidad frente al promedio de la generación, con indicadores de color automáticos.
- **Distribución de tipos** — histograma con todos los tipos primarios presentes en Kanto.
- **Dispersión Ataque vs Defensa** — scatter plot de todos los Pokémon coloreado por tipo.

---

## 🗄️ Dataset (`pokemon_gen1.csv`)

El script `pokeapi_batch.py` extrae los siguientes campos para cada Pokémon:

| Campo | Descripción |
|---|---|
| `pokemon_id` | ID nacional (1–151) |
| `name` | Nombre en minúsculas |
| `is_legendary` | Booleano (`True` para los 5 legendarios) |
| `rarity` | `common`, `uncommon`, `rare` o `legendary` |
| `type_primary` / `type_secondary` | Tipos del Pokémon |
| `types` | Tipos concatenados con coma |
| `height_dm` | Altura en decímetros |
| `weight_hg` | Peso en hectogramos |
| `base_experience` | Experiencia base al derrotarlo |
| `stat_hp` … `stat_speed` | Las 6 estadísticas base |
| `abilities` / `hidden_ability` | Habilidades normales y oculta |
| `sprite_url` | URL del artwork oficial |

> **Fuente de datos:** [PokéAPI](https://pokeapi.co/) — API REST gratuita y sin autenticación.

---

## 📦 Dependencias

| Paquete | Uso |
|---|---|
| `streamlit` | Framework del dashboard |
| `plotly` | Gráficos interactivos |
| `pandas` | Manipulación del dataset |
| `requests` | Llamadas HTTP a la PokeAPI (solo `pokeapi_batch.py`) |

---

## 📝 Notas

- El script de ingesta incluye un retardo de **0,3 s entre peticiones** (comentado por defecto) para respetar los límites de la PokeAPI en entornos de producción. Actívalo descomentando `time.sleep(DELAY_BETWEEN)` en `pokeapi_batch.py` si recibes errores 429.
- La clasificación de **rareza** es una heurística propia basada en el tipo primario y no corresponde a ninguna mecánica oficial del juego.
