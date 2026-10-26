package analyticsclient

import (
    "fmt"
    "net/http"
    "net/url"
    "encoding/json"
    "io/ioutil"
    "strings"
    "strconv"
    _ "crypto/sha512"
    "crypto/tls"
    "os"
    "bytes"
    "io"
    "mime/multipart"
    "bufio"
    "time"
)

// secureHTTPClient enforces TLS 1.2+ with a strong cipher suite list so that
// connections never negotiate weak ciphers. On older Go versions that do not
// know about TLS 1.3 constants the values still resolve - tls.VersionTLS13 has
// been available since Go 1.12.
var secureHTTPClient = &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{
            MinVersion: tls.VersionTLS12,
            MaxVersion: tls.VersionTLS13,
            CipherSuites: []uint16{
                // TLS 1.3 (Go selects these automatically; listed for clarity).
                tls.TLS_AES_256_GCM_SHA384,
                tls.TLS_AES_128_GCM_SHA256,
                tls.TLS_CHACHA20_POLY1305_SHA256,
                // Strong TLS 1.2 suites.
                tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                tls.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
                tls.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,
                tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
                tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
            },
        },
    },
}

    /*
    Client - Contains the client details.

    ClientVersion - ZohoAnalytics client version.

    AnalyticsServerUrl - ZohoAnalytics domain URL.

    AccountsServerUrl - ZohoAccounts domain URL.

    ClientId - Client id of the user.

    ClientSecret - Client secret of the user.

    RefreshToken - Refresh token of the user.

    AccessToken - Access token of the user.
    */
    type Client struct {
        ClientVersion string
        AnalyticsServerUrl string
        AccountsServerUrl string
        ClientId string
        ClientSecret string
        RefreshToken string
        AccessToken string
    }

    /*
    GetAnalyticsClient - Returns the Client object.

    clientid - Client id of the user.

    clientsecret - Client secret of the user.

    refreshtoken - Refresh token of the user.
    */
    func GetAnalyticsClient(clientid, clientsecret, refreshtoken string) Client {
        ac := Client{
        ClientId : clientid,
        ClientSecret : clientsecret,
        RefreshToken : refreshtoken,

        ClientVersion : "2.9.0",
        AnalyticsServerUrl : "https://@@ANALYTICS_URL",
        AccountsServerUrl : "https://@@ACCOUNTS_URL",
        AccessToken : "",
        }
        return ac
    }

    /*
    GetOrgs - Returns list of all accessible organizations.

    orgs - Returns org list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetOrgs() (orgs interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/orgs"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            orgs = response.(map[string]interface{})["data"].(map[string]interface{})["orgs"].(interface{})
        }
        return
    }

    /*
    GetWorkspaces - Returns list of all accessible workspaces.

    workspaces - Returns workspace list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetWorkspaces() (workspaces map[string]interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/workspaces"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaces = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    GetOwnedWorkspaces - Returns list of owned workspaces.

    workspaces - Returns workspace list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetOwnedWorkspaces() (workspaces interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/workspaces/owned"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaces = response.(map[string]interface{})["data"].(map[string]interface{})["workspaces"].(interface{})
        }
        return
    }

    /*
    GetSharedWorkspaces - Returns list of shared workspaces.

    workspaces - Returns workspace list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetSharedWorkspaces() (workspaces interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/workspaces/shared"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaces = response.(map[string]interface{})["data"].(map[string]interface{})["workspaces"].(interface{})
        }
        return
    }

    /*
    GetRecentViews - Returns list of recently accessed views.

    views - Returns view list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetRecentViews() (views interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/recentviews"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }

    /*
    GetWorkspaceDetails - Returns details of the specified workspace.

    workspaceid - The ID of the workspace.

    workspaceDetails - Returns workspace details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetWorkspaceDetails(workspaceid string) (workspaceDetails map[string]interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/workspaces/" + workspaceid
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaceDetails = response.(map[string]interface{})["data"].(map[string]interface{})["workspaces"].(map[string]interface{})
        }
        return
    }

    /*
    GetViewDetails - Returns details of the specified view.

    viewid - The ID of the view.

    config - Contains the control configurations.

    viewDetails - Returns the view details as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetViewDetails(viewid string, config map[string]interface{}) (viewDetails map[string]interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/views/" + viewid
        response, exception := ac.sendAPIRequest("GET", endpoint, config, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            viewDetails = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(map[string]interface{})
        }
        return
    }

    /*
    GetDashboards - Returns the list of all accessible dashboards.

    dashboards - Returns the owned and shared dashboards as map.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetDashboards() (dashboards map[string]interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/dashboards"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            dashboards = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    GetOwnedDashboards - Returns the list of dashboards owned by the user.

    views - Returns the owned dashboards as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetOwnedDashboards() (views interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/dashboards/owned"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }

    /*
    GetSharedDashboards - Returns the list of dashboards shared to the user.

    views - Returns the shared dashboards as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (ac *Client) GetSharedDashboards() (views interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/dashboards/shared"
        response, exception := ac.sendAPIRequest("GET", endpoint, nil, nil)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }


    /*
    OrgAPI - OrgAPI contains organization level operations.
    */
    type OrgAPI struct {
        requestHeaders map[string]string
        ac *Client
    }

    
    /*
    GetOrgInstance - Returns the OrgAPI object.

    ac - Client structure pointer.

    orgid - The ID of the organization.
    */
    func GetOrgInstance(ac *Client, orgid string) OrgAPI {

        org := OrgAPI{
            ac : ac,
            requestHeaders : map[string]string{
                "ZANALYTICS-ORGID" : orgid,
            },
        }
        return org
    }

    /*
    CreateWorkspace - Create a blank workspace in the specified organization.

    workspacename - Name of the workspace to be created.

    config - Contains any additional control configurations.

    workspaceid - Returns the new workspace id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) CreateWorkspace(workspacename string, config map[string]interface{}) (workspaceid string, serverexception *ServerException) {
        endpoint := "/restapi/v2/workspaces/"
        config["workspaceName"] = workspacename
        response, exception := org.ac.sendAPIRequest("POST", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaceid = response.(map[string]interface{})["data"].(map[string]interface{})["workspaceId"].(string)
        }
        return
    }

    /*
    GetAdmins - Returns list of admins for a specified organization.

    orgadmins - Returns orgadmin list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetAdmins() (orgadmins interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/orgadmins"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            orgadmins = response.(map[string]interface{})["data"].(map[string]interface{})["orgAdmins"].(interface{})
        }
        return
    }

    /*
    GetUsers - Returns list of users for the specified organization.

    users - Returns user list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetUsers() (users interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/users"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            users = response.(map[string]interface{})["data"].(map[string]interface{})["users"].(interface{})
        }
        return
    }

    /*
    AddUsers - Add users to the specified organization.

    emailids - The email address of the users to be added.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) AddUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/users"
        config["emailIds"] = emailids
        _, exception := org.ac.sendAPIRequest("POST", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveUsers - Remove users from the specified organization.

    emailids - The email address of the users to be removed.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) RemoveUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/users"
        config["emailIds"] = emailids
        _, exception := org.ac.sendAPIRequest("DELETE", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ActivateUsers - Activate users in the specified organization.

    emailids - The email address of the users to be activated.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) ActivateUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/users/active"
        config["emailIds"] = emailids
        _, exception := org.ac.sendAPIRequest("PUT", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeactivateUsers - Deactivate users in the specified organization.

    emailids - The email address of the users to be deactivated.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) DeactivateUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/users/inactive"
        config["emailIds"] = emailids
        _, exception := org.ac.sendAPIRequest("PUT", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeUserRole - Change role for the specified users.

    emailids - The email address of the users.

    role - Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN".

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) ChangeUserRole(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/users/role"
        config["emailIds"] = emailids
        config["role"] = role
        _, exception := org.ac.sendAPIRequest("PUT", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetMetaDetails - Returns details of the specified workspace/view.

    workspacename - The name of the workspace.
    
    viewname - The name of the view.

    metadetails - Returns details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetMetaDetails(workspacename, viewname string) (metadetails interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/metadetails"
        config := map[string]interface{}{}
        config["workspaceName"] = workspacename
        if viewname != ""{
            config["viewName"] = viewname
        }
        response, exception := org.ac.sendAPIRequest("GET", endpoint, config, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            metadetails = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    GetSubscriptionDetails - Returns subscription details of the specified organization.

    subscriptioninfo - Returns details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetSubscriptionDetails() (subscriptioninfo interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/subscription"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            subscriptioninfo = response.(map[string]interface{})["data"].(map[string]interface{})["subscription"].(interface{})
        }
        return
    }

    /*
    GetResourceDetails - Returns resource usage details of the specified organization.

    resourceinfo - Returns details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetResourceDetails() (resourceinfo interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/resources"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            resourceinfo = response.(map[string]interface{})["data"].(map[string]interface{})["resourceDetails"].(interface{})
        }
        return
    }

    /*
    GetAutoMLAnalysis - Returns list of automl analysis for the specified organization.

    analysis - Returns AutoML analysis list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetAutoMLAnalysis() (analysis interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/automl/analysis"

        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            analysis = response.(map[string]interface{})["data"].(map[string]interface{})["analysis"].(interface{})
        }
        return
    }


    /*
    GetCustomRoles - Returns list of all custom roles available in the organization.
    roles - Returns custom role list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetCustomRoles() (roles interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/orgs/roles"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            roles = response.(map[string]interface{})["data"].(map[string]interface{})["roles"].(interface{})
        }
        return
    }
    /*
    CreateCustomRole - Create a new custom role in the organization.
    rolename - Name of the custom role.
    accesstype - Access type for the custom role.
    permissions - Permissions configuration for the custom role.
    config - Contains any additional control configurations.
    roleid - Returns the new custom role id.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) CreateCustomRole(rolename, accesstype string, permissions map[string]interface{}, config map[string]interface{}) (roleid string, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["roleName"] = rolename
        config["accessType"] = accesstype
        config["permissions"] = permissions
        endpoint := "/restapi/v2/orgs/roles"
        response, exception := org.ac.sendAPIRequest("POST", endpoint, config, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            roleid = fmt.Sprintf("%v", response.(map[string]interface{})["data"].(map[string]interface{})["roleId"])
        }
        return
    }
    /*
    UpdateCustomRole - Update the existing custom role in the organization.
    roleid - Id of the custom role to be updated.
    rolename - New name for the custom role.
    accesstype - New access type for the custom role.
    permissions - New permissions configuration for the custom role.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) UpdateCustomRole(roleid, rolename, accesstype string, permissions map[string]interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["roleName"] = rolename
        config["accessType"] = accesstype
        config["permissions"] = permissions
        endpoint := "/restapi/v2/orgs/roles/" + roleid
        _, exception := org.ac.sendAPIRequest("PUT", endpoint, config, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    DeleteCustomRole - Delete the specified custom role from the organization.
    roleid - Id of the custom role to be deleted.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) DeleteCustomRole(roleid string) (serverexception *ServerException) {
        endpoint := "/restapi/v2/orgs/roles/" + roleid
        _, exception := org.ac.sendAPIRequest("DELETE", endpoint, nil, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetOrgAccessRestrictions - Returns the access restriction settings configured for the organization.
    accessrestrictions - Returns the organization access restriction settings as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetOrgAccessRestrictions() (accessrestrictions interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/security-controls/access-restrictions"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            accessrestrictions = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    UpdateOrgAccessRestrictions - Update the access restriction settings of the organization.
    config - Contains the access restriction configurations to be updated.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) UpdateOrgAccessRestrictions(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := "/restapi/v2/security-controls/access-restrictions"
        _, exception := org.ac.sendAPIRequest("PUT", endpoint, config, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetLinkedWorkspaces - Returns list of linked workspaces available in the specified organization.
    linkedworkspaces - Returns the linked workspaces list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (org *OrgAPI) GetLinkedWorkspaces() (linkedworkspaces interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/linkedworkspaces"
        response, exception := org.ac.sendAPIRequest("GET", endpoint, nil, org.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            linkedworkspaces = response.(map[string]interface{})["data"].(map[string]interface{})["linkedWorkspaces"].(interface{})
        }
        return
    }

    /*
    WorkspaceAPI - WorkspaceAPI contains workspace level operations.
    */
    type WorkspaceAPI struct {
        ac *Client
        requestHeaders map[string]string    
        workspaceEndpoint string
        securityControlsEndpoint string
        workspaceID string
    }

    /*
    GetWorkspaceInstance - Returns the WorkspaceAPI object.

    ac - Client structure pointer.

    orgid - The ID of the organization.

    workspaceid - Id of the workspace.
    */
    func GetWorkspaceInstance(ac *Client, orgid string, workspaceid string) WorkspaceAPI {
        workspace := WorkspaceAPI{
            ac : ac,
            requestHeaders : map[string]string{
                "ZANALYTICS-ORGID" : orgid,
            },
            workspaceEndpoint : "/restapi/v2/workspaces/" + workspaceid,
            securityControlsEndpoint : "/restapi/v2/security-controls/workspaces/" + workspaceid,
            workspaceID : workspaceid,
        }
        return workspace
    }

    /*
    Copy - Copy the specified workspace from one organization to another or within the organization.

    newworkspacename - Name of the new workspace.

    config - Contains any additional control configurations.

    destorgid - Id of the organization where the destination workspace is present.

    newworkspaceid - Returns copied workspace id as string.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) Copy(newworkspacename string, config map[string]interface{}, destorgid string) (newworkspaceid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint
        config["newWorkspaceName"] = newworkspacename
        requestHeaders := workspace.requestHeaders
        if (destorgid != "") {
            requestHeaders["ZANALYTICS-DEST-ORGID"] = destorgid
        }
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            newworkspaceid = response.(map[string]interface{})["data"].(map[string]interface{})["workspaceId"].(string)
        }
        return
    }

    /*
    Rename - Rename a specified workspace in the organization.

    workspacename - New name of the workspace.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) Rename(workspacename string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint
        config["workspaceName"] = workspacename
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    Delete - Delete a specified workspace in the organization.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) Delete() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetSecretKey - Returns the secret key of the specified workspace.

    config - Contains any additional control configurations.

    secretkey - Returns workspace secret key.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetSecretKey(config map[string]interface{}) (secretkey string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/secretkey"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            secretkey = response.(map[string]interface{})["data"].(map[string]interface{})["workspaceKey"].(string)
        }
        return
    }

    /*
    AddFavorite - Adds a specified workspace as favorite.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddFavorite() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/favorite"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveFavorite - Remove a specified workspace from favorite.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveFavorite() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/favorite"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddDefault - Adds a specified workspace as default.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddDefault() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/default"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveDefault - Remove a specified workspace from default.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveDefault() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/default"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetAdmins - Returns list of admins for the specified workspace.

    workspaceadmins - Returns workspace admin list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAdmins() (workspaceadmins interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/admins"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            workspaceadmins = response.(map[string]interface{})["data"].(map[string]interface{})["workspaceAdmins"].(interface{})
        }
        return
    }

    /*
    AddAdmins - Add admins for the specified workspace.

    emailids - The email address of the admin users to be added.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddAdmins(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/admins"
        config["emailIds"] = emailids
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveAdmins - Remove admins from the specified workspace.

    emailids - The email address of the admin users to be removed.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveAdmins(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/admins"
        config["emailIds"] = emailids
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetShareInfo - Returns shared details of the specified workspace.

    shareinfo - Returns ShareInfo as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetShareInfo() (shareinfo interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/share"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            shareinfo = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ShareViews - Share views to the specified users.

    viewids - View ids which to be shared.

    emailids - The email address of the users to whom the views need to be shared.

    permissions - Contains permission details.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ShareViews(viewids, emailids interface{}, permissions map[string]bool, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/share"
        config["emailIds"] = emailids
        config["viewIds"] = viewids
        config["permissions"] = permissions
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveShare - Remove shared views for the specified users.

    viewids - View ids whose sharing needs to be removed.

    emailids - The email address of the users to whom the sharing need to be removed.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveShare(viewids, emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/share"
        config["emailIds"] = emailids
        if(viewids != nil){
            config["viewIds"] = viewids
        }

        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetSharedDetailsForViews - Returns shared details of the specified views.

    viewids - View ids for which sharing details are required.

    shareinfo - Returns share details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetSharedDetailsForViews(viewids interface{}) (shareinfo interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/share/shareddetails"
        config := map[string]interface{}{}
        config["viewIds"] = viewids
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            shareinfo = response.(map[string]interface{})["data"].(map[string]interface{})["sharedDetails"].(interface{})
        }
        return
    }

    /*
    GetFolders - Returns list of all accessible folders for the specified workspace.

    folders - Returns folder list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetFolders() (folders interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            folders = response.(map[string]interface{})["data"].(map[string]interface{})["folders"].(interface{})
        }
        return
    }

    /*
    CreateFolder - Create a folder in the specified workspace.

    foldername - The name of the folder.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateFolder(foldername string, config map[string]interface{}) (folderid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/"
        config["folderName"] = foldername
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            folderid = response.(map[string]interface{})["data"].(map[string]interface{})["folderId"].(string)
        }
        return
    }

    /*
    GetViews - Returns list of all accessible views for the specified workspace.

    config - Contains any additional control configurations.

    views - Returns view list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetViews(config map[string]interface{}) (views interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/views"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }

    /*
    CreateTable - Create a table in the specified workspace.

    tabledesign - Structure of the table to be created.

    viewid - Returns created table id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateTable(tabledesign map[string]interface{}) (viewid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/tables"
        config := map[string]interface{}{}
        config["tableDesign"] = tabledesign
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            viewid = response.(map[string]interface{})["data"].(map[string]interface{})["viewId"].(string)
        }
        return
    }

    /*
    CopyViews - Copy the specified views from one workspace to another workspace.

    viewids - The id of the views to be copied.

    destworkspaceid - The destination workspace id.

    config - Contains any additional control configurations.

    destorgid - Id of the organization where the destination workspace is present.

    views - Returns view list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CopyViews(viewids interface{}, destworkspaceid string, config map[string]interface{}, destorgid string) (views interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/views/copy"
        config["viewIds"] = viewids
        config["destWorkspaceId"] = destworkspaceid
        requestHeaders := workspace.requestHeaders
        if (destorgid != "") {
            requestHeaders["ZANALYTICS-DEST-ORGID"] = destorgid
        }
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }

        return
    }

    /*
    GetGroups - Returns list of groups for the specified workspace.

    groups - Returns the list of groups as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetGroups() (groups interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            groups = response.(map[string]interface{})["data"].(map[string]interface{})["groups"].(interface{})
        }
        return
    }

    /*
    CreateGroup - Create a group in the specified workspace.

    groupname - Name of the group.

    emailids - The email address of the users to be added to the group.

    config - Contains any additional control configurations.

    groupid - Returns the created group id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateGroup(groupname string, emailids interface{}, config map[string]interface{}) (groupid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups"
        config["groupName"] = groupname
        config["emailIds"] = emailids
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            groupid = response.(map[string]interface{})["data"].(map[string]interface{})["groupId"].(string)
        }
        return
    }

    /*
    GetSlideshows - Create a group in the specified workspace.

    slideshows - Returns the list of slideshows as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetSlideshows() (slideshows interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            slideshows = response.(map[string]interface{})["data"].(map[string]interface{})["slideshows"].(interface{})
        }
        return
    }

    /*
    CreateSlideshow - Create a slideshow in the specified workspace.

    slidename - Name of the slideshow to be created.

    viewids - Ids of the view to be included in the slideshow.

    config - Contains any additional control configurations.

    slideid - Returns the created slideshow id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateSlideshow(slidename string, viewids interface{}, config map[string]interface{}) (slideid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides"
        config["slideName"] = slidename
        config["viewIds"] = viewids
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            slideid = response.(map[string]interface{})["data"].(map[string]interface{})["slideId"].(string)
        }
        return
    }

    /*
    EnableDomainAccess - Enable workspace to the specified white label domain.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) EnableDomainAccess() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/wlaccess"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DisableDomainAccess - Disable workspace from the specified white label domain.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DisableDomainAccess() (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/wlaccess"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RenameFolder - Rename a specified folder in the workspace.

    folderid - The id of the folder.

    folderename - The new name of the folder.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RenameFolder(folderid, folderename string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/" + folderid
        config["folderName"] = folderename
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteFolder - Delete a specified folder in the workspace.

    folderid - The id of the folder.

    config - Contains any additional control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteFolder(folderid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/" + folderid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeFolderHierarchy - Swaps the hierarchy of a parent folder and a subfolder.

    folderid - The id of the folder.

    hierarchy - New hierarchy for the folder. (0 - Parent; 1 - Child)

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeFolderHierarchy(folderid string, hierarchy int, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/" + folderid + "/move"
        config["hierarchy"] = hierarchy
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeFolderPosition - Place the folder above the reference folder.

    folderid - Id of the folder to be moved.

    referencefolderid - Id of the reference folder.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeFolderPosition(folderid, referencefolderid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/" + folderid + "/reorder"
        config["referenceFolderId"] = referencefolderid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    MoveViewsToFolder - Move views to the mentioned folder.

    folderid - Id of the folder.

    viewids - View ids to be moved.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) MoveViewsToFolder(folderid string, viewids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/views/movetofolder"
        config["viewIds"] = viewids
        config["folderId"] = folderid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetGroupDetails - Returns details of the specified group.

    groupid - The id of the group.

    groupinfo - Returns group detail as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetGroupDetails(groupid string) (groupinfo interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups/" + groupid
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            groupinfo = response.(map[string]interface{})["data"].(map[string]interface{})["groups"].(interface{})
        }
        return
    }

    /*
    RenameGroup - Rename a specified group.

    groupid - The id of the group.

    groupname - The new name of the group.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RenameGroup(groupid, groupname string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups/" + groupid
        config["groupName"] = groupname
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddGroupMembers - Add users to the specified group.

    groupid - The id of the group.

    emailids - The email address of the users to be added to the group.

    config - Contains any additional control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddGroupMembers(groupid string, emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups/" + groupid + "/members"
        config["emailIds"] = emailids
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveGroupMembers - Remove users from the specified group.

    groupid - The id of the group.

    emailids - The email address of the users to be removed from the group.

    config - Contains any additional control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveGroupMembers(groupid string, emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups/" + groupid + "/members"
        config["emailIds"] = emailids
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteGroup - Delete a specified group.

    groupid - The id of the group.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteGroup(groupid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/groups/" + groupid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    UpdateSlideshow - Update details of the specified slideshow.

    slideid - The id of the slideshow.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateSlideshow(slideid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides/" + slideid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteSlideshow - Delete a specified slideshow in the workspace.

    slideid - The id of the slideshow.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteSlideshow(slideid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides/" + slideid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }


    /*
    GetSlideshowUrl - Returns slide URL to access the specified slideshow.

    slideid - The id of the slideshow.

    config - Contains the control configurations.

    slideurl - Returns the slideshow URL. 
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetSlideshowUrl(slideid string, config map[string]interface{}) (slideurl string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides/" + slideid + "/publish"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            slideurl = response.(map[string]interface{})["data"].(map[string]interface{})["slideUrl"].(string)
        }
        return
    }

    /*
    GetSlideshowDetails - Returns details of the specified slideshow.

    slideid - The id of the slideshow.

    slideinfo - Returns the slideshow details as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetSlideshowDetails(slideid string) (slideinfo interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/slides/" + slideid
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            slideinfo = response.(map[string]interface{})["data"].(map[string]interface{})["slideInfo"].(interface{})
        }
        return
    }

    /*
    CreateVariable - Create a variable in the workspace.

    variablename - Name of the variable to be created.

    variabledatatype - Datatype of the variable to be created.
    
    variabletype - Type of the variable to be created.

    config - Contains the control configurations.

    variableid - Returns the new variable id.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateVariable(variablename string, variabledatatype int, variabletype int, config map[string]interface{}) (variableid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/variables"
        config["variableName"] = variablename
        config["variableDataType"] = variabledatatype
        config["variableType"] = variabletype
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            variableid = response.(map[string]interface{})["data"].(map[string]interface{})["variableId"].(string)
        }
        return
    }

    /*
    UpdateVariable - Update details of the specified variable in the workspace.

    variableid - Id of the variable.

    variablename - New name for the variable.

    variabledatatype - New datatype for the variable.
    
    variabletype - New type for the variable.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateVariable(variableid string, variablename string, variabledatatype int, variabletype int, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/variables/" + variableid
        config["variableName"] = variablename
        config["variableDataType"] = variabledatatype
        config["variableType"] = variabletype
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteVariable - Delete the specified variable in the workspace.

    variableid - Id of the variable.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteVariable(variableid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/variables/" + variableid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetVariableDetails - Returns details of the specified variable.

    variableid - Id of the variable.

    variableinfo - Returns the variable details as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetVariableDetails(variableid string) (variableinfo interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/variables/" + variableid
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            variableinfo = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }

    /*
    GetVariables - Returns list of variables for the specified workspace.

    variablelist - Returns variable list as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetVariables() (variablelist interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/variables"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            variablelist = response.(map[string]interface{})["data"].(map[string]interface{})["variables"].(interface{})
        }
        return
    }

    /*
    MakeDefaultFolder - Make the specified folder as default.

    folderid - Id of the folder.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) MakeDefaultFolder(folderid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/folders/" + folderid + "/default"
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetDatasources - Returns list of datasources for the specified workspace.

    datasourcelist - Returns Datasource list as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetDatasources() (datasourcelist interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/datasources"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            datasourcelist = response.(map[string]interface{})["data"].(map[string]interface{})["dataSources"].(interface{})
        }
        return
    }

    /*
    SyncData - Make the specified folder as default.

    datasourceid - Id of the datasource.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) SyncData(datasourceid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/datasources/" + datasourceid + "/sync"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    UpdateDatasourceConnection - Update connection details for the specified datasource.

    datasourceid - Id of the datasource.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateDatasourceConnection(datasourceid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/datasources/" + datasourceid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetViews - Returns list of all views available in trash for the specified workspace.

    views - Returns view list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetTrashViews() (views interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/trash"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }

    /*
    RestoreTrashView - Restore the specified view from trash.

    viewid - Id of the view.

    config - Contains any additional control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RestoreTrashView(viewid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/trash/" + viewid
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteTrashView - Delete the specified view permanently from trash.

    viewid - Id of the view.

    config - Contains any additional control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteTrashView(viewid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/trash/" + viewid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ExportAsTemplate - Export views as templates.

    viewids - View ids to be exported as template.

    filepath - Path of the file where the data exported to be stored. ( Should be in 'atpt' format )

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ExportAsTemplate(viewids interface{}, filepath string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/template/data"
        config["viewids"] = viewids
        _, exception := workspace.ac.sendExportAPIRequest(filepath, endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetWorkspaceUsers - Returns list of users for the specified workspace.

    users - Returns the list of users as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceUsers() (users interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/users"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            users = response.(map[string]interface{})["data"].(map[string]interface{})["users"].(interface{})
        }
        return
    }

    /*
    AddWorkspaceUsers - Add users to the specified workspace.

    emailids - The email address of the users to be added.

    role - Role of the users to be added.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddWorkspaceUsers(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/users"
        config["emailIds"] = emailids
        config["role"] = role
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveWorkspaceUsers - Remove users from the specified workspace.

    emailids - The email address of the users to be removed.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveWorkspaceUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/users"
        config["emailIds"] = emailids
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeWorkspaceUserStatus - Change users staus in the specified workspace.

    emailids - The email address of the users to be modified.

    operation - New status for the users ( Values -  activate | deactivate )

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeWorkspaceUserStatus(emailids interface{}, operation string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/users/status"
        config["emailIds"] = emailids
        config["operation"] = operation
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeWorkspaceUserRole - Change users role in the specified workspace.

    emailids - The email address of the users to be modified.

    role - New role of the users.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeWorkspaceUserRole(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/users/role"
        config["emailIds"] = emailids
        config["role"] = role
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    CreateQueryTable - Create a new query table in the workspace.

    sqlquery - SQL query to construct the query table.

    querytablename - Name of the query table to be created.
    
    config - Contains the control configurations.

    viewid - Returns the newly created view id.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateQueryTable(sqlquery string, querytablename string, config map[string]interface{}) (viewid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/querytables"
        config["sqlQuery"] = sqlquery
        config["queryTableName"] = querytablename
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            viewid = response.(map[string]interface{})["data"].(map[string]interface{})["viewId"].(string)
        }
        return
    }

    /*
    EditQueryTable - Update the mentioned query table in the workspace.

    viewid - Id of the query table to be updated.

    sqlquery - New SQL query to be updated.

    config - Contains any additional control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) EditQueryTable(viewid, sqlquery string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/querytables/" + viewid
        config["sqlQuery"] = sqlquery
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }
    /*
    GetQueryTables - Returns list of all query tables for the specified workspace.
    config - Contains any additional control configurations.
    querytables - Returns query table list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetQueryTables(config map[string]interface{}) (querytables interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/querytables"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            querytables = response.(map[string]interface{})["data"].(map[string]interface{})["queryTables"].(interface{})
        }
        return
    }

    /*
    GetWorkspaceUsers - Returns list of email schedules available in the specified workspace.

    emailschedules - List of email schedules.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetEmailSchedules() (emailschedules interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            emailschedules = response.(map[string]interface{})["data"].(map[string]interface{})["emailSchedules"].(interface{})
        }
        return
    }

    /*
    CreateEmailSchedule - Create an email schedule in the specified workspace.

    schedulename - Name of the email schedule.

    viewids - View ids to be mailed.

    format - The format in which the data has to be mailed.

    emailids - The recipients' email addresses for sending views.

    scheduledetails - Contains schedule frequency, date, and time info.

    config - Contains any additional control configurations.

    scheduleid - Returns the created email schedule id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateEmailSchedule(schedulename string, viewids interface{}, format string, emailids interface{}, scheduledetails map[string]interface{}, config map[string]interface{}) (scheduleid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules"
        config["scheduleName"] = schedulename
        config["viewIds"] = viewids
        config["exportType"] = format
        config["emailIds"] = emailids
        config["scheduleDetails"] = scheduledetails
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            scheduleid = response.(map[string]interface{})["data"].(map[string]interface{})["scheduleId"].(string)
        }
        return
    }

    /*
    UpdateEmailSchedule - Update configurations of the specified email schedule in the workspace.

    scheduleid - Id for the email schedule.

    config - Contains the control configurations.

    newscheduleid - Returns the updated email schedule id value.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateEmailSchedule(scheduleid string, config map[string]interface{}) (newscheduleid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules/" + scheduleid
        response, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            newscheduleid = response.(map[string]interface{})["data"].(map[string]interface{})["scheduleId"].(string)
        }
        return
    }

    /*
    TriggerEmailSchedule - Trigger configured email schedules instantly.

    scheduleid - Id for the email schedule.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) TriggerEmailSchedule(scheduleid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules/" + scheduleid
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ChangeEmailScheduleStatus - Trigger configured email schedules instantly.

    scheduleid - Id for the email schedule.

    operation - New status for the schedule ( Values -  activate | deactivate ).

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeEmailScheduleStatus(scheduleid, operation string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules/" + scheduleid + "/status"
        config := map[string]interface{}{}
        config["operation"] = operation
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteEmailSchedule - Delete the specified email schedule in the workspace.

    scheduleid - Id for the email schedule.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteEmailSchedule(scheduleid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/emailschedules/" + scheduleid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetAggregateFormulas - Returns list of all aggregate formulas for the specified workspace.

    config - Contains any additional control configurations.

    formulas - Aggregate formula list.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAggregateFormulas(config map[string]interface{}) (formulas interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/aggregateformulas"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            formulas = response.(map[string]interface{})["data"].(map[string]interface{})["aggregateFormulas"].(interface{})
        }
        return
    }

    /*
    GetAggregateFormulaDependents - Returns list of all dependent views and formulas for the specified aggregate formula.

    formulaid - Id of the aggregate formula.

    dependents - Returns dependent list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAggregateFormulaDependents(formulaid string) (dependents interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/aggregateformulas/" + formulaid + "/dependents"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            dependents = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }

    /*
    GetAggregateFormulaValue - Returns the value of the aggregate formula.

    formulaid - Id of the aggregate formula.

    value - Aggregate formula value.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAggregateFormulaValue(formulaid string) (value string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/aggregateformulas/" + formulaid + "/value"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            value = response.(map[string]interface{})["data"].(map[string]interface{})["formulaValue"].(string)
        }
        return
    }

    /*
    CreateReport - Create a report in the specified workspace.

    config - Contains the control configurations.

    viewid - Created view id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateReport(config map[string]interface{}) (viewid string, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/reports"
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            viewid = response.(map[string]interface{})["data"].(map[string]interface{})["viewId"].(string)
        }
        return
    }

    /*
    UpdateReport - Update the design and configuration of the specified report.

    viewid - Id for the view.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateReport(viewid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/reports/" + viewid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetQueryTableDetails - Returns details of the specified query table.

    querytableid - Id of the query table.

    details - Returns query table details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetQueryTableDetails(querytableid string) (details interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/querytables/" + querytableid

        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            details = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }


    /*
    GetAutoMLAnalysis - Returns list of automl analysis for the specified workspace.

    analysis - Returns AutoML analysis list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAutoMLAnalysis() (analysis interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID + "/analysis"

        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            analysis = response.(map[string]interface{})["data"].(map[string]interface{})["analysis"].(interface{})
        }
        return
    }

    /*
    GetAutoMLAnalysisDetails - Retrieve detailed information for a specific AutoML analysis.

    analysisid - Id of the AutoML Analysis.

    details - Returns AutoML analysis details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAutoMLAnalysisDetails(analysisid string) (details interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID + "/analysis/" + analysisid

        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            details = response.(map[string]interface{})["data"].(map[string]interface{})["analysis"].(interface{})
        }
        return
    }

    /*
    GetDeploymentDetails - Returns deployment details available for an AutoML analysis model.

    analysisid - Id of the AutoML Analysis.
    modelid - Id of the AutoML Analysis Model.

    deployments - Returns deployment details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetDeploymentDetails(analysisid, modelid string) (deployments interface{}, serverexception *ServerException) {
        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/models/" + modelid + "/deployments"

        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            deployments = response.(map[string]interface{})["data"].(map[string]interface{})["deployments"].(interface{})
        }
        return
    }

    /*
    CreateAutoMLAnalysis - Create a new AutoML analysis within the workspace.

    name - Name of the AutoML analysis.
    trainingtableid - Id of the training table.
    predictiontype - Prediction type (REGRESSION, CLASSIFICATION, CLUSTERING).
    features - List of feature column names.
    serveroption - Compute size option.
    algorithms - Algorithms configuration.
    config - Contains any additional control parameters.

    analysisid - Returns created AutoML Analysis Id as string.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateAutoMLAnalysis(
        name string,
        trainingtableid string,
        predictiontype string,
        features []interface{},
        serveroption int,
        algorithms map[string]interface{},
        config map[string]interface{},
    ) (analysisid string, serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        config["name"] = name
        config["trainingTableId"] = trainingtableid
        config["predictionType"] = predictiontype
        config["features"] = features
        config["serverOption"] = serveroption
        config["algorithms"] = algorithms

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID + "/analysis"

        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            analysisid = fmt.Sprintf("%v", response.(map[string]interface{})["data"].(map[string]interface{})["id"])
        }
        return
    }

    /*
    DeleteAutoMLAnalysis - Delete a specified AutoML analysis from the workspace.

    analysisid - Id of the AutoML Analysis.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteAutoMLAnalysis(analysisid string, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID + "/analysis/" + analysisid

        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    DeleteAutoMLAnalysisModel - Delete a specified model from an AutoML analysis.

    analysisid - Id of the AutoML Analysis.
    modelid - Id of the model within the analysis.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteAutoMLAnalysisModel(
        analysisid string,
        modelid string,
        config map[string]interface{},
    ) (serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/models/" + modelid

        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    CreateAutoMLAnalysisDeployment - Deploy the AutoML analysis model.

    analysisid - Id of the AutoML Analysis.
    modelid - Id of the AutoML Analysis model.
    inputtableid - Id of the input table.
    outputtable - Name of the output table to be created.
    outputcolumns - List of output column names.
    predictioncolumn - Name of the prediction column.
    serveroption - Compute size option.
    importtype - Import type (APPEND, TRUNCATEADD, UPDATEADD).
    scheduledetails - Schedule configuration.
    config - Contains any additional control parameters.

    deployments - Returns created AutoML deployment details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateAutoMLAnalysisDeployment(
        analysisid string,
        modelid string,
        inputtableid string,
        outputtable string,
        outputcolumns []interface{},
        predictioncolumn string,
        serveroption int,
        importtype string,
        scheduledetails interface{},
        config map[string]interface{},
    ) (deployments interface{}, serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        config["inputTableId"] = inputtableid
        config["outputTable"] = outputtable
        config["outputColumns"] = outputcolumns
        config["predictionColumn"] = predictioncolumn
        config["serverOption"] = serveroption
        config["importType"] = importtype

        if scheduledetails == nil {
            config["scheduleDetails"] = "none"
        } else {
            config["scheduleDetails"] = scheduledetails
        }

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/models/" + modelid + "/deployments"

        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            deployments = response.(map[string]interface{})["data"].(map[string]interface{})["deployments"].(interface{})
        }
        return
    }

    /*
    DeployAutoMLAnalysis - Execute an AutoML analysis deployment.

    analysisid - Id of the AutoML Analysis.
    deploymentid - Id of the deployment.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeployAutoMLAnalysis(
        analysisid string,
        deploymentid string,
        config map[string]interface{},
    ) (serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/deployments/" + deploymentid + "/execute"

        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }


    /*
    DeleteAutoMLAnalysisDeployment - Delete an AutoML analysis deployment.

    analysisid - Id of the AutoML Analysis.
    deploymentid - Id of the deployment.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteAutoMLAnalysisDeployment(
        analysisid string,
        deploymentid string,
        config map[string]interface{},
    ) (serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/deployments/" + deploymentid

        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    AutoMLAnalysisPrediction - Get predictions using a trained AutoML model.

    analysisid - Id of the AutoML Analysis.
    modelid - Id of the AutoML Analysis model.
    features - Feature name to value mapping.
    config - Contains any additional control parameters.

    prediction - Returns prediction details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AutoMLAnalysisPrediction(
        analysisid string,
        modelid string,
        features map[string]interface{},
        config map[string]interface{},
    ) (prediction interface{}, serverexception *ServerException) {

        if config == nil {
            config = make(map[string]interface{})
        }

        config["features"] = features

        endpoint := "/restapi/v2/automl/workspaces/" + workspace.workspaceID +
            "/analysis/" + analysisid + "/models/" + modelid + "/whatif"

        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            prediction = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }





    /*
    GetTags - Returns list of all tags for the specified workspace.
    tags - Returns tags list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetTags() (tags interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/tags"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            tags = response.(map[string]interface{})["data"].(map[string]interface{})["tags"].(interface{})
        }
        return
    }
    /*
    CreateTag - Create a tag in the specified workspace.
    tagname - Name of the tag to be created.
    colorcode - Color of the tag in HEX color code.
    config - Contains any additional control configurations.
    tagid - Returns the new tag id.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateTag(tagname, colorcode string, config map[string]interface{}) (tagid string, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["name"] = tagname
        config["colorCode"] = colorcode
        endpoint := workspace.workspaceEndpoint + "/tags"
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            tagid = fmt.Sprintf("%v", response.(map[string]interface{})["data"].(map[string]interface{})["tagId"])
        }
        return
    }
    /*
    UpdateTag - Update details of the specified tag in the workspace.
    tagid - Id of the tag.
    config - Contains the control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateTag(tagid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/tags/" + tagid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    DeleteTag - Delete the specified tag from the workspace.
    tagid - Id of the tag.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteTag(tagid string) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/tags/" + tagid
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    AddTagToViews - Adds the specified tag to multiple views in the workspace.
    tagid - Id of the tag.
    viewids - View ids to be associated with the tag.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) AddTagToViews(tagid string, viewids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["viewIds"] = viewids
        endpoint := workspace.workspaceEndpoint + "/tags/" + tagid + "/views"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    RemoveTagFromViews - Removes the specified tag from multiple views in the workspace.
    tagid - Id of the tag.
    viewids - View ids to be dissociated. Pass nil when dissociateAll is true.
    dissociateAll - To dissociate the tag from all associated views.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RemoveTagFromViews(tagid string, viewids interface{}, dissociateAll bool, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        if dissociateAll {
            config["dissociateAll"] = true
        } else {
            config["viewIds"] = viewids
        }
        endpoint := workspace.workspaceEndpoint + "/tags/" + tagid + "/views"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetTaggedViews - Returns the list of views associated with the specified tag.
    tagid - Id of the tag.
    views - Returns view list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetTaggedViews(tagid string) (views interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/tags/" + tagid + "/views"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            views = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }
    /*
    GetLinkedWorkspaces - Returns list of workspaces linked to the specified master workspace.
    linkedworkspaces - Returns the linked workspaces list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetLinkedWorkspaces() (linkedworkspaces interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            linkedworkspaces = response.(map[string]interface{})["data"].(map[string]interface{})["linkedWorkspaces"].(interface{})
        }
        return
    }
    /*
    GetLinkableWorkspaces - Returns list of organizations and workspaces that can be linked to the specified master workspace.
    orgs - Returns the organizations with their linkable workspaces as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetLinkableWorkspaces() (orgs interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces/linkable"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            orgs = response.(map[string]interface{})["data"].(map[string]interface{})["orgs"].(interface{})
        }
        return
    }
    /*
    GetWorkspaceLinkingCompatibility - Returns the linking compatibility details for the specified client workspaces.
    clients - Contains the client workspaces to be verified for linking compatibility.
    config - Contains any additional control configurations.
    compatibility - Returns the client workspace compatibility details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceLinkingCompatibility(clients interface{}, config map[string]interface{}) (compatibility interface{}, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["clients"] = clients
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces/compatibility"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            compatibility = response.(map[string]interface{})["data"].(map[string]interface{})["clients"].(interface{})
        }
        return
    }
    /*
    LinkWorkspaces - Link the specified client workspaces to the master workspace.
    clients - Contains the client workspaces to be linked with the master workspace.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) LinkWorkspaces(clients interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["clients"] = clients
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    UnlinkWorkspaces - Unlink the client workspaces from the specified master workspace.
    scope - Scope of the unlink operation.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UnlinkWorkspaces(scope string, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["scope"] = scope
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    SyncLinkedWorkspaces - Sync the metadata of the master workspace to its linked client workspaces.
    scope - Scope of the sync operation.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) SyncLinkedWorkspaces(scope string, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["scope"] = scope
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces/sync"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetLinkedWorkspaceSyncDetails - Returns the sync details of the specified linked workspaces.
    sandboxids - Ids of the linked workspaces for which the sync details are fetched.
    config - Contains any additional control configurations.
    workspaces - Returns the linked workspace sync details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetLinkedWorkspaceSyncDetails(sandboxids interface{}, config map[string]interface{}) (workspaces interface{}, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["sandboxIds"] = sandboxids
        endpoint := workspace.workspaceEndpoint + "/linkedworkspaces/sync"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            workspaces = response.(map[string]interface{})["data"].(map[string]interface{})["workspaces"].(interface{})
        }
        return
    }
    /*
    GetWorkspaceBackups - Returns the backup configuration and the list of backups available for the specified workspace.
    backups - Returns the workspace backup details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceBackups() (backups interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/backups"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            backups = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    BackupWorkspaceNow - Trigger an instant backup for the specified workspace.
    config - Contains any additional control configurations.
    backupdetails - Returns the triggered backup details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) BackupWorkspaceNow(config map[string]interface{}) (backupdetails interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/backups"
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            backupdetails = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    GetWorkspaceBackupStatus - Returns the status of the specified workspace backup.
    backupid - Id of the backup.
    backupstatus - Returns the backup status details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceBackupStatus(backupid string) (backupstatus interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/backups/" + backupid + "/status"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            backupstatus = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    DownloadWorkspaceBackup - Download the specified workspace backup.
    backupid - Id of the backup.
    filepath - Path of the file where the downloaded backup is to be stored.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DownloadWorkspaceBackup(backupid string, filepath string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/backups/" + backupid + "/download"
        _, exception := workspace.ac.sendExportAPIRequest(filepath, endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    RestoreWorkspaceFromBackup - Restore the specified workspace from the given backup.
    backupid - Id of the backup.
    confirmrestore - Pass true to confirm that the existing workspace data can be overwritten.
    config - Contains any additional control configurations.
    restoredetails - Returns the triggered restore details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RestoreWorkspaceFromBackup(backupid string, confirmrestore bool, config map[string]interface{}) (restoredetails interface{}, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["confirmRestore"] = confirmrestore
        endpoint := workspace.workspaceEndpoint + "/backups/" + backupid + "/restore"
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            restoredetails = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    GetWorkspaceRestoreStatus - Returns the status of the specified workspace restore.
    restoreid - Id of the restore.
    restorestatus - Returns the restore status details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceRestoreStatus(restoreid string) (restorestatus interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/restores/" + restoreid + "/status"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            restorestatus = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    CreateDashboard - Create a dashboard in the specified workspace.
    displayname - Name of the dashboard.
    layout - Layout configuration of the dashboard.
    config - Contains any additional control configurations.
    dashboardid - Returns the new dashboard id as string.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) CreateDashboard(displayname string, layout string, config map[string]interface{}) (dashboardid string, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["displayName"] = displayname
        config["layout"] = layout
        endpoint := workspace.workspaceEndpoint + "/dashboards"
        response, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            dashboardid = fmt.Sprintf("%v", response.(map[string]interface{})["data"].(map[string]interface{})["dashboardId"])
        }
        return
    }
    /*
    UpdateDashboard - Update the specified dashboard in the workspace.
    dashboardid - Id of the dashboard.
    config - Contains the dashboard configurations to be updated.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateDashboard(dashboardid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/dashboards/" + dashboardid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetDashboardMetadata - Returns the metadata of the specified dashboard.
    dashboardid - Id of the dashboard.
    config - Contains any additional control configurations.
    dashboardconfig - Returns the dashboard configuration as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetDashboardMetadata(dashboardid string, config map[string]interface{}) (dashboardconfig interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/dashboards/" + dashboardid + "/metadata"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            dashboardconfig = response.(map[string]interface{})["data"].(map[string]interface{})["dashboardConfig"].(interface{})
        }
        return
    }
    /*
    GetReportMetadata - Returns the metadata of the specified report.
    viewid - Id of the report.
    reportconfig - Returns the report configuration as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetReportMetadata(viewid string) (reportconfig interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/reports/" + viewid + "/metadata"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            reportconfig = response.(map[string]interface{})["data"].(map[string]interface{})["reportConfig"].(interface{})
        }
        return
    }
    /*
    GetAlertsInWorkspace - Returns list of data alerts available in the specified workspace.
    alerts - Returns the data alerts list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAlertsInWorkspace() (alerts interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/alerts"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            alerts = response.(map[string]interface{})["data"].(map[string]interface{})["alerts"].(interface{})
        }
        return
    }
    /*
    GetAlertConfiguration - Returns the configuration of the specified data alert.
    alertid - Id of the data alert.
    alertconfig - Returns the data alert configuration as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAlertConfiguration(alertid string) (alertconfig interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/alerts/" + alertid
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            alertconfig = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    UpdateAlert - Update the specified data alert in the workspace.
    alertid - Id of the data alert.
    alertname - Name of the data alert.
    scheduledetails - Contains the schedule configurations of the data alert.
    rules - Contains the rules to be evaluated by the data alert.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateAlert(alertid string, alertname string, scheduledetails map[string]interface{}, rules interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["alertName"] = alertname
        config["scheduleDetails"] = scheduledetails
        config["rules"] = rules
        endpoint := workspace.workspaceEndpoint + "/alerts/" + alertid
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    DeleteAlerts - Delete the specified data alerts from the workspace.
    alertids - Ids of the data alerts to be deleted.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) DeleteAlerts(alertids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["alertIds"] = alertids
        endpoint := workspace.workspaceEndpoint + "/alerts"
        _, exception := workspace.ac.sendAPIRequest("DELETE", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    ChangeAlertStatus - Enable or disable the specified data alerts in the workspace.
    alertids - Ids of the data alerts.
    enabled - Pass true to enable the data alerts and false to disable them.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) ChangeAlertStatus(alertids interface{}, enabled bool, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["alertIds"] = alertids
        config["enabled"] = enabled
        endpoint := workspace.workspaceEndpoint + "/alerts/status"
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    RunAlert - Execute the specified data alert immediately.
    alertid - Id of the data alert.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) RunAlert(alertid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/alerts/" + alertid + "/execute"
        _, exception := workspace.ac.sendAPIRequest("POST", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetAlertEvents - Returns the execution events of the specified data alert.
    alertid - Id of the data alert.
    config - Contains any additional control configurations.
    alertevents - Returns the data alert events along with the page details as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetAlertEvents(alertid string, config map[string]interface{}) (alertevents interface{}, serverexception *ServerException) {
        endpoint := workspace.workspaceEndpoint + "/alerts/" + alertid + "/events"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            alertevents = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    GetWorkspaceAccessRestrictions - Returns the access restriction settings configured for the specified workspace.
    accessrestrictions - Returns the workspace access restriction settings as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) GetWorkspaceAccessRestrictions() (accessrestrictions interface{}, serverexception *ServerException) {
        endpoint := workspace.securityControlsEndpoint + "/access-restrictions"
        response, exception := workspace.ac.sendAPIRequest("GET", endpoint, nil, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            accessrestrictions = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }
    /*
    UpdateWorkspaceAccessRestrictions - Update the access restriction settings of the specified workspace.
    config - Contains the access restriction configurations to be updated.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (workspace *WorkspaceAPI) UpdateWorkspaceAccessRestrictions(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := workspace.securityControlsEndpoint + "/access-restrictions"
        _, exception := workspace.ac.sendAPIRequest("PUT", endpoint, config, workspace.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    ViewAPI contains view level operations.
    */
    type ViewAPI struct {
        ac *Client
        requestHeaders map[string]string    
        viewEndpoint string
    }

    /*
    GetViewInstance - Returns the ViewAPI object.

    ac - Client structure pointer.

    orgid - The ID of the organization.

    workspaceid - Id of the workspace.
    
    viewid - Id of the view.
    */
    func GetViewInstance(ac *Client, orgid string, workspaceid string, viewid string) ViewAPI {
        view := ViewAPI{
            ac : ac,
            requestHeaders : map[string]string{
                "ZANALYTICS-ORGID" : orgid,
            },
            viewEndpoint : "/restapi/v2/workspaces/" + workspaceid + "/views/" + viewid,
        }
        return view
    }

    /*
    Rename - Rename a specified view in the workspace.

    viewename - The new name of the view.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) Rename(viewename string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint
        config["viewName"] = viewename
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    Delete - Delete a specified view in the workspace.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) Delete(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    SaveAs - Copy a specified view within the workspace.

    newviewname - The name of the new view.

    config - Contains the control configurations.

    viewid - Returns id of the new view.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) SaveAs(newviewname string, config map[string]interface{}) (viewid string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/saveas"
        config["viewName"] = newviewname
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            viewid = response.(map[string]interface{})["data"].(map[string]interface{})["viewId"].(string)
        }
        return
    }

    /*
    CopyFormulas - Copy the specified formulas from one table to another within the workspace or across workspaces.

    formulanames - The name of the formula columns to be copied.

    destworkspaceid - The ID of the destination workspace.

    config - Contains the control configurations.

    destorgid - Id of the organization where the destination workspace is present.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) CopyFormulas(formulanames interface{}, destworkspaceid string, config map[string]interface{}, destorgid string) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/formulas/copy"
        config["formulaColumnNames"] = formulanames
        config["destWorkspaceId"] = destworkspaceid

        requestHeaders := view.requestHeaders
        if (destorgid != "") {
            requestHeaders["ZANALYTICS-DEST-ORGID"] = destorgid
        }

        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddFavorite - Adds a specified view as favorite.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddFavorite() (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/favorite"
        _, exception := view.ac.sendAPIRequest("POST", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveFavorite - Remove a specified view from favorite.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RemoveFavorite() (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/favorite"
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    CreateSimilarViews - Create reports for the specified table based on the reference table.

    refviewid - The ID of the reference view.

    folderid - The folder id where the views to be saved.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) CreateSimilarViews(refviewid, folderid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/similarviews"
        config["referenceViewId"] = refviewid
        config["folderId"] = folderid
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AutoAnalyse - Auto generate reports for the specified table.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AutoAnalyse(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/autoanalyse"
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetMyPermissions - Returns permissions for the specified view.

    permissions - Returns the permission details as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetMyPermissions() (permissions interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/share/userpermissions"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            permissions = response.(map[string]interface{})["data"].(map[string]interface{})["permissions"].(interface{})
        }
        return
    }

    /*
    GetViewUrl - Returns the URL to access the specified view.

    config - Contains the control configurations.

    viewurl - Returns the view URL.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetViewUrl(config map[string]interface{}) (viewurl string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            viewurl = response.(map[string]interface{})["data"].(map[string]interface{})["viewUrl"].(string)
        }
        return
    }

    /*
    GetEmbedUrl - Returns embed URL to access the specified view.

    config - Contains the control configurations.

    embedurl - Returns the embed URL.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetEmbedUrl(config map[string]interface{}) (embedurl string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/embed"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            embedurl = response.(map[string]interface{})["data"].(map[string]interface{})["embedUrl"].(string)
        }
        return
    }

    /*
    GetPrivateUrl - Returns private URL to access the specified view.

    config - Contains the control configurations.

    privateurl - Returns the private URL.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetPrivateUrl(config map[string]interface{}) (privateurl string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/privatelink"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            privateurl = response.(map[string]interface{})["data"].(map[string]interface{})["privateUrl"].(string)
        }
        return
    }

    /*
    CreatePrivateUrl - Create a private URL for the specified view.

    config - Contains the control configurations.

    privateurl - Returns the private URL.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) CreatePrivateUrl(config map[string]interface{}) (privateurl string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/privatelink"
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            privateurl = response.(map[string]interface{})["data"].(map[string]interface{})["privateUrl"].(string)
        }
        return
    }

    /*
    RemovePrivateAccess - Remove private link access for the specified view.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RemovePrivateAccess() (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/privatelink"
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    MakeViewPublic - Make the specified view publically accessible.

    config - Contains the control configurations.

    privateurl - Returns the view URL.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) MakeViewPublic(config map[string]interface{}) (privateurl string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/public"
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            privateurl = response.(map[string]interface{})["data"].(map[string]interface{})["publicUrl"].(string)
        }
        return
    }

    /*
    RemovePublicAccess - Remove public access for the specified view.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RemovePublicAccess() (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/public"
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetPublishConfigurations - Returns details of the specified slideshow.

    publishinfo - Returns publish configurations for the specified view.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetPublishConfigurations() (publishinfo interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/config"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            publishinfo = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }

    /*
    UpdatePublishConfigurations - Update publish configurations for the specified view.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) UpdatePublishConfigurations(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/publish/config"
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddColumn - Add a column in the specified table.

    columnname - The name of the column.

    datatype - The data-type of the column.

    config - Contains the control configurations.

    columnid - Returns id of the new column.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddColumn(columnname, datatype string, config map[string]interface{}) (columnid string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns"
        config["columnName"] = columnname
        config["dataType"] = datatype
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            columnid = response.(map[string]interface{})["data"].(map[string]interface{})["columnId"].(string)
        }
        return
    }

    /*
    HideColumns - Hide the specified columns in the table.

    columnids - Ids of the column to be hidden.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) HideColumns(columnids interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/hide"
        config := map[string]interface{}{}
        config["columnIds"] = columnids
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ShowColumns - Show the specified hidden columns in the table.

    columnids - Ids of the column to be shown.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) ShowColumns(columnids interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/show"
        config := map[string]interface{}{}
        config["columnIds"] = columnids
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddRow - Add a single row in the specified table.

    columnvalues - Contains the values for the row. The column names are the key.

    config - Contains the control configurations.

    data - Returns details of the added rows as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddRow(columnvalues, config map[string]interface{}) (data interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/rows"
        config["columns"] = columnvalues
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            data = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    UpdateRow - Update rows in the specified table.

    columnvalues - Contains the values for the row. The column names are the key.

    criteria - The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows.

    config - Contains the control configurations.

    data - Returns details of the updated rows as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) UpdateRow(columnvalues map[string]interface{}, criteria string, config map[string]interface{}) (data interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/rows"
        config["columns"] = columnvalues
        if(criteria != ""){
            config["criteria"] = criteria
        }
        response, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            data = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    DeleteRow - Delete rows in the specified table.

    criteria - The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows.

    config - Contains the control configurations.

    deletedCount - Returns deleted rows count.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) DeleteRow(criteria string, config map[string]interface{}) (deletedCount float64, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/rows"
        if(criteria != ""){
            config["criteria"] = criteria
        }
        response, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            deletedCount = response.(map[string]interface{})["data"].(map[string]interface{})["deletedRows"].(float64)
        }
        return
    }

    /*
    RenameColumn - Rename a specified column in the table.

    columnid - The id of the column.

    columnname - The new name of the column.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RenameColumn(columnid, columnname string) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid
        config := map[string]interface{}{}
        config["columnName"] = columnname
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteColumn - Delete a specified column in the table.

    columnid - The id of the column.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) DeleteColumn(columnid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AddLookup - Add a lookup in the specified child table.

    columnid - The id of the column.

    refviewid - The ID of the table contains the parent column.

    refcolumnid - The ID of the parent column.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddLookup(columnid, refviewid, refcolumnid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid + "/lookup"
        config["referenceViewId"] = refviewid
        config["referenceColumnId"] = refcolumnid
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RemoveLookup - Remove the lookup for the specified column in the table.

    columnid - The id of the column.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RemoveLookup(columnid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid + "/lookup"
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    AutoAnalyseColumn - Auto generate reports for the specified column.

    columnid - The id of the column.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AutoAnalyseColumn(columnid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid + "/autoanalyse"
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetViewDependents - Returns list of dependents views for the specified view.

    dependents - Returns dependent list as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetViewDependents() (dependents interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/dependents"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            dependents = response.(map[string]interface{})["data"].(map[string]interface{})["views"].(interface{})
        }
        return
    }

    /*
    GetColumnDependents - Returns list of dependents views and formulas for the specified column.

    columnid - The id of the column.

    dependents - Returns dependent list as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetColumnDependents(columnid string) (dependents interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/columns/" + columnid + "/dependents"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            dependents = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }

    /*
    UpdateSharedDetails - Update the existing sharing configuration for views.

    config - Contains the control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) UpdateSharedDetails(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/share"
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    RefetchData - Sync data from available datasource for the specified view.

    config - Contains any additonal control configurations.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RefetchData(config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/sync"
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetLastImportDetails - Returns last import details of the specified view.

    importDetails - Returns the last import details as interface.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetLastImportDetails() (importDetails interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/importdetails"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            importDetails = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }


    /*
    GetFormulaColumns - Returns list of all formula columns for the specified table.

    formulas - Returns formula column list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetFormulaColumns() (formulas interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/formulacolumns"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            formulas = response.(map[string]interface{})["data"].(map[string]interface{})["formulaColumns"].(interface{})
        }
        return
    }

    /*
    AddFormulaColumn - Add a formula column in the specified table.

    formulaname - Name of the formula column to be created.

    expression - Formula expression.

    config - Contains the control configurations.

    formulaid - Returns id of the formula created.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddFormulaColumn(formulaname string, expression string, config map[string]interface{}) (formulaid string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/formulacolumns"
        config["formulaName"] = formulaname
        config["expression"] = expression
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            formulaid = response.(map[string]interface{})["data"].(map[string]interface{})["formulaId"].(string)
        }
        return
    }

    /*
    EditFormulaColumn - Edit the specified formula column.

    formulaid - Id of the formula column to be updated.

    expression - Formula expression.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) EditFormulaColumn(formulaid string, expression string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/formulacolumns/" + formulaid
        config["expression"] = expression
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteFormulaColumn - Delete the specified formula column.

    formulaid - Id of the formula column to be deleted.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) DeleteFormulaColumn(formulaid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/formulacolumns/" + formulaid
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    GetAggregateFormulas - Returns list of all aggregate formulas for the specified table.

    formulas - Returns aggregate formula list as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetAggregateFormulas() (formulas interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/aggregateformulas"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            formulas = response.(map[string]interface{})["data"].(map[string]interface{})["aggregateFormulas"].(interface{})
        }
        return
    }

    /*
    AddAggregateFormula - Add an aggregate formula in the specified table.

    formulaname - Name of the formula to be created.

    expression - Formula expression.

    config - Contains the control configurations.

    formulaid - Returns id of the created formula.
    
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddAggregateFormula(formulaname string, expression string, config map[string]interface{}) (formulaid string, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/aggregateformulas"
        config["formulaName"] = formulaname
        config["expression"] = expression
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            formulaid = response.(map[string]interface{})["data"].(map[string]interface{})["formulaId"].(string)
        }
        return
    }

    /*
    EditAggregateFormula - Edit the specified aggregate formula.

    formulaid - Id of the aggregate formula to be updated.

    expression - Formula expression.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) EditAggregateFormula(formulaid string, expression string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/aggregateformulas/" + formulaid
        config["expression"] = expression
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    DeleteAggregateFormula - Delete the specified aggregate formula.

    formulaid - Id of the aggregate formula to be deleted.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) DeleteAggregateFormula(formulaid string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/aggregateformulas/" + formulaid
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    ReorderColumns - Updates the column order of the current table.

    columnids - A list containing the full set of column IDs in the new order in which they should appear.
    config - Contains any additional control parameters.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) ReorderColumns(columnids []interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }

        config["columns"] = columnids
        endpoint := view.viewEndpoint + "/columns/reorder"

        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    SortDataByColumns - Sorts the data in the table based on the specified columns.

    columns - A list of column IDs to sort by.
    sortorder - Sorting order indicator.
                1 -> Ascending
                2 -> Descending
    resetsort - If true, resets any existing sort configuration.
    config - Contains any additional control parameters.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) SortDataByColumns(columns []interface{}, sortorder int, resetsort bool, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }

        if resetsort {
            config["resetSort"] = "true"
        } else {
            config["sortOrder"] = sortorder
            config["columns"] = columns
        }

        endpoint := view.viewEndpoint + "/data/sort"
        _, exception := view.ac.sendAPIRequest("PUT", endpoint, config, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }

    /*
    GetTableMetadata - Retrieves metadata information for the current table.

    metadata - Returns table metadata details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetTableMetadata() (metadata interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/metadata"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            metadata = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }




    /*
    GetViewTags - Returns the list of tags associated with the specified view.
    tags - Returns tag list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetViewTags() (tags interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/tags"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            tags = response.(map[string]interface{})["data"].(map[string]interface{})["tags"].(interface{})
        }
        return
    }
    /*
    AddTagsToView - Adds multiple tags to the specified view.
    tagids - Tag ids to be associated with the view.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) AddTagsToView(tagids interface{}, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["tagIds"] = tagids
        endpoint := view.viewEndpoint + "/tags"
        _, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    RemoveTagsFromView - Removes multiple tags from the specified view.
    tagids - Tag ids to be dissociated. Pass nil when dissociateAll is true.
    dissociateAll - To dissociate all tags from the view.
    config - Contains any additional control configurations.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) RemoveTagsFromView(tagids interface{}, dissociateAll bool, config map[string]interface{}) (serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        if dissociateAll {
            config["dissociateAll"] = true
        } else {
            config["tagIds"] = tagids
        }
        endpoint := view.viewEndpoint + "/tags"
        _, exception := view.ac.sendAPIRequest("DELETE", endpoint, config, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        }
        return
    }
    /*
    GetAlertsInView - Returns list of data alerts configured for the specified view.
    alerts - Returns the data alerts list as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetAlertsInView() (alerts interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/alerts"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            alerts = response.(map[string]interface{})["data"].(map[string]interface{})["alerts"].(interface{})
        }
        return
    }
    /*
    CreateAlert - Create a data alert for the specified view.
    alertname - Name of the data alert.
    scheduledetails - Contains the schedule configurations of the data alert.
    rules - Contains the rules to be evaluated by the data alert.
    config - Contains any additional control configurations.
    alertid - Returns the new data alert id as string.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) CreateAlert(alertname string, scheduledetails map[string]interface{}, rules interface{}, config map[string]interface{}) (alertid string, serverexception *ServerException) {
        if config == nil {
            config = make(map[string]interface{})
        }
        config["alertName"] = alertname
        config["scheduleDetails"] = scheduledetails
        config["rules"] = rules
        endpoint := view.viewEndpoint + "/alerts"
        response, exception := view.ac.sendAPIRequest("POST", endpoint, config, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            alertid = fmt.Sprintf("%v", response.(map[string]interface{})["data"].(map[string]interface{})["alertId"])
        }
        return
    }
    /*
    GetViewMetadataForAlert - Returns the view metadata that can be used while configuring a data alert for the specified view.
    metadata - Returns the view metadata for data alert configuration as interface.
    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (view *ViewAPI) GetViewMetadataForAlert() (metadata interface{}, serverexception *ServerException) {
        endpoint := view.viewEndpoint + "/alerts/metadata"
        response, exception := view.ac.sendAPIRequest("GET", endpoint, nil, view.requestHeaders)
        if exception != nil {
            serverexception = exception
        } else {
            metadata = response.(map[string]interface{})["data"].(interface{})
        }
        return
    }

    /*
    BulkAPI contains bulk data operation.
    */
    type BulkAPI struct {
        ac *Client
        requestHeaders map[string]string    
        dataEndpoint string
        bulkEndpoint string
    }

    /*
    GetBulkInstance - Returns the BulkAPI object.

    ac - Client structure pointer.

    orgid - The ID of the organization.

    workspaceid - Id of the workspace.
        */
    func GetBulkInstance(ac *Client, orgid string, workspaceid string) BulkAPI {
        bulk := BulkAPI{
            ac : ac,
            requestHeaders : map[string]string{
                "ZANALYTICS-ORGID" : orgid,
            },
            dataEndpoint : "/restapi/v2/workspaces/" + workspaceid,
            bulkEndpoint : "/restapi/v2/bulk/workspaces/" + workspaceid,
        }
        return bulk
    }

    /*
    ImportDataInNewTable - Create a new table and import the data contained in the mentioned file into the created table.

    tablename - Name of the new table to be created.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    config - Contains the control configurations.

    result - Returns the import result as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportDataInNewTable(tablename, filetype, autoidentify, filepath string, config map[string]interface{}) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.dataEndpoint + "/data"
        
        config["tableName"] = tablename
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendImportAPIRequest(filepath, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ImportData - Create a new table and import the data contained in the mentioned file into the created table.

    viewid - Id of the view where the data to be imported.

    importtype - The type of import. Can be one of - append, truncateadd, updateadd.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    config - Contains the control configurations.

    result - Returns the import result as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportData(viewid, importtype, filetype, autoidentify, filepath string, config map[string]interface{}) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.dataEndpoint + "/views/" + viewid + "/data"
        
        config["importType"] = importtype
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendImportAPIRequest(filepath, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ImportRawDataInNewTable - Create a new table and import the raw data provided into the created table.

    tablename - Name of the new table to be created.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    data - Raw data to be imported.

    config - Contains the control configurations.

    result - Returns the import result as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportRawDataInNewTable(tablename, filetype, autoidentify, data string, config map[string]interface{}) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.dataEndpoint + "/data"

        config["tableName"] = tablename
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendRawImportAPIRequest(data, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ImportRawData - Import the raw data provided into the table.

    viewid - Id of the view where the data to be imported.

    importtype - The type of import. Can be one of - append, truncateadd, updateadd.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    data - Raw data to be imported.

    config - Contains the control configurations.

    result - Returns the import result as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportRawData(viewid, importtype, filetype, autoidentify, data string, config map[string]interface{}) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.dataEndpoint + "/views/" + viewid + "/data"

        config["importType"] = importtype
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendRawImportAPIRequest(data, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ImportBulkDataInNewTable - Asynchronously create a new table and import the data contained in the mentioned file into the created table.

    tablename - Name of the new table to be created.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    config - Contains the control configurations.

    jobid - Returns the import job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportBulkDataInNewTable(tablename, filetype, autoidentify, filepath string, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/data"
        
        config["tableName"] = tablename
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendImportAPIRequest(filepath, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    ImportBulkData - Asynchronously import the data contained in the mentioned file into the table.

    viewid - Id of the view where the data to be imported.

    importtype - The type of import. Can be one of - append, truncateadd, updateadd.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    config - Contains the control configurations.

    jobid - Returns the import job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportBulkData(viewid, importtype, filetype, autoidentify, filepath string, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/views/" + viewid + "/data"
        
        config["importType"] = importtype
        config["fileType"] = filetype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendImportAPIRequest(filepath, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    ImportBulkDataInNewTable - Asynchronously create a new table and import the data contained in the mentioned file into the created table.

    tablename - Name of the new table to be created.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    batchSize - Number of lines per batch

    config - Contains the control configurations.

    jobid - Returns the import job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportBulkDataInNewTableAsBatches(tablename, autoidentify, filepath string, batchSize int, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/data/batch"
        
        config["tableName"] = tablename
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendBatchImportAPIRequest(filepath, endpoint, batchSize, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    ImportBulkData - Asynchronously import the data contained in the mentioned file into the table.

    viewid - Id of the view where the data to be imported.

    importtype - The type of import. Can be one of - append, truncateadd, updateadd.

    filetype - Type of the file to be imported.

    autoidentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.

    filepath - Path of the file to be imported.

    batchSize - Number of lines per batch.

    config - Contains the control configurations.

    jobid - Returns the import job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ImportBulkDataAsBatches(viewid, importtype, autoidentify, filepath string, batchSize int, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/views/" + viewid + "/data/batch"
        
        config["importType"] = importtype
        config["autoIdentify"] = autoidentify

        response, exception := bulk.ac.sendBatchImportAPIRequest(filepath, endpoint, batchSize, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    GetImportJobDetails - Returns the details of the import job.

    jobid - Id of the import job.

    result - Returns the import job details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) GetImportJobDetails(jobid string) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/importjobs/" + jobid

        response, exception := bulk.ac.sendAPIRequest("GET", endpoint, nil, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }


    /*
    ExportData - Export the mentioned table (or) view data.

    viewid - Id of the view to be exported.

    responseformat - The format in which the data is to be exported.

    filepath - Path of the file where the data exported to be stored.

    config - Contains the control configurations.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ExportData(viewid, responseformat, filepath string, config map[string]interface{}) (serverexception *ServerException) {
        endpoint := bulk.dataEndpoint + "/views/" + viewid + "/data"
        config["responseFormat"] = responseformat
        _, exception := bulk.ac.sendExportAPIRequest(filepath, endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }

    /*
    InitiateBulkExport - Initiate asynchronous export for the mentioned table (or) view data.

    viewid - Id of the view to be exported.

    responseformat - The format in which the data is to be exported.

    config - Contains the control configurations.

    jobid - Returns the export job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) InitiateBulkExport(viewid, responseformat string, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/views/" + viewid + "/data"
        config["responseFormat"] = responseformat
        response, exception := bulk.ac.sendAPIRequest("GET", endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    InitiateBulkExportUsingSQL - Initiate asynchronous export with the given SQL Query.

    sqlquery - The SQL Query whose output is exported.

    responseformat - The format in which the data is to be exported.

    config - Contains the control configurations.

    jobid - Returns the export job id.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) InitiateBulkExportUsingSQL(sqlquery, responseformat string, config map[string]interface{}) (jobid string, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/data"
        config["responseFormat"] = responseformat
        config["sqlQuery"] = sqlquery
        response, exception := bulk.ac.sendAPIRequest("GET", endpoint, config, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            jobid = response.(map[string]interface{})["data"].(map[string]interface{})["jobId"].(string)
        }
        return
    }

    /*
    GetExportJobInfo - Returns the details of the export job.

    jobid - Id of the export job.

    result - Returns the export job details as interface.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) GetExportJobDetails(jobid string) (result interface{}, serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/exportjobs/" + jobid

        response, exception := bulk.ac.sendAPIRequest("GET", endpoint, nil, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }else{
            result = response.(map[string]interface{})["data"].(map[string]interface{})
        }
        return
    }

    /*
    ExportBulkData - Download the exported data for the mentioned job id.

    jobid - Returns the export job id.

    filepath - Path of the file where the data exported to be stored.

    serverexception - Throws a server exception. If the server has received the request but did not process the request due to some error.
    */
    func (bulk *BulkAPI) ExportBulkData(jobid, filepath string) (serverexception *ServerException) {
        endpoint := bulk.bulkEndpoint + "/exportjobs/" + jobid + "/data"
        _, exception := bulk.ac.sendExportAPIRequest(filepath, endpoint, nil, bulk.requestHeaders)
        if(exception != nil){
            serverexception = exception
        }
        return
    }
