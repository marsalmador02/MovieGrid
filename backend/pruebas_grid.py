from app.core.database import SessionLocal
from app.models import Credit

def peliculas_en_comun(db, person_id_a, person_id_b):
    """Devuelve la lista de movie_id donde ambas personas tienen un crédito."""
    creditos_a = db.query(Credit.movie_id).filter(Credit.person_id == person_id_a).scalar_subquery()

    resultado = (
        db.query(Credit.movie_id)
        .filter(Credit.person_id == person_id_b)
        .filter(Credit.movie_id.in_(creditos_a))
        .distinct()
        .all()
    )
    return [r[0] for r in resultado]


db = SessionLocal()


persona_a = 2227    # Nicole Kidman
persona_b = 500     # Tom Cruise

comunes = peliculas_en_comun(db, persona_a, persona_b)
print(f"Películas en común: {comunes}")

db.close()