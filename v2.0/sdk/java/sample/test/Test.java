//$Id$
package test;
import com.zoho.analytics.client.*;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;

public class Test {

    private long orgId = 60000006l;
    private long workspaceId = 176702400000652603l;
    private long viewId = 177002400000300234l;

    public static void main(String args[]){

        String clientId = "";
        String clientSecret = "";
        String refreshToken = "";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            //tObj.setProxy(ac);
            tObj.getResourceDetails(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : "  + ex.getErrorMessage());
        }
        catch (ParseException ex) {
            System.out.println("Parser exception - ErrorMessage : "  + ex.getResponseMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            //ex.printStackTrace();
        }
    }

    public void setAnalyticsDomain(AnalyticsClient ac) throws Exception {
        String serverURL = "";
        ac.setAnalyticsServerURL(serverURL);
        System.out.println("success");
    }

    public void setAccountsDomain(AnalyticsClient ac) throws Exception {
        String serverURL = "";
        ac.setAccountsServerURL(serverURL);
        System.out.println("success");
    }

    public void getReadTimeout(AnalyticsClient ac) throws Exception {
        int timeout = ac.getReadTimeout();
        System.out.println(timeout);
    }

    public void setReadTimeout(AnalyticsClient ac) throws Exception {
        int timeout = 1000;
        ac.setReadTimeout(timeout);
        System.out.println("success");
    }

    public void getConnectionTimeout(AnalyticsClient ac) throws Exception {
        int timeout = ac.getConnectionTimeout();
        System.out.println(timeout);
    }

    public void setConnectionTimeout(AnalyticsClient ac) throws Exception {
        int timeout = 1000;
        ac.setConnectionTimeout(timeout);
        System.out.println("success");
    }

    public void setProxy(AnalyticsClient ac) throws Exception {
        String proxyHost = "";
        int proxyPort = 8443;
        String proxyUser = "";
        String proxyPass = "";
        ac.setProxy(proxyHost, proxyPort, proxyUser, proxyPass);
        System.out.println("Proxy configured");
    }


    public void addRows(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        JSONObject columnValues = new JSONObject();
        columnValues.put("Region", "East");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.addRow(columnValues, null);
        System.out.println(result);
    }

    public void updateRows(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        JSONObject columnValues = new JSONObject();
        columnValues.put("Region", "East");
        String criteria = "\"Region\"='East1'";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.updateRow(columnValues, criteria, null);
        System.out.println(result);
    }

    public void deleteRows(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        JSONObject columnValues = new JSONObject();
        columnValues.put("Region", "East");
        String criteria = "\"Region\"='East1'";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        int result = view.deleteRow(criteria, null);
        System.out.println(result);
    }


    public void importDataInNewTable(AnalyticsClient ac) throws Exception {

        String tableName = "JAVA Table";
        String fileType = "csv";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject response = data.importDataInNewTable(tableName, fileType, autoIdentify, filePath, config);
        System.out.println(response);
    }

    public void importData(AnalyticsClient ac) throws Exception {

        String importType = "TRUNCATEADD";
        String fileType = "csv";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject response = data.importData(viewId, importType, fileType, autoIdentify, filePath, config);
        System.out.println(response);
    }

    public void importRawDataInNewTable(AnalyticsClient ac) throws Exception {

        String tableName = "JAVA json Table_1";
        String fileType = "json";
        boolean autoIdentify = true;
        JSONArray rawData = new JSONArray("[{\"Date\":\"23 March, 2017\",\"Region\":\"West\",\"Product Category\":\"Grocery\",\"Product\":\"12\",\"Customer Name\":\"Vincent Herbert\",\"Sales\":\"$1,682.39\",\"Cost\":\"$200.05\"},{\"Date\":\"23 March, 2017\",\"Region\":\"West\",\"Product Category\":\"Grocery\",\"Product\":\"Fruits and Vegetables\",\"Customer Name\":\"Vincent Herbert\",\"Sales\":\"$1,682.39\",\"Cost\":\"$200.05\"}]");
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject response = data.importRawDataInNewTable(tableName, fileType, autoIdentify, rawData.toString(), config);
        System.out.println(response);
    }

    public void importRawData(AnalyticsClient ac) throws Exception {

        String importType = "APPEND";
        String fileType = "json";
        boolean autoIdentify = true;
        JSONArray rawData = new JSONArray("[{\"Date\":\"23 March, 2017\",\"Region\":\"West\",\"Product Category\":\"Grocery\",\"Product\":\"12\",\"Customer Name\":\"Vincent Herbert\",\"Sales\":\"$1,682.39\",\"Cost\":\"$200.05\"},{\"Date\":\"23 March, 2017\",\"Region\":\"West\",\"Product Category\":\"Grocery\",\"Product\":\"Fruits and Vegetables\",\"Customer Name\":\"Vincent Herbert\",\"Sales\":\"$1,682.39\",\"Cost\":\"$200.05\"}]");
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject response = data.importRawData(viewId, importType, fileType, autoIdentify, rawData.toString(), config);
        System.out.println(response);
    }

    public void importBulkDataInNewTable(AnalyticsClient ac) throws Exception {

        String tableName = "JAVA Bulk Table";
        String fileType = "csv";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.importBulkDataInNewTable(tableName, fileType, autoIdentify, filePath, config);
        System.out.println(jobId);
    }

    public void importBulkData(AnalyticsClient ac) throws Exception {

        String importType = "TRUNCATEADD";
        String fileType = "csv";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        JSONObject config = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.importBulkData(viewId, importType, fileType, autoIdentify, filePath, config);
        System.out.println(jobId);
    }

    public void importDataInNewTableAsBatches(AnalyticsClient ac) throws Exception {
        String tableName = "Batch Import New Table";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        int batchSize = 100000;
        JSONObject config = new JSONObject();
        JSONObject toolConfig = new JSONObject();

        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.importDataInNewTableAsBatches(tableName, autoIdentify, filePath, batchSize, config, toolConfig);
        System.out.println(jobId);
    }

    public void importDataAsBatches(AnalyticsClient ac) throws Exception {
        long viewId = 100007000000038009l;
        String importType = "append";
        boolean autoIdentify = true;
        String filePath = "/home/local/admin/Files/Sales.csv";
        int batchSize = 100000;
        JSONObject config = new JSONObject();
        JSONObject toolConfig = new JSONObject();
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.importDataAsBatches(viewId, importType, autoIdentify, filePath, batchSize, config, toolConfig);
        System.out.println(jobId);
    }

    public void getImportJobDetails(AnalyticsClient ac) throws Exception {
        long jobId = 35130000001343088l;
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject jobInfo = data.getImportJobDetails(jobId);
        System.out.println(jobInfo);
    }

    public void exportData(AnalyticsClient ac) throws Exception {
        String responseFormat = "csv";
        String filePath = "/home/local/admin/Files/Sales.csv";
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        data.exportData(viewId, responseFormat, filePath, null);
        System.out.println("completed");
    }

    public void exportDataUsingStream(AnalyticsClient ac) throws Exception {
        OutputStream os = new ByteArrayOutputStream();
        String responseFormat = "csv";
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        data.exportData(viewId, responseFormat, os, null);

        String response = new String(((ByteArrayOutputStream) os).toByteArray());
        System.out.println(response);
    }

    public void initiateBulkExport(AnalyticsClient ac) throws Exception {
        String responseFormat = "html";
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.initiateBulkExport(viewId, responseFormat, null);
        System.out.println(jobId);
    }

    public void initiateBulkExportUsingSQL(AnalyticsClient ac) throws Exception {
        String sqlQuery = "select * from Sales";
        String responseFormat = "csv";
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        long jobId = data.initiateBulkExportUsingSQL(sqlQuery, responseFormat, null);
        System.out.println(jobId);
    }

    public void getExportJobDetails(AnalyticsClient ac) throws Exception {
        long jobId = 35130000001343084l;
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        JSONObject jobInfo = data.getExportJobDetails(jobId);
        System.out.println(jobInfo);
    }

    public void exportBulkData(AnalyticsClient ac) throws Exception {
        long jobId = 35130000001342175l;
        String filePath = "/home/local/admin/Files/Sales.csv";
        BulkAPI data = ac.getBulkInstance(orgId, workspaceId);
        data.exportBulkData(jobId, filePath);
        System.out.println("success");
    }

    public void createWorkspace(AnalyticsClient ac) throws Exception {
        String workspaceName = "JAVA Lib";
        OrgAPI org = ac.getOrgInstance(orgId);
        long result = org.createWorkspace(workspaceName, null);
        System.out.println(result);
    }

    public void copyWorkspace(AnalyticsClient ac) throws Exception {
        long workspaceId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String workspaceName = "JAVA Lib";
        Long destOrgId = null;
        long result = workspace.copy(workspaceName, null, destOrgId);
        System.out.println(result);
    }

    public void renameWorkspace(AnalyticsClient ac) throws Exception {
        long workspaceId = 0l;
        String workspaceName = "JAVA Lib";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.rename(workspaceName, null);
        System.out.println("success");
    }

    public void deleteWorkspace(AnalyticsClient ac) throws Exception {
        long workspaceId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.delete();
        System.out.println("success");
    }

    public void createTable(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject tableDesign = new JSONObject();
        long result = workspace.createTable(tableDesign);
        System.out.println(result);
    }

    public void createQueryTable(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String sqlQuery = "Select * from Sales";
        String queryTableName = "Sales_QT";
        long result = workspace.createQueryTable(sqlQuery, queryTableName, null);
        System.out.println(result);
    }

    public void updateQueryTable(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String sqlQuery = "Select * from Sales_1";
        long queryTableId = 100007000000038009l;
        workspace.updateQueryTable(queryTableId, sqlQuery, null);
        System.out.println("success");
    }

    public void saveAsView(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        String newViewName = "";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long newViewId = view.saveAs(newViewName, null);
        System.out.println(newViewId);
    }

    public void renameView(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        String viewName = "";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.rename(viewName, null);
        System.out.println("success");
    }

    public void deleteView(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.delete(null);
        System.out.println("success");
    }

    public void createFolder(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String folderName = "";
        long result = workspace.createFolder(folderName, null);
        System.out.println(result);
    }

    public void renameFolder(AnalyticsClient ac) throws Exception {
        long folderId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String folderName = "";
        workspace.renameFolder(folderId, folderName, null);
        System.out.println("success");
    }

    public void deleteFolder(AnalyticsClient ac) throws Exception {
        long folderId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteFolder(folderId);
        System.out.println("success");
    }

    public void addColumn(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        String columnName = "";
        String dataType = "";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long result = view.addColumn(columnName, dataType, null);
        System.out.println(result);
    }

    public void renameColumn(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long columnId = 0l;
        String columnName = "";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.renameColumn(columnId, columnName);
        System.out.println("success");
    }

    public void deleteColumn(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long columnId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.deleteColumn(columnId, null);
        System.out.println("success");
    }

    public void addLookup(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long columnId = 0l;
        long refViewId = 0l;
        long refColumnId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.addLookup(columnId, refViewId, refColumnId, null);
        System.out.println("success");
    }

    public void removeLookup(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long columnId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removeLookup(columnId, null);
        System.out.println("success");
    }

    public void hideColumns(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        JSONArray columnIds = new JSONArray();
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.hideColumns(columnIds);
        System.out.println("success");
    }

    public void showColumns(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        JSONArray columnIds = new JSONArray();
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.showColumns(columnIds);
        System.out.println("success");
    }

    public void copyViews(AnalyticsClient ac) throws Exception {
        JSONArray viewIds = new JSONArray();
        long destWorkspaceId = 0l;
        Long destOrgId = null;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray views = workspace.copyViews(viewIds, destWorkspaceId, null, destOrgId);
        System.out.println(views);
    }

    public void copyFormulas(AnalyticsClient ac) throws Exception {
        long viewId = 1148746000002449089l;
        JSONArray formulaNames = new JSONArray();
        formulaNames.put("Total");
        long destWorkspaceId = 1148746000002662004l;
        Long destOrgId = null;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.copyFormulas(formulaNames, destWorkspaceId, null, destOrgId);
        System.out.println("success");
    }

    public void createSimilarViews(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long refViewId = 0l;
        long folderId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.createSimilarViews(refViewId, folderId, null);
        System.out.println("success");
    }

    public void autoAnalyseView(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.autoAnalyse(null);
        System.out.println("success");
    }

    public void autoAnalyseColumn(AnalyticsClient ac) throws Exception {
        long viewId = 0l;
        long columnId = 0l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.autoAnalyseColumn(columnId, null);
        System.out.println("success");
    }

    public void createVariable(AnalyticsClient ac) throws Exception {
        String variableName = "Variable_1";
        int variableDataType = 1;
        int variableType = 3;

        JSONObject format = new JSONObject();
        format.put("alignment", "left");

        JSONArray values_1 = new JSONArray();
        values_1.put("1");
        values_1.put("2");

        JSONArray emailIds_1 = new JSONArray();
        emailIds_1.put("user+1@zoho.com");
        emailIds_1.put("user+2@zoho.com");

        JSONArray values_2 = new JSONArray();
        values_2.put("3");
        values_2.put("4");

        JSONArray emailIds_2 = new JSONArray();
        emailIds_2.put("user+3@zoho.com");
        emailIds_2.put("user+4@zoho.com");

        JSONObject dataset_1 = new JSONObject();
        dataset_1.put("values", values_1);
        dataset_1.put("emailIds", emailIds_1);

        JSONObject dataset_2 = new JSONObject();
        dataset_2.put("values", values_2);
        dataset_2.put("emailIds", emailIds_2);

        JSONArray userSpecificData = new JSONArray();
        userSpecificData.put(dataset_1);
        userSpecificData.put(dataset_2);

        JSONObject config = new JSONObject();
        config.put("format", format);
        config.put("userSpecificData", userSpecificData);


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createVariable(variableName, variableDataType, variableType, config);
        System.out.println(result);
    }

    public void updateVariable(AnalyticsClient ac) throws Exception {
        long variableId = 0l;
        String variableName = "Variable_2";
        int variableDataType = 1;
        int variableType = 3;

        JSONObject format = new JSONObject();
        format.put("alignment", "right");

        JSONArray values_1 = new JSONArray();
        values_1.put("11");
        values_1.put("12");

        JSONArray emailIds_1 = new JSONArray();
        emailIds_1.put("user+1@zoho.com");
        emailIds_1.put("user+2@zoho.com");

        JSONArray values_2 = new JSONArray();
        values_2.put("13");
        values_2.put("14");

        JSONArray emailIds_2 = new JSONArray();
        emailIds_2.put("user+3@zoho.com");
        emailIds_2.put("user+4@zoho.com");

        JSONObject dataset_1 = new JSONObject();
        dataset_1.put("values", values_1);
        dataset_1.put("emailIds", emailIds_1);

        JSONObject dataset_2 = new JSONObject();
        dataset_2.put("values", values_2);
        dataset_2.put("emailIds", emailIds_2);

        JSONArray userSpecificData = new JSONArray();
        userSpecificData.put(dataset_1);
        userSpecificData.put(dataset_2);

        JSONObject config = new JSONObject();
        config.put("format", format);
        config.put("userSpecificData", userSpecificData);


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateVariable(variableId, variableName, variableDataType, variableType, config);
        System.out.println("success");
    }

    public void deleteVariable(AnalyticsClient ac) throws Exception {
        long variableId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteVariable(variableId);
        System.out.println("success");
    }

    public void getVariables(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getVariables();
        System.out.println(result);
    }

    public void getVariableDetails(AnalyticsClient ac) throws Exception {
        long variableId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getVariableDetails(variableId);
        System.out.println(result);
    }

    public void makeDefaultFolder(AnalyticsClient ac) throws Exception {
        long folderId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.makeDefaultFolder(folderId);
        System.out.println("success");
    }

    public void getOrgWorkspaces(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getOrgWorkspaces();
        System.out.println(result);
    }

    public void getViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getViews(null);
        System.out.println(result);
    }

