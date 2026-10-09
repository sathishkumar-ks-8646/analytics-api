---
type: Guide
title: How to use this bundle
description: Structure of the Zoho Analytics REST API v2 OKF bundle, the frontmatter contract of each concept type, and navigation rules for AI assistants, SDK generators, Postman runners and MCP servers.
tags:
  - zoho-analytics
  - okf
  - guide
  - start-here
  - tooling
generated:
  at: {{NOW}}
status: stable
---

# Summary

This bundle follows the Open Knowledge Format (OKF) v0.2: a directory tree of markdown files, each with YAML frontmatter that starts with a `type`. Reserved files `index.md` (directory listing) and `log.md` (history) carry no frontmatter except `okf_version` at the root. Links in document bodies are relative to the document that contains them, so they resolve on GitHub, in a clone and under any raw-file base. Paths that start with `/` appear only in frontmatter (`resource`, `sources[].resource`, `api.openapi.file`, `api.sdk_examples`) and are relative to the bundle root. The bundle is generated from the source documents of this API version in the `analytics-api` repository (`<version>/md`, `<version>/zenesis-oas`, `<version>/zenesis-oas-samples`) by `tools/okf/build_okf.py`; regenerate it instead of editing generated files by hand.

# Directory Layout

| Path | Contents | Concept type |
|---|---|---|
| `/overview.md` | What the API is and the five conventions. | `API Overview` |
| `/endpoint-catalog.md` | Every endpoint in one table. | `API Catalog` |
| `/foundations/` | Shared rules: authentication, data centers, request conventions, response envelope, HTTP statuses, error codes, scopes, roles, permission matrix, identifiers, criteria syntax, async jobs, rate limits, export and import enums, white label, glossary, SDK clients. | `Reference`, `Concept`, `Error Catalog`, `Authentication` |
| `/domains/<domain>/overview.md` | One document per domain: description, groups, endpoints. | `API Domain` |
| `/domains/<domain>/<group>/overview.md` | One document per API group: concepts, limits, permission model, shared CONFIG attributes, notes. | `API Group` |
| `/domains/<domain>/<group>/<operation-id>.md` | One document per endpoint. | `API Endpoint` |
| `/workflows/` | Step-by-step multi-endpoint procedures. | `Playbook` |
| `/sdk-examples/<domain>/<group>/<operation-id>.md` | Code samples in 9 languages per endpoint. | `SDK Example` |
| `/references/openapi/` | The OpenAPI 3 files (one per domain) and the shared components file. | JSON, not concepts |
| `/references/endpoint-catalog.json` | Machine-readable catalog of every endpoint with method, path, scopes, permission, error codes and doc paths. | JSON |

# The `API Endpoint` Frontmatter Contract

Every endpoint document carries an `api` mapping designed for programmatic consumption:

| Key | Meaning |
|---|---|
| `api.operation_id` | Stable identifier, identical to the OpenAPI `operationId`. Also the file name in kebab-case. |
| `api.method`, `api.path` | HTTP method and path template with `{placeholders}`. |
| `api.domain`, `api.group` | Slugs matching the directory names. |
| `api.oauth_scopes` | Scopes accepted by the endpoint. |
| `api.org_id_header` | `required`, `optional` or `not-required`. |
| `api.config_parameter.location` | `query`, `form`, `multipart` or `none`; `.required` says whether CONFIG may be omitted. |
| `api.request_content_type` | Present when the endpoint has a request body. |
| `api.success_status` | `200` or `204`. |
| `api.response_content_types` | Media types of a successful response (JSON or file types for exports). |
| `api.permission_required` | Human-readable role or view-permission requirement. |
| `api.error_codes` | Every documented error code for the endpoint. |
| `api.openapi.file`, `api.openapi.pointer` | Where to find the operation in the OpenAPI files; `config_schema` and `response_schema` name the component schemas. |
| `api.sdk_examples` | Path to the SDK examples concept. |

The body of every endpoint document uses the same H1 sections in the same order: `Summary`, `Endpoint`, `Request`, `Response`, `Examples`, `Notes & Behaviour` (when present), `Error Codes`, `Related`. Tables inside `Request` describe CONFIG fields with columns Parameter, Type, Mandatory, Default, Description.

# Navigation Rules for Agents

1. **Answering "how do I..." questions**: start at `/overview.md`, then the relevant domain `overview.md`, then the endpoint document. Read the group `overview.md` for limits and permission models before recommending an endpoint.
2. **Building a request**: take method, path and CONFIG location from the endpoint frontmatter, the CONFIG fields from the `Request` section, and encoding rules from [Request conventions](/foundations/request-conventions.md).
3. **Diagnosing a failure**: look up `data.errorCode` in [Error code catalog](/foundations/error-codes.md); the anchor is `#error-<code>`.
4. **Choosing scopes**: use `api.oauth_scopes` of every endpoint the integration calls, or consult [OAuth scopes](/foundations/oauth-scopes.md) for the operations per scope.
5. **Checking authorization**: [Permission matrix](/foundations/permission-matrix.md) lists the required role per endpoint; [Roles & permissions](/foundations/roles-and-permissions.md) defines the roles.
6. **Generating SDKs or collections**: read `/references/endpoint-catalog.json` for the inventory, then the OpenAPI files for schemas; use `/sdk-examples/` for idiomatic usage per language.
7. **Multi-step tasks**: check `/workflows/` first; each playbook links the exact endpoints in order and names the IDs that flow between them.

# Provenance and Trust

Every concept carries `generated.at` (build time) and, where applicable, `sources` pointing at the OpenAPI file or the bundle concepts it was derived from; all source references are bundle-internal paths or public URLs. No concept carries `verified`, so the trust tier of the whole bundle is **unverified** in OKF terms: content is faithful to the source documents but has not been re-confirmed by a human against the live service. Add `verified: { by: human:<id>, at: <timestamp> }` to a concept after reviewing it. Concepts whose content came from outside the source documents (only [Data centers](/foundations/data-centers.md) and the general OAuth flow in [Authentication](/foundations/authentication.md)) say so explicitly in their body.

# Regenerating

```bash
python3 tools/okf/build_okf.py --version v2.0   # rebuilds v2.0/okf/ from the v2.0 sources and tools/okf/handwritten/v2.0/
python3 tools/okf/validate_okf.py v2.0/okf          # checks frontmatter, reserved files and link targets
```

Hand-written concepts live in `tools/okf/handwritten/v2.0/` and are copied into the bundle on every build.
