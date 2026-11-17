# Arquitectura: BarberSync

> Responsable: Julio Gudiño — Architecture / Development Lead.
> Estado: propuesta técnica de Fase 2 (SDD), pendiente de revisión del equipo.
> Revisión: 17 de noviembre de 2026. Rama: `docs/arquitectura-julio`.

## 1. Alcance y dependencias

BarberSync propone gestionar reservas sin solapar las citas confirmadas de un mismo barbero. Este documento describe una arquitectura por implementar; no acredita código funcionando ni pruebas aprobadas.

En la revisión del repositorio, `outcomes.md`, `requirements.md`, `business-rules.md` y `acceptance-criteria.md` todavía estaban vacíos. Esta propuesta deberá contrastarse con esos documentos y con la guía original del profesor antes de aprobar el diseño. La aprobación del Issue #1 sigue pendiente.

### Supuestos por validar

| ID | Propuesta provisional | Validación pendiente |
|---|---|---|
| A01 | Primera demostración mediante API y documentación interactiva. | Confirmar con Product si el entregable exige también interfaz web para clientes y barberos. |
| A02 | Python, FastAPI y SQLite para una aplicación local de alcance académico. | Confirmar tecnologías permitidas en la guía y acuerdo del equipo. |
| A03 | Una barbería; horario común de lunes a sábado, de 09:00 a 18:00. | Product debe incorporarlo o corregirlo en las reglas de negocio. |
| A04 | Zona `America/Panama`; comienzos cada 5 minutos; duración según servicio. | Validar calendario y duración con Product y QA. |
| A05 | Datos ficticios; teléfono panameño como clave de cliente; sin autenticación en la demo local. | No confundir identificación con autenticación. Acordar controles e interfaz antes de publicar para usuarios reales. |
| A06 | Cancelación lógica; un segundo intento de cancelación devuelve 409. | Validar con Product y QA. |

## 2. Tecnologías propuestas

| Componente | Tecnología | Motivo |
|---|---|---|
| Lenguaje | Python 3.11 o superior | Compatible con el diseño inicial y las herramientas de prueba propuestas. |
| API | FastAPI, Pydantic y Uvicorn | Contratos de entrada/salida y documentación en `/docs`. |
| Persistencia | SQLite en un archivo local | Instalación sencilla y transacciones suficientes para la demo. |
| Acceso a datos | SQLAlchemy 2.x, API síncrona | Modelos y una unidad de trabajo por operación. |
| Pruebas | pytest y TestClient de FastAPI, con httpx | Pruebas de reglas, API y persistencia. |
| Colaboración | Git y GitHub | Issues, ramas, commits, PR y revisión por otro integrante. |

Antes de implementar se fijarán versiones compatibles en el archivo de dependencias. SQLite es una propuesta, no un requisito verificado del profesor. La alternativa Node.js + Express requeriría revisar dependencias, estructura, transacciones y pruebas; no basta con cambiar el nombre del stack.

## 3. Capas y responsabilidades

| Capa | Responsabilidad | Dependencia |
|---|---|---|
| Routers y schemas | Recibir HTTP, validar estructura y traducir resultados a respuestas. | Servicios. |
| Servicios | Aplicar reglas de reserva, horario, cliente y cancelación. | Unidad de trabajo y repositorios. |
| Repositorios y modelos | Consultar y persistir datos con la conexión recibida. | SQLite mediante SQLAlchemy. |

Los servicios controlan la transacción completa. Un repositorio no realiza commits independientes; la base de datos refuerza la integridad mediante claves, checks e índices.

### Estructura prevista

| Ruta | Contenido por implementar |
|---|---|
| `src/barbersync/main.py` | Aplicación y registro de routers. |
| `src/barbersync/config.py` | Archivo SQLite, zona horaria, calendario y tiempo de espera. |
| `src/barbersync/database.py` | Conexiones, sesiones, claves foráneas y unidad de trabajo. |
| `src/barbersync/models/` | Entidades de `data-model.md`. |
| `src/barbersync/schemas/` | Contratos de `api.md`. |
| `src/barbersync/routers/` | Endpoints HTTP. |
| `src/barbersync/repositories/` | Consultas y escrituras sin commits propios. |
| `src/barbersync/services/booking_service.py` | Creación y cancelación de citas. |
| `src/barbersync/services/availability.py` | Cálculo de intervalos disponibles. |
| `tests/` | Pruebas de servicio, API, persistencia y concurrencia acordadas con QA. |

## 4. Prevención de reservas superpuestas

Se usan intervalos semiabiertos `[inicio, fin)`: una cita de 10:00 a 10:30 permite otra que comience a las 10:30. Hay conflicto cuando coinciden el barbero y el estado `confirmed`, y se cumple:

```text
existente.start_time < nuevo.end_time
AND existente.end_time > nuevo.start_time
```

### Operación de creación propuesta

