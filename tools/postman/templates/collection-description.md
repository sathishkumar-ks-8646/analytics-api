# Zoho Analytics REST API v2

**185 API requests** · **10 domains** · **35 sections** · OpenAPI 3.1 accurate

The official Postman collection for the [Zoho Analytics](https://www.zoho.com/analytics/)  
REST API v2 — every public endpoint, grouped exactly the way the API reference is grouped, with  
a ready-to-send `CONFIG` example on each request.

Generated from the two sources of truth:  
[<b>analytics-oas</b>](https://github.com/zoho/analytics-oas) (OpenAPI 3.1 specifications) and the  
[<b>analytics-okf</b>](https://github.com/zoho/analytics-okf) knowledge bundle (endpoint catalog, permissions and workflow playbooks).

---

## 🚀 Quick start

| Step | Action |
| --- | --- |
| 1 | **Fork** this collection and import the **`Zoho Analytics REST Variables`** environment shipped with it. |
| 2 | Fill `client-id`, `client-secret`, `accounts-domain`, `analytics-domain` for your data centre. |
| 3 | Run **🔐 Authentication › Generate Tokens** — the token variables populate themselves. |
| 4 | Run **🏢 Organization Management › Get Org List** and copy `orgId` into `organization-id`. |
| 5 | Run **🏢 Organization Management › Get Meta Details From Name** to turn a workspace or view _name_ into the `workspace-id` / `view-id` every other request needs. |

> Steps 4–5 are the **Bootstrap** playbook. Nothing else works until `organization-id` is set. 
  

---

## 🧭 What's inside

| Domain | APIs | Sections |
| --- | --- | --- |
| **Organization Management** | 4 | 1 |
| **Users & Groups** | 26 | 4 |
| **Workspace Management** | 24 | 4 |
| **Data Modeling & Schema** | 33 | 7 |
| **Data Operations** | 20 | 6 |
| **Views Management** | 27 | 5 |
| **Reports & Dashboards** | 9 | 2 |
| **Share & Publish** | 22 | 4 |
| **Schedules & Alerts** | 6 | 1 |
| **Data Science & Machine Learning** | 11 | 1 |

Every folder carries its own documentation: the sub-sections it contains, a table of its APIs  
with method, path and OAuth scope, and the multi-call **workflows** those APIs take part in.

---

## 🧩 Five conventions that apply everywhere

|  |  |
| --- | --- |
| **Base URL** | `https://{{analytics-domain}}/restapi/v2/…` — always HTTPS, always region-specific. |
| **Authorization** | `Bearer {{access-token}}`, set once at collection level. Zoho's own docs write the same header as `Zoho-oauthtoken` followed by the token; both schemes are accepted. |
| **`ZANALYTICS-ORGID`** | Required by almost every endpoint — each request says so. Missing it returns error `8083`. |
| **`CONFIG`** | One JSON object carries every optional argument. `GET` → URL-encoded **query** parameter (a collection pre-request script encodes it for you). `POST`/`PUT`/`DELETE` → **form field**. Imports → **multipart** field. |
| **Response envelope** | `{ "status": "success", "summary": "…", "data": { … } }`. Write operations often answer **`204 No Content`** with no body — that is success. Failures return `{ "status": "failure", "summary": …, "data": { "errorCode": …, "errorMessage": … } }`. |

---

## 🧪 Workflows

Most real integrations are a _sequence_ of calls. These playbooks are documented on the folders  
that own them:

| Playbook | Call sequence |
| --- | --- |
| **Bootstrap: from access token to workspace and view IDs** | List organizations → Resolve the workspace → Resolve the view → Resolve deeper IDs as needed |
| **Embed a view for many tenants with per-tenant row filters** | Mint a URL per tenant → Re-mint before expiry → Audit → Revoke |
| **Export a view, dashboard or SQL result asynchronously** | Create the job → Wait for completion → Download |
| **Load data into a table (small, large and very large files)** | Build CONFIG → Send the request → Read the result → Verify |
| **Add users to an organization and a workspace, and set their roles** | Add to the organization → Set the organization role → Add to a workspace → Give access to views → Change workspace role or status → Offboard |
| **Schedule a recurring email delivery of a report or dashboard** | Create → Test → List and inspect → Pause or resume → Update → Delete |
| **Share views with users or groups, with row and column restrictions** | (Optional) Create a group → Share → Inspect → Change → Revoke |
| **Train an AutoML model, deploy it and score a table** | Create the analysis → Wait for training → (Optional) What-if → Deploy → Run → Read predictions → Clean up |

---

## 🌍 Data centres

Set both variables to the same region. Tokens are **not** portable across regions.

| Region | `analytics-domain` | `accounts-domain` |
| --- | --- | --- |
| United States | `analyticsapi.zoho.com` | `accounts.zoho.com` |
| Europe | `analyticsapi.zoho.eu` | `accounts.zoho.eu` |
| India | `analyticsapi.zoho.in` | `accounts.zoho.in` |
| Australia | `analyticsapi.zoho.com.au` | `accounts.zoho.com.au` |
| Japan | `analyticsapi.zoho.jp` | `accounts.zoho.jp` |
| China | `analyticsapi.zoho.com.cn` | `accounts.zoho.com.cn` |
| Canada | `analyticsapi.zohocloud.ca` | `accounts.zohocloud.ca` |
| Saudi Arabia | `analyticsapi.zoho.sa` | `accounts.zoho.sa` |

---

## 🔢 Variables

This collection ships **no collection-level variables** — they would shadow your own. Instead an  
environment is shipped alongside it:

> **`Zoho Analytics REST Variables`** — import it, select it in the environment dropdown, and  
fill in `analytics-domain`, `accounts-domain`, `client-id` and `client-secret`. 
  

Credentials and `organization-id` are **enabled** out of the box. The identifier variables  
(`workspace-id`, `view-id`, `column-id`, `job-id`, `dest-organization-id`, …) ship  
**disabled** — tick the one a request needs and paste the ID. **2️⃣ v2** lists every variable,  
what it is for, and the API that returns it.

---

## ⚙️ Working with async jobs

Large imports and exports run as **jobs**. Create the job, keep the `jobId`, then poll  
**Get Import Job Details** / **Get Export Job Details** until `jobCode` reports completion, and  
finally **Download Exported Data**. Supply a `callbackUrl` in `CONFIG` to be notified instead of  
polling. See the workflow notes in **🔄 Data Operations**.

---

## 📚 Further reading

- [API reference ↗](https://www.zoho.com/analytics/api/v2/introduction.html)
    
- [OpenAPI specifications ↗](https://github.com/zoho/analytics-oas)
    
- [Common error codes ↗](https://www.zoho.com/analytics/api/v2/common-error-codes.html)
    
- [API units, limits &amp; pricing ↗](https://www.zoho.com/analytics/api/v2/api-limits-pricing.html)
    
- [Client SDKs ↗](https://www.zoho.com/analytics/api/v2/client-library.html) — Java, C#, Python, PHP, Go, Node.js, Ruby