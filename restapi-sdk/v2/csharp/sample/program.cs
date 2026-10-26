using System.Diagnostics;


using System;
using System.Collections.Generic;
using ZohoAnalytics;
using System.Text.Json;

namespace AnalyticsSample
{
    class Program
    {
        long orgId = 47332811;
        long workspaceId = 4206000000061012;
        long viewId = 4206000000073010;




        public void AddRow(IAnalyticsClient ac)
        {
            Dictionary<string, string> columnValues = new Dictionary<string, string>();
            columnValues.Add("Region", "East");
            columnValues.Add("Product", "Test");
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement response = view.AddRow(columnValues, null);
            Console.WriteLine(response);
        }


        public void UpdateRow(IAnalyticsClient ac)
        {
            Dictionary<string, string> columnValues = new Dictionary<string, string>();
            columnValues.Add("Product", "Test");
            string criteria = "\"Region\"='East'";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement response = view.UpdateRow(columnValues, criteria, null);
            Console.WriteLine(response);
        }


        public void DeleteRow(IAnalyticsClient ac)
        {
            string criteria = "\"Region\"='East'";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            int deletedRowCount = view.DeleteRow(criteria, null);
            Console.WriteLine(deletedRowCount);
        }


        public void ImportDataInNewTable(IAnalyticsClient ac)
        {
            string tableName = "c#_nov17";
            string fileType = "csv";
            bool autoIdentify = true;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable_Export_nov_23.csv";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement importResult = data.ImportDataInNewTable(tableName, fileType, autoIdentify, filePath, null);
            Console.WriteLine(importResult);
        }


        public void ImportData(IAnalyticsClient ac)
        {
            string importType = "append";
            string fileType = "csv";
            bool autoIdentify = true;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable_Export_nov_23.csv";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement importResult = data.ImportData(viewId, importType, fileType, autoIdentify, filePath, null);
            Console.WriteLine(importResult);
        }

        public void ImportRawDataInNewTable(IAnalyticsClient ac)
        {
            string tableName = "c#_v2 RawData";
            string fileType = "json";
            bool autoIdentify = true;
            string rawData = "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement importResult = data.ImportRawDataInNewTable(tableName, fileType, autoIdentify, rawData, null);
            Console.WriteLine(importResult);
        }

        public void ImportRawData(IAnalyticsClient ac)
        {
            string importType = "append";
            string fileType = "json";
            bool autoIdentify = true;
            string rawData = "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement importResult = data.ImportRawData(viewId, importType, fileType, autoIdentify, rawData, null);
            Console.WriteLine(importResult);
        }


        public void ImportBulkDataInNewTable(IAnalyticsClient ac)
        {
            string tableName = "c#_v2_nov_17_3";
            string fileType = "csv";
            bool autoIdentify = true;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable_Export_nov_23.csv";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.ImportBulkDataInNewTable(tableName, fileType, autoIdentify, filePath, null);
            Console.WriteLine(jobId);
        }


        public void ImportBulkData(IAnalyticsClient ac)
        {
            string importType = "append";
            string fileType = "json";
            bool autoIdentify = true;
            string filePath = "D:\\sales_v2.json";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.ImportBulkData(viewId, importType, fileType, autoIdentify, filePath, null);
            Console.WriteLine(jobId);
        }


        public void GetImportJobDetails(IAnalyticsClient ac)
        {
            long jobId = 1767024000009297003;
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement jobInfo = data.GetImportJobDetails(jobId);
            Console.WriteLine(jobInfo);
        }


        public void ImportBulkDataInNewTableAsBatches(IAnalyticsClient ac)
        {
            string tableName = "c_v2_batch_Sep_123";
            bool autoIdentify = true;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable.csv";
            int batchSize = 5000;
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.ImportBulkDataInNewTableAsBatches(tableName, autoIdentify, filePath, batchSize, null);
            Console.WriteLine(jobId);
        }


        public void ImportBulkDataAsBatches(IAnalyticsClient ac)
        {
            string importType = "append";
            bool autoIdentify = true;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable.csv";
            int batchSize = 5000;
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.ImportBulkDataAsBatches(viewId, importType, autoIdentify, filePath, batchSize, null);
            Console.WriteLine(jobId);
        }


        public void ExportData(IAnalyticsClient ac)
        {
            string responseFormat = "csv";
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable_Export_nov_23.csv";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            data.ExportData(viewId, responseFormat, filePath, null);
            Console.WriteLine("success");
        }

        public void ExportDataAsStream(IAnalyticsClient ac)
        {
            string responseFormat = "csv";
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            Stream responseStream = null;
            StreamReader reader = null;
            try
            {
                responseStream = bulk.ExportData(viewId, responseFormat, null);
                reader = new StreamReader(responseStream);

                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    Console.WriteLine(line);
                }
            }
            finally
            {
                reader?.Close();
                responseStream?.Close();
            }
        }

        public void InitiateBulkExport(IAnalyticsClient ac)
        {
            string responseFormat = "pdf";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.InitiateBulkExport(viewId, responseFormat, null);
            Console.WriteLine(jobId);
        }


        public void InitiateBulkExportUsingSQL(IAnalyticsClient ac)
        {
            string responseFormat = "pdf";
            String sqlQuery = "select * from Sales";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = data.InitiateBulkExportUsingSQL(sqlQuery, responseFormat, null);
            Console.WriteLine(jobId);
        }


        public void GetExportJobDetails(IAnalyticsClient ac)
        {
            long jobId = 1767024000009298001;
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement jobInfo = data.GetExportJobDetails(jobId);
            Console.WriteLine(jobInfo);
        }

        public void ExportBulkData(IAnalyticsClient ac)
        {
            long jobId = 1767024000009293160;
            string filePath = "C:\\Users\\Administrator\\Downloads\\SalesTable_Export_nov_23.pdf";
            IBulkAPI data = ac.GetBulkInstance(orgId, workspaceId);
            data.ExportBulkData(jobId, filePath);
            Console.WriteLine("success");
        }