1. Validar la estructura de entrada y normalizar fecha y teléfono.
2. Abrir una unidad de trabajo dedicada a escritura. Ejecutar `BEGIN IMMEDIATE` antes de leer datos que determinen la reserva.
3. En esa misma conexión, comprobar barbero, servicio, duración, horario, fecha futura y solapamientos. Calcular `end_time` en el servidor.
4. Buscar el cliente por teléfono normalizado; crearlo solo si no existe.
5. Insertar la cita y confirmar con un único commit. Cualquier fallo revierte también la creación del cliente.
6. Responder 201 únicamente después del commit.

La comprobación de disponibilidad y la inserción deben permanecer en una sola transacción. Consultar primero y abrir la transacción después dejaría una carrera entre solicitudes.

SQLite admite una sola transacción de escritura a la vez. `BEGIN IMMEDIATE` toma ese turno antes de consultar; se propone una espera de bloqueo de 5 segundos. Si la conexión sigue ocupada al vencer la espera, responder 503 con `Retry-After: 1`, sin afirmar que el horario está reservado. Un conflicto de citas comprobado responde 409.

SQLAlchemy deberá configurar el comienzo explícito de estas transacciones sin anidar `BEGIN` dentro de una transacción ya abierta por el driver o por una consulta previa. No se propone `isolation_level="IMMEDIATE"` como opción genérica de SQLAlchemy. La integración concreta se verificará durante la implementación.

El índice parcial de `data-model.md` impide inicios idénticos para un mismo barbero confirmado. **No impide por sí solo solapamientos con inicios diferentes**. La garantía depende del protocolo transaccional en todos los caminos de escritura de la aplicación. No se permitirán escrituras directas que lo omitan.

Cancelar una cita usará también una transacción de escritura. Una futura operación de reprogramación o bloqueo deberá aplicar la misma disciplina.

## 5. Calendario, fechas y disponibilidad

- Entradas HTTP: ISO 8601 con desplazamiento explícito, por ejemplo `2026-11-20T10:00:00-05:00`. Se rechazan horas sin zona.
- Comparaciones y persistencia: UTC normalizado. Respuestas de citas: horario de Panamá con `-05:00`.
- `date` representa un día de Panamá. Su filtro se traduce a un intervalo UTC `[medianoche local, medianoche local siguiente)`.
- Se generan comienzos cada 5 minutos desde la apertura; la cita completa debe terminar a más tardar a las 18:00. Segundos y microsegundos del inicio deben ser cero.
- Domingo no ofrece horarios. Para disponibilidad, una fecha pasada devuelve 422; el día actual excluye comienzos menores o iguales al reloj actual.
- Disponibilidad filtra citas confirmadas y considera la duración solicitada. Consultarla no retiene el horario: crear una cita vuelve a comprobarlo dentro de la transacción.
- En la base inicial no hay almuerzos, permisos ni bloqueos extraordinarios implementados.

## 6. Verificación prevista con QA

Las siguientes son pruebas propuestas, todavía no ejecutadas contra BarberSync:

- Rechazo de duplicados exactos y de solapamientos parciales con inicios diferentes.
- Aceptación de citas adyacentes y de citas simultáneas para barberos distintos.
- Cancelación que libera el horario sin eliminar el historial.
- Rechazo de barbero inactivo, fechas pasadas, horas sin zona y citas que terminan después del cierre.
- Dos solicitudes concurrentes para intervalos superpuestos: en condiciones normales, una crea y otra recibe 409; debe quedar una sola cita confirmada. El agotamiento del tiempo de espera se prueba por separado como 503.

Para concurrencia se usará un archivo SQLite temporal y conexiones independientes. Una base `:memory:` compartida con `StaticPool` puede servir para pruebas seriales, pero no demuestra aislamiento entre dos conexiones. Las fixtures deben activar claves foráneas y reproducir la configuración transaccional de la aplicación. El reloj debe controlarse o las fechas deben generarse para el futuro.

## 7. Ampliación conocida y cambio posterior

El borrador original ya anticipaba `blocked_slots` y el almuerzo; por tanto, ese ejemplo es conocido por el equipo. Se deja fuera del contrato base para implementar primero una versión verificable.

Cuando llegue un cambio real, registrar la solicitud en un Issue, conservar el commit y las pruebas de la base, actualizar especificaciones, código y pruebas en otra rama y revisar mediante PR. Si se utiliza el almuerzo como ejercicio, identificarlo como cambio simulado previamente conocido; validar con la guía si eso satisface la actividad.

## 8. Fuentes técnicas consultadas

- [SQLite: transacciones](https://www.sqlite.org/lang_transaction.html).
- [SQLAlchemy: SQLite, transacciones y conexiones](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html).
- [SQLite: claves foráneas](https://www.sqlite.org/foreignkeys.html).

Estas fuentes respaldan mecanismos técnicos; no acreditan requisitos de la asignatura ni aprobación del equipo.
