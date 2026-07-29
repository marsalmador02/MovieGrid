"use strict";
// TODO: naming archivos en español
// 1. Se muestra un recuadro donde se indican en inglés el nombre del juego y las instrucciones, así como un botón de Start.
// 2. Al pulsar el botón de Start, se ejecuta pruebas_grid.py y se genera un archivo JSON con los datos de las películas y
//    actores. Se recibe esta información en el frontend: fila y columna 0 contienen los nombres de los actores y directores
//    que definen los cruces, y las otras filas y columnas contienen las respuestas válidas a los cruces de actores y
//    directores.
// 3. Se construye un grid 4x4 que se corresponde con la información recibida. La fila y columna 0 se muestran con los
//    nombres de los actores y directores, y las otras filas y columnas contienen botones que permiten al usuario introducir
//    sus respuestas por teclado. Al pulsar un botón/enter, se comprueba si la respuesta es correcta. Si lo es, se muestra
//    en esa casilla el nombre del actor/director y entre paréntesis el nombre de la película que los relaciona. Si no lo es,
//    se colorea la casilla de rojo y se muestra un mensaje de error. Se permite al usuario introducir respuestas hasta que
//    complete el grid.
// 4. Una vez completado el grid, se muestra un mensaje de felicitación y se ofrece la opción de volver a jugar.
Object.defineProperty(exports, "__esModule", { value: true });
//# sourceMappingURL=app.js.map