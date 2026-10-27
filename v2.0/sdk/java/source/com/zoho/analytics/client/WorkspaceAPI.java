// $Id$
package com.zoho.analytics.client;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * WorkspaceAPI contains workspace level operations.
 */
public class WorkspaceAPI {
    private final AnalyticsClient ac;
    private final long orgId;
    private final long workspaceId;
    private final String workspaceEndPoint;
    private final String securityControlsEndPoint;
    private final Map<String, String> reqHeader = new HashMap<>();

    /**
     * Creates a new <code>WorkspaceAPI</code> instance.
     * @param ac <code>AnalyticsClient</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     */
    protected WorkspaceAPI(AnalyticsClient ac, long orgId, long workspaceId){
        this.ac = ac;
        this.orgId = orgId;
        this.workspaceId = workspaceId;
        workspaceEndPoint = "/restapi/v2/workspaces/" + workspaceId;
        securityControlsEndPoint = "/restapi/v2/security-controls/workspaces/" + workspaceId;
        reqHeader.put("ZANALYTICS-ORGID", String.valueOf(orgId));
    }

    /**
     * Returns details of the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of workspace details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getWorkspaceDetails(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        JSONObject response = ac.sendAPIRequest("GET", workspaceEndPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONObject("workspaces");
    }

    /**
     * Rename a specified workspace in the organization.
     * @param workspaceName New name of the workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void rename(String workspaceName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        config = (config == null) ? new JSONObject() : config;
        config.put("workspaceName", workspaceName);
        ac.sendAPIRequest("PUT", workspaceEndPoint, config, reqHeader);
    }

    /**
     * Delete a specified workspace in the organization.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void delete() throws ServerException, ParseException, IOException, JSONException {
        ac.sendAPIRequest("DELETE", workspaceEndPoint, null, reqHeader);
    }

    /**
     * Returns the secret key of the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of workspace secret key.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getSecretKey(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/secretkey";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("workspaceKey");
    }

    /**
     * Copy the specified workspace from one organization to another or within the organization.
     * @param newWorkspaceName Name of the new workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @param destOrgId Id of the organization where the destination workspace is present. Can be null.
     * @return A <code>long</code> of new workspace id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long copy(String newWorkspaceName, JSONObject config, Long destOrgId) throws ServerException, ParseException, IOException, JSONException {
        config = (config == null) ? new JSONObject() : config;
        config.put("newWorkspaceName", newWorkspaceName);
        Map<String, String> header = new HashMap<>();
        header.putAll(reqHeader);
        if(destOrgId != null)
        {
            header.put("ZANALYTICS-DEST-ORGID", String.valueOf(destOrgId));
        }
        JSONObject response = ac.sendAPIRequest("POST", workspaceEndPoint, config, header);
        String workspaceId = response.getJSONObject("data").getString("workspaceId");
        return Long.valueOf(workspaceId);
    }

    /**
     * Adds a specified workspace as favorite.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addFavorite() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/favorite";
        ac.sendAPIRequest("POST", endPoint, null, reqHeader);
    }

    /**
     * Remove a specified workspace from favorite.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeFavorite() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/favorite";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Adds a specified workspace as default.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addDefault() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/default";
        ac.sendAPIRequest("POST", endPoint, null, reqHeader);
    }

    /**
     * Remove a specified workspace from default.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeDefault() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/default";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Enable workspace to the specified white label domain.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void enableDomainAccess() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/wlaccess";
        ac.sendAPIRequest("POST", endPoint, null, reqHeader);
    }

    /**
     * Disable workspace from the specified white label domain.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void disableDomainAccess() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/wlaccess";
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Deprecated.
     */
    public JSONArray getViews() throws ServerException, ParseException, IOException, JSONException {
        return getViews(null);
    }

