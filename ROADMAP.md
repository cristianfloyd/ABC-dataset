# ABC Dataset - Roadmap del Proyecto

## Objetivo del Proyecto
Crear una plataforma web para buscar y analizar ofertas de Actos Públicos Digitales de la provincia de Buenos Aires, Argentina.

---

## FASE 1: MVP con Streamlit (1-2 días) ✅ EN PROGRESO

### Objetivo
Validar la idea con usuarios reales mediante un dashboard funcional y rápido.

### Tecnologías
- **Backend/Frontend**: Streamlit (Python)
- **Datos**: Pandas + JSON
- **Visualización**: Plotly, Matplotlib
- **Deploy**: Streamlit Cloud (gratuito)

### Features del MVP

#### 1. Página de Búsqueda de Cargos
- [ ] Filtros interactivos:
  - Modalidad (ARTISTICA, SECUNDARIA, etc.)
  - Distrito
  - Cargo/Área de incumbencia
  - Rango de fechas
  - Estado de la oferta
- [ ] Búsqueda por texto libre
- [ ] Tabla con resultados paginados
- [ ] Vista detallada de cada oferta
- [ ] Exportar resultados a CSV/Excel

#### 2. Dashboard de Estadísticas
- [ ] Métricas principales (cards):
  - Total de ofertas
  - Ofertas por modalidad
  - Distritos más activos
  - Cargos más demandados
- [ ] Gráficos interactivos:
  - Distribución por distrito (mapa/barras)
  - Ofertas por modalidad (pie chart)
  - Timeline de ofertas (línea temporal)
  - Top 10 cargos más ofertados
  - Horas/módulos por distrito
- [ ] Filtros globales aplicables a todos los gráficos

#### 3. Página de Cargos Habilitantes/Bonificantes
- [ ] Visualización de cargos del JSON
- [ ] Filtro por modalidad
- [ ] Indicador de habilitante vs bonificante
- [ ] Puntajes asociados

#### 4. Features Adicionales
- [ ] Sidebar con navegación
- [ ] About/Info del proyecto
- [ ] Instrucciones de uso
- [ ] Fecha de última actualización de datos
- [ ] Botón para actualizar datos (ejecutar scraper)

### Archivos a Crear
```
ABC-dataset/
├── app.py                    # ← App principal de Streamlit
├── pages/
│   ├── 1_busqueda.py        # ← Página de búsqueda
│   ├── 2_estadisticas.py    # ← Dashboard de stats
│   └── 3_cargos.py          # ← Info de cargos
├── utils/
│   ├── data_loader.py       # ← Cargar y cachear datos
│   └── visualizations.py    # ← Funciones para gráficos
├── requirements.txt          # ← Dependencias
└── .streamlit/
    └── config.toml           # ← Configuración UI
```

### Deploy
- Subir a GitHub
- Conectar con Streamlit Cloud
- URL pública gratuita

### Tiempo estimado: 1-2 días

---

## FASE 2: Aplicación Web Profesional con FastAPI + React (2-3 semanas)

### Objetivo
Crear una aplicación escalable, profesional y moderna para el portafolio.

### Arquitectura

#### Backend: FastAPI
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión DB (opcional)
│   ├── models/              # Pydantic models
│   │   ├── oferta.py
│   │   └── cargo.py
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── ofertas.py
│   │       │   ├── cargos.py
│   │       │   └── stats.py
│   │       └── router.py
│   ├── services/            # Lógica de negocio
│   │   ├── scraper_service.py
│   │   └── stats_service.py
│   └── utils/
│       └── data_loader.py
├── tests/
├── requirements.txt
└── Dockerfile
```

**API Endpoints:**
```
GET  /api/v1/ofertas              # Listar ofertas con paginación
GET  /api/v1/ofertas/{id}         # Detalle de oferta
GET  /api/v1/ofertas/search       # Búsqueda avanzada
GET  /api/v1/cargos               # Listar cargos
GET  /api/v1/cargos/{codigo}      # Detalle de cargo
GET  /api/v1/stats/general        # Estadísticas generales
GET  /api/v1/stats/por-distrito   # Stats por distrito
GET  /api/v1/stats/por-modalidad  # Stats por modalidad
POST /api/v1/scraper/run          # Ejecutar scraper (admin)
GET  /api/v1/scraper/status       # Estado del scraper
```

#### Frontend: React + TypeScript
```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── common/          # Botones, inputs, cards
│   │   ├── ofertas/         # Componentes de ofertas
│   │   ├── stats/           # Gráficos y dashboards
│   │   └── layout/          # Header, footer, sidebar
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Busqueda.tsx
│   │   ├── Estadisticas.tsx
│   │   ├── Cargos.tsx
│   │   └── OfertaDetalle.tsx
│   ├── services/
│   │   └── api.ts           # Cliente API
│   ├── hooks/               # Custom hooks
│   ├── types/               # TypeScript types
│   ├── utils/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

