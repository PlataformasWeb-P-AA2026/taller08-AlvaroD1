# taller08

## Integración de datos y uso de ORM

Integrar datos de un formato común y almacenarlos en sqlite / mysql / mariaDb


## Archivos proporcionados
* Fuente 1: jugadores_futbol.csv

## Acciones

1. Crear una base de datos en sqlite, llamada paises

2. Crear las siguientes entidades

2.1. Continente
2.2. Pais
2.3. Jugador

3. Leer la información de la fuente y migrar a las tablas de forma adecuada. Usar los conceptos de ORM

4. Generar app en Streamlit que permita visualizar un tabla con la siguiente información

En una tabla:

nombre_jugador  pais_nacimiento   pais_donde_juega  posicion  edad  numero_partidos_seleccion goles_seleccion continente

En una tabla

continente  número de jugadores de la base, número goles en función de los goles de cada jugador

En una tabla

paise número de jugadores de la base, número de goles en función de los goles de cada jugador

5. Probar el funcionamiento una base de datos mariaDB o mySQL

## Scripts y orden de ejecución

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Crear la base de datos SQLite (`data/paises.db`) y cargar los datos:
   ```bash
   python load_data.py
   ```
3. Ejecutar el frontend:
   ```bash
   streamlit run app.py
   ```

### Probar con MariaDB / MySQL

Configura `DATABASE_URL` antes de ejecutar los scripts (crea la base `paises` previamente en tu servidor). Ejemplos:

- 3MySQL:
  ```bash
  DATABASE_URL="mysql+pymysql://user:12345@127.0.0.1:3306/paises" python load_data.py
  DATABASE_URL="mysql+pymysql://user:12345@127.0.0.1:3306/paises" streamlit run app.py
  ```

## Entregables

* Script(s) replicables (indicar el orden de ejecución)
* Script de frontend
* Evidencia de la base de datos sqlite
* <img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/ccc725b1-fdb1-4013-bca1-bac01409b8ef" />

* Evidencia de la base de datos en mySQL
* <img width="704" height="371" alt="Captura desde 2026-05-26 12-36-17" src="https://github.com/user-attachments/assets/da5220d9-a1b4-4781-898e-d71e40338f26" />
 
* Evidencia del frontend funcionando
* <img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8aed3315-864c-4078-9175-b2980a2aef39" />

