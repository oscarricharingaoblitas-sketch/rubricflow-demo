# RubricFlow - muestra no oficial Crea y Emprende 2026

Demostracion tecnica independiente para la categoria B del Concurso Nacional Crea y Emprende 2026. Conserva los criterios y topes publicados por MINEDU, usa solo proyectos y puntajes ficticios y no sustituye la deliberacion del jurado.

## Que valida

- Rubrica del proyecto: 7 criterios, escala entera 1-4, maximo 28.
- Rubrica del portafolio: 12 criterios, escala entera 1-4, maximo 48.
- Presentacion en Expoferia: 5 criterios, escala entera 1-4, maximo 20.
- Consolidado de exactamente tres jurados (J1, J2 y J3), conforme al formato D14.
- Rechazo de puntajes fuera de rango, fraccionarios, faltantes o con jurados duplicados.

El promedio y el orden son ayudas auditables. No adjudican ganadores y la decision permanece en el jurado humano.

## Ejecutar

```powershell
python grader.py synthetic_jury_scores.csv --rubric crea_y_emprende_2026_category_b_rubric.csv -o results.csv
python -m unittest -v
```

Fuentes oficiales:

- Bases 2026: https://www.gob.pe/institucion/minedu/informes-publicaciones/8263999-bases-crea-y-emprende-2026
- Campana 2026: https://www.gob.pe/institucion/minedu/campanas/64639-concurso-nacional-crea-y-emprende-2026

RubricFlow no esta afiliado ni aprobado por MINEDU. Esta muestra no contiene datos de estudiantes reales.
