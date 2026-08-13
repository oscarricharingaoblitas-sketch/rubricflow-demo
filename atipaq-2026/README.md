Exit code: 0
Wall time: 0.6 seconds
Output:
# RubricFlow â€” muestra no oficial ATIPAQ 2026

Muestra tÃ©cnica preparada a partir de las bases pÃºblicas de ATIPAQ 2026. Utiliza Ãºnicamente postulaciones ficticias y no representa una evaluaciÃ³n realizada, encargada ni aprobada por MisiÃ³n 3 o la Universidad CÃ©sar Vallejo.

## Criterios publicados

- MÃ©rito innovador: 30 puntos.
- Modelo de negocio: 15 puntos.
- Escalabilidad: 15 puntos.
- Equipo emprendedor: 40 puntos.

Las bases indican un mÃ­nimo total de 70 puntos por evaluador y al menos 25 puntos combinados en mÃ©rito innovador mÃ¡s escalabilidad por al menos un evaluador. `reference_check` muestra Ãºnicamente si el resultado automatizado alcanza esos lÃ­mites matemÃ¡ticos; nunca reemplaza la valoraciÃ³n del jurado.

## Ejecutar

```powershell
python grader.py synthetic_applications.csv --rubric atipaq_2026_rubric.csv -o results.csv
python -m unittest -v
```

El resultado conserva puntuaciÃ³n de evidencia, puntos ponderados y frases de respaldo para cada criterio. Antes de cualquier uso real se requiere calibraciÃ³n con ejemplos desidentificados revisados por el equipo evaluador.

Fuente oficial: https://www.mision3.com/wp-content/uploads/2026/03/BASES%20ATIPAQ%202026%20%28end%29.pdf

