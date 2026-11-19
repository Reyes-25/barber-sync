# BarberSync 💈

## Descripción
**BarberSync** es un sistema de reservas en línea diseñado para barberías que buscan eliminar los cruces de horarios y optimizar su agenda. A través de una plataforma intuitiva, los clientes pueden consultar disponibilidad en tiempo real y agendar sus citas de forma autónoma, mientras el barbero administra su tiempo sin intervención manual.

Este proyecto aplica el enfoque de **Desarrollo Orientado por Especificaciones y Resultados (ODD/SDD)** para garantizar una solución centrada en el valor del usuario.

## 👥 Integrantes y Roles (Rotativos)
*   **[Amir Reyes]** — Product / Spec Lead
*   **[Julio Gudiño]** — Architecture / Development Lead
*   **[Hector Ortega]** — QA / DevOps Lead

## 🛠️ Stack Tecnológico
*   Python 3.11+
*   FastAPI + SQLAlchemy 2.0
*   SQLite
*   Jinja2 + HTML/CSS/JavaScript
*   pytest + pytest-cov
*   Docker + Docker Compose
*   GitHub Actions

## 📂 Estructura del Proyecto
*   `specs/`: Especificaciones del proyecto (ODD y SDD).
*   `docs/`: Documentación de uso de IA, decisiones y testing.
*   `src/barbersync/`: Código fuente de la aplicación.
*   `tests/`: Pruebas automatizadas.
*   `.github/workflows/`: CI/CD.

## 🚀 Estado del Proyecto
*   [x] Fase 0: Setup inicial y estructura.
*   [x] Fase 1: ODD (Definición de Problema y Outcome).
*   [x] Fase 2: SDD (Especificaciones y Criterios de Aceptación).
*   [x] Fase 3: Desarrollo e Implementación.
*   [x] Fase 4: Pruebas y Despliegue.

## ⚡ Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn barbersync.main:app --app-dir src --reload
```

La aplicación estará disponible en `http://localhost:8000`.

## 🧪 Tests
```bash
pytest
```

Resultados actuales: 21 tests passed, cobertura ≥ 80 %.

## 🐳 Docker
```bash
docker-compose up --build
```

## 📋 Documentación de API
Con la app en ejecución visita `http://localhost:8000/docs`.
