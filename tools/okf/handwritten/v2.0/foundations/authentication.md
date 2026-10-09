---
type: Authentication
title: Authentication (OAuth 2.0)
description: How to authenticate Zoho Analytics REST API v2 calls with OAuth 2.0 access tokens, the Authorization header format, token lifetime and refresh, and the errors returned when authentication fails.
resource: https://accounts.zoho.com/oauth/v2/token
tags:
  - zoho-analytics
  - rest-api-v2
  - authentication
  - oauth
  - security
sources:
  - id: openapi-common
    resource: /references/openapi/zoho-analytics-api-common.json
    title: Shared OpenAPI components (securitySchemes.iam-oauth2-schema)
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
  - id: zoho-oauth-docs
    resource: https://www.zoho.com/analytics/api/v2/authentication/generating-token.html
    title: Zoho Analytics API v2 - Generating tokens (public documentation)
    author: team:zoho-analytics-public-docs
generated:
  at: {{NOW}}
status: stable
---

# Summary

Every Zoho Analytics REST API v2 request must carry an OAuth 2.0 **access token** in the `Authorization` header:

```http
Authorization: Zoho-oauthtoken 1000.8cb99dxxxxxxxxxxxxx9be93.9b8xxxxxxxxxxxxxxxf
```

The scheme name is the literal string `Zoho-oauthtoken` (not `Bearer`). The token must have been issued with every OAuth scope that the endpoint declares (see each endpoint's `api.oauth_scopes` and [OAuth scopes](/foundations/oauth-scopes.md)). A missing, expired, revoked or under-scoped token fails with HTTP 401 and error code [`8535`](/foundations/error-codes.md#error-8535) (`INVALID_OAUTHTOKEN`).

# OAuth Endpoints

The OpenAPI security scheme (`iam-oauth2-schema`) declares the authorization-code flow with these URLs for the US data center. Other data centers use the matching `accounts` host listed in [Data centers](/foundations/data-centers.md).

| Purpose | URL |
|---|---|
| Authorization (user consent) | `https://accounts.zoho.com/oauth/v2/auth` |
| Token exchange | `https://accounts.zoho.com/oauth/v2/token` |
| Token refresh | `https://accounts.zoho.com/oauth/v2/token` |

# Flow

1. **Register a client** in the Zoho API Console (`https://api-console.zoho.com`, or the console of your data center). Choose a *Server-based application* for web apps with a redirect URI, or a *Self Client* for server-to-server integrations that act as one user. Note the `client_id` and `client_secret`.
2. **Request an authorization code** by sending the user to the authorization URL with `scope` (comma-separated scopes, for example `ZohoAnalytics.data.read,ZohoAnalytics.metadata.read`), `client_id`, `response_type=code`, `redirect_uri` and `access_type=offline` (to receive a refresh token). A Self Client generates the code directly in the console.
3. **Exchange the code** with a POST to the token URL (`grant_type=authorization_code`, `code`, `client_id`, `client_secret`, `redirect_uri`). The response contains `access_token`, `refresh_token`, `expires_in`, `token_type` and `api_domain`. Pass `scope` as comma-separated values; `redirect_uri` is not needed for a Self Client.
4. **Call the API** with `Authorization: Zoho-oauthtoken <access_token>`.
5. **Refresh** when the access token expires by POSTing to the token URL with `grant_type=refresh_token`, `refresh_token`, `client_id`, `client_secret`. The refresh token is long-lived and does not change on refresh.

Access tokens are valid for **one hour** (`expires_in: 3600`); read `expires_in` rather than assuming. Refresh tokens stay valid until revoked, and a user may hold at most **20 refresh tokens** per client; creating a 21st silently deletes the oldest. The official SDKs (see [SDK clients](/foundations/sdk-clients.md)) take `client_id`, `client_secret` and `refresh_token`, and manage access tokens automatically.

# Scope Selection

- Each endpoint document lists its scopes under `api.oauth_scopes`; request the union of scopes across every endpoint your integration calls.
- `ZohoAnalytics.<family>.all` covers read, create, update and delete of one family; `ZohoAnalytics.fullaccess.all` covers everything. Prefer the narrowest set that works.
- The full list with operations per scope is in [OAuth scopes](/foundations/oauth-scopes.md).

# Authorization After Authentication

A valid token proves *who* is calling. Whether that user may perform the operation is a separate check against the user's organization role, workspace role or view permission; failures return HTTP 403 with error [`7301`](/foundations/error-codes.md#error-7301). See [Roles & permissions](/foundations/roles-and-permissions.md) and [Permission matrix](/foundations/permission-matrix.md).

# Failure Signals

| Symptom | Code | Cause | Fix |
|---|---|---|---|
| HTTP 401, `INVALID_OAUTHTOKEN` | 8535 | Token missing, malformed, expired, revoked, issued on another data center, or lacking the required scope. | Refresh or regenerate the token on the correct `accounts` host with the correct scopes. |
| HTTP 400, `ORGID_NOT_PRESENT_IN_THE_HEADER` | 8083 | Token is fine but the `ZANALYTICS-ORGID` header is missing. | Send the organization ID header (see [Request conventions](/foundations/request-conventions.md)). |
| HTTP 403, `SECURITY_NOT_PERMITTED` | 7301 | Authenticated user lacks the role or permission. | See [Roles & permissions](/foundations/roles-and-permissions.md). |

# Security Notes

- Treat access and refresh tokens as secrets; never embed them in client-side code or URLs.
- Tokens are bound to a data center. A token from `accounts.zoho.eu` does not work against `analyticsapi.zoho.com`.
- Embed URLs, private URLs and slideshow keys returned by the publish APIs are themselves credentials (they grant login-free access); see [Share & Publish](/domains/share-and-publish/overview.md).

# Related

- [OAuth scopes](/foundations/oauth-scopes.md)
- [Data centers](/foundations/data-centers.md)
- [Request conventions](/foundations/request-conventions.md)
- [SDK clients](/foundations/sdk-clients.md)
