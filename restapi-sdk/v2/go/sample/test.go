package main

import (
	"fmt"
	ZAnalytics "zoho/pkg/analyticsclient"
)

var (
	clientId     = ""
	clientSecret = ""
	refreshToken = ""

	orgId       = ""
	workspaceId = ""
	viewId      = ""
)

func GetOrgs(ac ZAnalytics.Client) {
	result, exception := ac.GetOrgs()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaces(ac ZAnalytics.Client) {
	result, exception := ac.GetWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetOwnedWorkspaces(ac ZAnalytics.Client) {
	result, exception := ac.GetOwnedWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetSharedWorkspaces(ac ZAnalytics.Client) {
	result, exception := ac.GetSharedWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetRecentViews(ac ZAnalytics.Client) {
	result, exception := ac.GetRecentViews()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RenameColumn(ac ZAnalytics.Client) {
	columnid := "1148746000002515001"
	columnname := "Renamed Column"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RenameColumn(columnid, columnname)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnid := "1148746000002515001"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.DeleteColumn(columnid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddLookup(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnid := "1148746000002449006"
	refviewId := "1148746000002449089"
	refcolumnid := "1148746000002449094"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.AddLookup(columnid, refviewId, refcolumnid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveLookup(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnid := "1148746000002449006"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RemoveLookup(columnid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AutoAnalyseColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnid := "1148746000002508122"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.AutoAnalyseColumn(columnid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddRow(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnvalues := map[string]interface{}{}
	columnvalues["Region"] = "Test"
	columnvalues["Product Category"] = "New"
	columnvalues["Product"] = "New"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, err := view.AddRow(columnvalues, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateRow(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnvalues := map[string]interface{}{}
	columnvalues["Region"] = "Test"
	columnvalues["Product Category"] = "Updated"
	columnvalues["Product"] = "Updated"
	criteria := "\"Region\"='Test'"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, err := view.UpdateRow(columnvalues, criteria, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func DeleteRow(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	criteria := "\"Region\"='Test'"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, err := view.DeleteRow(criteria, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CopyWorkspace(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	newworkspacename := "Go Lib Copied db"
	destorgid := ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.Copy(newworkspacename, config, destorgid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RenameWorkspace(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	workspacename := "Renamed Go Lib"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.Rename(workspacename, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.Delete()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetWorkspaceSecretKey(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetSecretKey(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceDetails(ac ZAnalytics.Client) {
	result, exception := ac.GetWorkspaceDetails(workspaceId)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetViewDetails(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	result, exception := ac.GetViewDetails(viewId, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddFavoriteWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.AddFavorite()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveFavoriteWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RemoveFavorite()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddDefaultWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.AddDefault()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveDefaultWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RemoveDefault()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetWorkspaceAdmins(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAdmins()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddWorkspaceAdmins(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.AddAdmins(emailids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveWorkspaceAdmins(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RemoveAdmins(emailids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetFolders(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetFolders()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateFolder(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	foldername := "Go Lib"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateFolder(foldername, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetTrashViews(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetTrashViews()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RestoreTrashView(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	viewid := "1148746000002449002"
	config := map[string]interface{}{}
	exception := workspace.RestoreTrashView(viewid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteTrashView(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	viewid := "1148746000002449002"
	config := map[string]interface{}{}
	exception := workspace.DeleteTrashView(viewid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetViews(ac ZAnalytics.Client) {
	var config map[string]interface{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetViews(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateTable(ac ZAnalytics.Client) {
	tableDesign := map[string]interface{}{}
	tableDesign["TABLENAME"] = "Table Name"
	tableDesign["TABLEDESCRIPTION"] = "Description"

	type column map[string]interface{}

	column1 := column{"COLUMNNAME": "Col1", "DATATYPE": "PLAIN"}
	column2 := column{"COLUMNNAME": "Col2", "DATATYPE": "NUMBER"}

	var columns []column
	columns = append(columns, column1, column2)

	tableDesign["COLUMNS"] = columns

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateTable(tableDesign)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CopyViews(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	destworkspaceid := "1148746000002449012"
	viewids := [2]string{}
	viewids[0] = "1148746000002449007"
	viewids[1] = "1148746000002449008"
	destorgid := ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CopyViews(viewids, destworkspaceid, config, destorgid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetGroups(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetGroups()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateGroup(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	var groupname = "API Group"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateGroup(groupname, emailids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetSlideshows(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetSlideshows()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateSlideshow(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	slidename := "Go Slide"
	viewids := [1]string{}
	viewids[0] = ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateSlideshow(slidename, viewids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func EnableDomainAccess(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.EnableDomainAccess()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DisableDomainAccess(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DisableDomainAccess()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetShareInfo(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, err := workspace.GetShareInfo()
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ShareViews(ac ZAnalytics.Client) {

	viewids := [1]string{}
	viewids[0] = "35130000001354002"

	emailids := [1]string{}
	emailids[0] = "user+1@zohotest.com"

	permissions := map[string]bool{}
	permissions["read"] = true

	config := map[string]interface{}{}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.ShareViews(viewids, emailids, permissions, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveShare(ac ZAnalytics.Client) {

	viewids := [1]string{}
	viewids[0] = "35130000001354002"

	emailids := [1]string{}
	emailids[0] = "user+1@zohotest.com"

	config := map[string]interface{}{}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.RemoveShare(viewids, emailids, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetSharedDetailsForViews(ac ZAnalytics.Client) {

	viewids := [1]string{}
	viewids[0] = "35130000001354002"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetSharedDetailsForViews(viewids)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RenameView(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	newviewname := "New view name"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.Rename(newviewname, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteView(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.Delete(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func SaveAsView(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	newviewname := "New view name"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.SaveAs(newviewname, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CopyFormulas(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	destworkspaceid := ""
	formulanames := [2]string{}
	formulanames[0] = "F1"
	formulanames[1] = "F2"
	destorgid := ""
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.CopyFormulas(formulanames, destworkspaceid, config, destorgid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddFavoriteView(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.AddFavorite()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveFavoriteView(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RemoveFavorite()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func CreateSimilarViews(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	refviewid := "1148746000002449002"
	folderid := "1148746000002508116"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.CreateSimilarViews(refviewid, folderid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AutoAnalyseView(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.AutoAnalyse(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func CreateVariable(ac ZAnalytics.Client) {
	variablename := "Variable_1"
	variabledatatype := 1
	variabletype := 3

	values_1 := [2]string{}
	values_1[0] = "1"
	values_1[1] = "2"

	emailids_1 := [1]string{}
	emailids_1[0] = "user+1@zoho.com"

	dataset_1 := map[string]interface{}{}
	dataset_1["values"] = values_1
	dataset_1["emailIds"] = emailids_1

	values_2 := [2]string{}
	values_2[0] = "3"
	values_2[1] = "4"

	emailids_2 := [1]string{}
	emailids_2[0] = "user+2@zoho.com"

	dataset_2 := map[string]interface{}{}
	dataset_2["values"] = values_2
	dataset_2["emailIds"] = emailids_2

	userspecificdata := [2]map[string]interface{}{}
	userspecificdata[0] = dataset_1
	userspecificdata[1] = dataset_2

	format := map[string]interface{}{}
	format["alignment"] = "left"

	config := map[string]interface{}{}
	config["userSpecificData"] = userspecificdata
	config["format"] = format

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateVariable(variablename, variabledatatype, variabletype, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateVariable(ac ZAnalytics.Client) {
	variableid := "1767024000004594001"
	variablename := "Variable_11"
	variabledatatype := 1
	variabletype := 3

	values_1 := [2]string{}
	values_1[0] = "1"
	values_1[1] = "2"

	emailids_1 := [1]string{}
	emailids_1[0] = "user+1@zoho.com"

	dataset_1 := map[string]interface{}{}
	dataset_1["values"] = values_1
	dataset_1["emailIds"] = emailids_1

	values_2 := [2]string{}
	values_2[0] = "3"
	values_2[1] = "4"

	emailids_2 := [1]string{}
	emailids_2[0] = "user+2@zoho.com"

	dataset_2 := map[string]interface{}{}
	dataset_2["values"] = values_2
	dataset_2["emailIds"] = emailids_2

	userspecificdata := [2]map[string]interface{}{}
	userspecificdata[0] = dataset_1
	userspecificdata[1] = dataset_2

	format := map[string]interface{}{}
	format["alignment"] = "left"

	config := map[string]interface{}{}
	config["userSpecificData"] = userspecificdata
	config["format"] = format

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UpdateVariable(variableid, variablename, variabledatatype, variabletype, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func DeleteVariable(ac ZAnalytics.Client) {
	variableid := "1767024000004592001"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteVariable(variableid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func GetVariableDetails(ac ZAnalytics.Client) {
	variableid := "1767024000004594001"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetVariableDetails(variableid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetVariables(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetVariables()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func MakeDefaultFolder(ac ZAnalytics.Client) {
	folderid := "1767024000004595001"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.MakeDefaultFolder(folderid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func GetDatasources(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetDatasources()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func SyncData(ac ZAnalytics.Client) {
	datasourceid := "1767024000004595194"
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.SyncData(datasourceid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func UpdateDatasourceConnection(ac ZAnalytics.Client) {
	datasourceid := "1767024000003890005"
	config := map[string]interface{}{}
	config["serviceName"] = "AMAZON RDS"
	config["databaseType"] = "MYSQL"
	config["hostName"] = "analyticsmysql1.cgemfx0ey69x.ap-south-1.rds.amazonaws.com"
	config["port"] = "3306"
	config["userName"] = "*apiuser"
	config["password"] = "swim2021"
	config["cloudDatabaseName"] = "sampledb"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UpdateDatasourceConnection(datasourceid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func RefetchData(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RefetchData(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func GetLastImportDetails(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetLastImportDetails()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetMyPermissions(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetMyPermissions()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetViewUrl(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetViewUrl(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetEmbedUrl(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetEmbedUrl(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetPrivateUrl(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetPrivateUrl(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreatePrivateUrl(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.CreatePrivateUrl(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RemovePrivateAccess(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RemovePrivateAccess()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func MakeViewPublic(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.MakeViewPublic(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RemovePublicAccess(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RemovePublicAccess()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetPublishConfigurations(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetPublishConfigurations()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdatePublishConfigurations(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	config := map[string]interface{}{}
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

	exception := view.UpdatePublishConfigurations(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	columnname := "Added Column"
	datatype := "NUMBER"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.AddColumn(columnname, datatype, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func HideColumns(ac ZAnalytics.Client) {
	columnids := [2]string{}
	columnids[0] = "1148746000002449007"
	columnids[1] = "1148746000002449008"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.HideColumns(columnids)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ShowColumns(ac ZAnalytics.Client) {
	columnids := [2]string{}
	columnids[0] = "1148746000002449007"
	columnids[1] = "1148746000002449008"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.ShowColumns(columnids)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ImportDataInNewTable(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	tablename := "v2 go library"
	filetype := "json"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.json"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportDataInNewTable(tablename, filetype, autoidentify, filepath, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportData(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	importtype := "append"
	filetype := "csv"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportData(viewId, importtype, filetype, autoidentify, filepath, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportRawDataInNewTable(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	tablename := "v2 go raw import"
	filetype := "json"
	autoidentify := "true"
	data := `[{"Date":"06 February, 2017","Region":"West","Product":"Fruits and Vegetables","Sales":1682},{"Date":"08 February, 2017","Region":"East","Product":"Clocks","Sales":272}]`
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportRawDataInNewTable(tablename, filetype, autoidentify, data, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportRawData(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	importtype := "append"
	filetype := "json"
	autoidentify := "true"
	data := `[{"Date":"06 February, 2017","Region":"West","Product":"Fruits and Vegetables","Sales":1682},{"Date":"08 February, 2017","Region":"East","Product":"Clocks","Sales":272}]`
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportRawData(viewId, importtype, filetype, autoidentify, data, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportBulkDataInNewTable(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	tablename := "go lang bulk import"
	filetype := "csv"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportBulkDataInNewTable(tablename, filetype, autoidentify, filepath, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportBulkData(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	importtype := "truncateadd"
	filetype := "csv"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportBulkData(viewId, importtype, filetype, autoidentify, filepath, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportBulkDataAsBatches(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	importtype := "truncateadd"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportBulkDataAsBatches(viewId, importtype, autoidentify, filepath, 50000, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ImportBulkDataInNewTableAsBatches(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	tablename := "Sales"
	autoidentify := "true"
	filepath := "/home/local/admin/Files/Sales.csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.ImportBulkDataInNewTableAsBatches(tablename, autoidentify, filepath, 5, config)

	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetImportJobDetails(ac ZAnalytics.Client) {
	jobid := "35130000001345001"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.GetImportJobDetails(jobid)

	if err != nil {
		fmt.Println(err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ExportData(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	responseformat := "pdf"
	filepath := "/home/local/admin/Files/Sales.pdf"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	exception := bulk.ExportData(viewId, responseformat, filepath, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func InitiateBulkExport(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	responseformat := "pdf"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.InitiateBulkExport(viewId, responseformat, config)

	if err != nil {
		fmt.Println(err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func InitiateBulkExportUsingSQL(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	sqlquery := "select * from Sales"
	responseformat := "csv"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.InitiateBulkExportUsingSQL(sqlquery, responseformat, config)

	if err != nil {
		fmt.Println(err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetExportJobDetails(ac ZAnalytics.Client) {
	jobid := "35130000001412003"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	result, err := bulk.GetExportJobDetails(jobid)

	if err != nil {
		fmt.Println(err.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func ExportBulkData(ac ZAnalytics.Client) {
	jobid := "35130000001412003"
	filepath := "/home/local/admin/Files/Sales.pdf"
	bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
	exception := bulk.ExportBulkData(jobid, filepath)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func UpdateSlideshow(ac ZAnalytics.Client) {
	slideid := ""

	config := map[string]interface{}{}
	slidename := ""
	viewids := [1]string{}
	viewids[0] = ""

	config["slideName"] = slidename
	config["viewIds"] = viewids
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UpdateSlideshow(slideid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteSlideshow(ac ZAnalytics.Client) {
	slideid := ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteSlideshow(slideid)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetSlideshowUrl(ac ZAnalytics.Client) {
	slideid := "35130000001396003"
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetSlideshowUrl(slideid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetSlideshowDetails(ac ZAnalytics.Client) {
	slideid := "35130000001396003"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetSlideshowDetails(slideid)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RenameFolder(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	folderid := "35130000001400167"
	foldername := "Renamed Go Folder"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RenameFolder(folderid, foldername, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteFolder(ac ZAnalytics.Client) {
	folderid := "35130000001400167"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteFolder(folderid)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetGroupDetails(ac ZAnalytics.Client) {
	groupid := "35130000001408001"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetGroupDetails(groupid)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func RenameGroup(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	groupid := "1148746000002506003"
	var groupname = "Renamed API Group"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RenameGroup(groupid, groupname, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func AddGroupMembers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+2@zohotest.com"
	groupid := "1148746000002506005"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.AddGroupMembers(groupid, emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveGroupMembers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+2@zohotest.com"
	groupid := "1148746000002506005"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RemoveGroupMembers(groupid, emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteGroup(ac ZAnalytics.Client) {
	groupid := "1148746000002506005"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteGroup(groupid)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func CreateWorkspace(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	workspacename := "Go Lib"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.CreateWorkspace(workspacename, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetOrgAdmins(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetAdmins()

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetMetaDetails(ac ZAnalytics.Client) {
	workspaceName := "Workspace"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetMetaDetails(workspaceName, "")

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetSubscriptionDetails(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetSubscriptionDetails()

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetUsers(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetUsers()

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+adduser@zohotest.com"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.AddUsers(emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ActivateUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+adduser@zohotest.com"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.ActivateUsers(emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeactivateUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+adduser@zohotest.com"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.DeactivateUsers(emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+adduser@zohotest.com"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.RemoveUsers(emailids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeUserRole(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "user+1@zohotest.com"
	role := "VIEWER"
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.ChangeUserRole(emailids, role, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetFormulaColumns(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetFormulaColumns()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddFormulaColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaname := "New Formula"
	expression := ""
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.AddFormulaColumn(formulaname, expression, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func EditFormulaColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaid := "1148746000002515001"
	expression := ""
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.EditFormulaColumn(formulaid, expression, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteFormulaColumn(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaid := "1148746000002515001"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.DeleteFormulaColumn(formulaid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetAggregateFormulas(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetAggregateFormulas()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddAggregateFormula(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaname := "New Formula"
	expression := ""
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.AddAggregateFormula(formulaname, expression, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func EditAggregateFormula(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaid := "1148746000002515001"
	expression := ""
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.EditAggregateFormula(formulaid, expression, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteAggregateFormula(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	formulaid := "1148746000002515001"
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.DeleteAggregateFormula(formulaid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeFolderHierarchy(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	folderid := "35130000001400167"
	hierarchy := 0
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.ChangeFolderHierarchy(folderid, hierarchy, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeFolderPosition(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	folderid := "35130000001400167"
	referencefolderid := "35130000001400165"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.ChangeFolderPosition(folderid, referencefolderid, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func MoveViewsToFolder(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	folderid := "35130000001400167"
	viewids := [2]string{}
	viewids[0] = "1148746000002449007"
	viewids[1] = "1148746000002449008"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.MoveViewsToFolder(folderid, viewids, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetViewDependents(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetViewDependents()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetColumnDependents(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	columnid := "35130000001400167"
	result, exception := view.GetColumnDependents(columnid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateSharedDetails(ac ZAnalytics.Client) {

	emailids := [1]string{}
	emailids[0] = "user+1@zohotest.com"

	permissions := map[string]bool{}
	permissions["read"] = true

	config := map[string]interface{}{}
	config["emailIds"] = emailids
	config["permissions"] = permissions

	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	err := view.UpdateSharedDetails(config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetResourceDetails(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetResourceDetails()

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceUsers(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetWorkspaceUsers()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func AddWorkspaceUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	role := "USER"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.AddWorkspaceUsers(emailids, role, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func RemoveWorkspaceUsers(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.RemoveWorkspaceUsers(emailids, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeWorkspaceUserStatus(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	operation := "activate"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.ChangeWorkspaceUserStatus(emailids, operation, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeWorkspaceUserRole(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	emailids := [1]string{}
	emailids[0] = "sampleuser+1@zohotest.com"
	role := "WORKSPACEADMIN"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.ChangeWorkspaceUserRole(emailids, role, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func CreateQueryTable(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	sqlquery := ""
	querytablename := ""

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.CreateQueryTable(sqlquery, querytablename, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func EditQueryTable(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	sqlquery := ""
	viewid := "35130000001400167"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.EditQueryTable(viewid, sqlquery, config)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ExportAsTemplate(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	viewids := [2]string{}
	viewids[0] = "1148746000002449007"
	viewids[1] = "1148746000002449008"
	filepath := "/home/local/admin/Files/SalesViews.atpt"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.ExportAsTemplate(viewids, filepath, config)

	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetEmailSchedules(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetEmailSchedules()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateEmailSchedule(ac ZAnalytics.Client) {

	schedulename := "Schedule1"
	format := "CSV"
	viewids := []int64{1148746000002578004, 1148746000002578002}
	emailids := []string{"user_1@zoho.com"}

	scheduledetails := map[string]interface{}{
		"calendarFrequency": "Daily",
		"hour":              10,
		"minute":            30,
	}

	config := map[string]interface{}{
		"subject": "Daily Sales Report",
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.CreateEmailSchedule(schedulename, viewids, format, emailids, scheduledetails, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateEmailSchedule(ac ZAnalytics.Client) {
	scheduleid := "115674600000150007"

	scheduledetails := map[string]interface{}{
		"calendarFrequency": "Daily",
		"hour":              8,
		"minute":            30,
	}

	config := map[string]interface{}{
		"subject":         "Daily Sales Overview",
		"scheduleDetails": scheduledetails,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.UpdateEmailSchedule(scheduleid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func TriggerEmailSchedule(ac ZAnalytics.Client) {
	scheduleid := "115674600000150007"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.TriggerEmailSchedule(scheduleid)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func ChangeEmailScheduleStatus(ac ZAnalytics.Client) {
	scheduleid := "115674600000150007"
	operation := "deactivate"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.ChangeEmailScheduleStatus(scheduleid, operation)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func DeleteEmailSchedule(ac ZAnalytics.Client) {
	scheduleid := "115674600000150007"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	err := workspace.DeleteEmailSchedule(scheduleid)
	if err != nil {
		fmt.Println("Error - " + err.ErrorMessage)
	} else {
		fmt.Println("success")
	}
}

func GetAggregateFormulasInWorkspace(ac ZAnalytics.Client) {
	var config map[string]interface{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAggregateFormulas(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetAggregateFormulaDependents(ac ZAnalytics.Client) {
	formulaid := "115674600000150007"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAggregateFormulaDependents(formulaid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetAggregateFormulaValue(ac ZAnalytics.Client) {
	formulaid := "115674600000150007"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAggregateFormulaValue(formulaid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateReport(ac ZAnalytics.Client) {

	basetablename := "Sales"

	xaxis := map[string]interface{}{
		"type":       "xAxis",
		"columnName": "Date",
		"operation":  "year",
	}

	yaxis := map[string]interface{}{
		"type":       "yAxis",
		"columnName": "Sales",
		"operation":  "sum",
	}

	axiscolumns := []map[string]interface{}{xaxis, yaxis}

	config := map[string]interface{}{
		"baseTableName": basetablename,
		"title":         "New Chart",
		"reportType":    "chart",
		"axisColumns":   axiscolumns,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	viewid, exception := workspace.CreateReport(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(viewid)
	}
}

func UpdateReport(ac ZAnalytics.Client) {

	viewid := "35130000006299001"

	xaxis := map[string]interface{}{
		"type":       "xAxis",
		"columnName": "Date",
		"operation":  "year",
	}

	yaxis := map[string]interface{}{
		"type":       "yAxis",
		"columnName": "Cost",
		"operation":  "sum",
	}

	axiscolumns := []map[string]interface{}{xaxis, yaxis}

	config := map[string]interface{}{
		"title":       "New Chart - Updated",
		"reportType":  "chart",
		"axisColumns": axiscolumns,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UpdateReport(viewid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println("Success")
	}
}

func GetTableMetadata(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	result, exception := view.GetTableMetadata()
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func ReorderColumns(ac ZAnalytics.Client) {
	columnIDs := []interface{}{
		"466206000000073013",
		"466206000000069003",
		"466206000000073014",
	}

	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	exception := view.ReorderColumns(columnIDs, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("success")
}

func SortDataByColumns(ac ZAnalytics.Client) {
	columnIDs := []interface{}{
		"466206000000073013",
		"466206000000073014",
	}

	sortOrder := 2 // 1 for ascending, 2 for descending

	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	exception := view.SortDataByColumns(columnIDs, sortOrder, false, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("success")
}

func SortDataByColumnsReset(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	exception := view.SortDataByColumns(nil, 0, true, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("success")
}

func GetQueryTableDetails(ac ZAnalytics.Client) {
	queryTableID := "466206000000061149"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetQueryTableDetails(queryTableID)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func GetAutoMLAnalysisInOrg(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)

	result, exception := org.GetAutoMLAnalysis()
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func GetAutoMLAnalysisInWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetAutoMLAnalysis()
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func GetAutoMLAnalysisDetails(ac ZAnalytics.Client) {
	analysisID := "466206000000061115"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetAutoMLAnalysisDetails(analysisID)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func GetDeploymentDetails(ac ZAnalytics.Client) {
	analysisID := "466206000000061115"
	modelID := "466206000000061119"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetDeploymentDetails(analysisID, modelID)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println(result)
}

func CreateAutoMLAnalysis(ac ZAnalytics.Client) {
	automlName := "Sales Analysis - Go SDK"
	trainingTableID := "466206000000061002"
	predictionType := "CLASSIFICATION"

	features := []interface{}{
		"Region",
		"Product Category",
		"Sales",
	}

	serverOption := 1

	algorithms := map[string]interface{}{
		"decisionTreeClassification": map[string]interface{}{
			"minimumSampleSplit": "2",
			"maximumDepth":       "100",
		},
		"randomForestClassification": map[string]interface{}{
			"minimumSampleSplit": "2",
			"maximumDepth":       "100",
			"numberOfTrees":      "25",
		},
	}

	config := map[string]interface{}{
		"description":  "Sales Table Analysis...",
		"targetColumn": "Product",
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	automlID, exception := workspace.CreateAutoMLAnalysis(
		automlName,
		trainingTableID,
		predictionType,
		features,
		serverOption,
		algorithms,
		config,
	)

	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("Created AutoML Analysis ID:", automlID)
}

func DeleteAutoMLAnalysis(ac ZAnalytics.Client) {
	analysisID := "466206000000100001"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.DeleteAutoMLAnalysis(analysisID, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Printf("AutoML Analysis %s deleted successfully.\n", analysisID)
}

func DeleteAutoMLAnalysisModel(ac ZAnalytics.Client) {
	analysisID := "466206000000061115"
	modelID := "466206000000061117"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.DeleteAutoMLAnalysisModel(analysisID, modelID, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Printf("Model %s from AutoML Analysis %s deleted successfully.\n", modelID, analysisID)
}

func CreateAutoMLDeployment(ac ZAnalytics.Client) {
	analysisID := "466206000000100001"
	modelID := "466206000000073003"

	inputTableID := "466206000000061002"
	outputTable := "SalesDep"

	outputColumns := []interface{}{
		"Sales",
		"Region",
	}

	predictionColumn := "precol"
	serverOption := 1
	importType := "APPEND"

	scheduleDetails := map[string]interface{}{
		"calendarFrequency": "hourly",
		"interval":          3,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	deploymentInfo, exception := workspace.CreateAutoMLAnalysisDeployment(
		analysisID,
		modelID,
		inputTableID,
		outputTable,
		outputColumns,
		predictionColumn,
		serverOption,
		importType,
		scheduleDetails,
		nil,
	)

	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("Deployment Details:", deploymentInfo)
}

func DeployAutoMLAnalysis(ac ZAnalytics.Client) {
	analysisID := "466206000000073001"
	deploymentID := "466206000000073057"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.DeployAutoMLAnalysis(analysisID, deploymentID, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
}

func DeleteAutoMLAnalysisDeployment(ac ZAnalytics.Client) {
	analysisID := "466206000000073001"
	deploymentID := "466206000000073057"

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.DeleteAutoMLAnalysisDeployment(analysisID, deploymentID, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
}

func AutoMLAnalysisPrediction(ac ZAnalytics.Client) {
	analysisID := "466206000000073001"
	modelID := "466206000000073003"

	features := map[string]interface{}{
		"Sales":            1000,
		"Region":           "East",
		"Product Category": "Stationery",
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	predictionResult, exception := workspace.AutoMLAnalysisPrediction(
		analysisID,
		modelID,
		features,
		nil,
	)

	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}

	fmt.Println("Prediction Result:")
	fmt.Println(predictionResult)
}

func GetTags(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetTags()
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println(result)
}

func CreateTag(ac ZAnalytics.Client) {
	tagName := "Sales Tag"
	colorCode := "#FF5733"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	tagId, exception := workspace.CreateTag(tagName, colorCode, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("Created Tag ID:", tagId)
}

func UpdateTag(ac ZAnalytics.Client) {
	tagId := ""
	config := map[string]interface{}{
		"name":      "Sales Tag Updated",
		"colorCode": "#33FF57",
	}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UpdateTag(tagId, config)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func DeleteTag(ac ZAnalytics.Client) {
	tagId := ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteTag(tagId)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func AddTagToViews(ac ZAnalytics.Client) {
	tagId := ""
	viewIds := []string{viewId}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.AddTagToViews(tagId, viewIds, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func RemoveTagFromViews(ac ZAnalytics.Client) {
	tagId := ""
	viewIds := []string{viewId}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RemoveTagFromViews(tagId, viewIds, false, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func GetTaggedViews(ac ZAnalytics.Client) {
	tagId := ""
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetTaggedViews(tagId)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println(result)
}

func GetViewTags(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetViewTags()
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println(result)
}

func AddTagsToView(ac ZAnalytics.Client) {
	tagIds := []string{""}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.AddTagsToView(tagIds, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func RemoveTagsFromView(ac ZAnalytics.Client) {
	tagIds := []string{""}
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	exception := view.RemoveTagsFromView(tagIds, false, nil)
	if exception != nil {
		fmt.Println("Error:", exception)
		return
	}
	fmt.Println("success")
}

func GetCustomRoles(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetCustomRoles()
	if exception != nil {
		fmt.Println("Error:", exception.ErrorMessage)
		return
	}
	fmt.Println(result)
}

func CreateCustomRole(ac ZAnalytics.Client) {
	roleName := "DashboardPowerUser"
	// Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
	accessType := "ALL_DASHBOARDS"
	permissions := map[string]interface{}{
		"interactionPermissions": map[string]interface{}{
			"read":      true,
			"vud":       true,
			"drillDown": true,
			"insight":   true,
		},
		"sharePermissions": map[string]interface{}{
			"discussion":   true,
			"privateLinks": true,
		},
		"publishPermissions": map[string]interface{}{
			"export": true,
		},
	}

	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	roleId, exception := org.CreateCustomRole(roleName, accessType, permissions, nil)
	if exception != nil {
		fmt.Println("Error:", exception.ErrorMessage)
		return
	}
	fmt.Println("Created Custom Role ID:", roleId)
}

func UpdateCustomRole(ac ZAnalytics.Client) {
	roleId := ""
	roleName := "DashboardPowerUser"
	// Allowed values for accessType: "ALL_DATA_REPORTS_AND_DASHBOARDS", "ALL_REPORTS_AND_DASHBOARDS", "ALL_DASHBOARDS"
	accessType := "ALL_DASHBOARDS"
	permissions := map[string]interface{}{
		"interactionPermissions": map[string]interface{}{
			"read":      true,
			"vud":       true,
			"drillDown": false,
			"insight":   false,
		},
		"sharePermissions": map[string]interface{}{
			"share":        true,
			"privateLinks": false,
		},
		"publishPermissions": map[string]interface{}{
			"export": true,
		},
	}

	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.UpdateCustomRole(roleId, roleName, accessType, permissions, nil)
	if exception != nil {
		fmt.Println("Error:", exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func DeleteCustomRole(ac ZAnalytics.Client) {
	roleId := ""
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.DeleteCustomRole(roleId)
	if exception != nil {
		fmt.Println("Error:", exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func GetQueryTables(ac ZAnalytics.Client) {
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetQueryTables(config)
	if exception != nil {
		fmt.Println("Error:", exception.ErrorMessage)
		return
	}
	fmt.Println(result)
}

func GetDashboards(ac ZAnalytics.Client) {
	result, exception := ac.GetDashboards()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetOwnedDashboards(ac ZAnalytics.Client) {
	result, exception := ac.GetOwnedDashboards()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetSharedDashboards(ac ZAnalytics.Client) {
	result, exception := ac.GetSharedDashboards()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetAlertsInView(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetAlertsInView()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetViewMetadataForAlert(ac ZAnalytics.Client) {
	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
	result, exception := view.GetViewMetadataForAlert()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateAlert(ac ZAnalytics.Client) {

	alertname := "Sales Drop Alert"

	scheduledetails := map[string]interface{}{
		"calendarFrequency": "daily",
		"hour":              9,
		"minute":            0,
	}

	rules := []interface{}{
		map[string]interface{}{
			"operator":        "lt",
			"viewColumnIndex": "2",
			"type":            "constant",
			"values":          []string{"1000"},
		},
	}

	config := map[string]interface{}{
		"email": map[string]interface{}{
			"notifyAdmins": true,
			"subject":      "Sales dropped below threshold",
			"message":      "Please review the report.",
		},
	}

	view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)

	result, exception := view.CreateAlert(alertname, scheduledetails, rules, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetAlertsInWorkspace(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAlertsInWorkspace()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetAlertConfiguration(ac ZAnalytics.Client) {
	alertid := "35130000001056611"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetAlertConfiguration(alertid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateAlert(ac ZAnalytics.Client) {

	alertid := "35130000001056611"
	alertname := "Sales Drop Alert (weekly)"

	scheduledetails := map[string]interface{}{
		"calendarFrequency": "weekly",
		"hour":              9,
		"minute":            30,
		"weekDays":          []int{6},
		"timeZone":          "Asia/Kolkata",
	}

	rules := []interface{}{
		map[string]interface{}{
			"operator":        "lt",
			"viewColumnIndex": "2",
			"type":            "constant",
			"values":          []string{"1000"},
		},
	}

	config := map[string]interface{}{
		"email": map[string]interface{}{
			"notifyAdmins": true,
			"emailIds":     []string{"finance@example.com"},
			"subject":      "Weekly sales monitor",
			"message":      "Weekly alert summary.",
		},
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.UpdateAlert(alertid, alertname, scheduledetails, rules, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func DeleteAlerts(ac ZAnalytics.Client) {
	alertids := []string{"137687000010815003", "137687000010815005"}
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DeleteAlerts(alertids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func ChangeAlertStatus(ac ZAnalytics.Client) {
	alertids := []string{"137687000010815003", "137687000010815005"}
	enabled := false
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.ChangeAlertStatus(alertids, enabled, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func RunAlert(ac ZAnalytics.Client) {
	alertid := "35130000001056611"
	config := map[string]interface{}{
		"validateSystemTags": false,
	}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.RunAlert(alertid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func GetAlertEvents(ac ZAnalytics.Client) {

	alertid := "35130000001056611"

	config := map[string]interface{}{
		"fromDate":       "2026-05-01 00:00:00",
		"toDate":         "2026-05-31 23:59:59",
		"status":         []string{"triggered", "error"},
		"pageNo":         1,
		"recordsPerPage": 50,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetAlertEvents(alertid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetLinkedWorkspaces(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetLinkedWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetLinkedWorkspacesForOrg(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetLinkedWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetLinkableWorkspaces(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetLinkableWorkspaces()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceLinkingCompatibility(ac ZAnalytics.Client) {

	clients := []interface{}{
		map[string]interface{}{
			"orgId":        "700000654321",
			"workspaceIds": []string{"466206000000071000"},
		},
	}

	config := map[string]interface{}{}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.GetWorkspaceLinkingCompatibility(clients, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func LinkWorkspaces(ac ZAnalytics.Client) {

	clients := []interface{}{
		map[string]interface{}{
			"orgId":        "700000654321",
			"workspaceIds": []string{"466206000000071000"},
		},
	}

	config := map[string]interface{}{}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.LinkWorkspaces(clients, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func UnlinkWorkspaces(ac ZAnalytics.Client) {
	scope := "ALL"
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.UnlinkWorkspaces(scope, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func SyncLinkedWorkspaces(ac ZAnalytics.Client) {
	scope := "ALL"
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.SyncLinkedWorkspaces(scope, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func GetLinkedWorkspaceSyncDetails(ac ZAnalytics.Client) {
	sandboxids := []string{"137687000012345001", "137687000012345002"}
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetLinkedWorkspaceSyncDetails(sandboxids, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceBackups(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetWorkspaceBackups()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func BackupWorkspaceNow(ac ZAnalytics.Client) {
	config := map[string]interface{}{
		"backupMode": "STRUCTURE",
	}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.BackupWorkspaceNow(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceBackupStatus(ac ZAnalytics.Client) {
	backupid := "35130000001056701"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetWorkspaceBackupStatus(backupid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func DownloadWorkspaceBackup(ac ZAnalytics.Client) {
	backupid := "35130000001056701"
	filepath := "/home/user/workspace-backup.zip"
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	exception := workspace.DownloadWorkspaceBackup(backupid, filepath, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func RestoreWorkspaceFromBackup(ac ZAnalytics.Client) {
	backupid := "35130000001056701"
	confirmrestore := true
	config := map[string]interface{}{}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.RestoreWorkspaceFromBackup(backupid, confirmrestore, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetWorkspaceRestoreStatus(ac ZAnalytics.Client) {
	restoreid := "35130000001056801"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetWorkspaceRestoreStatus(restoreid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func CreateDashboard(ac ZAnalytics.Client) {

	displayname := "Sales Overview"
	layout := `{"1":{"type":"USERFILTERS","width":80,"height":3,"left":0,"top":0},"2":{"type":"HTML","width":80,"height":5,"left":0,"top":3,"content":"<b>Sales Dashboard</b>"},"3":{"type":"VIEW","width":80,"height":20,"left":0,"top":8,"viewName":"Sales Chart","properties":{}}}`

	config := map[string]interface{}{
		"settings": map[string]interface{}{
			"allowDrillDown": "true",
			"fitToWidth":     "true",
		},
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	result, exception := workspace.CreateDashboard(displayname, layout, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateDashboard(ac ZAnalytics.Client) {

	dashboardid := "35130000001055801"
	layout := `{"1":{"type":"USERFILTERS","width":80,"height":3,"left":0,"top":0},"2":{"type":"HTML","width":80,"height":5,"left":0,"top":3,"content":"<b>Updated Title</b>"},"3":{"type":"VIEW","width":80,"height":20,"left":0,"top":8,"viewName":"Sales Chart","properties":{}}}`

	config := map[string]interface{}{
		"layout": layout,
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.UpdateDashboard(dashboardid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func GetDashboardMetadata(ac ZAnalytics.Client) {
	dashboardid := "35130000001055801"
	config := map[string]interface{}{
		"include": "layout",
	}
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetDashboardMetadata(dashboardid, config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetReportMetadata(ac ZAnalytics.Client) {
	reportid := "35130000001055901"
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetReportMetadata(reportid)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func GetOrgAccessRestrictions(ac ZAnalytics.Client) {
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	result, exception := org.GetOrgAccessRestrictions()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateOrgAccessRestrictions(ac ZAnalytics.Client) {
	config := map[string]interface{}{
		"accessRestrictionEnabled": true,
	}
	org := ZAnalytics.GetOrgInstance(&ac, orgId)
	exception := org.UpdateOrgAccessRestrictions(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func GetWorkspaceAccessRestrictions(ac ZAnalytics.Client) {
	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
	result, exception := workspace.GetWorkspaceAccessRestrictions()
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
	} else {
		fmt.Println(result)
	}
}

func UpdateWorkspaceAccessRestrictions(ac ZAnalytics.Client) {

	config := map[string]interface{}{
		"useOrganizationSettings": false,
		"shareViews": map[string]interface{}{
			"domainRestrictionEnabled": true,
			"trustedDomains":           []string{"example.com", "partner.example.org"},
		},
		"privateLinks": map[string]interface{}{"enabled": false},
		"publicViews":  map[string]interface{}{"enabled": false},
		"exportViews":  map[string]interface{}{"enabled": true},
	}

	workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

	exception := workspace.UpdateWorkspaceAccessRestrictions(config)
	if exception != nil {
		fmt.Println(exception.ErrorMessage)
		return
	}
	fmt.Println("success")
}

func main() {

	ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
	CreateEmailSchedule(ac)

}