/*
Internally used.
*/
func (ac *Client) sendBatchImportAPIRequest(filepath, endpoint string, batchSize int, config map[string]interface{}, requestHeaders map[string]string) (successResp interface{}, serverexception *ServerException) {
    requestUrl := ac.AnalyticsServerUrl + endpoint
    
    if ac.AccessToken == "" {
        serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
        if(serverexception != nil){
                return
        }
    }
    config["batchKey"] = "start"
    
    file, err := os.Open(filepath)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    // Create a buffered reader for the file
    reader := bufio.NewReader(file)

    // Read the first line of the file
    header, _, eof := reader.ReadLine()
    var line []byte
    //line := []byte("")
    //fmt.Print(string(line))
    for eof!=io.EOF{

        tempfile, errtempfile := ioutil.TempFile("", "tempfile")
        if errtempfile != nil {
            panic(errtempfile)
        }
        tempfilepath := tempfile.Name()
        tempfile.Write(header)
        tempfile.WriteString("\n")
        isLastBatch := "false"
        for i := 0; i < batchSize; i++ {
            
            defer os.Remove(tempfilepath) // remove the temporary file after we're done with it
            defer tempfile.Close()

            // Write the string to the temporary file
            line, _, eof = reader.ReadLine()
            if eof != nil {
                if eof == io.EOF {
                    isLastBatch = "true"
                    break
                }
                panic(eof)
            }
            _, err = tempfile.Write(line)
            if err != nil {
                panic(err)
            }
            tempfile.WriteString("\n")
        }
        config["isLastBatch"] = isLastBatch
        
        paramValues := url.Values{}
        if config != nil {
            jsonConfig, err := json.Marshal(config)
            if err != nil {
                panic(err)
            }
            paramValues.Add("CONFIG", string(jsonConfig))
        }
        parameters := paramValues.Encode()
        url := requestUrl + "?" + parameters

        
        respObj := ac.submitImportRequest(tempfilepath, url,  requestHeaders, ac.AccessToken)
        statusCode := respObj.StatusCode
        response := respObj.ResponseContent
        
        if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
            if ac.isOAuthExpired(response) {
                serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
                if(serverexception != nil){
                    return
                }
                respObj = ac.submitImportRequest(tempfilepath, url,  requestHeaders, ac.AccessToken)
                statusCode = respObj.StatusCode
                response = respObj.ResponseContent
                
            }
            if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
                serverexception = ac.raiseServerException(response, statusCode, false)
            }
        }
        if statusCode != 200 {
            return
        }
        time.Sleep(2 * time.Second)
        json.Unmarshal(response, &successResp)
        config["batchKey"] = successResp.(map[string]interface{})["data"].(map[string]interface{})["batchKey"].(string)
    }
    return
}

