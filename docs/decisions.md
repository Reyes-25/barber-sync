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
