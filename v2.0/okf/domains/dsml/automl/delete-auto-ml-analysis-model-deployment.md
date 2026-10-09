---
type: API Endpoint
title: Delete AutoML Analysis Model Deployment
description: Deletes an AutoML analysis deployment.
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - delete
  - modeling
api:
  operation_id: deleteAutoMLAnalysisModelDeployment
  method: DELETE
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}"
  domain: dsml
  group: automl
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1deployments~1{deployment-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/dsml/automl/delete-auto-ml-analysis-model-deployment.md"
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

**DELETE `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}`** - Delete AutoML Analysis Model Deployment (AutoML / Data Science & Machine Learning (AutoML)).

Deletes a deployment. The model becomes deployable again; the analysis, the model, and the output table are unaffected.

> This API has no CONFIG parameter. As with [Run AutoML Analysis](run-auto-ml-analysis.md), the path addresses the deployment under the **analysis**, not under the model.

From the OpenAPI specification:

Deletes an AutoML analysis deployment. The deployment stops running on its schedule, and the output table it was writing to is retained. The deployment ID can be obtained using the Get Deployments For A Model API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteAutoMLAnalysisModelDeployment` |
| HTTP method | DELETE |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1deployments~1{deployment-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{analysis-id}` | string | ID of the AutoML analysis. | [How to obtain](../../../foundations/identifiers.md#analysis-id) |
| `{deployment-id}` | string | ID of the AutoML analysis deployment. | [How to obtain](../../../foundations/identifiers.md#deployment-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Remove a deployment so the model can be redeployed with a different configuration**

```http
DELETE /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/deployments/137687000000198176 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
DELETE /restapi/v2/automl/workspaces/137687000271334009/analysis/137687000000061119/deployments/137687000000198190 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — The deployment does not belong to the analysis in the URL**

```json
{
    "status": "failure",
    "summary": "DEPLOYMENT_NOT_BELONGS_TO_ANALYSIS",
    "data": {
        "errorCode": 21000012,
        "errorMessage": "The given deployment does not belong to this analysis."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete AutoML Analysis Model Deployment](../../../sdk-examples/dsml/automl/delete-auto-ml-analysis-model-deployment.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Deployment returns a bare HTTP `204 No Content`. |
| **The de-facto "edit deployment" step** | Deployments are immutable, so changing the input table, output table, schedule, or `importType` means deleting the deployment and creating a new one. This API is the first half of that operation. |
| **Frees the model for redeployment** | After deletion `isDeployed` returns to `false` in [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), and [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) will succeed again. |
| **The output table and its rows survive** | Predictions already written remain. A new deployment writing to the same `outputTable` will append to, replace, or merge with them depending on its `importType`. |
| **Cancels future scheduled runs** | Any recurring schedule attached to the deployment stops; a run already in progress is not rolled back. |
| **Not idempotent** | A repeat delete fails with `21000012`. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Deployments For A Model](get-deployments-for-model.md) → `deploymentId` → Delete Deployment → (optionally) [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) with the new configuration. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/delete-auto-ml-analysis-model-deployment.md).
