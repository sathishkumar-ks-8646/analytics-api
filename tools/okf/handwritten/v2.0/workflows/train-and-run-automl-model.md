---
type: Playbook
title: Train an AutoML model, deploy it and score a table
description: The end-to-end AutoML sequence - create an analysis on a training table, wait for models to train, deploy the best model, run predictions into an output table, and clean up.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - automl
  - machine-learning
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Produce predictions for a table using AutoML, from training to a populated output table.

# Prerequisites

- AutoML enabled for the organization and plan; all eleven endpoints are blocked from Client Portal hosts (`7301`).
- Caller is Account Admin, Organization Admin, or the Workspace Admin (owner) of the workspace. Get AutoML Analysis In Org is Account/Organization Admin only.
- `workspaceId` and the `trainingTableId` (a table's `viewId` from [Get View List](/domains/views-management/view-operations/get-views.md)).

# Steps

1. **Create the analysis** with [Create AutoML Analysis](/domains/dsml/automl/create-auto-ml-analysis.md) naming the training table and target column. Training starts immediately; one model per algorithm. Keep `analysisId` (`21000003` if the name already exists).
2. **Wait for training** by polling [Get AutoML Analysis Details](/domains/dsml/automl/get-auto-ml-analysis-details.md) until every `models[].trainingStatus` you care about is `Completed`. This is the **only** endpoint that returns `models[].id`; keep the `modelId` of the best model.
3. **(Optional) What-if** with [AutoML What If Analysis](/domains/dsml/automl/auto-ml-what-if-analysis.md) to get a one-off prediction from the model without storing anything (`21000043` while training).
4. **Deploy** with [Create AutoML Analysis Deployment](/domains/dsml/automl/create-auto-ml-analysis-deployment.md) giving the `modelId` and an `inputTableId`. Keep `deploymentId` and `outputTableId`. One deployment per model (`21000051`); a model still training (`21000052`) or failed (`21000053`) cannot be deployed.
5. **Run** with [Run AutoML Analysis](/domains/dsml/automl/run-auto-ml-analysis.md) using the `deploymentId`; predictions are written to the output table. Check status with [Get Deployments For A Model](/domains/dsml/automl/get-deployments-for-model.md).
6. **Read predictions** from the output table with the [export](/workflows/export-data-asynchronously.md) or [row](/domains/data-operations/row-operations/overview.md) APIs.
7. **Clean up.** [Delete AutoML Analysis Model Deployment](/domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) removes only the deployment; [Delete AutoML Analysis Model](/domains/dsml/automl/delete-auto-ml-analysis-model.md) removes the model and its deployment; [Delete AutoML Analysis](/domains/dsml/automl/delete-auto-ml-analysis.md) removes the whole subtree. The output table is never deleted automatically; remove it with [Delete View](/domains/views-management/view-operations/delete-view.md).

# Related

- [AutoML](/domains/dsml/automl/overview.md) - permission model, plan limits, dependency rules.