        public void ExportBulkDataAsStream(IAnalyticsClient ac)
        {
            long jobId = 1767024000009298001;
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            Stream responseStream = null;
            StreamReader reader = null;
            try
            {
                responseStream = bulk.ExportBulkData(jobId);
                reader = new StreamReader(responseStream);

                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    Console.WriteLine(line);
                }
            }
            finally
            {
                reader?.Close();
                responseStream?.Close();
            }
        }


        public void CreateWorkspace(IAnalyticsClient ac)
        {
            string workspaceName = "Delete";
            IOrgAPI org = ac.GetOrgInstance(orgId);
            long workspaceId = org.CreateWorkspace(workspaceName, null);
            Console.WriteLine(workspaceId);
        }


        public void CopyWorkspace(IAnalyticsClient ac)
        {
            string newWorkspaceName = "C# Lib Copy";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long newWorkspaceId = ws.Copy(newWorkspaceName, null, null);
            Console.WriteLine(newWorkspaceId);
        }

        public void DeleteWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.Delete();
            Console.WriteLine("success");
        }

        public void RenameWorkspace(IAnalyticsClient ac)
        {
            string newWorkspaceName = "Renamed C# Lib";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.Rename(newWorkspaceName, null);
            Console.WriteLine("success");
        }

        public void CreateTable(IAnalyticsClient ac)
        {
            Dictionary<string, object> tableDesign = new Dictionary<string, object>();
            tableDesign.Add("TABLENAME", "Test C#");
            tableDesign.Add("TABLEDESCRIPTION", "Test C# Desc");
            List<Dictionary<string, object>> columns = new List<Dictionary<string, object>>();
            Dictionary<string, object> column1 = new Dictionary<string, object>();
            column1.Add("COLUMNNAME", "Col1");
            column1.Add("DATATYPE", "PLAIN");
            Dictionary<string, object> column2 = new Dictionary<string, object>();
            column2.Add("COLUMNNAME", "Col2");
            column2.Add("DATATYPE", "NUMBER");
            columns.Add(column1);
            columns.Add(column2);
            tableDesign.Add("COLUMNS", columns);

            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long viewId = ws.CreateTable(tableDesign);
            Console.WriteLine(viewId);
        }

        public void SaveAsView(IAnalyticsClient ac)
        {
            string newViewName = "Saveas table";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long destViewId = view.SaveAs(newViewName, null);
            Console.WriteLine(destViewId);
        }

        public void RenameView(IAnalyticsClient ac)
        {
            string newViewName = "Renamed table";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.Rename(newViewName, null);
            Console.WriteLine("success");
        }

        public void DeleteView(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.Delete(null);
            Console.WriteLine("success");
        }

        public void RestoreTrashView(IAnalyticsClient ac)
        {
            long viewId = 1148746000002545001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RestoreTrashView(viewId, null);
            Console.WriteLine("success");
        }

        public void DeleteTrashView(IAnalyticsClient ac)
        {
            long viewId = 1148746000002545001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.DeleteTrashView(viewId, null);
            Console.WriteLine("success");
        }

        public void CreateFolder(IAnalyticsClient ac)
        {
            string folderName = "Test folder";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long folderId = ws.CreateFolder(folderName, null);
            Console.WriteLine(folderId);
        }

        public void RenameFolder(IAnalyticsClient ac)
        {
            long folderId = 1148746000002559043;
            string folderName = "Renamed folder";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RenameFolder(folderId, folderName, null);
            Console.WriteLine("success");
        }

        public void MakeDefaultFolder(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long folderId = 1148746000002545001;
            workspace.MakeDefaultFolder(folderId);
            Console.WriteLine("success");
        }

        public void DeleteFolder(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long folderId = 1148746000002559043;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.DeleteFolder(folderId);
            Console.WriteLine("success");
        }

        public void AddColumn(IAnalyticsClient ac)
        {
            string columnName = "Add col";
            string dataType = "PLAIN";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long columnId = view.AddColumn(columnName, dataType, null);
            Console.WriteLine(columnId);
        }

        public void RenameColumn(IAnalyticsClient ac)
        {
            long columnId = 1148746000002557002;
            string columnName = "Renamed column";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RenameColumn(columnId, columnName);
            Console.WriteLine("success");
        }

        public void DeleteColumn(IAnalyticsClient ac)
        {
            long columnId = 1148746000002557002;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.DeleteColumn(columnId, null);
            Console.WriteLine("success");
        }

        public void AddLookup(IAnalyticsClient ac)
        {
            long columnId = 1148746000002449006;
            long refViewId = 1148746000002449089;
            long refColumnId = 1148746000002449094;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AddLookup(columnId, refViewId, refColumnId, null);
            Console.WriteLine("success");
        }

        public void RemoveLookup(IAnalyticsClient ac)
        {
            long columnId = 1148746000002449006;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemoveLookup(columnId, null);
            Console.WriteLine("success");
        }

        public void HideColumns(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002449002;
            List<long> columnIds = new List<long>();
            columnIds.Add(1148746000002449006);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.HideColumns(columnIds);
            Console.WriteLine("success");
        }

        public void ShowColumns(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002449002;
            List<long> columnIds = new List<long>();
            columnIds.Add(1148746000002449006);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.ShowColumns(columnIds);
            Console.WriteLine("success");
        }


        public void CopyViews(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002457001);
            long destWorkspaceId = 1148746000002556007;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.CopyViews(viewIds, destWorkspaceId, null, null);
            Console.WriteLine(views);
        }

        public void CopyFormulas(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002449002;
            List<string> formulaNames = new List<string>();
            formulaNames.Add("F1");
            long destWorkspaceId = 1148746000002556007;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.CopyFormulas(formulaNames, destWorkspaceId, null, null);
            Console.WriteLine("success");
        }

        public void CreateSimilarViews(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002449089;
            long refViewId = 1148746000002449002;
            long folderId = 1148746000002508116;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.CreateSimilarViews(refViewId, folderId, null);
            Console.WriteLine("success");
        }

        public void AutoAnalyseView(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002553005;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AutoAnalyse(null);
            Console.WriteLine("success");
        }

        public void AutoAnalyseColumn(IAnalyticsClient ac)
        {
            long workspaceId = 1148746000002449012;
            long viewId = 1148746000002449002;
            long columnId = 1148746000002449006;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AutoAnalyseColumn(columnId, null);
            Console.WriteLine("success");
        }


        public void GetVariables(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement variables = workspace.GetVariables();
            Console.WriteLine(variables);
        }


        public void GetVariableDetails(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long variableId = 1148746000002545001;
            JsonElement variableDetails = workspace.GetVariableDetails(variableId);
            Console.WriteLine(variableDetails);
        }

        public void CreateVariable(IAnalyticsClient ac)
        {
            string variableName = "Variable_1";
            int variableDataType = 1;
            int variableType = 3;

            Dictionary<string, object> format = new Dictionary<string, object>();
            format.Add("alignment", "left");

            List<string> emailIds_1 = new List<string>();
            emailIds_1.Add("user+1@zoho.com");
            emailIds_1.Add("user+2@zoho.com");

            List<string> values_1 = new List<string>();
            values_1.Add("1");
            values_1.Add("2");
            values_1.Add("3");

            Dictionary<string, object> dataset_1 = new Dictionary<string, object>();
            dataset_1.Add("values", values_1);
            dataset_1.Add("emailIds", emailIds_1);

            List<string> emailIds_2 = new List<string>();
            emailIds_2.Add("user+3@zoho.com");
            emailIds_2.Add("user+4@zoho.com");

            List<string> values_2 = new List<string>();
            values_2.Add("4");
            values_2.Add("5");
            values_2.Add("6");

            Dictionary<string, object> dataset_2 = new Dictionary<string, object>();
            dataset_2.Add("values", values_2);
            dataset_2.Add("emailIds", emailIds_2);

            List<object> userSpecificData = new List<object>();
            userSpecificData.Add(dataset_1);
            userSpecificData.Add(dataset_2);

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("format", format);
            config.Add("userSpecificData", userSpecificData);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long variableId = workspace.CreateVariable(variableName, variableDataType, variableType, config);
            Console.WriteLine(variableId);
        }

        public void UpdateVariable(IAnalyticsClient ac)
        {
            long variableId = 1148746000002545001;
            string variableName = "Variable_NEW_1";
            int variableDataType = 1;
            int variableType = 3;

            Dictionary<string, object> format = new Dictionary<string, object>();
            format.Add("alignment", "left");

            List<string> emailIds_1 = new List<string>();
            emailIds_1.Add("user+1@zoho.com");
            emailIds_1.Add("user+2@zoho.com");

            List<string> values_1 = new List<string>();
            values_1.Add("4");
            values_1.Add("5");
            values_1.Add("6");

            Dictionary<string, object> dataset_1 = new Dictionary<string, object>();
            dataset_1.Add("values", values_1);
            dataset_1.Add("emailIds", emailIds_1);

            List<string> emailIds_2 = new List<string>();
            emailIds_2.Add("user+3@zoho.com");
            emailIds_2.Add("user+4@zoho.com");

            List<string> values_2 = new List<string>();
            values_2.Add("1");
            values_2.Add("2");
            values_2.Add("3");

            Dictionary<string, object> dataset_2 = new Dictionary<string, object>();
            dataset_2.Add("values", values_2);
            dataset_2.Add("emailIds", emailIds_2);

            List<object> userSpecificData = new List<object>();
            userSpecificData.Add(dataset_1);
            userSpecificData.Add(dataset_2);

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("format", format);
            config.Add("userSpecificData", userSpecificData);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateVariable(variableId, variableName, variableDataType, variableType, config);
            Console.WriteLine("success");
        }

        public void DeleteVariable(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long variableId = 1148746000002545001;
            workspace.DeleteVariable(variableId);
            Console.WriteLine("success");
        }

        public void GetOrgs(IAnalyticsClient ac)
        {
            JsonElement orgs = ac.GetOrgs();
            Console.WriteLine(orgs.ToString());
        }

        public void GetWorkspaces(IAnalyticsClient ac)
        {
            JsonElement workspaces = ac.GetWorkspaces();
            Console.WriteLine(workspaces);
        }

        public void GetOwnedWorkspaces(IAnalyticsClient ac)
        {
            JsonElement workspaces = ac.GetOwnedWorkspaces();
            Console.WriteLine(workspaces);
        }

        public void GetSharedWorkspaces(IAnalyticsClient ac)
        {
            JsonElement workspaces = ac.GetSharedWorkspaces();
            Console.WriteLine(workspaces);
        }

        public void GetViews(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.GetViews(null);
            Console.WriteLine(views);
        }

        public void GetFolders(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.GetFolders();
            Console.WriteLine(views);
        }

        public void GetRecentViews(IAnalyticsClient ac)
        {
            JsonElement views = ac.GetRecentViews();
            Console.WriteLine(views);
        }

        public void GetTrashViews(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.GetTrashViews();
            Console.WriteLine(views);
        }

        public void GetDashboards(IAnalyticsClient ac)
        {
            JsonElement dashboards = ac.GetDashboards();
            Console.WriteLine(dashboards);
        }

        public void GetOwnedDashboards(IAnalyticsClient ac)
        {
            JsonElement dashboards = ac.GetOwnedDashboards();
            Console.WriteLine(dashboards);
        }

        public void GetSharedDashboards(IAnalyticsClient ac)
        {
            JsonElement dashboards = ac.GetSharedDashboards();
            Console.WriteLine(dashboards);
        }

        public void GetWorkspaceSecretKey(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string views = ws.GetSecretKey(null);
            Console.WriteLine(views);
        }

        public void GetWorkspaceDetails(IAnalyticsClient ac)
        {
            JsonElement workspace = ac.GetWorkspaceDetails(workspaceId);
            Console.WriteLine(workspace);
        }

        public void GetViewDetails(IAnalyticsClient ac)
        {

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("withInvolvedMetaInfo", true);
            JsonElement views = ac.GetViewDetails(viewId, config);
            Console.WriteLine(views);
        }

        public void GetViewDependents(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement views = view.GetViewDependents();
            Console.WriteLine(views);
        }

        public void GetColumnDependents(IAnalyticsClient ac)
        {
            long columnId = 1148746000002557002;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement data = view.GetColumnDependents(columnId);
            Console.WriteLine(data);
        }

        public void AddFavoriteWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.AddFavorite();
            Console.WriteLine("success");
        }

        public void RemoveFavoriteWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveFavorite();
            Console.WriteLine("success");
        }

        public void AddFavoriteView(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AddFavorite();
            Console.WriteLine("success");
        }

        public void RemoveFavoriteView(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemoveFavorite();
            Console.WriteLine("success");
        }

        public void AddDefaultWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.AddDefault();
            Console.WriteLine("success");
        }

        public void RemoveDefaultWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveDefault();
            Console.WriteLine("success");
        }

        public void GetFormulaColumns(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement formulas = view.GetFormulaColumns();
            Console.WriteLine(formulas);
        }

        public void GetAggregateFormulas(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement formulas = view.GetAggregateFormulas();
            Console.WriteLine(formulas);
        }


        public void GetMetaDetails(IAnalyticsClient ac)
        {
            string workspaceName = "API Lib";
            string viewName = "Sales";
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement metaDetails = org.GetMetaDetails(workspaceName, viewName);
            Console.WriteLine(metaDetails);
        }

        public void GetDatasources(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement datasources = workspace.GetDatasources();
            Console.WriteLine(datasources);
        }

        public void SyncData(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long datasourceId = 1148746000002545001;
            workspace.SyncData(datasourceId, null);
            Console.WriteLine("success");
        }

        public void RefetchData(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RefetchData(null);
            Console.WriteLine("success");
        }

        public void UpdateDatasourceConnection(IAnalyticsClient ac)
        {
            long datasourceId = 1148746000002545001;

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("serviceName", "AMAZON RDS");
            config.Add("databaseType", "POSTGRESQL");
            config.Add("hostName", "******");
            config.Add("port", "5432");
            config.Add("userName", "******");
            config.Add("password", "******");
            config.Add("cloudDatabaseName", "sampledb");

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateDatasourceConnection(datasourceId, config);
            Console.WriteLine("success");
        }

        public void GetLastImportDetails(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement importDetails = view.GetLastImportDetails();
            Console.WriteLine(importDetails);
        }

        public void EnableDomainAccess(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.EnableDomainAccess();
            Console.WriteLine("success");
        }

        public void DisableDomainAccess(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.DisableDomainAccess();
            Console.WriteLine("success");
        }

        public void GetOrgAdmins(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement admins = org.GetAdmins();
            Console.WriteLine(admins);
        }

        public void GetWorkspaceAdmins(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.GetAdmins();
            Console.WriteLine(views);
        }

        public void AddWorkspaceAdmins(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+1@zohotest.com");
            ws.AddAdmins(emailIds, null);
            Console.WriteLine("success");
        }

        public void RemoveWorkspaceAdmins(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+1@zohotest.com");
            ws.RemoveAdmins(emailIds, null);
            Console.WriteLine("success");
        }

        public void GetWorkspaceShareInfo(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.GetShareInfo();
            Console.WriteLine(views);
        }

        public void ShareViews(IAnalyticsClient ac)
        {
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002449002);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+1@zohotest.com");
            Dictionary<string, bool> permissions = new Dictionary<string, bool>();
            permissions.Add("read", true);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.ShareViews(viewIds, emailIds, permissions, null);
            Console.WriteLine("success");
        }

        public void RemoveShare(IAnalyticsClient ac)
        {
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002449002);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+1@zohotest.com");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveShare(viewIds, emailIds, null);
            Console.WriteLine("success");
        }

        public void GetMyPermissions(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement views = view.GetMyPermissions();
            Console.WriteLine(views);
        }

        public void GetSharedDetailsForViews(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002449002);
            JsonElement sharedDetails = ws.GetSharedDetailsForViews(viewIds);
            Console.WriteLine(sharedDetails);
        }

        public void GetGroups(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement groups = ws.GetGroups();
            Console.WriteLine(groups);
        }

        public void GetGroupDetails(IAnalyticsClient ac)
        {
            long groupId = 1148746000002556001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement info = ws.GetGroupDetails(groupId);
            Console.WriteLine(info);
        }

        public void CreateGroup(IAnalyticsClient ac)
        {
            string groupName = "API";
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+1@zohotest.com");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long groupId = ws.CreateGroup(groupName, emailIds, null);
            Console.WriteLine(groupId);
        }

        public void RenameGroup(IAnalyticsClient ac)
        {
            long groupId = 1148746000002556001;
            string groupName = "Renamed API";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RenameGroup(groupId, groupName, null);
            Console.WriteLine("success");
        }

        public void AddGroupMembers(IAnalyticsClient ac)
        {
            long groupId = 1148746000002556001;
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+2@zohotest.com");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.AddGroupMembers(groupId, emailIds, null);
            Console.WriteLine("success");
        }

        public void RemoveGroupMembers(IAnalyticsClient ac)
        {
            long groupId = 1148746000002556001;
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar.krishnasamy+2@zohotest.com");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveGroupMembers(groupId, emailIds, null);
            Console.WriteLine("success");
        }

        public void DeleteGroup(IAnalyticsClient ac)
        {
            long groupId = 1148746000002556001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.DeleteGroup(groupId);
            Console.WriteLine("success");
        }

        public void GetViewUrl(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string viewUrl = view.GetViewURL(null);
            Console.WriteLine(viewUrl);
        }

        public void GetEmbedUrl(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string viewUrl = view.GetEmbedURL(null);
            Console.WriteLine(viewUrl);
        }

        public void GetPrivateUrl(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string viewUrl = view.GetPrivateURL(null);
            Console.WriteLine(viewUrl);
        }

        public void CreatePrivateUrl(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string viewUrl = view.CreatePrivateURL(null);
            Console.WriteLine(viewUrl);
        }

        public void RemovePrivateAccess(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemovePrivateAccess();
            Console.WriteLine("success");
        }

        public void MakeViewPublic(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string viewUrl = view.MakeViewPublic(null);
            Console.WriteLine(viewUrl);
        }

        public void RemovePublicAccess(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemovePublicAccess();
            Console.WriteLine("success");
        }

        public void GetPublishConfigurations(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement data = view.GetPublishConfigurations();
            Console.WriteLine(data);
        }

        public void UpdatePublishConfigurations(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("includeTitle", true);
            config.Add("includeDesc", true);
            config.Add("includeToolBar", false);
            config.Add("includeSocialWidgets", false);
            config.Add("includeSearchBox", true);
            config.Add("includeDatatypeSymbol", false);
            config.Add("includeShowHideOption", false);
            config.Add("isInteractive", true);
            config.Add("legendPosition", "RIGHT");
            config.Add("width", 800);
            config.Add("height", 600);
            config.Add("autoRefresh", -1);
            config.Add("URLCriteria", "");
            config.Add("includeAskZia", false);

            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.UpdatePublishConfigurations(config);
            Console.WriteLine("success");
        }

        public void GetSlideshows(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement slideshows = workspace.GetSlideshows();
            Console.WriteLine(slideshows);
        }

        public void GetSlideshowUrl(IAnalyticsClient ac)
        {
            long slideId = 1148746000002545001;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string slideshowUrl = workspace.GetSlideshowURL(slideId, null);
            Console.WriteLine(slideshowUrl);
        }

        public void GetSlideshowDetails(IAnalyticsClient ac)
        {
            long slideId = 114874600000267890;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement slideshowInfo = workspace.GetSlideshowDetails(slideId);
            Console.WriteLine(slideshowInfo);
        }

        public void CreateSlideshow(IAnalyticsClient ac)
        {
            string slideName = "Slideshows 1";
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002449002);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long slideId = workspace.CreateSlideshow(slideName, viewIds, null);
            Console.WriteLine(slideId);
        }

        public void UpdateSlideshow(IAnalyticsClient ac)
        {
            long slideId = 114874600000267890;
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002449002);

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("viewIds", viewIds);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateSlideshow(slideId, config);
        }

        public void DeleteSlideshow(IAnalyticsClient ac)
        {
            long slideId = 114874600000267890;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteSlideshow(slideId);
        }

        public void GetUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement users = org.GetUsers();
            Console.WriteLine(users);
        }

        public void AddUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar+1@zohotest.com");
            org.AddUsers(emailIds, null);
            Console.WriteLine("success");
        }

        public void RemoveUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar+1@zohotest.com");
            org.RemoveUsers(emailIds, null);
            Console.WriteLine("success");
        }

        public void ActivateUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar+1@zohotest.com");
            org.ActivateUsers(emailIds, null);
            Console.WriteLine("success");
        }

        public void DeactivateUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar+1@zohotest.com");
            org.DeactivateUsers(emailIds, null);
            Console.WriteLine("success");
        }

        public void ChangeUserRole(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("vinothkumar+1@zohotest.com");
            string role = "USER";
            org.ChangeUserRole(emailIds, role, null);
        }

        public void GetSubscriptionDetails(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement subscriptionInfo = org.GetSubscriptionDetails();
            Console.WriteLine(subscriptionInfo);
        }

        public void GetResourceDetails(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement resourceInfo = org.GetResourceDetails();
            Console.WriteLine(resourceInfo);
        }

        public void ExportAsTemplate(IAnalyticsClient ac)
        {
            string filePath = "D:\\Workspace_1.atpt";
            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002578004);
            viewIds.Add(1148746000002578002);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ExportAsTemplate(viewIds, filePath, null);
            Console.WriteLine("success");
        }

        public void GetEmailSchedules(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement emailSchedules = workspace.GetEmailSchedules();
            Console.WriteLine(emailSchedules);
        }

        public void CreateEmailSchedule(IAnalyticsClient ac)
        {
            string scheduleName = "Schedule1";
            string format = "CSV";

            List<long> viewIds = new List<long>();
            viewIds.Add(1148746000002578004);
            viewIds.Add(1148746000002578002);

            List<string> emailIds = new List<string>();
            emailIds.Add("user_1@zoho.com");

            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "Daily");
            scheduleDetails.Add("hour", 10);
            scheduleDetails.Add("minute", 30);
            //{"calendarFrequency":"Daily","hour":10, "minute":30}

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("subject", "Daily Sales Report");

            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long scheduleId = ws.CreateEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config);
            Console.WriteLine(scheduleId);
        }

        public void UpdateEmailSchedule(IAnalyticsClient ac)
        {
            long scheduleId = 115674600000150007;

            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "Daily");
            scheduleDetails.Add("hour", 8);
            scheduleDetails.Add("minute", 30);

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("subject", "Daily Sales Overview");
            config.Add("scheduleDetails", scheduleDetails);

            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long newScheduleId = ws.UpdateEmailSchedule(scheduleId, config);
            Console.WriteLine(newScheduleId);
        }


        public void TriggerEmailSchedule(IAnalyticsClient ac)
        {
            long scheduleId = 115674600000150007;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.TriggerEmailSchedule(scheduleId);
        }

        public void ChangeEmailScheduleStatus(IAnalyticsClient ac)
        {
            long scheduleId = 115674600000150007;
            string operation = "activate";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.ChangeEmailScheduleStatus(scheduleId, operation);
        }

        public void DeleteEmailSchedule(IAnalyticsClient ac)
        {
            long scheduleId = 115674600000150007;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.DeleteEmailSchedule(scheduleId);
        }

        public void GetAggregateFormulasInWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement formulas = ws.GetAggregateFormulas(null);
            Console.WriteLine(formulas);
        }

        public void GetAggregateFormulaDependents(IAnalyticsClient ac)
        {
            long formulaId = 376702700009130004;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement dependents = ws.GetAggregateFormulaDependents(formulaId);
            Console.WriteLine(dependents);
        }

        public void GetAggregateFormulaValue(IAnalyticsClient ac)
        {
            long formulaId = 376702700009130004;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string value = ws.GetAggregateFormulaValue(formulaId);
            Console.WriteLine(value);
        }

        public void CreateReport(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("baseTableName", "Sales");
            config.Add("title", "New Chart");
            config.Add("reportType", "chart");

            List<Dictionary<string, object>> axisColumns = new List<Dictionary<string, object>>();

            Dictionary<string, object> xAxis = new Dictionary<string, object>();
            xAxis.Add("type", "xAxis");
            xAxis.Add("columnName", "Date");
            xAxis.Add("operation", "year");

            Dictionary<string, object> yAxis = new Dictionary<string, object>();
            yAxis.Add("type", "yAxis");
            yAxis.Add("columnName", "Sales");
            yAxis.Add("operation", "sum");

            axisColumns.Add(xAxis);
            axisColumns.Add(yAxis);
            config.Add("axisColumns", axisColumns);

            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            long viewId = ws.CreateReport(config);
            Console.WriteLine(viewId);
        }

        public void UpdateReport(IAnalyticsClient ac)
        {
            long viewId = 35130000006291041;

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("reportType", "chart");

            List<Dictionary<string, object>> axisColumns = new List<Dictionary<string, object>>();

            Dictionary<string, object> xAxis = new Dictionary<string, object>();
            xAxis.Add("type", "xAxis");
            xAxis.Add("columnName", "Date");
            xAxis.Add("operation", "year");

            Dictionary<string, object> yAxis = new Dictionary<string, object>();
            yAxis.Add("type", "yAxis");
            yAxis.Add("columnName", "Cost");
            yAxis.Add("operation", "sum");

            axisColumns.Add(xAxis);
            axisColumns.Add(yAxis);
            config.Add("axisColumns", axisColumns);

            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.UpdateReport(viewId, config);
            Console.WriteLine("Success");
        }

        public void GetTableMetadata(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement result = view.GetTableMetadata();
            Console.WriteLine(result.ToString());
        }

        public void ReorderColumns(IAnalyticsClient ac)
        {
            List<long> columnIds = new()
            {
                466206000000069003,
                466206000000073014,
                466206000000073013
            };

            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.ReorderColumns(columnIds, null);

            Console.WriteLine("success");
        }

        public void SortDataByColumns(IAnalyticsClient ac)
        {
            List<long> columnIds = new()
            {
                466206000000069003,
                466206000000073013
            };

            int sortOrder = 2;   // 1 -> ascending, 2 -> descending

            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.SortDataByColumns(columnIds, sortOrder, false, null);

            Console.WriteLine("success");
        }

        public void SortDataByColumnsReset(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);

            view.SortDataByColumns(null, null, true, null);

            Console.WriteLine("success");
        }

        public void GetQueryTableDetails(IAnalyticsClient ac)
        {
            long queryTableId = 466206000000061149;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetQueryTableDetails(queryTableId);

            Console.WriteLine(result.ToString());
        }

        public void GetAutomlAnalysisInOrg(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetAutomlAnalysis();

            Console.WriteLine(result.ToString());
        }


        public void GetAutomlAnalysisInWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAutomlAnalysis();

            Console.WriteLine(result.ToString());
        }

        public void GetAutomlAnalysisDetails(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAutomlAnalysisDetails(analysisId);

            Console.WriteLine(result.ToString());
        }
        public void GetDeploymentDetails(IAnalyticsClient ac)
        {
            long analysisId = 466206000000073001;
            long modelId = 466206000000073003;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetDeploymentDetails(analysisId, modelId);

            Console.WriteLine(result.ToString());
        }

        public void CreateAutomlAnalysis(IAnalyticsClient ac)
        {
            string automlName = "Sales Analysis - CSharp SDK";
            long trainingTableId = 466206000000061002;
            string predictionType = "CLASSIFICATION";

            List<string> features = new List<string>
            {
                "Region",
                "Product Category",
                "Sales"
            };

            int serverOption = 1;

            Dictionary<string, object> algorithms = new Dictionary<string, object>
            {
                {
                    "decisionTreeClassification",
                    new Dictionary<string, object>
                    {
                        { "minimumSampleSplit", "2" },
                        { "maximumDepth", "100" }
                    }
                },
                {
                    "randomForestClassification",
                    new Dictionary<string, object>
                    {
                        { "minimumSampleSplit", "2" },
                        { "maximumDepth", "100" },
                        { "numberOfTrees", "25" }
                    }
                }
            };

            Dictionary<string, object> config = new Dictionary<string, object>
            {
                { "description", "Sales Table Analysis..." },
                { "targetColumn", "Product" }
            };

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);

            long automlId = workspace.CreateAutomlAnalysis(
                automlName,
                trainingTableId,
                predictionType,
                features,
                serverOption,
                algorithms,
                config
            );

            Console.WriteLine("Created AutoML Analysis ID: " + automlId);
        }

        public void DeleteAutomlAnalysis(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAutomlAnalysis(analysisId, null);

            Console.WriteLine("AutoML Analysis deleted successfully.");
        }

        public void DeleteAutomlAnalysisModel(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;
            long modelId = 466206000000197003;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAutomlAnalysisModel(analysisId, modelId, null);

            Console.WriteLine("Model deleted successfully.");
        }

        public void CreateAutomlDeployment(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;
            long modelId = 466206000000197003;
            long inputTableId = 466206000000061002;
            string outputTable = "SalesDep";
            string predictionColumn = "precol";
            int serverOption = 1;
            string importType = "APPEND";

            List<string> outputColumns = new List<string>
            {
                "Sales",
                "Region"
            };

            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>
            {
                { "calendarFrequency", "hourly" },
                { "interval", 3 }
            };

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);

            JsonElement deploymentInfo =
                workspace.CreateAutomlAnalysisDeployment(
                    analysisId,
                    modelId,
                    inputTableId,
                    outputTable,
                    outputColumns,
                    predictionColumn,
                    serverOption,
                    importType,
                    scheduleDetails,
                    null
                );

            Console.WriteLine(deploymentInfo.ToString());
        }

        public void DeployAutomlAnalysis(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;
            long deploymentId = 466206000000198109;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeployAutomlAnalysis(analysisId, deploymentId, null);

            Console.WriteLine("Deployment triggered successfully.");
        }

        public void DeleteAutomlAnalysisDeployment(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;
            long deploymentId = 466206000000198109;

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAutomlAnalysisDeployment(analysisId, deploymentId, null);

            Console.WriteLine("Deployment deleted successfully.");
        }

        public void AutomlAnalysisPrediction(IAnalyticsClient ac)
        {
            long analysisId = 466206000000197001;
            long modelId = 466206000000197003;

            Dictionary<string, object> features = new Dictionary<string, object>
            {
                { "Sales", 1000 },
                { "Region", "East" },
                { "Product Category", "Stationery" }
            };

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);

            JsonElement predictionResult =
                workspace.AutomlAnalysisPrediction(
                    analysisId,
                    modelId,
                    features,
                    null
                );

            Console.WriteLine(predictionResult.ToString());
        }

                public void GetTags(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetTags();
            Console.WriteLine(result.ToString());
        }

        public void CreateTag(IAnalyticsClient ac)
        {
            string tagName = "Sales Tag";
            string colorCode = "#FF5733";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string tagId = workspace.CreateTag(tagName, colorCode, null);
            Console.WriteLine(tagId);
        }

        public void UpdateTag(IAnalyticsClient ac)
        {
            long tagId = 0L;
            Dictionary<string, object> config = new Dictionary<string, object>
            {
                { "name", "Sales Tag Updated" },
                { "colorCode", "#33FF57" }
            };
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateTag(tagId, config);
            Console.WriteLine("success");
        }

        public void DeleteTag(IAnalyticsClient ac)
        {
            long tagId = 0L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteTag(tagId);
            Console.WriteLine("success");
        }

        public void AddTagToViews(IAnalyticsClient ac)
        {
            long tagId = 0L;
            List<long> viewIds = new List<long> { viewId };
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.AddTagToViews(tagId, viewIds, null);
            Console.WriteLine("success");
        }

        public void RemoveTagFromViews(IAnalyticsClient ac)
        {
            long tagId = 0L;
            List<long> viewIds = new List<long> { viewId };
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.RemoveTagFromViews(tagId, viewIds, false, null);
            Console.WriteLine("success");
        }

        public void GetTaggedViews(IAnalyticsClient ac)
        {
            long tagId = 0L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetTaggedViews(tagId);
            Console.WriteLine(result.ToString());
        }

        public void GetViewTags(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement result = view.GetViewTags();
            Console.WriteLine(result.ToString());
        }

        public void AddTagsToView(IAnalyticsClient ac)
        {
            List<long> tagIds = new List<long> { 0L };
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AddTagsToView(tagIds, null);
            Console.WriteLine("success");
        }

        public void RemoveTagsFromView(IAnalyticsClient ac)
        {
            List<long> tagIds = new List<long> { 0L };
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemoveTagsFromView(tagIds, false, null);
            Console.WriteLine("success");
        }

        public void GetCustomRoles(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetCustomRoles();
            Console.WriteLine(result);
        }

        public void CreateCustomRole(IAnalyticsClient ac)
        {
            string roleName = "DashboardPowerUser";
            // Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
            string accessType = "ALL_DASHBOARDS";

            Dictionary<string, object> permissions = new Dictionary<string, object>
            {
                { "interactionPermissions", new Dictionary<string, object>
                    {
                        { "read", true },
                        { "vud", true },
                        { "drillDown", true },
                        { "insight", true }
                    }
                },
                { "sharePermissions", new Dictionary<string, object>
                    {
                        { "discussion", true },
                        { "privateLinks", true }
                    }
                },
                { "publishPermissions", new Dictionary<string, object>
                    {
                        { "export", true }
                    }
                }
            };

            IOrgAPI org = ac.GetOrgInstance(orgId);
            long roleId = org.CreateCustomRole(roleName, accessType, permissions, null);
            Console.WriteLine("Created Custom Role ID: " + roleId);
        }

        public void UpdateCustomRole(IAnalyticsClient ac)
        {
            long roleId = 0L;
            string roleName = "DashboardPowerUser";
            // Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
            string accessType = "ALL_DASHBOARDS";

            Dictionary<string, object> permissions = new Dictionary<string, object>
            {
                { "interactionPermissions", new Dictionary<string, object>
                    {
                        { "read", true },
                        { "vud", true },
                        { "drillDown", false },
                        { "insight", false }
                    }
                },
                { "sharePermissions", new Dictionary<string, object>
                    {
                        { "share", true },
                        { "privateLinks", false }
                    }
                },
                { "publishPermissions", new Dictionary<string, object>
                    {
                        { "export", true }
                    }
                }
            };

            IOrgAPI org = ac.GetOrgInstance(orgId);
            org.UpdateCustomRole(roleId, roleName, accessType, permissions, null);
            Console.WriteLine("success");
        }

        public void DeleteCustomRole(IAnalyticsClient ac)
        {
            long roleId = 0L;
            IOrgAPI org = ac.GetOrgInstance(orgId);
            org.DeleteCustomRole(roleId);
            Console.WriteLine("success");
        }

        public void GetQueryTables(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetQueryTables(null);
            Console.WriteLine(result);
        }


        public void GetAlertsInView(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement result = view.GetAlertsInView();
            Console.WriteLine(result);
        }


        public void GetViewMetadataForAlert(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement result = view.GetViewMetadataForAlert();
            Console.WriteLine(result);
        }


        public void CreateAlert(IAnalyticsClient ac)
        {
            string alertName = "Sales Drop Alert";

            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "daily");
            scheduleDetails.Add("hour", 9);
            scheduleDetails.Add("minute", 0);

            Dictionary<string, object> rule = new Dictionary<string, object>();
            rule.Add("operator", "lt");
            rule.Add("viewColumnIndex", "2");
            rule.Add("type", "constant");
            rule.Add("values", new List<string> { "1000" });

            List<Dictionary<string, object>> rules = new List<Dictionary<string, object>>();
            rules.Add(rule);

            Dictionary<string, object> email = new Dictionary<string, object>();
            email.Add("notifyAdmins", true);
            email.Add("subject", "Sales dropped below threshold");
            email.Add("message", "Please review the report.");

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("email", email);

            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long alertId = view.CreateAlert(alertName, scheduleDetails, rules, config);
            Console.WriteLine(alertId);
        }


        public void GetAlertsInWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAlertsInWorkspace();
            Console.WriteLine(result);
        }


        public void GetAlertConfiguration(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAlertConfiguration(alertId);
            Console.WriteLine(result);
        }


        public void UpdateAlert(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611;
            string alertName = "Sales Drop Alert (weekly)";

            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "weekly");
            scheduleDetails.Add("hour", 9);
            scheduleDetails.Add("minute", 30);
            scheduleDetails.Add("weekDays", new List<int> { 6 });
            scheduleDetails.Add("timeZone", "Asia/Kolkata");

            Dictionary<string, object> rule = new Dictionary<string, object>();
            rule.Add("operator", "lt");
            rule.Add("viewColumnIndex", "2");
            rule.Add("type", "constant");
            rule.Add("values", new List<string> { "1000" });

            List<Dictionary<string, object>> rules = new List<Dictionary<string, object>>();
            rules.Add(rule);

            Dictionary<string, object> email = new Dictionary<string, object>();
            email.Add("notifyAdmins", true);
            email.Add("emailIds", new List<string> { "finance@example.com" });
            email.Add("subject", "Weekly sales monitor");
            email.Add("message", "Weekly alert summary.");

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("email", email);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateAlert(alertId, alertName, scheduleDetails, rules, config);
            Console.WriteLine("success");
        }


        public void DeleteAlerts(IAnalyticsClient ac)
        {
            List<long> alertIds = new List<long>();
            alertIds.Add(137687000010815003);
            alertIds.Add(137687000010815005);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAlerts(alertIds, null);
            Console.WriteLine("success");
        }


        public void ChangeAlertStatus(IAnalyticsClient ac)
        {
            List<long> alertIds = new List<long>();
            alertIds.Add(137687000010815003);
            alertIds.Add(137687000010815005);
            bool enabled = false;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeAlertStatus(alertIds, enabled, null);
            Console.WriteLine("success");
        }


        public void RunAlert(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("validateSystemTags", false);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.RunAlert(alertId, config);
            Console.WriteLine("success");
        }


        public void GetAlertEvents(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611;

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("fromDate", "2026-05-01 00:00:00");
            config.Add("toDate", "2026-05-31 23:59:59");
            config.Add("status", new List<string> { "triggered", "error" });
            config.Add("pageNo", 1);
            config.Add("recordsPerPage", 50);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAlertEvents(alertId, config);
            Console.WriteLine(result);
        }


        public void GetLinkedWorkspaces(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetLinkedWorkspaces();
            Console.WriteLine(result);
        }


        public void GetLinkedWorkspacesForOrg(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetLinkedWorkspaces();
            Console.WriteLine(result);
        }


        public void GetLinkableWorkspaces(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetLinkableWorkspaces();
            Console.WriteLine(result);
        }


        public void GetWorkspaceLinkingCompatibility(IAnalyticsClient ac)
        {
            Dictionary<string, object> client = new Dictionary<string, object>();
            client.Add("orgId", 700000654321);
            client.Add("workspaceIds", new List<string> { "466206000000071000" });

            List<Dictionary<string, object>> clients = new List<Dictionary<string, object>>();
            clients.Add(client);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceLinkingCompatibility(clients, null);
            Console.WriteLine(result);
        }


        public void LinkWorkspaces(IAnalyticsClient ac)
        {
            Dictionary<string, object> client = new Dictionary<string, object>();
            client.Add("orgId", 700000654321);
            client.Add("workspaceIds", new List<string> { "466206000000071000" });

            List<Dictionary<string, object>> clients = new List<Dictionary<string, object>>();
            clients.Add(client);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.LinkWorkspaces(clients, null);
            Console.WriteLine("success");
        }


        public void UnlinkWorkspaces(IAnalyticsClient ac)
        {
            string scope = "ALL";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UnlinkWorkspaces(scope, null);
            Console.WriteLine("success");
        }


        public void SyncLinkedWorkspaces(IAnalyticsClient ac)
        {
            string scope = "ALL";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.SyncLinkedWorkspaces(scope, null);
            Console.WriteLine("success");
        }


        public void GetLinkedWorkspaceSyncDetails(IAnalyticsClient ac)
        {
            List<long> sandboxIds = new List<long>();
            sandboxIds.Add(137687000012345001);
            sandboxIds.Add(137687000012345002);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetLinkedWorkspaceSyncDetails(sandboxIds, null);
            Console.WriteLine(result);
        }


        public void GetWorkspaceBackups(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceBackups();
            Console.WriteLine(result);
        }


        public void BackupWorkspaceNow(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("backupMode", "STRUCTURE");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.BackupWorkspaceNow(config);
            Console.WriteLine(result);
        }


        public void GetWorkspaceBackupStatus(IAnalyticsClient ac)
        {
            long backupId = 35130000001056701;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceBackupStatus(backupId);
            Console.WriteLine(result);
        }


        public void DownloadWorkspaceBackup(IAnalyticsClient ac)
        {
            long backupId = 35130000001056701;
            string filePath = "C:\\Users\\Administrator\\Downloads\\workspace-backup.zip";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DownloadWorkspaceBackup(backupId, filePath, null);
            Console.WriteLine("success");
        }


        public void RestoreWorkspaceFromBackup(IAnalyticsClient ac)
        {
            long backupId = 35130000001056701;
            bool confirmRestore = true;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.RestoreWorkspaceFromBackup(backupId, confirmRestore, null);
            Console.WriteLine(result);
        }


        public void GetWorkspaceRestoreStatus(IAnalyticsClient ac)
        {
            long restoreId = 35130000001056801;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceRestoreStatus(restoreId);
            Console.WriteLine(result);
        }


        public void CreateDashboard(IAnalyticsClient ac)
        {
            string displayName = "Sales Overview";
            string layout = "{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Sales Dashboard</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}";

            Dictionary<string, object> settings = new Dictionary<string, object>();
            settings.Add("allowDrillDown", "true");
            settings.Add("fitToWidth", "true");

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("settings", settings);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long dashboardId = workspace.CreateDashboard(displayName, layout, config);
            Console.WriteLine(dashboardId);
        }


        public void UpdateDashboard(IAnalyticsClient ac)
        {
            long dashboardId = 35130000001055801;
            string layout = "{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Updated Title</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}";

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("layout", layout);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateDashboard(dashboardId, config);
            Console.WriteLine("success");
        }


        public void GetDashboardMetadata(IAnalyticsClient ac)
        {
            long dashboardId = 35130000001055801;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("include", "layout");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetDashboardMetadata(dashboardId, config);
            Console.WriteLine(result);
        }


        public void GetReportMetadata(IAnalyticsClient ac)
        {
            long reportId = 35130000001055901;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetReportMetadata(reportId);
            Console.WriteLine(result);
        }


        public void GetOrgAccessRestrictions(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetOrgAccessRestrictions();
            Console.WriteLine(result);
        }


        public void UpdateOrgAccessRestrictions(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("accessRestrictionEnabled", true);
            IOrgAPI org = ac.GetOrgInstance(orgId);
            org.UpdateOrgAccessRestrictions(config);
            Console.WriteLine("success");
        }


        public void GetWorkspaceAccessRestrictions(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceAccessRestrictions();
            Console.WriteLine(result);
        }


        public void UpdateWorkspaceAccessRestrictions(IAnalyticsClient ac)
        {
            Dictionary<string, object> shareViews = new Dictionary<string, object>();
            shareViews.Add("domainRestrictionEnabled", true);
            shareViews.Add("trustedDomains", new List<string> { "example.com", "partner.example.org" });

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("useOrganizationSettings", false);
            config.Add("shareViews", shareViews);
            config.Add("privateLinks", new Dictionary<string, object> { { "enabled", false } });
            config.Add("publicViews", new Dictionary<string, object> { { "enabled", false } });
            config.Add("exportViews", new Dictionary<string, object> { { "enabled", true } });

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateWorkspaceAccessRestrictions(config);
            Console.WriteLine("success");
        }


        public void SetAnalyticsServerURL(IAnalyticsClient ac)
        {
            string serverUrl = "https://analyticsapi.zoho.eu";
            ac.SetAnalyticsServerURL(serverUrl);
            Console.WriteLine("success");
        }


        public void SetAccountsServerURL(IAnalyticsClient ac)
        {
            string serverUrl = "https://accounts.zoho.eu";
            ac.SetAccountsServerURL(serverUrl);
            Console.WriteLine("success");
        }


        public void GetReadTimeout(IAnalyticsClient ac)
        {
            int timeout = ac.GetReadTimeout();
            Console.WriteLine(timeout);
        }


        public void SetReadTimeout(IAnalyticsClient ac)
        {
            int timeout = 1000;
            ac.SetReadTimeout(timeout);
            Console.WriteLine("success");
        }


        public void GetConnectionTimeout(IAnalyticsClient ac)
        {
            int timeout = ac.GetConnectionTimeout();
            Console.WriteLine(timeout);
        }


        public void SetConnectionTimeout(IAnalyticsClient ac)
        {
            int timeout = 1000;
            ac.SetConnectionTimeout(timeout);
            Console.WriteLine("success");
        }


        public void SetProxy(IAnalyticsClient ac)
        {
            string proxyHost = "proxy.example.com";
            int proxyPort = 8443;
            string proxyUsername = "proxyUser";
            string proxyPassword = "proxyPassword";
            ac.SetProxy(proxyHost, proxyPort, proxyUsername, proxyPassword);
            Console.WriteLine("success");
        }


        public void SetDebugLogPath()
        {
            string logFilePath = "C:\\Users\\Administrator\\Downloads\\zoho-analytics-sdk.log";
            AnalyticsClient.SetDebugLogPath(logFilePath);
            Console.WriteLine("success");
        }


        public void ChangeFolderHierarchy(IAnalyticsClient ac)
        {
            long folderId = 148746000002541001;
            int hierarchy = 0;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeFolderHierarchy(folderId, hierarchy, null);
            Console.WriteLine("success");
        }


        public void ChangeFolderPosition(IAnalyticsClient ac)
        {
            long folderId = 148746000002541001;
            long referenceFolderId = 148746000002541005;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeFolderPosition(folderId, referenceFolderId, null);
            Console.WriteLine("success");
        }


        public void MoveViewsToFolder(IAnalyticsClient ac)
        {
            long folderId = 148746000002541001;

            List<long> viewIds = new List<long>();
            viewIds.Add(148746000002542009);
            viewIds.Add(148746000002542007);

            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.MoveViewsToFolder(folderId, viewIds, null);
            Console.WriteLine("success");
        }


        public void GetWorkspaceUsers(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceUsers();
            Console.WriteLine(result);
        }


        public void AddWorkspaceUsers(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("user1@zoho.com");
            string role = "USER";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.AddWorkspaceUsers(emailIds, role, null);
            Console.WriteLine("success");
        }


        public void RemoveWorkspaceUsers(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("user1@zoho.com");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.RemoveWorkspaceUsers(emailIds, null);
            Console.WriteLine("success");
        }


        public void ChangeWorkspaceUserStatus(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("user1@zoho.com");
            string operation = "activate";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeWorkspaceUserStatus(emailIds, operation, null);
            Console.WriteLine("success");
        }


        public void ChangeWorkspaceUserRole(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("user1@zoho.com");
            string role = "USER";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeWorkspaceUserRole(emailIds, role, null);
            Console.WriteLine("success");
        }


        public void CreateQueryTable(IAnalyticsClient ac)
        {
            string sqlQuery = "Select * from Sales";
            string queryTableName = "Sales_QT";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long queryTableId = workspace.CreateQueryTable(sqlQuery, queryTableName, null);
            Console.WriteLine(queryTableId);
        }


        public void EditQueryTable(IAnalyticsClient ac)
        {
            long queryTableId = 100007000000038009;
            string sqlQuery = "Select * from Sales_1";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.EditQueryTable(queryTableId, sqlQuery, null);
            Console.WriteLine("success");
        }


        public void AddFormulaColumn(IAnalyticsClient ac)
        {
            string formulaName = "square";
            string expression = "square(\"Cost\")";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long formulaId = view.AddFormulaColumn(formulaName, expression, null);
            Console.WriteLine(formulaId);
        }


        public void EditFormulaColumn(IAnalyticsClient ac)
        {
            long formulaId = 148746000002541001;
            string expression = "sqrt(\"Cost\")";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.EditFormulaColumn(formulaId, expression, null);
            Console.WriteLine("success");
        }


        public void DeleteFormulaColumn(IAnalyticsClient ac)
        {
            long formulaId = 148746000002541001;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.DeleteFormulaColumn(formulaId, null);
            Console.WriteLine("success");
        }


        public void AddAggregateFormula(IAnalyticsClient ac)
        {
            string formulaName = "Sum";
            string expression = "sum(\"SalesTable\".\"Sales\")";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long formulaId = view.AddAggregateFormula(formulaName, expression, null);
            Console.WriteLine(formulaId);
        }


        public void EditAggregateFormula(IAnalyticsClient ac)
        {
            long formulaId = 148746000002541001;
            string expression = "avg(\"SalesTable\".\"Sales\")";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.EditAggregateFormula(formulaId, expression, null);
            Console.WriteLine("success");
        }


        public void DeleteAggregateFormula(IAnalyticsClient ac)
        {
            long formulaId = 148746000002541001;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.DeleteAggregateFormula(formulaId, null);
            Console.WriteLine("success");
        }


        public void UpdateSharedDetails(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("vincent.h@zoho.com");

            Dictionary<string, object> permissions = new Dictionary<string, object>();
            permissions.Add("read", true);
            permissions.Add("export", true);

            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("emailIds", emailIds);
            config.Add("permissions", permissions);

            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.UpdateSharedDetails(config);
            Console.WriteLine("success");
        }


        static void Main(string[] args)
        {
            string clientId = "1000.XXXXXXXXXX";
            string clientSecret = "XXXXXXXXXXXXXXXXXXXX";
            string refreshToken = "1000.XXXXXXXXXX.XXXXXXXXXX";

            try
            {
                IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
                Program obj = new();
                obj.DeleteAutomlAnalysis(ac);
            }
            catch (ServerException ex)
            {
                Console.WriteLine("Server exception - HTTPStatusCode : " + ex.GetHTTPStatusCode()
                    + ", ErrorCode : " + ex.GetErrorCode()
                    + ", ErrorMessage : " + ex.GetErrorMessage());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Other exception - " + ex.Message);
            }
        }
    }
}
