# Zoho Analytics REST API v2

**182 APIs** · **10 domains** · **35 sections** · generated from OpenAPI 3.1

Everything under this folder is **version 2** of the Zoho Analytics REST API — every public  
endpoint, grouped exactly the way the API reference is grouped, with a ready-to-send `CONFIG`  
example on each request.

Built from the two sources of truth:  
[<b>analytics-oas</b>](https://github.com/zoho/analytics-oas) (OpenAPI 3.1 specifications) and the  
[<b>analytics-okf</b>](https://github.com/zoho/analytics-okf) knowledge bundle (endpoint catalog, permissions and workflow playbooks).

> Authenticate first using the **🔐 Authentication** folder at the root of this collection.  
Every request below assumes a valid access token. 
  

---

## 🚀 Start here

| Step | Action | Gives you |
| --- | --- | --- |
| 1 | Import and select the **`Zoho Analytics REST Variables`** environment | Every variable these requests read |
| 2 | **🏢 Organization Management › Get Org List** | `orgId` → set `organization-id` |
| 3 | **🏢 Organization Management › Get Meta Details From Name** | `workspaceId`, `viewId` from plain names — **enable** those two variables first |
| 4 | Any endpoint in the domain you need | — |

Nothing else works until `organization-id` is set — it is the `ZANALYTICS-ORGID` header that  
almost every v2 endpoint requires. Identifier variables such as `workspace-id` and `view-id`  
ship **disabled**; tick the one you need in the environment editor before running a request.

---

## 🧭 What's inside

| Domain | APIs | Sections | Covers |
| --- | --- | --- | --- |
| **🏢 Organization Management** | 4 | 1 | Org list, resource usage, subscription, name → ID lookup |
| **👥 Users & Groups** | 26 | 4 | Org users, custom roles, workspace users and admins, groups |
| **🗂️ Workspace Management** | 24 | 4 | Workspace lifecycle, folders, preferences, white-label access |
| **🧱 Data Modeling & Schema** | 33 | 7 | Tables, columns, lookups, query tables, formulas, variables |
| **🔄 Data Operations** | 20 | 6 | Rows, sync/async/batch import, sync/async export, datasource sync |
| **📋 Views Management** | 27 | 5 | View lifecycle, favourites, tags, trash, auto analysis |
| **📊 Reports & Dashboards** | 9 | 2 | Analysis views and dashboards — create, read, update |
| **🔗 Share & Publish** | 22 | 4 | Sharing, public/private URLs, embed URLs, slideshows |
| **⏰ Schedules & Alerts** | 6 | 1 | Recurring email delivery of reports and dashboards |
| **🤖 Data Science & Machine Learning** | 11 | 1 | AutoML analyses, models, deployments, what-if |

Each domain folder documents its own sections, lists every API with method, path and OAuth  
scope, and names the multi-call **workflows** those APIs take part in.

---

## 🧩 Conventions shared by every v2 call

|  |  |
| --- | --- |
| **Base URL** | `https://{{analytics-domain}}/restapi/v2/...` — always HTTPS, always the API host of your data centre. |
| **`ZANALYTICS-ORGID`** | Required by almost every endpoint; each request's documentation says which. Missing it returns error `8083`. |
| **`CONFIG`** | A single JSON object carries every optional argument. `GET` → URL-encoded **query** parameter (a collection pre-request script encodes it for you). `POST` / `PUT` / `DELETE` → **form field**. Imports → **multipart** field. |
| **Identifiers** | Opaque numeric strings. Never construct one — read it from a listing API. See the variables table below. |
| **Success envelope** | `{ "status": "success", "summary": "...", "data": { ... } }`. Many write operations answer **`204 No Content`** with no body — that is success. |
| **Failure envelope** | `{ "status": "failure", "summary": "...", "data": { "errorCode": ..., "errorMessage": "..." } }`. HTTP status maps to the error code; see [Common error codes](https://www.zoho.com/analytics/api/v2/common-error-codes.html). |

---

## 🧪 Workflows

Most real integrations are a _sequence_ of v2 calls. Each playbook is documented on the domain  
folder that owns it:

| Playbook | Domain | Call sequence |
| --- | --- | --- |
| **Bootstrap: access token → workspace and view IDs** | 🏢 Organization Management | List organizations → Resolve the workspace → Resolve the view → Resolve deeper IDs |
| **Load data into a table (small, large, very large)** | 🔄 Data Operations | Build CONFIG → Send the request → Read the result → Verify |
| **Export a view, dashboard or SQL result asynchronously** | 🔄 Data Operations | Create the job → Wait for completion → Download |
| **Add users to an org and a workspace, set their roles** | 👥 Users & Groups | Add to the organization → Set the org role → Add to a workspace → Give access to views → Change role or status → Offboard |
| **Share views with row and column restrictions** | 🔗 Share & Publish | (Optional) Create a group → Share → Inspect → Change → Revoke |
| **Embed a view for many tenants with per-tenant filters** | 🔗 Share & Publish | Mint a URL per tenant → Re-mint before expiry → Audit → Revoke |
| **Schedule a recurring email delivery** | ⏰ Schedules & Alerts | Create → Test → List and inspect → Pause or resume → Update → Delete |
| **Train an AutoML model, deploy it and score a table** | 🤖 Data Science & ML | Create the analysis → Wait for training → (Optional) What-if → Deploy → Run → Read predictions → Clean up |

---

## 🔢 Variables these requests expect

Every request below is parameterised. Import the **`Zoho Analytics REST Variables`**  
environment that ships alongside this collection and select it in the environment dropdown —  
nothing here reads collection-level variables.

**Always on**

| Variable | Set it to |
| --- | --- |
| `analytics-domain` | The API host of your data centre, e.g. `analyticsapi.zoho.com`. See the collection overview for the full list. |
| `access-token` | Filled in automatically by **🔐 Authentication › Generate Tokens**. |
| `organization-id` | **Get Org List** → `orgId`. Sent as `ZANALYTICS-ORGID` by almost every request here. |

**Disabled by default — enable the one your request needs**

Identifier variables ship **unchecked** in the environment so the list stays readable and  
nothing silently resolves to a placeholder. Tick the box next to a variable, paste the ID, and  
run.

| Variable | Enable it for | Read the ID from |
| --- | --- | --- |
| `workspace-id` | Nearly every domain below | **Get Meta Details From Name** / **Get All Workspace List** |
| `view-id` | Rows, exports, sharing, publish, tags, reports | **Get Meta Details From Name** / **Get View List** |
| `column-id` | 🧱 Columns | **Get Table Metadata** |
| `folder-id` | 🗂️ Workspace Folders | **Get Folder List** |
| `querytable-id` | 🧱 Query Tables | **Get Query Tables** |
| `dashboard-id` | 📊 Dashboards | **Get All Dashboards** |
| `formula-id` | 🧱 Custom Formula Columns, Aggregate Formulas | **Get Custom Formulas** / **Get Aggregate Formula** |
| `variable-id` | 🧱 Workspace Variables | **Get Variables** |
| `group-id` | 👥 Workspace Groups | **Get Group List** |
| `role-id` | 👥 Custom Roles | **Get Custom Roles** |
| `tag-id` | 📋 Tags | **Get Tags List** |
| `slide-id` | 🔗 Slideshow Management | **Get Slide List** |
| `schedule-id` | ⏰ Email Schedules | **Get Email Schedules** |
| `datasource-id` | 🔄 Data Sync & Connectivity | **Get Datasources** |
| `job-id` | 🔄 Async import / export | Returned when the job is created |
| `analysis-id` | 🤖 AutoML | **Get AutoML Analysis In Workspace** |
| `model-id` | 🤖 AutoML | **Get AutoML Analysis Details** |
| `deployment-id` | 🤖 AutoML | **Get Deployments For A Model** |
| `dest-organization-id` | **Copy Workspace**, **Copy Views**, **Copy Custom Formulas** | **Get Org List** — the _destination_ org |

> **Cross-organization copies.** Those three copy requests carry a **disabled**  
`ZANALYTICS-DEST-ORGID` header. To copy into another organization you administer, enable both  
the header on the request and the `dest-organization-id` environment variable. Leave both off  
and the copy lands in the organization from `ZANALYTICS-ORGID`. 
  

---

## ⚙️ Working with asynchronous jobs

Large imports and exports run as **jobs** rather than returning a result inline:

1. Create the job — **Create Import Job…** / **Create Export Job…** — and keep the `jobId`.
    
2. Poll **Get Import Job Details** / **Get Export Job Details** until `jobCode` reports  
    completion, or pass a `callbackUrl` in `CONFIG` and be notified instead of polling.
    
3. For exports, finish with **Download Exported Data**.
    

Batch imports additionally key each chunk so the server can assemble them in order. See  
**🔄 Data Operations** for the full sequence.

---

## 📚 Further reading

- [API reference ↗](https://www.zoho.com/analytics/api/v2/introduction.html)
    
- [OpenAPI specifications ↗](https://github.com/zoho/analytics-oas)
    
- [Common error codes ↗](https://www.zoho.com/analytics/api/v2/common-error-codes.html)
    
- [API units, limits and pricing ↗](https://www.zoho.com/analytics/api/v2/api-limits-pricing.html)
    
- [Client SDKs ↗](https://www.zoho.com/analytics/api/v2/client-library.html) — Java, C#, Python, PHP, Go, Node.js, Ruby