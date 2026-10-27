/*$Id$*/
var analyticsClient = require('./AnalyticsClient');

/*
 * Sample output helper. The SDK never writes to stdout itself; this exists only so the
 * examples below can show what each call returned.
 */
function log(value) {
    var text = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
    process.stdout.write(text + '\n');
}

var clientId = '';
var clientSecret = '';
var refreshtoken = '';

var orgId = '';

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var org = ac.getOrgInstance(orgId);
org.getUsers().then((response) => {
    //log(response);

    }).catch((error) => {
        //log('errorCode : '+error.errorCode);
        //log('errorMessage : '+error.errorMessage);
});

var workspaceId = '';
var viewId = '';

function getAlertsInView() {
    var view = ac.getViewInstance(orgId, workspaceId, viewId);
    view.getAlertsInView().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getViewMetadataForAlert() {
    var view = ac.getViewInstance(orgId, workspaceId, viewId);
    view.getViewMetadataForAlert().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function createAlert() {
    var alertName = 'Sales Drop Alert';

    var scheduleDetails = {
        'calendarFrequency': 'daily',
        'hour': 9,
        'minute': 0
    };

    var rules = [
        {
            'operator': 'lt',
            'viewColumnIndex': '2',
            'type': 'constant',
            'values': ['1000']
        }
    ];

    var config = {
        'email': {
            'notifyAdmins': true,
            'subject': 'Sales dropped below threshold',
            'message': 'Please review the report.'
        }
    };

    var view = ac.getViewInstance(orgId, workspaceId, viewId);
    view.createAlert(alertName, scheduleDetails, rules, config).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function refetchData() {
    var config = {
        'userName': 'john@zylker.com',
        'password': 'Zoho@123'
    };

    var view = ac.getViewInstance(orgId, workspaceId, viewId);
    view.refetchData(config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getAlertsInWorkspace() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getAlertsInWorkspace().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getAlertConfiguration() {
    var alertId = '35130000001056611';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getAlertConfiguration(alertId).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function updateAlert() {
    var alertId = '35130000001056611';
    var alertName = 'Sales Drop Alert (weekly)';

    var scheduleDetails = {
        'calendarFrequency': 'weekly',
        'hour': 9,
        'minute': 30,
        'weekDays': [6],
        'timeZone': 'Asia/Kolkata'
    };

    var rules = [
        {
            'operator': 'lt',
            'viewColumnIndex': '2',
            'type': 'constant',
            'values': ['1000']
        }
    ];

    var config = {
        'email': {
            'notifyAdmins': true,
            'emailIds': ['finance@example.com'],
            'subject': 'Weekly sales monitor',
            'message': 'Weekly alert summary.'
        }
    };

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.updateAlert(alertId, alertName, scheduleDetails, rules, config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function deleteAlerts() {
    var alertIds = ['137687000010815003', '137687000010815005'];
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.deleteAlerts(alertIds).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function changeAlertStatus() {
    var alertIds = ['137687000010815003', '137687000010815005'];
    var enabled = false;
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.changeAlertStatus(alertIds, enabled).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function runAlert() {
    var alertId = '35130000001056611';
    var config = { 'validateSystemTags': false };
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.runAlert(alertId, config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getAlertEvents() {
    var alertId = '35130000001056611';

    var config = {
        'fromDate': '2026-05-01 00:00:00',
        'toDate': '2026-05-31 23:59:59',
        'status': ['triggered', 'error'],
        'pageNo': 1,
        'recordsPerPage': 50
    };

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getAlertEvents(alertId, config).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getLinkedWorkspaces() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getLinkedWorkspaces().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getLinkedWorkspacesForOrg() {
    var org = ac.getOrgInstance(orgId);
    org.getLinkedWorkspaces().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getLinkableWorkspaces() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getLinkableWorkspaces().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getWorkspaceLinkingCompatibility() {
    var clients = [
        {
            'orgId': '700000654321',
            'workspaceIds': ['466206000000071000']
        }
    ];

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getWorkspaceLinkingCompatibility(clients).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function linkWorkspaces() {
    var clients = [
        {
            'orgId': '700000654321',
            'workspaceIds': ['466206000000071000']
        }
    ];

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.linkWorkspaces(clients).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function unlinkWorkspaces() {
    var scope = 'ALL';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.unlinkWorkspaces(scope).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function syncLinkedWorkspaces() {
    var scope = 'ALL';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.syncLinkedWorkspaces(scope).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getLinkedWorkspaceSyncDetails() {
    var sandboxIds = ['137687000012345001', '137687000012345002'];
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getLinkedWorkspaceSyncDetails(sandboxIds).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getWorkspaceBackups() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getWorkspaceBackups().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function backupWorkspaceNow() {
    var config = { 'backupMode': 'STRUCTURE' };
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.backupWorkspaceNow(config).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getWorkspaceBackupStatus() {
    var backupId = '35130000001056701';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getWorkspaceBackupStatus(backupId).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function downloadWorkspaceBackup() {
    var backupId = '35130000001056701';
    var filePath = '/home/user/workspace-backup.zip';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.downloadWorkspaceBackup(backupId, filePath).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function restoreWorkspaceFromBackup() {
    var backupId = '35130000001056701';
    var confirmRestore = true;
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.restoreWorkspaceFromBackup(backupId, confirmRestore).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getWorkspaceRestoreStatus() {
    var restoreId = '35130000001056801';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getWorkspaceRestoreStatus(restoreId).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function createDashboard() {
    var displayName = 'Sales Overview';

    var layout = JSON.stringify({
        '1': { 'type': 'USERFILTERS', 'width': 80, 'height': 3, 'left': 0, 'top': 0 },
        '2': { 'type': 'HTML', 'width': 80, 'height': 5, 'left': 0, 'top': 3, 'content': '<b>Sales Dashboard</b>' },
        '3': { 'type': 'VIEW', 'width': 80, 'height': 20, 'left': 0, 'top': 8, 'viewName': 'Sales Chart', 'properties': {} }
    });

    var config = {
        'settings': {
            'allowDrillDown': 'true',
            'fitToWidth': 'true'
        }
    };

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.createDashboard(displayName, layout, config).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function updateDashboard() {
    var dashboardId = '35130000001055801';

    var layout = JSON.stringify({
        '1': { 'type': 'USERFILTERS', 'width': 80, 'height': 3, 'left': 0, 'top': 0 },
        '2': { 'type': 'HTML', 'width': 80, 'height': 5, 'left': 0, 'top': 3, 'content': '<b>Updated Title</b>' },
        '3': { 'type': 'VIEW', 'width': 80, 'height': 20, 'left': 0, 'top': 8, 'viewName': 'Sales Chart', 'properties': {} }
    });

    var config = { 'layout': layout };

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.updateDashboard(dashboardId, config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getDashboardMetadata() {
    var dashboardId = '35130000001055801';
    var config = { 'include': 'layout' };
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getDashboardMetadata(dashboardId, config).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getReportMetadata() {
    var reportId = '35130000001055901';
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getReportMetadata(reportId).then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getOrgAccessRestrictions() {
    var org = ac.getOrgInstance(orgId);
    org.getOrgAccessRestrictions().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function updateOrgAccessRestrictions() {
    var config = { 'accessRestrictionEnabled': true };
    var org = ac.getOrgInstance(orgId);
    org.updateOrgAccessRestrictions(config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function getWorkspaceAccessRestrictions() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.getWorkspaceAccessRestrictions().then((result) => {
        log(result);
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}

function updateWorkspaceAccessRestrictions() {
    var config = {
        'useOrganizationSettings': false,
        'shareViews': {
            'domainRestrictionEnabled': true,
            'trustedDomains': ['example.com', 'partner.example.org']
        },
        'privateLinks': { 'enabled': false },
        'publicViews': { 'enabled': false },
        'exportViews': { 'enabled': true }
    };

    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    workspace.updateWorkspaceAccessRestrictions(config).then(() => {
        log('success');
    }).catch((error) => {
        log('errorCode : ' + error.errorCode + ', errorMessage : ' + error.errorMessage);
    });
}
