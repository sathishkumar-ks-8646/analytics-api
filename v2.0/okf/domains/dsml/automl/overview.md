---
type: API Group
title: AutoML
description: "APIs for creating, running, deploying, and managing AutoML analyses and models."
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - api-group
api:
  domain: dsml
  group: automl
  endpoint_count: 11
  endpoints:
    - operation_id: getAutoMLAnalysisInOrg
      method: GET
      path: "/restapi/v2/automl/analysis"
      doc: "/domains/dsml/automl/get-auto-ml-analysis-in-org.md"
    - operation_id: getAutoMLAnalysisInWorkspace
      method: GET
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
      doc: "/domains/dsml/automl/get-auto-ml-analysis-in-workspace.md"
    - operation_id: getAutoMLAnalysisDetails
      method: GET
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}"
      doc: "/domains/dsml/automl/get-auto-ml-analysis-details.md"
    - operation_id: getDeploymentsForModel
      method: GET
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
      doc: "/domains/dsml/automl/get-deployments-for-model.md"
    - operation_id: createAutoMLAnalysis
      method: POST
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
      doc: "/domains/dsml/automl/create-auto-ml-analysis.md"
    - operation_id: deleteAutoMLAnalysis
      method: DELETE
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}"
      doc: "/domains/dsml/automl/delete-auto-ml-analysis.md"
    - operation_id: deleteAutoMLAnalysisModel
      method: DELETE
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}"
      doc: "/domains/dsml/automl/delete-auto-ml-analysis-model.md"
    - operation_id: createAutoMLAnalysisDeployment
      method: POST
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
      doc: "/domains/dsml/automl/create-auto-ml-analysis-deployment.md"
    - operation_id: runAutoMLAnalysis
      method: POST
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute"
      doc: "/domains/dsml/automl/run-auto-ml-analysis.md"
    - operation_id: deleteAutoMLAnalysisModelDeployment
      method: DELETE
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}"
      doc: "/domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md"
    - operation_id: autoMLWhatIfAnalysis
      method: POST
      path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif"
      doc: "/domains/dsml/automl/auto-ml-what-if-analysis.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

This document covers the V2 **AutoML** REST APIs of Zoho Analytics — the APIs that train machine-learning models on a table, inspect the trained models, deploy a chosen model to score new data on a schedule, run predictions on demand, and explore hypothetical predictions.

