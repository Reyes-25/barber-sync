# Plan de implementación: BarberSync

> Responsable del aporte: Julio Gudiño — Architecture / Development Lead.
> Estado: propuesta de planificación, pendiente de validación del equipo y de ODD.
> Referencia: `DSaIA-Proyecto2.pdf`, profesor Regis Rivera, pp. 1–3.
> Trazabilidad inicial: Issue #2 y PR #3 (`docs/arquitectura-julio` → `main`).

## 1. Punto de partida y alcance

El commit `6401681` de Julio contiene tres especificaciones propuestas y entradas de IA/decisiones; el PR #3 está en borrador. Al retomar la revisión, `main` avanzó a `6316a22`: Amir publicó problema, outcome y preguntas de exploración para Tavo BarberShop, además de su registro de IA. El Issue #1 sigue abierto y no mostraba comentarios de revisión. Requisitos, reglas de negocio y criterios de aceptación siguen sin contenido publicado. No hay implementación funcional ni pruebas automatizadas de BarberSync acreditadas todavía.

Este plan se prepara como borrador para facilitar el trabajo del equipo. Antes de implementar, el equipo debe revisar el ODD publicado y completar/validar las especificaciones. El adelanto inicial de documentos no sustituye esa secuencia. La actualización de la rama de Julio debe integrar `main` y preservar las entradas de IA de ambos aportes.

La tecnología propuesta es Python/FastAPI/SQLAlchemy/SQLite, permitida por la libertad tecnológica de la guía, p. 3, punto 10. La elección concreta se acuerda en el equipo. Aunque la guía no prescribe una interfaz web, se propone HTML/CSS/JavaScript para demostrar la reserva autónoma del cliente que describe ODD. `/docs` facilita la revisión técnica, pero el recorrido del cliente se verificará en la interfaz acordada.

## 2. Rotación propuesta por ciclos

La guía exige rotar roles según los ciclos (p. 1). La tabla es una propuesta de reparto; no acredita que la rotación haya ocurrido ni compromete a otros integrantes sin acuerdo.

| Ciclo | Product / Spec Lead | Architecture / Development Lead | QA / DevOps Lead | Evidencia prevista |
|---|---|---|---|---|
| C1: ODD, SDD y base funcional parcial | Amir Reyes | Julio Gudiño | Hector Ortega | Issues, documentos, commits, PR, revisión y primeras pruebas. |
| C2: cambio a mitad del desarrollo | Julio Gudiño | Hector Ortega | Amir Reyes | Issue del cambio, especificaciones actualizadas, implementación y pruebas antes/después. |
| C3: completar alcance, integrar y preparar defensa | Hector Ortega | Amir Reyes | Julio Gudiño | Ajustes finales, pruebas de aceptación, README y demo reproducible. |

Liderar no significa trabajar solo. El equipo debe compartir explicaciones y revisar los cambios de otro integrante. Antes de cada ciclo se registrarán los responsables reales en el Issue correspondiente. Si se acuerda otra rotación, actualizar la tabla antes de ejecutar ese ciclo.

## 3. Trabajo y dependencias

Los identificadores P01–P12 son elementos de este plan, no números de Issues existentes. Solo #1, #2 y #3 se refieren a elementos ya observados en GitHub.

