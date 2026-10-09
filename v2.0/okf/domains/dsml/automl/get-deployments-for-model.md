---
type: API Endpoint
title: Get Deployments For A Model
description: "Returns the deployment details configured for an AutoML analysis model, including the input and output tables, the schedule status and the time at which the deployment last ran."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - get
  - metadata
api:
  operation_id: getDeploymentsForModel
  method: GET
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
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
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1deployments/get"
    config_schema: null
    response_schema: GetDeploymentsForModelResponse
  sdk_examples: "/sdk-examples/dsml/automl/get-deployments-for-model.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments`** - Get Deployments For A Model (AutoML / Data Science & Machine Learning (AutoML)).

Returns the deployment configured for a model — its input and output tables, schedule outcome, and last run status.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getDeploymentsForModel` |
| HTTP method | GET |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1deployments/get`; response schema `GetDeploymentsForModelResponse` |

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
| `{analysis-id}` | string | ID of the AutoML analysis. | [How to obtain](../../../foundations/identifiers.md#analysis-id) |
| `{model-id}` | string | ID of the AutoML analysis model. | [How to obtain](../../../foundations/identifiers.md#model-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get deployments for a model"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.deployments` | JSONObject | The deployment configured for the model. **A single object, not an array** — despite the plural key, a model can hold at most one deployment. |
| `deployments.deploymentId` | String | ID of the deployment, as a string. This is the `<deployment-id>` for [Run AutoML Analysis](run-auto-ml-analysis.md) and [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md). |
| `deployments.analysisId` | String | ID of the analysis the deployment belongs to. Echoes the URL. |
| `deployments.inputTable` | String | Name of the table whose rows are scored. |
| `deployments.inputTableId` | String | ID of that input table, as a string. |
| `deployments.outputTable` | String | Name of the table the predictions are written to. |
| `deployments.outputTableId` | String | ID of the output table. Use it with the [Row / Export APIs](../../data-operations/row-operations/overview.md) to read the predictions. |
| `deployments.status` | String | Status of the **most recent run** of the deployment, e.g. `"In progress"`, `"Completed"`. **Distinct from the top-level `status`.** |
| `deployments.lastDeploymentTime` | String | When the deployment last ran, in `dd MMM yyyy HH:mm:ss` format. |
| `deployments.outputColumns` | JSONArray of String | Columns copied from the input table into the output table alongside the prediction. |
| `deployments.predictionColumn` | String | Name of the column in the output table that holds the predicted value. |
| `deployments.stack` | String | Server memory used for the deployment job (`"8 GB"`, `"16 GB"`, `"32 GB"`). |
| `deployments.importType` | String | How predictions are written to the output table. **Returned in lower case** (`"truncateadd"`, `"append"`, `"updateadd"`), whereas [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) expects upper case. |

> `matchingColumns` and the schedule definition are **not** returned, even for an `updateadd` deployment. Retain them yourself if you need to reproduce a deployment.

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/deployments HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/automl/workspaces/137687000271334009/analysis/137687000000061119/models/137687000000198140/deployments HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Deployment whose most recent run is still executing**

```json
{
    "status": "success",
    "summary": "Get deployments for a model",
    "data": {
        "deployments": {
            "deploymentId": "137687000000198176",
            "analysisId": "137687000000061115",
            "inputTable": "RealEstate_TestData",
            "inputTableId": "137687000000061003",
            "outputTable": "PricePredictionOutput",
            "outputTableId": "137687000000198129",
            "status": "In progress",
            "lastDeploymentTime": "28 Jan 2026 20:35:10",
            "outputColumns": [
                "City",
                "Bedrooms",
                "Bathrooms",
                "Garage"
            ],
            "predictionColumn": "PricePrediction",
            "stack": "8 GB",
            "importType": "truncateadd"
        }
    }
}
```

**HTTP 200 OK — Deployment configured with UPDATEADD**

```json
{
    "status": "success",
    "summary": "Get deployments for a model",
    "data": {
        "deployments": {
            "deploymentId": "137687000000198180",
            "analysisId": "137687000000061115",
            "inputTable": "RealEstate_TestData",
            "inputTableId": "137687000000061003",
            "outputTable": "PricePredictionOutput",
            "outputTableId": "137687000000198131",
            "status": "Completed",
            "lastDeploymentTime": "28 Jan 2026 21:05:44",
            "outputColumns": [
                "City",
                "Bedrooms"
            ],
            "predictionColumn": "PricePrediction",
            "stack": "16 GB",
            "importType": "updateadd"
        }
    }
}
```

**HTTP 400 Bad Request — The model does not belong to the analysis in the URL**

```json
{
    "status": "failure",
    "summary": "MODEL_NOT_BELONGS_TO_ANALYSIS",
    "data": {
        "errorCode": 21000010,
        "errorMessage": "The given model does not belong to this analysis."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Deployments For A Model](../../../sdk-examples/dsml/automl/get-deployments-for-model.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Plural key, singular value** | `data.deployments` is a JSONObject, not a JSONArray, because the one-deployment-per-model rule makes a list unnecessary. Do not iterate it. |
| **Two different `status` fields** | `deployments.status` is the outcome of the last scoring run; the top-level `status` is the HTTP call result. |
| **The run-status polling endpoint** | [Run AutoML Analysis](run-auto-ml-analysis.md) returns 204 immediately without a job handle. This API is the only way to observe whether that run finished. |
| **`outputTableId` is the handoff to the data APIs** | The predictions themselves are ordinary table rows — read them with the [Row / Export APIs](../../data-operations/row-operations/overview.md) using this ID. |
| **Case asymmetry on `importType`** | Lower case here, upper case on the request. |
| **Schedule is not echoed** | The `scheduleDetails` sent at creation cannot be read back through any API. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `modelId` → Get Deployments For A Model → `deploymentId` → [Run AutoML Analysis](run-auto-ml-analysis.md) / [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/get-deployments-for-model.md).
