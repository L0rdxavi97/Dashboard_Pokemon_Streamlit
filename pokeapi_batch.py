import csv
import logging
import time
from pathlib import Path

import requests

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pokeapi-batch")

# ── Configuración ─────────────────────────────────────────────────────────────
POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"
GEN1_RANGE = range(1, 152)          # IDs 1-151
DELAY_BETWEEN = 0.3
# OUTPUT_DIR = Path("data")
# CSV_PATH = OUTPUT_DIR / "pokemon_gen1.csv"
CSV_PATH = Path("data/pokemon_gen1.csv")

LEGENDARY_IDS = {144, 145, 146, 150, 151}


# ── Extracción y normalización ────────────────────────────────────────────────

def fetch_pokemon(pokemon_id: int) -> dict | None:
    """Descarga y normaliza un Pokémon de la PokeAPI."""
    url = f"{POKEAPI_BASE}/{pokemon_id}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as exc:
        log.error("Error descargando pokemon_id=%d: %s", pokemon_id, exc)
        return None

    types_raw = data.get("types", [])
    types_sorted = sorted(types_raw, key=lambda t: t["slot"])
    type_list = [t["type"]["name"] for t in types_sorted]
    type_primary = type_list[0] if type_list else "unknown"
    type_secondary = type_list[1] if len(type_list) > 1 else None

    stats_raw = {s["stat"]["name"]: s["base_stat"]
                 for s in data.get("stats", [])}

    abilities = [
        a["ability"]["name"]
        for a in data.get("abilities", [])
        if not a.get("is_hidden", False)
    ]
    hidden_ability = next(
        (a["ability"]["name"]
         for a in data.get("abilities", []) if a.get("is_hidden")),
        None,
    )

    sprites = data.get("sprites", {})
    sprite_url = (
        sprites.get("other", {})
        .get("official-artwork", {})
        .get("front_default")
        or sprites.get("front_default")
    )

    if pokemon_id in LEGENDARY_IDS:
        rarity = "legendary"
    elif type_primary in {"dragon", "ghost", "psychic", "ice"}:
        rarity = "rare"
    elif type_primary in {"fire", "electric", "rock", "fighting", "ground"}:
        rarity = "uncommon"
    else:
        rarity = "common"

    return {
        "pokemon_id":       pokemon_id,
        "name":             data["name"],
        "is_legendary":     pokemon_id in LEGENDARY_IDS,
        "rarity":           rarity,
        "type_primary":     type_primary,
        "type_secondary":   type_secondary,
        "types":            ",".join(type_list),
        "height_dm":        data.get("height", 0),
        "weight_hg":        data.get("weight", 0),
        "base_experience":  data.get("base_experience", 0),
        "stat_hp":          stats_raw.get("hp", 0),
        "stat_attack":      stats_raw.get("attack", 0),
        "stat_defense":     stats_raw.get("defense", 0),
        "stat_sp_attack":   stats_raw.get("special-attack", 0),
        "stat_sp_defense":  stats_raw.get("special-defense", 0),
        "stat_speed":       stats_raw.get("speed", 0),
        "abilities":        ",".join(abilities),
        "hidden_ability":   hidden_ability,
        "sprite_url":       sprite_url,
    }


def fetch_all_gen1() -> list[dict]:
    """Descarga los 151 Pokémon con barra de progreso en consola."""
    results = []
    total = len(GEN1_RANGE)

    for i, pid in enumerate(GEN1_RANGE, start=1):
        pokemon = fetch_pokemon(pid)
        if pokemon:
            results.append(pokemon)
            log.info(
                "[%3d/%d] ✓ #%03d %-12s  tipo=%-10s  rareza=%s",
                i, total, pid, pokemon["name"],
                pokemon["type_primary"], pokemon["rarity"],
            )
        else:
            log.warning("[%3d/%d] ✗ #%03d  → omitido por error", i, total, pid)

        # if i < total:
        #     time.sleep(DELAY_BETWEEN)

    return results


# ── Guardado ──────────────────────────────────────────────────────────────────

def save_csv(data: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(data[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    log.info("CSV guardado en: %s  (%d registros)", path, len(data))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("═" * 60)
    log.info("  PokeAPI Batch Ingestion — Generación 1 (IDs 1-151)")
    log.info("═" * 60)

    pokemons = fetch_all_gen1()

    if not pokemons:
        log.critical(
            "No se descargó ningún Pokémon. Revisa la conexión a internet.")
        raise SystemExit(1)

    log.info("\nDescargados %d/%d Pokémon correctamente.\n", len(pokemons), 151)

    save_csv(pokemons, CSV_PATH)


if __name__ == "__main__":
    main()