APIs for creating, running, deploying, and managing AutoML analyses and models.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) | GET | `/restapi/v2/automl/analysis` | `getAutoMLAnalysisInOrg` | `ZohoAnalytics.metadata.read` | 200 |
| [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `getAutoMLAnalysisInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `getAutoMLAnalysisDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Deployments For A Model](get-deployments-for-model.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `getDeploymentsForModel` | `ZohoAnalytics.metadata.read` | 200 |
| [Create AutoML Analysis](create-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `createAutoMLAnalysis` | `ZohoAnalytics.modeling.create` | 200 |
| [Delete AutoML Analysis](delete-auto-ml-analysis.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `deleteAutoMLAnalysis` | `ZohoAnalytics.modeling.delete` | 204 |
| [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}` | `deleteAutoMLAnalysisModel` | `ZohoAnalytics.modeling.delete` | 204 |
| [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `createAutoMLAnalysisDeployment` | `ZohoAnalytics.modeling.create` | 200 |
| [Run AutoML Analysis](run-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute` | `runAutoMLAnalysis` | `ZohoAnalytics.modeling.create` | 204 |
| [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}` | `deleteAutoMLAnalysisModelDeployment` | `ZohoAnalytics.modeling.delete` | 204 |
| [AutoML What If Analysis](auto-ml-what-if-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif` | `autoMLWhatIfAnalysis` | `ZohoAnalytics.modeling.create` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is "AutoML" in Zoho Analytics?

AutoML lets you build predictive models directly on Zoho Analytics tables without writing code. The feature is organised as a strict four-level hierarchy, and almost every API in this document operates on one level of it:

```
Workspace
└── Analysis            ← created from ONE training table + a target column + a feature list
    └── Model           ← one model per algorithm you configured; created automatically by training
        └── Deployment  ← scores an input table into an output table, on a schedule or on demand
```

| Level | Created by | Deleted by | Notes |
|-------|-----------|-----------|-------|
| **Analysis** | [Create AutoML Analysis](create-auto-ml-analysis.md) | [Delete AutoML Analysis](delete-auto-ml-analysis.md) | The training job. One analysis = one training table + one target column + one feature set + one or more algorithms. |
| **Model** | **Not created directly.** One model is generated per algorithm listed in the `algorithms` object when the analysis is created. | [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md) | Each model trains independently and carries its own score, training status, and hyperparameters. |
| **Deployment** | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) | [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) | Binds one model to an input table and an output table. **A model can have at most one deployment.** |

> **There is no "train model" API and no "update analysis" API.** Training starts automatically when the analysis is created, and none of the four levels can be edited afterwards — an analysis, a model, and a deployment are all create-and-delete objects. To change a feature list, a target column, or an algorithm's hyperparameters, delete the analysis and create a new one.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The four read APIs use the **`metadata`** scope family; the seven write APIs use the **`modeling`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All eleven APIs require the `ZANALYTICS-ORGID` header. Ten are workspace-scoped under `/restapi/v2/automl/workspaces/<workspace-id>/...`; only [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) is organization-scoped.
> - **All eleven APIs are disabled in Client Portal / White Label request contexts.** A request that arrives through a custom domain is rejected with [`7301`](../../../foundations/error-codes.md#error-7301) before any business logic runs — see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour).
> - **AutoML must be enabled for the organization**, and the organization must be within its AutoML plan limit. Otherwise every call fails with `21000014` — see [Feature Enablement and Plan Limits](overview.md#feature-enablement-and-plan-limits).
> - Permissions are **owner-only**: there is no permission-based alternative for a non-owner. See [Permission Model](overview.md#permission-model).
> - None of these APIs accepts a `criteria` attribute. Rows are selected by choosing the training table and input table, not by a filter expression.

---

# How the APIs Depend on Each Other

Every AutoML API needs IDs produced by an earlier one. This is the end-to-end order, and there is no way to skip a step.

## The full lifecycle

```
 [Get View List]                     → trainingTableId  (a table in the workspace)
        │
        ▼
 5. Create AutoML Analysis           → analysisId
        │   (training starts immediately; one model per algorithm)
        ▼
 3. Get AutoML Analysis Details      → models[].id  (= modelId), models[].trainingStatus
        │   ── poll until trainingStatus is "Completed" ──
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
 8. Create Deployment (needs modelId) → deploymentId   11. What If Analysis (needs modelId)
        │                                                  → one-off prediction, nothing stored
        ▼
 4. Get Deployments For A Model      → deployment status, outputTableId
        │
        ▼
 9. Run AutoML Analysis (needs deploymentId) → scores the input table into the output table
```

## Which ID comes from where

| ID | Produced by | Consumed by |
|----|-------------|-------------|
| `workspaceId` | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) | All ten workspace-scoped APIs |
| `trainingTableId`, `inputTableId` | [Get View List](../../views-management/view-operations/get-views.md) | [Create AutoML Analysis](create-auto-ml-analysis.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) |
| `analysisId` | [Create AutoML Analysis](create-auto-ml-analysis.md) response, or [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) / [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) | Every API with `<analysis-id>` in its path |
| `modelId` | **[Get AutoML Analysis Details](get-auto-ml-analysis-details.md) only** (`models[].id`) | Every API with `<model-id>` in its path |
| `deploymentId` | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) response, or [Get Deployments For A Model](get-deployments-for-model.md) | Every API with `<deployment-id>` in its path |
| `outputTableId` | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) response | Read the predictions with the [Row / Export APIs](../../data-operations/row-operations/overview.md) |

> **`modelId` has exactly one source.** Models are never returned by the two list APIs — [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) is the only API that exposes `models[].id`. Any workflow that deploys a model, deletes a model, or runs a What-If must call Get AutoML Analysis Details first.

## Ordering rules enforced by the server

| Rule | Enforced by | Error |
|------|-------------|-------|
| A model cannot be deployed while it is still training | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) | `21000052` |
| A model that failed training cannot be deployed | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) | `21000053` |
| A model can hold **only one** deployment at a time | [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) | `21000051` |
| What-If cannot run while the model is still training | [AutoML What If Analysis](auto-ml-what-if-analysis.md) | `21000043` |
| What-If is not supported by every algorithm | [AutoML What If Analysis](auto-ml-what-if-analysis.md) | `21000054` |
| The analysis must belong to the workspace in the URL | Every API with `<analysis-id>` in its path | `21000009` |
| The model must belong to the analysis in the URL | Every API with `<model-id>` in its path | `21000010` |
| The deployment must belong to the analysis in the URL | Every API with `<deployment-id>` in its path | `21000012` |

