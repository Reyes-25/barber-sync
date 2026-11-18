# Reglas de Negocio — BarberSync

> Responsable del aporte: Product / Spec Lead (Amir Reyes) y QA / DevOps Lead (Hector Ortega).
> Estado: versión inicial derivada del ODD y la propuesta técnica.

1. **RN-01 Jornada de atención**: la barbería atiende de lunes a sábado, de 09:00 a 18:00 (hora de Panamá). El domingo no tiene horarios disponibles.
2. **RN-02 Duración de servicio**: cada servicio tiene una duración fija en minutos; el fin de la cita se calcula en el servidor.
3. **RN-03 Intervalos de 5 minutos**: los horarios de inicio ofrecidos se generan cada 5 minutos y deben tener segundos/microsegundos en cero.
4. **RN-04 Reserva futura**: solo se permite reservar citas con inicio en el futuro respecto al momento actual en `America/Panama`.
5. **RN-05 Sin solapamiento**: dos citas confirmadas del mismo barbero no pueden tener intervalos que se intersecten. Las citas adyacentes sí están permitidas.
6. **RN-06 Cancelación lógica**: cancelar una cita cambia su estado a `cancelled` y libera el horario; no se elimina el registro histórico.
7. **RN-07 Cliente único por teléfono**: el teléfono se normaliza a formato `+507XXXXXXXX`; si ya existe un cliente con ese teléfono, se reutiliza.
8. **RN-08 Barbero activo**: solo los barberos marcados como activos pueden recibir nuevas reservas.
9. **RN-09 Confirmación inmediata**: una reserva exitosa queda en estado `confirmed` y el sistema responde después de persistir el registro.
10. **RN-10 Cita completa dentro de la jornada**: el inicio más la duración del servicio debe caber dentro del horario de atención del día seleccionado.
