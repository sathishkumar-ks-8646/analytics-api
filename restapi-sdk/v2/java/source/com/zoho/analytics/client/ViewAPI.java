// $Id$
package com.zoho.analytics.client;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * ViewAPI contains view level operations.
 */
public class ViewAPI {
    private final AnalyticsClient ac;
    private final String viewEndPoint;
    private final Map<String, String> reqHeader = new HashMap<>();

    /**
     * Creates a new <code>ViewAPI</code> instance.
     * @param ac <code>AnalyticsClient</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     * @param viewId The ID of the view.
     */
    protected ViewAPI(AnalyticsClient ac, long orgId, long workspaceId, long viewId){
        this.ac = ac;
        viewEndPoint = "/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId;
        reqHeader.put("ZANALYTICS-ORGID", String.valueOf(orgId));
    }

    /**
     * Add a single row in the specified table.
     * @param columnValues Contains the values for the row. The column names are the key.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of values of the added rows.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject addRow(JSONObject columnValues, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/rows";
        config = (config == null) ? new JSONObject() : config;
        config.put("columns", columnValues);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Update rows in the specified table.
     * @param columnValues Contains the values for the row. The column names are the key.
     * @param criteria The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of values of the updated rows.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject updateRow(JSONObject columnValues, String criteria, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/rows";
        config = (config == null) ? new JSONObject() : config;
        config.put("columns", columnValues);
        if(criteria != null) {
            config.put("criteria", criteria);
        }
        JSONObject response = ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Delete rows in the specified table.
     * @param criteria The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>int</code> of deleted rows count.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public int deleteRow(String criteria, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/rows";
        config = (config == null) ? new JSONObject() : config;
        if(criteria != null) {
            config.put("criteria", criteria);
        }
        JSONObject response = ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
        return response.getJSONObject("data").getInt("deletedRows");
    }

    /**
     * Rename a specified view in the workspace.
     * @param viewName The new name of the view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void rename(String viewName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        config = (config == null) ? new JSONObject() : config;
        config.put("viewName", viewName);
        ac.sendAPIRequest("PUT", viewEndPoint, config, reqHeader);
    }

    /**
     * Delete a specified view in the workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void delete(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        ac.sendAPIRequest("DELETE", viewEndPoint, config, reqHeader);
    }

    /**
     * Copy a specified view within the workspace.
     * @param newViewName The name of the new view.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of view id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long saveAs(String newViewName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/saveas";
        config = (config == null) ? new JSONObject() : config;
        config.put("viewName", newViewName);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String viewId = response.getJSONObject("data").getString("viewId");
        return Long.valueOf(viewId);
    }

    /**
     * Create reports for the specified table based on the reference table.
     * @param refViewId The ID of the reference view.
     * @param folderId The folder id where the views to be saved.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void createSimilarViews(long refViewId, long folderId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/similarviews";
        config = (config == null) ? new JSONObject() : config;
        config.put("referenceViewId", refViewId);
        config.put("folderId", folderId);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Auto generate reports for the specified table.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void autoAnalyse(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/autoanalyse";
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Adds a specified view as favorite.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addFavorite() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/favorite";
        ac.sendAPIRequest("POST", endPoint, null, reqHeader);
    }

    /**
     * Remove a specified view from favorite.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeFavorite() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/favorite";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns the URL to access the specified view.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of view URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getViewURL(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("viewUrl");
    }

    /**
     * Returns embed URL to access the specified view.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of Embed URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getEmbedURL(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/embed";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("embedUrl");
    }

    /**
     * Returns private URL to access the specified view.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of private URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getPrivateURL(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/privatelink";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("privateUrl");
    }

    /**
     * Create a private URL for the specified view.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of private URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String createPrivateURL(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/privatelink";
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("privateUrl");
    }

    /**
     * Remove private link access for the specified view.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removePrivateAccess() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/privatelink";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Make the specified view publically accessible.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of public URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String makeViewPublic(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/public";
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("publicUrl");
    }

    /**
     * Remove public access for the specified view.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removePublicAccess() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/public";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns publish configurations for the specified view.
     * @return A <code>JSONObject</code> of publish details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getPublishConfigurations() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/config";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Update publish configurations for the specified view.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updatePublishConfigurations(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/publish/config";
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Returns permissions for the specified view.
     * @return A <code>JSONObject</code> of permission details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getMyPermissions() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/share/userpermissions";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("permissions");
    }

    /**
     * Add a column in the specified table.
     * @param columnName The name of the column.
     * @param dataType The data-type of the column.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of column id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long addColumn(String columnName, String dataType, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns";
        config = (config == null) ? new JSONObject() : config;
        config.put("columnName", columnName);
        config.put("dataType", dataType);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String columnId = response.getJSONObject("data").getString("columnId");
        return Long.valueOf(columnId);
    }

    /**
     * Rename a specified column in the table.
     * @param columnId The id of the column.
     * @param columnName The new name of the column.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void renameColumn(long columnId, String columnName) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/" + columnId;
        JSONObject config = new JSONObject();
        config.put("columnName", columnName);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete a specified column in the table.
     * @param columnId The id of the column.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteColumn(long columnId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/" + columnId;
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Add a lookup in the specified child table.
     * @param columnId The id of the column.
     * @param refViewId The ID of the table contains the parent column.
     * @param refColumnId The ID of the parent column.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addLookup(long columnId, long refViewId, long refColumnId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/" + columnId + "/lookup";
        config = (config == null) ? new JSONObject() : config;
        config.put("referenceViewId", refViewId);
        config.put("referenceColumnId", refColumnId);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove the lookup for the specified column in the table.
     * @param columnId The id of the column.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeLookup(long columnId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/" + columnId + "/lookup";
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Hide the specified columns in the table.
     * @param columnIds The array of column ids to be hidden.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void hideColumns(JSONArray columnIds) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/hide";
        JSONObject config = new JSONObject();
        config.put("columnIds", columnIds);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Show the specified hidden columns in the table.
     * @param columnIds The array of column ids to be shown.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void showColumns(JSONArray columnIds) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/show";
        JSONObject config = new JSONObject();
        config.put("columnIds", columnIds);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Auto generate reports for the specified column.
     * @param columnId The id of the column.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void autoAnalyseColumn(long columnId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/" + columnId + "/autoanalyse";
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Copy the specified formulas from one table to another within the workspace or across workspaces.
     * @param formulaNames The name of the formula columns to be copied.
     * @param destWorkspaceId The ID of the destination workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @param destOrgId Id of the organization where the destination workspace is present. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void copyFormulas(JSONArray formulaNames, long destWorkspaceId, JSONObject config, Long destOrgId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/formulas/copy";
        config = (config == null) ? new JSONObject() : config;
        config.put("formulaColumnNames", formulaNames);
        config.put("destWorkspaceId", destWorkspaceId);
        Map<String, String> header = new HashMap<>();
        header.putAll(reqHeader);
        if(destOrgId != null)
        {
            header.put("ZANALYTICS-DEST-ORGID", String.valueOf(destOrgId));
        }
        ac.sendAPIRequest("POST", endPoint, config, header);
    }

    /**
     * Sync data from available datasource for the specified view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void refetchData(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/sync";
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Returns last import details of the specified view.
     * @return A <code>JSONObject</code> of last import details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getLastImportDetails() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/importdetails";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns list of all formula columns for the specified table.
     * @return A <code>JSONArray</code> of custom formulas.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getFormulaColumns() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/formulacolumns";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("formulaColumns");
    }

    /**
     * Add a formula column in the specified table.
     * @param formulaName Name of the formula column to be created.
     * @param expression Formula expression.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of created formula id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long addFormulaColumn(String formulaName, String expression, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/formulacolumns";
        config = (config == null) ? new JSONObject() : config;
        config.put("formulaName", formulaName);
        config.put("expression", expression);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String formulaId = response.getJSONObject("data").getString("formulaId");
        return Long.valueOf(formulaId);
    }

    /**
     * Edit the specified formula column.
     * @param formulaId Id of the formula column to be updated.
     * @param expression Formula expression.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void editFormulaColumn(long formulaId, String expression, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/formulacolumns/" + formulaId;
        config = (config == null) ? new JSONObject() : config;
        config.put("expression", expression);

        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete the specified formula column.
     * @param formulaId Id of the formula column to be deleted.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteFormulaColumn(long formulaId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/formulacolumns/" + formulaId;
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns list of all aggregate formulas for the specified table.
     * @return A <code>JSONArray</code> of aggregate formulas.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAggregateFormulas() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/aggregateformulas";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("aggregateFormulas");
    }

    /**
     * Add a aggregate formula in the specified table.
     * @param formulaName Name of the aggregate formula to be created.
     * @param expression Formula expression.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of created formula id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long addAggregateFormula(String formulaName, String expression, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/aggregateformulas";
        config = (config == null) ? new JSONObject() : config;
        config.put("formulaName", formulaName);
        config.put("expression", expression);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String formulaId = response.getJSONObject("data").getString("formulaId");
        return Long.valueOf(formulaId);
    }

    /**
     * Edit the specified aggregate formula.
     * @param formulaId Id of the aggregate formula to be updated.
     * @param expression Formula expression.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void editAggregateFormula(long formulaId, String expression, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/aggregateformulas/" + formulaId;
        config = (config == null) ? new JSONObject() : config;
        config.put("expression", expression);

        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete the specified aggregate formula.
     * @param formulaId Id of the aggregate formula to be deleted.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteAggregateFormula(long formulaId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/aggregateformulas/" + formulaId;
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns list of dependents views for the specified view.
     * @return A <code>JSONArray</code> of dependent views.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getViewDependents() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/dependents";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("views");
    }

    /**
     * Returns list of dependents views and formulas for the specified column.
     * @param columnId Id of the column.
     * @return A <code>JSONObject</code> of dependent views and formulas.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getColumnDependents(long columnId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/columns/"+ columnId + "/dependents";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

        /**
     * Update the existing sharing configuration for the specified view.
     * @param config Contains the required control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void UpdateSharedDetails(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/share";
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Retrieves metadata information for the current table, including
     * the list of available columns and their attributes.
     *
     * @return A <code>JSONObject</code> containing table metadata.
     * @throws ServerException If the server has received the request but did not process it.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject getTableMetadata()
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint = viewEndPoint + "/metadata";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Updates the column order of the current table.
     *
     * @param columnIds JSONArray containing the full set of column IDs in the new order in which they should appear.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void reorderColumns(JSONArray columnIds, JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint = viewEndPoint + "/columns/reorder";
        config = (config == null) ? new JSONObject() : config;
        config.put("columns", columnIds);

        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Sorts the data in the current table based on specified columns.
     *
     * @param columnIds JSONArray of column IDs to sort by.
     * @param sortOrder Sorting order:
     *                  1 - Ascending
     *                  2 - Descending
     * @param resetSort If true, resets existing sort configuration.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void sortDataByColumns(
            JSONArray columnIds,
            Integer sortOrder,
            boolean resetSort,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint = viewEndPoint + "/data/sort";
        config = (config == null) ? new JSONObject() : config;

        if (resetSort) {
            config.put("resetSort", "true");
        } else {
            config.put("columns", columnIds);
            config.put("sortOrder", sortOrder);
        }

        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }




    /**
     * Returns the list of tags associated with the specified view.
     * @return A <code>JSONArray</code> of tags.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getViewTags() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/tags";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("tags");
    }
    /**
     * Adds multiple tags to the specified view.
     * @param tagIds List of tag ids to be associated with the view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addTagsToView(JSONArray tagIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/tags";
        config = (config == null) ? new JSONObject() : config;
        config.put("tagIds", tagIds);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }
    /**
     * Removes multiple tags from the specified view.
     * @param tagIds List of tag ids to be dissociated. Can be null when dissociateAll is true.
     * @param dissociateAll To dissociate all the associated tags from the view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeTagsFromView(JSONArray tagIds, boolean dissociateAll, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/tags";
        config = (config == null) ? new JSONObject() : config;
        if(dissociateAll) {
            config.put("dissociateAll", true);
        } else {
            config.put("tagIds", tagIds);
        }
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns list of data alerts configured for the specified view.
     * @return A <code>JSONArray</code> of data alerts.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAlertsInView() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/alerts";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("alerts");
    }

    /**
     * Create a data alert for the specified view.
     * @param alertName Name of the data alert.
     * @param scheduleDetails Contains the schedule configurations of the data alert.
     * @param rules Contains the rules to be evaluated by the data alert.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of new data alert id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createAlert(String alertName, JSONObject scheduleDetails, JSONArray rules, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/alerts";
        config = (config == null) ? new JSONObject() : config;
        config.put("alertName", alertName);
        config.put("scheduleDetails", scheduleDetails);
        config.put("rules", rules);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String alertId = response.getJSONObject("data").getString("alertId");
        return Long.valueOf(alertId);
    }

    /**
     * Returns the view metadata that can be used while configuring a data alert for the specified view.
     * @return A <code>JSONObject</code> of view metadata for data alert configuration.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getViewMetadataForAlert() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = viewEndPoint + "/alerts/metadata";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

}
