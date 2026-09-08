# py-mcp-inventory-v2


### create venv
```sh
python3 -m venv .venv
```
### activate
```sh
source .venv/bin/activate
```
### install dependecies
```sh
pip install -e .
```
### run
```sh
python -m app.main
```

## run mcp inspector
```sh
# Session 1 (venv activated and NO EXPORT env)
npx @modelcontextprotocol/inspector

# Sesssion 2 (venv activated)
python -m app.main

# Setup Transport Type: streamable http
http://localhost:5000/mcp
```

```
mcp-enterprise-server/
├── README.md
├── pyproject.toml                 # Dependencies (uv, poetry, or pip-tools)
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── config/
│   ├── settings.py                # Pydantic BaseSettings for env management
│   └── logging.py                 # Structured JSON logging & OpenTelemetry setup
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── main.py                # Server entry point (ASGI / FastMCP instantiation)
│       │
│       ├── domain/                # CORE DOMAIN (No external dependencies)
│       │   ├── __init__.py
│       │   ├── models/            # Core business entities & value objects
│       │   │   └── customer.py
│       │   ├── exceptions.py      # Domain-specific errors
│       │   └── ports/             # Interfaces / Abstract Base Classes
│       │       ├── crm_port.py    # Abstract CRM repository interface
│       │       └── cache_port.py  # Abstract cache interface
│       │
│       ├── application/           # USE CASES (Business Rules)
│       │   ├── __init__.py
│       │   ├── dtos/              # Input/Output DTOs for tool execution
│       │   │   └── customer_dto.py
│       │   └── use_cases/         # Application logic orchestrators
│       │       ├── fetch_customer.py
│       │       └── update_subscription.py
│       │
│       ├── infrastructure/        # ADAPTERS (External Systems)
│       │   ├── __init__.py
│       │   ├── clients/           # Downstream REST/gRPC implementations
│       │   │   ├── crm_client.py  # httpx implementation of crm_port.py
│       │   │   └── resilience.py  # PyBreaker circuit breakers & retries
│       │   ├── security/          # Auth, Token Exchange, OIDC
│       │   │   └── token_exchange.py
│       │   ├── cache/             # Redis implementation of cache_port.py
│       │   │   └── redis_adapter.py
│       │   └── telemetry/         # OpenTelemetry tracing & metrics
│       │       └── tracer.py
│       │
│       └── presentation/          # MCP ADAPTERS (Protocol Layer)
│           ├── __init__.py
│           ├── mcp_app.py         # FastMCP setup & lifecycle hooks
│           ├── schemas/           # Pydantic models for MCP Tool Args (LLM-facing)
│           │   └── customer_schemas.py
│           ├── tools/             # MCP Tool definitions (@mcp.tool)
│           │   ├── __init__.py
│           │   └── customer_tools.py
│           ├── resources/         # MCP Resource definitions (@mcp.resource)
│           │   └── crm_resources.py
│           └── prompts/           # MCP Prompt templates (@mcp.prompt)
│               └── support_prompts.py
│
└── tests/
    ├── unit/                      # Tests domain & use cases (fast, no external calls)
    ├── integration/               # Tests clients with mock servers (WireMock/respx)
    └── e2e/                       # Tests full MCP JSON-RPC protocol roundtrips
```