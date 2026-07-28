import random
from sqlalchemy import func
from app.core.database import SessionLocal
from app.models import Credit, Person


def obtener_pool_de_personas(db, minimo_creditos=5):
    """Person_id con al menos N créditos, para asegurar que tengan
    suficientes conexiones como para ser un buen eje de grid."""
    resultado = (
        db.query(Credit.person_id, func.count(Credit.movie_id).label("num_creditos"))
        .group_by(Credit.person_id)
        .having(func.count(Credit.movie_id) >= minimo_creditos)
        .all()
    )
    return [r[0] for r in resultado]


def personas_conectadas_a_persona(db, person_id):
    """Personas que han trabajado con person_id (comparten alguna película)."""
    peliculas_de_la_persona = (
        db.query(Credit.movie_id)
        .filter(Credit.person_id == person_id)
        .scalar_subquery()
    )
    resultado = (
        db.query(Credit.person_id)
        .filter(Credit.movie_id.in_(peliculas_de_la_persona))
        .filter(Credit.person_id != person_id)
        .distinct()
        .all()
    )
    return [r[0] for r in resultado]


def generar_grid_solo_personas(db, pool, max_intentos=200):
    """Elige 3 personas para filas y 3 para columnas, comprobando que
    las 9 intersecciones tengan al menos una respuesta válida."""

    for intento in range(max_intentos):
        elegidos = random.sample(pool, 6)
        filas, columnas = elegidos[:3], elegidos[3:]

        conectados = {
            persona_id: personas_conectadas_a_persona(db, persona_id)
            for persona_id in elegidos
        }

        grid_valido = True
        respuestas_grid = {}

        for fila in filas:
            for columna in columnas:
                interseccion = set(conectados[fila]).intersection(conectados[columna])
                if not interseccion:
                    grid_valido = False
                    break
                respuestas_grid[(fila, columna)] = interseccion
            if not grid_valido:
                break

        if grid_valido:
            print(f"Grid válido encontrado en el intento {intento + 1}")
            return filas, columnas, respuestas_grid

    raise RuntimeError(f"No se encontró un grid válido tras {max_intentos} intentos")


db = SessionLocal()

pool = obtener_pool_de_personas(db, minimo_creditos=5)
print(f"Pool de candidatos: {len(pool)} personas")

filas, columnas, respuestas = generar_grid_solo_personas(db, pool)

nombres = {p.person_id: p.full_name for p in db.query(Person).filter(Person.person_id.in_(filas + columnas))}

print("\nFilas:   ", [nombres[f] for f in filas])
print("Columnas:", [nombres[c] for c in columnas])

db.close()