# Decisiones del proyecto

<!-- barbersync-julio-sdd-decisions-20261117 -->
## Propuestas de arquitectura — 17 de noviembre de 2026

**Autor del aporte:** Julio Gudiño. **Estado de todas las decisiones:** propuestas, pendientes de revisión del equipo y de ODD/requisitos.

| ID | Propuesta | Razón y consecuencia |
|---|---|---|
| ADR-P01 | Python, FastAPI, SQLAlchemy y SQLite. | Facilita la demo local. Se debe validar que la guía permita SQLite y confirmar si hace falta una interfaz web. |
| ADR-P02 | Separar API, servicios y persistencia. | Las reglas se prueban sin depender de detalles HTTP; el servicio controla una única transacción. |
| ADR-P03 | Reservas con intervalos `[inicio, fin)` y transacción de escritura antes de comprobar conflictos. | Permite citas adyacentes y evita carreras entre solicitudes si todos los caminos de escritura respetan el protocolo. El índice único es solo una defensa adicional. |
| ADR-P04 | UTC canónico en persistencia y desplazamiento explícito en HTTP. | Evita comparar horas ambiguas o mezclar formatos. Los filtros de día se interpretan en Panamá. |
| ADR-P05 | Precio en centavos enteros; cadena decimal en API. | Evita depender de precisión decimal implícita en SQLite. |
| ADR-P06 | Cliente reutilizado por teléfono normalizado y cancelación lógica. | Evita duplicados por formato y conserva historial. No resuelve autenticación; alcance limitado a la demo local con datos ficticios. |
| ADR-P07 | Alcance base sin `blocked_slots`. | El borrador recibido ya conocía el ejemplo de almuerzo. Una ampliación posterior debe registrar cuándo se solicitó y si es un ejercicio simulado. |

No se ha consultado la guía original del profesor en esta revisión. Estas propuestas no reemplazan `outcomes.md`, `requirements.md`, `business-rules.md` ni la aprobación de otro integrante.

<!-- barbersync-julio-guide-decisions-20261117 -->
## Contraste académico — 17 de noviembre de 2026

Referencia: guía `DSaIA-Proyecto2.pdf`, Proyecto #2, profesor Regis Rivera.

| ID | Hallazgo o propuesta | Estado |
|---|---|---|
| ADR-G01 | La guía permite cualquier lenguaje, base de datos y stack, documentados en `architecture.md` (p. 3, punto 10). | Hecho verificado en la guía. La elección de Python/SQLite sigue pendiente de ratificación del equipo. |
| ADR-G02 | La guía no prescribe interfaz web ni proveedor de despliegue. El ODD publicado exige reserva autónoma; se propone una interfaz HTML/CSS/JavaScript y se distingue la demo de una disponibilidad real 24/7. | Libertad verificada en la guía; propuesta de interfaz y despliegue pendientes de acuerdo del equipo. |
| ADR-G03 | Se requiere ODD antes de SDD, luego código, pruebas y valor al usuario (pp. 1–2). | Requisito confirmado. El adelanto técnico actual se mantiene como borrador. |
| ADR-G04 | El cambio se introduce a mitad del desarrollo y debe actualizar también criterios de aceptación y plan/tareas (p. 3, punto 13). | Requisito confirmado; secuencia propuesta en `specs/implementation-plan.md`. |
| ADR-G05 | Rotar los tres roles según ciclos (p. 1). | Requisito confirmado; reparto de tres ciclos propuesto, todavía no acordado ni ejecutado. |
| ADR-G06 | Las pruebas mínimas incluyen unidades, reglas críticas, conflictos, validaciones de usuario y aceptación; doble reserva requiere automatización (p. 3, punto 12). | Requisito confirmado; implementación y resultados pendientes. |
| ADR-G07 | Integrar el `main` observado en `6316a22` a la rama de Julio y conservar el registro de IA de Amir junto al de Julio. | Integración preparada; se verificará con la ejecución real de Git. |

Estas entradas complementan las propuestas anteriores. La lectura de la guía confirma requisitos del curso, pero no equivale a una aprobación de las decisiones de dominio por parte del equipo.