/*
Internally used.
*/
/*
Internally used.
*/
func (ac *Client) sendRawImportAPIRequest(data, endpoint string, config map[string]interface{}, requestHeaders map[string]string) (successResp interface{}, serverexception *ServerException) {
    requestUrl := ac.AnalyticsServerUrl + endpoint
    paramValues := url.Values{}
    if config != nil {
        jsonConfig, err := json.Marshal(config)
        if err != nil {
            panic(err)
        }
        paramValues.Add("CONFIG", string(jsonConfig))
    }
    parameters := paramValues.Encode()
    requestUrl = requestUrl + "?" + parameters

    if ac.AccessToken == "" {
        serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
        if(serverexception != nil){
                return
        }
    }

    respObj := ac.submitRawImportRequest(data, requestUrl,  requestHeaders, ac.AccessToken)
    statusCode := respObj.StatusCode
    response := respObj.ResponseContent

    if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
        if ac.isOAuthExpired(response) {
            serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
            if(serverexception != nil){
                return
            }
            respObj = ac.submitRawImportRequest(data, requestUrl,  requestHeaders, ac.AccessToken)
            statusCode = respObj.StatusCode
            response = respObj.ResponseContent

        }
        if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
            serverexception = ac.raiseServerException(response, statusCode, false)
        }
    }
    if statusCode != 200 {
        return
    }

    json.Unmarshal(response, &successResp)
    return
}