| ID | Trabajo | Responsable principal propuesto | Depende de | Evidencia de terminación |
|---|---|---|---|---|
| P01 | Revisar el `outcomes.md` ya publicado y acordar cómo se medirán cero conflictos, autonomía, confirmación y acceso 24/7. | Product C1 con el equipo | Inicio | Issue #1 con revisión real; aclarar si el contexto proviene de entrevista o de un escenario académico. |
| P02 | Escribir alcance, requisitos y reglas: jornada, servicios, cancelación, usuarios y no doble reserva. | Product C1 | P01 | `requirements.md` y `business-rules.md` con identificadores trazables. |
| P03 | Revisar arquitectura, datos, API y este plan contra P01/P02; resolver supuestos A01–A06. | Arquitectura C1 | P02 | PR #3 ajustado y revisado; decisiones ratificadas o corregidas. |
| P04 | Definir criterios de aceptación observables y su matriz de pruebas. | QA C1, con Product | P02/P03 | `acceptance-criteria.md` y catálogo inicial en `docs/testing.md`. |
| P05 | Preparar entorno reproducible, dependencias, estructura de aplicación, configuración y persistencia. | Arquitectura C1 | P03/P04 | Rama de implementación, arranque documentado y seed idempotente. |
| P06 | Implementar catálogos, disponibilidad y creación de citas con validación/transacción, más el recorrido mínimo de cliente; mantener alcance restante pendiente. | Arquitectura C1 | P05 | Base funcional parcial: consulta, reserva y confirmación; rechazo de solapamientos. |
| P07 | Automatizar pruebas iniciales: unidades, reglas críticas, conflictos y validación de usuario. | QA C1 | P06 | Ejecución real registrada, commit base y resultados reproducibles. |
| P08 | Introducir y registrar un requisito adicional a mitad del desarrollo; evaluar impacto antes de cambiar código. | Product C2 | P06/P07 | Issue nuevo del cambio, alcance y responsables del ciclo. |
| P09 | Actualizar especificaciones, criterios de aceptación y tareas; implementar y probar el cambio. | Los tres roles C2 | P08 | PR del cambio con trazabilidad completa y evidencia antes/después. |
| P10 | Completar el alcance pendiente: cancelación, filtros, interacción de usuario acordada y manejo de errores. | Arquitectura C3 | P09 | Funcionalidad restante y pruebas correspondientes. |
| P11 | Integrar, ejecutar regresión y criterios de aceptación; preparar ejecución o despliegue de la demo. | QA C3 | P10 | `docs/testing.md`, resultados reales y README reproducible. |
| P12 | Relacionar resultados con el outcome, ensayar defensa y verificar entrega. | Product C3 y todo el equipo | P11 | Demostración, evidencias y material de presentación utilizado. |

El hito de cambio está **entre la base parcial y la terminación del alcance**, no antes de escribir código ni después de finalizar todo el proyecto. Si el alcance validado cambia, ajustar las tareas para mantener ese punto intermedio real.

## 4. Base técnica a implementar después de validar SDD

1. Crear entorno Python y fijar dependencias compatibles. Los archivos de dependencia y comandos exactos se incorporarán al README cuando se comprueben.
2. Configurar una aplicación local, un archivo SQLite de desarrollo y bases temporales de prueba independientes. Excluir entornos, bases de desarrollo y secretos del repositorio.
3. Implementar modelos, constraints, índices, activación de claves foráneas y la unidad de trabajo definidos en las especificaciones.
4. Implementar primero reglas de dominio y persistencia; conectar después routers y schemas.
5. Mantener la comprobación de solapamientos y la inserción en la misma transacción. Verificar la implementación concreta de `BEGIN IMMEDIATE` con SQLAlchemy.
6. Acordar e implementar una interfaz sencilla para consultar disponibilidad, reservar y ver confirmación; definir con Product el alcance de gestión del barbero. El acceso al sistema a cualquier hora no equivale a atender citas fuera de la jornada ni acredita todavía disponibilidad de un servidor 24/7.

Esta lista es planificación. No implica que dependencias, endpoints, transacciones o interfaz ya estén implementados.

## 5. Pruebas mínimas y propuesta de cobertura

La guía, p. 3, punto 12, exige las cinco categorías siguientes y una prueba automatizada de no doble reserva. Los casos son propuestas para que QA los convierta en pruebas; no son resultados ejecutados.

| Categoría exigida | Casos propuestos | Evidencia esperada |
|---|---|---|
| Unitarias | Duración y fin de cita, normalización de teléfono y conversión de fecha/hora. | Pruebas aisladas con resultados registrados. |
| Reglas críticas | Jornada completa, barbero activo, intervalos adyacentes y cancelación lógica. | Pruebas que enlacen reglas identificadas con resultados. |
| Conflictos de reserva | Duplicado exacto y solapamiento parcial para el mismo barbero; admitir otro barbero. | Prueba automatizada obligatoria que rechace doble reserva. |
| Validaciones de usuario | Nombre vacío, teléfono inválido, datos incompletos, IDs inválidos, fecha pasada y fecha sin zona. | Respuestas y ausencia de cambios parciales comprobadas. |
| Criterios de aceptación | Recorridos del usuario acordados: consultar, reservar, recibir confirmación y cancelar si aplica. | Cada criterio aceptado asociado a una prueba y su resultado. |

