# AutoML

* [AutoML](overview.md) - APIs for creating, running, deploying, and managing AutoML analyses and models.

# Concepts

* [AutoML What If Analysis](auto-ml-what-if-analysis.md) - Generates a single prediction for a hypothetical set of feature values — a live "what if I changed these inputs?" query against a trained model.
* [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) - Binds a trained model to an input table and an output table so that predictions can be generated — on a recurring schedule, on demand, or both.
* [Create AutoML Analysis](create-auto-ml-analysis.md) - Creates an analysis and immediately starts training one model per configured algorithm.
* [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) - Deletes a deployment.
* [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md) - Deletes one model from an analysis, along with the deployment attached to it.
* [Delete AutoML Analysis](delete-auto-ml-analysis.md) - Deletes an analysis and everything beneath it — all its models, and all deployments attached to those models.
* [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) - Returns the full definition of one analysis together with every model trained under it — including each model's ID, score, training status, and hyperparameters.
* [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md) - Returns every AutoML analysis across all workspaces in the organization, each tagged with the workspace it belongs to.
* [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) - Returns every AutoML analysis defined in one workspace.
* [Get Deployments For A Model](get-deployments-for-model.md) - Returns the deployment configured for a model — its input and output tables, schedule outcome, and last run status.
* [Run AutoML Analysis](run-auto-ml-analysis.md) - Triggers a deployment immediately — the "run now" action.