/*
Internally used.
*/
func (ac *Client) submitRawImportRequest(data, requestUrl string, requestHeaders map[string]string, AccessToken string) (respObj *responseObj) {

    bodyBuf := bytes.NewBufferString("")
    bodyWriter := multipart.NewWriter(bodyBuf)
    if err := bodyWriter.WriteField("DATA", data); err != nil {
        panic(err)
    }
    boundary := bodyWriter.Boundary()
    if err := bodyWriter.Close(); err != nil {
        panic(err)
    }

    request, err := http.NewRequest("POST", requestUrl, bytes.NewReader(bodyBuf.Bytes()))
    if err != nil {
        panic(err)
    }

    request.Header.Set("User-Agent" , "ZohoAnalytics Go Client v2_" + ac.ClientVersion)
    if AccessToken != "" {
        request.Header.Set("Authorization" , "Zoho-oauthtoken " + AccessToken)
    }
    for headerName, headerValue := range requestHeaders {
        request.Header.Set(headerName , headerValue)
    }
    request.Header.Add("Content-Type", "multipart/form-data; boundary="+boundary)
    request.ContentLength = int64(bodyBuf.Len())

    client := secureHTTPClient
    response, resperror := client.Do(request)
        if resperror != nil {
                panic(resperror)
        }

    respObj = &responseObj{}
    responseBody, _ := ioutil.ReadAll(response.Body)
    respObj.ResponseContent = responseBody
    respObj.StatusCode = response.StatusCode

    defer response.Body.Close()

    return
}