    /**
     * Returns list of all accessible views for the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONArray</code> of views list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getViews(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/views";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONArray("views");
    }

    /**
     * Create a table in the specified workspace.
     * @param tableDesign JSON object of table structure.
     * @return A <code>long</code> of table id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createTable(JSONObject tableDesign) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tables";
        JSONObject config = new JSONObject();
        config.put("tableDesign", tableDesign);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String viewId = response.getJSONObject("data").getString("viewId");
        return Long.valueOf(viewId);
    }

    /**
     * Copy the specified views from one workspace to another workspace.
     * @param viewIds The id of the views to be copied.
     * @param destWorkspaceId The destination workspace id.
     * @param config Contains any additional control configurations. Can be null.
     * @param destOrgId Id of the organization where the destination workspace is present. Can be null.
     * @return A <code>JSONArray</code> of views list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray copyViews(JSONArray viewIds, long destWorkspaceId, JSONObject config, Long destOrgId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/views/copy";
        config = (config == null) ? new JSONObject() : config;
        config.put("viewIds", viewIds);
        config.put("destWorkspaceId", destWorkspaceId);
        Map<String, String> header = new HashMap<>();
        header.putAll(reqHeader);
        if(destOrgId != null)
        {
            header.put("ZANALYTICS-DEST-ORGID", String.valueOf(destOrgId));
        }

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, header);
        return response.getJSONObject("data").getJSONArray("views");
    }

    /**
     * Returns list of all accessible folders for the specified workspace.
     * @return A <code>JSONArray</code> of folders list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getFolders() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("folders");
    }

    /**
     * Create a folder in the specified workspace.
     * @param folderName The name of the folder.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of folder id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createFolder(String folderName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders";
        config = (config == null) ? new JSONObject() : config;
        config.put("folderName", folderName);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String folderId = response.getJSONObject("data").getString("folderId");
        return Long.valueOf(folderId);
    }

    /**
     * Rename a specified folder in the workspace.
     * @param folderId The id of the folder.
     * @param folderName The new name of the folder.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void renameFolder(long folderId, String folderName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders/" + folderId;
        config = (config == null) ? new JSONObject() : config;
        config.put("folderName", folderName);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete a specified folder in the workspace.
     * @param folderId The id of the folder.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteFolder(long folderId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders/" + folderId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns list of groups for the specified workspace.
     * @return A <code>JSONArray</code> of groups list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getGroups() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("groups");
    }

    /**
     * Returns details of the specified group.
     * @param groupId The id of the group.
     * @return A <code>JSONObject</code> of group details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getGroupDetails(long groupId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups/" + groupId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("groups");
    }

    /**
     * Create a group in the specified workspace.
     * @param groupName Name of the group.
     * @param emailIds The email address of the users to be added to the group.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of group id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String createGroup(String groupName, JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups";
        config = (config == null) ? new JSONObject() : config;
        config.put("groupName", groupName);
        config.put("emailIds", emailIds);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("groupId");
    }

    /**
     * Rename a specified group.
     * @param groupId The id of the group.
     * @param groupName The new name of the group.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void renameGroup(long groupId, String groupName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups/" + groupId;
        config = (config == null) ? new JSONObject() : config;
        config.put("groupName", groupName);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete a specified group.
     * @param groupId The id of the group.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteGroup(long groupId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups/" + groupId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Add users to the specified group.
     * @param groupId The id of the group.
     * @param emailIds The email address of the users to be added to the group.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addGroupMembers(long groupId, JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups/" + groupId + "/members";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove users from the specified group.
     * @param groupId The id of the group.
     * @param emailIds The email address of the users to be removed from the group.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeGroupMembers(long groupId, JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/groups/" + groupId + "/members";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns list of admins for the specified workspace.
     * @return A <code>JSONArray</code> of workspace admins.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAdmins() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/admins";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("workspaceAdmins");
    }

    /**
     * Add admins for the specified workspace.
     * @param emailIds The email address of the admin users to be added.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addAdmins(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/admins";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove admins from the specified workspace.
     * @param emailIds The email address of the admin users to be removed.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeAdmins(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/admins";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns shared details of the specified workspace.
     * @return A <code>ShareInfo</code> object.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public ShareInfo getShareInfo() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/share";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return new ShareInfo(response.getJSONObject("data"));
    }

    /**
     * Share views to the specified users.
     * @param viewIds View ids which to be shared.
     * @param emailIds The email address of the users to whom the views need to be shared.
     * @param permissions Contains permission details.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void shareViews(JSONArray viewIds, JSONArray emailIds, JSONObject permissions, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/share";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        config.put("viewIds", viewIds);
        config.put("permissions", permissions);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove shared views for the specified users.
     * @param viewIds View ids whose sharing needs to be removed.
     * @param emailIds The email address of the users to whom the sharing need to be removed.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeShare(JSONArray viewIds, JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/share";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        if(viewIds != null) {
            config.put("viewIds", viewIds);
        }
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Returns shared details of the specified views.
     * @param viewIds Ids of the view to be included in the slideshow.
     * @return A <code>JSONArray</code> of shared info of views.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getSharedDetailsForViews(JSONArray viewIds) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/share/shareddetails";
        JSONObject config = new JSONObject();
        config.put("viewIds", viewIds);
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        JSONArray sharedDetails = response.getJSONObject("data").getJSONArray("sharedDetails");
        return sharedDetails;
    }

    /**
     * Returns list of slideshows for the specified workspace.
     * @return A <code>JSONArray</code> of slideshows.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getSlideshows() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        JSONArray slideshows = response.getJSONObject("data").getJSONArray("slideshows");
        return slideshows;
    }

    /**
     * Returns details of the specified slideshow.
     * @param slideId The id of the slideshow.
     * @return A <code>JSONObject</code> of slideshow details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getSlideshowDetails(long slideId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides/" + slideId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("slideInfo");
    }

    /**
     * Returns slide URL to access the specified slideshow.
     * @param slideId The id of the slideshow.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of slideshow URL.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getSlideshowURL(long slideId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides/" + slideId + "/publish";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("slideUrl");
    }

    /**
     * Create a slideshow in the specified workspace.
     * @param slideName Name of the slideshow to be created.
     * @param viewIds Ids of the view to be included in the slideshow.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of created slideshow id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createSlideshow(String slideName, JSONArray viewIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides";
        config = (config == null) ? new JSONObject() : config;
        config.put("slideName", slideName);
        config.put("viewIds", viewIds);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String slideId = response.getJSONObject("data").getString("slideId");
        return Long.valueOf(slideId);
    }

    /**
     * Update details of the specified slideshow.
     * @param slideId The id of the slideshow.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateSlideshow(long slideId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides/" + slideId;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete a specified slideshow in the workspace.
     * @param slideId The id of the slideshow.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteSlideshow(long slideId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/slides/" + slideId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Create a variable in the workspace.
     * @param variableName Name of the variable to be created.
     * @param variableDataType Datatype of the variable to be created.
     * @param variableType Type of the variable to be created.
     * @param config Contains the control configurations.
     * @return A <code>long</code> of created variable id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createVariable(String variableName, int variableDataType, int variableType, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/variables";
        config = (config == null) ? new JSONObject() : config;
        config.put("variableName", variableName);
        config.put("variableDataType", variableDataType);
        config.put("variableType", variableType);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String variableId = response.getJSONObject("data").getString("variableId");
        return Long.valueOf(variableId);
    }

    /**
     * Update details of the specified variable in the workspace.
     * @param variableId Id for the variable.
     * @param variableName Name of the variable to be created.
     * @param variableDataType Datatype of the variable to be created.
     * @param variableType Type of the variable to be created.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateVariable(long variableId, String variableName, int variableDataType, int variableType, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/variables/" + variableId;
        config = (config == null) ? new JSONObject() : config;
        config.put("variableName", variableName);
        config.put("variableDataType", variableDataType);
        config.put("variableType", variableType);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete a specified variable in the workspace.
     * @param variableId Id of the variable.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteVariable(long variableId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/variables/" + variableId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns list of all variables for the specified workspace.
     * @return A <code>JSONArray</code> of variables list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getVariables() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/variables";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("variables");
    }

    /**
     * Returns details of the specified variable.
     * @param variableId The id of the variable.
     * @return A <code>JSONObject</code> of variable details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getVariableDetails(long variableId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/variables/" + variableId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Make the specified folder as default.
     * @param folderId Id of the variable.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void makeDefaultFolder(long folderId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders/" + folderId + "/default";
        ac.sendAPIRequest("PUT", endPoint, null, reqHeader);
    }

    /**
     * Returns list of all datasource for the specified workspace.
     * @return A <code>JSONArray</code> of datasource list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getDatasources() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/datasources";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("dataSources");
    }

    /**
     * Initiate data sync for the specified datasource.
     * @param datasourceId Id for the datasource.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void syncData(long datasourceId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/datasources/" + datasourceId + "/sync";
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Update connection details for the specified datasource.
     * @param datasourceId Id of the datasource.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateDatasourceConnection(long datasourceId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/datasources/" + datasourceId;    
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Returns list of all views available in trash for the specified workspace.
     * @return A <code>JSONArray</code> of trash views.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getTrashViews() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/trash";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("views");
    }

    /**
     * Restore the specified view from trash.
     * @param viewId Id of the view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void restoreTrashView(long viewId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/trash/" + viewId;    
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Delete the specified view permanently from trash.
     * @param viewId Id of the view.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteTrashView(long viewId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/trash/" + viewId;    
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Create a new query table in the workspace.
     * @param sqlQuery SQL query to construct the query table.
     * @param queryTableName Name of the query table to be created.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of created query table id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createQueryTable(String sqlQuery, String queryTableName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/querytables";
        config = (config == null) ? new JSONObject() : config;
        config.put("sqlQuery", sqlQuery);
        config.put("queryTableName", queryTableName);

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String viewId = response.getJSONObject("data").getString("viewId");
        return Long.valueOf(viewId);
    }

    /**
     * Returns list of all query tables for the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONArray</code> of query tables.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getQueryTables(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/querytables";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONArray("queryTables");
    }
    /**
     * Update the mentioned query table in the workspace.
     * @param viewId Id of the query table to be updated.
     * @param sqlQuery New SQL query to be updated.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateQueryTable(long viewId, String sqlQuery, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/querytables/" + viewId;
        config = (config == null) ? new JSONObject() : config;
        config.put("sqlQuery", sqlQuery);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Swaps the hierarchy of a parent folder and a subfolder.
     * @param folderId Id for the folder.
     * @param hierarchy New hierarchy for the folder. (0 - Parent; 1 - Child)
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeFolderHierarchy(long folderId, int hierarchy, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders/" + folderId + "/move";
        config = (config == null) ? new JSONObject() : config;
        config.put("hierarchy", hierarchy);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Place the folder above the reference folder.
     * @param folderId Id for the folder.
     * @param referenceFolderId Id of the reference folder.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeFolderPosition(long folderId, long referenceFolderId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/folders/" + folderId + "/reorder";
        config = (config == null) ? new JSONObject() : config;
        config.put("referenceFolderId", referenceFolderId);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Move views to the mentioned folder.
     * @param folderId Id for the folder.
     * @param viewIds Ids of the views to be moved.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void moveViewsToFolder(long folderId, JSONArray viewIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/views/movetofolder";
        config = (config == null) ? new JSONObject() : config;
        config.put("folderId", folderId);
        config.put("viewIds", viewIds);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }


    /**
     * Returns list of users for the specified workspace.
     * @return A <code>JSONArray</code> of users.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getWorkspaceUsers() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/users";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("users");
    }


    /**
     * Add users to the specified workspace.
     * @param emailIds The email address of the users to be added.
     * @param role Role of the users to be added.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addWorkspaceUsers(JSONArray emailIds, String role, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/users";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        config.put("role", role);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove users from the specified workspace.
     * @param emailIds The email address of the users to be removed.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeWorkspaceUsers(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/users";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Change users staus in the specified workspace.
     * @param emailIds Email address of the users.
     * @param operation New status for the users ( Values -  activate | deactivate )
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeWorkspaceUserStatus(JSONArray emailIds, String operation, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/users/status";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        config.put("operation", operation);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Change role of the specified users in the workspace.
     * @param emailIds Email address of the users.
     * @param role Name of the role.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeWorkspaceUserRole(JSONArray emailIds, String role, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/users/role";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        config.put("role", role);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Export the mentioned views as templates.
     * @param viewIds Ids of the view to be exported.
     * @param filePath Path of the file where the data exported to be stored. ( Should be in 'atpt' format )
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void exportAsTemplate(JSONArray viewIds, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/template/data";
        config = (config == null) ? new JSONObject() : config;
        config.put("viewIds", viewIds);
        File file = new File(filePath);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, file);
    }

    /**
     * Returns list of email schedules available in the specified workspace.
     * @return A <code>JSONArray</code> of emailschedules.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getEmailSchedules() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("emailSchedules");
    }

    /**
     * Create an email schedule in the specified workspace.
     * @param scheduleName Name of the email schedule.
     * @param viewIds View ids to be mailed.
     * @param format The format in which the data has to be mailed.
     * @param emailIds The recipients' email addresses for sending views.
     * @param scheduleDetails Contains schedule frequency, date, and time info.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of email schedule id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createEmailSchedule(String scheduleName, JSONArray viewIds, String format, JSONArray emailIds, JSONObject scheduleDetails, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules";
        config = (config == null) ? new JSONObject() : config;
        config.put("scheduleName", scheduleName);
        config.put("viewIds", viewIds);
        config.put("exportType", format);
        config.put("emailIds", emailIds);
        config.put("scheduleDetails", scheduleDetails);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String scheduleId = response.getJSONObject("data").getString("scheduleId");
        return Long.valueOf(scheduleId);
    }

    /**
     * Update configurations of the specified email schedule in the workspace.
     * @param scheduleId Id of the email schedule.
     * @param config Contains the control configurations.
     * @return A <code>long</code> of updatd email schedule id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long updateEmailSchedule(long scheduleId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules/" + scheduleId;
        config = (config == null) ? new JSONObject() : config;
        JSONObject response = ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
        String newScheduleId = response.getJSONObject("data").getString("scheduleId");
        return Long.valueOf(newScheduleId);
    }

    /**
     * Trigger configured email schedules instantly.
     * @param scheduleId Id of the email schedule.
     * @return A <code>long</code> of updatd email schedule id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void triggerEmailSchedule(long scheduleId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules/" + scheduleId;
        ac.sendAPIRequest("POST", endPoint, null, reqHeader);
    }

    /**
     * Update configurations of the specified email schedule in the workspace.
     * @param scheduleId Id of the email schedule.
     * @param operation New status for the email schedule ( Values -  activate | deactivate )
     * @return A <code>long</code> of updatd email schedule id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeEmailScheduleStatus(long scheduleId, String operation) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules/" + scheduleId + "/status";
        JSONObject config = new JSONObject();
        config.put("operation", operation);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete the specified email schedule in the workspace.
     * @param scheduleId Id of the email schedule to be deleted.
     * @return A <code>long</code> of updatd email schedule id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteEmailSchedule(long scheduleId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/emailschedules/" + scheduleId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns list of all aggregate formulas for the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONArray</code> of aggregate formulas.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAggregateFormulas(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/aggregateformulas";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONArray("aggregateFormulas");
    }

    /**
     * Returns list of all dependent views and formulas for the specified aggregate formula.
     * @param formulaId Id of the aggregate formula.
     * @return A <code>JSONObject</code> of dependent views and formulas.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getAggregateFormulaDependents(long formulaId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/aggregateformulas/" + formulaId + "/dependents";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns the value of the aggregate formula.
     * @param formulaId Id of the aggregate formula.
     * @return A <code>String</code> contains aggregate formula value.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String getAggregateFormulaValue(long formulaId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/aggregateformulas/" + formulaId + "/value";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getString("formulaValue");
    }

    /**
     * Create a report in the specified workspace.
     * @param config Contains the control configurations.
     * @return A <code>long</code> of created view id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createReport(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/reports";
        config = (config == null) ? new JSONObject() : config;

        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String variableId = response.getJSONObject("data").getString("viewId");
        return Long.valueOf(variableId);
    }

    /**
     * Update the design and configuration of the specified report.
     * @param viewId Id of the view.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateReport(long viewId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/reports/" + viewId;
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Internally used in JDBC driver
     */
    public JSONObject getWorkspaceMetadata() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/metadata";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("workspaces");
    }

    /**
     * Returns details of the specified query table.
     *
     * @param queryTableId Id of the query table.
     * @return Query table details.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject getQueryTableDetails(String queryTableId)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint = workspaceEndPoint + "/querytables/" + queryTableId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns list of AutoML analysis for the specified workspace.
     *
     * @return AutoML analysis list.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONArray getAutoMLAnalysis()
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint = "/restapi/v2/automl/workspaces/" + workspaceId + "/analysis";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("analysis");
    }

    /**
     * Retrieves detailed information for a specific AutoML analysis.
     *
     * @param analysisId Id of the AutoML analysis.
     * @return AutoML analysis details.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject getAutoMLAnalysisDetails(String analysisId)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/" + analysisId;

        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("analysis");
    }

    /**
     * Returns deployment details for a specific AutoML analysis model.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param modelId Id of the AutoML analysis model.
     * @return Deployment details.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject getDeploymentDetails(String analysisId, String modelId)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/models/" + modelId + "/deployments";

        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("deployments");
    }

    /**
     * Creates a new AutoML analysis in the workspace.
     *
     * @param name Name of the AutoML analysis.
     * @param trainingTableId Id of the training table.
     * @param predictionType Prediction type (REGRESSION / CLASSIFICATION / CLUSTERING).
     * @param features Feature column names.
     * @param serverOption Compute size (1 -> 8GB, 2 -> 16GB, 3 -> 32GB).
     * @param algorithms Algorithms configuration.
     * @param config Additional control parameters. Can be null.
     * @return Created AutoML analysis Id.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public String createAutoMLAnalysis(
            String name,
            String trainingTableId,
            String predictionType,
            JSONArray features,
            int serverOption,
            JSONObject algorithms,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        config = (config == null) ? new JSONObject() : config;

        config.put("name", name);
        config.put("trainingTableId", trainingTableId);
        config.put("predictionType", predictionType);
        config.put("features", features);
        config.put("serverOption", serverOption);
        config.put("algorithms", algorithms);

        String endPoint = "/restapi/v2/automl/workspaces/" + workspaceId + "/analysis";
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("id");
    }

    /**
     * Deletes a specified AutoML analysis from the workspace.
     *
     * @param analysisId Id of the AutoML analysis to be deleted.
     * @param config Additional control parameters. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void deleteAutoMLAnalysis(String analysisId, JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/" + analysisId;

        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Deletes a specified model from an AutoML analysis.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param modelId Id of the model to be deleted.
     * @param config Additional control parameters. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void deleteAutoMLAnalysisModel(
            String analysisId,
            String modelId,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/models/" + modelId;

        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Creates a deployment for an AutoML analysis model.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param modelId Id of the AutoML model.
     * @param inputTableId Id of the input table.
     * @param outputTable Name of the output table.
     * @param outputColumns Columns to be included in the output table.
     * @param predictionColumn Prediction column name.
     * @param serverOption Compute size (1 -> 8GB, 2 -> 16GB, 3 -> 32GB).
     * @param importType Import type (APPEND, TRUNCATEADD, UPDATEADD).
     * @param scheduleDetails Schedule details. Can be null.
     * @param config Additional control parameters. Can be null.
     * @return Deployment details.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject createAutoMLAnalysisDeployment(
            String analysisId,
            String modelId,
            String inputTableId,
            String outputTable,
            JSONArray outputColumns,
            String predictionColumn,
            int serverOption,
            String importType,
            Object scheduleDetails,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        config = (config == null) ? new JSONObject() : config;

        config.put("inputTableId", inputTableId);
        config.put("outputTable", outputTable);
        config.put("outputColumns", outputColumns);
        config.put("predictionColumn", predictionColumn);
        config.put("serverOption", serverOption);
        config.put("importType", importType);

        if (scheduleDetails == null) {
            config.put("scheduleDetails", "none");
        } else {
            config.put("scheduleDetails", scheduleDetails);
        }

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/models/" + modelId +
                        "/deployments";

        JSONObject response =
                ac.sendAPIRequest("POST", endPoint, config, reqHeader);

        return response.getJSONObject("data").getJSONObject("deployments");
    }

    /**
     * Executes a specific AutoML deployment.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param deploymentId Id of the deployment to be executed.
     * @param config Additional control parameters. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void deployAutoMLAnalysis(
            String analysisId,
            String deploymentId,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/deployments/" + deploymentId +
                        "/execute";

        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Deletes a specific AutoML deployment.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param deploymentId Id of the deployment to be deleted.
     * @param config Additional control parameters. Can be null.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public void deleteAutoMLAnalysisDeployment(
            String analysisId,
            String deploymentId,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/deployments/" + deploymentId;

        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Generates predictions using a trained AutoML model with sample input values.
     *
     * @param analysisId Id of the AutoML analysis.
     * @param modelId Id of the AutoML model.
     * @param features Feature values for prediction.
     * @param config Additional control parameters. Can be null.
     * @return Prediction details.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONObject autoMLAnalysisPrediction(
            String analysisId,
            String modelId,
            JSONObject features,
            JSONObject config)
            throws ServerException, ParseException, IOException, JSONException {

        config = (config == null) ? new JSONObject() : config;
        config.put("features", features);

        String endPoint =
                "/restapi/v2/automl/workspaces/" + workspaceId +
                        "/analysis/" + analysisId +
                        "/models/" + modelId +
                        "/whatif";

        JSONObject response =
                ac.sendAPIRequest("POST", endPoint, config, reqHeader);

        return response.getJSONObject("data");
    }


    /**
     * Returns list of all tags for the specified workspace.
     * @return A <code>JSONArray</code> of tags list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getTags() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("tags");
    }
    /**
     * Create a tag in the specified workspace.
     * @param tagName Name of the tag to be created.
     * @param colorCode Color of the tag in HEX color code.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of created tag id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createTag(String tagName, String colorCode, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags";
        config = (config == null) ? new JSONObject() : config;
        config.put("name", tagName);
        config.put("colorCode", colorCode);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String tagId = response.getJSONObject("data").getString("tagId");
        return Long.valueOf(tagId);
    }
    /**
     * Update details of the specified tag in the workspace.
     * @param tagId Id of the tag.
     * @param config Contains the control configurations.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateTag(long tagId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags/" + tagId;
        config = (config == null) ? new JSONObject() : config;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }
    /**
     * Delete the specified tag from the workspace.
     * @param tagId Id of the tag.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteTag(long tagId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags/" + tagId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }
    /**
     * Adds the specified tag to multiple views in the workspace.
     * @param tagId Id of the tag.
     * @param viewIds List of view ids to be associated with the tag.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addTagToViews(long tagId, JSONArray viewIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags/" + tagId + "/views";
        config = (config == null) ? new JSONObject() : config;
        config.put("viewIds", viewIds);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }
    /**
     * Removes the specified tag from multiple views in the workspace.
     * @param tagId Id of the tag.
     * @param viewIds List of view ids to be dissociated. Can be null when dissociateAll is true.
     * @param dissociateAll To dissociate the tag from all associated views.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeTagFromViews(long tagId, JSONArray viewIds, boolean dissociateAll, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags/" + tagId + "/views";
        config = (config == null) ? new JSONObject() : config;
        if(dissociateAll) {
            config.put("dissociateAll", true);
        } else {
            config.put("viewIds", viewIds);
        }
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }
    /**
     * Returns the list of views associated with the specified tag.
     * @param tagId Id of the tag.
     * @return A <code>JSONArray</code> of tagged views.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getTaggedViews(long tagId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/tags/" + tagId + "/views";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("views");
    }

    /**
     * Returns list of workspaces linked to the specified master workspace.
     * @return A <code>JSONArray</code> of linked workspaces.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getLinkedWorkspaces() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("linkedWorkspaces");
    }

    /**
     * Returns list of organizations and workspaces that can be linked to the specified master workspace.
     * @return A <code>JSONArray</code> of organizations with their linkable workspaces.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getLinkableWorkspaces() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces/linkable";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("orgs");
    }

    /**
     * Returns the linking compatibility details for the specified client workspaces.
     * @param clients Contains the client workspaces to be verified for linking compatibility.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONArray</code> of client workspace compatibility details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getWorkspaceLinkingCompatibility(JSONArray clients, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces/compatibility";
        config = (config == null) ? new JSONObject() : config;
        config.put("clients", clients);
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONArray("clients");
    }

    /**
     * Link the specified client workspaces to the master workspace.
     * @param clients Contains the client workspaces to be linked with the master workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void linkWorkspaces(JSONArray clients, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces";
        config = (config == null) ? new JSONObject() : config;
        config.put("clients", clients);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Unlink the client workspaces from the specified master workspace.
     * @param scope Scope of the unlink operation.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void unlinkWorkspaces(String scope, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces";
        config = (config == null) ? new JSONObject() : config;
        config.put("scope", scope);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Sync the metadata of the master workspace to its linked client workspaces.
     * @param scope Scope of the sync operation.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void syncLinkedWorkspaces(String scope, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces/sync";
        config = (config == null) ? new JSONObject() : config;
        config.put("scope", scope);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Returns the sync details of the specified linked workspaces.
     * @param sandboxIds Ids of the linked workspaces for which the sync details are fetched.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONArray</code> of linked workspace sync details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getLinkedWorkspaceSyncDetails(JSONArray sandboxIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/linkedworkspaces/sync";
        config = (config == null) ? new JSONObject() : config;
        config.put("sandboxIds", sandboxIds);
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONArray("workspaces");
    }

    /**
     * Returns the backup configuration and the list of backups available for the specified workspace.
     * @return A <code>JSONObject</code> of workspace backup details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getWorkspaceBackups() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/backups";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Trigger an instant backup for the specified workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of the triggered backup details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject backupWorkspaceNow(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/backups";
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns the status of the specified workspace backup.
     * @param backupId Id of the backup.
     * @return A <code>JSONObject</code> of backup status details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getWorkspaceBackupStatus(long backupId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/backups/" + backupId + "/status";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Download the specified workspace backup.
     * @param backupId Id of the backup.
     * @param filePath Path of the file where the downloaded backup is to be stored.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void downloadWorkspaceBackup(long backupId, String filePath, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/backups/" + backupId + "/download";
        File file = new File(filePath);
        ac.sendExportAPIRequest(endPoint, config, reqHeader, file);
    }

    /**
     * Restore the specified workspace from the given backup.
     * @param backupId Id of the backup.
     * @param confirmRestore Pass <code>true</code> to confirm that the existing workspace data can be overwritten.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of the triggered restore details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject restoreWorkspaceFromBackup(long backupId, boolean confirmRestore, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/backups/" + backupId + "/restore";
        config = (config == null) ? new JSONObject() : config;
        config.put("confirmRestore", confirmRestore);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns the status of the specified workspace restore.
     * @param restoreId Id of the restore.
     * @return A <code>JSONObject</code> of restore status details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getWorkspaceRestoreStatus(long restoreId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/restores/" + restoreId + "/status";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Create a dashboard in the specified workspace.
     * @param displayName Name of the dashboard.
     * @param layout Layout configuration of the dashboard.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of new dashboard id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createDashboard(String displayName, String layout, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/dashboards";
        config = (config == null) ? new JSONObject() : config;
        config.put("displayName", displayName);
        config.put("layout", layout);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String dashboardId = response.getJSONObject("data").getString("dashboardId");
        return Long.valueOf(dashboardId);
    }

    /**
     * Update the specified dashboard in the workspace.
     * @param dashboardId Id of the dashboard.
     * @param config Contains the dashboard configurations to be updated.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateDashboard(long dashboardId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/dashboards/" + dashboardId;
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Returns the metadata of the specified dashboard.
     * @param dashboardId Id of the dashboard.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of dashboard configuration.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getDashboardMetadata(long dashboardId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/dashboards/" + dashboardId + "/metadata";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data").getJSONObject("dashboardConfig");
    }

    /**
     * Returns the metadata of the specified report.
     * @param viewId Id of the report.
     * @return A <code>JSONObject</code> of report configuration.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getReportMetadata(long viewId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/reports/" + viewId + "/metadata";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("reportConfig");
    }

    /**
     * Returns list of data alerts available in the specified workspace.
     * @return A <code>JSONArray</code> of data alerts.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAlertsInWorkspace() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("alerts");
    }

    /**
     * Returns the configuration of the specified data alert.
     * @param alertId Id of the data alert.
     * @return A <code>JSONObject</code> of data alert configuration.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getAlertConfiguration(long alertId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts/" + alertId;
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Update the specified data alert in the workspace.
     * @param alertId Id of the data alert.
     * @param alertName Name of the data alert.
     * @param scheduleDetails Contains the schedule configurations of the data alert.
     * @param rules Contains the rules to be evaluated by the data alert.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateAlert(long alertId, String alertName, JSONObject scheduleDetails, JSONArray rules, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts/" + alertId;
        config = (config == null) ? new JSONObject() : config;
        config.put("alertName", alertName);
        config.put("scheduleDetails", scheduleDetails);
        config.put("rules", rules);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Delete the specified data alerts from the workspace.
     * @param alertIds Ids of the data alerts to be deleted.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteAlerts(JSONArray alertIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts";
        config = (config == null) ? new JSONObject() : config;
        config.put("alertIds", alertIds);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Enable or disable the specified data alerts in the workspace.
     * @param alertIds Ids of the data alerts.
     * @param enabled Pass <code>true</code> to enable the data alerts and <code>false</code> to disable them.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeAlertStatus(JSONArray alertIds, boolean enabled, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts/status";
        config = (config == null) ? new JSONObject() : config;
        config.put("alertIds", alertIds);
        config.put("enabled", enabled);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Execute the specified data alert immediately.
     * @param alertId Id of the data alert.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void runAlert(long alertId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts/" + alertId + "/execute";
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Returns the execution events of the specified data alert.
     * @param alertId Id of the data alert.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>JSONObject</code> of data alert events along with the page details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getAlertEvents(long alertId, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = workspaceEndPoint + "/alerts/" + alertId + "/events";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns the access restriction settings configured for the specified workspace.
     * @return A <code>JSONObject</code> of workspace access restriction settings.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getWorkspaceAccessRestrictions() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = securityControlsEndPoint + "/access-restrictions";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Update the access restriction settings of the specified workspace.
     * @param config Contains the access restriction configurations to be updated.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateWorkspaceAccessRestrictions(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = securityControlsEndPoint + "/access-restrictions";
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

}
