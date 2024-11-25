TPO - VIDEO JUEGO DE AUTOS.


Instrucciones para el programador:
- pip install pillow
- Run python file en TPO.py
Instrucciones para hacer pruebas unitarias:
- Navegar por consola hasta la carpeta "games"
- Ejecutar el comando: python -m unittest discover -s tests


Instrucciones del juego:
- Utilice las flechas del teclado para mover el auto:
⬆️ Flecha arriba: Mover el auto hacia arriba.
⬇️ Flecha abajo: Mover el auto hacia abajo.
⬅️ Flecha izquierda: Mover el auto hacia la izquierda.
➡️ Flecha derecha: Mover el auto hacia la derecha.
- Evite los obstáculos:
Los autos y los cactus son obstáculos que debe evitar.
Si choca con un obstáculo, el juego terminará.
- Manténgase dentro de la carretera:
No se salga de los márgenes de la carretera.
- Pausar el juego:
Presione la barra espaciadora para pausar o reanudar el juego.
- Objetivo del juego:
Recorra la mayor distancia posible sin chocar con los obstáculos.
A medida que avance, la velocidad del juego aumentará.
- Puntuación:
La puntuación se basa en la distancia recorrida.
Intente superar su puntuación más alta.


Progreso / Ideas
[o] iniciado de proyecto con pygame. [o] definicion de la carretera. [o] definicion de imagenes. [o] creacion de limites. [o] creacion de obstaculos. [o] seteo de game over. [o] definicion de dificultad. [o] modularizacion de codigo. 160 lineas aprx es el optimo. [o] agregado de README.md. [o] creacion de score. [o] creacion de niveles. [o] modificacion de dificultad. [o] agregado de mas obstaculos con diferente imagen. [o] que se grabe el record y un leaderboard de maximo 10 max scores. [o] pantalla de record al romperlo (game over). [o] que la velocidad del auto y la carretera arranque en un valor bajo y vaya aumentando a lo largo del juego. [o] velocidad maxima del auto entre 20 y 35, velocidad maxima de obstaculos entre 20 y 30, velocidad maxima de la carretera entre 50 y 100. [o] al perder el juego que aparezca una pantalla game over con el score final y un boton de Salir para cerrar el juego y otro boton para jugar de nuevo. [o] utilizar pruebas unitarias para comprobar la logica del juego (por ejemplo, si la puntuacion y distancia es 0, quiere decir que el juego no arranco. Si superaste cierta cantidad de distancia deberias estar en dicho nivel) [o] que la barra de space sea pausa. [o] diseño. [o] pep8 correcciones. [o] Mejorar el readme con readme.so (WEB) [o] Mejorar el leaderboard (que no se repitan los mismos records con mismos nombres)