func (ac *Client) sendImportAPIRequest(filepath, endpoint string, config map[string]interface{}, requestHeaders map[string]string) (successResp interface{}, serverexception *ServerException) {
    requestUrl := ac.AnalyticsServerUrl + endpoint
    paramValues := url.Values{}
    if config != nil {
        jsonConfig, err := json.Marshal(config)
        if err != nil {
            panic(err)
        }
        paramValues.Add("CONFIG", string(jsonConfig))
    }
    parameters := paramValues.Encode()
    requestUrl = requestUrl + "?" + parameters

    if ac.AccessToken == "" {
        serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
        if(serverexception != nil){
                return
        }
    }

    respObj := ac.submitImportRequest(filepath, requestUrl,  requestHeaders, ac.AccessToken)
    statusCode := respObj.StatusCode
    response := respObj.ResponseContent
    
    if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
        if ac.isOAuthExpired(response) {
            serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
            if(serverexception != nil){
                return
            }
            respObj = ac.submitImportRequest(filepath, requestUrl,  requestHeaders, ac.AccessToken)
            statusCode = respObj.StatusCode
            response = respObj.ResponseContent
            
        }
        if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
            serverexception = ac.raiseServerException(response, statusCode, false)
        }
    }
    if statusCode != 200 {
        return
    }
    
    json.Unmarshal(response, &successResp)
    return
}

