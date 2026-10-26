using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace ZohoAnalytics
{
    /// <exclude></exclude>
    public interface IAnalyticsClient
    {
        void SetAnalyticsServerURL(string serverUrl);
        void SetAccountsServerURL(string serverUrl);
        int GetConnectionTimeout();
        void SetConnectionTimeout(int timeout);
        int GetReadTimeout();
        void SetReadTimeout(int timeout);
        void SetProxy(string proxyHost, int proxyPort, string proxyUsername, string proxyPassword);
        IOrgAPI GetOrgInstance(long orgId);
        IWorkspaceAPI GetWorkspaceInstance(long orgId, long workspaceId);
        IViewAPI GetViewInstance(long orgId, long workspaceId, long viewId);
        IBulkAPI GetBulkInstance(long orgId, long workspaceId);
        JsonElement GetOrgs();
        JsonElement GetWorkspaces();
        JsonElement GetOwnedWorkspaces();
        JsonElement GetSharedWorkspaces();
        JsonElement GetRecentViews();
        JsonElement GetDashboards();
        JsonElement GetOwnedDashboards();
        JsonElement GetSharedDashboards();
        JsonElement GetWorkspaceDetails(long workspaceId);
        JsonElement GetViewDetails(long viewId, Dictionary<string, object> config);
    }

    /// <exclude></exclude>
    public interface IOrgAPI
    {
        long CreateWorkspace(string workspaceName, Dictionary<string, object> config);
        JsonElement GetAdmins();
        JsonElement GetUsers();
        void AddUsers(List<string> emailIds, Dictionary<string, object> config);
        void RemoveUsers(List<string> emailIds, Dictionary<string, object> config);
        void ActivateUsers(List<string> emailIds, Dictionary<string, object> config);
        void DeactivateUsers(List<string> emailIds, Dictionary<string, object> config);
        void ChangeUserRole(List<string> emailIds, string role, Dictionary<string, object> config);
        JsonElement GetMetaDetails(string workspaceName, string viewName);
        JsonElement GetSubscriptionDetails();
        JsonElement GetResourceDetails();
        JsonElement GetAutomlAnalysis();
        JsonElement GetCustomRoles();
        long CreateCustomRole(string roleName, string accessType, Dictionary<string, object> permissions, Dictionary<string, object> config);
        void UpdateCustomRole(long roleId, string roleName, string accessType, Dictionary<string, object> permissions, Dictionary<string, object> config);
        void DeleteCustomRole(long roleId);
        JsonElement GetOrgAccessRestrictions();
        void UpdateOrgAccessRestrictions(Dictionary<string, object> config);
        JsonElement GetLinkedWorkspaces();

    }

    /// <exclude></exclude>
    public interface IWorkspaceAPI
    {
        void Rename(string workspaceName, Dictionary<string, object> config);
        void Delete();
        string GetSecretKey(Dictionary<string, object> config);
        long Copy(string newWorkspaceName, Dictionary<string, object> config, long? destOrgId);
        void AddFavorite();
        void RemoveFavorite();
        void AddDefault();
        void RemoveDefault();
        void EnableDomainAccess();
        void DisableDomainAccess();
        JsonElement GetViews(Dictionary<string, object> config);
        long CreateTable(Dictionary<string, object> tableDesign);
        JsonElement CopyViews(List<long> viewIds, long destWorkspaceId, Dictionary<string, object> config, long? destOrgId);
        JsonElement GetFolders();
        long CreateFolder(string folderName, Dictionary<string, object> config);
        void RenameFolder(long folderId, string folderName, Dictionary<string, object> config);
        void DeleteFolder(long folderId);
        JsonElement GetGroups();
        JsonElement GetGroupDetails(long groupId);
        long CreateGroup(string groupName, List<string> emailIds, Dictionary<string, object> config);
        void RenameGroup(long groupId, string groupName, Dictionary<string, object> config);
        void AddGroupMembers(long groupId, List<string> emailIds, Dictionary<string, object> config);
        void RemoveGroupMembers(long groupId, List<string> emailIds, Dictionary<string, object> config);
        void DeleteGroup(long groupId);
        JsonElement GetAdmins();
        void AddAdmins(List<string> emailIds, Dictionary<string, object> config);
        void RemoveAdmins(List<string> emailIds, Dictionary<string, object> config);
        JsonElement GetShareInfo();
        void ShareViews(List<long> viewIds, List<string> emailIds, Dictionary<string, bool> permissions, Dictionary<string, object> config);
        void RemoveShare(List<long> viewIds, List<string> emailIds, Dictionary<string, object> config);
        JsonElement GetSharedDetailsForViews(List<long> viewIds);
        JsonElement GetSlideshows();
        JsonElement GetSlideshowDetails(long slideId);
        string GetSlideshowURL(long slideId, Dictionary<string, object> config);
        long CreateSlideshow(string slideName, List<long> viewIds, Dictionary<string, object> config);
        void UpdateSlideshow(long slideId, Dictionary<string, object> config);
        void DeleteSlideshow(long slideId);
        long CreateVariable(string variableName, int variableDataType, int variableType, Dictionary<string, object> config);
        void UpdateVariable(long variableId, string variableName, int variableDataType, int variableType, Dictionary<string, object> config);
        void DeleteVariable(long variableId);
        JsonElement GetVariables();
        JsonElement GetVariableDetails(long variableId);
        void MakeDefaultFolder(long folderId);
        JsonElement GetDatasources();
        void SyncData(long datasourceId, Dictionary<string, object> config);
        void UpdateDatasourceConnection(long datasourceId, Dictionary<string, object> config);
        JsonElement GetTrashViews();
        void RestoreTrashView(long viewId, Dictionary<string, object> config);
        void DeleteTrashView(long viewId, Dictionary<string, object> config);
        void ChangeFolderHierarchy(long folderId, int hierarchy, Dictionary<string, object> config);
        void ChangeFolderPosition(long folderId, long referenceFolderId, Dictionary<string, object> config);
        void MoveViewsToFolder(long folderId, List<long> viewIds, Dictionary<string, object> config);
        JsonElement GetWorkspaceUsers();
        void AddWorkspaceUsers(List<string> emailIds, string role, Dictionary<string, object> config);
        void RemoveWorkspaceUsers(List<string> emailIds, Dictionary<string, object> config);
        void ChangeWorkspaceUserStatus(List<string> emailIds, string operation, Dictionary<string, object> config);
        void ChangeWorkspaceUserRole(List<string> emailIds, string role, Dictionary<string, object> config);
        long CreateQueryTable(string sqlQuery, string queryTableName, Dictionary<string, object> config);
        JsonElement GetQueryTables(Dictionary<string, object> config);
        void EditQueryTable(long viewId, string sqlQuery, Dictionary<string, object> config);
        void ExportAsTemplate(List<long> viewIds, string filePath, Dictionary<string, object> config);
        JsonElement GetEmailSchedules();
        long CreateEmailSchedule(string scheduleName, List<long> viewIds, string format, List<string> emailIds, Dictionary<string, object> scheduleDetails, Dictionary<string, object> config);
        long UpdateEmailSchedule(long scheduleId, Dictionary<string, object> config);
        void DeleteEmailSchedule(long scheduleId);
        void TriggerEmailSchedule(long scheduleId);
        void ChangeEmailScheduleStatus(long scheduleId, string operation);
        JsonElement GetAggregateFormulas(Dictionary<string, object> config);
        JsonElement GetAggregateFormulaDependents(long formulaId);
        string GetAggregateFormulaValue(long formulaId);
        long CreateReport(Dictionary<string, object> config);
        void UpdateReport(long viewId, Dictionary<string, object> config);
        JsonElement GetQueryTableDetails(long queryTableId);
        JsonElement GetAutomlAnalysis();
        JsonElement GetAutomlAnalysisDetails(long analysisId);
        JsonElement GetDeploymentDetails(long analysisId, long modelId);
        long CreateAutomlAnalysis(
            string name,
            long trainingTableId,
            string predictionType,
            List<string> features,
            int serverOption,
            Dictionary<string, object> algorithms,
            Dictionary<string, object> config);
        void DeleteAutomlAnalysis(long analysisId, Dictionary<string, object> config);
        void DeleteAutomlAnalysisModel(
            long analysisId,
            long modelId,
            Dictionary<string, object> config);
        JsonElement CreateAutomlAnalysisDeployment(
            long analysisId,
            long modelId,
            long inputTableId,
            string outputTable,
            List<string> outputColumns,
            string predictionColumn,
            int serverOption,
            string importType,
            Dictionary<string, object> scheduleDetails,
            Dictionary<string, object> config);
        void DeployAutomlAnalysis(
            long analysisId,
            long deploymentId,
            Dictionary<string, object> config);
        void DeleteAutomlAnalysisDeployment(
            long analysisId,
            long deploymentId,
            Dictionary<string, object> config);
        JsonElement AutomlAnalysisPrediction(
            long analysisId,
            long modelId,
            Dictionary<string, object> features,
            Dictionary<string, object> config);
        JsonElement GetTags();
        string CreateTag(string tagName, string colorCode, Dictionary<string, object> config);
        void UpdateTag(long tagId, Dictionary<string, object> config);
        void DeleteTag(long tagId);
        void AddTagToViews(long tagId, List<long> viewIds, Dictionary<string, object> config);
        void RemoveTagFromViews(long tagId, List<long> viewIds, bool dissociateAll, Dictionary<string, object> config);
        JsonElement GetTaggedViews(long tagId);

        JsonElement GetLinkedWorkspaces();
        JsonElement GetLinkableWorkspaces();
        JsonElement GetWorkspaceLinkingCompatibility(List<Dictionary<string, object>> clients, Dictionary<string, object> config);
        void LinkWorkspaces(List<Dictionary<string, object>> clients, Dictionary<string, object> config);
        void UnlinkWorkspaces(string scope, Dictionary<string, object> config);
        void SyncLinkedWorkspaces(string scope, Dictionary<string, object> config);
        JsonElement GetLinkedWorkspaceSyncDetails(List<long> sandboxIds, Dictionary<string, object> config);
        JsonElement GetWorkspaceBackups();
        JsonElement BackupWorkspaceNow(Dictionary<string, object> config);
        JsonElement GetWorkspaceBackupStatus(long backupId);
        void DownloadWorkspaceBackup(long backupId, string filePath, Dictionary<string, object> config);
        JsonElement RestoreWorkspaceFromBackup(long backupId, bool confirmRestore, Dictionary<string, object> config);
        JsonElement GetWorkspaceRestoreStatus(long restoreId);
        long CreateDashboard(string displayName, string layout, Dictionary<string, object> config);
        void UpdateDashboard(long dashboardId, Dictionary<string, object> config);
        JsonElement GetDashboardMetadata(long dashboardId, Dictionary<string, object> config);
        JsonElement GetReportMetadata(long viewId);
        JsonElement GetAlertsInWorkspace();
        JsonElement GetAlertConfiguration(long alertId);
        void UpdateAlert(long alertId, string alertName, Dictionary<string, object> scheduleDetails, List<Dictionary<string, object>> rules, Dictionary<string, object> config);
        void DeleteAlerts(List<long> alertIds, Dictionary<string, object> config);
        void ChangeAlertStatus(List<long> alertIds, bool enabled, Dictionary<string, object> config);
        void RunAlert(long alertId, Dictionary<string, object> config);
        JsonElement GetAlertEvents(long alertId, Dictionary<string, object> config);
        JsonElement GetWorkspaceAccessRestrictions();
        void UpdateWorkspaceAccessRestrictions(Dictionary<string, object> config);

    }


    /// <exclude></exclude>
    public interface IViewAPI
    {
        JsonElement AddRow(Dictionary<string, string> columnValues, Dictionary<string, object> config);
        JsonElement UpdateRow(Dictionary<string, string> columnValues, string criteria, Dictionary<string, object> config);
        int DeleteRow(string criteria, Dictionary<string, object> config);
        void Rename(string newViewName, Dictionary<string, object> config);
        void Delete(Dictionary<string, object> config);
        long SaveAs(string newViewName, Dictionary<string, object> config);
        void CreateSimilarViews(long refViewId, long folderId, Dictionary<string, object> config);
        void AutoAnalyse(Dictionary<string, object> config);
        void AddFavorite();
        void RemoveFavorite();
        string GetViewURL(Dictionary<string, object> config);
        string GetEmbedURL(Dictionary<string, object> config);
        string GetPrivateURL(Dictionary<string, object> config);
        string CreatePrivateURL(Dictionary<string, object> config);
        void RemovePrivateAccess();
        string MakeViewPublic(Dictionary<string, object> config);
        void RemovePublicAccess();
        JsonElement GetPublishConfigurations();
        void UpdatePublishConfigurations(Dictionary<string, object> config);
        JsonElement GetMyPermissions();
        long AddColumn(string columnName, string dataType, Dictionary<string, object> config);
        void RenameColumn(long columnId, string columnName);
        void DeleteColumn(long columnId, Dictionary<string, object> config);
        void AddLookup(long columnId, long refViewId, long refColumnId, Dictionary<string, object> config);
        void RemoveLookup(long columnId, Dictionary<string, object> config);
        void HideColumns(List<long> columnIds);
        void ShowColumns(List<long> columnIds);
        void AutoAnalyseColumn(long columnId, Dictionary<string, object> config);
        void CopyFormulas(List<string> formulaNames, long destWorkspaceId, Dictionary<string, object> config, long? destOrgId);
        void RefetchData(Dictionary<string, object> config);
        JsonElement GetLastImportDetails();
        JsonElement GetFormulaColumns();
        long AddFormulaColumn(string formulaName, string expression, Dictionary<string, object> config);
        void EditFormulaColumn(long formulaId, string expression, Dictionary<string, object> config);
        void DeleteFormulaColumn(long formulaId, Dictionary<string, object> config);
        JsonElement GetAggregateFormulas();
        long AddAggregateFormula(string formulaName, string expression, Dictionary<string, object> config);
        void EditAggregateFormula(long formulaId, string expression, Dictionary<string, object> config);
        void DeleteAggregateFormula(long formulaId, Dictionary<string, object> config);
        JsonElement GetViewDependents();
        JsonElement GetColumnDependents(long columnId);
        void UpdateSharedDetails(Dictionary<string, object> config);
        JsonElement GetTableMetadata();
        void ReorderColumns(List<long> columnIds, Dictionary<string, object> config);
        void SortDataByColumns(List<long> columns, int? sortOrder, bool resetSort, Dictionary<string, object> config);
        JsonElement GetViewTags();
        void AddTagsToView(List<long> tagIds, Dictionary<string, object> config);
        void RemoveTagsFromView(List<long> tagIds, bool dissociateAll, Dictionary<string, object> config);
        JsonElement GetAlertsInView();
        long CreateAlert(string alertName, Dictionary<string, object> scheduleDetails, List<Dictionary<string, object>> rules, Dictionary<string, object> config);
        JsonElement GetViewMetadataForAlert();

    }

    /// <exclude></exclude>
    public interface IBulkAPI
    {
        JsonElement ImportDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config);
        JsonElement ImportRawDataInNewTable(string tableName, string fileType, bool autoIdentify, string rawData, Dictionary<string, object> config);
        JsonElement ImportData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config);
        JsonElement ImportRawData(long viewId, string importType, string fileType, bool autoIdentify, string rawData, Dictionary<string, object> config);
        long ImportBulkDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config);
        long ImportBulkData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config);
        long ImportBulkDataInNewTableAsBatches(string tableName, bool autoIdentify, string filePath, int batchSize, Dictionary<string, object> config);
        long ImportBulkDataAsBatches(long viewId, string importType, bool autoIdentify, string filePath, int batchSize, Dictionary<string, object> config);
        JsonElement GetImportJobDetails(long jobId);
        void ExportData(long viewId, string responseFormat, string filePath, Dictionary<string, object> config);
        Stream ExportData(long viewId, string responseFormat, Dictionary<string, object> config);
        long InitiateBulkExport(long viewId, string responseFormat, Dictionary<string, object> config);
        long InitiateBulkExportUsingSQL(string sqlQuery, string responseFormat, Dictionary<string, object> config);
        JsonElement GetExportJobDetails(long jobId);
        void ExportBulkData(long jobId, string filePath);
        Stream ExportBulkData(long jobId);
    }
}
