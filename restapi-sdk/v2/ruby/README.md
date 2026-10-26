# Zoho Analytics Ruby SDK

A comprehensive Ruby client library for interacting with the Zoho Analytics API. This SDK provides a simple and intuitive interface for managing organizations, workspaces, views, and performing data operations within Zoho Analytics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Authentication](#authentication)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Error Handling](#error-handling)

## Features

The Zoho Analytics Ruby SDK provides comprehensive functionality for:

- **Authentication**: OAuth 2.0 and direct access token support with automatic token refresh
- **Organization Management**: Create, manage, and retrieve organization details
- **Workspace Operations**: Create, copy, rename, and manage workspaces
- **View Management**: Create tables, query tables, and manage views
- **Bulk Operations**: Import and export large datasets efficiently

## Installation

Add this line to your application's Gemfile:

```ruby
gem 'zoho_analytics_client'
```

And then execute:

```bash
$ bundle install
```

Or install it yourself as:

```bash
$ gem install zoho_analytics_client
```

## Authentication

The SDK supports two authentication methods:

### 1. OAuth 2.0 Authentication (Recommended)

```ruby
require 'zoho_analytics_client'

client = AnalyticsClient.new
  .with_data_center("US")
  .with_oauth({
    "clientId" => "your_client_id",
    "clientSecret" => "your_client_secret",
    "refreshToken" => "your_refresh_token"
  })
  .with_token_store_path("/path/to/token/store")
  .build
```

### 2. OAuth 2.0 Authentication (Without storing the token)

```ruby
require 'zoho_analytics_client'

client = AnalyticsClient.new
  .with_data_center("US")
  .with_oauth({
    "clientId" => "your_client_id",
    "clientSecret" => "your_client_secret",
    "refreshToken" => "your_refresh_token"
  })
  .build
```

### 3. Direct Access Token

```ruby
client = AnalyticsClient.new
  .with_data_center("US")
  .with_access_token("your_direct_access_token")
  .build
```

### Data Centers

The SDK supports multiple data centers. Specify the appropriate data center for your Zoho Analytics account:

- `US` - United States (accounts.zoho.com)
- `EU` - Europe (accounts.zoho.eu)
- `IN` - India (accounts.zoho.in)
- `AU` - Australia (accounts.zoho.com.au)
- `CN` - China (accounts.zoho.com.cn)
- `CA` - Canada (accounts.zohocloud.ca)
- `JP` - Japan (accounts.zoho.jp)
- `SA` - Saudi Arabia (accounts.zoho.sa)
- `UAE` - United Arab Emirates (accounts.zoho.ae)

## Quick Start

Here's a simple example to get you started:

```ruby
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
```



## API Reference

The SDK is structured around different API categories:

### `AnalyticsClient`

This is the main client class for interacting with the Zoho Analytics API. It provides methods for authentication and access to other API instances.

- `AnalyticsClient.new`: Returns a `Builder` instance to configure the client.
- `set_accounts_server_url(url)`: Sets the accounts server URL.
- `get_accounts_server_url`: Gets the current accounts server URL.
- `set_analytics_server_url(url)`: Sets the analytics server URL.
- `get_analytics_server_url`: Gets the current analytics server URL.
- `get_org_instance(org_id)`: Returns an `OrgAPI` instance for organization-level operations.
- `get_workspace_instance(org_id, workspace_id)`: Returns a `WorkspaceAPI` instance for workspace-level operations.
- `get_view_instance(org_id, workspace_id, view_id)`: Returns a `ViewAPI` instance for view-level operations.
- `get_bulk_instance(org_id, workspace_id)`: Returns a `BulkAPI` instance for bulk data operations.
- `get_orgs`: Returns a list of all accessible organizations.
- `get_workspaces`: Returns a list of all accessible workspaces.
- `get_owned_workspaces`: Returns a list of owned workspaces.
- `get_shared_workspaces`: Returns a list of shared workspaces.
- `get_recent_views`: Returns a list of recently accessed views.
- `get_dashboards`: Returns a list of all accessible dashboards.
- `get_owned_dashboards`: Returns a list of owned dashboards.
- `get_shared_dashboards`: Returns a list of shared dashboards.
- `get_workspace_details(workspace_id)`: Returns details of the specified workspace.
- `get_view_details(view_id, config = {})`: Returns details of the specified view.

### `OrgAPI`

Provides methods for organization-level operations.

- `create_workspace(workspace_name, config = {})`: Creates a blank workspace.
- `get_admins`: Returns a list of admins for the organization.
- `get_users`: Returns a list of users for the organization.
- `add_users(email_ids, config = {})`: Adds users to the organization.
- `remove_users(email_ids, config = {})`: Removes users from the organization.
- `activate_users(email_ids, config = {})`: Activates users in the organization.
- `deactivate_users(email_ids, config = {})`: Deactivates users in the organization.
- `change_user_role(email_ids, role, config = {})`: Changes the role for specified users.
- `get_subscription_details`: Returns subscription details of the organization.
- `get_resource_details`: Returns resource usage details of the organization.
- `get_meta_details(workspace_name, view_name = nil)`: Returns metadata details of a workspace or view.

### `WorkspaceAPI`

Provides methods for workspace-level operations.

- `copy(new_workspace_name, config = {}, dest_org_id = nil)`: Copies the specified workspace.
- `rename(workspace_name, config = {})`: Renames the specified workspace.
- `delete`: Deletes the specified workspace.
- `get_secret_key(config = {})`: Gets the secret key for the workspace.
- `add_favorite`: Marks the workspace as favorite.
- `remove_favorite`: Unmarks the workspace as favorite.
- `add_default`: Sets the workspace as default.
- `remove_default`: Unsets the workspace from default.
- `get_admins`: Returns a list of admins for the workspace.
- `add_admins(email_ids, config = {})`: Adds admins to the workspace.
- `remove_admins(email_ids, config = {})`: Removes admins from the workspace.
- `create_folder(folder_name, config = {})`: Creates a new folder in the workspace.
- `get_views(config = {})`: Gets a list of all views in the workspace.
- `create_table(table_design)`: Creates a new table in the workspace.
- `create_query_table(sql_query, query_table_name, config = {})`: Creates a new query table.
- `edit_query_table(view_id, sql_query, config = {})`: Updates an existing query table.
- `copy_views(view_ids, dest_workspace_id, config = {}, dest_org_id = nil)`: Copies views to another workspace.
- `enable_domain_access`: Enables the workspace for white-label domain access.
- `disable_domain_access`: Disables white-label domain access for the workspace.

### `ViewAPI`

Provides methods for view-level operations.

- `rename(view_name, config = {})`: Renames the specified view.
- `delete(config = {})`: Deletes the specified view.
- `save_as(new_view_name, config = {})`: Creates a copy of the view with a new name.
- `copy_formulas(formula_names, dest_workspace_id, config = {}, dest_org_id = nil)`: Copies formulas to another workspace or view.
- `add_favorite`: Marks the view as a favorite.
- `remove_favorite`: Removes the view from favorites.
- `create_similar_views(ref_view_id, folder_id, config = {})`: Creates similar reports based on a reference view.
- `auto_analyse(config = {})`: Performs auto analysis or auto generation of reports.
- `get_my_permissions`: Retrieves the current user's permissions for the view.
- `get_view_url(config = {})`: Gets the published URL of the view.
- `get_embed_url(config = {})`: Gets the embed URL for embedding the view in web pages.
- `get_private_url(config = {})`: Gets the private URL for secure access to the view.
- `create_private_url(config = {})`: Creates a private URL for the view.
- `remove_private_access`: Removes private access for the view.
- `make_view_public(config = {})`: Publishes the view publicly.
- `remove_public_access`: Removes public access for the view.
- `get_publish_configurations`: Gets the current publish configurations for the view.
- `update_publish_configurations(config = {})`: Updates publish configurations for the view.
- `add_column(column_name, data_type, config = {})`: Adds a new column to the view.
- `hide_columns(column_ids)`: Hides specified columns in the view.
- `show_columns(column_ids)`: Shows previously hidden columns.
- `add_row(column_values, config = {})`: Adds a data row to the view.
- `update_row(column_values, criteria, config = {})`: Updates rows matching criteria.
- `delete_row(criteria, config = {})`: Deletes rows matching criteria.
- `rename_column(column_id, column_name, config = {})`: Renames a specified column.
- `delete_column(column_id, config = {})`: Deletes a column from the view.
- `add_lookup(column_id, ref_view_id, ref_column_id, config = {})`: Adds a lookup (reference) column.
- `remove_lookup(column_id, config = {})`: Removes a lookup.
- `auto_analyse_column(column_id, config = {})`: Performs auto-analysis for a column.
- `refetch_data(config = {})`: Triggers a data sync for the view.
- `get_last_import_details`: Retrieves details of the last data import into the view.
- `get_formula_columns`: Lists all formula columns in the view.
- `add_formula_column(formula_name, expression, config = {})`: Adds a formula column.
- `edit_formula_column(formula_id, expression, config = {})`: Edits an existing formula column.
- `delete_formula_column(formula_id, config = {})`: Deletes a formula column.
- `get_aggregate_formulas`: Retrieves aggregate formulas for the view.
- `add_aggregate_formula(formula_name, expression, config = {})`: Adds an aggregate formula.
- `edit_aggregate_formula(formula_id, expression, config = {})`: Edits an aggregate formula.
- `delete_aggregate_formula(formula_id, config = {})`: Deletes an aggregate formula.
- `get_view_dependents`: Lists dependent views relying on this view.
- `get_column_dependents(column_id)`: Gets dependents for a specific column.
- `update_shared_details(config = {})`: Updates sharing configurations of the view.


### `BulkAPI`

Provides methods for bulk data operations.
- `import_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})`: Imports data from a file into a newly created table.
- `import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config = {}, tool_config = {})`: Imports data into a new table asynchronously in batches.
- `import_raw_data_in_new_table(table_name, file_type, auto_identify, data, config = {})`: Imports raw data (string or bytes) into a new table.
- `import_data(view_id, import_type, file_type, auto_identify, file_path, config = {})`: Imports data from a file into an existing view.
- `import_raw_data(view_id, import_type, file_type, auto_identify, data, config = {})`: Imports raw data into an existing view.
- `import_bulk_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})`: Initiates a bulk asynchronous import to a new table.
- `import_bulk_data(view_id, import_type, file_type, auto_identify, file_path, config = {})`: Initiates a bulk asynchronous import to an existing view.
- `import_data_as_batches(view_id, import_type, auto_identify, file_path, batch_size, config = {}, tool_config = {})`: Imports data into an existing view asynchronously in batches.
- `get_import_job_details(job_id)`: Retrieves details and status of an ongoing or completed import job.
- `export_data(view_id, response_format, file_path, config = {})`: Exports data from the specified view to a local file.
- `initiate_bulk_export(view_id, response_format, config = {})`: Initiates an asynchronous bulk export job.
- `initiate_bulk_export_using_sql(sql_query, response_format, config = {})`: Initiates an asynchronous bulk export using a SQL query.
- `get_export_job_details(job_id)`: Retrieves metadata and status of an export job.
- `export_bulk_data(job_id, file_path)`: Downloads the exported bulk data file for a completed job.

## Examples

Refer to the `sample.rb` file in the SDK for more examples of how to use the different API methods.

## Error Handling

The SDK raises custom exceptions for different error scenarios:

- `ArgumentError`: Raised for invalid or missing arguments.
- `ServerError`: Raised when the Zoho Analytics API returns an error (e.g., authentication failure, invalid request).
- `ParseError`: Raised when the API response cannot be parsed.

It is recommended to wrap your API calls in `begin...rescue` blocks to handle these exceptions gracefully.