/*
Internally used.
*/
func (ac *Client) submitImportRequest(filepath, requestUrl string, requestHeaders map[string]string, AccessToken string) (respObj *responseObj) {


    bodyBuf := bytes.NewBufferString("")
    bodyWriter := multipart.NewWriter(bodyBuf)
    _, err := bodyWriter.CreateFormFile("FILE", filepath)
    if err != nil {
        panic(err)
    }
    file, err := os.Open(filepath)
    if err != nil {
        panic(err)
    } 
    boundary := bodyWriter.Boundary()
    closeBuf := bytes.NewBufferString(fmt.Sprintf("\r\n--%s--\r\n", boundary))
    requestReader := io.MultiReader(bodyBuf, file, closeBuf)
    filereq, err := file.Stat()
    if err != nil {
        panic(err)
    }

    request, err := http.NewRequest("POST", requestUrl, requestReader)  
    if err != nil {
        panic(err)
    }

    request.Header.Set("User-Agent" , "ZohoAnalytics Go Client v2_" + ac.ClientVersion)
    if AccessToken != "" {
        request.Header.Set("Authorization" , "Zoho-oauthtoken " + AccessToken)
    }
    for headerName, headerValue := range requestHeaders {
        request.Header.Set(headerName , headerValue)
    }
    request.Header.Add("Content-Type", "multipart/form-data; boundary="+boundary)
    request.ContentLength = filereq.Size() + int64(bodyBuf.Len()) + int64(closeBuf.Len())
    

    client := secureHTTPClient
    response, resperror := client.Do(request)
        if resperror != nil {
                panic(resperror)
        }

    respObj = &responseObj{}
    responseBody, _ := ioutil.ReadAll(response.Body)
    respObj.ResponseContent = responseBody 
    respObj.StatusCode = response.StatusCode

    defer response.Body.Close()

    //var jsonRespObj map[string]interface{}
    //json.Unmarshal(responseBody, &jsonRespObj)

    return
}

