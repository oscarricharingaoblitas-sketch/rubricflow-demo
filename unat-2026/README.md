# RubricFlow - muestra no oficial UNAT 2026

Muestra tecnica independiente preparada a partir de las bases publicas del Concurso de Otorgamiento de Subvenciones de Tesis 2026 de la UNAT. Usa unicamente propuestas ficticias; no representa una evaluacion realizada, encargada ni aprobada por la UNAT.

## Rubrica publicada

- Pertinencia y alineacion tematica: 20 puntos.
- Calidad cientifica y metodologica: 25 puntos.
- Coherencia del plan de actividades y presupuesto: 20 puntos.
- Idoneidad del asesor y/o coasesor: 15 puntos.
- Potencial de impacto y aplicabilidad: 15 puntos.
- Integridad del expediente y calidad de la presentacion: 5 puntos.

Las bases clasifican 80-100 como Excelente/Seleccionado, 70-79 como Bueno/Seleccionado en lista de espera, 60-69 como Regular/Desaprobado y menos de 60 como Deficiente/Descalificado. El campo `published_result_if_score_confirmed` solo aplica la banda matematica al puntaje preliminar; `human_review_required` siempre permanece en `YES`.

## Ejecutar

```powershell
python grader.py synthetic_proposals.csv --rubric unat_2026_rubric.csv -o results.csv
python -m unittest -v
```

El resultado conserva puntuacion de evidencia, puntos y frases de respaldo por criterio. Antes de cualquier uso real se requiere calibracion con expedientes desidentificados y revisados por los pares evaluadores.

Fuente oficial: https://www.gob.pe/institucion/unat/informes-publicaciones/8405217-convocatoria-para-el-concurso-de-otorgamiento-de-subvenciones-economicas-para-trabajos-de-investigacion-y-o-tesis-a-favor-de-estudiantes-de-pregrado-y-graduados-de-la-unat-2026
