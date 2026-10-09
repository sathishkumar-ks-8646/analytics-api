---
type: Reference
title: Error codes - quick reference
description: "Compact one-line-per-code table of all 352 Zoho Analytics REST API v2 error codes (code, summary constant, HTTP status, meaning); use the full catalog for per-operation reasons and solutions."
tags:
  - zoho-analytics
  - rest-api-v2
  - errors
  - error-codes
  - quick-reference
error_code_count: 352
full_catalog: "/foundations/error-codes.md"
sources:
  - id: error-catalog
    resource: "/foundations/error-codes.md"
    title: Error code catalog (this bundle)
    author: team:zoho-analytics-api-docs
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

One row per error code. Follow the code link for the full entry with per-operation reasons, solutions and the operations that raise it. Failure envelope: `{"status":"failure","summary":"<CONSTANT>","data":{"errorCode":<int>,"errorMessage":"..."}}`. HTTP status is "observed" from documented samples or "typical" for the code family. See [Error code catalog](error-codes.md) and [HTTP status codes](http-status-codes.md).

# Codes

| Code | Constant | HTTP | Meaning | Ops |
|---|---|---|---|---|
| [6004](error-codes.md#error-6004) | - | 400 (typical) | Adding these users would exceed the organisation's user seat limit under the current plan. | 2 |
| [6026](error-codes.md#error-6026) | - | 400 (typical) | The current plan does not support adding extra users (free plan restriction). | 1 |
| [6054](error-codes.md#error-6054) | `PUBLISHCNT_VIOLATION` | 400 (typical) | PUBLISHCNTVIOLATION — The current plan does not allow this publish operation. | 4 |
| [6055](error-codes.md#error-6055) | `REGENERATE_VIOLATION` | 400 (typical) | REGENERATEVIOLATION — The current plan does not allow regenerating a private-link key. | 1 |
| [6056](error-codes.md#error-6056) | `SHAREDUSR_PUBLISHCNT_VIOLATION` | 400 (typical) | SHAREDUSRPUBLISHCNTVIOLATION — A shared user attempted a plan-restricted private-link creation. | 3 |
| [6057](error-codes.md#error-6057) | `SHAREDUSR_REGENERATE_VIOLATION` | 400 (typical) | SHAREDUSRREGENERATEVIOLATION — A shared user attempted a plan-restricted key regeneration. | 1 |
| [6063](error-codes.md#error-6063) | `SLIDESHOW_NOT_ALLOWED` | 400 (typical) | SLIDESHOWNOTALLOWED — The workspace owner's plan does not include the slideshow feature. | 6 |
| [6071](error-codes.md#error-6071) | - | 400 (typical) | One or more of the specified email addresses is already a member of this organisation. | 1 |
| [6089](error-codes.md#error-6089) | - | 400 (typical) | Attempted to assign "ORGADMIN" role via a custom domain (domainName). Organization Admin role cannot be assigned through a custom portal domain. | 2 |
| [6121](error-codes.md#error-6121) | `EXCEEDING_USR_PLN_PRIVATE_LINKS` | 400 (typical) | EXCEEDINGUSRPLNPRIVATELINKS — The organization has used all private links allowed by its plan. | 1 |
| [6122](error-codes.md#error-6122) | `EXCEEDING_USR_PLN_PRIVATE_LINKS_DM` | 400 (typical) | EXCEEDINGUSRPLNPRIVATELINKSDM — Same limit, reported to a non-super-admin caller. | 1 |
| [6142](error-codes.md#error-6142) | `CUSTOMROLES_NOT_ALLOWED_IN_PLAN` | 400 (observed) | CUSTOMROLESNOTALLOWEDINPLAN — The plan does not include custom roles. | 4 |
| [7005](error-codes.md#error-7005) | `COMMON_INTERNAL_SERVER_ERROR` | 500 (typical) | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | 3 |
| [7016](error-codes.md#error-7016) | - | 400 (typical) | title is empty or whitespace-only. | 2 |
| [7018](error-codes.md#error-7018) | - | 400 (typical) | Malformed URL — the ID is not a valid numeric path segment. | 1 |
| [7082](error-codes.md#error-7082) | - | 400 (typical) | An unexpected error occurred during the trash restore operation. | 2 |
| [7089](error-codes.md#error-7089) | - | 400 (typical) | (For hide) All columns cannot be hidden simultaneously. | 2 |
| [7092](error-codes.md#error-7092) | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` | 400 (typical) | DDLLOCKSINCEIMPORTINPROGRESS — A batch import is holding a lock in this workspace. | 12 |
| [7103](error-codes.md#error-7103) | `META_OBJECT_NOT_PRESENT` | 404 (typical) | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. | 96 |
| [7104](error-codes.md#error-7104) | `META_OBJECT_NOT_PRESENT` | 404 (typical) | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. | 44 |
| [7105](error-codes.md#error-7105) | - | 400 (typical) | The specified view does not exist. | 1 |
| [7106](error-codes.md#error-7106) | `META_OBJECT_NOT_PRESENT` | 404 (observed) | The report does not exist or has been deleted. | 3 |
| [7107](error-codes.md#error-7107) | `META_OBJECT_NOT_PRESENT` | 400 (observed) | The specified column does not exist in the table. | 13 |
| [7111](error-codes.md#error-7111) | `META_DBOBJECT_NAME_DUPLICATED` | 400 (observed) | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. | 13 |
| [7112](error-codes.md#error-7112) | - | 400 (typical) | The formula expression could not be parsed (syntax error). | 4 |
| [7113](error-codes.md#error-7113) | - | 400 (typical) | The expression references an unknown/unsupported function. | 4 |
| [7115](error-codes.md#error-7115) | - | 400 (typical) | The expression references a column that does not exist, or the formula is otherwise invalid. | 4 |
| [7116](error-codes.md#error-7116) | - | 400 (typical) | The expression references a column that does not exist, or the formula is otherwise invalid. | 4 |
| [7125](error-codes.md#error-7125) | - | 400 (typical) | The specified data type is not compatible with the column's configuration. | 2 |
| [7126](error-codes.md#error-7126) | - | 400 (typical) | A column name is empty or missing. | 1 |
| [7127](error-codes.md#error-7127) | - | 400 (typical) | A column name exceeds the maximum allowed length. | 1 |
| [7128](error-codes.md#error-7128) | `COLUMNS` | 400 (typical) | Duplicate column names found in the COLUMNS array. | 1 |
| [7137](error-codes.md#error-7137) | `NOT_A_TABLE` | 400 (observed) | NOTATABLE — The target view is not a table. | 3 |
| [7138](error-codes.md#error-7138) | `META_OBJECT_NOT_PRESENT` | 400 (typical) | baseTableName does not resolve to a table in this workspace. | 5 |
| [7140](error-codes.md#error-7140) | - | 400 (typical) | A folder with the same name already exists in the workspace. | 2 |
| [7143](error-codes.md#error-7143) | `DEFAULT`, `AUTO_NUMBER` | 400 (typical) | A DEFAULT value was provided for an AUTONUMBER column. | 1 |
| [7144](error-codes.md#error-7144) | `FOLDERNAME` | 400 (typical) | The specified folder does not exist. | 10 |
| [7146](error-codes.md#error-7146) | `DATATYPE` | 400 (typical) | The DATATYPE value is not a recognised data type. | 2 |
| [7157](error-codes.md#error-7157) | - | 400 (typical) | A column with the same name already exists in the table. | 2 |
| [7160](error-codes.md#error-7160) | - | 400 (typical) | Formula columns are not allowed for this user/view combination. | 7 |
| [7164](error-codes.md#error-7164) | `SYSTEM_TABLE_DATA_MOD` | 400 (typical) | SYSTEMTABLEDATAMOD — System table data cannot be modified. | 7 |
| [7165](error-codes.md#error-7165) | `SNAPSHOT_TABLE_DATAMOD` | 400 (typical) | SNAPSHOTTABLEDATAMOD — Snapshot table data cannot be modified. | 6 |
| [7166](error-codes.md#error-7166) | - | 400 (typical) | The child column is itself a lookup-derived column (lookup-on-lookup is not allowed). | 1 |
| [7173](error-codes.md#error-7173) | - | 400 (typical) | The aggregate formula is currently used by one or more dependent views/dashboards/formulas; deletion blocked. | 1 |
| [7180](error-codes.md#error-7180) | - | 400 (typical) | The formula creates a circular dependency (it references a formula that, directly or indirectly, references this one). | 2 |
| [7181](error-codes.md#error-7181) | - | 400 (typical) | The formula creates a circular dependency (it references a formula that, directly or indirectly, references this one). | 2 |
| [7183](error-codes.md#error-7183) | - | 400 (typical) | The lookup column's data type is incompatible with the referenced column's data type. | 2 |
| [7184](error-codes.md#error-7184) | - | 400 (typical) | Adding this lookup would create a circular relationship chain across tables. | 1 |
| [7196](error-codes.md#error-7196) | `SLIDENAME_ALREADY_EXISTS` | 404 (observed) | SLIDENAMEALREADYEXISTS — Another slideshow in this workspace already uses slideName. | 2 |
| [7203](error-codes.md#error-7203) | `IMPORT_FILE_EMPTY` | 400 (typical) | IMPORTFILEEMPTY — No file was uploaded for this batch, or it is empty. | 4 |
| [7208](error-codes.md#error-7208) | `IMPORT_FILE_NUMBER_OF_FIELDS_EXCEEDS_SIZE` | 400 (typical) | IMPORTFILENUMBEROFFIELDSEXCEEDSSIZE — A row contains more fields than the header defines. | 2 |
| [7232](error-codes.md#error-7232) | `IMPORT_ABORTED`, `ABORT` | 400 (observed) | IMPORTABORTED — A value could not be parsed and onError is ABORT. errorMessage carries the per-line detail. | 2 |
| [7248](error-codes.md#error-7248) | `INVALID_FILE_CONTENT` | 400 (typical) | INVALIDFILECONTENT — The payload could not be parsed as the declared fileType. | 6 |
| [7277](error-codes.md#error-7277) | - | 400 (typical) | The folder contains tables that have dependent child views; deletion blocked. | 3 |
| [7280](error-codes.md#error-7280) | - | 400 (typical) | A lookup relationship already exists on this child column. | 1 |
| [7282](error-codes.md#error-7282) | - | 400 (typical) | A group with the same name already exists in this workspace. Group names must be unique per workspace. | 2 |
| [7301](error-codes.md#error-7301) | `SECURITY_NOT_PERMITTED` | 403 (observed) | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. | 175 |
| [7307](error-codes.md#error-7307) | `OWNER_CANNOT_SHARE_HIMSELF` | 400 (typical) | OWNERCANNOTSHAREHIMSELF — The sharer attempted to share a view to themselves. | 1 |
| [7309](error-codes.md#error-7309) | `SECURITY_NEEDS_LOGIN` | 400 (typical) | SECURITYNEEDSLOGIN — No authentication was supplied. | 7 |
| [7319](error-codes.md#error-7319) | `OBJID_NOT_BELONGS_TO_DB` | 400 (typical) | The view does not belong to the specified workspace. | 51 |
| [7320](error-codes.md#error-7320) | `CANNOT_SHARETO_SELF` | 400 (typical) | CANNOTSHARETOSELF — Same as above (alternate path). | 1 |
| [7321](error-codes.md#error-7321) | `VIEW_ALREADY_SHARED` | 400 (typical) | VIEWALREADYSHARED — The view is already shared with this user. | 1 |
| [7322](error-codes.md#error-7322) | `VIEW_ALREADY_SHARED` | 400 (typical) | VIEWALREADYSHARED (group form) — The view is already shared with this group. | 1 |
| [7323](error-codes.md#error-7323) | `CANNOT_SHARED_TO_OBJOWNER` | 400 (typical) | CANNOTSHAREDTOOBJOWNER — Attempted to share the view with its own owner. | 1 |
| [7327](error-codes.md#error-7327) | `FILTER_CRITERIA_INVALID` | 400 (typical) | FILTERCRITERIAINVALID — criteria parsed but could not be converted into a query. | 2 |
| [7330](error-codes.md#error-7330) | `UNKNOWN_COLUMN_IN_FILTERCRITERIA` | 400 (typical) | UNKNOWNCOLUMNINFILTERCRITERIA — A column named in criteria does not exist in the view. | 4 |
| [7331](error-codes.md#error-7331) | `FILTERCRITERIA_PARSE_ERROR` | 400 (typical) | FILTERCRITERIAPARSEERROR — criteria is syntactically malformed. | 2 |
| [7332](error-codes.md#error-7332) | `UNKNOWN_TABLE_IN_FILTERCRITERIA` | 400 (typical) | UNKNOWNTABLEINFILTERCRITERIA — A table qualifier in criteria is not part of the view. | 2 |
| [7333](error-codes.md#error-7333) | `INVALID_GROUP_FUNC_USE_IN_FILTERCRITERIA` | 400 (typical) | INVALIDGROUPFUNCUSEINFILTERCRITERIA — An aggregate function was used in criteria. | 2 |
| [7336](error-codes.md#error-7336) | `BATCH_IMPORT_LIMIT_EXCEEDED` | 400 (observed) | BATCHIMPORTLIMITEXCEEDED — More than 100 batches were sent for one job. | 2 |
| [7337](error-codes.md#error-7337) | `BATCH_IMPORT_LAST_BATCH_ALREADY_RECEIVED` | 400 (observed) | BATCHIMPORTLASTBATCHALREADYRECEIVED — A batch was sent after isLastBatch: true. | 2 |
| [7338](error-codes.md#error-7338) | `BATCH_IMPORT_INVALID_KEY` | 400 (observed) | The specified <group-id> does not belong to this workspace. | 7 |
| [7340](error-codes.md#error-7340) | `BATCH_IMPORT_VIEWID_MISMATCH` | 400 (observed) | BATCHIMPORTVIEWIDMISMATCH — The batchKey belongs to a different table. | 1 |
| [7351](error-codes.md#error-7351) | `SLIDESHOW_NOT_BELONGS_TO_DB` | 400 (observed) | SLIDESHOWNOTBELONGSTODB — The slideshow does not exist, or belongs to a different workspace. | 4 |
| [7362](error-codes.md#error-7362) | - | 400 (typical) | folderId does not exist in the workspace. | 2 |
| [7367](error-codes.md#error-7367) | - | 400 (typical) | The lookup is used by one or more dependent views; removal blocked. | 1 |
| [7377](error-codes.md#error-7377) | - | 400 (typical) | An identical lookup relationship (same child column → same reference column) is already defined. | 1 |
| [7378](error-codes.md#error-7378) | - | 400 (typical) | No lookup relationship is defined on this column. | 1 |
| [7379](error-codes.md#error-7379) | - | 400 (typical) | A lookup column cannot reference a column within the same table. | 2 |
| [7390](error-codes.md#error-7390) | `WORKSPACE_NOT_BELONGS_TO_ORG` | 400 (typical) | WORKSPACENOTBELONGSTOORG — The workspace does not belong to the organization in ZANALYTICS-ORGID. | 11 |
| [7395](error-codes.md#error-7395) | - | 400 (typical) | The column specified in LOOKUPCOLUMN.COLUMNNAME does not exist in the referenced table. | 1 |
| [7396](error-codes.md#error-7396) | `SLIDE_NOT_PRESENT_IN_DB` | 400 (typical) | SLIDENOTPRESENTINDB — The slideshow record exists but no slide details could be read for it. | 2 |
| [7397](error-codes.md#error-7397) | - | 400 (typical) | The view is not a table. | 6 |
| [7399](error-codes.md#error-7399) | - | 400 (typical) | The query references a spatial (GEO) file-based table, which is not supported for query tables. | 1 |
| [7400](error-codes.md#error-7400) | - | 400 (typical) | Query tables are not supported/allowed for this workspace. | 1 |
| [7401](error-codes.md#error-7401) | - | 400 (typical) | The SQL statement is not a valid/allowed SQL construct. | 3 |
| [7402](error-codes.md#error-7402) | - | 400 (typical) | The SQL statement is invalid. | 2 |
| [7403](error-codes.md#error-7403) | - | 400 (typical) | Parsing of the SQL query failed. | 2 |
| [7404](error-codes.md#error-7404) | - | 400 (typical) | Conversion of the SQL query to the internal execution engine failed. | 2 |
| [7405](error-codes.md#error-7405) | `DML_NOT_ALLOWED` | 400 (typical) | DMLNOTALLOWED — Row modification is not allowed for this table. | 3 |
| [7407](error-codes.md#error-7407) | `SELECT` | 400 (typical) | An invalid column was referenced in the SELECT clause. | 2 |
| [7408](error-codes.md#error-7408) | `WHERE` | 400 (typical) | An invalid column was referenced elsewhere in the query (e.g., WHERE, GROUP BY). | 1 |
| [7409](error-codes.md#error-7409) | - | 400 (typical) | An invalid/unknown table was referenced in the query. | 2 |
| [7413](error-codes.md#error-7413) | `TABLENAME` | 400 (typical) | TABLENAME is missing or null. | 3 |
| [7414](error-codes.md#error-7414) | - | 400 (typical) | Folder name cannot be empty. | 2 |
| [7415](error-codes.md#error-7415) | - | 400 (typical) | The specified workspace is not the calling user's current default workspace. This API does not succeed silently for non-default workspaces. | 1 |
| [7421](error-codes.md#error-7421) | - | 400 (typical) | A general SQL parse error occurred. | 1 |
| [7422](error-codes.md#error-7422) | - | 400 (typical) | The query table is referenced as a source by a child view, preventing this type of structural change. | 1 |
| [7427](error-codes.md#error-7427) | - | 400 (typical) | The specified <formula-id> is not a valid formula column on this view. | 2 |
| [7428](error-codes.md#error-7428) | - | 400 (typical) | The specified <formula-id> is not a valid aggregate formula on this view. | 4 |
| [7429](error-codes.md#error-7429) | - | 400 (typical) | A design edit (schema change) is already in progress for this query table. | 1 |
| [7433](error-codes.md#error-7433) | `SELECT` | 400 (typical) | Duplicate column names detected in the SELECT clause (after aliasing). | 1 |
| [7439](error-codes.md#error-7439) | - | 400 (typical) | The view is not a table. | 3 |
| [7447](error-codes.md#error-7447) | - | 400 (typical) | The query result would exceed the allowed row/column limit. | 2 |
| [7467](error-codes.md#error-7467) | - | 400 (typical) | Formula columns are not supported on Pipeline Tables. | 3 |
| [7478](error-codes.md#error-7478) | `MORE_THAN_MAX_COLUMN` | 400 (typical) | MORETHANMAXCOLUMN — The source has more columns than a table can hold. | 6 |
| [7479](error-codes.md#error-7479) | - | 400 (typical) | A card is missing one or more of type, width, height, left, top. | 2 |
| [7480](error-codes.md#error-7480) | - | 400 (typical) | Negative offset, width/height of 1 or less, or left + width > 80. | 2 |
| [7481](error-codes.md#error-7481) | - | 400 (typical) | The referenced view exists but the caller cannot read it. | 2 |
| [7482](error-codes.md#error-7482) | - | 400 (typical) | Two cards overlap. | 2 |
| [7483](error-codes.md#error-7483) | `HTML`, `TITLE` | 400 (typical) | A HTML, TITLE, PARA, IMAGE or EMBED card has absent, null or empty content. | 2 |
| [7484](error-codes.md#error-7484) | - | 400 (typical) | More than 100 cards in the layout. | 2 |
| [7485](error-codes.md#error-7485) | - | 400 (typical) | Unrecognised card type. | 2 |
| [7486](error-codes.md#error-7486) | - | 400 (typical) | A positional field has the wrong JSON type. | 2 |
| [7487](error-codes.md#error-7487) | - | 400 (typical) | displayName or layout is absent, null or empty. | 2 |
| [7488](error-codes.md#error-7488) | - | 400 (typical) | A settings or themes key has an empty or null value, or an unrecognised key reached the server. | 2 |
| [7491](error-codes.md#error-7491) | - | 400 (typical) | The sub-object required by themes.type is missing, or card is absent. | 2 |
| [7492](error-codes.md#error-7492) | - | 400 (typical) | A required field inside the type sub-object or inside card is missing. | 2 |
| [7493](error-codes.md#error-7493) | - | 400 (typical) | A sub-object belonging to a different theme type is present, or a forbidden key accompanies default. | 2 |
| [7496](error-codes.md#error-7496) | - | 400 (typical) | Maximum subfolder nesting depth exceeded. | 1 |
| [7500](error-codes.md#error-7500) | `UNAUTHORIZED_ORG_CANNOT_MAKEPUBLIC` | 400 (typical) | UNAUTHORIZEDORGCANNOTMAKEPUBLIC — publicPermLevel: "3" requested but the caller does not belong to the workspace admin's business organization. | 1 |
| [7507](error-codes.md#error-7507) | - | 400 (typical) | displayName exceeds 100 characters, or description exceeds 250. | 2 |
| [7509](error-codes.md#error-7509) | - | 400 (typical) | The reference column contains duplicate values; it must be unique to serve as the reference side. | 1 |
| [7510](error-codes.md#error-7510) | - | 400 (typical) | layout is not parseable JSON, or a themes sub-object is null. | 2 |
| [7511](error-codes.md#error-7511) | - | 400 (typical) | The target is a tabbed dashboard. | 2 |
| [7512](error-codes.md#error-7512) | `INVALID_DATE_FORMAT` | 400 (typical) | INVALIDDATEFORMAT — A date pattern could not be parsed. | 10 |
| [7513](error-codes.md#error-7513) | - | 400 (typical) | chartEffect.type supplied while chartEffect.apply is 1. | 2 |
| [7514](error-codes.md#error-7514) | - | 400 (typical) | chartEffect.apply is 2 but chartEffect.type is absent. | 2 |
| [7515](error-codes.md#error-7515) | `UNKNOWN_LOOKUP_VALUE` | 400 (typical) | UNKNOWNLOOKUPVALUE — A value for a lookup column does not exist in the parent table. | 2 |
| [7531](error-codes.md#error-7531) | `PUBLIC_TO_ORG_NOT_SUPPORTED_IN_FREE` | 400 (typical) | PUBLICTOORGNOTSUPPORTEDINFREE — publicPermLevel 2 or 3 is not supported on the Free plan. | 1 |
| [7533](error-codes.md#error-7533) | `CANNOT_SHARE_OBJECT_TO_GROUP` | 400 (typical) | CANNOTSHAREOBJECTTOGROUP — The view's type does not support group sharing. | 2 |
| [7535](error-codes.md#error-7535) | `CANNOT_SHARE_TO_MEMBERS_NOT_PART_OF_ORG` | 400 (typical) | CANNOTSHARETOMEMBERSNOTPARTOFORG — One or more emailIds do not belong to the organization. | 1 |
| [7541](error-codes.md#error-7541) | `FILTER_CRITERIA_NOT_SUPPORTED_FOR_MULTI_VIEW_SHARE` | 400 (typical) | FILTERCRITERIANOTSUPPORTEDFORMULTIVIEWSHARE — criteria supplied with more than one viewIds entry. | 1 |
| [7542](error-codes.md#error-7542) | `FILTER_CRITERIA_NOT_PERMITTED_FOR_SHARED_USER` | 400 (typical) | FILTERCRITERIANOTPERMITTEDFORSHAREDUSER — criteria update is not permitted for this share type. | 1 |
| [7543](error-codes.md#error-7543) | `ONLY_BASETABLE_COL_IN_TABULAR_FILTERCRITERIA`, `VUD_OR_DRILL_COLUMNS_EDIT_NOT_SUPPORTED_FOR_MULTI_VIEW_SHARE` | 400 (typical) | ONLYBASETABLECOLINTABULARFILTERCRITERIA — criteria on a tabular view referenced a column outside its base table. | 3 |
| [7545](error-codes.md#error-7545) | `SHARE_AND_WRITE_PERMISSIONS_NOT_ALLOWED_FOR_RO_USERS` | 400 (typical) | SHAREANDWRITEPERMISSIONSNOTALLOWEDFORROUSERS — A Read-Only/embedded user was granted share together with a write permission. | 2 |
| [7548](error-codes.md#error-7548) | `NO_SUCH_ROLE_EXIST` | 400 (observed) | NOSUCHROLEEXIST — No role exists for the given <role-id>. | 2 |
| [7549](error-codes.md#error-7549) | `CANNOT_SHARE_TO_CUSTOMROLE_USER` | 400 (typical) | CANNOTSHARETOCUSTOMROLEUSER — Attempted to share directly to a user who only has a custom-role-based org-level permission. | 1 |
| [7550](error-codes.md#error-7550) | - | 400 (typical) | The specified role name does not exist as a custom role in the org. | 2 |
| [7553](error-codes.md#error-7553) | `ROLENAME_EXISTS` | 400 (observed) | ROLENAMEEXISTS — A role with this name already exists in the organization. | 2 |
| [7554](error-codes.md#error-7554) | `INVALID_VIEWTYPE_GROUP` | 400 (typical) | INVALIDVIEWTYPEGROUP — accessType did not resolve to a known level. | 2 |
| [7559](error-codes.md#error-7559) | `EXPORT_PERM_NEEDED_FOR_EMAILSCH` | 400 (observed) | EXPORTPERMNEEDEDFOREMAILSCH — manageEmailSchedules is true but export is not. | 2 |
| [7565](error-codes.md#error-7565) | `UNVERIFIED_EMAIL` | 400 (typical) | UNVERIFIEDEMAIL — The calling user's primary email address is not verified. | 11 |
| [7571](error-codes.md#error-7571) | `UNKNOWN_VIEWID_PASSED` | 400 (typical) | UNKNOWNVIEWIDPASSED — A tableCriteriaList[].viewId does not exist in this workspace. | 1 |
| [7573](error-codes.md#error-7573) | `CR_DATA_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` | 400 (observed) | CRDATAPERMNOTALLOWEDFORACCESSTYPE — A data permission was enabled below the full access level. | 2 |
| [7574](error-codes.md#error-7574) | `CR_DESIGN_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` | 400 (typical) | CRDESIGNPERMNOTALLOWEDFORACCESSTYPE — designModify was enabled below the full access level. | 2 |
| [7575](error-codes.md#error-7575) | `CR_CREATE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` | 400 (typical) | CRCREATEPERMNOTALLOWEDFORACCESSTYPE — createTable, createQueryTable, or createFormula was enabled below the full access level. | 2 |
| [7576](error-codes.md#error-7576) | `CR_ALERT_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE`, `ALL_DASHBOARDS` | 400 (typical) | CRALERTPERMNOTALLOWEDFORACCESSTYPE — manageDataAlerts was enabled with ALLDASHBOARDS. | 2 |
| [7577](error-codes.md#error-7577) | `CR_SCHEDULED_DATA_DELETION_PERM_NOT_ALLOWED` | 400 (typical) | CRSCHEDULEDDATADELETIONPERMNOTALLOWED — dataArchives is true but not every data permission is enabled. | 2 |
| [7578](error-codes.md#error-7578) | `CR_DESIGN_MODIFY_REQUIRES_PRESET_PERMS` | 400 (typical) | CRDESIGNMODIFYREQUIRESPRESETPERMS — designModify is true without both preset permissions. | 2 |
| [7579](error-codes.md#error-7579) | `CR_READ_PERM_MUST_BE_ENABLED` | 400 (observed) | CRREADPERMMUSTBEENABLED — interactionPermissions.read is missing or false. | 2 |
| [7580](error-codes.md#error-7580) | `CR_ACCESS_TYPE_AND_PERMS_REQUIRED_TOGETHER` | 400 (observed) | CRACCESSTYPEANDPERMSREQUIREDTOGETHER — One of accessType / permissions was sent without the other. | 1 |
| [7581](error-codes.md#error-7581) | `CR_NO_FIELDS_TO_UPDATE` | 400 (observed) | CRNOFIELDSTOUPDATE — Neither roleName nor accessType was supplied. | 1 |
| [7584](error-codes.md#error-7584) | `CR_DATASOURCE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` | 400 (typical) | CRDATASOURCEPERMNOTALLOWEDFORACCESSTYPE — A datasource permission was enabled below the full access level. | 2 |
| [7585](error-codes.md#error-7585) | `CR_USE_DATASOURCE_REQUIRES_CREATETABLE` | 400 (typical) | CRUSEDATASOURCEREQUIRESCREATETABLE — useDatasource is true but createTable is not. | 2 |
| [7586](error-codes.md#error-7586) | `CR_VIEW_DATASOURCE_REQUIRED_FOR_DATASOURCE_PERMS` | 400 (typical) | CRVIEWDATASOURCEREQUIREDFORDATASOURCEPERMS — Another datasource permission is enabled without viewDatasource. | 2 |
| [7701](error-codes.md#error-7701) | - | 400 (typical) | A chart report has no X-axis or no Y-axis column. | 2 |
| [7703](error-codes.md#error-7703) | - | 400 (typical) | A colorAxis column is present alongside more than one Y-axis column. | 2 |
| [7727](error-codes.md#error-7727) | - | 400 (typical) | More than 15 Y-axis columns on a chart. | 2 |
| [7801](error-codes.md#error-7801) | `MARGIN_VALUE_EXCEEDS` | 400 (typical) | MARGINVALUEEXCEEDS — A PDF margin is outside 0–1 inches. | 3 |
| [7803](error-codes.md#error-7803) | `INVALID_DIMENSION` | 400 (typical) | INVALIDDIMENSION — width or height is outside the permitted image range. | 2 |
| [7806](error-codes.md#error-7806) | `XLS_CELL_LIMIT_EXCEEDS` | 400 (typical) | XLSCELLLIMITEXCEEDS — The XLS export exceeds the per-sheet cell limit. | 1 |
| [7807](error-codes.md#error-7807) | `XLS_COL_LIMIT_EXCEEDS` | 400 (typical) | XLSCOLLIMITEXCEEDS — More than 256 columns were requested for an XLS export. | 1 |
| [7808](error-codes.md#error-7808) | `XLS_CELL_CHAR_LIMIT_EXCEEDS` | 400 (typical) | XLSCELLCHARLIMITEXCEEDS — A single cell exceeds 32,767 characters. | 1 |
| [7809](error-codes.md#error-7809) | `XLS_NO_DATA` | 400 (typical) | XLSNODATA — The XLS export produced no data. | 1 |
| [7812](error-codes.md#error-7812) | `SCHEDULE_DELETED` | 400 (observed) | SCHEDULEDELETED — No schedule exists with the given <schedule-id>. | 4 |
| [7824](error-codes.md#error-7824) | `EXPORT_REQ_BLOCKED` | 400 (typical) | EXPORTREQBLOCKED — Export has been blocked for this workspace. | 3 |
| [7827](error-codes.md#error-7827) | `EXP_PDF_RECORD_LIMIT` | 400 (typical) | EXPPDFRECORDLIMIT — The PDF exceeds 1,000,000 cells. | 3 |
| [7830](error-codes.md#error-7830) | `EXP_ALL_RECORD_LIMIT` | 400 (typical) | EXPALLRECORDLIMIT — The exported payload exceeds 100 MB. | 1 |
| [7832](error-codes.md#error-7832) | `INVALID_EXPORT_TYPE` | 400 (typical) | INVALIDEXPORTTYPE — exportType is not one of the supported formats. | 1 |
| [7835](error-codes.md#error-7835) | `NO_TABLES_INVOLVED_IN_SQL_EXPORT` | 400 (typical) | NOTABLESINVOLVEDINSQLEXPORT — The statement references no table. | 1 |
| [7836](error-codes.md#error-7836) | `GIVEN_TABLE_NOT_INVOLVED_IN_SQL_EXPORT` | 400 (observed) | GIVENTABLENOTINVOLVEDINSQLEXPORT — A tableCriteriaList[].viewId is not used by the statement. | 1 |
| [7837](error-codes.md#error-7837) | `INVOLVED_TABLE_DOES_NOT_HAVE_PERMISSION` | 400 (typical) | INVOLVEDTABLEDOESNOTHAVEPERMISSION — A table used by the query has no matching tableCriteriaList entry where one is required. | 1 |
| [7929](error-codes.md#error-7929) | - | 400 (typical) | The view has already been restored from trash. | 2 |
| [7941](error-codes.md#error-7941) | - | 400 (typical) | The view has parent dependencies that are also in trash and must be restored together. | 1 |
| [7942](error-codes.md#error-7942) | - | 400 (typical) | The view has child dependent views in trash that must be deleted together. | 1 |
| [7943](error-codes.md#error-7943) | - | 400 (typical) | The requesting user does not have permission to restore this specific trashed view. | 1 |
| [7951](error-codes.md#error-7951) | - | 400 (typical) | The organisation has reached its workspace creation limit based on the current subscription plan. | 2 |
| [8000](error-codes.md#error-8000) | `DUPLICATE_SCHEDULE` | 400 (observed) | DUPLICATESCHEDULE — A schedule with this scheduleName already exists in the workspace. | 2 |
| [8001](error-codes.md#error-8001) | `INVALID_RESP_FORMAT`, `MAILCOUNT_PER_SCHED_EXCEED` | 400 (typical) | INVALIDRESPFORMAT — responseFormat is not a supported value. | 5 |
| [8002](error-codes.md#error-8002) | `SCHMAIL_ACTION_NOTSUPPORTED` | 400 (observed) | SCHMAILACTIONNOTSUPPORTED — The schedule is not in this workspace, or the caller may not act on it. | 4 |
| [8003](error-codes.md#error-8003) | `ALL_SCH_RUNERROR` | 400 (typical) | ALLSCHRUNERROR — The schedule could not be activated. | 1 |
| [8004](error-codes.md#error-8004) | `ALL_SCH_PAUSEERROR` | 400 (typical) | ALLSCHPAUSEERROR — The schedule could not be deactivated. | 1 |
| [8005](error-codes.md#error-8005) | `SCH_NOT_IN_WS` | 400 (typical) | SCHNOTINWS — The schedule does not belong to the specified workspace. | 4 |
| [8008](error-codes.md#error-8008) | - | 400 (typical) | behaviour was supplied on a daterange or relative user filter. | 2 |
| [8009](error-codes.md#error-8009) | `MAIL_MULTIVIEW_MAXCOUNT_EXCEEEDED` | 400 (typical) | MAILMULTIVIEWMAXCOUNTEXCEEEDED — Too many views in one schedule. | 1 |
| [8014](error-codes.md#error-8014) | `API_IMAGE_RESPONSE_NOT_POSSIBLE` | 400 (observed) | APIIMAGERESPONSENOTPOSSIBLE — image was requested for a view that is not a chart. | 3 |
| [8015](error-codes.md#error-8015) | `API_EXPORT_COLUMN_NOT_PRESENT` | 400 (observed) | APIEXPORTCOLUMNNOTPRESENT — A name in selectedColumns does not match any column in the view. | 3 |
| [8016](error-codes.md#error-8016) | `API_NO_COLUMN_PRESENT` | 400 (typical) | APINOCOLUMNPRESENT — None of the supplied column names matched a column in the table. | 2 |
| [8017](error-codes.md#error-8017) | `INVALID_IMAGE_FORMAT` | 400 (typical) | INVALIDIMAGEFORMAT — imageFormat is not png, jpg, or jpeg. | 2 |
| [8021](error-codes.md#error-8021) | - | 400 (typical) | The pivot or summary structure is invalid — no data column in a pivot, too many data or groupBy columns, or a column in a position its type cannot occupy. On Update, also raised when reportType does not match the stored  | 3 |
| [8023](error-codes.md#error-8023) | `OEM_OPERATION_NOT_ALLOWED` | 403 (observed) | OEMOPERATIONNOTALLOWED — The organization/workspace is not enabled for Embedded Analytics. | 3 |
| [8024](error-codes.md#error-8024) | - | 400 (typical) | Cross-org copy attempted without a valid workspaceKey, or the provided key does not match the source workspace's secret key. | 1 |
| [8027](error-codes.md#error-8027) | `VIEW` | 400 (typical) | One or more VIEW cards name a view that does not exist in this workspace, or viewName is absent / null / non-string. | 2 |
| [8029](error-codes.md#error-8029) | `SHARE_INVALID_EMAIL_ADDRESS` | 400 (typical) | SHAREINVALIDEMAILADDRESS — One or more emailIds entries is not a valid email address. | 1 |
| [8030](error-codes.md#error-8030) | `EMAILEXPORT_DISABLED_IN_ORG` | 400 (observed) | EMAILEXPORTDISABLEDINORG — Email export is disabled for this organization. | 2 |
| [8031](error-codes.md#error-8031) | `UNTRUSTED_EMAILIDS`, `REMOVESHARE_API_PARAMS` | 400 (typical) | UNTRUSTEDEMAILIDS — A recipient address is outside the organization's trusted domains. | 3 |
| [8032](error-codes.md#error-8032) | `VIEW_NOT_SHARED`, `EMAILINGVIEW_DISABLED` | 400 (typical) | VIEWNOTSHARED — The view is not currently shared with the specified user. | 5 |
| [8033](error-codes.md#error-8033) | `MAILSCH_SELECT_ATLEASTONE_EMAILID` | 400 (typical) | MAILSCHSELECTATLEASTONEEMAILID — No recipient could be resolved from emailIds, groupIds, and cc. | 2 |
| [8034](error-codes.md#error-8034) | `ONLY_ONE_DASHBOARD_IS_ALLOWED_PER_SCH` | 400 (typical) | ONLYONEDASHBOARDISALLOWEDPERSCH — More than one view scheduled where the first is a dashboard. | 1 |
| [8035](error-codes.md#error-8035) | `EXPORT_FORMATS_ALLOWED_FOR_DASHBOARD`, `HTML` | 400 (typical) | EXPORTFORMATSALLOWEDFORDASHBOARD — Dashboard scheduled with a format other than PDF/HTML. | 1 |
| [8036](error-codes.md#error-8036) | `EXPORT_FORMATS_ALLOWED_FOR_CHART` | 400 (typical) | EXPORTFORMATSALLOWEDFORCHART — IMG requested for a view that is not a chart. | 1 |
| [8037](error-codes.md#error-8037) | `ONLY_ONE_VIEW_IS_ALLOWED_FOR_XLS` | 400 (typical) | ONLYONEVIEWISALLOWEDFORXLS — XLS requested with more than one view. | 1 |
| [8040](error-codes.md#error-8040) | - | 400 (typical) | One or more specified email addresses are not currently Workspace Admins in this workspace. | 1 |
| [8046](error-codes.md#error-8046) | `INVALID_COLUMNS_SELECTED` | 400 (typical) | INVALIDCOLUMNSSELECTED — A name in selectedColumns is not present in the source data. | 4 |
| [8050](error-codes.md#error-8050) | `INVALID_VALUE` | 400 (observed) | A value is invalid — unknown columnName, an operation incompatible with the column, a null axisColumns. | 3 |
| [8051](error-codes.md#error-8051) | - | 400 (typical) | A required field is missing — title, reportType, axisColumns, or a mandatory key inside an axis/filter object. | 2 |
| [8052](error-codes.md#error-8052) | - | 400 (typical) | More than 1000 entries in axisColumns, filters or userFilters. | 2 |
| [8054](error-codes.md#error-8054) | `INVALID_FILTER_CRITERIA` | 400 (typical) | INVALIDFILTERCRITERIA — criteria could not be parsed. | 4 |
| [8057](error-codes.md#error-8057) | - | 400 (typical) | The column named in windowFunction.baseField cannot be used as a base field here. | 2 |
| [8058](error-codes.md#error-8058) | - | 400 (typical) | The organisation ID provided in ZANALYTICS-DEST-ORGID does not exist. | 3 |
| [8059](error-codes.md#error-8059) | - | 400 (typical) | The tableName is not part of the workspace or is not joined to the base table. | 2 |
| [8060](error-codes.md#error-8060) | `DOMAIN_NOT_EXIST` | 400 (typical) | The specified domainName does not exist. | 17 |
| [8061](error-codes.md#error-8061) | `DOMAIN_DOES_NOT_BELONGS_TO_USER` | 400 (typical) | The specified domainName does not belong to the org's Account Admin. | 17 |
| [8062](error-codes.md#error-8062) | `ADD_ROW_REQUEST_STILL_IN_PROGRESS` | 400 (typical) | ADDROWREQUESTSTILLINPROGRESS — Another row-write request for this table is still being processed. | 3 |
| [8074](error-codes.md#error-8074) | `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` | 400 (typical) | READPERMSHOULDBETRUEFORSHARING — permissions.read was sent as false. | 4 |
| [8077](error-codes.md#error-8077) | `EMPTY_JSON_CONFIGURATION`, `CONFIG` | 400 (typical) | EMPTYJSONCONFIGURATION — CONFIG was not sent, or was sent empty. | 2 |
| [8078](error-codes.md#error-8078) | `EMPTY_JSON_ATTRIBUTE_FOUND` | 400 (observed) | EMPTYJSONATTRIBUTEFOUND — A mandatory attribute was sent blank. | 6 |
| [8079](error-codes.md#error-8079) | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION`, `UPDATEADD` | 400 (typical) | A required attribute (expression or formulaName) is missing from CONFIG. | 20 |
| [8080](error-codes.md#error-8080) | `INVALID_JSON_CONFIGURATION` | 400 (typical) | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. | 14 |
| [8083](error-codes.md#error-8083) | `ORGID_NOT_PRESENT_IN_THE_HEADER` | 400 (typical) | The ZANALYTICS-ORGID header is missing from a request that requires it. | 14 |
| [8085](error-codes.md#error-8085) | `SHAREDTO_EXTERNAL_DOMAIN_NOT_ALLOWED` | 400 (typical) | SHAREDTOEXTERNALDOMAINNOTALLOWED — Sharing to an email outside the allowed domain(s) is disabled by org policy. | 1 |
| [8086](error-codes.md#error-8086) | `SHAREDTO_EXTERNAL_DOMAIN_NOT_ALLOWED` | 400 (typical) | SHAREDTOEXTERNALDOMAINNOTALLOWED — Sharing to an email outside the allowed domain(s) is disabled by org policy. | 1 |
| [8088](error-codes.md#error-8088) | `SECURITY_CONTROLS_FEATURE_DISABLED` | 400 (typical) | SECURITYCONTROLSFEATUREDISABLED — Export is disabled for the organization. | 7 |
| [8092](error-codes.md#error-8092) | - | 400 (typical) | reportType resolves to a view kind that cannot be saved standalone. | 2 |
| [8105](error-codes.md#error-8105) | `REMOVESHARE_ALL_VIEWS_PRESENT` | 400 (typical) | REMOVESHAREALLVIEWSPRESENT — Both viewIds and removeAllViews: true were supplied together. | 1 |
| [8114](error-codes.md#error-8114) | - | 400 (typical) | One or more specified email addresses are not members of this organisation. | 4 |
| [8115](error-codes.md#error-8115) | `VIEW_NOT_PUBLISHED_AS_PRIVATE` | 404 (observed) | VIEWNOTPUBLISHEDASPRIVATE — The view has no private link. | 2 |
| [8116](error-codes.md#error-8116) | - | 400 (typical) | Auto analysis has already been completed for this table and analyseAgain was not set to true. | 2 |
| [8119](error-codes.md#error-8119) | `INVALID_VALUE_FOR_ATTRIBUTE` | 400 (observed) | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. | 20 |
| [8120](error-codes.md#error-8120) | `EXPORT_JOB_NOT_FOUND` | 404 (observed) | EXPORTJOBNOTFOUND — No export job exists for the given ID (HTTP 404). | 2 |
| [8121](error-codes.md#error-8121) | `EXPORT_JOB_NOT_INITIATED` | 400 (observed) | EXPORTJOBNOTINITIATED — The job is queued but has not started (jobCode 1001). | 1 |
| [8122](error-codes.md#error-8122) | `EXPORT_JOB_NOT_COMPLETED` | 400 (observed) | EXPORTJOBNOTCOMPLETED — The job is still running (jobCode 1002). | 1 |
| [8123](error-codes.md#error-8123) | `EXPORT_JOB_ERROR_OCCURRED` | 400 (observed) | EXPORTJOBERROROCCURRED — The job failed (jobCode 1003). | 1 |
| [8124](error-codes.md#error-8124) | `EXPORT_JOB_ACCESS_DENIED` | 403 (observed) | EXPORTJOBACCESSDENIED — The caller did not create this job (HTTP 403). | 2 |
| [8125](error-codes.md#error-8125) | `CALLBACKURL_NOT_VALID`, `CALLBACKURL_CONNECTION_ERROR` | 400 (typical) | Callback URL is malformed, unreachable, or private. | 6 |
| [8126](error-codes.md#error-8126) | `CALLBACKURL_CONNECTION_ERROR`, `CALLBACKURL_NOT_VALID` | 400 (typical) | Callback URL is malformed, unreachable, or private. | 6 |
| [8127](error-codes.md#error-8127) | `CALLBACKURL_RESTRICTED`, `CALLBACKURL_NOT_VALID` | 400 (typical) | Callback URL is malformed, unreachable, or private. | 6 |
| [8128](error-codes.md#error-8128) | `INTERNAL_ERROR_ON_INITIATING_EXPORT` | 400 (typical) | INTERNALERRORONINITIATINGEXPORT — The job could not be queued. | 2 |
| [8130](error-codes.md#error-8130) | `INVALID_UPDATE_CRITERIA_CONFIGURATION` | 400 (observed) | INVALIDUPDATECRITERIACONFIGURATION — Both criteria and updateAllRows were sent, or neither was. | 1 |
| [8131](error-codes.md#error-8131) | `INVALID_DELETE_CRITERIA_CONFIGURATION` | 400 (observed) | INVALIDDELETECRITERIACONFIGURATION — Both criteria and deleteAllRows were sent, or neither was. | 1 |
| [8132](error-codes.md#error-8132) | `ASYNC_EXPORT_LIMIT_EXCEEDED` | 400 (observed) | ASYNCEXPORTLIMITEXCEEDED — 5 export jobs are already queued or running for the organization. | 2 |
| [8133](error-codes.md#error-8133) | `SYNC_EXPORT_NOT_ALLOWED` | 400 (observed) | SYNCEXPORTNOTALLOWED — The view is a dashboard, a query table, a live-connect view, or a table above the row limit. | 1 |
| [8134](error-codes.md#error-8134) | `ASYNC_IMPORT_LIMIT_EXCEEDED` | 400 (observed) | ASYNCIMPORTLIMITEXCEEDED — The maximum number of simultaneous import jobs is in progress. | 4 |
| [8137](error-codes.md#error-8137) | `IMPORT_JOB_NOT_FOUND` | 400 (typical) | IMPORTJOBNOTFOUND — No import job exists with this ID. | 1 |
| [8138](error-codes.md#error-8138) | `IMPORT_JOB_ACCESS_DENIED` | 403 (observed) | IMPORTJOBACCESSDENIED — The job was created by a different user. | 1 |
| [8139](error-codes.md#error-8139) | `PASTED_DATA_LIMIT_EXCEEDED`, `DATA` | 400 (typical) | PASTEDDATALIMITEXCEEDED — The DATA parameter exceeds 10,000,000 characters. | 2 |
| [8144](error-codes.md#error-8144) | - | 400 (typical) | chartType is not a recognised chart name. | 2 |
| [8145](error-codes.md#error-8145) | - | 400 (typical) | folderId was supplied. | 1 |
| [8147](error-codes.md#error-8147) | - | 400 (typical) | settings was supplied for a non-pivot report. | 2 |
| [8148](error-codes.md#error-8148) | `DECIMAL_AND_THOUSAND_SEPARATOR_SAME` | 400 (typical) | Separator configuration errors. | 6 |
| [8149](error-codes.md#error-8149) | `DECIMAL_AND_THOUSAND_COLUMN_SEPARATOR_LEGNTH_VALIDATION` | 400 (typical) | DECIMALANDTHOUSANDCOLUMNSEPARATORLEGNTHVALIDATION — A columnSeparators entry has fewer than two values. | 6 |
| [8150](error-codes.md#error-8150) | `VIEW_NOT_SHARED_TO_GROUP` | 400 (typical) | VIEWNOTSHAREDTOGROUP — The view is not currently shared with the specified group. | 2 |
| [8152](error-codes.md#error-8152) | `INTERVAL_SHOULD_BE_120_OR_ABOVE` | 400 (observed) | INTERVALSHOULDBE120ORABOVE — autoRefresh is a positive value below 120 seconds. | 1 |
| [8154](error-codes.md#error-8154) | `COLUMN_NOT_PRESENT_IN_TABLE` | 400 (typical) | COLUMNNOTPRESENTINTABLE — A column in vudColumns / drillColumns (or in criteria) does not exist in the given table. | 4 |
| [8162](error-codes.md#error-8162) | - | 400 (typical) | rangeSize was supplied as a string, or on an operation that does not support ranges. | 2 |
| [8166](error-codes.md#error-8166) | - | 400 (typical) | The operation is incompatible with the column's data type. | 2 |
| [8167](error-codes.md#error-8167) | - | 400 (typical) | The filterType is not valid for the column type + operation combination. | 2 |
| [8168](error-codes.md#error-8168) | - | 400 (typical) | A values entry does not match the expected format for the filterType. | 2 |
| [8170](error-codes.md#error-8170) | - | 400 (typical) | An axis type is not valid for the chosen reportType. | 2 |
| [8173](error-codes.md#error-8173) | - | 400 (typical) | The number of columns in bulk mode exceeds the allowed limit. | 1 |
| [8174](error-codes.md#error-8174) | `DUPLICATE_TAG_NAME_FOUND` | 403 (observed) | DUPLICATETAGNAMEFOUND — A tag with this name already exists in the workspace. | 2 |
| [8175](error-codes.md#error-8175) | `OEM_KEY_NOT_PRESENT` | 404 (observed) | No embed URL on this view matches the supplied rsConfig. | 1 |
| [8176](error-codes.md#error-8176) | `OEM_VIEW_HOLD_NO_KEYS` | 404 (observed) | deleteAllUrls was requested but the view has no embed URLs. | 1 |
| [8177](error-codes.md#error-8177) | `MAX_ALLOWED_VALUE_EXCEEDED` | 400 (typical) | MAXALLOWEDVALUEEXCEEDED — validityPeriod exceeds the maximum of 86400 seconds (1 day). | 1 |
| [8178](error-codes.md#error-8178) | `INVALID_DELETE_EMBED_URL_CONFIGURATION` | 400 (observed) | Both rsConfig and deleteAllUrls: true were sent, or neither was. | 1 |
| [8179](error-codes.md#error-8179) | `DONT_HAVE_PERMISSION_TO_CREATE_TAGS` | 403 (observed) | DONTHAVEPERMISSIONTOCREATETAGS — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | 4 |
| [8180](error-codes.md#error-8180) | `DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS` | 403 (observed) | DONTHAVEPERMISSIONTOASSOCIATEANDUNASSOCIATETAGS — The caller is a read-only user. | 6 |
| [8181](error-codes.md#error-8181) | `TAG_COUNT_EXCEEDS` | 403 (observed) | TAGCOUNTEXCEEDS — One or more views would exceed 10 tags. The message lists them. | 2 |
| [8182](error-codes.md#error-8182) | `SYNC_CANNOT_BE_INITIATED_FOR_CONNECTOR_WITH_MULTIPLE_SCHEDULES`, `CANNOT_UPDATE_THE_TAG` | 403 (observed) | resetSort: true and sortOrder cannot be used together. | 3 |
| [8183](error-codes.md#error-8183) | `SCHEDULE_ID_NOT_ASSOCIATED_WITH_CONNECTOR` | 400 (typical) | SCHEDULEIDNOTASSOCIATEDWITHCONNECTOR — The syncIntervalId does not belong to this datasource. | 1 |
| [8184](error-codes.md#error-8184) | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` | 403 (observed) | VIEWORTAGNOTPRESENTINDBTOTAG — The tag does not exist in this workspace. | 6 |
| [8185](error-codes.md#error-8185) | `CANNOT_DELETE_OR_UPDATE_TAG` | 400 (typical) | CANNOTDELETEORUPDATETAG — The update matched no row. | 2 |
| [8187](error-codes.md#error-8187) | `TAG_NOT_PRESENT_IN_DB` | 400 (observed) | TAGNOTPRESENTINDB — The tag does not exist in this workspace. | 1 |
| [8188](error-codes.md#error-8188) | `EXPORT_INVALID_PASSWORD` | 400 (typical) | EXPORTINVALIDPASSWORD — password is blank or shorter than 6 characters. | 3 |
| [8191](error-codes.md#error-8191) | - | 400 (typical) | An invalid date value was supplied to a date filter. | 2 |
| [8201](error-codes.md#error-8201) | `INVALID_CONFIGURATION_REMOVE_VIEWS_LINKED_WITH_TAG` | 400 (observed) | INVALIDCONFIGURATIONREMOVEVIEWSLINKEDWITHTAG — viewIds is empty or absent and dissociateAll is not true. | 1 |
| [8202](error-codes.md#error-8202) | `INVALID_CONFIGURATION_REMOVE_TAGS_FOR_VIEW` | 400 (observed) | INVALIDCONFIGURATIONREMOVETAGSFORVIEW — tagIds is empty or absent and dissociateAll is not true. | 1 |
| [8241](error-codes.md#error-8241) | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` | 409 (typical) | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. | 13 |
| [8250](error-codes.md#error-8250) | - | 400 (typical) | compType is not applicable to the column category — e.g. slider on a dimension, singleSelect on a measure. | 2 |
| [8252](error-codes.md#error-8252) | - | 400 (typical) | reportType is absent or null. | 2 |
| [8253](error-codes.md#error-8253) | - | 400 (typical) | A mandatory userFilters key is missing, typically compType or filterType. | 2 |
| [8254](error-codes.md#error-8254) | - | 400 (typical) | A geoRole value is wrong for the column type. | 2 |
| [8255](error-codes.md#error-8255) | - | 400 (typical) | geoRole was supplied on a column that cannot be geocoded. | 2 |
| [8256](error-codes.md#error-8256) | - | 400 (typical) | More than one geo operation on the same axis. | 2 |
| [8257](error-codes.md#error-8257) | - | 400 (typical) | A numeric geo column coexists with a categorical geo column. | 2 |
| [8258](error-codes.md#error-8258) | - | 400 (typical) | A categorical geo column was placed on an axis other than X. | 2 |
| [8504](error-codes.md#error-8504) | `LESS_THAN_MIN_OCCURANCE`, `CONFIG` | 400 (typical) | LESSTHANMINOCCURANCE — CONFIG was not sent. | 25 |
| [8507](error-codes.md#error-8507) | `MORE_THAN_MAX_LENGTH`, `CONFIG` | 400 (typical) | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. | 17 |
| [8509](error-codes.md#error-8509) | `PATTERN_NOT_MATCHED` | 400 (typical) | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. | 10 |
| [8516](error-codes.md#error-8516) | `UNABLE_TO_PARSE_DATA_TYPE` | 400 (typical) | UNABLETOPARSEDATATYPE — A CONFIG value has the wrong JSON type. | 6 |
| [8517](error-codes.md#error-8517) | - | 400 (typical) | A field has the wrong JSON data type — exclude: "yes", isAxisMerge: "maybe", compType: 123. | 4 |
| [8525](error-codes.md#error-8525) | `URL_RULE_NOT_CONFIGURED` | 400 (typical) | URLRULENOTCONFIGURED — <role-id> is not numeric, so the request matched no route. | 2 |
| [8534](error-codes.md#error-8534) | `CONFIG`, `JSON_PARSE_ERROR` | 400 (typical) | JSONPARSEERROR — CONFIG is not valid JSON. | 6 |
| [8535](error-codes.md#error-8535) | `INVALID_OAUTHTOKEN` | 401 (typical) | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | 135 |
| [8539](error-codes.md#error-8539) | `INVALID_VALUE_NOT_ALLOWED` | 400 (typical) | INVALIDVALUENOTALLOWED — An attribute carries a value that is structurally valid but not accepted, such as an empty roleName. | 1 |
| [8542](error-codes.md#error-8542) | `CONFIG` | 400 (typical) | An unknown key is present in CONFIG, or a windowFunction is mis-configured. | 4 |
| [8544](error-codes.md#error-8544) | `OUT_OF_RANGE` | 400 (typical) | OUTOFRANGE — A schedule value is outside its declared range. | 1 |
| [8547](error-codes.md#error-8547) | `ARRAY_SIZE_OUT_OF_RANGE` | 400 (typical) | ARRAYSIZEOUTOFRANGE — selectedColumns is empty or holds more than 300 entries. | 8 |
| [9001](error-codes.md#error-9001) | `USERFILTERS` | 400 (typical) | Every card in the layout is a USERFILTERS card. | 2 |
| [9102](error-codes.md#error-9102) | `LANGUAGE_NOT_SUPPORTED` | 400 (typical) | LANGUAGENOTSUPPORTED — language is not one of the supported language names. | 1 |
| [12049](error-codes.md#error-12049) | - | 400 (typical) | The workspace is already enabled for White Label domain access. Calling Enable on an already-enabled workspace is not idempotent. | 1 |
| [12050](error-codes.md#error-12050) | - | 400 (typical) | The workspace is not currently enabled for White Label domain access. Calling Disable on an already-disabled workspace is not idempotent. | 1 |
| [12052](error-codes.md#error-12052) | `WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS` | 400 (typical) | WORKSPACENOTENABLEDFORDOMAINACCESS — The workspace is not enabled for access through the requested portal domain. | 4 |
| [14037](error-codes.md#error-14037) | - | 400 (typical) | The column is disabled in its Query Table definition and cannot be used for analysis. | 1 |
| [15007](error-codes.md#error-15007) | - | 400 (typical) | The copy operation is not allowed — the destination workspace's organisation does not match the caller's organisation, and no valid workspaceKey was supplied (or it does not match). | 2 |
| [18055](error-codes.md#error-18055) | `DBTYPE_SERVICENAME_NOTMACHED` | 400 (observed) | DBTYPESERVICENAMENOTMACHED — The databaseType is not available for the given serviceName. | 1 |
| [18056](error-codes.md#error-18056) | `NO_SOURCE_AVAILABLE_FOR_TABLE` | 400 (observed) | NOSOURCEAVAILABLEFORTABLE — The table has no datasource behind it. | 1 |
| [18057](error-codes.md#error-18057) | `INVALID_CLOUD_SERVICENAME` | 400 (observed) | INVALIDCLOUDSERVICENAME — serviceName is not a recognised service. | 1 |
| [18061](error-codes.md#error-18061) | `CONNECTION_ID_NOT_ASSOSIATED_FOR_WORKSPACE` | 400 (typical) | CONNECTIONIDNOTASSOSIATEDFORWORKSPACE — The datasource ID does not exist in this workspace, or the source type cannot be synced this way (HTTP 404). | 2 |
| [18063](error-codes.md#error-18063) | `DBTYPE_CANNOT_BE_UPDATED_FOR_LIVECONNECT_DB` | 400 (observed) | DBTYPECANNOTBEUPDATEDFORLIVECONNECTDB — databaseType differs from the stored one on a Live Connect database. | 1 |
| [18064](error-codes.md#error-18064) | `SERVICE_NAME_CANNOT_BE_UPDATED_FOR_LIVECONNECT_DB` | 400 (typical) | SERVICENAMECANNOTBEUPDATEDFORLIVECONNECTDB — serviceName differs from the stored one on a Live Connect database. | 1 |
| [18072](error-codes.md#error-18072) | `TABLE_SYNC_INPROGRESS` | 400 (observed) | TABLESYNCINPROGRESS — A sync for this table is already running. | 1 |
| [18073](error-codes.md#error-18073) | `DATASOURCE_SYNC_INPROGRESS` | 400 (typical) | DATASOURCESYNCINPROGRESS — A sync for this datasource is already running. | 1 |
| [70320](error-codes.md#error-70320) | `USERVARIABLE_VARIABLE_NOT_FOUND` | 400 (typical) | USERVARIABLEVARIABLENOTFOUND — <variable-id> does not exist in this workspace. | 1 |
| [70321](error-codes.md#error-70321) | `USERVARIABLE_VARIABLE_IN_USE` | 400 (typical) | USERVARIABLEVARIABLEINUSE — The variable is currently referenced elsewhere and cannot be deleted. | 1 |
| [70322](error-codes.md#error-70322) | `USERVARIABLE_VARIABLE_IN_USE` | 400 (typical) | USERVARIABLEVARIABLEINUSE (multi-variable form) — One or more of the requested variables are in use. | 1 |
| [70323](error-codes.md#error-70323) | `DUPLICATE_USER_VARIABLE` | 400 (typical) | DUPLICATEUSERVARIABLE — A variable with this name already exists in the workspace. | 2 |
| [70324](error-codes.md#error-70324) | `BLANK_VARIABLE_NAME` | 400 (typical) | BLANKVARIABLENAME — variableName is empty. | 2 |
| [70325](error-codes.md#error-70325) | `INVALID_VAR_NAME` | 400 (typical) | INVALIDVARNAME — The name uses a reserved pattern (system. prefix, ${ prefix, or } suffix). | 2 |
| [70326](error-codes.md#error-70326) | `CANT_DELETE_VARIABLE` | 400 (typical) | CANTDELETEVARIABLE — The variable cannot be deleted by this user (ownership restriction). | 1 |
| [70329](error-codes.md#error-70329) | `CANT_DELETE_VARIABLE`, `UNAUTHORIZED_VAR_ACTION` | 400 (typical) | CANTDELETEVARIABLE (UNAUTHORIZEDVARACTION) — <variable-id> does not exist in this workspace. | 2 |
| [70335](error-codes.md#error-70335) | `VARIABLE_RANGE_NOT_ALLOWED_ON_DT` | 400 (typical) | VARIABLERANGENOTALLOWEDONDT — Range type combined with Text data type. | 2 |
| [70336](error-codes.md#error-70336) | `VARIABLE_DATA_NOT_PRESENT` | 400 (typical) | VARIABLEDATANOTPRESENT — No usable value entries could be derived from the request. | 2 |
| [70337](error-codes.md#error-70337) | `VARIABLE_DEFAULT_VALUE_NOT_PRESENT_IN_LIST` | 400 (typical) | VARIABLEDEFAULTVALUENOTPRESENTINLIST — The defaultValue is not one of the values supplied for a List-type entry. | 2 |
| [70338](error-codes.md#error-70338) | `VARIABLE_RANGE_INSUFFICIENT_DATA`, `VARIABLE_RANGE_EXCESS_DATA` | 400 (typical) | VARIABLERANGEINSUFFICIENTDATA / VARIABLERANGEEXCESSDATA — Range entry is missing a required field or has extra unexpected data. | 2 |
| [70339](error-codes.md#error-70339) | `VARIABLE_RANGE_INSUFFICIENT_DATA`, `VARIABLE_RANGE_EXCESS_DATA` | 400 (typical) | VARIABLERANGEINSUFFICIENTDATA / VARIABLERANGEEXCESSDATA — Range entry is missing a required field or has extra unexpected data. | 2 |
| [70340](error-codes.md#error-70340) | `VARIABLE_RANGE_DEFAULT_VALUE_OUT_OF_RANGE`, `VARIABLE_RANGE_DEF_BW_MINMAX_RANGE` | 400 (typical) | VARIABLERANGEDEFAULTVALUEOUTOFRANGE / VARIABLERANGEDEFBWMINMAXRANGE — The defaultValue falls outside [minValue, maxValue]. | 2 |
| [70341](error-codes.md#error-70341) | `VARIABLE_DUPLICATE_MAIL_ID_OR_GROUP` | 400 (typical) | VARIABLEDUPLICATEMAILIDORGROUP — The same email address appears in more than one userSpecificData entry. | 2 |
| [70342](error-codes.md#error-70342) | `VARIABLE_ALL_VALUES_NO_VARIABLE_DATA` | 400 (typical) | VARIABLEALLVALUESNOVARIABLEDATA — userSpecificData/defaultData were supplied for an All Values-type variable. | 2 |
| [70343](error-codes.md#error-70343) | `VARIABLE_NO_VARIABLE_DATA_PRESENT` | 400 (typical) | VARIABLENOVARIABLEDATAPRESENT — defaultData is missing for a List or Range-type variable. | 2 |
| [70348](error-codes.md#error-70348) | `VARIABLE_EMAIL_NOT_PRESENT` | 400 (typical) | VARIABLEEMAILNOTPRESENT — A userSpecificData entry has an empty emailIds array. | 2 |
| [70350](error-codes.md#error-70350) | `VARIABLE_INVALID_VARTYPE` | 400 (typical) | VARIABLEINVALIDVARTYPE — variableType is not one of 0, 1, or 3. | 2 |
| [70351](error-codes.md#error-70351) | `VARIABLE_INVALID_DATATYPE` | 400 (typical) | VARIABLEINVALIDDATATYPE — variableDataType is not one of the six supported values. | 2 |
| [70352](error-codes.md#error-70352) | `VARIABLE_RANGE_MIN_LESS_THAN_MAX` | 400 (typical) | VARIABLERANGEMINLESSTHANMAX — minValue is not less than maxValue. | 2 |
| [70353](error-codes.md#error-70353) | `VARIABLE_RANGE_INCR_LESSTHAN_RANGESIZE` | 400 (typical) | VARIABLERANGEINCRLESSTHANRANGESIZE — stepSize is larger than the range span. | 2 |
| [70354](error-codes.md#error-70354) | `VARIABLE_RANGE_INCR_ZERO_ERR` | 400 (typical) | VARIABLERANGEINCRZEROERR — stepSize is zero. | 2 |
| [70355](error-codes.md#error-70355) | `VARIABLE_RANGE_INCR_DIV_EQUALLY_ERR` | 400 (typical) | VARIABLERANGEINCRDIVEQUALLYERR — stepSize does not evenly divide the range span. | 2 |
| [70356](error-codes.md#error-70356) | `VARIABLE_RANGE_DEFAULT_VALUE_OUT_OF_RANGE`, `VARIABLE_RANGE_DEF_BW_MINMAX_RANGE` | 400 (typical) | VARIABLERANGEDEFAULTVALUEOUTOFRANGE / VARIABLERANGEDEFBWMINMAXRANGE — The defaultValue falls outside [minValue, maxValue]. | 2 |
| [70357](error-codes.md#error-70357) | `USERVARIABLE_VARIABLE_CANNOT_BE_DELETED` | 400 (typical) | USERVARIABLEVARIABLECANNOTBEDELETED — Deletion blocked due to unresolved references. | 1 |
| [70358](error-codes.md#error-70358) | `VARIABLE_CANNOT_BE_UPDATED` | 400 (typical) | VARIABLECANNOTBEUPDATED — The requested type/data type change conflicts with existing formula/report references to this variable. | 1 |
| [101021](error-codes.md#error-101021) | `NOT_A_STREAM_TABLE` | 400 (typical) | NOTASTREAMTABLE — Row operations are not supported on a stream table. | 2 |
| [19000048](error-codes.md#error-19000048) | `CONN_SYNCNOW_CNT_EXCEEDED` | 400 (observed) | Server message: "You have exceeded the maximum number of manual syncs allowed for this connection." | 0 |
| [21000003](error-codes.md#error-21000003) | `ANALYSISNAME_DUPLICATED` | 400 (observed) | Server message: "A similar analysis named PricePredictionAnalysis already exists in this workspace. Please choose a different name." | 0 |
| [21000009](error-codes.md#error-21000009) | `ANALYSIS_NOT_BELONGS_TO_DB` | 400 (observed) | Server message: "The given analysis does not belong to this workspace." | 0 |
| [21000010](error-codes.md#error-21000010) | `MODEL_NOT_BELONGS_TO_ANALYSIS` | 400 (observed) | Server message: "The given model does not belong to this analysis." | 0 |
| [21000012](error-codes.md#error-21000012) | `DEPLOYMENT_NOT_BELONGS_TO_ANALYSIS` | 400 (observed) | Server message: "The given deployment does not belong to this analysis." | 0 |
| [21000014](error-codes.md#error-21000014) | `AUTOML_NOT_ENABLED` | 400 (observed) | Server message: "The AutoML Feature is not enabled. Please enable the features from Org Settings > Feature Controls > DSML." | 0 |
| [21000016](error-codes.md#error-21000016) | `INVALID_ALGORITHM` | 400 (observed) | Server message: "supportVectorRegression is not a valid algorithm. Please choose a supported algorithm." | 0 |
| [21000043](error-codes.md#error-21000043) | `MODEL_TRAINING_INPROGRESS` | 400 (observed) | Server message: "Training in progress for the model.Please try again once training is completed." | 0 |
| [21000050](error-codes.md#error-21000050) | `FEATURE_MISSING_IN_WHATIF` | 400 (observed) | Server message: "One or more features used in training the model is missing in the input.Please ensure that all features used in training are included." | 0 |
| [21000051](error-codes.md#error-21000051) | `MODEL_ALREADY_DEPLOYED` | 400 (observed) | Server message: "A deployment already exists for this model." | 0 |