## Cascade on delete

| Deleting… | Also removes |
|---|---|
| An **analysis** ([Delete AutoML Analysis](delete-auto-ml-analysis.md)) | **Every model under it, and every deployment under those models.** A single call tears down the whole subtree. |
| A **model** ([Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md)) | The deployment attached to that model, if any. The analysis and its other models survive. |
| A **deployment** ([Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md)) | Only the deployment. The model becomes deployable again (`isDeployed` returns to `false`). |

> Deleting an analysis or a deployment does **not** delete the output table that a deployment created. Prediction data already written to the output table remains in the workspace and must be removed separately with [Delete View](../../views-management/view-operations/delete-view.md).

---

# Permission Model

AutoML permissions are stricter than most of the API suite: the check is **workspace ownership**, with no permission-based or custom-role alternative.

| API | Who may call it |
|-----|-----------------|
| [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) | **Account Admin or Organization Admin only.** A Workspace Admin receives `7301` even for their own workspaces. |
| The other ten APIs | The authenticated user must be an Account Admin or Organization Admin, or the **Workspace Admin (owner) of the workspace named in the URL**. |

Every other role is rejected with [`7301`](../../../foundations/error-codes.md#error-7301) — shared users, group members, and ordinary org users have no AutoML access at all, and a Workspace Admin of workspace A cannot touch an analysis in workspace B.

---

# Feature Enablement and Plan Limits

Before any business logic runs, the write APIs check two things:

| Condition | Error | Message |
|-----------|-------|---------|
| AutoML is not switched on for the organization | `21000014` `AUTOML_NOT_ENABLED` | *"The AutoML Feature is not enabled. Please enable the features from Org Settings > Feature Controls > DSML."* |
| The organization has used up its AutoML allowance | `21000014` `AUTOML_PRICING_EXCEED` | *"AutoML allowed limit exceeded for your plan. Kindly increase the limit to continue to use AutoML."* |

> Both conditions share the numeric code `21000014` and are told apart only by the `summary` field. Match on `summary`, not on `errorCode`, when you need to distinguish "turn the feature on" from "buy more capacity".

---

# White Label / Client Portal Behaviour

All eleven APIs are blocked in Client Portal / White Label request contexts — the same posture as the [Embed URL](../../share-and-publish/embed-url/overview.md#white-label--client-portal-behaviour) and [Email Schedule](../../schedules-and-alerts/email-schedules/overview.md#white-label--client-portal-behaviour) families.

| Scenario | Result |
|----------|--------|
| The API request arrives **through** a Client Portal / White Label custom domain | **Rejected with `7301`** before any business logic runs. AutoML cannot be managed from a portal-domain context. |
| The API request is sent to the **standard API host** for a workspace that happens to be white-labelled | **Allowed**, and behaves exactly as for any other workspace. |

There is no `domainName` attribute on any AutoML API. Manage AutoML for a white-labelled workspace by calling the standard `analyticsapi.zoho.*` host.

---

# API-Specific Notes and Behaviours

## Get AutoML Analysis In Org

- **The only organization-wide AutoML API, and the only one that names the workspace.** `workspaceId` and `workspaceName` appear nowhere else, which makes this the entry point when you do not already know which workspace holds an analysis.
- **A stricter role gate than everything else in the family.** Account Admin or Organization Admin only — a Workspace Admin who can fully manage AutoML inside their own workspace still receives [`7301`](../../../foundations/error-codes.md#error-7301) here. Do not treat a [`7301`](../../../foundations/error-codes.md#error-7301) from this API as evidence that the user has no AutoML access at all; retry with [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) against a specific workspace.
- **Inventory only.** No models, no deployments, no feature lists. Every deeper field requires [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), one analysis at a time.
- **`isDraft` distinguishes UI-created stubs.** Analyses created through the API always begin training immediately and are never drafts; a `true` here means somebody saved an analysis in the Zoho Analytics UI without training it.
- **Dependency chain:** Get AutoML Analysis In Org → `workspaceId` + `id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md).

## Get AutoML Analysis In Workspace

- **The workspace-scoped twin of [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md)**, returning an identical per-analysis object minus `workspaceId` and `workspaceName`. Prefer it whenever the workspace is already known — it is available to Workspace Admins, who cannot call the org-level API at all.
- **Still not a source of `modelId`.** This is the most common misstep in the family: neither list API exposes models, so a deploy or What-If workflow must always pass through [Get AutoML Analysis Details](get-auto-ml-analysis-details.md).
- **Unfiltered and unpaged**, like every listing API here. Filter client-side.
- **Case asymmetry on `predictionType`.** Title case on read, upper case on write — never round-trip the value without normalising.
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Get AutoML Analysis In Workspace → `id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md).

## Get AutoML Analysis Details

- **The hub of the whole family.** It is the sole source of `modelId`, the sole way to see per-model scores and hyperparameters, and the polling endpoint that tells you when training has finished. Four of the eleven APIs are unreachable without calling it first.
- **Poll `models[].trainingStatus`, not `analysis.status`.** Models train independently, so one model can be `"Completed"` and ready to deploy while a sibling is still `"In Progress"` or has `"Failed"`. Deploying or running What-If against a model that is not `"Completed"` fails with `21000052` or `21000043`.
- **Two `status` fields with different meanings.** `data.analysis.status` is the training state; the top-level `status` is the HTTP outcome. Reading the wrong one produces confidently wrong logic.
- **`isDeployed` is the cheap pre-check for deployment.** Consult it rather than discovering `21000051` the hard way.
- **Everything numeric returns as a string.** `score` and every hyperparameter value are strings, even though `algorithms` accepts them as numbers on the request side — a create/read round-trip needs explicit conversion.
- **Dependency chain:** [Create AutoML Analysis](create-auto-ml-analysis.md) → `analysisId` → Get AutoML Analysis Details → `models[].id` → [Get Deployments For A Model](get-deployments-for-model.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).

## Get Deployments For A Model

- **A JSONObject behind a plural key.** `data.deployments` is a single object because a model may hold only one deployment. Code that iterates it will break.
- **The only way to observe a run.** [Run AutoML Analysis](run-auto-ml-analysis.md) returns 204 with no job handle, so `deployments.status` here is the sole progress signal for a scoring job.
- **`outputTableId` is the bridge to the data APIs.** Predictions are ordinary table rows; this ID is what you feed to the [Row / Export APIs](../../data-operations/row-operations/overview.md) to actually consume them.
- **The schedule is write-only.** `scheduleDetails` and `matchingColumns` are never echoed by any API, so an integration that wants to reproduce or clone a deployment must retain its own copy of what it sent.
- **Case asymmetry on `importType`.** Lower case on read, upper case on write.
- **Dependency chain:** [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `modelId` → Get Deployments For A Model → `deploymentId` → [Run AutoML Analysis](run-auto-ml-analysis.md) / [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md).

## Create AutoML Analysis

- **One request fans out into many models.** Each key in `algorithms` produces its own independently trained, scored, and deployable model. This is the intended way to compare algorithms — send several keys and then pick the best `score` from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md).
- **Immutable once created.** There is no update API at any level of the hierarchy. Changing the training table, target column, feature list, algorithms, or server option means delete-and-recreate, which invalidates every downstream ID.
- **The published limits are looser than the enforced ones.** `name` is capped at 50 characters (not the documented 60), and `features` must contain 3–20 entries (not the documented 1–100). Both mismatches fail late, at `21000020` / `21000026` / `21000027`.
- **`maxEntropy` is a special case in two directions.** It must be the only algorithm in the request, and it inverts the feature rule by requiring exactly one feature where every other algorithm requires at least three.
- **`targetColumn` must not appear in `features`.** The server rejects it (`21000048`) precisely because it would leak the answer into the model.
- **Clustering takes no target column at all** — it is unsupervised, and the attribute is simply not read.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → `trainingTableId` → Create AutoML Analysis → `data.id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) to poll training.

## Delete AutoML Analysis

- **204 No Content, no body.** Verified against the implementation.
- **The widest blast radius in the family.** One call removes the analysis, every model under it, and every deployment under those models — including their schedules. There is no partial mode and no confirmation step.
- **Output tables and their data survive.** The prediction tables that deployments created remain in the workspace, orphaned. Clean them up separately with [Delete View](../../views-management/view-operations/delete-view.md) if they are no longer wanted.
- **No trash, no restore.** Recreating the analysis produces entirely new IDs at all three levels and retrains from scratch.
- **Frees AutoML capacity**, so a create previously blocked by `21000014` `AUTOML_PRICING_EXCEED` may succeed afterwards.
- **Dependency chain:** [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) → `analysisId` → Delete AutoML Analysis.

## Delete AutoML Analysis Model

- **204 No Content, no body.** Verified against the implementation.
- **The pruning tool for a multi-algorithm analysis.** After comparing scores in [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), delete the models you do not want and keep the winner. The analysis and the surviving models are untouched.
- **It takes the model's deployment with it**, so a deployed model can be removed in one call rather than two.
- **Deleting every model leaves an empty analysis.** The analysis is not auto-removed; use [Delete AutoML Analysis](delete-auto-ml-analysis.md) for that.
- **Models cannot be regenerated.** There is no add-model or retrain API, so a deleted algorithm can only be recovered by creating a new analysis that includes it.
- **Dependency chain:** [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `models[].id` → Delete AutoML Analysis Model.

## Create AutoML Analysis Deployment

- **The gate with the most preconditions in the family.** The model must exist, belong to the analysis, have finished training (`21000052`), not have failed (`21000053`), and not already be deployed (`21000051`) — and the input table must carry every feature the model was trained on (`21000001`). Check `trainingStatus` and `isDeployed` from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) before calling.
- **One deployment per model, and deployments are immutable.** Reconfiguring means [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) followed by a fresh create — there is no update API.
- **It creates the output table as a side effect.** A brand-new table appears in the workspace if `outputTable` does not already exist, and its ID is returned as `outputTableId`. Against an existing table, `importType` decides whether rows are replaced (`TRUNCATEADD`), accumulated (`APPEND`), or merged (`UPDATEADD`).
- **`matchingColumns` must be a subset of `outputColumns`.** A merge key that is not written to the destination fails with `21000042`.
- **Creating is not running.** With `calendarFrequency: "none"` nothing happens until [Run AutoML Analysis](run-auto-ml-analysis.md) is called.
- **Weekly and monthly schedules do not currently work.** The server reads a `day` attribute that the published request template does not declare, while the declared `weekDay` / `monthDay` / `hourInterval` keys are never read. Use `none`, `daily`, or `hourly` and see the caveat under [`scheduleDetails` Fields](create-auto-ml-analysis-deployment.md#scheduledetails-fields).
- **Dependency chain:** [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `modelId` + [Get View List](../../views-management/view-operations/get-views.md) → `inputTableId` → Create Deployment → `deploymentId` + `outputTableId`.

## Run AutoML Analysis

- **204 No Content, no body.** Verified against the implementation.
- **The path drops the model ID.** It is `/analysis/<analysis-id>/deployments/<deployment-id>/execute`, not `/models/<model-id>/deployments/...`. Building the URL by analogy with [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) produces a 404-class failure.
- **It writes real data with no dry-run.** A `TRUNCATEADD` deployment deletes the output table's existing rows on every run. There is no preview mode and no undo.
- **Asynchronous with no handle.** The 204 means the job started; `deployments.status` from [Get Deployments For A Model](get-deployments-for-model.md) is the only way to learn whether it finished or failed.
- **Independent of the schedule.** It works on unscheduled deployments, forces an extra run on scheduled ones, and never shifts the next scheduled occurrence.
- **Dependency chain:** [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) → `deploymentId` → Run AutoML Analysis → poll [Get Deployments For A Model](get-deployments-for-model.md) → read predictions from `outputTableId`.

## Delete AutoML Analysis Model Deployment

- **204 No Content, no body.** Verified against the implementation.
- **It is the first half of "edit a deployment".** Because deployments are immutable, every change of input table, output table, schedule, or `importType` is expressed as delete-then-create. Expect to call it routinely, not exceptionally.
- **It releases the model.** `isDeployed` flips back to `false` and [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) succeeds again — this is the only way to clear `21000051`.
- **Data already written stays.** The output table and its prediction rows survive, so a replacement deployment pointed at the same table will interact with the old rows according to its own `importType`.
- **Addressed under the analysis, not the model** — same path shape as [Run AutoML Analysis](run-auto-ml-analysis.md).
- **Dependency chain:** [Get Deployments For A Model](get-deployments-for-model.md) → `deploymentId` → Delete Deployment → (optionally) [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md).

## AutoML What If Analysis

- **A read disguised as a POST.** It persists nothing, needs no deployment, and leaves the model unchanged — the POST verb exists only to carry the feature values. It is the fastest way to sanity-check a model before committing to a deployment.
- **All-or-nothing input.** Every feature used in training must be present; a partial `features` object fails with `21000050` rather than substituting defaults. Extra keys beyond the training set are ignored, so a superset is safe.
- **The feature list must be fetched, not guessed.** `analysis.features` from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) is the authoritative key set.
- **Not universally supported.** Some algorithms have no What-If capability and fail with `21000054`; the model must also have finished training (`21000043`).
- **Strings in, string out.** Numeric features are sent as JSON strings and `predictions` returns as a string, so both directions need conversion. A value that cannot be coerced to its column's type surfaces as `21000006` rather than a specific type error.
- **Requires a write scope for a read operation.** `modeling.create` is needed even though nothing is created — worth knowing when scoping a read-only integration token.
- **Dependency chain:** [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `models[].id` + `analysis.features` → What If Analysis.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Four of eleven APIs return 204 with no body** | [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Run AutoML Analysis](run-auto-ml-analysis.md), and [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) return HTTP **204 No Content** — treat the 2xx status code as the success indicator and never expect or parse a JSON body. The other seven return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `ANALYSIS_NOT_BELONGS_TO_DB`, `MODEL_ALREADY_DEPLOYED`), not a localised sentence. |
| **AutoML errors occupy the 21000xxx range** | Domain-specific failures use eight-digit codes starting `21000`, clearly separated from the 7xxx/8xxx codes shared with the rest of the API suite. Two distinct conditions share `21000014` and are told apart only by `summary` — see [Feature Enablement and Plan Limits](overview.md#feature-enablement-and-plan-limits). |
| **All IDs are strings** | `id`, `trainingTableId`, `models[].id`, `deploymentId`, `outputTableId`, `inputTableId`, and `analysisId` are JSON **strings** in every response, even though the request side accepts `trainingTableId` and `inputTableId` as native numbers. Parse them as strings or longs to avoid precision loss. |
| **Numbers are returned as strings too** | `models[].score` and every hyperparameter value inside `models[].algorithm` come back as strings, despite being sent as numbers. Convert explicitly when round-tripping. |
| **Beware the three nested `status` fields** | The top-level `status` is the HTTP outcome; `data.analysis.status` is the training state of an analysis; `data.deployments.status` is the outcome of the last scoring run. They are unrelated and use different vocabularies. |
| **Case asymmetry between request and response** | `predictionType` is sent upper case (`REGRESSION`) and returned title case (`"Regression"`); `importType` is sent upper case (`TRUNCATEADD`) and returned lower case (`"truncateadd"`). Normalise before comparing. |
| **Plural keys holding single objects** | `data.deployments` is a JSONObject in both [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) and [Get Deployments For A Model](get-deployments-for-model.md), because a model may hold at most one deployment. Only `data.analysis` in the two list APIs is genuinely an array — and in [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) the same key is an object. |
| **Empty array, never a missing key** | `data.analysis` is always present in both list APIs, empty (`[]`) when there is nothing to report. |
| **Create responses return IDs only** | [Create AutoML Analysis](create-auto-ml-analysis.md) returns just `data.id`, and [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) just `deploymentId` and `outputTableId`. Neither echoes the configuration that was sent — confirm it with the corresponding read API. |
| **Write-only configuration** | `algorithms` hyperparameters are readable back through `models[].algorithm`, but a deployment's `scheduleDetails`, `matchingColumns`, and `timezone` are never returned by any API. Retain your own copy if you need to clone or reproduce a deployment. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | Invalid value provided. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | A mandatory attribute was sent with an empty value. The error message names the attribute. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A mandatory attribute is missing from the configuration. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | CONFIG was not sent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | A schedule value is outside its declared range. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | viewIds is empty or has more than 1000 entries. |

# Related

- [Data Science & Machine Learning (AutoML)](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
