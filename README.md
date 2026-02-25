# Supporting Information: MD-Models infrastructure

This project runs a local `mdmodels` stack with:

- a Postgres/pgvector database
- a REST API for dataset CRUD operations
- an MCP server that Claude Desktop can connect to

The notebook `UploadDataset.ipynb` uses the REST API directly (`http://localhost:8800`) to create and list `Experiment` datasets defined by `model.md`.

## What is running

`docker-compose.yml` starts 4 services:

- `db` (Postgres + pgvector)
- `bootstrap` (initializes schema/config via `mdmodels`)
- `api` (REST API exposed on host port `8800`)
- `mcp` (MCP streamable HTTP endpoint exposed on host port `7001`)

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)
- `npx` (Node.js installed) for Claude Desktop MCP bridge:
  - command used: `npx mcp-remote http://127.0.0.1:7001/mcp`
- Claude Desktop installed

## 1) Start the stack locally

From this folder:

```bash
cd /Users/janrange/GitHub/md-models-demo/database
./start.sh
```

`start.sh` does:

1. `docker compose -p md-models-demo down`
2. `docker compose up --build -d`

This builds images and starts all services in the background.

### Verify services

```bash
docker compose ps
```

You should see `db`, `api`, and `mcp` up, and `bootstrap` completed successfully.

### Quick API check

```bash
curl http://localhost:8800/experiment/
```

If the API is healthy, you should get a JSON array response.

### Quick MCP check

```bash
curl http://127.0.0.1:7001/mcp
```

You should get an HTTP response (often not a user-friendly body, but reachable).

## 2) Add this MCP server to Claude Desktop (local)

Edit Claude Desktop config file:

- macOS path: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add/update your MCP server entry like this:

```json
{
  "mcpServers": {
    "Experiments": {
      "command": "npx",
      "args": ["mcp-remote", "http://127.0.0.1:7001/mcp"],
      "env": {}
    }
  }
}
```

Notes:

- Your selected block (`Experiments` with `npx mcp-remote`) is correct for a local MCP HTTP endpoint.
- If you already have other entries under `mcpServers`, keep them and add this as another key.
- Fully quit and relaunch Claude Desktop after editing the config.
- Ensure the Docker stack is running before starting Claude, otherwise this MCP server will fail to connect.

## 3) How `UploadDataset.ipynb` uses the API

The notebook is an API client example for the local REST service:

1. Installs/imports `mdmodels`, `httpx`, `rich`
2. Loads model schema from `model.md`
3. Creates a typed `Experiment` object (conditions + molecules + enzymes)
4. Sends it to the REST API:
   - `POST http://localhost:8800/experiment/`
5. Reads existing datasets:
   - `GET http://localhost:8800/experiment/`

This means:

- MCP integration (Claude Desktop) and notebook usage both point to the same local backend data stack.
- If API calls from the notebook fail, verify containers are running and `localhost:8800` is reachable.

## Useful commands

Start/restart:

```bash
./start.sh
```

View logs:

```bash
docker compose logs -f api
docker compose logs -f mcp
```

Stop everything:

```bash
docker compose down
```

## Representative Claude Desktop conversations

These conversations were conducted via Claude Desktop and utilize the local MCP server described in this repository.

- [Create a new experiment](https://claude.ai/share/c970ec8f-5276-4424-af5c-763444ddc6bc)
- [Query existing experiments](https://claude.ai/share/29a18161-596b-4036-9d9d-56e43ab397d1)
