# AI Development Log

| Fecha | Actividad | IA Utilizada | Solicitud (Prompt) | Resultado | Decisión del Equipo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 13/11/2026 | Setup inicial y Git | DeepSeek (Web) | "Necesito ayuda con los comandos de PowerShell para crear la estructura de carpetas de un proyecto en Windows" | Comandos `New-Item` y resolución de errores de ruta en Git. | Aceptado. Funcionó para inicializar el repo. |
| 13/11/2026 | Definir ODD | DeepSeek (Web) | "Ayúdame a redactar el problema y el outcome para un sistema de reservas de barbería que busca eliminar la doble reserva" | Redacción del contexto, problema, outcome y valor entregado. | Aceptado. Ajustamos las palabras para que coincidan con nuestro proyecto en clase. |
| 13/11/2026 | Redacción de Reglas de Negocio | DeepSeek (Web) | "Dame ejemplos de reglas de negocio para un sistema de reservas, incluyendo la regla de no doble reserva" | Redacción del archivo `business-rules.md`. | Aceptado. Lo usaremos como base para la lógica en código. |
| 13/11/2026 | Soporte en VS Code | GitHub Copilot | Autocompletado de código y tablas Markdown en VS Code. | Sugerencias de formato y sintaxis para los archivos Markdown. | Aceptado. Agilizó la escritura del código y la documentación. |

---

# Registro de uso de IA

<!-- barbersync-julio-sdd-review-20261117 -->
## 17 de noviembre de 2026 — Revisión de la propuesta de arquitectura

- **Responsable del aporte:** Julio Gudiño, Architecture / Development Lead.
- **Herramienta:** ChatGPT, con consulta del repositorio y documentación técnica oficial.
- **Solicitud del usuario:** ayudar a adelantar su parte conforme a la hoja de ruta del equipo, revisar los tres documentos preparados y orientar el trabajo en una rama propia.
- **Material revisado:** borradores aportados de `architecture.md`, `data-model.md` y `api.md`; README, árbol del repositorio, ramas e Issue #1.
- **Estado observado:** `outcomes.md` y las restantes especificaciones de Product/QA estaban vacíos. El README asigna Product a Amir Reyes, Arquitectura/Desarrollo a Julio Gudiño y QA/DevOps a Hector Ortega. La salida de PowerShell compartida por Julio confirmó la creación y publicación de `docs/arquitectura-julio`; la consulta remota también mostró esa rama.
- **Aportes de IA incorporados al borrador:** explicitar supuestos pendientes; precisar la exclusión de solapamientos y el manejo transaccional; diferenciar conflicto 409 de espera agotada 503; normalizar zona horaria y teléfono; completar comportamiento de cliente existente, precio y errores HTTP; proponer pruebas con conexiones independientes.
- **Corrección al borrador inicial:** se retiraron `blocked_slots` y su endpoint de la base. El almuerzo ya había sido anticipado en los archivos recibidos, por lo que se registra como ampliación conocida, no como sorpresa ocurrida después. Se conserva esta explicación para mantener trazabilidad.
- **Estado de las recomendaciones:** incorporadas por el asistente a una propuesta para revisión. No se registra aprobación humana, de Product o de QA que todavía no haya ocurrido.
- **Verificación realizada en esta revisión:** lectura cruzada de los tres documentos y comprobación de los ejemplos JSON y referencias internas del paquete. No se implementó el backend ni se ejecutó la futura suite de BarberSync. Los nombres de pruebas son propuestas.
- **Trabajo pendiente:** validar la guía del profesor, completar ODD y requisitos, revisar supuestos con el equipo, asociar este aporte con su Issue y PR y, posteriormente, implementar y comprobar los contratos acordados.
- **Evidencia posterior:** el commit y el push se harán desde el Git local del estudiante. El script de preparación generará un registro de esa ejecución; no se da por realizada antes de ejecutarlo.

<!-- barbersync-julio-guide-review-20261117 -->
## 17 de noviembre de 2026 — Contraste con la guía del Proyecto #2

- **Responsable del aporte:** Julio Gudiño, Arquitectura/Desarrollo en el ciclo inicial.
- **Actividad:** revisar la guía del profesor y ajustar la propuesta técnica y la planificación.
- **IA utilizada:** ChatGPT; lectura de las tres páginas del PDF, revisión visual y consulta del estado del repositorio/PR.
- **Solicitud:** continuar el avance de BarberSync conforme a la hoja de ruta; se adjuntó `DSaIA-Proyecto2.pdf` para confirmar condiciones antes de programar.
- **Resultado:** libertad tecnológica confirmada; la guía no prescribe una interfaz web concreta. Se prepararon plan, rotación propuesta, cinco categorías de pruebas y ciclo del cambio a mitad del desarrollo. Al retomar, se leyó el nuevo ODD de Amir y se propuso una interfaz simple para demostrar la reserva autónoma, diferenciando acceso 24/7 de horario de atención y de disponibilidad real del servidor.
- **Decisión propuesta:** conservar Python/FastAPI/SQLAlchemy/SQLite como tecnología permitida pendiente de acuerdo del equipo; completar ODD y validar SDD antes de implementar; introducir el cambio después de una base funcional parcial y antes de finalizar el alcance. La rotación propuesta requiere acuerdo de los tres integrantes.
- **Verificación realizada:** lectura de las páginas 1–3 y comprobación documental. En la primera consulta ODD estaba vacío; al retomar, `main` estaba en `6316a22` con `outcomes.md` y el registro de IA de Amir. El PR #3 seguía en borrador en `6401681`. El Issue #1 no tenía comentarios de revisión. Se preparó la integración de ambos registros de IA sin atribuir una aprobación humana ni resultados del backend.
- **Observación para coordinar:** el registro de Amir menciona un borrador de reglas de negocio, pero `specs/business-rules.md` continúa vacío en el repositorio observado; queda pendiente publicarlo. Las entradas anteriores se conservan como historial.
- **Pendientes:** Product y QA deben completar sus especificaciones; consultar Laboratorio 13 y material complementario citado por la guía; ejecutar y registrar la implementación y las pruebas en los ciclos correspondientes.
