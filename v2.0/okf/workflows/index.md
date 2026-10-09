# Workflows

# Concepts

* [Bootstrap: from access token to workspace and view IDs](bootstrap-identifiers.md) - The first three calls of every integration - list organizations, pick the org ID for the header, and resolve workspace and view names into the IDs that all other endpoints need.
* [Embed a view for many tenants with per-tenant row filters](embed-view-multi-tenant.md) - Mint one short-lived embed URL per end customer, each carrying its own criteria, permissions and column restrictions, then audit and revoke URLs.
* [Export a view, dashboard or SQL result asynchronously](export-data-asynchronously.md) - Create an export job, poll or receive a callback, and download the file - the path for dashboards, query tables, large tables and ad-hoc SQL that the synchronous export rejects.
* [Load data into a table (small, large and very large files)](import-large-dataset.md) - Choose between synchronous import, asynchronous import job and batch import, then create or fill a table and verify the result.
* [Add users to an organization and a workspace, and set their roles](manage-users-and-roles.md) - Invite users to the organization, place them in a workspace with a role, promote or demote admins, deactivate leavers, and understand who may perform each step.
* [Schedule a recurring email delivery of a report or dashboard](schedule-email-report.md) - Create an email schedule with recipients and calendar frequency, trigger it once to test, enable or disable it, and update it safely.
* [Share views with users or groups, with row and column restrictions](share-view-with-row-filter.md) - Grant a permission set on one or more views to users or a group, optionally limiting rows with criteria and columns with column lists, then inspect, update or revoke the share.
* [Train an AutoML model, deploy it and score a table](train-and-run-automl-model.md) - The end-to-end AutoML sequence - create an analysis on a training table, wait for models to train, deploy the best model, run predictions into an output table, and clean up.
