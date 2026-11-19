# Criterios de Aceptación — BarberSync

> Responsable del aporte: QA / DevOps Lead (Hector Ortega) con revisión de Product.
> Estado: versión inicial que traza requisitos, reglas y casos de prueba.

## CA-01 Consultar disponibilidad
**Dado** que existe un barbero activo con horario configurado,
**cuando** un cliente consulta disponibilidad para una fecha futura y un servicio,
**entonces** el sistema devuelve los comienzos disponibles ordenados, excluyendo citas confirmadas.

## CA-02 Reservar cita exitosa
**Dado** un horario disponible para un barbero activo,
**cuando** el cliente envía nombre, teléfono, barbero, servicio e inicio válidos,
**entonces** la cita queda en estado `confirmed`, el sistema responde 201 con los detalles y el horario ya no aparece disponible.

## CA-03 Evitar doble reserva
**Dado** que un horario ya está reservado para un barbero,
**cuando** otro cliente intenta reservar el mismo o un intervalo solapado,
**entonces** el sistema responde 409 y no crea la segunda cita.

## CA-04 Permitir citas adyacentes
**Dado** una cita confirmada de 10:00 a 10:30,
**cuando** un cliente reserva de 10:30 a 11:00 para el mismo barbero,
**entonces** el sistema acepta la segunda reserva.

## CA-05 Cancelar cita
**Dado** una cita confirmada futura,
**cuando** se solicita su cancelación,
**entonces** el estado cambia a `cancelled` y el horario vuelve a estar disponible.

## CA-06 Rechazar datos inválidos
**Dado** una solicitud de reserva con fecha pasada, teléfono inválido o sin zona horaria,
**cuando** el cliente la envía,
**entonces** el sistema responde 422 sin crear la cita.

## CA-07 Reutilizar cliente por teléfono
**Dado** un cliente previamente registrado,
**cuando** se reserva con el mismo teléfono en otro formato,
**entonces** el sistema reutiliza el cliente existente y no crea un duplicado.

## CA-08 Panel de citas
**Dado** que el barbero accede al panel administrativo,
**cuando** existen citas,
**entonces** puede ver el listado completo con estado y detalles.

## CA-09 Límite de reservas activas
**Dado** un cliente que ya alcanzó el límite de reservas activas configurado,
**cuando** intenta reservar una cita adicional,
**entonces** el sistema responde 422 y no crea la nueva cita.

## CA-10 Tests automatizados
**Dado** el pipeline de CI/CD,
**cuando** se ejecuta `pytest`,
**entonces** todos los tests pasan, incluyendo las pruebas automatizadas de rechazo de doble reserva y concurrencia, y la cobertura es ≥ 80 %.