**Stack Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TanStack Query (data fetching)
- Zustand (state management)
- React Router (routing)
- Recharts / Chart.js (gráficos)
- Tailwind CSS + shadcn/ui (UI)
- Axios (HTTP client)

### Features Fase 2

#### Backend
- [ ] API RESTful completa con FastAPI
- [ ] Validación de datos con Pydantic
- [ ] Paginación, ordenamiento, filtros
- [ ] Cache con Redis (opcional)
- [ ] Rate limiting
- [ ] CORS configurado
- [ ] Logging y monitoreo
- [ ] Tests unitarios (pytest)
- [ ] Documentación automática (Swagger)
- [ ] Integración con base de datos (PostgreSQL opcional)
- [ ] Scraper como tarea asíncrona (Celery + Redis)
- [ ] Autenticación JWT (para admin)

#### Frontend
- [ ] UI moderna y responsive
- [ ] Búsqueda con autocompletado
- [ ] Filtros avanzados con URL params
- [ ] Tabla virtual para miles de registros
- [ ] Gráficos interactivos (zoom, tooltips)
- [ ] Exportación de datos
- [ ] Dark mode
- [ ] Favoritos/guardados (localStorage)
- [ ] Notificaciones
- [ ] PWA (Progressive Web App)
- [ ] Loading states y skeletons
- [ ] Error boundaries
- [ ] Tests (Vitest + Testing Library)

### Mejoras Adicionales
- [ ] Base de datos PostgreSQL
  - Indexación para búsquedas rápidas
  - Histórico de ofertas
  - Usuarios y preferencias
- [ ] Sistema de notificaciones
  - Email cuando aparecen cargos específicos
  - Webhooks
- [ ] Panel de administración
  - Gestión de cargos
  - Programar scraping automático
  - Ver logs y errores
- [ ] Analytics
  - Google Analytics
  - Métricas de uso

### Deploy Fase 2
- **Backend**: Railway / Render / Fly.io
- **Frontend**: Vercel / Netlify
- **Base de datos**: Supabase / Neon / Railway
- **Cache**: Upstash Redis
- **CI/CD**: GitHub Actions

### Portafolio - Qué Destacar
✅ **Backend:**
- FastAPI con arquitectura limpia
- API RESTful con buenas prácticas
- Async/await para performance
- Tests y documentación

✅ **Frontend:**
- React + TypeScript
- State management moderno
- UI/UX profesional
- Responsive design

✅ **DevOps:**
- Docker
- CI/CD
- Deploy en producción

### Tiempo estimado: 2-3 semanas

---

## FASE 3 (Opcional): Escalabilidad y Monetización

### Features Avanzadas
- [ ] Mobile app (React Native)
- [ ] Sistema de suscripciones
- [ ] API pública con rate limits por tier
- [ ] Machine Learning:
  - Predicción de cargos más probables
  - Recomendación personalizada
- [ ] Kubernetes para escalabilidad
- [ ] Monitoreo con Grafana + Prometheus

---

## Checklist de Tareas Inmediatas

### Hoy (Fase 1)
- [x] Crear ROADMAP.md
- [ ] Instalar Streamlit
- [ ] Crear app.py básica
- [ ] Implementar carga de datos
- [ ] Crear página de búsqueda
- [ ] Crear dashboard de estadísticas
- [ ] Deploy en Streamlit Cloud

### Próxima semana
- [ ] Recopilar feedback de usuarios
- [ ] Iterar sobre el MVP
- [ ] Decidir features para Fase 2

### En 1-2 semanas (Fase 2)
- [ ] Setup proyecto FastAPI
- [ ] Crear API básica
- [ ] Setup proyecto React + Vite
- [ ] Implementar primeras páginas
- [ ] Integrar frontend con backend
- [ ] Deploy inicial

---

## Recursos y Referencias

### Streamlit (Fase 1)
- [Documentación oficial](https://docs.streamlit.io)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Gallery de ejemplos](https://streamlit.io/gallery)

### FastAPI (Fase 2)
- [Documentación oficial](https://fastapi.tiangolo.com)
- [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

### React + TypeScript (Fase 2)
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org)
- [shadcn/ui](https://ui.shadcn.com)
- [TanStack Query](https://tanstack.com/query)

---

## Notas

- El MVP (Fase 1) es funcional para uso real
- La Fase 2 convierte el proyecto en portfolio-ready
- Cada fase es deployable y usable independientemente
- El código de la Fase 1 se puede reutilizar en la Fase 2

---

**Última actualización:** 2025-12-04
**Estado actual:** Fase 1 en progreso
