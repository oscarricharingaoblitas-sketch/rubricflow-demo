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
| INV-001 | 90/100 | Evidencia sólida | Diseño cuasiexperimental; muestra de 180 participantes; cronograma de 8 meses; presupuesto por actividad | Verificar las afirmaciones y tomar la decisión final |
| INV-002 | 25.5/100 | Evidencia insuficiente | Problema, muestra e instrumento mencionados | Faltan análisis, viabilidad, presupuesto y capacidad del equipo |
| INV-003 | 0/100 | Evidencia insuficiente | No se detectó evidencia explícita para la rúbrica | Solicitar información antes de evaluar |

Estos resultados se generaron con el motor publicado, la rúbrica y tres postulaciones sintéticas. Pueden descargarse y reproducirse desde los enlaces de la demo.

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
