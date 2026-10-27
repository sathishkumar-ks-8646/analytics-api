// $Id$
package com.zoho.analytics.client;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * BulkAPI contains bulk data operation.
 */
public class BulkAPI {
    private final AnalyticsClient ac;
    private final String dataEndPoint;
    private final String bulkDataEndPoint;
    Map<String, String> reqHeader = new HashMap<>();

    /**
     * Creates a new <code>BulkAPI</code> instance.
     * @param ac <code>AnalyticsClient</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     */
    protected BulkAPI(AnalyticsClient ac, long orgId, long workspaceId){
        this.ac = ac;
        dataEndPoint = "/restapi/v2/workspaces/" + workspaceId;
        bulkDataEndPoint = "/restapi/v2/bulk/workspaces/" + workspaceId;
        reqHeader.put("ZANALYTICS-ORGID", String.valueOf(orgId));
    }

    /**
     * Create a new table and import the data contained in the mentioned file into the created table.
     * @param tableName Name of the new table to be created.
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of import result.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject importDataInNewTable(String tableName, String fileType, boolean autoIdentify, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("tableName", tableName);
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);

        File file = new File(filePath);
        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, file);
        return response.getJSONObject("data");
    }

    /**
     * Import the data contained in the mentioned file into the table.
     * @param viewId Id of the view where the data to be imported.
     * @param importType The type of import. Can be one of <ul><li>append</li><li>truncateadd</li><li>updateadd</li></ul>
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of import result.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject importData(long viewId, String importType, String fileType, boolean autoIdentify, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/views/" + viewId + "/data";

        config = (config == null) ? new JSONObject() : config;
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);
        config.put("importType", importType);

        File file = new File(filePath);
        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, file);
        return response.getJSONObject("data");
    }

    /**
     * Create a new table and import the raw data provided into the created table.
     * @param tableName Name of the new table to be created.
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param data Raw data to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of import result.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject importRawDataInNewTable(String tableName, String fileType, boolean autoIdentify, String data, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("tableName", tableName);
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);

        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, data);
        return response.getJSONObject("data");
    }

    /**
     * Import the raw data provided into the table.
     * @param viewId Id of the view where the data to be imported.
     * @param importType The type of import. Can be one of <ul><li>APPEND</li><li>TRUNCATEADD</li><li>UPDATEADD</li></ul>
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param data Raw data to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of import result.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject importRawData(long viewId, String importType, String fileType, boolean autoIdentify, String data, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/views/" + viewId + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);
        config.put("importType", importType);

        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, data);
        return response.getJSONObject("data");
    }

    /**
     * Asynchronously create a new table and import the data contained in the mentioned file into the created table.
     * @param tableName Name of the new table to be created.
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of the job id created.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long importBulkDataInNewTable(String tableName, String fileType, boolean autoIdentify, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("tableName", tableName);
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);

        File file = new File(filePath);
        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, file);
        String jobId =  response.getJSONObject("data").getString("jobId");
        return Long.valueOf(jobId);
    }

    /**
     * Asynchronously import the data contained in the mentioned file into the table.
     * @param viewId Id of the view where the data to be imported.
     * @param importType The type of import. Can be one of <ul><li>APPEND</li><li>TRUNCATEADD</li><li>UPDATEADD</li></ul>
     * @param fileType Type of the file to be imported.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of job id created.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long importBulkData(long viewId, String importType, String fileType, boolean autoIdentify, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/views/" + viewId + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("fileType", fileType);
        config.put("autoIdentify", autoIdentify);
        config.put("importType", importType);

        File file = new File(filePath);
        JSONObject response = ac.sendImportAPIRequest(endPoint, config, reqHeader, file);
        String jobId =  response.getJSONObject("data").getString("jobId");
        return Long.valueOf(jobId);
    }

    /**
     * Returns the details of the import job.
     * @param jobId Id of the import job.
     * @return A <code>JSONObject</code> of import result.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getImportJobDetails(long jobId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/importjobs/" + jobId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Export the mentioned table (or) view data.
     * @param viewId Id of the view to be exported.
     * @param responseFormat The format in which the data is to be exported.
     * @param filePath Path of the file where the data exported to be stored.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void exportData(long viewId, String responseFormat,  String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/views/" + viewId + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("responseFormat", responseFormat);
        File file = new File(filePath);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, file);
    }

    /**
     * Export the mentioned table (or) view data.
     * @param viewId Id of the view to be exported.
     * @param responseFormat The format in which the data is to be exported.
     * @param stream Outputstream where the data exported to be stored.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void exportData(long viewId, String responseFormat, OutputStream stream, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/views/" + viewId + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("responseFormat", responseFormat);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, stream);
    }

    /**
         * Internally used in JDBC driver
     */
    public void exportDataUsingSQL(String sqlQuery, String responseFormat, OutputStream stream, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("sqlQuery", sqlQuery);
        config.put("responseFormat", responseFormat);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, stream);
    }

    /**
         * Internally used in JDBC driver
     */
    public void exportDataUsingSQL(String sqlQuery, String responseFormat, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = dataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("sqlQuery", sqlQuery);
        config.put("responseFormat", responseFormat);
        File file = new File(filePath);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, file);
    }

    /**
     * Initiate asynchronous export for the mentioned table (or) view data.
     * @param viewId Id of the view to be exported.
     * @param responseFormat The format in which the data is to be exported.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long initiateBulkExport(long viewId, String responseFormat, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/views/" + viewId + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("responseFormat", responseFormat);
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        String jobId =  response.getJSONObject("data").getString("jobId");
        return Long.valueOf(jobId);
    }

    /**
     * Initiate asynchronous export with the given SQL Query.
     * @param sqlQuery The SQL Query whose output is exported.
     * @param responseFormat The format in which the data is to be exported.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long initiateBulkExportUsingSQL(String sqlQuery, String responseFormat, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("sqlQuery", sqlQuery);
        config.put("responseFormat", responseFormat);
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        String jobId =  response.getJSONObject("data").getString("jobId");
        return Long.valueOf(jobId);
    }

    /**
     * Returns the details of the export job.
     * @param jobId Id of the export job.
     * @return A <code>JSONObject</code> of export job details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getExportJobDetails(long jobId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/exportjobs/" + jobId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Download the exported data for the mentioned job id.
     * @param jobId Id of the job to be exported.
     * @param filePath Path of the file where the data exported to be stored.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void exportBulkData(long jobId, String filePath) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/exportjobs/" + jobId + "/data";
        File file = new File(filePath);
        ac.sendExportAPIRequest(endPoint, null, reqHeader, file);
    }

    /**
     * Download the exported data for the mentioned job id.
     * @param jobId Id of the job to be exported.
     * @param stream Outputstream where the data exported to be stored.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void exportBulkData(long jobId, OutputStream stream) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = bulkDataEndPoint + "/exportjobs/" + jobId + "/data";
        ac.sendExportAPIRequest(endPoint, null, reqHeader, stream);
    }


     /**
     * Create a new table and import the data contained in the mentioned file into the created table.
     * @param tableName Name of the new table to be created.
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param batchSize Number of lines per batch.
     * @param config Contains any additional control configurations. Can be null.
     * @param toolConfig Contains any additional control configurations for the parser tool. Can be null.
     * @return A <code>long</code> of the job id created.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long importDataInNewTableAsBatches(String tableName, boolean autoIdentify, String filePath, int batchSize, JSONObject config, JSONObject toolConfig) throws ServerException, ParseException, IOException, JSONException, Exception {
        String endPoint = bulkDataEndPoint + "/data/batch";
        config = (config == null) ? new JSONObject() : config;
        config.put("tableName", tableName);
        config.put("autoIdentify", autoIdentify);
        config.put("batchKey", "start");

        File file = new File(filePath);
        JSONObject response = ac.importDataInBatches(endPoint, config, reqHeader, file, batchSize, toolConfig);
        return Long.valueOf(response.getString("jobId"));
    }

    /**
     * Asynchronously import the data contained in the mentioned file into the table.
     * @param viewId Id of the view where the data to be imported.
     * @param importType The type of import. Can be one of <ul><li>APPEND</li><li>TRUNCATEADD</li><li>UPDATEADD</li></ul>
     * @param autoIdentify Used to specify whether to auto identify the CSV format.
     * @param filePath Path of the file to be imported.
     * @param batchSize Number of lines per batch.
     * @param config Contains any additional control configurations. Can be null.
     * @param toolConfig Contains any additional control configurations for the parser tool. Can be null.
     * @return A <code>long</code> of job id created.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long importDataAsBatches(long viewId, String importType, boolean autoIdentify, String filePath, int batchSize, JSONObject config, JSONObject toolConfig) throws ServerException, ParseException, IOException, JSONException, Exception {
        String endPoint = bulkDataEndPoint + "/views/" + viewId + "/data/batch";
        config = (config == null) ? new JSONObject() : config;
        config.put("importType", importType);
        config.put("autoIdentify", autoIdentify);
        config.put("batchKey", "start");

        File file = new File(filePath);
        JSONObject response = ac.importDataInBatches(endPoint, config, reqHeader, file, batchSize, toolConfig);
        return Long.valueOf(response.getString("jobId"));
    }

    public JSONObject handleCustomBatchImport(long viewId, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException, Exception {
        String endPoint = this.bulkDataEndPoint + "/views/" + viewId + "/data/batch";
        config = (config == null) ? new JSONObject() : config;
        File file = new File(filePath);
        JSONObject response = this.ac.sendImportAPIRequest(endPoint, config, this.reqHeader, file);
        return response.getJSONObject("data");
    }

}
