# Decisiones Técnicas — BarberSync

## Stack
- **Python 3.11+**, **FastAPI**, **SQLAlchemy 2.0**, **SQLite**.
- **Jinja2 + HTML/CSS/JS vanilla** para el frontend mínimo.
- **pytest + pytest-cov** para tests.
- **ruff** para lint/formato.
- **Docker + Docker Compose** para despliegue reproducible.
- **GitHub Actions** para CI/CD.

## Decisiones de dominio
- Se adoptó la propuesta de Julio: entidades `Barber`, `Customer`, `Service` y `Appointment`.
- Precio almacenado en centavos y expuesto como cadena decimal con dos posiciones.
- Teléfono normalizado a formato `+507XXXXXXXX`.
- Fechas de cita en UTC canónico en base de datos; respuestas en `America/Panama`.
- Horario de atención lunes-sábado 09:00-18:00, definido en configuración.
- Slots de disponibilidad cada 5 minutos.
- Estado inicial de cita: `confirmed`; cancelación lógica a `cancelled`.

## Simplificaciones respecto a la propuesta original
- El protocolo `BEGIN IMMEDIATE` se omitió porque SQLite serializa escrituras nativamente; se mantiene la validación de solapamiento dentro de la transacción.
- No se implementó paginación compleja ni autenticación, acorde al alcance de demo local.
- El manejo del 503 por timeout de escritura queda documentado como mejora futura.

## Referencias
- Especificaciones en `specs/`.
- Guía académica `DSaIA-Proyecto2.pdf` (profesor Regis Rivera).