/*
Internally used.
*/
func (ac *Client) sendExportAPIRequest(filepath, endpoint string, config map[string]interface{}, requestHeaders map[string]string) (successResp interface{}, serverexception *ServerException) {
    requestUrl := ac.AnalyticsServerUrl + endpoint
    paramValues := url.Values{}
    requestMethod := "GET"
    if config != nil {
        jsonConfig, err := json.Marshal(config)
        if err != nil {
            panic(err)
        }
        paramValues.Add("CONFIG", string(jsonConfig))
    }
    parameters := paramValues.Encode()

    if ac.AccessToken == "" {
        serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
        if(serverexception != nil){
                return
        }
    }

    respObj := ac.submitRequest(requestMethod, requestUrl,  parameters, requestHeaders, ac.AccessToken)
    statusCode := respObj.StatusCode
    response := respObj.ResponseContent
    
    if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
        if ac.isOAuthExpired(response) {
            serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
            if(serverexception != nil){
                return
            }
            respObj = ac.submitRequest(requestMethod, requestUrl,  parameters, requestHeaders, ac.AccessToken)
            statusCode = respObj.StatusCode
            response = respObj.ResponseContent
            
        }
        if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
            serverexception = ac.raiseServerException(response, statusCode, false)
        }
    }
    if statusCode != 200 {
        return
    }
    
    file, err := os.Create(filepath)
    if err != nil {
        panic(err)
    }
    defer file.Close()
    _, err = file.WriteString(string(response))
    if err != nil {
        panic(err)
    }
    return
}

