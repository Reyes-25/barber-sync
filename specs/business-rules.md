# Reglas de Negocio (Business Rules)

1. **Regla de Oro (No Doble Reserva):** Un barbero no puede tener dos citas en el mismo bloque de tiempo. Si un horario está ocupado, el sistema debe rechazar la nueva reserva inmediatamente.
2. **Horarios de Atención:** El sistema solo permite reservas de Lunes a Sábado, en horarios de 9:00 AM a 7:00 PM.
3. **Reservas Pasadas:** No se permite agendar citas en fechas u horas anteriores al momento actual.
4. **Límite de Reservas:** Un cliente (identificado por su número de teléfono) no puede tener más de una reserva activa en el mismo día.