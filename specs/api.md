# API: BarberSync

> Responsable: Julio Gudiño — Architecture / Development Lead.
> Estado: contrato propuesto para Fase 2; todavía no implementado ni aprobado.
> Revisión: 17 de noviembre de 2026. Los ejemplos son ilustrativos, no resultados de pruebas.

## 1. Convenciones

- JSON; prefijo `/api/v1`; documentación prevista en `/docs`.
- Aplican los supuestos pendientes A01–A06 de [architecture.md](architecture.md).
- IDs enteros positivos. Campos obligatorios ausentes, formatos incorrectos o campos de entrada no admitidos: 422.
- Fechas de cita ISO 8601 con desplazamiento explícito. Ejemplo: `2026-11-20T10:00:00-05:00`. Se acepta otro desplazamiento explícito y se convierte al mismo instante; no se aceptan fechas sin zona. Las respuestas se expresan en `America/Panama`.
- `date` significa un día local de Panamá con formato `YYYY-MM-DD`.
- `price` es una cadena decimal con dos posiciones, calculada desde centavos enteros.
- El prototipo local no incluye autenticación. Las operaciones de consulta y cancelación necesitan controles antes de un uso público con datos reales.

### Respuestas de error

| HTTP | Significado |
|---|---|
| 404 | Un recurso referenciado con ID válido no existe. |
| 409 | Reserva superpuesta o cita ya cancelada. |
| 422 | Entrada inválida o regla de horario/estado del barbero incumplida. |
| 503 | La base permanece ocupada al agotar la espera; no equivale a horario reservado. |

Los errores de negocio usan un mensaje:

```json
{ "detail": "El horario ya está reservado para este barbero." }
```

La validación automática de FastAPI puede usar una **lista** en `detail`. Se conserva ese formato en vez de prometer que siempre será una cadena. Ejemplo simplificado:

```json
{
  "detail": [
    { "type": "missing", "loc": ["body", "service_id"], "msg": "Field required" }
  ]
}
```

La lista puede contener información adicional propia de la versión fijada de FastAPI/Pydantic. El 503 llevará `Retry-After: 1`; tras rollback el cliente puede reintentar, y la reserva volverá a validarse.

## 2. Catálogo de barberos

`GET /api/v1/barbers`

Devuelve únicamente barberos activos, ordenados por `id`. Sin resultados: `[]`.

Respuesta 200:

```json
[
  { "id": 1, "name": "Carlos", "active": true }
]
```

## 3. Catálogo de servicios

`GET /api/v1/services`

Lista ordenada por `id`. Respuesta 200:

```json
[
  { "id": 1, "name": "Corte", "duration_minutes": 30, "price": "8.00" }
]
```

## 4. Disponibilidad de un barbero

`GET /api/v1/barbers/{barber_id}/availability?date=2026-11-20&service_id=1`

Ambos parámetros de consulta son obligatorios. Se generan comienzos cada 5 minutos, se calcula el fin según el servicio y se excluyen intervalos que intersecten citas confirmadas. Se aplica la jornada completa de 09:00 a 19:00, de lunes a sábado, como supuesto por validar.

Respuesta 200, ejemplo de forma:

```json
{
  "barber_id": 1,
  "service_id": 1,
  "date": "2026-11-20",
  "timezone": "America/Panama",
  "slots": ["09:00", "09:05", "09:10"]
}
```

La lista real contiene todos los comienzos disponibles en orden. Los elementos son alternativas: reservar uno puede invalidar otros próximos. Sin disponibilidad o en domingo: `slots: []`.

Errores: 404 si no existe el barbero o el servicio; 422 si el barbero está inactivo, la fecha es pasada o hay datos mal formados. Para hoy, se excluyen comienzos menores o iguales al momento actual. Este endpoint no bloquea ni garantiza el horario consultado.

## 5. Crear una cita

`POST /api/v1/appointments`

Solicitud:

```json
{
  "barber_id": 1,
  "service_id": 1,
  "start_time": "2026-11-20T10:00:00-05:00",
  "customer": { "name": "Ana Pérez", "phone": "6000-0000" }
}
```

`customer.name` se recorta y debe tener entre 1 y 100 caracteres. El teléfono se normaliza según [data-model.md](data-model.md). Si ya existe, se reutiliza el cliente y se conserva su nombre registrado. Si no existe, se crea junto con la cita dentro de la misma transacción.

No se aceptan `id`, `customer_id`, `end_time`, `status` ni `created_at` como campos de entrada. La aplicación los determina. El inicio debe tener segundos y microsegundos en cero y coincidir con la cuadrícula de 5 minutos. Debe ser futuro y la cita completa debe caber en el horario.

Respuesta 201, objeto `Appointment`:

```json
{
  "id": 15,
  "barber_id": 1,
  "service_id": 1,
  "customer_id": 7,
  "start_time": "2026-11-20T10:00:00-05:00",
  "end_time": "2026-11-20T10:30:00-05:00",
  "status": "confirmed",
  "created_at": "2026-11-19T14:00:00-05:00"
}
```

| Condición | HTTP |
|---|---|
| Cita confirmada del mismo barbero que se solapa, incluido un inicio diferente. | 409 |
| Barbero o servicio inexistente. | 404 |
| Barbero inactivo, horario inválido, inicio pasado o entrada inválida. | 422 |
| Tiempo de espera de escritura agotado antes de completar la operación. | 503 |

La respuesta 201 se envía después del commit. No se realiza un commit separado para el cliente. El conflicto revierte la operación completa. No se incluyen bloqueos extraordinarios en este contrato base.

## 6. Consultar una cita

`GET /api/v1/appointments/{appointment_id}`

Respuesta 200: objeto `Appointment`, con la misma estructura que en la creación y el estado actual. Se pueden consultar citas pasadas y canceladas. ID inexistente: 404; ID mal formado: 422.

## 7. Listar citas

`GET /api/v1/appointments?date=2026-11-20&barber_id=1&status=confirmed&limit=50&offset=0`

| Parámetro | Regla |
|---|---|
| `date` | Opcional; filtra por el inicio de la cita en ese día de Panamá. Admite fechas pasadas para consultar historial. |
| `barber_id` | Opcional; entero positivo; 404 si no existe. Se admite un barbero inactivo para consultar su historial. |
| `status` | Opcional; `confirmed` o `cancelled`; omitido incluye ambos estados. |
| `limit` | Opcional; 50 por defecto; entre 1 y 100. |
| `offset` | Opcional; 0 por defecto; entero mayor o igual a cero. |

Respuesta 200: lista de objetos `Appointment`, ordenados por `start_time` y después `id`, aplicando filtros antes de paginar. Sin coincidencias: `[]`. Parámetros inválidos: 422.

## 8. Cancelar una cita

`PATCH /api/v1/appointments/{appointment_id}/cancel`

Sin cuerpo. Cambia `confirmed` a `cancelled`, conserva el historial y libera el intervalo. En esta propuesta se permite cancelar cualquier cita confirmada; Product debe validar si requiere un límite temporal.

Respuesta 200:

```json
{ "id": 15, "status": "cancelled" }
```

Errores: 404 si no existe; 409 si ya está cancelada; 422 para un ID inválido; 503 si se agota la espera de escritura. La cancelación también usa una transacción.

## 9. Casos propuestos para QA

Estos nombres son sugeridos; no se afirma que existan archivos de prueba ni resultados PASS.

| Caso | Resultado previsto |
|---|---|
| `test_rejects_double_booking` | Segunda cita del mismo barbero e inicio: 409. |
| `test_rejects_partial_overlap` | Intervalos 10:00–10:30 y 10:15–10:45: 409 para el segundo. |
| `test_allows_adjacent_appointments` | 10:00–10:30 y 10:30–11:00: ambas 201. |
| `test_allows_different_barbers` | Mismo intervalo para dos barberos: ambas 201. |
| `test_cancel_frees_slot` | Cancelar y reservar ese intervalo nuevamente: 200 y 201. |
| `test_availability_excludes_booked_slots` | No ofrecer ningún comienzo cuya duración solape una cita confirmada. |
| `test_concurrent_overlap_creates_one` | Dos conexiones, un archivo SQLite temporal y transacciones breves: 201 y 409; una fila confirmada. |
| `test_write_timeout_returns_503` | Bloqueo sostenido hasta agotar espera: 503, sin inserción parcial. |
| `test_reuses_normalized_phone` | Dos formatos del mismo teléfono reutilizan `customer_id`. |
| `test_rejects_naive_datetime` | Fecha sin desplazamiento: 422. |
| `test_missing_service_returns_404` | Servicio inexistente: 404 tanto en disponibilidad como en reserva. |
| `test_cancel_already_cancelled` | Segunda cancelación: 409. |

Las pruebas usarán reloj controlado o fechas futuras; copiar literalmente una fecha de ejemplo no debe volverlas dependientes del día de ejecución. QA debe convertir la propuesta en criterios de aceptación y añadir bordes de horario, validación e integridad.

## 10. Cambio posterior y fuente técnica

El endpoint `POST /barbers/{barber_id}/blocked-slots` era una idea anticipada del borrador original y queda fuera de la API base. Su contrato se definirá en el Issue del cambio si el equipo adopta ese requisito; no se presenta como endpoint implementado.

[FastAPI: manejo de errores y validación](https://fastapi.tiangolo.com/tutorial/handling-errors/) respalda la distinción entre mensajes de negocio y listas de errores de validación. Las decisiones del dominio siguen pendientes de revisión del equipo.
