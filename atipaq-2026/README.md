# RubricFlow — muestra no oficial ATIPAQ 2026

Muestra técnica preparada a partir de las bases públicas de ATIPAQ 2026. Utiliza únicamente postulaciones ficticias y no representa una evaluación realizada, encargada ni aprobada por Misión 3 o la Universidad César Vallejo.

## Criterios publicados

- Mérito innovador: 30 puntos.
- Modelo de negocio: 15 puntos.
- Escalabilidad: 15 puntos.
- Equipo emprendedor: 40 puntos.

Las bases indican un mínimo total de 70 puntos por evaluador y al menos 25 puntos combinados en mérito innovador más escalabilidad por al menos un evaluador. `reference_check` muestra únicamente si el resultado automatizado alcanza esos límites matemáticos; nunca reemplaza la valoración del jurado.

## Ejecutar

```powershell
python grader.py synthetic_applications.csv --rubric atipaq_2026_rubric.csv -o results.csv
python -m unittest -v
```

El resultado conserva puntuación de evidencia, puntos ponderados y frases de respaldo para cada criterio. Antes de cualquier uso real se requiere calibración con ejemplos desidentificados revisados por el equipo evaluador.

Fuente oficial: https://www.mision3.com/wp-content/uploads/2026/03/BASES%20ATIPAQ%202026%20%28end%29.pdf
