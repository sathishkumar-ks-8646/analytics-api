---
type: API Endpoint
title: Get AutoML Analysis In Workspace
description: Returns every AutoML analysis defined in one workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - get
  - metadata
api:
  operation_id: getAutoMLAnalysisInWorkspace
  method: GET
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
  domain: dsml
  group: automl
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis/get"
    config_schema: null
    response_schema: GetAutoMLAnalysisInWorkspaceResponse
  sdk_examples: "/sdk-examples/dsml/automl/get-auto-ml-analysis-in-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/automl/workspaces/{workspace-id}/analysis`** - Get AutoML Analysis In Workspace (AutoML / Data Science & Machine Learning (AutoML)).

Returns every AutoML analysis defined in one workspace. Identical to [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) except that it is workspace-scoped and therefore omits the workspace fields.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAutoMLAnalysisInWorkspace` |
| HTTP method | GET |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis/get`; response schema `GetAutoMLAnalysisInWorkspaceResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get autoML analysis in workspace"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.analysis` | JSONArray | One entry per analysis in the workspace. **Always present**; empty array `[]` when there are none. |
| `analysis[].id` | String | ID of the analysis, as a string. Use as `<analysis-id>`. |
| `analysis[].name` | String | Name of the analysis. Unique within the workspace. |
| `analysis[].predictionType` | String | `"Regression"`, `"Classification"`, or `"Clustering"` — title case, unlike the upper-case request value. |
| `analysis[].trainingTable` | String | Name of the training table. |
| `analysis[].trainingTableId` | String | ID of the training table, as a string. |
| `analysis[].isDraft` | Boolean | `true` for an untrained draft created in the UI. |

> `workspaceId` and `workspaceName` are **not** returned here — they are unique to [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md).

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/automl/workspaces/137687000271334001/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/automl/workspaces/137687000271334009/analysis HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Workspace with several analyses**

```json
{
    "status": "success",
    "summary": "Get autoML analysis in workspace",
    "data": {
        "analysis": [
            {
                "id": "137687000000061115",
                "name": "PricePredictionAnalysis",
                "predictionType": "Regression",
                "trainingTable": "RealEstate_TrainData",
                "trainingTableId": "137687000000061002",
                "isDraft": false
            },
            {
                "id": "137687000000061117",
                "name": "SegmentationAnalysis",
                "predictionType": "Clustering",
                "trainingTable": "RealEstate_TrainData",
                "trainingTableId": "137687000000061002",
                "isDraft": false
            }
        ]
    }
}
```

**HTTP 200 OK — Workspace with no analyses**

```json
{
    "status": "success",
    "summary": "Get autoML analysis in workspace",
    "data": {
        "analysis": []
    }
}
```

**HTTP 403 Forbidden — Caller is the admin of a different workspace**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WorkspaceAdmin2) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get AutoML Analysis In Workspace](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-in-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Same entry shape as the org API, minus two fields** | The per-analysis object is identical except that `workspaceId` and `workspaceName` are absent, because the workspace is already fixed by the URL. |
| **Available to Workspace Admins** | Unlike [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), the owner of this workspace may call it. |
| **Still no models** | Model IDs require [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). |
| **Unfiltered and unpaged** | No search, sort, or paging parameters. |
| **Empty array, not an error** | A workspace with no analyses returns HTTP 200 with `"analysis": []`. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Get AutoML Analysis In Workspace → `id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller does not own this workspace. | Call from the standard API host as an Account Admin, Organization Admin, or the workspace's own admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-in-workspace.md).
