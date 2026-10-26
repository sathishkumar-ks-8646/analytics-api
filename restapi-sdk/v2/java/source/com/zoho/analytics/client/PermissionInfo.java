// $Id$
package com.zoho.analytics.client;

import java.util.HashMap;

/**
 * PermissionInfo contains the complete information of each permission entry.
 */
public class PermissionInfo {
    private String viewName;
    private long viewId;
    private String sharedBy;
    private String filterCriteria = null;

    protected PermissionInfo(String viewName, long viewId, String sharedBy) {
        this.viewName = viewName;
        this.viewId = viewId;
        this.sharedBy = sharedBy;
    }

    private HashMap<String,Boolean> permsMap = new HashMap<>();

    void setPermission(String permName, boolean permValue) {
        permsMap.put(permName, permValue);
    }

    void setFilterCriteria(String filterCriteria) {
        this.filterCriteria = filterCriteria;
    }

    /**
     * This method is used to get the name of the View that is shared.
     * @return A <code>String</code> value holds the name of the view.
     */
    public String getViewName() {
        return viewName;
    }

    /**
     * This method is used to get the id of the View that is shared.
     * @return A <code>Long</code> value holds the id of the view.
     */
    public long getViewId() {
        return viewId;
    }

    /**
     * This method is used to get the email address of the user who shared the View.
     * @return A <code>String</code> value holds the email address of the user who shared the view.
     */
    public String getSharedBy() {
        return sharedBy;
    }

    /**
     * This method is used to get the filter criteria associated to this PermissionInfo.
     * @return A <code>String</code> value holds the filter criteria.
     */
    public String getFilterCriteria() {
        return filterCriteria;
    }

    /**
     * This method is used to find whether this permission entry has READ permission.
     * @return A <code>Boolean</code> value holds whether the READ operation is allowed or not.
     */
    public Boolean hasReadPermission() {
        return permsMap.get("read");
    }

    /**
     * This method is used to find whether this permission entry has EXPORT permission.
     * @return A <code>Boolean</code> value holds whether EXPORT operation is allowed or not.
     */
    public Boolean hasExportPermission() {
        return permsMap.get("export");
    }

    /**
     * This method is used to find whether this permission entry has View Underlying Data permission.
     * @return A <code>Boolean</code> value holds whether View Underlying Data operation is allowed or not.
     */
    public Boolean hasVUDPermission() {
        return permsMap.get("vud");
    }

    /**
     * This method is used to find whether this permission entry has ADDROW permission.
     * @return A <code>Boolean</code> value holds whether the ADDROW operation is allowed or not.
     */
    public Boolean hasAddRowPermission() {
        return permsMap.get("addRow");
    }

    /**
     * This method is used to find whether this permission entry has UPDATEROW permission.
     * @return A <code>Boolean</code> value holds whether the UPDATEROW operation is allowed or not.
     */
    public Boolean hasUpdateRowPermission() {
        return permsMap.get("updateRow");
    }

    /**
     * This method is used to find whether this permission entry has DELETEROW permission.
     * @return A <code>Boolean</code> value holds whether the DELETEROW operation is allowed or not.
     */
    public Boolean hasDeleteRowPermission() {
        return permsMap.get("deleteRow");
    }

    /**
     * This method is used to find whether this permission entry has DELETEALLROWS permission.
     * @return A <code>Boolean</code> value holds whether the DELETE ALL ROWS operation is allowed or not.
     */
    public Boolean hasDeleteAllRowsPermission() {
        return permsMap.get("deleteAllRows");
    }

    /**
     * This method is used to find whether this permission entry has APPEND IMPORT permission.
     * @return A <code>Boolean</code> value holds whether the APPEND IMPORT operation is allowed or not.
     */
    public Boolean hasAppendImportPermission() {
        return permsMap.get("importAppend");
    }

    /**
     * This method is used to find whether this permission entry has UPDATE IMPORT permission.
     * @return A <code>Boolean</code> value holds whether the UPDATE IMPORT operation is allowed or not.
     */
    public Boolean hasUpdateImportPermission() {
        return permsMap.get("importAddOrUpdate");
    }

    /**
     * This method is used to find whether this permission entry has TRUNCATE IMPORT permission.
     * @return A <code>Boolean</code> value holds whether the TRUNCATE IMPORT operation is allowed or not.
     */
    public Boolean hasTruncateImportPermission() {
        return permsMap.get("importDeleteAllAdd");
    }

    /**
     * This method is used to find whether this permission entry has DELETE UPDATEADD IMPORT permission.
     * @return A <code>Boolean</code> value holds whether the DELETE UPDATEADD IMPORT operation is allowed or not.
     */
    public Boolean hasDeleteUpdateAddImportPermission() {
        return permsMap.get("importDeleteUpdateAdd");
    }

    /**
     * This method is used to find whether this permission entry has DRILLDOWN permission.
     * @return A <code>Boolean</code> value holds whether the DRILLDOWN permission operation is allowed or not.
     */
    public Boolean hasDrillDownPermission() {
        return permsMap.get("drillDown");
    }

    /**
     * This method is used to find whether this permission entry has SHARE permission.
     * @return A <code>Boolean</code> value holds whether the SHARE permission operation is allowed or not.
     */
    public Boolean hasSharePermission() {
        return permsMap.get("share");
    }

    /**
     * This method is used to find whether this permission entry has DISCUSSION permission.
     * @return A <code>Boolean</code> value holds whether the DISCUSSION permission operation is allowed or not.
     */
    public Boolean hasDiscussionPermission() {
        return permsMap.get("discussion");
    }
}