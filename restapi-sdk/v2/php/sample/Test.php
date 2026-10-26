<?php

    require 'AnalyticsClient.php';

    class Test
    {
        public $ac = NULL;

        public $client_id = "1000.********************";
        public $client_secret = "****************************************";
        public $refresh_token = "1000.********************.********************";

        public $org_id = "";
        public $workspace_id = "";
        public $view_id = "";

        function __construct() {
            $this->ac =  new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function addRow() {
            $column_values = array();
            $column_values["name"] = "Vincent";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->addRow($column_values);
            print_r($response);
        }

        function updateRow() {
            $column_values = array();
            $column_values["name"] = "Vincent";
            $criteria = "\"age\"='30'";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->updateRow($column_values, $criteria);
            print_r($response);
        }

        function deleteRow() {
            $criteria = "\"name\"='Vincent'";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->deleteRow($criteria);
            print_r($response);
        }

        function importDataInNewTable() {
            $table_name = "php_import";
            $file_type = "csv";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.csv";

            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importDataInNewTable($table_name, $file_type, $auto_identify, $file_path);
            print_r($response);
        }

        function importData() {
            $import_type = "append";
            $file_type = "csv";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importData($this->view_id, $import_type, $file_type, $auto_identify, $file_path);
            print_r($response);
        }

        function importRawDataInNewTable() {
            $table_name = "php_newtab";
            $file_type = "json";
            $auto_identify = "true";
            $raw_data = '[{"Date":"06 February, 2017","Region":"West","Product Category":"Grocery","Product":"Fruits and Vegetables","Customer Name":"Vincent Herbert","Sales":"$1,682.39","Cost":"$200.05"},{"Date":"08 February, 2017","Region":"East","Product Category":"Furniture","Product":"Clocks","Customer Name":"John Britto","Sales":"$272.34","Cost":"$14.58"}]';
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importRawDataInNewTable($table_name, $file_type, $auto_identify, $raw_data);
            print_r($response);
        }

        function importRawData() {
            $import_type = "truncateadd";
            $file_type = "json";
            $auto_identify = "true";
            $raw_data = '[{"Date":"06 February, 2017","Region":"West","Product Category":"Grocery","Product":"Fruits and Vegetables","Customer Name":"Vincent Herbert","Sales":"$1,682.39","Cost":"$200.05"},{"Date":"08 February, 2017","Region":"East","Product Category":"Furniture","Product":"Clocks","Customer Name":"John Britto","Sales":"$272.34","Cost":"$14.58"}]';
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importRawData($this->view_id, $import_type, $file_type, $auto_identify, $raw_data);
            print_r($response);
        }

        function importBulkDataInNewTable() {
            $table_name = "json1";
            $file_type = "json";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.json";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importBulkDataInNewTable($table_name, $file_type, $auto_identify, $file_path);
            print_r($response);
        }

        function importBulkData() {
            $import_type = "truncateadd";
            $file_type = "csv";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importBulkData($this->view_id, $import_type, $file_type, $auto_identify, $file_path);
            print_r($response);
        }

        function importBulkDataInNewTableAsBatches() {
            $table_name = "php_batch_import";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.csv";
            $batch_size = 50000;

            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importBulkDataInNewTableAsBatches($table_name, $auto_identify, $file_path, $batch_size);
            print_r($response);
        }

        function importBulkDataAsBatches() {
            $import_type = "truncateadd";
            $auto_identify = "true";
            $file_path = "/home/local/admin/Files/Sales.csv";
            $batch_size = 50000;

            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importBulkDataAsBatches($this->view_id, $import_type, $auto_identify, $file_path, $batch_size);
            print_r($response);
        }

        function getImportJobDetails() {
            $job_id = "35130000001342088";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->getImportJobDetails($job_id);
            print_r($response);
        }

        function exportData() {
            $response_format = "csv";
            $file_path = "/home/admin/2.9.0/v2/php/Sales.csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $bulk->exportData($this->view_id, $response_format, $file_path);
        }

        function exportDataStream() {

            $response_format = "csv";
        
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
        
            $stream = $bulk->exportDataStream(
                $this->view_id,
                $response_format
            );
        
            try {
                while (!feof($stream)) {
                    $line = fgets($stream);
                    if ($line !== false) {
                        echo rtrim($line) . PHP_EOL;
                    }
                }
            } finally {
                fclose($stream);
            }
        }
        

        function initiateBulkExport() {
            $response_format = "csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->initiateBulkExport($this->view_id, $response_format);
            print_r($response);
        }

        function initiateBulkExportUsingSQL() {
            $sql_query = "select * from Sales";
            $response_format = "csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->initiateBulkExportUsingSQL($sql_query, $response_format);
            print_r($response);
        }

        function getExportJobDetails() {
            $job_id = "35130000001345002";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->getExportJobDetails($job_id);
            print_r($response);
        }

        function exportBulkData() {
            $job_id = "35130000001345002";
            $file_path = "/home/local/admin/Files/Sales.csv";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $bulk->exportBulkData($job_id, $file_path);
        }

        function exportBulkDataAsStream() {

            $job_id = "466206000000104004";
        
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
        
            $stream = $bulk->exportBulkDataStream($job_id);
        
            try {
                while (!feof($stream)) {
                    $line = fgets($stream);
                    if ($line !== false) {
                        echo rtrim($line) . PHP_EOL;
                    }
                }
            } finally {
                fclose($stream);
            }
        }
        

        function createWorkspace() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $workspace_name = "PHP Lib workspace - 1";
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->createWorkspace($workspace_name);
            print_r($response);
        }

        function copyWorkspace() {
            $new_workspace_name = "PHP Lib copy workspace";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->copy($new_workspace_name);
            print_r($response);
        }

        function renameWorkspace() {
            $workspace_name = "Renamed PHP Lib workspace";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->rename($workspace_name);
            echo "success\n";
        }

        function deleteWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->delete();
            echo "success\n";
        }

        function createTable() {
            $table_design = array();
            $table_design["TABLENAME"] = "Sample";
            $table_design["TABLEDESCRIPTION"] = "Description";

            $column1 = array();
            $column1["COLUMNNAME"] = "Col1";
            $column1["DATATYPE"] = "PLAIN";

            $column2 = array();
            $column2["COLUMNNAME"] = "Col2";
            $column2["DATATYPE"] = "NUMBER";

            $columns = array($column1, $column2);
            $table_design["COLUMNS"] = $columns;

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createTable($table_design);
            print_r($response);
        }

        function createQueryTable() {
            $sql_query = "";
            $query_table_name = "";

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createQueryTable($sql_query, $query_table_name);
            print_r($response);
        }

        function editQueryTable() {
            $query_table_id = "";
            $sql_query = "";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->editQueryTable($query_table_id, $sql_query);
            echo "success\n";
        }

        function saveAsView() {
            $new_view_name = "New View";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->saveAs($new_view_name);
            print_r($response);
        }

        function renameView() {
            
            $view_name = "Renamed view 1";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->rename($view_name);
            echo "success\n";
        }

        function deleteView() {
            
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->delete();
            echo "success\n";
        }

        function createFolder() {
            $folder_name = "API Lib workspace";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createFolder($folder_name);
            print_r($response);
        }

        function renameFolder() {
            $folder_id = "1148746000002451001";
            $folder_name = "Renamed folder";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->renameFolder($folder_id, $folder_name);
            echo "success\n";
        }

        function deleteFolder() {
            $folder_id = "1148746000002451001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteFolder($folder_id);
            echo "success\n";
        }

        function changeFolderHierarchy() {
            $folder_id = "1148746000002451001";
            $hierarchy = "1";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeFolderHierarchy($folder_id, $hierarchy);
            echo "success\n";
        }

        function changeFolderPosition() {
            $folder_id = "1148746000002451001";
            $reference_folder_id = "1148746000002451003";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeFolderPosition($folder_id, $reference_folder_id);
            echo "success\n";
        }

        function moveViewsToFolder() {
            $folder_id = "1148746000002451001";
            $view_ids = array("1148746000002449094", "1148746000002449095");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->moveViewsToFolder($folder_id, $view_ids);
            echo "success\n";
        }

        function exportAsTemplate() {
            $file_path = "/home/local/admin/Files/Sales.atpt";
            $view_ids = array("35130000001080001", "35130000001080082");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->exportAsTemplate($view_ids, $file_path);
            echo "success\n";
        }

        function getWorkspaceUsers() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceUsers();
            print_r($response);
        }

        function addWorkspaceUsers() {
            $email_ids = array("user1@zoho.com");
            $role = "USER";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addWorkspaceUsers($email_ids, $role, NULL);
            echo "success\n";
        }

        function removeWorkspaceUsers() {
            $email_ids = array("user1@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeWorkspaceUsers($email_ids);
            echo "success\n";
        }

        function changeWorkspaceUserStatus() {
            $email_ids = array("user1@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $operation = "deactivate";
            $workspace->changeWorkspaceUserStatus($email_ids, $operation);
            echo "success\n";
        }

        function changeWorkspaceUserRole() {
            $email_ids = array("user1@zoho.com");
            $role = "USER";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeWorkspaceUserRole($email_ids, $role);
            echo "success\n";
        }

        function getFormulaColumns() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getFormulaColumns();
            print_r($response);
        }

        function addFormulaColumn() {
            $formula_name = "New Column";
            $expression = "square(\"Cost\")";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->addFormulaColumn($formula_name, $expression);
            print_r($response);
        }

        function editFormulaColumn() {
            $formula_id = "1148746000002453001";
            $expression = "square(\"Cost\")";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->editFormulaColumn($formula_id, $expression);
            echo "success\n";
        }

        function deleteFormulaColumn() {
            $formula_id = "1148746000002453001";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->deleteFormulaColumn($formula_id, $expression);
            echo "success\n";
        }

        function getAggregateFormulas() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getAggregateFormulas();
            print_r($response);
        }

        function addAggregateFormula() {
            $formula_name = "New Column";
            $expression = "sum(\"Cost\")";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->addAggregateFormula($formula_name, $expression);
            print_r($response);
        }

        function editAggregateFormula() {
            $formula_id = "1148746000002453001";
            $expression = "sum(\"Cost\")";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->editAggregateFormula($formula_id, $expression);
            echo "success\n";
        }

        function deleteAggregateFormula() {
            $formula_id = "1148746000002453001";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->deleteAggregateFormula($formula_id);
            echo "success\n";
        }

        function getEmailSchedules() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $email_schedules = $workspace->getEmailSchedules();
            print_r($email_schedules);
        }

        function createEmailSchedule() {
            $schedule_name = "Schedule1";
            $format = "CSV";

            $view_ids = array(1148746000002578004, 1148746000002578002);
            $email_ids = array("user_1@zoho.com");

            $schedule_details = array(
                "calendarFrequency" => "Daily",
                "hour" => 10,
                "minute" => 30
            );

            $config = array(
                "subject" => "Daily Sales Report"
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $scheduleId = $workspace->createEmailSchedule($schedule_name, $view_ids, $format, $email_ids, $schedule_details, $config);
            echo $scheduleId;
        }

        function updateEmailSchedule() {
            $schedule_id = 115674600000150007;

            $schedule_details = array(
                "calendarFrequency" => "Daily",
                "hour" => 8,
                "minute" => 30
            );

            $config = array(
                "subject" => "Daily Sales Overview",
                "scheduleDetails" => $schedule_details
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $newScheduleId = $workspace->updateEmailSchedule($schedule_id, $config);
            echo $newScheduleId;
        }

        function triggerEmailSchedule() {
            $schedule_id = 115674600000150007;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->triggerEmailSchedule($schedule_id);
        }

        function changeEmailScheduleStatus() {
            $schedule_id = 115674600000150007;
            $operation = "activate";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeEmailScheduleStatus($schedule_id, $operation);
        }

        function deleteEmailSchedule() {
            $schedule_id = 115674600000150007;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteEmailSchedule($schedule_id);
        }


        function getViewDependents() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getViewDependents();
            print_r($response);
        }

        function getColumnDependents() {
            $column_id = "1148746000002453001";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getColumnDependents($column_id);
            print_r($response);
        }

        function addColumn() {
            $column_name = "New Column";
            $data_type = "PLAIN";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->addColumn();
            print_r($response);
        }

        function renameColumn() {
            $column_id = "1148746000002453001";
            $column_name = "Renamed Col 1";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->renameColumn($column_id, $column_name);
            echo "success\n";
        }

        function deleteColumn() {
            $column_id = "1148746000002453001";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->deleteColumn($column_id);
            echo "success\n";
        }

        function createLookup() {
            $column_id = "1148746000002449094";
            $ref_view_id = "1148746000002449002";
            $ref_column_id = "1148746000002449006";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->createLookup($column_id, $ref_view_id, $ref_column_id);
            echo "success\n";
        }

        function removeLookup() {
            $column_id = "1148746000002449094";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->removeLookup($column_id);
            echo "success\n";
        }

        function hideColumns() {
            $column_ids = array("1148746000002449094", "1148746000002449095");
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->hideColumns($column_ids);
            echo "success\n";
        }

        function showColumns() {
            
            $column_ids = array("1148746000002449094", "1148746000002449095");
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->showColumns($column_ids);
            echo "success\n";
        }
        function copyViews() {
            $dest_workspace_id = "1148746000002449089";
            $view_ids = array("1148746000002449094", "1148746000002449095");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->copyViews($view_ids, $dest_workspace_id);
            print_r($response);
        }
        function copyFormulas() {
            $dest_workspace_id = "1148746000002449089";
            $formula_names = array("F1", "F2");
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->copyFormulas($formula_names, $dest_workspace_id);
            echo "success\n";
        }

        function createSimilarViews() {
            
            $ref_view_id = "1148746000002449002";
            $folder_id = "1148746000002449073";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->createSimilarViews($ref_view_id, $folder_id);
            echo "success\n";
        }

        function autoAnalyseView() {
            
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->autoAnalyse();
            echo "success\n";
        }

        function autoAnalyseColumn() {
            $column_id = "35130000001352010";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->autoAnalyseColumn($column_id);
            echo "success\n";
        }

        function getOrgs() {
            $response = $this->ac->getOrgs();
            print_r($response);
        }

        function getWorkspaces() {
            $response = $this->ac->getWorkspaces();
            print_r($response);
        }

        function getOwnedWorkspaces() {
            $response = $this->ac->getOwnedWorkspaces();
            print_r($response);
        }

        function getSharedWorkspaces() {
            $response = $this->ac->getSharedWorkspaces();
            print_r($response);
        }

        function getViews() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getViews();
            print_r($response);
        }

        function getFolders() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getFolders();
            print_r($response);
        }

        function getRecentViews() {
            $response = $this->ac->getRecentViews();
            print_r($response);
        }

        function getDashboards() {
            $response = $this->ac->getDashboards();
            print_r($response);
        }

        function getOwnedDashboards() {
            $response = $this->ac->getOwnedDashboards();
            print_r($response);
        }

        function getSharedDashboards() {
            $response = $this->ac->getSharedDashboards();
            print_r($response);
        }

        function getWorkspaceSecretKey() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getSecretKey();
            print_r($response);
        }

        function getWorkspaceDetails() {
            $response = $this->ac->getWorkspaceDetails($this->workspace_id);
            print_r($response);
        }  

        function getViewDetails() {
            $response = $this->ac->getViewDetails($this->view_id, NULL);
            print_r($response);
        }

        function addFavoriteWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addFavorite();
            echo "success\n";
        }

        function removeFavoriteWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeFavorite();
            echo "success\n";
        }

        function addFavoriteView() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->addFavorite();
            echo "success\n";
        }

        function removeFavoriteView() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->removeFavorite();
            echo "success\n";
        }

        function addDefaultWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addDefault();
            echo "success\n";
        }

        function removeDefaultWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeDefault();
            echo "success\n";
        }

        function getMetaDetails() {
            $workspace_name = "PHP Lib workspace - 1";
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getMetaDetails($workspace_name, NULL);
            print_r($response);
        }

        function enableDomainAccess() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->enableDomainAccess();
            echo "success\n";
        }

        function disableDomainAccess() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->disableDomainAccess();
            echo "success\n";
        }

        function getOrgAdmins() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getAdmins();
            print_r($response);
        }

        function addOrgAdmins() {
            $email_ids = array("vinothkumar.krishnasamy+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->addAdmins($email_ids);
            echo "success\n";
        }

        function removeOrgAdmins() {
            $email_ids = array("vinothkumar.krishnasamy+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->removeAdmins($email_ids);
            echo "success\n";
        }

        function getWorkspaceAdmins() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAdmins();
            print_r($response);
        }

        function addWorkspaceAdmins() {
            $email_ids = array("vinothkumar.krishnasamy+1@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addAdmins($email_ids);
            echo "success\n";
        }

        function removeWorkspaceAdmins() {
            $email_ids = array("vinothkumar.krishnasamy+1@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeAdmins($email_ids);
            echo "success\n";
        }

        function getWorkspaceShareInfo() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getShareInfo();
            print_r($response);
        }

        function shareViews() {
        
            $view_ids = array("35130000001353002", "35130000001355005");
            $email_ids = array("user+1@zoho.com", "user+2@zoho.com");
            $permissions = array();
            $permissions["read"] = "true";

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->shareViews($view_ids, $email_ids, $permissions);
            echo "success\n";
        }

        function removeShare() {
        
            $view_ids = array("35130000001080001", "35130000001080082");
            $email_ids = array("user+1@zoho.com", "user+2@zoho.com");

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeShare($view_ids, $email_ids);
            echo "success\n";
        }

        function getSharedDetailsForViews() {
            $view_ids = array("1767024000008742002", "1767024000008742002");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $workspace->getSharedDetailsForViews($view_ids);
            print_r($response);
        }

        function updateSharedDetails() {
        
            $email_ids = array("user+1@zoho.com", "user+2@zoho.com");
            $permissions = array();
            $permissions["read"] = "true";
            $permissions["export"] = "true";

            $config = array();
            $config["emailIds"] = $email_ids;
            $config["permissions"] = $permissions;
            
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->updateSharedDetails($config);
            echo "success\n";
        }

        function getMyPermissions() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getMyPermissions();
            print_r($response);
        }

        function getGroups() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getGroups();
            print_r($response);
        }

        function getGroupDetails() {
            $group_id = "35130000001364001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getGroupDetails($group_id);
            print_r($response);
        }

        function createGroup() {
            $group_name = "Sample Group 1";
            $group_members = array("vinothkumar.krishnasamy+1@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response =  $workspace->createGroup($group_name, $group_members);
            print_r($response);
        }

        function renameGroup() {
            $group_id = "35130000001364001";
            $new_group_name = "Renamed Group 1";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->renameGroup($group_id, $new_group_name);
            echo "success\n";
        }

        function addGroupMembers() {
            $group_id = "35130000001364001";
            $group_members = array("vinothkumar.krishnasamy+2@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addGroupMembers($group_id, $group_members);
            echo "success\n";
        }

        function removeGroupMembers() {
            $group_id = "35130000001364001";
            $group_members = array("vinothkumar.krishnasamy+2@zoho.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeGroupMembers($group_id, $group_members);
            echo "success\n";
        }

        function deleteGroup() {
            $group_id = "35130000001364001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteGroup($group_id);
            echo "success\n";
        }

        function getViewURL() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getViewURL();
            print_r($response);
        }

        function getEmbedURL() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getEmbedURL();
            print_r($response);
        }

        function getPrivateURL() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getPrivateURL();
            print_r($response);
        }

        function createPrivateURL() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->createPrivateURL();
            print_r($response);
        }

        function removePrivateAccess() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->removePrivateAccess();
            echo "success\n";
        }

        function makeViewPublic() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->makeViewPublic();
            print_r($response);
        }

        function removePublicAccess() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->removePublicAccess();
            echo "success\n";
        }

        function getPublishConfigurations() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getPublishConfigurations();
            print_r($response);
        }

        function updatePublishConfigurations() {

            $config = array();
            $config["includeTitle"] = "true";
            $config["includeDesc"] = "true";
            $config["includeToolBar"] = "false";
            $config["includeSocialWidgets"] = "false";
            $config["includeSearchBox"] = "true";
            $config["includeDatatypeSymbol"] = "false";
            $config["includeShowHideOption"] = "false";
            $config["isInteractive"] = "true";
            $config["legendPosition"] = "RIGHT";
            $config["width"] = "800";
            $config["height"] = "600";
            $config["autoRefresh"] = "-1";
            $config["URLCriteria"] = "";
            $config["includeAskZia"] = "false";

            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->updatePublishConfigurations($config);
            echo "success\n";
        }

        function getSlideshows() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getSlideshows();
            print_r($response);
        }

        function getSlideshowDetails() {
            $slide_id = "35130000001396003";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getSlideshowDetails($slide_id);
            print_r($response);
        }

        function getSlideshowUrl() {
            $slide_id = "";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getSlideshowUrl($slide_id);
            print_r($response);
        }

        function createSlideshow() {
            $slide_name = "Sample Group 1";
            $view_ids = array("");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response =  $workspace->createGroup($slide_name, $view_ids);
            print_r($response);
        }

        function updateSlideshow() {
            $slide_id = "";
            $slide_name = "Slideshow 1";
            $view_ids = array("35130000001080001", "35130000001080082");

            $config = array();
            $config["slideName"] = $slide_name;
            $config["viewIds"] = $view_ids;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateSlideshow($slide_id, $config);
        }

        function deleteSlideshow() {
            $slide_id = "";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteSlideshow($slide_id);
        }

        function createVariable() {
            $variable_name = "Variable 2";
            $variable_datatype = "1";
            $variable_type = "3";
            
            $format = array();
            $format["alignment"] = "left";

            $values_1 = array("1", "2");
            $email_ids_1 = array("user+1@zoho.com", "user+2@zoho.com");

            $dataset_1 = array();
            $dataset_1["values"] = $values_1;
            $dataset_1["emailIds"] = $email_ids_1;
            
            $values_2 = array("3", "4");
            $email_ids_2 = array("user+3@zoho.com", "user+4@zoho.com");

            $dataset_2 = array();
            $dataset_2["values"] = $values_2;
            $dataset_2["emailIds"] = $email_ids_2;

            $user_specific_data = array($dataset_1, $dataset_2);

            $config = array();
            $config["format"] = $format;
            $config["userSpecificData"] = $user_specific_data;

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response =  $workspace->createVariable($variable_name, $variable_datatype, $variable_type, $config);
            print_r($response);
        }

        function updateVariable() {
            $variable_id = "1767024000004613001";
            $variable_name = "Variable 11";
            $variable_datatype = "1";
            $variable_type = "3";
            
            $format = array();
            $format["alignment"] = "left";

            $values_1 = array("11", "12");
            $email_ids_1 = array("user+1@zoho.com", "user+2@zoho.com");

            $dataset_1 = array();
            $dataset_1["values"] = $values_1;
            $dataset_1["emailIds"] = $email_ids_1;
            
            $values_2 = array("13", "14");
            $email_ids_2 = array("user+3@zoho.com", "user+4@zoho.com");

            $dataset_2 = array();
            $dataset_2["values"] = $values_2;
            $dataset_2["emailIds"] = $email_ids_2;

            $user_specific_data = array($dataset_1, $dataset_2);

            $config = array();
            $config["format"] = $format;
            $config["userSpecificData"] = $user_specific_data;

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateVariable($variable_id, $variable_name, $variable_datatype, $variable_type, $config);
            echo "success\n";
        }

        function deleteVariable() {
            $variable_id = "1767024000004613001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteVariable($variable_id);
            echo "success\n";
        }

        function getVariables() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getVariables();
            print_r($response);
        }

        function getVariableDetails() {
            $variable_id = "1767024000004613001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getVariableDetails($variable_id);
            print_r($response);
        }

        function makeDefaultFolder() {
            $folder_id = "1767024000004595001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->makeDefaultFolder($folder_id);
            echo "success\n";
        }

        function getDatasources() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getDatasources();
            print_r($response);
        }

        function syncData() {
            $datasource_id = "1767024000004595194";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->syncData($datasource_id);
            echo "success\n";
        }

        function updateDatasourceConnection() {
            $datasource_id = "1767024000003890005";

            $config = array();
            $config["serviceName"] = "AMAZON RDS";
            $config["databaseType"] = "MYSQL";
            $config["hostName"] = "******";
            $config["port"] = "3306";
            $config["userName"] = "******";
            $config["password"] = "******";
            $config["cloudDatabaseName"] = "sampledb";

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateDatasourceConnection($datasource_id, $config);
            echo "success\n";
        }

        function getTrashViews() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getTrashViews();
            print_r($response);
        }

        function restoreTrashView() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->restoreTrashView($this->view_id);
            echo "success\n";
        }

        function deleteTrashView() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteTrashView($this->view_id);
            echo "success\n";
        }

        function refetchData() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->refetchData();
            echo "success\n";
        }

        function getLastImportDetails() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getLastImportDetails();
            print_r($response);
        }

        function getUsers() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getUsers();
            print_r($response);
        }

        function addUsers() {
            $email_ids = array("vinothtest+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->addUsers($email_ids, NULL);
            echo "success\n";
        }

        function removeUsers() {
            $email_ids = array("vinothtest+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->removeUsers($email_ids);
            echo "success\n";
        }

        function activateUsers() {
            $email_ids = array("vinothtest+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->activateUsers($email_ids);
            echo "success\n";
        }

        function deactivateUsers() {
            $email_ids = array("vinothtest+2@zoho.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->deactivateUsers($email_ids);
            echo "success\n";
        }

        function changeUserRole() {
            $email_ids = array("user+2@zoho.com");
            $role = "USER";
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->changeUserRole($email_ids, $role);
            echo "success\n";
        }

        function getSubscriptionDetails() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getSubscriptionDetails();
            print_r($response);
        }

        function getResourceDetails() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getResourceDetails();
            print_r($response);
        }

        function getAggregateFormulasInWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAggregateFormulas();
            print_r($response);
        }

        function getAggregateFormulaDependents() {
            $formula_id = "1148746000002453001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAggregateFormulaDependents($formula_id);
            print_r($response);
        }

        function getAggregateFormulaValue() {
            $formula_id = "1148746000002453001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAggregateFormulaValue($formula_id);
            print_r($response);
        }

        function createReport() {
            $base_table_name = "Sales";

            $x_axis = [
                "type" => "xAxis",
                "columnName" => "Date",
                "operation" => "year"
            ];

            $y_axis = [
                "type" => "yAxis",
                "columnName" => "Sales",
                "operation" => "sum"
            ];

            $axis_columns = [$x_axis, $y_axis];

            $config = [
                "baseTableName" => $base_table_name,
                "title" => "New Chart",
                "reportType" => "chart",
                "axisColumns" => $axis_columns
            ];

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $view_id = $workspace->createReport($config);
            print_r($view_id);
        }

        function updateReport() {
            $view_id = "35130000006310013";

            $x_axis = [
                "type" => "xAxis",
                "columnName" => "Date",
                "operation" => "year"
            ];

            $y_axis = [
                "type" => "yAxis",
                "columnName" => "Cost",
                "operation" => "sum"
            ];

            $axis_columns = [$x_axis, $y_axis];

            $config = [
                "reportType" => "chart",
                "axisColumns" => $axis_columns
            ];

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->updateReport($view_id, $config);
            print_r($response);
        }

        function getTableMetadata() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $result = $view->getTableMetadata();
            print_r($result);
        }

        function reorderColumns() {
            $column_ids = array(
                "466206000000073013",
                "466206000000073014",
                "466206000000069003"
            );
        
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->reorderColumns($column_ids);
            echo "success\n";
        }

        function sortDataByColumns() {
            $column_ids = array(
                "466206000000073014",
                "466206000000073013"
            );
        
            $sort_order = 2; // 1 = Ascending, 2 = Descending
        
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->sortDataByColumns($column_ids, $sort_order, false);
            echo "success\n";
        }
        

        function resetSort() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->sortDataByColumns(NULL, NULL, true);
            echo "success\n";
        }

        function getQueryTableDetails() {
            $query_table_id = "466206000000061149";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getQueryTableDetails($query_table_id);
            print_r($response);
        }
        
        function getAutoMLAnalysisInOrg() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getAutoMLAnalysis();
            print_r($response);
        }

        function getAutoMLAnalysisInWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAutoMLAnalysis();
            print_r($response);
        }

        function getAutoMLAnalysisDetails() {
            $analysis_id = "466206000000126001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAutoMLAnalysisDetails($analysis_id);
            print_r($response);
        }

        function getDeploymentDetails() {
            $analysis_id = "466206000000061115";
            $model_id = "466206000000061119";
        
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getDeploymentDetails($analysis_id, $model_id);
            print_r($response);
        }

        function createAutoMLAnalysis() {
            $automl_name = "Sales Analysis";
            $training_table_id = "466206000000061002";
            $prediction_type = "CLASSIFICATION";
        
            $features = array("Region", "Product Category", "Sales");
            $server_option = 1;
        
            $algorithms = array(
                "decisionTreeClassification" => array(
                    "minimumSampleSplit" => "2",
                    "maximumDepth" => "100"
                ),
                "randomForestClassification" => array(
                    "minimumSampleSplit" => "2",
                    "maximumDepth" => "100",
                    "numberOfTrees" => "25"
                )
            );
        
            $config = array(
                "description" => "Sales Table Analysis...",
                "targetColumn" => "Product"
            );
        
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $automl_id = $workspace->createAutoMLAnalysis(
                $automl_name,
                $training_table_id,
                $prediction_type,
                $features,
                $server_option,
                $algorithms,
                $config
            );
        
            echo "Created AutoML Analysis ID: " . $automl_id . PHP_EOL;
        }
        
        function deleteAutoMLAnalysis() {
            $analysis_id = "466206000000126001";
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $workspace->deleteAutoMLAnalysis($analysis_id);
        
            echo "AutoML Analysis {$analysis_id} deleted successfully\n";
        }

        function deleteAutoMLAnalysisModel() {
            $analysis_id = "466206000000126001";
            $model_id = "466206000000126003";
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $workspace->deleteAutoMLAnalysisModel($analysis_id, $model_id);
        
            echo "Model {$model_id} from AutoML Analysis {$analysis_id} deleted successfully\n";
        }

        function createAutoMLDeployment() {
            $analysis_id = "466206000000126001";
            $model_id = "466206000000126003";
        
            $input_table_id = "466206000000061002";
            $output_table = "SalesDep - 1";
        
            $output_columns = array("Sales", "Region");
            $prediction_column = "precol";
        
            $server_option = 1;
            $import_type = "APPEND";
        
            $schedule_details = array(
                "calendarFrequency" => "hourly",
                "interval" => 3
            );
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $deployment_info = $workspace->createAutoMLAnalysisDeployment(
                $analysis_id,
                $model_id,
                $input_table_id,
                $output_table,
                $output_columns,
                $prediction_column,
                $server_option,
                $import_type,
                $schedule_details
            );
        
            echo "Deployment Details:\n";
            print_r($deployment_info);
        }

        function deployAutoMLAnalysis() {
            $analysis_id = "466206000000126001";
            $deployment_id = "466206000000126117";
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $workspace->deployAutoMLAnalysis($analysis_id, $deployment_id);
        
            echo "AutoML Deployment executed successfully\n";
        }

        function deleteAutoMLAnalysisDeployment() {
            $analysis_id = "466206000000126001";
            $deployment_id = "466206000000126117";
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $workspace->deleteAutoMLAnalysisDeployment($analysis_id, $deployment_id);
        
            echo "AutoML Deployment deleted successfully\n";
        }

        function autoMLAnalysisPrediction() {
            $analysis_id = "466206000000126001";
            $model_id = "466206000000126003";
        
            $features = array(
                "Sales" => 1000,
                "Region" => "East",
                "Product Category" => "Stationery"
            );
        
            $workspace = $this->ac->getWorkspaceInstance(
                $this->org_id,
                $this->workspace_id
            );
        
            $prediction_result = $workspace->autoMLAnalysisPrediction(
                $analysis_id,
                $model_id,
                $features
            );
        
            echo "Prediction Result:\n";
            print_r($prediction_result);
        }

        function getCustomRoles() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getCustomRoles();
            print_r($response);
        }
        function createCustomRole() {
            $role_name = "DashboardPowerUser";
            // Allowed values for $access_type: 'ALL_DATA_REPORTS_AND_DASHBOARDS', 'ALL_REPORTS_AND_DASHBOARDS', 'ALL_DASHBOARDS'
            $access_type = "ALL_DASHBOARDS";
            $permissions = array(
                "interactionPermissions" => array(
                    "read" => true,
                    "vud" => true,
                    "drillDown" => true,
                    "insight" => true
                ),
                "sharePermissions" => array(
                    "discussion" => true,
                    "privateLinks" => true
                ),
                "publishPermissions" => array(
                    "export" => true
                )
            );
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->createCustomRole($role_name, $access_type, $permissions);
            print_r($response);
        }
        function updateCustomRole() {
            $role_id = "";
            $role_name = "DashboardPowerUser";
            // Allowed values for $access_type: 'ALL_DATA_REPORTS_AND_DASHBOARDS', 'ALL_REPORTS_AND_DASHBOARDS', 'ALL_DASHBOARDS'
            $access_type = "ALL_DASHBOARDS";
            $permissions = array(
                "interactionPermissions" => array(
                    "read" => true,
                    "vud" => true,
                    "drillDown" => false,
                    "insight" => false
                ),
                "sharePermissions" => array(
                    "share" => true,
                    "privateLinks" => false
                ),
                "publishPermissions" => array(
                    "export" => true
                )
            );
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->updateCustomRole($role_id, $role_name, $access_type, $permissions);
            echo "success\n";
        }
        function deleteCustomRole() {
            $role_id = "";
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->deleteCustomRole($role_id);
            echo "success\n";
        }
        function getQueryTables() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getQueryTables();
            print_r($response);
        }
        function getTags() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getTags();
            print_r($response);
        }

        function createTag() {
            $tag_name = "Sales Tag";
            $color_code = "#FF5733";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createTag($tag_name, $color_code);
            print_r($response);
        }

        function updateTag() {
            $tag_id = "";
            $config = array(
                "name" => "Sales Tag Updated",
                "colorCode" => "#33FF57"
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateTag($tag_id, $config);
            echo "success\n";
        }

        function deleteTag() {
            $tag_id = "";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteTag($tag_id);
            echo "success\n";
        }

        function addTagToViews() {
            $tag_id = "";
            $view_ids = array($this->view_id);
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addTagToViews($tag_id, $view_ids);
            echo "success\n";
        }

        function removeTagFromViews() {
            $tag_id = "";
            $view_ids = array($this->view_id);
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->removeTagFromViews($tag_id, $view_ids, false);
            echo "success\n";
        }

        function getTaggedViews() {
            $tag_id = "";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getTaggedViews($tag_id);
            print_r($response);
        }

        function getViewTags() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getViewTags();
            print_r($response);
        }

        function addTagsToView() {
            $tag_ids = array("");
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->addTagsToView($tag_ids);
            echo "success\n";
        }

        function removeTagsFromView() {
            $tag_ids = array("");
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $view->removeTagsFromView($tag_ids, false);
            echo "success\n";
        }

        function getAlertsInView() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getAlertsInView();
            print_r($response);
        }

        function getViewMetadataForAlert() {
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->getViewMetadataForAlert();
            print_r($response);
        }

        function createAlert() {
            $alert_name = "Sales Drop Alert";

            $schedule_details = array(
                "calendarFrequency" => "daily",
                "hour" => 9,
                "minute" => 0
            );

            $rules = array(
                array(
                    "operator" => "lt",
                    "viewColumnIndex" => "2",
                    "type" => "constant",
                    "values" => array("1000")
                )
            );

            $config = array(
                "email" => array(
                    "notifyAdmins" => true,
                    "subject" => "Sales dropped below threshold",
                    "message" => "Please review the report."
                )
            );

            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $alertId = $view->createAlert($alert_name, $schedule_details, $rules, $config);
            echo $alertId;
        }

        function getAlertsInWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAlertsInWorkspace();
            print_r($response);
        }

        function getAlertConfiguration() {
            $alert_id = "35130000001056611";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAlertConfiguration($alert_id);
            print_r($response);
        }

        function updateAlert() {
            $alert_id = "35130000001056611";
            $alert_name = "Sales Drop Alert (weekly)";

            $schedule_details = array(
                "calendarFrequency" => "weekly",
                "hour" => 9,
                "minute" => 30,
                "weekDays" => array(6),
                "timeZone" => "Asia/Kolkata"
            );

            $rules = array(
                array(
                    "operator" => "lt",
                    "viewColumnIndex" => "2",
                    "type" => "constant",
                    "values" => array("1000")
                )
            );

            $config = array(
                "email" => array(
                    "notifyAdmins" => true,
                    "emailIds" => array("finance@example.com"),
                    "subject" => "Weekly sales monitor",
                    "message" => "Weekly alert summary."
                )
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateAlert($alert_id, $alert_name, $schedule_details, $rules, $config);
            echo "success\n";
        }

        function deleteAlerts() {
            $alert_ids = array("137687000010815003", "137687000010815005");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteAlerts($alert_ids);
            echo "success\n";
        }

        function changeAlertStatus() {
            $alert_ids = array("137687000010815003", "137687000010815005");
            $enabled = false;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeAlertStatus($alert_ids, $enabled);
            echo "success\n";
        }

        function runAlert() {
            $alert_id = "35130000001056611";
            $config = array("validateSystemTags" => false);
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->runAlert($alert_id, $config);
            echo "success\n";
        }

        function getAlertEvents() {
            $alert_id = "35130000001056611";

            $config = array(
                "fromDate" => "2026-05-01 00:00:00",
                "toDate" => "2026-05-31 23:59:59",
                "status" => array("triggered", "error"),
                "pageNo" => 1,
                "recordsPerPage" => 50
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAlertEvents($alert_id, $config);
            print_r($response);
        }

        function getLinkedWorkspaces() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getLinkedWorkspaces();
            print_r($response);
        }

        function getLinkedWorkspacesForOrg() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getLinkedWorkspaces();
            print_r($response);
        }

        function getLinkableWorkspaces() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getLinkableWorkspaces();
            print_r($response);
        }

        function getWorkspaceLinkingCompatibility() {
            $clients = array(
                array(
                    "orgId" => "700000654321",
                    "workspaceIds" => array("466206000000071000")
                )
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceLinkingCompatibility($clients);
            print_r($response);
        }

        function linkWorkspaces() {
            $clients = array(
                array(
                    "orgId" => "700000654321",
                    "workspaceIds" => array("466206000000071000")
                )
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->linkWorkspaces($clients);
            echo "success\n";
        }

        function unlinkWorkspaces() {
            $scope = "ALL";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->unlinkWorkspaces($scope);
            echo "success\n";
        }

        function syncLinkedWorkspaces() {
            $scope = "ALL";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->syncLinkedWorkspaces($scope);
            echo "success\n";
        }

        function getLinkedWorkspaceSyncDetails() {
            $sandbox_ids = array("137687000012345001", "137687000012345002");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getLinkedWorkspaceSyncDetails($sandbox_ids);
            print_r($response);
        }

        function getWorkspaceBackups() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceBackups();
            print_r($response);
        }

        function backupWorkspaceNow() {
            $config = array("backupMode" => "STRUCTURE");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->backupWorkspaceNow($config);
            print_r($response);
        }

        function getWorkspaceBackupStatus() {
            $backup_id = "35130000001056701";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceBackupStatus($backup_id);
            print_r($response);
        }

        function downloadWorkspaceBackup() {
            $backup_id = "35130000001056701";
            $file_path = "/home/user/workspace-backup.zip";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->downloadWorkspaceBackup($backup_id, $file_path);
            echo "success\n";
        }

        function restoreWorkspaceFromBackup() {
            $backup_id = "35130000001056701";
            $confirm_restore = true;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->restoreWorkspaceFromBackup($backup_id, $confirm_restore);
            print_r($response);
        }

        function getWorkspaceRestoreStatus() {
            $restore_id = "35130000001056801";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceRestoreStatus($restore_id);
            print_r($response);
        }

        function createDashboard() {
            $display_name = "Sales Overview";

            $layout = json_encode(array(
                "1" => array("type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0),
                "2" => array("type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Sales Dashboard</b>"),
                "3" => array("type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => new stdClass())
            ));

            $config = array(
                "settings" => array(
                    "allowDrillDown" => "true",
                    "fitToWidth" => "true"
                )
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $dashboardId = $workspace->createDashboard($display_name, $layout, $config);
            echo $dashboardId;
        }

        function updateDashboard() {
            $dashboard_id = "35130000001055801";

            $layout = json_encode(array(
                "1" => array("type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0),
                "2" => array("type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Updated Title</b>"),
                "3" => array("type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => new stdClass())
            ));

            $config = array("layout" => $layout);

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateDashboard($dashboard_id, $config);
            echo "success\n";
        }

        function getDashboardMetadata() {
            $dashboard_id = "35130000001055801";
            $config = array("include" => "layout");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getDashboardMetadata($dashboard_id, $config);
            print_r($response);
        }

        function getReportMetadata() {
            $report_id = "35130000001055901";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getReportMetadata($report_id);
            print_r($response);
        }

        function getOrgAccessRestrictions() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getOrgAccessRestrictions();
            print_r($response);
        }

        function updateOrgAccessRestrictions() {
            $config = array("accessRestrictionEnabled" => true);
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->updateOrgAccessRestrictions($config);
            echo "success\n";
        }

        function getWorkspaceAccessRestrictions() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getWorkspaceAccessRestrictions();
            print_r($response);
        }

        function updateWorkspaceAccessRestrictions() {
            $config = array(
                "useOrganizationSettings" => false,
                "shareViews" => array(
                    "domainRestrictionEnabled" => true,
                    "trustedDomains" => array("example.com", "partner.example.org")
                ),
                "privateLinks" => array("enabled" => false),
                "publicViews" => array("enabled" => false),
                "exportViews" => array("enabled" => true)
            );

            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateWorkspaceAccessRestrictions($config);
            echo "success\n";
        }
        function getReadTimeout() {
            $timeout = $this->ac->getReadTimeout();
            echo $timeout;
        }

        function setReadTimeout() {
            $time_limit = 1000;
            $this->ac->setReadTimeout($time_limit);
            echo "success\n";
        }

        function getConnectionTimeout() {
            $timeout = $this->ac->getConnectionTimeout();
            echo $timeout;
        }

        function setConnectionTimeout() {
            $time_limit = 1000;
            $this->ac->setConnectionTimeout($time_limit);
            echo "success\n";
        }

        function setProxy() {
            $proxy_host = "proxy.example.com";
            $proxy_port = 8443;
            // Allowed values for proxy_type: "HTTP", "HTTPS", "BOTH"
            $proxy_type = "BOTH";
            $proxy_user_name = "proxyUser";
            $proxy_password = "proxyPassword";
            $this->ac->setProxy($proxy_host, $proxy_port, $proxy_type, $proxy_user_name, $proxy_password);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->exportData();
    }
    catch(ServerException $se) {
        echo "Server exception - ErrorCode : " . $se->getErrorCode() . ", ErrorMessage : " . $se->getErrorMessage() . "\n";
    }
    catch(IOException $ioe) {
        echo "IO exception : " . $ioe->getErrorMessage() . "\n";
    }
    catch(ParseException $pe) {
        echo "Parser exception : " . $pe->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getErrorMessage() . "\n";
    }
