# Estrategia de Testing — BarberSync

Responsable: **Hector Ortega (QA / DevOps Lead)** — Ciclo 1.

## Niveles de prueba

1. **Unitarios**: funciones puras de `services.py` (normalización de teléfono, conversión de zonas horarias).
2. **Integración**: endpoints REST con `TestClient` de FastAPI y base SQLite de prueba independiente.
3. **Reglas críticas**: disponibilidad, solapamiento, citas adyacentes, cancelación lógica.
4. **Aceptación**: recorridos de cliente y barbero en las vistas HTML.

## Herramientas
- `pytest`: runner de tests.
- `pytest-cov`: cobertura con umbral mínimo del 80 %.
- `httpx` + `TestClient`: clientes síncronos para FastAPI.
- `ruff`: lint y formato.
- GitHub Actions: CI/CD.

## Entorno de prueba
- Base de datos SQLite separada (`test_barbersync.db`) creada por fixture.
- `DATABASE_URL` apunta a la base de prueba antes de importar la aplicación.
- Cada test recibe una base limpia gracias a `scope=function` y `drop_all`/`create_all`.

## Cómo ejecutar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Resultados registrados
- **Fecha:** 17 de noviembre de 2026.
- **Commit:** (ver rama `feature/full-implementation`).
- **Tests:** 21 passed.
- **Cobertura:** 84 %.
- **Lint:** `ruff check src tests` sin errores.

## CI/CD
- GitHub Actions ejecuta lint + tests en cada push/PR a `main`.

## Nota sobre concurrencia
La propuesta de `BEGIN IMMEDIATE` de la arquitectura se simplificó: SQLite serializa las escrituras de forma nativa y, para la demo académica, la validación de solapamiento dentro de una transacción normal es suficiente. Si el equipo decide reforzar la concurrencia, se retomará el protocolo transaccional explícito.
