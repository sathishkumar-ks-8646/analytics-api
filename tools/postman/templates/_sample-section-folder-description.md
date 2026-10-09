## Synchronous Data Import

This section covers the two **synchronous** data-import REST APIs of Zoho Analytics — the APIs that upload a CSV/JSON/XML/Excel payload and load it into a workspace, either by creating a new table or by writing into an existing one, and return the import result in the same HTTP response.

### APIs in this section

| # | API | Method | Path | Scope |
| ---: | :--- | :--- | :--- | :--- |
| 1 | **Import Data into a New Table (Synchronous)** | `POST` | `/restapi/v2/workspaces/{workspace-id}/data` | `data.create` |
| 2 | **Import Data into an Existing Table (Synchronous)** | `POST` | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `data.create` |

### Workflows that use these APIs

- **Load data into a table (small, large and very large files)** — Choose between synchronous import, asynchronous import job and batch import, then create or fill a table and verify the result.  
  `Build CONFIG → Send the request → Read the result → Verify`