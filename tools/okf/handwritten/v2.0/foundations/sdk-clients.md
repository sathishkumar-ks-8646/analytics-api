---
type: Reference
title: SDK clients and code samples
description: The official Zoho Analytics client libraries (Java, C#, Go, PHP, Python, Node.js, Ruby), the Deluge scripting pattern, how each client is constructed from OAuth credentials, and how to read the per-endpoint SDK example documents.
tags:
  - zoho-analytics
  - rest-api-v2
  - sdk
  - client-libraries
  - code-samples
  - deluge
sources:
  - id: sdk-samples
    resource: /sdk-examples/index.md
    title: SDK code samples (10 files, 9 languages, 166 endpoints)
generated:
  at: {{NOW}}
status: stable
---

# Summary

Zoho Analytics publishes client libraries that wrap the REST API v2, handle OAuth token refresh, and expose the API as methods grouped by scope: an **org instance** (organization-level calls), a **workspace instance**, a **view instance**, and a **bulk instance** (import and export). Every OpenAPI-documented endpoint in this bundle has an [SDK example document](/sdk-examples/index.md) with a sample in each language plus cURL and Deluge. The samples use placeholder credentials (`1000.xxxxxxx`) and IDs; replace them with your own.

# Client Construction

All clients take the OAuth **client ID**, **client secret** and **refresh token** (see [Authentication](/foundations/authentication.md)) and obtain access tokens themselves.

| Language | Construction | Error type |
|---|---|---|
| Java | `AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);` then `ac.getOrgInstance(orgId)`, `ac.getWorkspaceInstance(orgId, workspaceId)`, `ac.getViewInstance(orgId, workspaceId, viewId)`, `ac.getBulkInstance(orgId, workspaceId)`. IDs are `long`. | `ServerException` with `getErrorCode()` and `getErrorMessage()`; `ParseException` for malformed responses. |
| C# | `IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);` then `ac.GetOrgInstance(orgId)` etc. Results are `System.Text.Json.JsonElement`. | `ServerException.GetErrorMessage()`. |
| Go | `ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)`; `ZAnalytics.GetOrgInstance(&ac, orgId)`, `GetBulkInstance(&ac, orgId, workspaceId)`. IDs are strings. | Returned `error` value. |
| PHP | `$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);` then `$ac->getOrgInstance($org_id)` etc. | `ServerException::getErrorMessage()`. |
| Python | `ac = AnalyticsClient(CLIENTID, CLIENTSECRET, REFRESHTOKEN)`; `ac.get_org_instance(ORGID)`, `ac.get_workspace_instance(ORGID, WORKSPACEID)`, `ac.get_view_instance(...)`, `ac.get_bulk_instance(ORGID, WORKSPACEID)`. Snake-case method names. | Exceptions carrying the server error message. |
| Node.js | `var ac = new analyticsClient(clientId, clientSecret, refreshToken);` then `ac.getOrgInstance(orgId)`, `ac.getBulkInstance(orgId, workspaceId)`. Methods return Promises. | Rejected promise with `errorCode` and `errorMessage`. |
| Ruby | Builder style: `AnalyticsClient.new.with_data_center("US").with_oauth({"clientId"=>..., "clientSecret"=>..., "refreshToken"=>...}).build`, then `get_org_instance(orgId)` etc. | Raised exception. |
| cURL | Plain HTTPS; put the access token in `Authorization: Zoho-oauthtoken <access_token>` and, for GET, send CONFIG with `--get --data-urlencode "CONFIG={...}"`. | Read the JSON failure envelope. |
| Deluge (Zoho scripting) | `invokeurl` with `url`, `type`, `headers` (a Map holding `ZANALYTICS-ORGID`) and `connection:"<oauth-connection-name>"`; CONFIG is URL-encoded with `zoho.encryption.urlEncode(config.toString())`. | Inspect the returned response map. |

# Mapping Endpoints to SDK Methods

SDK method names are camelCase (Java, C#, Node, PHP) or snake_case (Python, Ruby) versions of the endpoint titles, for example `getOrganizations`, `exportData`, `importData`, `shareViews`. The bulk instance carries import and export methods that write directly to or read from a local file path, for example `bulk.exportData(viewId, "csv", "/home/local/Sales.csv", config)`, so the caller never handles the job polling for asynchronous exports.

# Reading an SDK Example Document

Each document at `/sdk-examples/<domain>/<group>/<operation-id>.md` has frontmatter `api.operation_id`, `api.method`, `api.path`, `api.endpoint_doc` and `api.languages`, followed by one `## <Language>` section per language containing a fenced code block. Where the source provides more than one snippet for a language (for example single and bulk modes), they appear as numbered variants.

# Related

- [Authentication](/foundations/authentication.md)
- [Data centers](/foundations/data-centers.md)
- [Request conventions](/foundations/request-conventions.md)
- [SDK examples](/sdk-examples/index.md)
