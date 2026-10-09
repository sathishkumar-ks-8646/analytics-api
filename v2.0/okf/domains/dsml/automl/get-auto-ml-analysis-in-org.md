---
type: API Endpoint
title: Get AutoML Analysis In Org
description: "Returns every AutoML analysis across all workspaces in the organization, each tagged with the workspace it belongs to."
resource: https://analyticsapi.zoho.com/restapi/v2/automl/analysis
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - get
  - metadata
api:
  operation_id: getAutoMLAnalysisInOrg
  method: GET
  path: "/restapi/v2/automl/analysis"
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
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organization. A Workspace Admin is not sufficient.
  error_codes:
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1analysis/get"
    config_schema: null
    response_schema: GetAutoMLAnalysisInOrgResponse
  sdk_examples: "/sdk-examples/dsml/automl/get-auto-ml-analysis-in-org.md"
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

**GET `/restapi/v2/automl/analysis`** - Get AutoML Analysis In Org (AutoML / Data Science & Machine Learning (AutoML)).

Returns every AutoML analysis across **all workspaces** in the organization, each tagged with the workspace it belongs to. This is the organization-wide inventory call.

> This API has no CONFIG parameter and no workspace in its path.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAutoMLAnalysisInOrg` |
| HTTP method | GET |
| URL | `/restapi/v2/automl/analysis` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID whose analyses are listed. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. A Workspace Admin is not sufficient. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1analysis/get`; response schema `GetAutoMLAnalysisInOrgResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get autoML analysis in organization"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.analysis` | JSONArray | One entry per analysis in the organization. **Always present**; empty array `[]` when there are none. |
| `analysis[].id` | String | ID of the analysis, serialised as a **string**. Use as `<analysis-id>` in the workspace-scoped APIs. |
| `analysis[].name` | String | Name of the analysis. Unique within its workspace. |
| `analysis[].predictionType` | String | `"Regression"`, `"Classification"`, or `"Clustering"`. **Returned in title case**, whereas [Create AutoML Analysis](create-auto-ml-analysis.md) accepts it in upper case — do not compare the two directly. |
| `analysis[].trainingTable` | String | Name of the table the analysis was trained on. |
| `analysis[].trainingTableId` | String | ID of the training table, as a string. |
| `analysis[].isDraft` | Boolean | `true` when the analysis was saved but never trained. Analyses created through this API are never drafts — drafts originate from the Zoho Analytics UI. |
| `analysis[].workspaceId` | String | ID of the workspace holding the analysis. **Only present in this API** — pair it with `id` to address the analysis in the workspace-scoped APIs. |
| `analysis[].workspaceName` | String | Name of that workspace. **Only present in this API.** |

# Examples

## Sample Requests

**Case 1 — Standard organization**

```http
GET /restapi/v2/automl/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/automl/analysis HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Analyses across two workspaces**

```json
{
    "status": "success",
    "summary": "Get autoML analysis in organization",
    "data": {
        "analysis": [
            {
                "id": "137687000000061115",
                "name": "Workspace1Analysis",
                "predictionType": "Regression",
                "trainingTable": "RealEstate_TrainData",
                "trainingTableId": "137687000000061002",
                "isDraft": false,
                "workspaceId": "137687000271334001",
                "workspaceName": "Real Estate Analytics"
            },
            {
                "id": "137687000000061116",
                "name": "Workspace2Analysis",
                "predictionType": "Classification",
                "trainingTable": "Churn_TrainData",
                "trainingTableId": "137687000000061004",
                "isDraft": false,
                "workspaceId": "137687000271334002",
                "workspaceName": "Customer Analytics"
            }
        ]
    }
}
```

**HTTP 200 OK — Organization with no AutoML analyses**

```json
{
    "status": "success",
    "summary": "Get autoML analysis in organization",
    "data": {
        "analysis": []
    }
}
```

**HTTP 403 Forbidden — Caller is a Workspace Admin, or the request came through a portal domain**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WorkspaceAdmin) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get AutoML Analysis In Org](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-in-org.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only organization-wide AutoML API** | Every other API in this family is scoped to a single workspace. Use this one to find analyses when you do not already know which workspace holds them. |
| **Adds `workspaceId` / `workspaceName`** | These two fields are what make the response actionable — every follow-up call needs the workspace in its path. [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) omits them because the workspace is already known. |
| **No models, no deployments** | The response is a flat analysis inventory. Model IDs come only from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). |
| **Stricter role gate than the rest of the family** | A Workspace Admin who can fully manage AutoML inside their own workspace still receives `7301` here, because the API is organization-scoped. |
| **Unfiltered and unpaged** | No search, sort, or paging parameters. Filter client-side on `workspaceId`, `predictionType`, or `isDraft`. |
| **Empty array, not an error** | An organization with no analyses returns HTTP 200 with `"analysis": []`. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | Get AutoML Analysis In Org → `workspaceId` + `id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller is not an Account Admin / Organization Admin of the organization. | Call from the standard API host as an Account Admin or Organization Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-in-org.md).
