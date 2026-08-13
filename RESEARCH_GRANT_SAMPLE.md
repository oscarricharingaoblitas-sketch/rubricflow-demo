# RubricFlow — muestra para convocatorias de investigación

Ejemplo demostrativo para una convocatoria de subvenciones o tesis. El sistema ordena la primera revisión y deja la decisión final en manos del comité.

## Rúbrica configurable

| Criterio | Peso | Evidencia mínima esperada |
|---|---:|---|
| Relevancia y definición del problema | 20% | Problema delimitado, población y datos de respaldo |
| Rigor metodológico | 25% | Diseño, muestra, instrumentos y plan de análisis |
| Viabilidad | 20% | Cronograma, recursos, permisos y riesgos |
| Impacto académico o social | 15% | Resultados esperados, beneficiarios e indicadores |
| Presupuesto | 10% | Partidas justificadas y coherentes con las actividades |
| Capacidad del equipo | 10% | Roles, experiencia y dedicación verificable |

## Resultado de ejemplo

| Código | Puntaje | Estado | Evidencia detectada | Bandera para revisión humana |
|---|---:|---|---|---|
| INV-001 | 86/100 | Priorizable | Diseño cuasiexperimental; muestra de 180 participantes; cronograma de 8 meses; presupuesto por actividad | Confirmar autorización ética y cálculo de muestra |
| INV-002 | 61/100 | Requiere aclaración | Problema e impacto descritos; método general | No especifica instrumentos ni desglose presupuestal |
| INV-003 | 38/100 | Evidencia insuficiente | Objetivo general y población objetivo | Faltan método, cronograma, riesgos y presupuesto |

## Salida auditable

Por cada expediente se entrega un CSV con:

- puntaje total y por criterio;
- fragmentos de evidencia que justifican cada puntaje;
- información faltante;
- banderas de elegibilidad y consistencia;
- recomendación de revisión, nunca una decisión automática.

## Piloto de alcance fijo

- Hasta 50 expedientes.
- Una rúbrica y una ronda de calibración.
- Entrega en CSV revisable.
- Precio piloto: USD 95.
- Datos de muestra o anonimizados; no se solicitan datos sensibles para la demostración.

Demo general: https://oscarricharingaoblitas-sketch.github.io/rubricflow-demo/

Solicitud de piloto: https://github.com/oscarricharingaoblitas-sketch/rubricflow-demo/issues/new?template=pilot-request.yml