    public void getFolders(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getFolders();
        System.out.println(result);
    }

    public void getOrgRecentItems(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getOrgRecentItems();
        System.out.println(result);
    }

    public void getOrgDashboards(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONObject config = new JSONObject();
        config.put("recordsPerPage", 50);
        JSONObject result = org.getOrgDashboards(config);
        System.out.println(result);
    }

    public void getWorkspaceSecretKey(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String result = workspace.getSecretKey(null);
        System.out.println(result);
    }

    public void getWorkspaceDetails(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceDetails(null);
        System.out.println(result);
    }

    public void getViewDetails(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONObject result = org.getViewDetails(viewId, null);
        System.out.println(result);
    }

    public void addFavouriteWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.addFavorite();
        System.out.println("success");
    }

    public void removeFavouriteWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.removeFavorite();
        System.out.println("success");
    }

    public void addFavouriteView(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.addFavorite();
        System.out.println("success");
    }

    public void removeFavouriteView(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removeFavorite();
        System.out.println("success");
    }

    public void addDefaultWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.addDefault();
        System.out.println("success");
    }

    public void removeDefaultWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.removeDefault();
        System.out.println("success");
    }

    public void getMetaDetails(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        String workspaceName = "API Lib";
        String viewName = "Sales";
        JSONObject result = org.getMetaDetails(workspaceName, viewName);
        System.out.println(result);
    }

    public void enableDomainAccess(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.enableDomainAccess();
        System.out.println("success");
    }

    public void disableDomainAccess(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.disableDomainAccess();
        System.out.println("success");
    }

    public void getOrgAdmins(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getAdmins();
        System.out.println(result);
    }

    public void getWorkspaceAdmins(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getAdmins();
        System.out.println(result);
    }

    public void addWorkspaceAdmins(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+1@zohotest.com");
        workspace.addAdmins(emailIds, null);
        System.out.println("success");
    }

    public void removeWorkspaceAdmins(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+1@zohotest.com");
        workspace.removeAdmins(emailIds, null);
        System.out.println("success");
    }

    public void getWorkspaceShareInfo(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        ShareInfo result = workspace.getShareInfo();
        System.out.println(result.getSharedUsers());
    }

    public void getDatasources(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getDatasources();
        System.out.println(result);
    }

    public void syncData(AnalyticsClient ac) throws Exception {
        long datasourceId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.syncData(datasourceId, null);
        System.out.println("success");
    }

    public void updateDatasourceConnection(AnalyticsClient ac) throws Exception {
        long datasourceId = 0l;

        JSONObject config = new JSONObject();
        config.put("serviceName", "AMAZON RDS");
        config.put("databaseType", "POSTGRESQL");
        config.put("hostName", "******");
        config.put("port", "5432");
        config.put("userName", "******");
        config.put("password", "******");
        config.put("cloudDatabaseName", "sampledb");

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateDatasourceConnection(datasourceId, config);
        System.out.println("success");
    }

    public void getTrashViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getTrashViews();
        System.out.println(result);
    }

    public void restoreTrashView(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long viewId = 0l;
        workspace.restoreTrashView(viewId, null);
        System.out.println("success");
    }

    public void deleteTrashView(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long viewId = 0l;
        workspace.deleteTrashView(viewId, null);
        System.out.println("success");
    }

    public void getLastImportDetails(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getLastImportDetails();
        System.out.println(result);
    }

    public void shareViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+1@zohotest.com");
        emailIds.put("vinothkumar.krishnasamy+2@zohotest.com");
        JSONArray viewIds = new JSONArray();
        viewIds.put("1148746000002449002");
        JSONObject permissions = new JSONObject();
        permissions.put("read", true);
        workspace.shareViews(viewIds, emailIds, permissions, null);
        System.out.println("success");
    }

    public void removeShare(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+2@zohotest.com");
        JSONArray viewIds = new JSONArray();
        viewIds.put("1148746000002449002");
        workspace.removeShare(viewIds, emailIds, null);
        System.out.println("success");
    }

    public void getSharedDetailsForViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray viewIds = new JSONArray();
        viewIds.put("1148746000002449002");
        JSONArray result = workspace.getSharedDetailsForViews(viewIds);
        System.out.println(result);
    }

    public void getMyPermissions(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getMyPermissions();
        System.out.println(result);
    }

    public void getGroups(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getGroups();
        System.out.println(result);
    }

    public void createGroup(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String groupName = "API Group";
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+1@zohotest.com");
        String result = workspace.createGroup(groupName, emailIds, null);
        System.out.println(result);
    }

    public void getGroupDetails(AnalyticsClient ac) throws Exception {
        long groupId = 1148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getGroupDetails(groupId);
        System.out.println(result);
    }

    public void renameGroup(AnalyticsClient ac) throws Exception {
        long groupId = 1148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String groupName = "Renamed API Group";
        workspace.renameGroup(groupId, groupName, null);
        System.out.println("success");
    }

    public void addGroupMembers(AnalyticsClient ac) throws Exception {
        long groupId = 1148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+2@zohotest.com");
        workspace.addGroupMembers(groupId, emailIds, null);
        System.out.println("success");
    }

    public void removeGroupMembers(AnalyticsClient ac) throws Exception {
        long groupId = 1148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+2@zohotest.com");
        workspace.removeGroupMembers(groupId, emailIds, null);
        System.out.println("success");
    }

    public void deleteGroup(AnalyticsClient ac) throws Exception {
        long groupId = 1148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteGroup(groupId);
        System.out.println("success");
    }

    public void getViewURL(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.getViewURL(null);
        System.out.println(result);
    }

    public void getEmbedURL(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.getEmbedURL(null);
        System.out.println(result);
    }

    public void getPrivateURL(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.getPrivateURL(null);
        System.out.println(result);
    }

    public void generatePrivateUrl(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.createPrivateURL(null);
        System.out.println(result);
    }

    public void removePrivateAccess(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removePrivateAccess();
        System.out.println("success");
    }

    public void makeViewPublic(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.makeViewPublic(null);
        System.out.println(result);
    }

    public void removePublicAccess(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removePublicAccess();
        System.out.println("success");
    }

    public void getPublishConfigurations(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getPublishConfigurations();
        System.out.println(result);
    }

    public void updatePublishConfigurations(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);

        JSONObject config = new JSONObject();
        config.put("includeTitle", true);
        config.put("includeDesc", true);
        config.put("includeToolBar", false);
        config.put("includeSocialWidgets", false);
        config.put("includeSearchBox", true);
        config.put("includeDatatypeSymbol", false);
        config.put("includeShowHideOption", false);
        config.put("isInteractive", true);
        config.put("legendPosition", "RIGHT");
        config.put("width", 800);
        config.put("height", 600);
        config.put("autoRefresh", -1);
        config.put("URLCriteria", "");
        config.put("includeAskZia", false);

        view.updatePublishConfigurations(config);
        System.out.println("success");
    }

    public void getSlideshows(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getSlideshows();
        System.out.println(result);
    }

    public void getSlideshowUrl(AnalyticsClient ac) throws Exception {
        long slideId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String result = workspace.getSlideshowURL(slideId, null);
        System.out.println(result);
    }

    public void getSlideshowInfo(AnalyticsClient ac) throws Exception {
        long slideId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getSlideshowDetails(slideId);
        System.out.println(result);
    }

    public void createSlideshows(AnalyticsClient ac) throws Exception {
        String slideName = "";
        JSONArray viewIds = new JSONArray();
        viewIds.put("");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createSlideshow(slideName, viewIds, null);
        System.out.println(result);
    }

    public void updateSlideshow(AnalyticsClient ac) throws Exception {
        long slideId = 148746000002541001l;
        String slideName = "";
        JSONArray viewIds = new JSONArray();
        viewIds.put("");

        JSONObject config = new JSONObject();
        config.put("slideName", slideName);
        config.put("viewIds", viewIds);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateSlideshow(slideId, config);
        System.out.println("success");
    }

    public void deleteSlideshow(AnalyticsClient ac) throws Exception {
        long slideId = 148746000002541001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteSlideshow(slideId);
        System.out.println("success");
    }

    public void getSubscriptionDetails(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONObject result = org.getSubscriptionDetails();
        System.out.println(result);
    }

    public void getResourceDetails(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getResourceDetails();
        System.out.println(result);
    }

    public void getUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getUsers();
        System.out.println(result);
    }

    public void addUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+101@zohotest.com");
        org.addUsers(emailIds, null);
        System.out.println("success");
    }

    public void activateUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+101@zohotest.com");
        org.activateUsers(emailIds, null);
        System.out.println("success");
    }

    public void deactivateUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+101@zohotest.com");
        org.deactivateUsers(emailIds, null);
        System.out.println("success");
    }

    public void removeUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("vinothkumar.krishnasamy+101@zohotest.com");
        org.removeUsers(emailIds, null);
        System.out.println("success");
    }

    public void changeUserRole(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user+1@zohotest.com");
        String role = "USER";
        org.changeUserRole(emailIds, role, null);
        System.out.println("success");
    }


    public void updateSharedDetails(AnalyticsClient ac) throws Exception {

        JSONArray emailIds = new JSONArray();
        emailIds.put("vincent.h@zoho.com");

        JSONObject permissions = new JSONObject();
        permissions.put("read", true);
        permissions.put("export", true);

        JSONObject config = new JSONObject();
        config.put("emailIds", emailIds);
        config.put("permissions", permissions);

        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.UpdateSharedDetails(config);
        System.out.println("success");
    }

    public void changeFolderHierarchy(AnalyticsClient ac) throws Exception {
        long folderId = 148746000002541001l;
        int hierarchy = 0;

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeFolderHierarchy(folderId, hierarchy, null);
        System.out.println("success");
    }

    public void changeFolderPosition(AnalyticsClient ac) throws Exception {
        long folderId = 148746000002541001l;
        long referenceFolderId = 148746000002541005l;

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeFolderPosition(folderId, referenceFolderId, null);
        System.out.println("success");
    }

    public void moveViewsToFolder(AnalyticsClient ac) throws Exception {
        long folderId = 148746000002541001l;
        JSONArray viewIds = new JSONArray();
        viewIds.put(148746000002542009l);
        viewIds.put(148746000002542007l);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.moveViewsToFolder(folderId, viewIds, null);
        System.out.println("success");
    }

    public void exportAsTemplate(AnalyticsClient ac) throws Exception {
        String filePath = "/home/local/admin/Files/Sales.atpt";

        JSONArray viewIds = new JSONArray();
        viewIds.put(148746000002542009l);
        viewIds.put(148746000002542007l);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.exportAsTemplate(viewIds, filePath, null);
        System.out.println("success");
    }

    public void getWorkspaceUsers(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getWorkspaceUsers();
        System.out.println(result);
    }

    public void addWorkspaceUsers(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user1@zoho.com");
        String role = "USER";
        workspace.addWorkspaceUsers(emailIds, role, null);
        System.out.println("success");
    }

    public void removeWorkspaceUsers(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user1@zoho.com");
        workspace.removeWorkspaceUsers(emailIds, null);
        System.out.println("success");
    }

    public void changeWorkspaceUserRole(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user1@zoho.com");
        String role = "USER";
        workspace.changeWorkspaceUserRole(emailIds, role, null);
        System.out.println("success");
    }

    public void changeWorkspaceUserStatus(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user1@zoho.com");
        String operation = "activate";
        workspace.changeWorkspaceUserStatus(emailIds, operation, null);
        System.out.println("success");
    }

    public void getFormulaColumns(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray fomulas = view.getFormulaColumns();
        System.out.println(fomulas);
    }

    public void addFormulaColumn(AnalyticsClient ac) throws Exception {
        String formulaName = "square";
        String expression = "square(\"Cost\")";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long result = view.addFormulaColumn(formulaName, expression, null);
        System.out.println(result);
    }

    public void editFormulaColumn(AnalyticsClient ac) throws Exception {
        long formulaId = 148746000002541001l;
        String expression = "sqrt(\"Cost\")";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.editFormulaColumn(formulaId, expression, null);
        System.out.println("success");
    }

    public void deleteFormulaColumn(AnalyticsClient ac) throws Exception {
        long formulaId = 148746000002541001l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.deleteFormulaColumn(formulaId, null);
        System.out.println("success");
    }

    public void getAggregateFormulas(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray fomulas = view.getAggregateFormulas();
        System.out.println(fomulas);
    }

    public void addAggregateFormula(AnalyticsClient ac) throws Exception {
        String formulaName = "Sum";
        String expression = "sum(\"SalesTable\".\"Sales\")";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long result = view.addAggregateFormula(formulaName, expression, null);
        System.out.println(result);
    }

    public void editAggregateFormula(AnalyticsClient ac) throws Exception {
        long formulaId = 148746000002541001l;
        String expression = "avg(\"SalesTable\".\"Sales\")";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.editAggregateFormula(formulaId, expression, null);
        System.out.println("success");
    }

    public void deleteAggregateFormula(AnalyticsClient ac) throws Exception {
        long formulaId = 148746000002541001l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.deleteAggregateFormula(formulaId, null);
        System.out.println("success");
    }

    public void getViewDependents(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray views = view.getViewDependents();
        System.out.println(views);
    }

    public void getColumnDependents(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long columnId = 148746000002541001l;
        JSONObject data = view.getColumnDependents(columnId);
        System.out.println(data);
    }

    public void getEmailSchedules(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getEmailSchedules();
        System.out.println(result);
    }

    public void createEmailSchedule(AnalyticsClient ac) throws Exception {


        String scheduleName = "Schedule1";
        String format = "CSV";

        JSONArray viewIds = new JSONArray();
        viewIds.put(1148746000002449002l);

        JSONArray emailIds = new JSONArray();
        emailIds.put("user+1@zoho.com");
        emailIds.put("user+2@zoho.com");

        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "Daily");
        scheduleDetails.put("hour", 10);
        scheduleDetails.put("minute", 30);

        JSONObject config = new JSONObject();
        config.put("subject", "Daily Sales Report");


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config);
        System.out.println(result);
    }

    public void updateEmailSchedule(AnalyticsClient ac) throws Exception {

        long scheduleId = 115674600000150007l;

        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "Daily");
        scheduleDetails.put("hour", 8);
        scheduleDetails.put("minute", 30);

        JSONObject config = new JSONObject();
        config.put("subject", "Daily Sales Overview");
        config.put("scheduleDetails", scheduleDetails);


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.updateEmailSchedule(scheduleId, config);
        System.out.println(result);
    }

    public void triggerEmailSchedule(AnalyticsClient ac) throws Exception {

        long scheduleId = 115674600000150007l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.triggerEmailSchedule(scheduleId);
        System.out.println("success");
    }

    public void changeEmailScheduleStatus(AnalyticsClient ac) throws Exception {

        long scheduleId = 115674600000150007l;
        String operation = "deactivate";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeEmailScheduleStatus(scheduleId, operation);
        System.out.println("success");
    }

    public void deleteEmailSchedule(AnalyticsClient ac) throws Exception {

        long scheduleId = 115674600000150007l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteEmailSchedule(scheduleId);
        System.out.println("success");
    }

    public void getAggregateFormulasInWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getAggregateFormulas(null);
        System.out.println(result);
    }

    public void getAggregateFormulaDependents(AnalyticsClient ac) throws Exception {
        long formulaId = 115674600000150007l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getAggregateFormulaDependents(formulaId);
        System.out.println(result);
    }

    public void getAggregateFormulaValue(AnalyticsClient ac) throws Exception {
        long formulaId = 115674600000150007l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String result = workspace.getAggregateFormulaValue(formulaId);
        System.out.println(result);
    }

    public void createReport(AnalyticsClient ac) throws Exception {

        String baseTableName = "Sales";

        JSONObject xAxis = new JSONObject();
        xAxis.put("type", "xAxis");
        xAxis.put("columnName", "Date");
        xAxis.put("operation", "year");

        JSONObject yAxis = new JSONObject();
        yAxis.put("type", "yAxis");
        yAxis.put("columnName", "Sales");
        yAxis.put("operation", "sum");

        JSONArray axisColumns = new JSONArray();
        axisColumns.put(xAxis);
        axisColumns.put(yAxis);

        JSONObject config = new JSONObject();
        config.put("baseTableName", baseTableName);
        config.put("title", "New Chart");
        config.put("reportType", "chart");
        config.put("axisColumns", axisColumns);


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long viewId = workspace.createReport(config);
        System.out.println(viewId);
    }

    public void updateReport(AnalyticsClient ac) throws Exception {

        long viewId = 35130000005594013l;

        JSONObject xAxis = new JSONObject();
        xAxis.put("type", "xAxis");
        xAxis.put("columnName", "Date");
        xAxis.put("operation", "year");

        JSONObject yAxis = new JSONObject();
        yAxis.put("type", "yAxis");
        yAxis.put("columnName", "Cost");
        yAxis.put("operation", "sum");

        JSONArray axisColumns = new JSONArray();
        axisColumns.put(xAxis);
        axisColumns.put(yAxis);

        JSONObject config = new JSONObject();
        config.put("reportType", "chart");
        config.put("axisColumns", axisColumns);


        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateReport(viewId, config);
        System.out.println("success");
    }

    public void getTableMetadata(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getTableMetadata();
        System.out.println(result);
    }

    public void reorderColumns(AnalyticsClient ac) throws Exception {
        JSONArray columnIds = new JSONArray();
        columnIds.put("466206000000073014");
        columnIds.put("466206000000073013");
        columnIds.put("466206000000069003");


        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.reorderColumns(columnIds, null);
        System.out.println("success");
    }

    public void sortDataByColumns(AnalyticsClient ac) throws Exception {
        JSONArray columnIds = new JSONArray();
        columnIds.put("466206000000073014");
        columnIds.put("466206000000073013");

        int sortOrder = 2; // 1 = ASC, 2 = DESC
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.sortDataByColumns(columnIds, sortOrder, false, null);
        System.out.println("success");
    }

    public void resetSort(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.sortDataByColumns(null, null, true, null);
        System.out.println("success");
    }

    public void getQueryTableDetails(AnalyticsClient ac) throws Exception {
        String queryTableId = "466206000000061149";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        JSONObject result = workspace.getQueryTableDetails(queryTableId);
        System.out.println(result);
    }

    public void getAutoMLAnalysisInOrg(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getAutoMLAnalysis();
        System.out.println(result);
    }

    public void getAutoMLAnalysisInWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        JSONArray result = workspace.getAutoMLAnalysis();
        System.out.println(result);
    }

    public void getAutoMLAnalysisDetails(AnalyticsClient ac) throws Exception {
        String analysisId = "466206000000182001";

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        JSONObject result = workspace.getAutoMLAnalysisDetails(analysisId);
        System.out.println(result);
    }

    public void getDeploymentDetails(AnalyticsClient ac) throws Exception {
        String analysisId = "466206000000073001";
        String modelId = "466206000000073003";

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        JSONObject result = workspace.getDeploymentDetails(analysisId, modelId);

        System.out.println(result);
    }

    public void createAutoMLAnalysis(AnalyticsClient ac) throws Exception {

        String automlName = "Sales Analysis Java SDk";
        String trainingTableId = "466206000000061002";
        String predictionType = "CLASSIFICATION";

        JSONArray features = new JSONArray();
        features.put("Region");
        features.put("Product Category");
        features.put("Sales");

        int serverOption = 1;

        JSONObject decisionTree = new JSONObject();
        decisionTree.put("minimumSampleSplit", "2");
        decisionTree.put("maximumDepth", "100");

        JSONObject randomForest = new JSONObject();
        randomForest.put("minimumSampleSplit", "2");
        randomForest.put("maximumDepth", "100");
        randomForest.put("numberOfTrees", "25");

        JSONObject algorithms = new JSONObject();
        algorithms.put("decisionTreeClassification", decisionTree);
        algorithms.put("randomForestClassification", randomForest);

        JSONObject config = new JSONObject();
        config.put("description", "Sales Table Analysis...");
        config.put("targetColumn", "Product");

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        String automlId = workspace.createAutoMLAnalysis(
                automlName,
                trainingTableId,
                predictionType,
                features,
                serverOption,
                algorithms,
                config
        );

        System.out.println("Created AutoML Analysis ID: " + automlId);
    }

    public void deleteAutoMLAnalysis(AnalyticsClient ac) throws Exception {
        String analysisId = "466206000000182001";
        WorkspaceAPI workspace =
                ac.getWorkspaceInstance(orgId, workspaceId);

        workspace.deleteAutoMLAnalysis(analysisId, null);
        System.out.println("AutoML Analysis deleted successfully.");
    }

    public void deleteAutoMLAnalysisModel(AnalyticsClient ac) throws Exception {
        String analysisId = "466206000000182001";
        String modelId = "466206000000182005";

        WorkspaceAPI workspace =
                ac.getWorkspaceInstance(orgId, workspaceId);

        workspace.deleteAutoMLAnalysisModel(analysisId, modelId, null);
        System.out.println("Model deleted successfully.");
    }

    public void createAutoMLDeployment(AnalyticsClient ac) throws Exception {

        String analysisId = "466206000000182001";
        String modelId = "466206000000182005";

        String inputTableId = "466206000000061002";
        String outputTable = "Sales - 1";

        JSONArray outputColumns = new JSONArray();
        outputColumns.put("Sales");
        outputColumns.put("Region");

        String predictionColumn = "precol";
        int serverOption = 1;
        String importType = "APPEND";

        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "hourly");
        scheduleDetails.put("interval", 3);

        WorkspaceAPI workspace =
                ac.getWorkspaceInstance(orgId, workspaceId);

        JSONObject deploymentInfo = workspace.createAutoMLAnalysisDeployment(
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

        System.out.println("Deployment Details : " + deploymentInfo);
    }

    public void deployAutoMLAnalysis(AnalyticsClient ac) throws Exception {

        String analysisId = "466206000000182001";
        String deploymentId = "466206000000185059";

        WorkspaceAPI workspace =
                ac.getWorkspaceInstance(orgId, workspaceId);

        workspace.deployAutoMLAnalysis(analysisId, deploymentId, null);

        System.out.println("AutoML deployment executed successfully.");
    }

    public void deleteAutoMLDeployment(AnalyticsClient ac) throws Exception {

        String analysisId = "466206000000182001";
        String deploymentId = "466206000000185059";

        WorkspaceAPI workspace =
                ac.getWorkspaceInstance(orgId, workspaceId);

        workspace.deleteAutoMLAnalysisDeployment(analysisId, deploymentId, null);

        System.out.println("AutoML deployment deleted successfully.");
    }

    public void autoMLPrediction(AnalyticsClient ac) throws Exception {

        String analysisId = "466206000000182001";
        String modelId = "466206000000182005";

        JSONObject features = new JSONObject();
        features.put("Sales", 1000);
        features.put("Region", "East");
        features.put("Product Category", "Stationery");

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);

        JSONObject predictionResult = workspace.autoMLAnalysisPrediction(
                analysisId,
                modelId,
                features,
                null
        );

        System.out.println("Prediction Result : " + predictionResult);
    }




    public void getCustomRoles(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getCustomRoles();
        System.out.println(result);
    }
    public void createCustomRole(AnalyticsClient ac) throws Exception {
        String roleName = "DashboardPowerUser";
        // Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
        String accessType = "ALL_DASHBOARDS";

        JSONObject interactionPermissions = new JSONObject();
        interactionPermissions.put("read", true);
        interactionPermissions.put("vud", true);
        interactionPermissions.put("drillDown", true);
        interactionPermissions.put("insight", true);

        JSONObject sharePermissions = new JSONObject();
        sharePermissions.put("discussion", true);
        sharePermissions.put("privateLinks", true);

        JSONObject publishPermissions = new JSONObject();
        publishPermissions.put("export", true);

        JSONObject permissions = new JSONObject();
        permissions.put("interactionPermissions", interactionPermissions);
        permissions.put("sharePermissions", sharePermissions);
        permissions.put("publishPermissions", publishPermissions);

        OrgAPI org = ac.getOrgInstance(orgId);
        String result = org.createCustomRole(roleName, accessType, permissions, null);
        System.out.println(result);
    }
    public void updateCustomRole(AnalyticsClient ac) throws Exception {
        String roleId = "";
        String roleName = "DashboardPowerUser";
        // Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
        String accessType = "ALL_DASHBOARDS";

        JSONObject interactionPermissions = new JSONObject();
        interactionPermissions.put("read", true);
        interactionPermissions.put("vud", true);
        interactionPermissions.put("drillDown", false);
        interactionPermissions.put("insight", false);

        JSONObject sharePermissions = new JSONObject();
        sharePermissions.put("share", true);
        sharePermissions.put("privateLinks", false);

        JSONObject publishPermissions = new JSONObject();
        publishPermissions.put("export", true);

        JSONObject permissions = new JSONObject();
        permissions.put("interactionPermissions", interactionPermissions);
        permissions.put("sharePermissions", sharePermissions);
        permissions.put("publishPermissions", publishPermissions);

        OrgAPI org = ac.getOrgInstance(orgId);
        org.updateCustomRole(roleId, roleName, accessType, permissions, null);
        System.out.println("success");
    }
    public void deleteCustomRole(AnalyticsClient ac) throws Exception {
        String roleId = "";
        OrgAPI org = ac.getOrgInstance(orgId);
        org.deleteCustomRole(roleId);
        System.out.println("success");
    }
    public void getQueryTables(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getQueryTables(null);
        System.out.println(result);
    }
    public void getTags(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getTags();
        System.out.println(result);
    }
    public void createTag(AnalyticsClient ac) throws Exception {
        String tagName = "Sales Tag";
        String colorCode = "#FF5733";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createTag(tagName, colorCode, null);
        System.out.println(result);
    }
    public void updateTag(AnalyticsClient ac) throws Exception {
        long tagId = 0l;
        JSONObject config = new JSONObject();
        config.put("name", "Sales Tag Updated");
        config.put("colorCode", "#33FF57");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateTag(tagId, config);
        System.out.println("success");
    }
    public void deleteTag(AnalyticsClient ac) throws Exception {
        long tagId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteTag(tagId);
        System.out.println("success");
    }
    public void addTagToViews(AnalyticsClient ac) throws Exception {
        long tagId = 0l;
        JSONArray viewIds = new JSONArray();
        viewIds.put("");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.addTagToViews(tagId, viewIds, null);
        System.out.println("success");
    }
    public void removeTagFromViews(AnalyticsClient ac) throws Exception {
        long tagId = 0l;
        JSONArray viewIds = new JSONArray();
        viewIds.put("");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.removeTagFromViews(tagId, viewIds, false, null);
        System.out.println("success");
    }
    public void getTaggedViews(AnalyticsClient ac) throws Exception {
        long tagId = 0l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getTaggedViews(tagId);
        System.out.println(result);
    }
    public void getViewTags(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray result = view.getViewTags();
        System.out.println(result);
    }
    public void addTagsToView(AnalyticsClient ac) throws Exception {
        JSONArray tagIds = new JSONArray();
        tagIds.put("");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.addTagsToView(tagIds, null);
        System.out.println("success");
    }
    public void removeTagsFromView(AnalyticsClient ac) throws Exception {
        JSONArray tagIds = new JSONArray();
        tagIds.put("");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removeTagsFromView(tagIds, false, null);
        System.out.println("success");
    }

    public void refetchData(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("userName", "john@zylker.com");
        config.put("password", "Zoho@123");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.refetchData(config);
        System.out.println("success");
    }
    public void getAlertsInView(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray result = view.getAlertsInView();
        System.out.println(result);
    }
    public void getViewMetadataForAlert(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getViewMetadataForAlert();
        System.out.println(result);
    }
    public void createAlert(AnalyticsClient ac) throws Exception {
        String alertName = "Sales Drop Alert";

        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "daily");
        scheduleDetails.put("hour", 9);
        scheduleDetails.put("minute", 0);

        JSONObject rule = new JSONObject();
        rule.put("operator", "lt");
        rule.put("viewColumnIndex", "2");
        rule.put("type", "constant");
        rule.put("values", new JSONArray().put("1000"));

        JSONArray rules = new JSONArray();
        rules.put(rule);

        JSONObject email = new JSONObject();
        email.put("notifyAdmins", true);
        email.put("subject", "Sales dropped below threshold");
        email.put("message", "Please review the report.");

        JSONObject config = new JSONObject();
        config.put("email", email);

        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long result = view.createAlert(alertName, scheduleDetails, rules, config);
        System.out.println(result);
    }
    public void getAlertsInWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getAlertsInWorkspace();
        System.out.println(result);
    }
    public void getAlertConfiguration(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getAlertConfiguration(alertId);
        System.out.println(result);
    }
    public void updateAlert(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;
        String alertName = "Sales Drop Alert (weekly)";

        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "weekly");
        scheduleDetails.put("hour", 9);
        scheduleDetails.put("minute", 30);
        scheduleDetails.put("weekDays", new JSONArray().put(6));
        scheduleDetails.put("timeZone", "Asia/Kolkata");

        JSONObject rule = new JSONObject();
        rule.put("operator", "lt");
        rule.put("viewColumnIndex", "2");
        rule.put("type", "constant");
        rule.put("values", new JSONArray().put("1000"));

        JSONArray rules = new JSONArray();
        rules.put(rule);

        JSONObject email = new JSONObject();
        email.put("notifyAdmins", true);
        email.put("emailIds", new JSONArray().put("finance@example.com"));
        email.put("subject", "Weekly sales monitor");
        email.put("message", "Weekly alert summary.");

        JSONObject config = new JSONObject();
        config.put("email", email);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateAlert(alertId, alertName, scheduleDetails, rules, config);
        System.out.println("success");
    }
    public void deleteAlerts(AnalyticsClient ac) throws Exception {
        JSONArray alertIds = new JSONArray();
        alertIds.put("137687000010815003");
        alertIds.put("137687000010815005");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteAlerts(alertIds, null);
        System.out.println("success");
    }
    public void changeAlertStatus(AnalyticsClient ac) throws Exception {
        JSONArray alertIds = new JSONArray();
        alertIds.put("137687000010815003");
        alertIds.put("137687000010815005");
        boolean enabled = false;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeAlertStatus(alertIds, enabled, null);
        System.out.println("success");
    }
    public void runAlert(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;
        JSONObject config = new JSONObject();
        config.put("validateSystemTags", false);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.runAlert(alertId, config);
        System.out.println("success");
    }
    public void getAlertEvents(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;

        JSONObject config = new JSONObject();
        config.put("fromDate", "2026-05-01 00:00:00");
        config.put("toDate", "2026-05-31 23:59:59");
        config.put("status", new JSONArray().put("triggered").put("error"));
        config.put("pageNo", 1);
        config.put("recordsPerPage", 50);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getAlertEvents(alertId, config);
        System.out.println(result);
    }
    public void getLinkedWorkspaces(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getLinkedWorkspaces();
        System.out.println(result);
    }
    public void getLinkedWorkspacesForOrg(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getLinkedWorkspaces();
        System.out.println(result);
    }
    public void getLinkableWorkspaces(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getLinkableWorkspaces();
        System.out.println(result);
    }
    public void getWorkspaceLinkingCompatibility(AnalyticsClient ac) throws Exception {
        JSONObject client = new JSONObject();
        client.put("orgId", 700000654321l);
        client.put("workspaceIds", new JSONArray().put("466206000000071000"));

        JSONArray clients = new JSONArray();
        clients.put(client);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getWorkspaceLinkingCompatibility(clients, null);
        System.out.println(result);
    }
    public void linkWorkspaces(AnalyticsClient ac) throws Exception {
        JSONObject client = new JSONObject();
        client.put("orgId", 700000654321l);
        client.put("workspaceIds", new JSONArray().put("466206000000071000"));

        JSONArray clients = new JSONArray();
        clients.put(client);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.linkWorkspaces(clients, null);
        System.out.println("success");
    }
    public void unlinkWorkspaces(AnalyticsClient ac) throws Exception {
        String scope = "ALL";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.unlinkWorkspaces(scope, null);
        System.out.println("success");
    }
    public void syncLinkedWorkspaces(AnalyticsClient ac) throws Exception {
        String scope = "ALL";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.syncLinkedWorkspaces(scope, null);
        System.out.println("success");
    }
    public void getLinkedWorkspaceSyncDetails(AnalyticsClient ac) throws Exception {
        JSONArray sandboxIds = new JSONArray();
        sandboxIds.put("137687000012345001");
        sandboxIds.put("137687000012345002");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getLinkedWorkspaceSyncDetails(sandboxIds, null);
        System.out.println(result);
    }
    public void getWorkspaceBackups(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceBackups();
        System.out.println(result);
    }
    public void backupWorkspaceNow(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("backupMode", "STRUCTURE");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.backupWorkspaceNow(config);
        System.out.println(result);
    }
    public void getWorkspaceBackupStatus(AnalyticsClient ac) throws Exception {
        long backupId = 35130000001056701l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceBackupStatus(backupId);
        System.out.println(result);
    }
    public void downloadWorkspaceBackup(AnalyticsClient ac) throws Exception {
        long backupId = 35130000001056701l;
        String filePath = "/home/user/workspace-backup.zip";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.downloadWorkspaceBackup(backupId, filePath, null);
        System.out.println("success");
    }
    public void restoreWorkspaceFromBackup(AnalyticsClient ac) throws Exception {
        long backupId = 35130000001056701l;
        boolean confirmRestore = true;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.restoreWorkspaceFromBackup(backupId, confirmRestore, null);
        System.out.println(result);
    }
    public void getWorkspaceRestoreStatus(AnalyticsClient ac) throws Exception {
        long restoreId = 35130000001056801l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceRestoreStatus(restoreId);
        System.out.println(result);
    }
    public void createDashboard(AnalyticsClient ac) throws Exception {
        String displayName = "Sales Overview";
        String layout = "{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Sales Dashboard</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}";

        JSONObject settings = new JSONObject();
        settings.put("allowDrillDown", "true");
        settings.put("fitToWidth", "true");

        JSONObject config = new JSONObject();
        config.put("settings", settings);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createDashboard(displayName, layout, config);
        System.out.println(result);
    }
    public void updateDashboard(AnalyticsClient ac) throws Exception {
        long dashboardId = 35130000001055801l;
        String layout = "{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Updated Title</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}";

        JSONObject config = new JSONObject();
        config.put("layout", layout);

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateDashboard(dashboardId, config);
        System.out.println("success");
    }
    public void getDashboardMetadata(AnalyticsClient ac) throws Exception {
        long dashboardId = 35130000001055801l;
        JSONObject config = new JSONObject();
        config.put("include", "layout");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getDashboardMetadata(dashboardId, config);
        System.out.println(result);
    }
    public void getReportMetadata(AnalyticsClient ac) throws Exception {
        long reportId = 35130000001055901l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getReportMetadata(reportId);
        System.out.println(result);
    }
    public void getOrgWorkspaces(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getOrgWorkspaces();
        System.out.println(result);
    }
    public void getOrgAccessRestrictions(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONObject result = org.getOrgAccessRestrictions();
        System.out.println(result);
    }
    public void updateOrgAccessRestrictions(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("accessRestrictionEnabled", true);
        OrgAPI org = ac.getOrgInstance(orgId);
        org.updateOrgAccessRestrictions(config);
        System.out.println("success");
    }
    public void getWorkspaceAccessRestrictions(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceAccessRestrictions();
        System.out.println(result);
    }
    public void updateWorkspaceAccessRestrictions(AnalyticsClient ac) throws Exception {
        JSONObject shareViews = new JSONObject();
        shareViews.put("domainRestrictionEnabled", true);
        shareViews.put("trustedDomains", new JSONArray().put("example.com").put("partner.example.org"));

        JSONObject config = new JSONObject();
        config.put("useOrganizationSettings", false);
        config.put("shareViews", shareViews);
        config.put("privateLinks", new JSONObject().put("enabled", false));
        config.put("publicViews", new JSONObject().put("enabled", false));
        config.put("exportViews", new JSONObject().put("enabled", true));

        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateWorkspaceAccessRestrictions(config);
        System.out.println("success");
    }

    public void setAccessToken(AnalyticsClient ac) throws Exception {
        // Use this when you already hold a valid access token and do not want the
        // SDK to generate one from the refresh token.
        String accessToken = "1000.xxxxxxx.xxxxxxx";
        ac.setAccessToken(accessToken);
        System.out.println("success");
    }

    public void setHeaders(AnalyticsClient ac) throws Exception {
        // Key accepts alphanumeric characters and hyphens only; value cannot contain newlines.
        ac.setHeaders("X-Custom-Source", "nightly-sync");
        System.out.println("success");
    }

    public void handleCustomBatchImport(AnalyticsClient ac) throws Exception {
        // Drives the batch import job manually, one chunk at a time. Use this when you
        // split the CSV yourself; importDataAsBatches does the same splitting for you.
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);

        String[] batchFiles = {
            "/home/user/sales-part-1.csv",
            "/home/user/sales-part-2.csv",
            "/home/user/sales-part-3.csv"
        };

        String batchKey = "start";

        for(int i = 0; i < batchFiles.length; i++) {
            JSONObject config = new JSONObject();
            config.put("batchKey", batchKey);
            config.put("isLastBatch", i == batchFiles.length - 1);

            if("start".equals(batchKey)) {
                // importType and autoIdentify are mandatory on the first batch only.
                config.put("importType", "APPEND");
                config.put("autoIdentify", true);
            }

            JSONObject response = bulk.handleCustomBatchImport(viewId, batchFiles[i], config);

            // The server returns the key to use for every following batch.
            batchKey = response.getString("batchKey");
            System.out.println(response);
        }
    }
}
