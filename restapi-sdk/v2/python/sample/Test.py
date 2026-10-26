#$Id$
from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json
import urllib
import requests


class Config:
    
    CLIENTID = "";
    CLIENTSECRET = "";
    REFRESHTOKEN = "";
    
    ORGID = ""
    WORKSPACEID = ""
    VIEWID = ""
    DBKEY = ""

    PROXY_HOST = ""
    PROXY_PORT = ""
    PROXY_USER = ""
    PROXY_PASSWORD = ""

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def add_row(self, ac):
        column_values = {}
        column_values["Region"] = "East"
        column_values["Product Category"] = "Sample"
        column_values["Product"] = "Test"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.add_row(column_values)
        print(result)

    def update_row(self, ac):
        column_values = {}
        column_values["Region"] = "Updated East"
        column_values["Product Category"] = "Updated Sample"
        column_values["Product"] = "Updated Test"
        criteria = "\"Region\"='East1'"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.update_row(column_values, criteria)
        print(result)

    def delete_row(self, ac):
        criteria = "\"Region\"='East1'"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.delete_row(criteria)
        print(result)

    def import_data_in_new_table(self, ac):
        table_name = "Sales 404"
        file_type = "csv"
        auto_identify = "true"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_data_in_new_table(table_name, file_type, auto_identify, file_path)
        print(result)

    def import_raw_data_in_new_table(self, ac):
        table_name = "NewSales 42"
        file_type = "json"
        auto_identify = "true"
        raw_data = [{"Date":"06 February, 2017","Region":"West","Product Category":"Grocery","Product":"Fruits and Vegetables","Customer Name":"Vincent Herbert","Sales":"$1,682.39","Cost":"$200.05"},{"Date":"08 February, 2017","Region":"East","Product Category":"Furniture","Product":"Clocks","Customer Name":"John Britto","Sales":"$272.34","Cost":"$14.58"}]
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_raw_data_in_new_table(table_name, file_type, auto_identify, raw_data)    
        print(result)

    def import_data(self, ac):
        import_type = "truncateadd"
        file_type = "csv"
        auto_identify = "true"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_data(Config.VIEWID, import_type, file_type, auto_identify, file_path)        
        print(result)

    def import_raw_data(self, ac):
        import_type = "append"
        file_type = "json"
        auto_identify = "true"
        raw_data = [{"Date":"06 February, 2017","Region":"West","Product Category":"Grocery","Product":"Fruits and Vegetables","Customer Name":"Vincent Herbert","Sales":"$1,682.39","Cost":"$200.05"},{"Date":"08 February, 2017","Region":"East","Product Category":"Furniture","Product":"Clocks","Customer Name":"John Britto","Sales":"$272.34","Cost":"$14.58"}]
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_raw_data(Config.VIEWID, import_type, file_type, auto_identify, raw_data)
        print(result)
    
    def import_bulk_data_in_new_table(self, ac):
        table_name = "Bulk Table"
        file_type = "csv"
        auto_identify = "true"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_bulk_data_in_new_table(table_name, file_type, auto_identify, file_path)
        print(result)

    def import_bulk_data(self, ac):
        import_type = "truncateadd"
        file_type = "csv"
        auto_identify = "true"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_bulk_data(Config.VIEWID, import_type, file_type, auto_identify, file_path)        
        print(result)
        
    def import_data_in_new_table_as_batches(self, ac):
        table_name = "Sales"
        auto_identify = "false"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        batch_size = 400;
        config = {}
        config["delimiter"] = 2
        config["commentChar"] = "("
        config["quoted"] = 2
        result = bulk.import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config)
        print(result)

    def import_data_as_batches(self, ac):
        import_type = "append"
        auto_identify = "true"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        batch_size = 400;
        config = {}
        result = bulk.import_data_as_batches(Config.VIEWID, import_type, auto_identify, file_path, batch_size, config)
        print(result)

    def get_import_job_details(self, ac):
        job_id = "35130000001336083"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.get_import_job_details(job_id)    
        print(result)

    def export_data(self, ac):
        response_format = "csv"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        bulk.export_data(Config.VIEWID, response_format, file_path)


    def initiate_bulk_export(self, ac):
        response_format = "HTML"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.initiate_bulk_export(Config.VIEWID, response_format) 
        print(result)

    def initiate_bulk_export_using_sql(self, ac):
        response_format = "CSV"
        sql_query = "select * from Sales where Region='East'"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.initiate_bulk_query_export(sql_query, response_format)     
        print(result)

    def get_export_job_details(self, ac):
        job_id = "35130000001334001"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.get_export_job_details(job_id)       
        print(result)

    def export_bulk_data(self, ac):
        job_id = "35130000001334001"
        file_path = "/home/local/admin/Files/Sales.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        bulk.export_bulk_data(job_id, file_path)           

    def create_workspace(self, ac):
        workspace_name = "Python Lib"
        org = ac.get_org_instance(Config.ORGID)
        result = org.create_workspace(workspace_name)
        print(result)

    def copy_workspace(self, ac):
        new_workspace_name = "Copied Python Lib"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.copy(new_workspace_name)
        print(result)

    def rename_workspace(self, ac):
        new_workspace_name = "Renamed Python Lib"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.rename(new_workspace_name)
        print("success")

    def delete_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete()
        print("success")

    def create_query_table(self, ac):
        
        sql_query = ""
        query_table_name = ""

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_query_table(sql_query, query_table_name)
        print(result)

    def edit_query_table(self, ac):
        
        view_id = ""
        sql_query = ""
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.edit_query_table(view_id, sql_query)
        print("success")

    def create_table(self, ac):
        columns_arr = []
        
        column1 = {}
        column1["COLUMNNAME"] = "Col1"
        column1["DATATYPE"] = "PLAIN"
        column2 = {}
        column2["COLUMNNAME"] = "Col2"
        column2["DATATYPE"] = "NUMBER"
        columns_arr.append(column1)
        columns_arr.append(column2)
        table_design = {}
        table_design["TABLENAME"] = "Created Table"
        table_design["COLUMNS"] = columns_arr
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_table(table_design)
        print(result)

    def save_as_view(self, ac):
        new_view_name = "Saveas Python Lib view 2"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.save_as(new_view_name)
        print(result)

    def rename_view(self, ac):
        view_id = "1148746000002553005"
        new_view_name = "Renamed Python Lib view"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.rename(new_view_name)
        print("success")

    def delete_view(self, ac):
        view_id = "1148746000002553005"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.delete()
        print("success")

    def create_folder(self, ac):
        folder_name = "New Folder 1"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_folder(folder_name)
        print(result)

    def rename_folder(self, ac):
        folder_id = "1148746000002683001"
        folder_name = "Renamed Folder 1"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.rename_folder(folder_id, folder_name)
        print("success")

    def delete_folder(self, ac):
        folder_id = "1148746000002581001"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_folder(folder_id)
        print("success")

    def change_folder_hierarchy(self, ac):
        folder_id = "1148746000002683001"
        hierarchy = "1"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_folder_hierarchy(folder_id, hierarchy)
        print("success")

    def change_folder_position(self, ac):
        folder_id = "1148746000002683001"
        reference_folder_id = "1148746000002683005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_folder_position(folder_id, reference_folder_id)
        print("success")

    def move_views_to_folder(self, ac):
        folder_id = "1148746000002683001"
        view_ids = []
        view_ids.append("114874000002697007")
        view_ids.append("114874000002697005")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.move_views_to_folder(folder_id, view_ids)
        print("success")

    def export_as_template(self, ac):
        file_path = "/home/local/admin/Files/Sales.atpt"
        view_ids = []
        view_ids.append("1148746000002457001")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.export_as_template(view_ids, file_path)
        print("success")

    def get_workspace_users(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_users()
        print(result)

    def add_workspace_users(self, ac):
        email_ids = []
        email_ids.append("")
        email_ids.append("")
        role = "WORKSPACEADMIN"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_workspace_users(email_ids, role)
        print("success")

    def remove_workspace_users(self, ac):
        email_ids = []
        email_ids.append("")
        email_ids.append("")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_workspace_users(email_ids)
        print("success")

    def change_workspace_user_status(self, ac):
        email_ids = []
        email_ids.append("")
        email_ids.append("")
        operation = "activate"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_workspace_user_status(email_ids, operation)
        print("success")

    def change_workspace_user_role(self, ac):
        email_ids = []
        email_ids.append("")
        email_ids.append("")
        role = "WORKSPACEADMIN"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_workspace_user_role(email_ids, role)
        print("success")

    def get_formula_columns(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_formula_columns()
        print(result)

    def add_formula_column(self, ac):
        formula_name = "Formula_1"
        expression = "square(\"Cost\")"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.add_formula_column(formula_name, expression)
        print(result)

    def edit_formula_column(self, ac):
        formula_id = "1767024000009066006"
        expression = "square(\"Cost\")"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.edit_formula_column(formula_id, expression)
        print("success")

    def delete_formula_column(self, ac):
        formula_id = "35130000001055095"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.delete_formula_column(formula_id)
        print("success")

    def get_aggregate_formulas(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_aggregate_formulas()
        print(result)

    def add_aggregate_formula(self, ac):
        formula_name = "Formula_1"
        expression = "sum(\"Cost\")"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.add_aggregate_formula(formula_name, expression)
        print(result)

    def edit_aggregate_formula(self, ac):
        formula_id = "35130000001055095"
        expression = "sum(\"Cost\")"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.edit_aggregate_formula(formula_id, expression)
        print("success")

    def delete_aggregate_formula(self, ac):
        formula_id = "35130000001055095"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.delete_aggregate_formula(formula_id,)
        print("success")

    def get_email_schedules(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_email_schedules()
        print(result)

    def create_email_schedule(self, ac):
        schedule_name = "Schedule1"
        format = "CSV"

        view_ids = ["1148746000002578004", "1148746000002578002"]

        email_ids = ["user_1@zoho.com"]

        schedule_details = {
            "calendarFrequency": "Daily",
            "hour": 10,
            "minute": 30
        }

        config = {
            "subject": "Daily Sales Report"
        }

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        schedule_id = workspace.create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config)
        print(schedule_id)

    def update_email_schedule(self, ac):
        schedule_id = "115674600000150007"

        schedule_details = {
            "calendarFrequency": "Daily",
            "hour": 8,
            "minute": 30
        }

        config = {
            "subject": "Daily Sales Overview",
            "scheduleDetails": schedule_details
        }

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        new_schedule_id = workspace.update_email_schedule(schedule_id, config)
        print(new_schedule_id)

    def trigger_email_schedule(self, ac):
        schedule_id = "115674600000150007"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.trigger_email_schedule(schedule_id)
        print("success")

    def change_email_schedule_status(self, ac):
        schedule_id = "115674600000150007"
        operation = "activate"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_email_schedule_status(schedule_id, operation)
        print("success")

    def delete_email_schedule(self, ac):
        schedule_id = "115674600000150007"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_email_schedule(schedule_id)
        print("success")


    def get_view_dependents(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_view_dependents()
        print(result)

    def get_column_dependents(self, ac):
        column_id = "35130000001055095"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_column_dependents(column_id)
        print(result)

    def add_column(self, ac):
        column_name = "Col 1"
        data_type = "PLAIN"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.add_column(column_name, data_type)
        print(result)

    def rename_column(self, ac):
        column_id = "35130000001055095"
        column_name = "Renamed Col"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.rename_column(column_id, column_name)
        print("success")

    def delete_column(self, ac):
        column_id = "1148746000002578003"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.delete_column(column_id)
        print("success")

    def add_lookup(self, ac):
        column_id = "1148746000002449006"
        ref_view_id = "1148746000002449089"
        ref_column_id = "1148746000002449094"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.add_lookup(column_id, ref_view_id, ref_column_id)
        print("success")

    def remove_lookup(self, ac):
        column_id = "1148746000002449006"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_lookup(column_id)
        print("success")

    def hide_columns(self, ac):
        column_ids = []
        column_ids.append("1148746000002449006")
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.hide_columns(column_ids)
        print("success")

    def show_columns(self, ac):
        column_ids = []
        column_ids.append("1148746000002449006")
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.show_columns(column_ids)
        print("success")

    def copy_views(self, ac):
        view_ids = []
        view_ids.append("1148746000002457001")
        dest_workspace_id = "1148746000002575005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.copy_views(view_ids, dest_workspace_id)
        print(result)

    def copy_formulas(self, ac):
        formula_names = []
        formula_names.append("Total")
        dest_workspace_id = "1148746000002682001"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.copy_formulas(formula_names, dest_workspace_id)
        print("success")

    def create_similar_views(self, ac):
        ref_view_id = "1148746000002449002"
        folder_id = "1148746000002508116"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.create_similar_views(ref_view_id, folder_id)
        print("success")

    def auto_analyse_view(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.auto_analyse()
        print("success")

    def auto_analyse_column(self, ac):
        column_id = "1148746000002449006"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.auto_analyse_column(column_id)
        print("success")

    def get_orgs(self, ac):
        result = ac.get_orgs()
        print(result)

    def get_workspaces(self, ac):
        result = ac.get_workspaces()
        print(result)

    def get_owned_workspaces(self, ac):
        result = ac.get_owned_workspaces()
        print(result)

    def get_shared_workspaces(self, ac):
        result = ac.get_shared_workspaces()
        print(result)

    def get_views(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_views()
        print(result)

    def get_folders(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_folders()
        print(result)

    def get_recent_views(self, ac):
        result = ac.get_recent_views()
        print(result)

    def get_dashboards(self, ac):
        result = ac.get_dashboards()
        print(result)

    def get_owned_dashboards(self, ac):
        result = ac.get_owned_dashboards()
        print(result)

    def get_shared_dashboards(self, ac):
        result = ac.get_shared_dashboards()
        print(result)

    def get_workspace_secret_key(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_secret_key()
        print(result)

    def get_workspace_details(self, ac):
        result = ac.get_workspace_details(Config.WORKSPACEID)
        print(result)

    def get_view_details(self, ac):
        result = ac.get_view_details(Config.VIEWID)
        print(result)

    def add_favorite_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_favorite()
        print("success")

    def remove_favorite_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_favorite()
        print("success")

    def add_favorite_view(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.add_favorite()
        print("success")

    def remove_favorite_view(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_favorite()
        print("success")

    def add_default_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_default()
        print("success")

    def remove_default_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_default()
        print("success")

    def get_meta_details(self, ac):
        workspace_name = "API Lib";
        view_name = "Sales"
        org = ac.get_org_instance(Config.ORGID)    
        result = org.get_meta_details(workspace_name, view_name)
        print(result)

    def enable_domain_access(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.enable_domain_access()
        print("success")
        
    def disable_domain_access(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.disable_domain_access()
        print("success")        

    def get_org_admins(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_admins()
        print(result)

    def add_org_admins(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohotest.com")
        org = ac.get_org_instance(Config.ORGID)
        org.add_admins(email_ids)
        print("success")

    def remove_org_admins(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohotest.com")
        org = ac.get_org_instance(Config.ORGID)
        org.remove_admins(email_ids)
        print("success")

    def get_workspace_admins(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_admins()
        print(result)

    def add_workspace_admins(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohotest.com")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_admins(email_ids)
        print("success")

    def remove_workspace_admins(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohotest.com")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_admins(email_ids)
        print("success")

    def get_workspace_share_info(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_share_info()
        print(result)

    def share_views(self, ac):
        try:            
            view_ids = []
            view_ids.append("1148746000002449002")
            
            email_ids = []
            email_ids.append("sampleuser+1@zohotest.com")
            
            permissions = {}
            permissions["read"] = True
            workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
            workspace.share_views(view_ids, email_ids, permissions)
            print("success")
        except Exception as e:
            print(str(e))

    def remove_share(self, ac):
        try:            
            view_ids = []
            view_ids.append("1148746000002449002")
            
            email_ids = []
            email_ids.append("sampleuser+1@zohotest.com")
            
            permissions = {}
            permissions["read"] = True
            workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
            workspace.remove_share(view_ids, email_ids)
            print("success")
        except Exception as e:
            print(str(e))

    def get_shared_details_for_views(self, ac):
        view_ids = []
        view_ids.append("1148746000002449002")

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_shared_details_for_views(view_ids)
        print(result)

    def update_shared_details(self, ac):        
        email_ids = []
        email_ids.append("sampleuser+1@zoho.com")
        
        permissions = {}
        permissions["read"] = True
        permissions["export"] = True

        conf = {}
        conf["emailIds"] = email_ids
        conf["permissions"] = permissions

        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.update_shared_details(conf)
        print("success")

    def get_my_permissions(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_my_permissions()
        print(result)

    def get_groups(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_groups()
        print(result)

    def get_group_details(self, ac):
        group_id = "1148746000002588001"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_group_details(group_id)        
        print(result)

    def create_group(self, ac):
        group_name = "Grp 1"
        email_ids = []
        email_ids.append("sampleuser+1@zohotest.com")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_group(group_name, email_ids)
        print(result)

    def rename_group(self, ac):
        group_id = "35130000001364002"
        group_name = "Renamed Grp 1"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.rename_group(group_id, group_name)
        print("success")

    def add_group_members(self, ac):
        group_id = "1148746000002674003"
        email_ids = []
        email_ids.append("sampleuser+2@zohotest.com")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_group_members(group_id, email_ids)
        print("success")

    def remove_group_members(self, ac):
        group_id = "1148746000002674003"
        email_ids = []
        email_ids.append("sampleuser+2@zohotest.com")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_group_members(group_id, email_ids)
        print("success")

    def delete_group(self, ac):
        group_id = "1148746000002588001"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_group(group_id)
        print("success")

    def get_view_url(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_publish_url()
        print(result)

    def get_embed_url(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_embed_url()
        print(result)

    def get_private_url(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_private_url()
        print(result)
        
    def create_private_url(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.create_private_url()            
        print(result)

    def remove_private_access(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_private_access()
        print("success")

    def make_view_public(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.make_view_public()            
        print(result)

    def remove_public_access(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_public_access()
        print("success")

    def get_publish_configurations(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_publish_configurations()            
        print(result)

    def update_publish_configurations(self, ac):
        config = {}
        config["includeTitle"] = "true"
        config["includeDesc"] = "true"
        config["includeToolBar"] = "false"
        config["includeSocialWidgets"] = "false"
        config["includeSearchBox"] = "true"
        config["includeDatatypeSymbol"] = "false"
        config["includeShowHideOption"] = "false"
        config["isInteractive"] = "true"
        config["legendPosition"] = "RIGHT"
        config["width"] = "800"
        config["height"] = "600"
        config["autoRefresh"] = "-1"
        config["URLCriteria"] = ""
        config["includeAskZia"] = "false"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.update_publish_configurations(config)
        print("success")

    def create_slideshow(self, ac):
        slide_name = "Slideshow 1"
        view_ids = []
        view_ids.append("35130000001080100")
        view_ids.append("35130000001102015")
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_slideshow(slide_name, view_ids)
        print(result)

    def update_slideshow(self, ac):
        slide_id = ""

        config = {}
        config["slideName"] = "Slideshow 2"
        config["accessType"] = "1"
        view_ids = []
        view_ids.append("35130000001102001")
        view_ids.append("35130000001102034")
        config["viewIds"] = view_ids

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_slideshow(slide_id, config)
        print("success") 

    def delete_slideshow(self, ac):
        slide_id = ""
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_slideshow(slide_id)
        print("success")  

    def get_slideshows(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_slideshows()
        print(result)

    def get_slideshow_url(self, ac):
        slide_id = "35130000001396003"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_slideshow_url(slide_id)
        print(result)

    def get_slideshow_details(self, ac):
        slide_id = ""
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_slideshow_details(slide_id)           
        print(result)

    def create_variable(self, ac):
        variable_name = "Variable 1"
        variable_datatype = "1"
        variable_type = "3"

        variable_format = {}
        variable_format["alignment"] = "left"

        values_1 = []
        values_1.append("1")
        values_1.append("2")

        email_ids_1 = []
        email_ids_1.append("user+1@zoho.com")
        email_ids_1.append("user+2@zoho.com")

        dataset_1 = {}
        dataset_1["values"] = values_1
        dataset_1["emailIds"] = email_ids_1

        values_2 = []
        values_2.append("3")
        values_2.append("4")

        email_ids_2 = []
        email_ids_2.append("user+3@zoho.com")
        email_ids_2.append("user+4@zoho.com")

        dataset_2 = {}
        dataset_2["values"] = values_2
        dataset_2["emailIds"] = email_ids_2

        user_specific_data = []
        user_specific_data.append(dataset_1)
        user_specific_data.append(dataset_2)

        config = {}
        config["format"] = variable_format
        config["userSpecificData"] = user_specific_data

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_variable(variable_name, variable_datatype, variable_type, config)           
        print(result)

    def update_variable(self, ac):
        variable_id = "1767024000004598005"
        variable_name = "Variable 11"
        variable_datatype = "1"
        variable_type = "3"

        variable_format = {}
        variable_format["alignment"] = "left"

        values_1 = []
        values_1.append("11")
        values_1.append("12")

        email_ids_1 = []
        email_ids_1.append("user+1@zoho.com")
        email_ids_1.append("user+2@zoho.com")

        dataset_1 = {}
        dataset_1["values"] = values_1
        dataset_1["emailIds"] = email_ids_1

        values_2 = []
        values_2.append("13")
        values_2.append("14")

        email_ids_2 = []
        email_ids_2.append("user+3@zoho.com")
        email_ids_2.append("user+4@zoho.com")

        dataset_2 = {}
        dataset_2["values"] = values_2
        dataset_2["emailIds"] = email_ids_2

        user_specific_data = []
        user_specific_data.append(dataset_1)
        user_specific_data.append(dataset_2)

        config = {}
        config["format"] = variable_format
        config["userSpecificData"] = user_specific_data

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_variable(variable_id, variable_name, variable_datatype, variable_type, config)           
        print("success")

    def delete_variable(self, ac):
        variable_id = "1767024000004598005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_variable(variable_id)           
        print("success")

    def get_variables(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_variables()
        print(result)

    def get_variable_details(self, ac):
        variable_id = "1767024000004598005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_variable_details(variable_id)
        print(result)

    def make_default_folder(self, ac):
        folder_id = "1767024000004419353"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.make_default_folder(folder_id)           
        print("success")

    def get_datasources(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_datasources()
        print(result)

    def sync_data(self, ac):
        datasource_id = "1767024000004595194"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.sync_data(datasource_id)           
        print("success")

    def update_datasource_connection(self, ac):
        datasource_id = "1767024000003890005"
        
        config = {}
        config["serviceName"] = "AMAZON RDS"
        config["databaseType"] = "POSTGRESQL"
        config["hostName"] = "******"
        config["port"] = "5432"
        config["userName"] = "******"
        config["password"] = "******"
        config["cloudDatabaseName"] = "sampledb"

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_datasource_connection(datasource_id, config)           
        print("success")

    def get_trash_views(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_trash_views()
        print(result)

    def restore_trash_views(self, ac):
        view_id = "1767024000004595194"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.restore_trash_views(view_id)           
        print("success")

    def delete_trash_views(self, ac):
        view_id = "1767024000004595194"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_trash_views(view_id)           
        print("success")

    def refetch_data(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.refetch_data()           
        print("success")

    def get_last_import_details(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_last_import_details()           
        print(result)

    def get_subscription_details(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_subscription_details()
        print(result)

    def get_resource_details(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_resource_details()
        print(result)

    def get_users(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_users()        
        print(result)

    def add_users(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohocorp.com")
        org = ac.get_org_instance(Config.ORGID)
        org.add_users(email_ids)
        print("success")

    def remove_users(self, ac):
        email_ids = []
        email_ids.append("sampleuser+1@zohocorp.com")
        org = ac.get_org_instance(Config.ORGID)
        org.remove_users(email_ids)
        print("success")

    def activate_users(self, ac):
        email_ids = []
        email_ids.append("vinothkumar+1@zohotest.com")
        org = ac.get_org_instance(Config.ORGID)
        org.activate_users(email_ids)
        print("success")

    def deactivate_users(self, ac):
        email_ids = []
        email_ids.append("vinothkumar+1@zohotest.com")
        org = ac.get_org_instance(Config.ORGID)
        org.deactivate_users(email_ids)
        print("success")

    def change_user_role(self, ac):
        email_ids = []
        email_ids.append("user+1@zohotest.com")
        role = "USER"
        org = ac.get_org_instance(Config.ORGID)
        org.change_user_role(email_ids, role)
        print("success")    

    def get_aggregate_formulas_in_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_aggregate_formulas()
        print(result)

    def get_aggregate_formula_dependents(self, ac):
        formula_id = "1767024000011512005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_aggregate_formula_dependents(formula_id)
        print(result)

    def get_aggregate_formula_value(self, ac):
        formula_id = "1767024000011512005"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_aggregate_formula_value(formula_id)
        print(result)

    def create_report(self, ac):
        base_table_name = "Sales"

        xaxis = {
            "type": "xAxis",
            "columnName": "Date",
            "operation": "year"
        }

        yaxis = {
            "type": "yAxis",
            "columnName": "Sales",
            "operation": "sum"
        }

        axis_columns = [xaxis, yaxis]

        config = {
            "baseTableName": base_table_name,
            "title": "New Chart",
            "reportType": "chart",
            "axisColumns": axis_columns
        }

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        view_id = workspace.create_report(config)
        print(view_id)

    

    def update_report(self, ac):
        view_id = "35130000006311001"

        xaxis = {
            "type": "xAxis",
            "columnName": "Date",
            "operation": "year"
        }

        yaxis = {
            "type": "yAxis",
            "columnName": "Cost",
            "operation": "sum"
        }

        axis_columns = [xaxis, yaxis]

        config = {
            "reportType": "chart",
            "axisColumns": axis_columns
        }

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_report(view_id, config)
        print("success")

    def get_table_metadata(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_table_metadata()
        print(result)

    def reorder_columns(self, ac):
        column_ids = ["100003000000002011", "100003000000002005", "100003000000002006", "100003000000002007", "100003000000002008", "100003000000002009", "100003000000002010"]
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.reorder_columns(column_ids)
        print("success")

    def sort_data_by_columns(self, ac):
        column_ids = ["100003000000002010", "100003000000002006"]
        sort_order = 2  # 1 for ascending, 2 for descending
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.sort_data_by_columns(column_ids, sort_order, False)
        print("success")

    def sort_data_by_columns_reset(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.sort_data_by_columns(None, None, True)
        print("success")

    def get_query_table_details(self, ac):
        query_table_id = "466206000000061149"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_query_table_details(query_table_id)
        print(result)

    def get_automl_analysis_in_org(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_automl_analysis()
        print(result)

    def get_automl_analysis_in_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_automl_analysis()
        print(result)

    def get_automl_analysis_details(self, ac):
        analysis_id = "466206000000073001"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_automl_analysis_details(analysis_id)
        print(result)

    def get_deployment_details(self, ac):
        analysis_id = "466206000000061115"
        model_id = "466206000000061117"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_deployment_details(analysis_id, model_id)
        print(result)

    def create_automl_analysis(self, ac):

        automl_name = "Sales Analysis"
        training_table_id = "466206000000061002"
        prediction_type = "CLASSIFICATION"

        # Columns that should be used as features during training
        features = []
        features.append("Region")
        features.append("Product Category")
        features.append("Sales")

        # Server compute size (1 → 8GB, 2 → 16GB, 3 → 32GB)
        server_option = 1

        # Algorithms and their parameters
        algorithms = {
            "decisionTreeClassification": {
                "minimumSampleSplit": "2",
                "maximumDepth": "100"
            },
            "randomForestClassification": {
                "minimumSampleSplit": "2",
                "maximumDepth": "100",
                "numberOfTrees": "25"
            }
        }

        config = {}
        config["description"] = "Sales Table Analysis..."
        config["targetColumn"] = "Product"

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)

        automl_id = workspace.create_automl_analysis(
            automl_name,
            training_table_id,
            prediction_type,
            features,
            server_option,
            algorithms,
            config
        )
        print("Created AutoML Analysis ID:", automl_id)

    def delete_automl_analysis_sample(self, ac):
        analysis_id = "466206000000061134"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_automl_analysis(analysis_id)
        print(f"AutoML Analysis {analysis_id} deleted successfully.")

    def delete_automl_analysis_model(self, ac):

        analysis_id = "466206000000061115"
        model_id = "466206000000061117"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_automl_analysis_model(analysis_id, model_id)
        print(f"Model {model_id} from AutoML Analysis {analysis_id} deleted successfully.")

    def create_automl_deployment(self, ac):

        analysis_id = "466206000000073001" 
        model_id = "466206000000073003"

        # Input table to run predictions on
        input_table_id = "466206000000061002"  

        # New output table that will be generated during deployment
        output_table = "SalesDep"

        # Columns to include in the output table
        output_columns = []
        output_columns.append("Sales")
        output_columns.append("Region")

        # Prediction column to be added in output table
        prediction_column = "precol"

        # Compute size option (1 → 8GB, 2 → 16GB, 3 → 32GB)
        server_option = 1

        # Import behavior: APPEND, TRUNCATEADD, or UPDATEADD
        import_type = "APPEND"

        # Schedule details (#optional. Can be None)
        schedule_details = {
            "calendarFrequency": "hourly",
            "interval": 3
        }

        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)

        deployment_info = workspace.create_automl_analysis_deployment(
            analysis_id,
            model_id,
            input_table_id,
            output_table,
            output_columns,
            prediction_column,
            server_option,
            import_type,
            schedule_details
        )
        print("Deployment Details:", deployment_info)

    def deploy_automl_analysis(self, ac):
        analysis_id = "466206000000073001"
        deployment_id = "466206000000073057"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.deploy_automl_analysis(analysis_id, deployment_id)

    def delete_automl_analysis_deployment(self, ac):
        analysis_id = "466206000000073001"
        deployment_id = "466206000000073057"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_automl_analysis_deployment(analysis_id, deployment_id)

    def automl_analysis_prediction(self, ac):

        analysis_id = "466206000000073001" 
        model_id = "466206000000073003"

        # Features for prediction (single input record)
        features = {
            "Sales": 1000,
            "Region": "East",
            "Product Category": "Stationery"
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)

        prediction_result = workspace.automl_analysis_prediction(
            analysis_id,
            model_id,
            features
           )

        print("Prediction Result:")
        print(prediction_result)


    def get_custom_roles(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_custom_roles()
        print(result)

    def create_custom_role(self, ac):
        role_name = "DashboardPowerUser"
        # Allowed values for access_type: 'ALL_DATA_REPORTS_AND_DASHBOARDS', 'ALL_REPORTS_AND_DASHBOARDS', 'ALL_DASHBOARDS'
        access_type = "ALL_DASHBOARDS"
        permissions = {
            "interactionPermissions": {
                "read": True,
                "vud": True,
                "drillDown": True,
                "insight": True
            },
            "sharePermissions": {
                "discussion": True,
                "privateLinks": True
            },
            "publishPermissions": {
                "export": True
            }
        }
        org = ac.get_org_instance(Config.ORGID)
        result = org.create_custom_role(role_name, access_type, permissions)
        print(result)

    def update_custom_role(self, ac):
        role_id = ""
        role_name = "DashboardPowerUser"
        # Allowed values for access_type: 'ALL_DATA_REPORTS_AND_DASHBOARDS', 'ALL_REPORTS_AND_DASHBOARDS', 'ALL_DASHBOARDS'
        access_type = "ALL_DASHBOARDS"
        permissions = {
            "interactionPermissions": {
                "read": True,
                "vud": True,
                "drillDown": False,
                "insight": False
            },
            "sharePermissions": {
                "share": True,
                "privateLinks": False
            },
            "publishPermissions": {
                "export": True
            }
        }
        org = ac.get_org_instance(Config.ORGID)
        org.update_custom_role(role_id, role_name, access_type, permissions)
        print("success")

    def delete_custom_role(self, ac):
        role_id = ""
        org = ac.get_org_instance(Config.ORGID)
        org.delete_custom_role(role_id)
        print("success")

    def get_query_tables(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_query_tables()
        print(result)

    def get_tags(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_tags()
        print(result)

    def create_tag(self, ac):
        tag_name = "Sales Tag"
        color_code = "#FF5733"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_tag(tag_name, color_code)
        print(result)

    def update_tag(self, ac):
        tag_id = ""
        config = {"name": "Sales Tag Updated", "colorCode": "#33FF57"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_tag(tag_id, config)
        print("success")

    def delete_tag(self, ac):
        tag_id = ""
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_tag(tag_id)
        print("success")

    def add_tag_to_views(self, ac):
        tag_id = ""
        view_ids = [""]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_tag_to_views(tag_id, view_ids)
        print("success")

    def remove_tag_from_views(self, ac):
        tag_id = ""
        view_ids = [""]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_tag_from_views(tag_id, view_ids)
        print("success")

    def get_tagged_views(self, ac):
        tag_id = ""
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_tagged_views(tag_id)
        print(result)

    def get_view_tags(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_view_tags()
        print(result)

    def add_tags_to_view(self, ac):
        tag_ids = [""]
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.add_tags_to_view(tag_ids)
        print("success")

    def remove_tags_from_view(self, ac):
        tag_ids = [""]
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_tags_from_view(tag_ids)
        print("success")



    def get_alerts_in_view(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_alerts_in_view()
        print(result)

    def get_view_metadata_for_alert(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.get_view_metadata_for_alert()
        print(result)

    def create_alert(self, ac):
        alert_name = "Sales Drop Alert"
        schedule_details = {
            "calendarFrequency": "daily",
            "hour": 9,
            "minute": 0
        }
        rules = [
            {
                "operator": "lt",
                "viewColumnIndex": "2",
                "type": "constant",
                "values": ["1000"]
            }
        ]
        config = {
            "email": {
                "notifyAdmins": True,
                "subject": "Sales dropped below threshold",
                "message": "Please review the report."
            }
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.create_alert(alert_name, schedule_details, rules, config)
        print(result)

    def get_alerts_in_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_alerts_in_workspace()
        print(result)

    def get_alert_configuration(self, ac):
        alert_id = "35130000001056611"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_alert_configuration(alert_id)
        print(result)

    def update_alert(self, ac):
        alert_id = "35130000001056611"
        alert_name = "Sales Drop Alert (weekly)"
        schedule_details = {
            "calendarFrequency": "weekly",
            "hour": 9,
            "minute": 30,
            "weekDays": [6],
            "timeZone": "Asia/Kolkata"
        }
        rules = [
            {
                "operator": "lt",
                "viewColumnIndex": "2",
                "type": "constant",
                "values": ["1000"]
            }
        ]
        config = {
            "email": {
                "notifyAdmins": True,
                "emailIds": ["finance@example.com"],
                "subject": "Weekly sales monitor",
                "message": "Weekly alert summary."
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_alert(alert_id, alert_name, schedule_details, rules, config)
        print("success")

    def delete_alerts(self, ac):
        alert_ids = ["137687000010815003", "137687000010815005"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_alerts(alert_ids)
        print("success")

    def change_alert_status(self, ac):
        alert_ids = ["137687000010815003", "137687000010815005"]
        enabled = False
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_alert_status(alert_ids, enabled)
        print("success")

    def run_alert(self, ac):
        alert_id = "35130000001056611"
        config = {"validateSystemTags": False}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.run_alert(alert_id, config)
        print("success")

    def get_alert_events(self, ac):
        alert_id = "35130000001056611"
        config = {
            "fromDate": "2026-05-01 00:00:00",
            "toDate": "2026-05-31 23:59:59",
            "status": ["triggered", "error"],
            "pageNo": 1,
            "recordsPerPage": 50
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_alert_events(alert_id, config)
        print(result)

    def get_linked_workspaces(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_linked_workspaces()
        print(result)

    def get_linked_workspaces_for_org(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_linked_workspaces()
        print(result)

    def get_linkable_workspaces(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_linkable_workspaces()
        print(result)

    def get_workspace_linking_compatibility(self, ac):
        clients = [
            {
                "orgId": "700000654321",
                "workspaceIds": ["466206000000071000"]
            }
        ]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_linking_compatibility(clients)
        print(result)

    def link_workspaces(self, ac):
        clients = [
            {
                "orgId": "700000654321",
                "workspaceIds": ["466206000000071000"]
            }
        ]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.link_workspaces(clients)
        print("success")

    def unlink_workspaces(self, ac):
        scope = "ALL"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.unlink_workspaces(scope)
        print("success")

    def sync_linked_workspaces(self, ac):
        scope = "ALL"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.sync_linked_workspaces(scope)
        print("success")

    def get_linked_workspace_sync_details(self, ac):
        sandbox_ids = ["137687000012345001", "137687000012345002"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_linked_workspace_sync_details(sandbox_ids)
        print(result)

    def get_workspace_backups(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_backups()
        print(result)

    def backup_workspace_now(self, ac):
        config = {"backupMode": "STRUCTURE"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.backup_workspace_now(config)
        print(result)

    def get_workspace_backup_status(self, ac):
        backup_id = "35130000001056701"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_backup_status(backup_id)
        print(result)

    def download_workspace_backup(self, ac):
        backup_id = "35130000001056701"
        file_path = "/home/user/workspace-backup.zip"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.download_workspace_backup(backup_id, file_path)
        print("success")

    def restore_workspace_from_backup(self, ac):
        backup_id = "35130000001056701"
        confirm_restore = True
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.restore_workspace_from_backup(backup_id, confirm_restore)
        print(result)

    def get_workspace_restore_status(self, ac):
        restore_id = "35130000001056801"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_restore_status(restore_id)
        print(result)

    def create_dashboard(self, ac):
        display_name = "Sales Overview"
        layout = json.dumps({
            "1": {"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
            "2": {"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Sales Dashboard</b>"},
            "3": {"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": {}}
        })
        config = {
            "settings": {
                "allowDrillDown": "true",
                "fitToWidth": "true"
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_dashboard(display_name, layout, config)
        print(result)

    def update_dashboard(self, ac):
        dashboard_id = "35130000001055801"
        layout = json.dumps({
            "1": {"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
            "2": {"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Updated Title</b>"},
            "3": {"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": {}}
        })
        config = {"layout": layout}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_dashboard(dashboard_id, config)
        print("success")

    def get_dashboard_metadata(self, ac):
        dashboard_id = "35130000001055801"
        config = {"include": "layout"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_dashboard_metadata(dashboard_id, config)
        print(result)

    def get_report_metadata(self, ac):
        report_id = "35130000001055901"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_report_metadata(report_id)
        print(result)

    def get_org_access_restrictions(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_org_access_restrictions()
        print(result)

    def update_org_access_restrictions(self, ac):
        config = {"accessRestrictionEnabled": True}
        org = ac.get_org_instance(Config.ORGID)
        org.update_org_access_restrictions(config)
        print("success")

    def get_workspace_access_restrictions(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_access_restrictions()
        print(result)

    def update_workspace_access_restrictions(self, ac):
        config = {
            "useOrganizationSettings": False,
            "shareViews": {
                "domainRestrictionEnabled": True,
                "trustedDomains": ["example.com", "partner.example.org"]
            },
            "privateLinks": {"enabled": False},
            "publicViews": {"enabled": False},
            "exportViews": {"enabled": True}
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_workspace_access_restrictions(config)
        print("success")



    def set_proxy(self, ac):
        ac.set_proxy(Config.PROXY_HOST, Config.PROXY_PORT, Config.PROXY_USER, Config.PROXY_PASSWORD)
        print("success")

    def get_secret_key(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_secret_key()
        print(result)

    def export_data_stream(self, ac):
        response_format = "csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        stream = bulk.export_data_stream(Config.VIEWID, response_format)
        with open("/home/local/admin/Files/Sales.csv", "wb") as out_file:
            for chunk in stream.stream(8192):
                out_file.write(chunk)
        stream.release_conn()
        print("success")

    def export_bulk_data_stream(self, ac):
        job_id = "35130000001334001"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        stream = bulk.export_bulk_data_stream(job_id)
        with open("/home/local/admin/Files/Sales.csv", "wb") as out_file:
            for chunk in stream.stream(8192):
                out_file.write(chunk)
        stream.release_conn()
        print("success")


try:
    obj = sample()
    obj.get_subscription_details(obj.ac);
    
except Exception as e:
    print(str(e))
