# 🔄 Data Operations

API for Data Operations in Zoho Analytics — covering row operations, import/export workflows, and datasource sync/connectivity.

> **20 APIs** in **6 sections** · scopes `data.*`, `metadata.*`

### Sections

| Section | APIs | What it covers |
| :--- | ---: | :--- |
| **Row Operations** | 3 | APIs for adding, updating, and deleting rows in a view. |
| **Synchronous Data Import** | 2 | APIs for importing data directly into new or existing tables. |
| **Asynchronous & Batch Data Import** | 5 | APIs for creating and monitoring asynchronous import jobs and batch imports. |
| **Synchronous Data Export** | 1 | APIs for exporting view data directly. |
| **Asynchronous Data Export** | 4 | APIs for creating export jobs and downloading generated exports. |
| **Data Sync & Connectivity** | 5 | APIs for import history, datasource sync/refetch, datasource updates, and listing datasources. |

### Workflows

| Playbook | Call sequence |
| :--- | :--- |
| **Export a view, dashboard or SQL result asynchronously**<br/>Create an export job, poll or receive a callback, and download the file - the path for dashboards, query tables, large tables and ad-hoc SQL that the synchronous export rejects. | Create the job → Wait for completion → Download |
| **Load data into a table (small, large and very large files)**<br/>Choose between synchronous import, asynchronous import job and batch import, then create or fill a table and verify the result. | Build CONFIG → Send the request → Read the result → Verify |
| **Train an AutoML model, deploy it and score a table**<br/>The end-to-end AutoML sequence - create an analysis on a training table, wait for models to train, deploy the best model, run predictions into an output table, and clean up. | Create the analysis → Wait for training → (Optional) What-if → Deploy → Run → Read predictions → Clean up |