# RubricFlow - muestra no oficial Demo Day Belcorp/Emprende UP 2026

Matriz técnica independiente preparada a partir de los términos públicos del programa Aceleradora de Fundación Belcorp y Emprende UP. Usa únicamente finalistas ficticias y no representa una evaluación realizada, encargada ni aprobada por las organizaciones.

## Qué conserva

- Los cinco criterios publicados para pitch y entrevista: viabilidad y gestión; crecimiento y escalabilidad; liderazgo; compromiso; claridad y coherencia.
- La condición publicada de asistencia superior al 85%.
- La exigencia de completar los formularios de diagnóstico inicial y de salida.
- Evidencia textual y vacíos por criterio.

Los términos no publican ponderaciones para los cinco criterios. Por ello, esta muestra no inventa pesos ni produce un puntaje oficial. `average_evidence_coverage_percent` mide únicamente qué proporción de señales de evidencia aparece en el texto; el puntaje del jurado siempre es obligatorio.

## Ejecutar

```powershell
python grader.py synthetic_finalists.csv --criteria belcorp_demo_day_criteria.csv -o results.csv
python -m unittest -v
```

Fuente oficial: https://emprendeup.pe/programa-aceleradora-mujeres-sin-limites-2026/terminos-y-condiciones-del-programa/
