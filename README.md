# Supporting Information: MD-Models infrastructure

This project runs a local `mdmodels` stack with:

- a Postgres/pgvector database
- a REST API for dataset CRUD operations
- an MCP server that Claude Desktop can connect to

The notebook `UploadDataset.ipynb` uses the REST API directly (`http://localhost:8800`) to create and list `Experiment` datasets defined by `model.md`.

## The `Experiment` model

`model.md` is the single Markdown specification the whole stack is built from. It
defines four objects and one enumeration:

- `Experiment` — a name, a description, a list of `Molecule` objects, a list of
  `Enzyme` objects, and a single `Conditions` object.
- `Molecule` — a name, an initial concentration, and a `Role`.
- `Enzyme` — a name, an initial concentration, and a `Role`.
- `Conditions` — temperature and pH.
- `Role` — an enumeration with the values `substrate`, `product`, `cofactor`,
  `inhibitor`, `enzyme`.

The frontmatter declares `schema:` and `OBO:` prefixes, and most attributes carry
a `Term:` annotation from schema.org, ChEBI, PR or PATO.

## Generated artefacts

`gen.toml` is the pipeline configuration. Running `md-models pipeline -i gen.toml`
regenerates every artefact from `model.md`:

- `code/` — Python (dataclass, Pydantic, Pydantic-XML), TypeScript, TypeScript
  (Zod), Rust, Go, Julia.
- `schemes/` — XSD, JSON Schema, Protobuf, GraphQL, LinkML.
- `diagrams/` — a Mermaid class diagram.

## MCP server tools

The MCP server (`mcp`, host port `7001`) is built by py-mdmodels (pinned to
0.3.1 in the Dockerfiles; the tool set is the same in 0.4.0) from `model.md`. With `all_create = true` in `config.toml` it exposes 14 tools for the
`Experiment` model:

| Tool | Function |
|---|---|
| `Get_Table_Schema` | Returns the Markdown data model with all fields, types, relationships and nesting. |
| `Get_Table_Relationships` | Returns the foreign-key mappings of a table. |
| `Upsert_Experiment`, `Upsert_Molecule`, `Upsert_Enzyme`, `Upsert_Conditions` | Write a nested record across the tables in one transaction, or update an existing one when its row key is given. Nested fields may reference existing rows by key. |
| `Select_Table` | Selects rows from one table with optional filters and a row limit. |
| `Aggregate_Table` | count / sum / avg / min / max / stddev / variance over a table, with optional filters. |
| `Plot_Table` | Queries a table with optional filters, optionally grouped by a column of a related table, and renders an interactive chart. |
| `Download_Entry` | Fetches one entry by primary key as a JSON tree for copying or download. |
| `Data_Entry` | Renders a typed form whose fields, labels, types and bounds are specified by the agent. |
| `Submit_Data_Entry` | Form callback: checks the submitted values against the form specification and returns them to the agent. |
| `Annotate_Entries`, `Get_Annotations` | Free-text annotations on rows of any table. |

A `Vector_Search` tool is added when a table has an embedding column. The form
fields are not derived from the schema: the agent writes the form and maps the
submitted values to columns when it calls an `Upsert_*` tool.

The conversations in `chats/` were run with earlier server versions. The first used
a `Create Experiment` tool, which the `Upsert_*` tools replaced in April 2026. Tool
calls were not logged, so their arguments are not part of the transcripts.

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

From the repository root:

```bash
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

## Analysis scripts

Two self-contained checks are kept alongside the model. Each has its own
`pyproject.toml` and is run with `uv run`.

- `reasoner-check/` — generates the OWL serialisation of `model.md` and of the
  EnzymeML v2 schema, then tests logical consistency with the HermiT reasoner and
  an OWL-RL closure. Output: `reasoner-check/report.json`.
- `linkml-roundtrip/` — exports each model to LinkML, reloads it with
  `linkml-runtime`, and reports which modelling features survive the conversion.
  Output: `linkml-roundtrip/report.json`.

Both need `md-models` 0.2.11 or newer available to `mdmodels-core`.

## Representative Claude Desktop conversations

These conversations were conducted via Claude Desktop and use the local MCP server described in this repository.

- [Create a new experiment](https://claude.ai/share/c970ec8f-5276-4424-af5c-763444ddc6bc)
- [Query existing experiments](https://claude.ai/share/29a18161-596b-4036-9d9d-56e43ab397d1)
