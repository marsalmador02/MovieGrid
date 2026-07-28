from app.core.database import SessionLocal
from app.models import Credit, Person, Movie

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


def personas_conectadas_a_pelicula(db, movie_id):
    """Personas acreditadas en esa película."""
    resultado = (
        db.query(Credit.person_id)
        .filter(Credit.movie_id == movie_id)
        .distinct()
        .all()
    )
    return [r[0] for r in resultado]


def personas_conectadas_a(db, tipo_eje, id_valor):
    """Punto de entrada único."""
    if tipo_eje == "persona":
        return personas_conectadas_a_persona(db, id_valor)
    elif tipo_eje == "pelicula":
        return personas_conectadas_a_pelicula(db, id_valor)
    else:
        raise ValueError(f"Tipo de eje desconocido: {tipo_eje}")

def respuestas_validas_para_celda(db, eje_fila, eje_columna):
    """Devuelve la lista de personas que cumplen con ambos criterios."""
    conectados_fila = personas_conectadas_a(db, eje_fila["tipo"], eje_fila["id"])
    conectados_columna = personas_conectadas_a(db, eje_columna["tipo"], eje_columna["id"])
    return list(set(conectados_fila) & set(conectados_columna))

db = SessionLocal()

eje_fila = {"tipo": "persona", "id": 500}
eje_columna = {"tipo": "pelicula", "id": 1}

respuestas = respuestas_validas_para_celda(db, eje_fila, eje_columna)

if respuestas:
    nombres = db.query(Person.full_name).filter(Person.person_id.in_(respuestas)).all()
    print(f"Personas que han trabajado con la persona {eje_fila['id']} y están acreditadas en la película {eje_columna['id']}: {nombres}")
else:
    print(f"No hay personas que hayan trabajado con la persona {eje_fila['id']} y estén acreditadas en la película {eje_columna['id']}.")

db.close()