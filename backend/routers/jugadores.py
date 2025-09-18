from fastapi import APIRouter
from backend.database import get_connection

router = APIRouter()


@router.get("/create-jugadores/")
def create_jugadores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            equipo TEXT NOT NULL,
            posicion TEXT NOT NULL,
            descripcion TEXT,
            imagen TEXT,
            video TEXT,
            pais TEXT
        )
    ''')

    conn.commit()
    conn.close()
    return {"message": "Tabla jugadores creada correctamente"}


@router.get("/init-jugadores/")
def init_jugadores():
    """
    Inserta 20 jugadores (solo los campos: nombre, equipo, posicion, descripcion, imagen, video, pais).
    Llama primero a /create-jugadores/ si aún no existe la tabla.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # limpiar tabla antes de insertar
    cursor.execute("DELETE FROM jugadores")

    jugadores = [
        ("Lionel Messi", "Inter Miami", "Delantero",
         "Considerado uno de los mejores de todos los tiempos: múltiples Balones de Oro, regate exquisito, visión y definición. Creador de ocasiones y líder creativo.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Lionel-Messi-Argentina-2022-FIFA-World-Cup_(cropped).jpg?width=330",
         "https://www.youtube.com/embed/bvZ8-neR1O8", "Argentina"),

        ("Cristiano Ronaldo", "Al Nassr", "Delantero",
         "Goleador histórico y atleta excepcional: potencia física, salto y remates poderosos; especialista en momentos decisivos.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Cristiano_Ronaldo.jpg?width=330",
         "https://www.youtube.com/embed/4q2pFjrHRIU", "Portugal"),

        ("Kylian Mbappé", "Real Madrid", "Delantero",
         "Velocidad explosiva y definición clínica. Dominante en transiciones y letal en el uno contra uno; estrella consagrada a temprana edad.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Kylian_Mbapp%C3%A9_(cropped).jpg?width=330",
         "https://www.youtube.com/embed/sy6jfCmskJA", "Francia"),

        ("Neymar Jr", "Al-Hilal", "Delantero",
         "Técnica brillante, regate creativo y gran capacidad para generar juego y asistencias desde la banda. Determinante en combinaciones ofensivas.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Neymar_2018_(cropped).jpg?width=330",
         "https://www.youtube.com/embed/uAk-S8y48Yg", "Brasil"),

        ("Kevin De Bruyne", "Manchester City", "Centrocampista",
         "Mediocentro con pase milimétrico y gran visión. Creador de juego y asistencias de auténtico calibre; peligroso en disparo desde fuera del área.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Kevin_De_Bruyne.jpg?width=330",
         "https://www.youtube.com/embed/expKD0SJTIQ", "Bélgica"),

        ("Robert Lewandowski", "FC Barcelona", "Delantero",
         "Delantero puro y goleador nato: definición increíble, movimientos en el área y eficacia implacable frente al arco.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Robert_Lewandowski.jpg?width=330",
         "https://www.youtube.com/embed/DL6VnHQEeOI", "Polonia"),

        ("Luka Modrić", "Real Madrid", "Centrocampista",
         "Maestro del ritmo y la pausa: control, pases precisos y visión táctica; determinante en fases de control del partido.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Luka_Modric.jpg?width=330",
         "https://www.youtube.com/embed/vaROYrOudU8", "Croacia"),

        ("Erling Haaland", "Manchester City", "Delantero",
         "Ariete moderno: combinación de potencia, velocidad y remate letal. Alta eficacia goleadora en todas las competiciones.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Erling_Haaland_2023.jpg?width=330",
         "https://www.youtube.com/embed/A_m7v9hVATw", "Noruega"),

        ("Mohamed Salah", "Liverpool", "Delantero",
         "Velocidad y definición por la banda: gran regularidad goleadora y decisivo en los partidos importantes. Referente ofensivo de su selección.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Mohamed_Salah_2017.jpg?width=330",
         "https://www.youtube.com/embed/iXA93SGfVS8", "Egipto"),

        ("Virgil van Dijk", "Liverpool", "Defensa",
         "Central imponente y lector del juego: anticipación, solvencia aérea y liderazgo en la zaga; pilar defensivo del equipo.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Virgil_van_Dijk_2019.jpg?width=330",
         "https://www.youtube.com/embed/YOFL2uhd8GM", "Países Bajos"),

        ("Karim Benzema", "Al-Ittihad", "Delantero",
         "Delantero inteligente y técnico: movilidad, técnica de remate y goleador en momentos decisivos; figura en competiciones europeas.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/KarimBenzema.jpg?width=330",
         "https://www.youtube.com/embed/S0Xd1IShdbI", "Francia"),

        ("Harry Kane", "Bayern Múnich", "Delantero",
         "Nueve completo: gran definición, visión para asistir y disparo potente. Consistencia goleadora temporada a temporada.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Harry_Kane_2023.jpg?width=330",
         "https://www.youtube.com/embed/VVEfg4wRoao", "Inglaterra"),

        ("Sergio Ramos", "Sevilla", "Defensa",
         "Veterano con carácter: fortaleza aérea, capacidad goleadora en fases a balón parado y liderazgo defensivo con experiencia en grandes torneos.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Sergio_Ramos.jpg?width=330",
         "https://www.youtube.com/embed/H0GVemJOmIg", "España"),

        ("Pedri", "FC Barcelona", "Centrocampista",
         "Centrocampista joven con gran control, visión entre líneas y madurez táctica. Excelente conservación y manejo del tempo del juego.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Pedri.jpg?width=330",
         "https://www.youtube.com/embed/1u7AB3cseiA", "España"),

        ("Gavi", "FC Barcelona", "Centrocampista",
         "Jugador de alta intensidad: recuperación, pase corto preciso y gran despliegue físico; pieza importante en el mediocampo moderno.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Gavi_(footballer).jpg?width=330",
         "https://www.youtube.com/embed/WhzAjPCQsLI", "España"),

        ("Antoine Griezmann", "Atlético de Madrid", "Delantero",
         "Ofensivo polivalente: movilidad entre líneas, buen tiro y capacidad de asociación; goleador y asistente en momentos clave.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Antoine_Griezmann.jpg?width=330",
         "https://www.youtube.com/embed/pctFQjuEpSY", "Francia"),

        ("Casemiro", "Manchester United", "Centrocampista",
         "Volante defensivo con gran capacidad de recuperación y protección de la defensa; imprescindible para el equilibrio táctico del equipo.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Casemiro.jpg?width=330",
         "https://www.youtube.com/embed/omaefUXe9QQ", "Brasil"),

        ("Marc-André ter Stegen", "FC Barcelona", "Portero",
         "Portero moderno: reflejos, juego con los pies y capacidad para iniciar jugadas desde la portería; seguro en los mano a mano.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Marc-Andr%C3%A9_ter_Stegen.jpg?width=330",
         "https://www.youtube.com/embed/-WgTpFzBbVY", "Alemania"),

        ("Thibaut Courtois", "Real Madrid", "Portero",
         "Arquero de gran envergadura y reflejos: intervenciones decisivas y dominio del área chica en partidos de alta exigencia.",
         "https://commons.wikimedia.org/wiki/Special:FilePath/Thibaut_Courtois_-_02.jpg?width=330",
         "https://www.youtube.com/embed/2untjoE62Qw", "Bélgica"),

        ("Andrés Iniesta", "Emirates Club", "Centrocampista",
         "Leyenda del fútbol español: maestro del pase y la pausa. Condujo el juego de Barcelona con su técnica sublime y lectura perfecta de espacios. Ganador del Mundial 2010 y múltiples Champions League. Su control del balón y entrega en el mediocampo lo hacen un genio imitado pero inalcanzable.",
         "https://upload.wikimedia.org/wikipedia/commons/5/52/Andres_Iniesta.jpg",
         "https://www.youtube.com/embed/fPzCFu-bDEI", "España"),
    ]

    cursor.executemany(
        "INSERT INTO jugadores (nombre, equipo, posicion, descripcion, imagen, video, pais) VALUES (?, ?, ?, ?, ?, ?, ?)",
        jugadores
    )

    conn.commit()
    conn.close()
    return {"message": "Jugadores insertados correctamente", "inserted": len(jugadores)}


@router.get("/jugadores")
def get_jugadores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, equipo, posicion, imagen FROM jugadores")
    data = [
        {"id": r[0], "nombre": r[1], "equipo": r[2], "posicion": r[3], "imagen": r[4]}
        for r in cursor.fetchall()
    ]
    conn.close()
    return data


@router.get("/jugadores/{jugador_id}")
def get_jugador(jugador_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, equipo, posicion, descripcion, imagen, video, pais FROM jugadores WHERE id=?",
                   (jugador_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"error": "Jugador no encontrado"}
    return {
        "id": row[0],
        "nombre": row[1],
        "equipo": row[2],
        "posicion": row[3],
        "descripcion": row[4],
        "imagen": row[5],
        "video": row[6],
        "pais": row[7]
    }
