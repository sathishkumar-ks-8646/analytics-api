---
type: API Domain
title: Data Science & Machine Learning (AutoML)
description: "API for DSML (Data Science & Machine Learning) in Zoho Analytics — covering AutoML analysis creation, execution, deployments, and what-if analysis."
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - api-domain
api:
  domain: dsml
  groups:
    - group: automl
      title: AutoML
      doc: "/domains/dsml/automl/overview.md"
      endpoint_count: 11
  endpoint_count: 11
  openapi: "/references/openapi/dsml-grouped-api.json"
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

API for DSML (Data Science & Machine Learning) in Zoho Analytics — covering AutoML analysis creation, execution, deployments, and what-if analysis.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [AutoML](automl/overview.md) | 11 | APIs for creating, running, deploying, and managing AutoML analyses and models. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get AutoML Analysis In Org](automl/get-auto-ml-analysis-in-org.md) | GET | `/restapi/v2/automl/analysis` | `getAutoMLAnalysisInOrg` | `ZohoAnalytics.metadata.read` | 200 |
| [Get AutoML Analysis In Workspace](automl/get-auto-ml-analysis-in-workspace.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `getAutoMLAnalysisInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get AutoML Analysis Details](automl/get-auto-ml-analysis-details.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `getAutoMLAnalysisDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Deployments For A Model](automl/get-deployments-for-model.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `getDeploymentsForModel` | `ZohoAnalytics.metadata.read` | 200 |
| [Create AutoML Analysis](automl/create-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `createAutoMLAnalysis` | `ZohoAnalytics.modeling.create` | 200 |
| [Delete AutoML Analysis](automl/delete-auto-ml-analysis.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `deleteAutoMLAnalysis` | `ZohoAnalytics.modeling.delete` | 204 |
| [Delete AutoML Analysis Model](automl/delete-auto-ml-analysis-model.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}` | `deleteAutoMLAnalysisModel` | `ZohoAnalytics.modeling.delete` | 204 |
| [Create AutoML Analysis Deployment](automl/create-auto-ml-analysis-deployment.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `createAutoMLAnalysisDeployment` | `ZohoAnalytics.modeling.create` | 200 |
| [Run AutoML Analysis](automl/run-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute` | `runAutoMLAnalysis` | `ZohoAnalytics.modeling.create` | 204 |
| [Delete AutoML Analysis Model Deployment](automl/delete-auto-ml-analysis-model-deployment.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}` | `deleteAutoMLAnalysisModelDeployment` | `ZohoAnalytics.modeling.delete` | 204 |
| [AutoML What If Analysis](automl/auto-ml-what-if-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif` | `autoMLWhatIfAnalysis` | `ZohoAnalytics.modeling.create` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/dsml-grouped-api.json)
- [Foundations](../../foundations/index.md)
