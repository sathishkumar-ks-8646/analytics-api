// $Id$
package com.zoho.analytics.client;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

/**
 *  ShareInfo contains the result of getWorkspaceShareInfo operation.
 */
public class ShareInfo {
    private HashMap<String, ArrayList<PermissionInfo>> sharedUserPermInfoMap = new HashMap<>();
    private HashMap<String, ArrayList<PermissionInfo>> groupPermInfoMap = new HashMap<>();
    private ArrayList<PermissionInfo> privateLinkPermInfo = new ArrayList<>();
    private ArrayList<PermissionInfo> publicPermInfo = new ArrayList<>();

    protected ShareInfo(JSONObject shareInfo) throws ParseException {
        try {
            JSONArray userShareInfo = shareInfo.getJSONArray("userShareInfo");
            if(userShareInfo.length() > 0) {
                sharedUserPermInfoMap = getUserPermissionsInfoMap(userShareInfo);
            }

            JSONArray groupShareInfo = shareInfo.getJSONArray("groupShareInfo");
            if(groupShareInfo.length() > 0) {
                groupPermInfoMap = getGroupPermissionsInfoMap(groupShareInfo);
            }

            JSONObject publicShareInfo = shareInfo.getJSONObject("publicShareInfo");
            if(publicShareInfo.has("views")) {
                JSONArray publicShareInfoViewsArr = publicShareInfo.getJSONArray("views");
                publicPermInfo = getPermissionInfoList(publicShareInfoViewsArr);
            }

            JSONObject privateLinkShareInfo = shareInfo.getJSONObject("privateLinkShareInfo");
            if(privateLinkShareInfo.has("views")) {
                JSONArray privateLinkShareInfoViewsArr = privateLinkShareInfo.getJSONArray("views");
                privateLinkPermInfo = getPermissionInfoList(privateLinkShareInfoViewsArr);
            }
        }
        catch (Exception ex) {
            throw new ParseException(shareInfo.toString(), "Exception while parsing the share info.", ex);
        }
    }

    /**
     * This method is used to get the Shared Users of the specified workspace.
     * @return Shared Users of the workspace as <code>Set</code>.
     */
    public Set<String> getSharedUsers() {
        return sharedUserPermInfoMap.keySet();
    }

    /**
     * This method is used to get the Permissions of the Shared Users.
     * @return The <code>HashMap</code><<code>String</code>,<code>ArrayList</code><<code>PermissionInfo</code>>>.
     * This HashMap contains Shared User Vs. <code>ArrayList</code> of <code>PermissionInfo</code>.
     */
    public HashMap<String,ArrayList<PermissionInfo>> getSharedUserPermissions() {
        return sharedUserPermInfoMap;
    }

    /**
     * This method is used to get the Group names of the specified workspace.
     * @return Group names of the workspace as <code>Set</code>.
     */
    public Set<String> getGroupNames() {
        return groupPermInfoMap.keySet();
    }

    /**
     * This method is used to get the Permissions of the Groups.
     * @return The <code>HashMap</code><<code>String</code>,<code>ArrayList</code><<code>PermissionInfo</code>>>. It contains the PermissionInfo list for the workspace Group.
     */
    public HashMap<String, ArrayList<PermissionInfo>> getGroupPermissions() {
        return groupPermInfoMap;
    }

    /**
     * This method is used to get the Permissions of the Private Link.
     * @return The <code>ArrayList</code><<code>PermissionInfo</code>>. It contains the PermissionInfo list for the Private Link.
     */
    public ArrayList<PermissionInfo> getPrivateLinkPermissions() {
        return privateLinkPermInfo;
    }

    /**
     * This method is used to get the Permissions of the Public Visitors.
     * @return The <code>ArrayList</code><<code>PermissionInfo</code>>. It contains the PermissionInfo list for the Public Visitors.
     */
    public ArrayList<PermissionInfo> getPublicPermissions() {
        return publicPermInfo;
    }

    private static HashMap<String,ArrayList<PermissionInfo>> getUserPermissionsInfoMap(JSONArray shareInfoArr) throws Exception {
        HashMap<String,ArrayList<PermissionInfo>> permInfo = new HashMap<>();
        int arrLength = shareInfoArr.length();
        if(arrLength > 0) {
            for(int i=0; i < arrLength; i++) {
                JSONObject permInfoObj = shareInfoArr.getJSONObject(i);
                String emailId = permInfoObj.getString("emailId");
                JSONArray views = permInfoObj.getJSONArray("views");
                ArrayList<PermissionInfo> permInfoList = getPermissionInfoList(views);
                permInfo.put(emailId, permInfoList);
            }
        }
        return permInfo;
    }

    private static HashMap<String,ArrayList<PermissionInfo>> getGroupPermissionsInfoMap(JSONArray shareInfoArr) throws Exception {
        HashMap<String,ArrayList<PermissionInfo>> permInfo = new HashMap<>();
        int arrLength = shareInfoArr.length();
        if(arrLength > 0) {
            for(int i=0; i < arrLength; i++) {
                JSONObject permInfoObj = shareInfoArr.getJSONObject(i);
                String groupName = permInfoObj.getString("groupName");
                JSONArray views = permInfoObj.getJSONArray("views");
                ArrayList<PermissionInfo> permInfoList = getPermissionInfoList(views);
                permInfo.put(groupName, permInfoList);
            }
        }
        return permInfo;
    }

    private static ArrayList<PermissionInfo> getPermissionInfoList(JSONArray viewsArr) throws Exception {
        ArrayList<PermissionInfo> permissionInfoList = new ArrayList<>();
        int viewsLength = viewsArr.length();
        for(int i=0; i<viewsLength; i++) {
            JSONObject viewPerm = viewsArr.getJSONObject(i);
            long viewId = viewPerm.getLong("viewId");
            String viewName = viewPerm.getString("viewName");
            String sharedBy = viewPerm.getString("sharedBy");

            PermissionInfo permInfo = new PermissionInfo(viewName, viewId, sharedBy);

            JSONObject permissions = viewPerm.getJSONObject("permissions");
            Iterator<String> ie = permissions.keys();
            while (ie.hasNext()){
                String permName = ie.next();
                permInfo.setPermission(permName, permissions.getBoolean(permName));
            }

            if(viewPerm.has("filterCriteria")){
                JSONObject criteriaObj =  viewPerm.getJSONObject("filterCriteria");
                permInfo.setFilterCriteria(criteriaObj.getString("criteria"));
            }
            permissionInfoList.add(permInfo);
        }
        return permissionInfoList;
    }
}