/*
sendAPIRequest - Internally used for send request.

Send request to the server and get response.
*/
func (ac *Client) sendAPIRequest(requestMethod, endpoint string, config map[string]interface{}, requestHeaders map[string]string) (successResp interface{}, serverexception *ServerException) {
    requestUrl := ac.AnalyticsServerUrl + endpoint
    paramValues := url.Values{}
    if config != nil {
        jsonConfig, err := json.Marshal(config)
        if err != nil {
            panic(err)
        }
        paramValues.Add("CONFIG", string(jsonConfig))
    }
    parameters := paramValues.Encode()

    if ac.AccessToken == "" {
        serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
        if(serverexception != nil){
                return
        }
    }

    respObj := ac.submitRequest(requestMethod, requestUrl,  parameters, requestHeaders, ac.AccessToken)
    statusCode := respObj.StatusCode
    response := respObj.ResponseContent
    
    if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
        if ac.isOAuthExpired(response) {
            serverexception = ac.regenerateAnalyticsOAuthToken(ac.ClientId, ac.ClientSecret, ac.RefreshToken)
            if(serverexception != nil){
                return
            }
            respObj = ac.submitRequest(requestMethod, requestUrl,  parameters, requestHeaders, ac.AccessToken)
            statusCode = respObj.StatusCode
            response = respObj.ResponseContent
            
        }
        if !strings.HasPrefix(strconv.Itoa(statusCode), "2") {
            serverexception = ac.raiseServerException(response, statusCode, false)
        }
    }
    if statusCode != 200 {
        return
    }
    json.Unmarshal(response, &successResp)
    return
}

/*
Internally used.
*/
func (ac *Client) submitRequest(requestMethod, requestUrl, parameters string, requestHeaders map[string]string, AccessToken string) (respObj *responseObj) {
    requestUrl = requestUrl + "?" + parameters
    request, requestError := http.NewRequest(requestMethod, requestUrl, nil)
    if requestError != nil {
        panic(requestError)
    }

    request.Header.Set("User-Agent" , "ZohoAnalytics Go Client v2_" + ac.ClientVersion)
    if AccessToken != "" {
        request.Header.Set("Authorization" , "Zoho-oauthtoken " + AccessToken)
    }
    for headerName, headerValue := range requestHeaders {
        request.Header.Set(headerName , headerValue)
    }

    client := secureHTTPClient
    response, responserverexceptionor := client.Do(request)
    if responserverexceptionor != nil {
        panic(responserverexceptionor)
    }
    defer response.Body.Close()
    

    respObj = &responseObj{}
    responseBody, _ := ioutil.ReadAll(response.Body)
    respObj.ResponseContent = responseBody //string(responseBody)
    respObj.StatusCode = response.StatusCode


    var jsonRespObj map[string]interface{}
    json.Unmarshal(responseBody, &jsonRespObj)

    return
}

/*
Internally used.
*/
func (ac *Client) isOAuthExpired(response []byte)(bool){
    var jsonRespObject map[string]interface{}
    json.Unmarshal(response, &jsonRespObject)
    if(jsonRespObject["data"] != nil) {
        errCode := jsonRespObject["data"].(map[string]interface{})["errorCode"].(float64)
        if errCode == 8535 {
            return true
        }
    }
    return false
}

/*
GetOAuthToken - Internal method for getting OAuth token.
*/
func (ac *Client) regenerateAnalyticsOAuthToken(ClientId, ClientSecret, RefreshToken string) (serverexception *ServerException) {
    urlparams := url.Values{}

    urlparams.Add("client_id", ClientId)
    urlparams.Add("client_secret", ClientSecret)
    urlparams.Add("refresh_token", RefreshToken)
    urlparams.Add("grant_type", "refresh_token")

    parameters := urlparams.Encode()
    requestUrl := ac.AccountsServerUrl + "/oauth/v2/token"

    var reqheader map[string]string
    respObj := ac.submitRequest("POST", requestUrl,  parameters, reqheader, "")
    statusCode := respObj.StatusCode
    response := respObj.ResponseContent

    var jsonResp map[string]interface{}
    json.Unmarshal(response, &jsonResp)
    if(statusCode == 200 && jsonResp["access_token"] != nil){
        ac.AccessToken = jsonResp["access_token"].(string)
        return
    }

    serverexception = ac.raiseServerException(response, statusCode, true)
    return
}

/*
Internally used.
*/
type responseObj struct{

    ResponseContent []byte
    StatusCode int
}

/*
Internally used.
*/
func (ac *Client) raiseServerException(response []byte, statusCode int, isiamerror bool) (serverexception *ServerException) {
    var jsonErrObject map[string]interface{}
    json.Unmarshal(response, &jsonErrObject)
    excep := &ServerException{}
    serverexception = excep
    serverexception.HttpStatusCode = statusCode
    if(isiamerror){

        serverexception.ErrorCode = 0
        serverexception.ErrorMessage = jsonErrObject["error"].(string)
    }else if(jsonErrObject["data"] != nil){
        serverexception.ErrorCode = jsonErrObject["data"].(map[string]interface{})["errorCode"].(float64)
        serverexception.ErrorMessage = jsonErrObject["data"].(map[string]interface{})["errorMessage"].(string)
    }else{
        panic(string(response))
    }
    return
}


/*
ServerException - ServerException is thrown if the Analytics server has received the request but did not process the request due to some error.

ErrorCode - The error code sent by the server.

ErrorMessage - The error message sent by the server.

HttpStatusCode - The HTTP status code for the request.

Action - The action to be performed over the resource specified by the URI.
*/
type ServerException struct{

    ErrorCode float64
    ErrorMessage string
    HttpStatusCode int
    Action string
}
