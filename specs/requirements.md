# Requisitos — BarberSync

> Responsable del aporte: Product / Spec Lead (Amir Reyes) y QA / DevOps Lead (Hector Ortega).
> Estado: versión inicial para Fase 2, alineada con `outcomes.md` y la propuesta de arquitectura/API.

## Requisitos funcionales

| ID | Descripción | Trazabilidad |
|---|---|---|
| RF-01 | El sistema debe permitir consultar el catálogo de barberos activos. | ODD: reserva autónoma. |
| RF-02 | El sistema debe permitir consultar el catálogo de servicios con duración y precio. | ODD: ver disponibilidad real. |
| RF-03 | El cliente debe poder consultar los horarios disponibles de un barbero para una fecha y servicio determinados. | ODD: disponibilidad en tiempo real. |
| RF-04 | El cliente debe poder reservar una cita seleccionando barbero, servicio e inicio de horario, proporcionando nombre y teléfono. | ODD: agendar de forma autónoma. |
| RF-05 | El sistema debe rechazar automáticamente reservas que se solapen con citas confirmadas del mismo barbero. | ODD: 0 % dobles reservas. |
| RF-06 | El sistema debe confirmar inmediatamente una reserva exitosa con identificador, fecha/hora y estado. | ODD: confirmación inmediata. |
| RF-07 | El barbero debe poder listar y consultar citas por fecha, barbero y estado. | ODD: automatizar agenda. |
| RF-08 | El sistema debe permitir cancelar lógicamente una cita confirmada, liberando el horario sin borrar el historial. | Regla de negocio RN-06. |
| RF-09 | El sistema debe reutilizar un cliente existente cuando el teléfono ya esté registrado. | Arquitectura ADR-P06. |

## Requisitos no funcionales

| ID | Descripción |
|---|---|
| RNF-01 | Tiempo de respuesta de consulta de disponibilidad < 500 ms en condiciones locales. |
| RNF-02 | Persistencia en SQLite para facilitar despliegue y demo local. |
| RNF-03 | Cobertura de tests automatizados ≥ 80 %. |
| RNF-04 | Pipeline CI/CD que ejecute lint y tests en cada push/PR a `main`. |
| RNF-05 | Contenerización con Docker para ejecución reproducible. |
| RNF-06 | Todas las fechas de entrada deben incluir zona horaria explícita; respuestas en `America/Panama`. |
| RNF-07 | El prototipo no incluye autenticación; los datos son ficticios y de demo. |
