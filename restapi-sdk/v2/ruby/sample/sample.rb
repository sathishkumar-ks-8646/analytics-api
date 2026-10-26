#$Id$
require 'json'
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  VIEWID = "35730000007354002"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new
           .with_data_center("US")
           .with_oauth({
             "clientId" => "1000.xxxxxxx",
             "clientSecret" => "xxxxxxx",
             "refreshToken" => "1000.xxxxxxx.xxxxxxx"
           })
           #.with_token_store_path("/home/admin/analytics_ruby_sdk/tokens") # Optional – specify a directory path to securely store the encrypted access token
           .build
  end

  def get_orgs
    result = @ac.get_orgs
    puts result
  end

  def get_workspaces
    result = @ac.get_workspaces
    puts result
  end

  def get_views
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = { 'viewTypes' => ['0'] }
    result = workspace.get_views(config)
    puts result
  end

  def add_row
    column_values = {
      "Region" => "East",
      "Product Category" => "Sample",
      "Product" => "Test"
    }

    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.add_row(column_values)
    puts result
  end

  def update_row
    column_values = {
      "Region" => "West",
      "Product Category" => "Fruits",
      "Product" => "Apple"
    }

    criteria = '"Sales"."Region"=\'East\''
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.update_row(column_values, criteria)
    puts result
  end

  def delete_row
    criteria = '"Sales"."Region"=\'East\''
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.delete_row(criteria)
    puts result
  end

  def export_data
    response_format = 'csv'
    file_path = '/home/admin/ruby/SalesData.csv'
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)

    config = {
      "criteria" => "\"Sales\".\"Region\"='East'"
    }

    bulk.export_data(Config::VIEWID, response_format, file_path, config)
    puts "success"
  end
 
  def import_data
    import_type = "append"
    file_type = "csv"
    auto_identify = "true"
    file_path = "/home/admin/ruby/SalesData.csv"
    
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    result = bulk.import_data(Config::VIEWID, import_type, file_type, auto_identify, file_path)
    
    puts result
  end

  def get_tags
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_tags
    puts result
  end

  def create_tag
    tag_name = "Sales Tag"
    color_code = "#FF5733"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_tag(tag_name, color_code)
    puts result
  end

  def update_tag
    tag_id = ""
    config = { "name" => "Sales Tag Updated", "colorCode" => "#33FF57" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_tag(tag_id, config)
    puts "success"
  end

  def delete_tag
    tag_id = ""
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_tag(tag_id)
    puts "success"
  end

  def add_tag_to_views
    tag_id = ""
    view_ids = [Config::VIEWID]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.add_tag_to_views(tag_id, view_ids)
    puts "success"
  end

  def remove_tag_from_views
    tag_id = ""
    view_ids = [Config::VIEWID]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.remove_tag_from_views(tag_id, view_ids, false)
    puts "success"
  end

  def get_tagged_views
    tag_id = ""
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_tagged_views(tag_id)
    puts result
  end

  def get_view_tags
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.get_view_tags
    puts result
  end

  def add_tags_to_view
    tag_ids = [""]
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.add_tags_to_view(tag_ids)
    puts "success"
  end

  def remove_tags_from_view
    tag_ids = [""]
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.remove_tags_from_view(tag_ids, false)
    puts "success"
  end

  def get_custom_roles
    org = @ac.get_org_instance(Config::ORGID)
    result = org.get_custom_roles
    puts result
  end

  def create_custom_role
    role_name = "DashboardPowerUser"
    # Allowed values for access_type: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
    access_type = "ALL_DASHBOARDS"
    permissions = {
      "interactionPermissions" => {
        "read" => true,
        "vud" => true,
        "drillDown" => true,
        "insight" => true
      },
      "sharePermissions" => {
        "discussion" => true,
        "privateLinks" => true
      },
      "publishPermissions" => {
        "export" => true
      }
    }
    org = @ac.get_org_instance(Config::ORGID)
    result = org.create_custom_role(role_name, access_type, permissions)
    puts result
  end

  def update_custom_role
    role_id = ""
    role_name = "DashboardPowerUser"
    # Allowed values for access_type: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
    access_type = "ALL_DASHBOARDS"
    permissions = {
      "interactionPermissions" => {
        "read" => true,
        "vud" => true,
        "drillDown" => false,
        "insight" => false
      },
      "sharePermissions" => {
        "share" => true,
        "privateLinks" => false
      },
      "publishPermissions" => {
        "export" => true
      }
    }
    org = @ac.get_org_instance(Config::ORGID)
    org.update_custom_role(role_id, role_name, access_type, permissions)
    puts "success"
  end

  def delete_custom_role
    role_id = ""
    org = @ac.get_org_instance(Config::ORGID)
    org.delete_custom_role(role_id)
    puts "success"
  end
  def refetch_data
    config = {
      "userName" => "john@zylker.com",
      "password" => "Zoho@123"
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.refetch_data(config)
    puts "success"
  end

  def get_alerts_in_view
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.get_alerts_in_view
    puts result
  end

  def get_view_metadata_for_alert
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.get_view_metadata_for_alert
    puts result
  end

  def create_alert
    alert_name = "Sales Drop Alert"

    schedule_details = {
      "calendarFrequency" => "daily",
      "hour" => 9,
      "minute" => 0
    }

    rules = [
      {
        "operator" => "lt",
        "viewColumnIndex" => "2",
        "type" => "constant",
        "values" => ["1000"]
      }
    ]

    config = {
      "email" => {
        "notifyAdmins" => true,
        "subject" => "Sales dropped below threshold",
        "message" => "Please review the report."
      }
    }

    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.create_alert(alert_name, schedule_details, rules, config)
    puts result
  end

  def get_alerts_in_workspace
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_alerts_in_workspace
    puts result
  end

  def get_alert_configuration
    alert_id = "35130000001056611"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_alert_configuration(alert_id)
    puts result
  end

  def update_alert
    alert_id = "35130000001056611"
    alert_name = "Sales Drop Alert (weekly)"

    schedule_details = {
      "calendarFrequency" => "weekly",
      "hour" => 9,
      "minute" => 30,
      "weekDays" => [6],
      "timeZone" => "Asia/Kolkata"
    }

    rules = [
      {
        "operator" => "lt",
        "viewColumnIndex" => "2",
        "type" => "constant",
        "values" => ["1000"]
      }
    ]

    config = {
      "email" => {
        "notifyAdmins" => true,
        "emailIds" => ["finance@example.com"],
        "subject" => "Weekly sales monitor",
        "message" => "Weekly alert summary."
      }
    }

    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_alert(alert_id, alert_name, schedule_details, rules, config)
    puts "success"
  end

  def delete_alerts
    alert_ids = ["137687000010815003", "137687000010815005"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_alerts(alert_ids)
    puts "success"
  end

  def change_alert_status
    alert_ids = ["137687000010815003", "137687000010815005"]
    enabled = false
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.change_alert_status(alert_ids, enabled)
    puts "success"
  end

  def run_alert
    alert_id = "35130000001056611"
    config = { "validateSystemTags" => false }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.run_alert(alert_id, config)
    puts "success"
  end

  def get_alert_events
    alert_id = "35130000001056611"

    config = {
      "fromDate" => "2026-05-01 00:00:00",
      "toDate" => "2026-05-31 23:59:59",
      "status" => ["triggered", "error"],
      "pageNo" => 1,
      "recordsPerPage" => 50
    }

    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_alert_events(alert_id, config)
    puts result
  end

  def get_linked_workspaces
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_linked_workspaces
    puts result
  end

  def get_linked_workspaces_for_org
    org = @ac.get_org_instance(Config::ORGID)
    result = org.get_linked_workspaces
    puts result
  end

  def get_linkable_workspaces
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_linkable_workspaces
    puts result
  end

  def get_workspace_linking_compatibility
    clients = [
      {
        "orgId" => "700000654321",
        "workspaceIds" => ["466206000000071000"]
      }
    ]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_linking_compatibility(clients)
    puts result
  end

  def link_workspaces
    clients = [
      {
        "orgId" => "700000654321",
        "workspaceIds" => ["466206000000071000"]
      }
    ]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.link_workspaces(clients)
    puts "success"
  end

  def unlink_workspaces
    scope = "ALL"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.unlink_workspaces(scope)
    puts "success"
  end

  def sync_linked_workspaces
    scope = "ALL"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.sync_linked_workspaces(scope)
    puts "success"
  end

  def get_linked_workspace_sync_details
    sandbox_ids = ["137687000012345001", "137687000012345002"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_linked_workspace_sync_details(sandbox_ids)
    puts result
  end

  def get_workspace_backups
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_backups
    puts result
  end

  def backup_workspace_now
    config = { "backupMode" => "STRUCTURE" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.backup_workspace_now(config)
    puts result
  end

  def get_workspace_backup_status
    backup_id = "35130000001056701"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_backup_status(backup_id)
    puts result
  end

  def download_workspace_backup
    backup_id = "35130000001056701"
    file_path = "/home/admin/ruby/workspace-backup.zip"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.download_workspace_backup(backup_id, file_path)
    puts "success"
  end

  def restore_workspace_from_backup
    backup_id = "35130000001056701"
    confirm_restore = true
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.restore_workspace_from_backup(backup_id, confirm_restore)
    puts result
  end

  def get_workspace_restore_status
    restore_id = "35130000001056801"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_restore_status(restore_id)
    puts result
  end

  def create_dashboard
    display_name = "Sales Overview"

    layout = {
      "1" => { "type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0 },
      "2" => { "type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Sales Dashboard</b>" },
      "3" => { "type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => {} }
    }.to_json

    config = {
      "settings" => {
        "allowDrillDown" => "true",
        "fitToWidth" => "true"
      }
    }

    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_dashboard(display_name, layout, config)
    puts result
  end

  def update_dashboard
    dashboard_id = "35130000001055801"

    layout = {
      "1" => { "type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0 },
      "2" => { "type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Updated Title</b>" },
      "3" => { "type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => {} }
    }.to_json

    config = { "layout" => layout }

    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_dashboard(dashboard_id, config)
    puts "success"
  end

  def get_dashboard_metadata
    dashboard_id = "35130000001055801"
    config = { "include" => "layout" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_dashboard_metadata(dashboard_id, config)
    puts result
  end

  def get_report_metadata
    report_id = "35130000001055901"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_report_metadata(report_id)
    puts result
  end

  def get_org_access_restrictions
    org = @ac.get_org_instance(Config::ORGID)
    result = org.get_org_access_restrictions
    puts result
  end

  def update_org_access_restrictions
    config = { "accessRestrictionEnabled" => true }
    org = @ac.get_org_instance(Config::ORGID)
    org.update_org_access_restrictions(config)
    puts "success"
  end

  def get_workspace_access_restrictions
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_access_restrictions
    puts result
  end

  def update_workspace_access_restrictions
    config = {
      "useOrganizationSettings" => false,
      "shareViews" => {
        "domainRestrictionEnabled" => true,
        "trustedDomains" => ["example.com", "partner.example.org"]
      },
      "privateLinks" => { "enabled" => false },
      "publicViews" => { "enabled" => false },
      "exportViews" => { "enabled" => true }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_workspace_access_restrictions(config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.add_row
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