Cobertura adicional propuesta por el diseño: dos conexiones concurrentes sobre un archivo SQLite temporal; comprobar que no quedan dos citas confirmadas superpuestas y que una espera agotada se distingue de un conflicto de negocio. No se atribuye a la guía una exigencia literal de este caso adicional.

La ejecución prevista con el stack propuesto será `python -m pytest -q`, una vez existan dependencias y pruebas. Registrar el comando realmente utilizado, fecha, commit, cantidad de pruebas y salida. No inventar resultados PASS. Controlar el reloj o generar fechas futuras para que los ejemplos no caduquen.

## 6. Ciclo obligatorio del cambio

La guía pide, en este orden, evidencia de:

1. **Cambio solicitado:** Issue nuevo con el requisito, motivo, solicitante o escenario y vínculo al commit base.
2. **Especificaciones actualizadas:** outcome/requisitos/reglas y arquitectura/datos/API afectados; explicar impacto y decisiones.
3. **Criterios de aceptación actualizados:** comportamiento esperado del cambio, revisado con QA.
4. **Plan y tareas actualizados:** editar este plan y el backlog, incluyendo responsables de la rotación.
5. **Código modificado:** implementación en una rama del cambio, con commits identificables.
6. **Pruebas modificadas:** casos nuevos y ajustes a los afectados; conservar regresión de reservas.
7. **Resultados comprobados:** ejecutar pruebas y demo; comparar con el resultado esperado; revisar el PR.

El almuerzo ya aparece como ejemplo anticipado en la conversación y en los borradores iniciales. No se declarará una sorpresa real posterior. Se propone recibir el requisito del hito cuando exista la base parcial; si se representa un cambio simulado conocido, documentarlo y confirmar con el profesor que cumple la dinámica esperada.

## 7. Git, revisión y uso de IA

- Mantener cada tarea relacionada con un Issue, una rama y commits identificables.
- El PR #3 seguirá en borrador mientras las especificaciones dependientes estén incompletas. Al resolverlas, actualizar la propuesta y solicitar la revisión del equipo mediante el flujo acordado.
- Para código y cambio, usar ramas separadas y PR o revisión equivalente. La guía admite revisión equivalente; el equipo eligió PR y protección de `main`.
- Documentar por cada uso de IA: **actividad, IA utilizada, solicitud, resultado y decisión**, conforme al punto 11 de la guía. Identificar quién tomó la decisión y qué se verificó realmente.
- Las decisiones propuestas por IA se mantienen como propuestas hasta que un integrante las revise. No atribuir al equipo aprobaciones que no haya dado.
- El texto exacto «Revisado y aprobado» en el Issue #1 es una convención de coordinación del equipo; no aparece como frase obligatoria en el PDF.

## 8. Lista de cierre y defensa

| Elemento | Comprobación al finalizar |
|---|---|
| Resultado al usuario | Mostrar qué problema se resuelve y cómo se comprobó el outcome, con datos reales de la demo o pruebas. |
| Especificaciones | Coherencia entre requisitos, reglas, arquitectura, datos, API, aceptación y plan. La estructura de nombres de la guía es recomendada; se conserva por acuerdo del equipo. |
| Implementación | Código correspondiente a la especificación aceptada y arranque reproducible. |
| Pruebas | Las cinco categorías mínimas, prueba anti doble reserva, resultados y regresión del cambio. |
| Historial | Issues, ramas, commits, PR/revisión y evidencia del cambio completo. |
| Registro de IA | Entradas con los cinco campos requeridos y decisiones honestas. |
| README | Propósito, integrantes y rotaciones reales, stack, instalación, ejecución, pruebas, demo y límites actuales. |
| Defensa | Los tres pueden explicar ODD, SDD, código, pruebas, Git y decisiones; el presentador se elige al azar. Prepararse para una petición de cambio en vivo. |
| Presentación y entrega | Diapositivas opcionales. Entregar también el material efectivamente utilizado. La guía permite que un integrante realice la entrega grupal. |

El rol QA/DevOps incluye integración y despliegue, pero la guía no fija proveedor, URL pública ni plataforma obligatoria. Acordar una demo reproducible y documentar cómo se ejecuta o despliega.

## 9. Material complementario pendiente

La guía remite al Laboratorio 13 y al material compartido para SDD. Deben consultarse antes de dar por cerrado el cumplimiento completo. Este plan se basa en las tres páginas del Proyecto #2, los documentos recibidos y el estado observado del repositorio; no presume instrucciones de materiales todavía no revisados.
