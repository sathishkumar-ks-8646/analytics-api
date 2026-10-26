// $Id$
package com.zoho.analytics.client;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * OrgAPI contains organization level operations.
 */
public class OrgAPI {
    private final AnalyticsClient ac;
    private final Map<String, String> reqHeader = new HashMap<>();

    /**
     * Creates a new <code>OrgAPI</code> instance.
     * @param ac <code>AnalyticsClient</code> instance.
     * @param orgId The ID of the organization.
     */
    protected OrgAPI(AnalyticsClient ac, long orgId){
        this.ac = ac;
        reqHeader.put("ZANALYTICS-ORGID", String.valueOf(orgId));
    }

    /**
     * Create a blank workspace in the specified organization.
     * @param workspaceName Name of the workspace.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>long</code> of new workspace id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public long createWorkspace(String workspaceName, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/workspaces/";
        config = (config == null) ? new JSONObject() : config;
        config.put("workspaceName", workspaceName);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        String workspaceId = response.getJSONObject("data").getString("workspaceId");
        return Long.valueOf(workspaceId);
    }

    /**
     * Returns list of admins for a specified organization.
     * @return A <code>JSONArray</code> of organization admins.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getAdmins() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgadmins";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("orgAdmins");
    }
    
    /**
     * Returns list of users for the specified organization.
     * @return A <code>JSONArray</code> of users.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getUsers() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("users");
    }

    /**
     * Add users to the specified organization.
     * @param emailIds The email address of the users to be added.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void addUsers(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("POST", endPoint, config, reqHeader);
    }

    /**
     * Remove users from the specified organization.
     * @param emailIds The email address of the users to be removed.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void removeUsers(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("DELETE", endPoint, config, reqHeader);
    }

    /**
     * Activate users in the specified organization.
     * @param emailIds The email address of the users to be activated.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void activateUsers(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users/active";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Deactivate users in the specified organization.
     * @param emailIds The email address of the users to be deactivated.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deactivateUsers(JSONArray emailIds, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users/inactive";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Change role for the specified users.
     * @param emailIds The email address of the users.
     * @param role Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN".
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void changeUserRole(JSONArray emailIds, String role, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/users/role";
        config = (config == null) ? new JSONObject() : config;
        config.put("emailIds", emailIds);
        config.put("role", role);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Returns details of the specified workspace/view.
     * @param workspaceName The name of the workspace.
     * @param viewName The name of the view.
     * @return A <code>JSONObject</code> of workspace/view details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getMetaDetails(String workspaceName, String viewName) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/metadetails";
        JSONObject config = new JSONObject();
        config.put("workspaceName", workspaceName);
        if(viewName != null) {
            config.put("viewName", viewName);
        }
        JSONObject response = ac.sendAPIRequest("GET", endPoint, config, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Returns subscription details of the specified organization.
     * @return A <code>JSONObject</code> of subscription details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getSubscriptionDetails() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/subscription";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONObject("subscription");
    }

    /**
     * Returns resource usage details of the specified organization.
     * @return A <code>JSONArray</code> of resource details.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getResourceDetails() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/resources";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("resourceDetails");
    }

    /**
     * Returns list of all accessible workspaces in the specified organization.
     * @return A <code>JSONArray</code> of workspace list.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getOrgWorkspaces() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgs/workspaces";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("workspaces");
    }

    /**
     * Returns all AutoML analysis available in the organization.
     *
     * @return AutoML analysis list.
     * @throws ServerException If the server failed to process the request.
     * @throws ParseException If the response could not be parsed.
     * @throws IOException If communication errors occur.
     * @throws JSONException If JSON processing fails.
     */
    public JSONArray getAutoMLAnalysis() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/automl/analysis";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("analysis");
    }
    /**
     * Returns list of custom roles for the specified organization.
     * @return A <code>JSONArray</code> of custom roles.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getCustomRoles() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgs/roles";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("roles");
    }
    /**
     * Create a new custom role in the specified organization.
     * @param roleName Name of the custom role to be created.
     * @param accessType Access type for the custom role.
     * @param permissions Contains the permission details for the custom role.
     * @param config Contains any additional control configurations. Can be null.
     * @return A <code>String</code> of the created custom role id.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public String createCustomRole(String roleName, String accessType, JSONObject permissions, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgs/roles";
        config = (config == null) ? new JSONObject() : config;
        config.put("roleName", roleName);
        config.put("accessType", accessType);
        config.put("permissions", permissions);
        JSONObject response = ac.sendAPIRequest("POST", endPoint, config, reqHeader);
        return response.getJSONObject("data").getString("roleId");
    }
    /**
     * Update the specified custom role in the organization.
     * @param roleId Id of the custom role.
     * @param roleName New name for the custom role.
     * @param accessType Access type for the custom role.
     * @param permissions Contains the permission details for the custom role.
     * @param config Contains any additional control configurations. Can be null.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateCustomRole(String roleId, String roleName, String accessType, JSONObject permissions, JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgs/roles/" + roleId;
        config = (config == null) ? new JSONObject() : config;
        config.put("roleName", roleName);
        config.put("accessType", accessType);
        config.put("permissions", permissions);
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }
    /**
     * Delete the specified custom role from the organization.
     * @param roleId Id of the custom role.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void deleteCustomRole(String roleId) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/orgs/roles/" + roleId;
        ac.sendAPIRequest("DELETE", endPoint, null, reqHeader);
    }

    /**
     * Returns the access restriction settings configured for the organization.
     * @return A <code>JSONObject</code> of organization access restriction settings.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONObject getOrgAccessRestrictions() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/security-controls/access-restrictions";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data");
    }

    /**
     * Update the access restriction settings of the organization.
     * @param config Contains the access restriction configurations to be updated.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public void updateOrgAccessRestrictions(JSONObject config) throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/security-controls/access-restrictions";
        ac.sendAPIRequest("PUT", endPoint, config, reqHeader);
    }

    /**
     * Returns list of linked workspaces available in the specified organization.
     * @return A <code>JSONArray</code> of linked workspaces.
     * @throws ServerException If the server has received the request but did not process the request, due to some error.
     * @throws ParseException If the server has responded but the client was not able to parse the response.
     * @throws IOException If any communication related errors like request time out occurs, when trying to contact the service.
     * @throws JSONException If any errors while processing the JSON data.
     */
    public JSONArray getLinkedWorkspaces() throws ServerException, ParseException, IOException, JSONException {
        String endPoint = "/restapi/v2/linkedworkspaces";
        JSONObject response = ac.sendAPIRequest("GET", endPoint, null, reqHeader);
        return response.getJSONObject("data").getJSONArray("linkedWorkspaces");
    }

}
