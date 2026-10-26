# Data Alerts

* [Data Alerts](overview.md) - APIs for creating, listing, updating, running and deleting data alerts on a view, changing their status and reading their event history.

# Concepts

* [Change Alert Status](change-alert-status.md) - Enables (resumes) or pauses one or more alerts without altering their configuration.
* [Create Alert](create-alert.md) - Creates an alert on the specified report and returns its id.
* [Delete Alerts](delete-alerts.md) - Deletes one or more alerts in a workspace.
* [Get Alert Configuration](get-alert-configuration.md) - Returns one alert's complete configuration in exactly the CONFIG shape that Create Alert and Update Alert accept, so the response can be edited and posted straight back.
* [Get Alert Events](get-alert-events.md) - Returns the audit trail of one alert's evaluations - when each ran, and whether it triggered, did not trigger, or failed.
* [Get Alerts In View](get-alerts-in-view.md) - Returns the alerts configured on one report.
* [Get Alerts In Workspace](get-alerts-in-workspace.md) - Returns every alert defined anywhere in the workspace, with its name, the view it watches, its enabled state, audit stamps, and the outcome of its last run.
* [Get View Metadata For Alert](get-view-metadata-for-alert.md) - Returns everything needed to construct a rule for a report: its alertable columns with their viewColumnIndex, the operator and rule-type catalogues each column permits, the chart thresholds on each column, and the view-level anomaly definitions.
* [Run Alert](run-alert.md) - Queues an off-schedule evaluation of one alert.
* [Update Alert](update-alert.md) - Replaces an existing alert's configuration.
