---
type: API Endpoint
title: Update Datasource Connection
description: "Updates the connection details of a database-style datasource — host, port, credentials, and the service-specific settings that go with them."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - put
  - metadata
api:
  operation_id: updateDatasourceConnection
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}"
  domain: data-operations
  group: data-sync-and-connectivity
  oauth_scopes:
    - ZohoAnalytics.metadata.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Edit Datasource permission on the workspace."
  error_codes:
    - 7301
    - 8077
    - 8078
    - 8079
    - 8504
    - 8507
    - 8509
    - 8535
    - 18055
    - 18057
    - 18061
    - 18063
    - 18064
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources~1{datasource-id}/put"
    config_schema: DatasourceConnectionConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-operations/data-sync-and-connectivity/update-datasource-connection.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}`** - Update Datasource Connection (Data Sync & Connectivity / Data Operations).

Updates the connection details of a **database-style datasource** — host, port, credentials, and the service-specific settings that go with them.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the datasource. |
| `<datasource-id>` | Long | `dataSources[].datasourceId` of a **database** connection. |

> **This API applies only to database connections** — cloud databases, local databases reached through Zoho Databridge, and Live Connect databases. File, web, cloud-storage, integration-connector, snapshot, and local-drive datasources are not editable through it, and a `datasourceId` belonging to one of those is rejected with [`18061`](../../../foundations/error-codes.md#error-18061).

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateDatasourceConnection` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Edit Datasource permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources~1{datasource-id}/put`; CONFIG schema `DatasourceConnectionConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{datasource-id}` | string | ID of the datasource. | [How to obtain](../../../foundations/identifiers.md#datasource-id) |

## CONFIG Parameters

**Always required**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceName` | String | **Yes** | The cloud service hosting the database. See [`serviceName` values](#servicename-values). An unrecognised value fails with `18057`. |
| `hostName` | String | **Yes** | Service endpoint or hostname, up to 10,000 characters. For **AMAZON ATHENA** send the AWS region instead; for **SNOWFLAKE** send the full account name. |
| `userName` | String | **Yes** | Login username for the database, up to 1,000 characters. |

**Commonly required**

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `databaseType` | String | Conditional | — | The database engine. **Mandatory whenever the chosen `serviceName` supports more than one engine**, otherwise `8079`. Omit only when the service has exactly one. A combination that does not exist fails with `18055`. |
| `password` | String | No | — | Login password, up to 1,000 characters. Omit to leave the stored password unchanged. |
| `port` | Long | No | Engine default | Database port. When omitted, the default port of the chosen `databaseType` is used. |
| `cloudDatabaseName` | String | No | — | Name of the database on the service, up to 10,000 characters. |
| `instanceName` | String | No | — | For **SQLSERVER**, the named instance. Omit to use the default instance. |
| `schemaName` | String | No | `""` | Schema to connect to, up to 10,000 characters. |

**Service-specific**

| Attribute | Type | Applies to | Description |
|-----------|------|------------|-------------|
| `warehouseName` | String | Snowflake | Warehouse to run queries on, up to 10,000 characters. |
| `s3OutputLocation` | String | Amazon Athena | S3 path where query results are written, up to 10,000 characters. |
| `workgroupName` | String | Amazon Athena, Amazon Redshift Serverless | Workgroup name, up to 150 characters. |
| `dataLocation` | String | Amazon Athena, Google BigQuery | Region or data location, up to 30 characters. |
| `projectId` | String | Google BigQuery | Project ID, up to 10,000 characters. |
| `sId` | String | Oracle | Oracle System ID (SID), up to 10,000 characters. |
| `catalogName` | String | Databricks and catalog-based engines | Catalog to connect to, up to 150 characters. Defaults to the engine's own default catalog when omitted for Databricks. |
| `httpPath` | String | Databricks | HTTP path of the SQL warehouse or cluster. |
| `refreshToken` | String | OAuth-authenticated services | OAuth refresh token, up to 1,000 characters. |
| `accessToken` | String | OAuth-authenticated services | OAuth access token, up to 1,000 characters. |
| `connectionString` | String | MongoDB variants, ODBC, OLEDB, HFSQL | Full connection string, up to 20,000 characters. For ODBC, OLEDB, and HFSQL this replaces the host/port/credential fields. |
| `authSource` | String | MongoDB variants | Authentication database, up to 1,000 characters. |
| `connType` | Integer | MongoDB variants | How the connection is expressed. `1` individual fields (host, port, user), `2` a single `connectionString`. For every other engine this is derived from `databaseType` and any value sent is replaced. |

**Transport security**

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `useSSL` | Boolean | No | `false` | Whether the connection uses SSL. |
| `useSSLCertificate` | Boolean | No | `false` | Whether a client SSL certificate is presented. |
| `useSSH` | Boolean | No | `false` | Whether the connection is tunnelled over SSH. When `false`, all `sshTunnel*` attributes are ignored. |
| `sshTunnelHost` | String | Conditional | `""` | SSH tunnel hostname, up to 10,000 characters. Required when `useSSH` is `true`. |
| `sshTunnelPort` | Long | Conditional | `""` | SSH tunnel port. |
| `sshTunnelUsername` | String | Conditional | `""` | SSH tunnel username, up to 10,000 characters. |
| `sshTunnelPassword` | String | Conditional | `""` | SSH tunnel password or passphrase, up to 10,000 characters. |
| `sshTunnelAuthType` | Integer | No | `0` | SSH authentication method. `0` password, `1` public key. |

### `serviceName` values

| Value | Notes |
|-------|-------|
| `AMAZON RDS` | Supports several engines — `databaseType` is required. |
| `AMAZON REDSHIFT` | |
| `MICROSOFT AZURE` | Supports several engines — `databaseType` is required. |
| `GOOGLE CLOUD SQL` | Supports several engines — `databaseType` is required. |
| `HEROKU POSTGRESQL` | |
| `LOCAL DATABASE` | A database reached through Zoho Databridge. Supports many engines. |
| `SNOWFLAKE` | Send the account name as `hostName`, and `warehouseName`. |
| `AMAZON ATHENA` | Send the AWS region as `hostName`, plus `s3OutputLocation`. |
| `GOOGLE BIG QUERY` | Send `projectId`. |
| `PANOPLY` | |
| `RACKSPACE CLOUD` | |
| `IBM CLOUD` | |
| `ORACLE CLOUD` | |
| `OTHER CLOUD SERVICES` | For a database not covered by a named service. |
| `MONGODB ATLAS` | Uses `connectionString` / `authSource` / `connType`. |
| `AMAZON DOCUMENTDB` | Uses `connectionString` / `authSource` / `connType`. |
| `SINGLESTORE` | |
| `DIGITALOCEAN` | |
| `AMAZON LIGHTSAIL` | |
| `YELLOWBRICK` | |
| `DATABRICKS` | Send `httpPath` and, optionally, `catalogName`. |

Values are matched case-insensitively.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm the update by re-reading [Get Datasources](get-datasources.md), or by running [Sync Data](sync-datasource.md) and checking the outcome.

# Examples

## Sample Requests

**Case 1 — rotate the password on an Amazon RDS MySQL connection**

The minimum useful update: the three mandatory attributes plus the new credential.

```http
PUT /restapi/v2/workspaces/466206000000071000/datasources/466206000000081000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "serviceName": "AMAZON RDS",
  "databaseType": "MYSQL",
  "hostName": "zylker.abcdef.us-east-1.rds.amazonaws.com",
  "port": 3306,
  "userName": "zylkeradmin",
  "password": "Zoho@123",
  "cloudDatabaseName": "sales_db",
  "useSSL": true
}
```

**Case 2 — a Snowflake connection, covering the service-specific attributes**

```json
{
  "serviceName": "SNOWFLAKE",
  "databaseType": "SNOWFLAKE",
  "hostName": "zylker-sales.us-east-1",
  "userName": "ZYLKER_ANALYTICS",
  "password": "Zoho@123",
  "cloudDatabaseName": "SALES_DB",
  "warehouseName": "COMPUTE_WH",
  "schemaName": "PUBLIC"
}
```

**Case 3 — a local database reached over an SSH tunnel**

Covers the whole transport-security group in one call.

```json
{
  "serviceName": "LOCAL DATABASE",
  "databaseType": "POSTGRESQL",
  "hostName": "10.0.0.14",
  "port": 5432,
  "userName": "zylker_ro",
  "password": "Zoho@123",
  "cloudDatabaseName": "warehouse",
  "schemaName": "public",
  "useSSL": true,
  "useSSLCertificate": false,
  "useSSH": true,
  "sshTunnelHost": "bastion.zylker.com",
  "sshTunnelPort": 22,
  "sshTunnelUsername": "tunneluser",
  "sshTunnelPassword": "Zoho@456",
  "sshTunnelAuthType": 0
}
```

**Case 4 — Amazon Athena, where `hostName` carries a region**

```json
{
  "serviceName": "AMAZON ATHENA",
  "databaseType": "AMAZON ATHENA",
  "hostName": "us-east-1",
  "userName": "AKIAIOSFODNN7EXAMPLE",
  "password": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "s3OutputLocation": "s3://zylker-athena-results/",
  "workgroupName": "primary",
  "dataLocation": "us-east-1"
}
```

## Sample Responses

**HTTP 204 No Content — the connection was updated**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — `serviceName` is not recognised**

```json
{
  "status": "failure",
  "summary": "INVALID_CLOUD_SERVICENAME",
  "data": {
    "errorCode": 18057,
    "errorMessage": "Invalid cloud service name."
  }
}
```

**HTTP 400 Bad Request — the engine does not belong to that service**

```json
{
  "status": "failure",
  "summary": "DBTYPE_SERVICENAME_NOTMACHED",
  "data": {
    "errorCode": 18055,
    "errorMessage": "The given database type does not match the given service name."
  }
}
```

**HTTP 400 Bad Request — attempting to change the engine of a Live Connect database**

```json
{
  "status": "failure",
  "summary": "DBTYPE_CANNOT_BE_UPDATED_FOR_LIVECONNECT_DB",
  "data": {
    "errorCode": 18063,
    "errorMessage": "Database type cannot be updated for a live connect database."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Datasource Connection](../../../sdk-examples/data-operations/data-sync-and-connectivity/update-datasource-connection.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It is a full replace of the connection, not a patch** | Attributes you omit are reset to their defaults rather than preserved. Always resend the complete connection definition, changing only what you intend to change. `password` is the one practical exception — omitting it keeps the stored password. |
| **`serviceName`, `hostName`, and `userName` are always mandatory** | Even when only the password is changing. |
| **`databaseType` is conditionally mandatory** | Required whenever the chosen service supports more than one engine. When the service has exactly one, it is inferred. Omitting it for a multi-engine service fails with `8079` naming `databaseType`. |
| **Live Connect connections are partly frozen** | `serviceName` cannot be changed (`18064`) and `databaseType` cannot be changed (`18063`). Credentials, host, and port can. |
| **`connType`, `authSource`, and `connectionString` are honoured only for MongoDB variants** | For every other engine the server derives them from `databaseType` and replaces whatever was sent. |
| **`useSSH` is the master switch for the tunnel** | With `useSSH` absent or `false`, all `sshTunnel*` attributes are ignored and stored empty. |
| **Every credential and endpoint field is treated as sensitive** | Host names, usernames, passwords, tokens, and connection strings are excluded from request logging. |
| **The connection is not tested by this call** | A `204` means the details were stored, not that they work. Run [Sync Data](sync-datasource.md) and check the result to confirm. |
| **It cannot create a datasource** | The `<datasource-id>` must already exist. A file, web, connector, or snapshot ID is rejected with `18061`. |
| **Dependency chain:** | [Get Datasources](get-datasources.md) → `datasourceId` → Update Datasource Connection → [Sync Data](sync-datasource.md) → [Get Last Import Details](get-last-import-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller lacks Create Table and Edit Datasource permission on the workspace. | Call from the standard API host with one of the two permissions. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` was not sent, or was sent empty. | Send a CONFIG object with at least `serviceName`, `hostName`, and `userName`. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — A mandatory attribute was sent blank. | The message names the attribute. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing — usually `databaseType` for a service that supports several engines. | The message names the attribute. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` is missing entirely. | Send the CONFIG object. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — An attribute exceeds its length limit. | See [Limitations](overview.md#limitations). |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — `serviceName` or `databaseType` is not one of the accepted values. | Send a value from [`serviceName` values](#servicename-values). |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.update`. |
| [18055](../../../foundations/error-codes.md#error-18055) | 400 | `DBTYPE_SERVICENAME_NOTMACHED` — The `databaseType` is not available for the given `serviceName`. | Pick an engine the service actually offers. |
| [18057](../../../foundations/error-codes.md#error-18057) | 400 | `INVALID_CLOUD_SERVICENAME` — `serviceName` is not a recognised service. | Send a value from [`serviceName` values](#servicename-values). |
| [18061](../../../foundations/error-codes.md#error-18061) | 400 | `CONNECTION_ID_NOT_ASSOSIATED_FOR_WORKSPACE` — The datasource ID does not exist in this workspace, or is not a database connection (HTTP 404). | Verify `<datasource-id>` with [Get Datasources](get-datasources.md). |
| [18063](../../../foundations/error-codes.md#error-18063) | 400 | `DBTYPE_CANNOT_BE_UPDATED_FOR_LIVECONNECT_DB` — `databaseType` differs from the stored one on a Live Connect database. | Resend the existing `databaseType`. |
| [18064](../../../foundations/error-codes.md#error-18064) | 400 | `SERVICE_NAME_CANNOT_BE_UPDATED_FOR_LIVECONNECT_DB` — `serviceName` differs from the stored one on a Live Connect database. | Resend the existing `serviceName`. |

# Related

- [Data Sync & Connectivity overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Sync Data](sync-datasource.md), [Refetch Data](refetch-datasource.md), [Get Datasources](get-datasources.md), [Get Last Import Details](get-last-import-details.md).
- [SDK examples](../../../sdk-examples/data-operations/data-sync-and-connectivity/update-datasource-connection.md).
