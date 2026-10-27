/*$Id$*/
const https = require('https');
const fs = require('fs');
const path = require('path');
const { Readable } = require('stream');
const crypto = require('crypto');
const querystring = require('querystring');
const analyticsURI = "@@ANALYTICS_URL";
const accountsURI = "@@ACCOUNTS_URL";
const clientVersion = "2.10.0";

// Strong TLS options, feature-detected once at module load. On Node < 11.4 the
// `minVersion`/`maxVersion` options don't exist, and `maxVersion: 'TLSv1.3'` on
// a runtime built against OpenSSL < 1.1.1 throws ERR_TLS_INVALID_PROTOCOL_VERSION
// at socket creation time. We only set values the runtime can honour so the
// request goes through over the strongest protocol this Node actually supports
// rather than being rejected.
const STRONG_TLS_CIPHERS = 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305';
const STRONG_TLS_OPTS = (function () {
    var opts = { ciphers: STRONG_TLS_CIPHERS, rejectUnauthorized: true };
    try {
        var tls = require('tls');
        if (typeof tls.DEFAULT_MAX_VERSION === 'string') {
            opts.minVersion = 'TLSv1.2';
            opts.maxVersion = (tls.DEFAULT_MAX_VERSION === 'TLSv1.3') ? 'TLSv1.3' : tls.DEFAULT_MAX_VERSION;
        } else {
            opts.secureProtocol = 'TLSv1_2_method';
        }
    } catch (e) { /* keep cipher + rejectUnauthorized only */ }
    return opts;
})();


// Minimal multipart/form-data encoder built on core modules only, so this client
// runs on a stock Node install with nothing to npm install first. It covers the
// three shapes this client posts: a plain string field, a Buffer with an explicit
// filename, and a streamed file, and exposes the same append/getHeaders/pipe
// surface the rest of the file already uses.
const MIME_BY_EXT = {
    '.csv': 'text/csv',
    '.json': 'application/json',
    '.tsv': 'text/tab-separated-values',
    '.txt': 'text/plain',
    '.xml': 'application/xml'
};

class FormData
{
    constructor()
    {
        this.boundary = '--------------------------' + crypto.randomBytes(12).toString('hex');
        this.parts = [];
    }

    append(name, value, options = {})
    {
        this.parts.push({ name: name, value: value, options: options });
    }

    getHeaders()
    {
        return { 'content-type': 'multipart/form-data; boundary=' + this.boundary };
    }

    partHeader(part)
    {
        const value = part.value;
        const isTextField = (typeof value === 'string');

        let filename = part.options.filename;
        if (filename === undefined && !isTextField && !Buffer.isBuffer(value) && value && value.path) {
            filename = path.basename(String(value.path));
        }

        let header = '--' + this.boundary + '\r\n'
            + 'Content-Disposition: form-data; name="' + escapeHeaderValue(part.name) + '"';

        if (filename !== undefined) {
            header += '; filename="' + escapeHeaderValue(filename) + '"';
        }
        header += '\r\n';

        if (!isTextField) {
            const ext = (filename === undefined) ? '' : path.extname(filename).toLowerCase();
            header += 'Content-Type: ' + (part.options.contentType || MIME_BY_EXT[ext] || 'application/octet-stream') + '\r\n';
        }

        return header + '\r\n';
    }

    async *chunks()
    {
        for (const part of this.parts) {
            yield Buffer.from(this.partHeader(part));

            const value = part.value;
            if (Buffer.isBuffer(value)) {
                yield value;
            } else if (value !== null && typeof value === 'object' && typeof value.pipe === 'function') {
                for await (const chunk of value) {
                    yield Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
                }
            } else {
                yield Buffer.from(String(value));
            }

            yield Buffer.from('\r\n');
        }

        yield Buffer.from('--' + this.boundary + '--\r\n');
    }

    pipe(dest)
    {
        const source = Readable.from(this.chunks());
        // A read error on a file part would otherwise surface as an unhandled
        // 'error' event; hand it to the request so the caller's existing
        // req.on('error') path reports it.
        source.on('error', (err) => dest.destroy(err));
        return source.pipe(dest);
    }
}

function escapeHeaderValue(value)
{
    return String(value).replace(/"/g, '%22').replace(/\r|\n/g, '');
}

class AnalyticsClient
{
    constructor(clientId, clientSecret, refreshToken)
    {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.refreshToken = refreshToken;
        this.accessToken = null;
    }

    /**
     * Returns a new OrgAPI instance.
     * @method getOrgInstance
     * @param {String} orgId - The ID of the organization.
     */
    getOrgInstance(orgId)
    {
        var orgInstance = new OrgAPI(this, orgId);
        return orgInstance;
    }
    
    /**
     * Returns a new WorkspaceAPI instance.
     * @method getWorkspaceInstance
     * @param {String} orgId - The ID of the organization.
     * @param {String} workspaceId - The ID of the workspace.
     */
    getWorkspaceInstance(orgId, workspaceId)
    {
        var workspaceInstance = new WorkspaceAPI(this, orgId, workspaceId);
        return workspaceInstance;
    }

    /**
     * Returns a new ViewAPI instance.
     * @method getViewInstance
     * @param {String} orgId - The ID of the organization.
     * @param {String} workspaceId - The ID of the workspace.
     * @param {String} viewId - The ID of the view.
     */
    getViewInstance(orgId, workspaceId, viewId)
    {
        var viewInstance = new ViewAPI(this, orgId, workspaceId, viewId);
        return viewInstance;
    }

    /**
     * Returns a new BulkAPI instance.
     * @method getBulkInstance
     * @param {String} orgId - The ID of the organization.
     * @param {String} workspaceId - The ID of the workspace.
     */
    getBulkInstance(orgId, workspaceId)
    {
        var bulkInstance = new BulkAPI(this, orgId, workspaceId);
        return bulkInstance;
    }

    sleep(ms)
    {
        return new Promise((resolve) => {
          setTimeout(resolve, ms);
        });
    }

    parseCSV(content, delimiter = ',', quotechar = '"') {
        const rows = [];
        let row = [];
        let field = '';
        let inQuotes = false;
    
        for (let i = 0; i < content.length; i++) {
            const char = content[i];
            const nextChar = content[i + 1];
    
            if (char === quotechar) {
                if (inQuotes && nextChar === quotechar) {
                    field += quotechar; // escaped quote
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (char === delimiter && !inQuotes) {
                row.push(field);
                field = '';
            } else if (char === '\n' && !inQuotes) {
                row.push(field);
                rows.push(row);
                row = [];
                field = '';
            } else {
                field += char;
            }
        }
    
        // last field
        if (field.length || row.length) {
            row.push(field);
            rows.push(row);
        }
    
        return rows;
    }

    stringifyCSV(rows, delimiter = ',', quotechar = '"') 
    {
        return rows.map(row =>
            row.map(field => {
                field = field ?? '';
                if (
                    field.includes(delimiter) ||
                    field.includes('\n') ||
                    field.includes(quotechar)
                ) {
                    return quotechar +
                        field.replaceAll(quotechar, quotechar + quotechar) +
                        quotechar;
                }
                return field;
            }).join(delimiter)
        ).join('\n') + '\n';
    }

    async handleBatchImportRequest(uriPath, config, header, filePath, batchSize, toolConfig = {}) {
        const fs = require('fs');
        const https = require('https');
    
        header['User-Agent'] = 'Analytics NodeJS Client v2_' + clientVersion;
    
        const delimiters = [',', '\t', ';', ' ', '|'];
        const quotedChars = ['\u0000', '\'', '"'];
    
        const delimiter = delimiters[config.delimiter ?? 0];
        const quotechar = quotedChars[config.quoted ?? 2];
        const isFirstRowHeader = toolConfig.isFirstRowHeader !== false;
    
        config.batchKey = 'start';
    
        const fileData = fs.readFileSync(filePath, 'utf8');
    
        const records = this.parseCSV(fileData, delimiter, quotechar);
    
        if (!records.length) return null;
    
        let headers;
        let index = 0;
    
        if (isFirstRowHeader) {
            headers = records[0];
            index = 1;
        } else {
            headers = toolConfig.columnHeaders;
            if (!headers || !headers.length) {
                throw new Error(
                    'columnHeaders cannot be empty when isFirstRowHeader is false'
                );
            }
        }
    
        let jobId;
        let response;
    
        while (index < records.length) {
            const batchRows = records.slice(index, index + batchSize);
            index += batchSize;
    
            const isLastBatch = index >= records.length;
            config.isLastBatch = String(isLastBatch);
    
            const csvBatch = this.stringifyCSV(
                [headers, ...batchRows],
                delimiter,
                quotechar
            );
    
            const encodedConfig = encodeURIComponent(JSON.stringify(config));
            const url = 'https://' + analyticsURI + uriPath + '?CONFIG=' + encodedConfig;
    
            if (!this.accessToken) {
                this.accessToken = await this.getOauth();
            }
    
            try {
                response = await this.sendBatchImportRequest(url, header, csvBatch);
            } catch (err) {
                if (err.errorCode === '8535') {
                    this.accessToken = await this.getOauth();
                    response = await this.sendBatchImportRequest(url, header, csvBatch);
                } else {
                    throw err;
                }
            }
    
            config.batchKey = response.batchKey;
            jobId = response.jobId;
    
            if (!isLastBatch) {
                await this.sleep(2000);
            }
        }
    
        return jobId;
    }
    

    sendBatchImportRequest(url, header, batch) {
        header['Authorization'] = 'Zoho-oauthtoken ' + this.accessToken;

        return new Promise((resolve, reject) => {
            const form = new FormData();
            form.append('FILE', Buffer.from(batch), { filename: 'batch.csv' });

            const requestOptions = {
                method: 'POST',
                headers: {
                    ...header,
                    ...form.getHeaders()
                },
                ...STRONG_TLS_OPTS
            };

            const req = https.request(url, requestOptions, (resp) => {
                let data = '';
                resp.on('data', (chunk) => { data += chunk; });
                resp.on('end', () => {
                    const respJSON = JSON.parse(data);
                    if (resp.statusCode !== 200) {
                        reject(respJSON.data);
                    } else {
                        resolve(respJSON.data);
                    }
                });
            });

            req.on('error', (err) => {
                reject({ errorCode: '0', errorMessage: err.message });
            });

            form.pipe(req);
        });
    }

async handleImportRequest(uriPath, config, header, filePath, data = null) {
    if (this.accessToken == null) {
        this.accessToken = await this.getOauth();
    }
    return await this.sendImportRequest(uriPath, config, header, filePath, data).catch(async error => {
        if (error.errorCode == "8535") {
            this.accessToken = await this.getOauth();
            return await this.sendImportRequest(uriPath, config, header, filePath, data);
        } else {
            throw error;
        }
    });
}

sendImportRequest(uriPath, config, header = {}, filePath, data) {
    header['User-Agent'] = 'Analytics NodeJS Client v2_' + clientVersion;
    header['Authorization'] = 'Zoho-oauthtoken ' + this.accessToken;

    if (config !== null) {
        const encodedConfig = encodeURIComponent(JSON.stringify(config));
        const configParam = "CONFIG=" + encodedConfig;
        uriPath = uriPath + "?" + configParam;
    }

    const url = new URL('https://' + analyticsURI + uriPath);

    return new Promise((resolve, reject) => {
        const form = new FormData();
        if (data !== null) {
            form.append('DATA', data);
        } else {
            const fileStream = fs.createReadStream(filePath);
            fileStream.on('error', reject);
            form.append('FILE', fileStream);
        }

        const options = {
            method: 'POST',
            hostname: url.hostname,
            path: url.pathname + url.search,
            headers: {
                ...header,
                ...form.getHeaders()
            },
            ...STRONG_TLS_OPTS
        };

        const req = https.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => responseData += chunk);
            res.on('end', () => {
                const respJSON = JSON.parse(responseData);
                if (res.statusCode !== 200) {
                    reject(respJSON.data);
                } else {
                    resolve(respJSON.data);
                }
            });
        });

        req.on('error', (err) => reject(JSON.parse(err)));
        form.pipe(req);
    });
}

async handleExportRequest(
    uriPath,
    config,
    header,
    { filePath = null, stream = false } = {}
) {
    if (this.accessToken == null) {
        this.accessToken = await this.getOauth();
    }

    try {
        return await this.sendExportRequest(
            uriPath,
            config,
            header,
            { filePath, stream }
        );
    } catch (error) {
        if (error.errorCode === '8535') {
            this.accessToken = await this.getOauth();
            return await this.sendExportRequest(
                uriPath,
                config,
                header,
                { filePath, stream }
            );
        }
        throw error;
    }
}


sendExportRequest(
    uriPath,
    config,
    header = {},
    { filePath = null, stream = false } = {}
) {
    header['User-Agent'] = 'Analytics NodeJS Client v2_' + clientVersion;
    header['Authorization'] = 'Zoho-oauthtoken ' + this.accessToken;

    if (config) {
        const encodedConfig = encodeURIComponent(JSON.stringify(config));
        uriPath += '?CONFIG=' + encodedConfig;
    }

    return new Promise((resolve, reject) => {
        const url = new URL('https://' + analyticsURI + uriPath);

        const options = {
            method: 'GET',
            hostname: url.hostname,
            path: url.pathname + url.search,
            headers: header,
            ...STRONG_TLS_OPTS
        };

        const req = https.request(options, (res) => {

            // ---- ERROR PATH ----
            if (!String(res.statusCode).startsWith('2')) {
                let errorData = '';

                res.setEncoding('utf8');
                res.on('data', chunk => errorData += chunk);
                res.on('end', () => {
                    try {
                        const parsed = JSON.parse(errorData);
                        reject(parsed.data || parsed);
                    } catch {
                        reject({
                            errorCode: res.statusCode,
                            errorMessage: errorData
                        });
                    }
                });
                return;
            }

            // ---- STREAM MODE ----
            if (stream) {
                resolve(res);
                return;
            }

            // ---- FILE MODE ----
            if (!filePath) {
                reject(new Error('filePath is required when stream=false'));
                return;
            }

            const fileStream = fs.createWriteStream(filePath);

            res.pipe(fileStream);

            fileStream.on('finish', () => resolve());
            fileStream.on('error', reject);
        });

        req.on('error', reject);
        req.end();
    });
}


async handleV2Request(uriPath, method, config, header, isExportReq = false) {
    if (this.accessToken == null) {
        this.accessToken = await this.getOauth();
    }
    return await this.sendV2Request(uriPath, method, config, header, isExportReq).catch(async error => {
        if (error.errorCode == "8535") {
            this.accessToken = await this.getOauth();
            return await this.sendV2Request(uriPath, method, config, header, isExportReq);
        } else {
            throw error;
        }
    });
}

sendV2Request(uriPath, reqMethod, config, header = {}, isExportReq = false) {
    header['User-Agent'] = 'Analytics NodeJS Client v2_' + clientVersion;
    header['Authorization'] = 'Zoho-oauthtoken ' + this.accessToken;

    if (config !== null && Object.keys(config).length !== 0) {
        const encodedConfig = encodeURIComponent(JSON.stringify(config));
        const configParam = "CONFIG=" + encodedConfig;
        uriPath = uriPath + "?" + configParam;
    }

    const options = {
        host: analyticsURI,
        path: uriPath,
        headers: header,
        method: reqMethod,
        ...STRONG_TLS_OPTS
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (resp) => {
            let data = '';
            resp.on('data', (chunk) => data += chunk);
            resp.on('end', () => {
                const isFailed = !(resp.statusCode.toString().startsWith('2'));

                // Handle empty body (204 or otherwise)
                if (!data || data.trim().length === 0) {
                    if (isFailed) {
                        reject({ error: 'Empty response body', statusCode: resp.statusCode });
                    } else {
                        resolve(null);
                    }
                    return;
                }
                
                if (isFailed) {
                    const respJSON = JSON.parse(data);
                    reject(respJSON.data);
                } else if (isExportReq) {
                    resolve(data);
                } else {
                    const respJSON = JSON.parse(data);
                    resolve(respJSON.data);
                }
            });
        });

        req.on("error", (err) => reject(JSON.parse(err)));
        req.end();
    });
}

getOauth() {
    const oauthinfo = {
        client_id: this.clientId,
        client_secret: this.clientSecret,
        refresh_token: this.refreshToken,
        grant_type: 'refresh_token'
    };

    const encodedParams = querystring.stringify(oauthinfo);

    const options = {
        host: accountsURI,
        path: '/oauth/v2/token',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Analytics NodeJS Client v2_' + clientVersion,
            'Content-Length': Buffer.byteLength(encodedParams)
        },
        method: "POST",
        ...STRONG_TLS_OPTS
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (resp) => {
            let data = '';
            resp.on('data', (chunk) => data += chunk);
            resp.on('end', () => {
                const respJSON = JSON.parse(data);
                if (!respJSON.error) {
                    resolve(respJSON.access_token);
                } else {
                    reject({ errorCode: '0', errorMessage: respJSON.error });
                }
            });
        });

        req.on("error", (err) => reject(err.message));
        req.write(encodedParams);
        req.end();
    });
}

  
};

class OrgAPI
{

    constructor(ac, orgId)
    {
        this.ac = ac;
        this.header = {};
        this.header['ZANALYTICS-ORGID'] = orgId;
    }

    /**
     * Returns the workspaces of the specified organization that the authenticated user can reach.
     * An Account Admin and an Organization Admin receive every active workspace of the organization,
     * every other user receives only the workspaces shared with them.
     * @method getOrgWorkspaces
     * @returns {JSONArray} Workspace list.
     * @throws {Error} If the request failed due to some error.
     */
    async getOrgWorkspaces()
    {
        var uriPath = "/restapi/v2/orgs/workspaces";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.workspaces;
    }

    /**
     * Returns the dashboards of the specified organization that the authenticated user may read,
     * across the workspaces the user can reach or across the workspaces named in workspaceIds.
     * @method getOrgDashboards
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Dashboards of the page along with the paging details.
     * @throws {Error} If the request failed due to some error.
     */
    async getOrgDashboards(config={})
    {
        var uriPath = "/restapi/v2/orgs/dashboards";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result;
    }

    /**
     * Returns the views the authenticated user opened most recently in the specified organization,
     * newest first. At most 20 items are returned.
     * @method getOrgRecentItems
     * @returns {JSONArray} View list.
     * @throws {Error} If the request failed due to some error.
     */
    async getOrgRecentItems()
    {
        var uriPath = "/restapi/v2/orgs/recentitems";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.views;
    }

    /**
     * Returns details of the specified view in the organization.
     * @method getViewDetails
     * @param {String} viewId - The ID of the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} View details.
     * @throws {Error} If the request failed due to some error.
     */
    async getViewDetails(viewId, config={})
    {
        var uriPath = "/restapi/v2/views/" + viewId;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.views;
    }

    /**
     * Create a blank workspace in the specified organization.
     * @method createWorkspace
     * @param {String} workspaceName - Name of the workspace.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created workspace id.
     * @throws {Error} If the request failed due to some error.
     */
    async createWorkspace(workspaceName, config={})
    {
        var uriPath = "/restapi/v2/workspaces";
        config.workspaceName = workspaceName;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.workspaceId;
    }

    /**
     * Returns list of admins for a specified organization.
     * @method getAdmins
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} Organization admin list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAdmins(config={})
    {
        var uriPath = "/restapi/v2/orgadmins";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.orgAdmins;
    }

    /**
     * Returns subscription details of the specified organization.
     * @method getSubscriptionDetails
     * @returns {Object} Subscription details.
     * @throws {Error} If the request failed due to some error.
     */
    async getSubscriptionDetails() {
        var uriPath = "/restapi/v2/subscription";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.subscription;
    }

    /**
     * Returns resource usage details of the specified organization.
     * @method getResourceDetails
     * @returns {Object} Resource details.
     * @throws {Error} If the request failed due to some error.
     */
    async getResourceDetails() {
        var uriPath = "/restapi/v2/resources";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.resourceDetails;
    }

    /**
     * Returns list of users for the specified organization.
     * @method getUsers
     * @returns {JSONArray} User list.
     * @throws {Error} If the request failed due to some error.
     */
    async getUsers() {
        var uriPath = "/restapi/v2/users";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.users;
    }

    /**
     * Add users to the specified organization.
     * @method addUsers
     * @param {JSONArray} emailIds - The email address of the users to be added.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addUsers(emailIds, config={}) {
        var uriPath = "/restapi/v2/users";
        config.emailIds = emailIds;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove users from the specified organization.
     * @method removeUsers
     * @param {JSONArray} emailIds - The email address of the users to be removed.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeUsers(emailIds, config={}) {
        var uriPath = "/restapi/v2/users";
        config.emailIds = emailIds;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Activate users in the specified organization.
     * @method activateUsers
     * @param {JSONArray} emailIds - The email address of the users to be activated.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async activateUsers(emailIds, config={}) {
        var uriPath = "/restapi/v2/users/active";
        config.emailIds = emailIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }


    /**
     * Deactivate users in the specified organization.
     * @method deActivateUsers
     * @param {JSONArray} emailIds - The email address of the users to be deactivated.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deActivateUsers(emailIds, config={}) {
        var uriPath = "/restapi/v2/users/inactive";
        config.emailIds = emailIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Change role for the specified users.
     * @method changeUserRole
     * @param {JSONArray} emailIds - The email address of the users.
     * @param {String} role - New role for the users.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeUserRole(emailIds, role, config={}) {
        var uriPath = "/restapi/v2/users/role";
        config.emailIds = emailIds;
        config.role = role;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns details of the specified workspace/view.
     * @method getMetaDetails
     * @param {String} workspaceName - Name of the workspace.
     * @param {String} viewName - Name of the view. Can be null.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Workspace (or) View meta details.
     * @throws {Error} If the request failed due to some error.
     */
    async getMetaDetails(workspaceName, viewName=null, config={})
    {
        var uriPath = "/restapi/v2/metadetails";
        config.workspaceName = workspaceName;
        if(viewName !== null)
        {
            config.viewName = viewName;
        }

        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result;
    }

    /**
     * Returns all the automl analysis available in an organization.
     * @method getAutomlAnalysis
     * @returns {Array} AutoML analysis list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAutomlAnalysis() {
        var uriPath = "/restapi/v2/automl/analysis";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.analysis;
    }
    /**
     * Returns list of all custom roles available in the organization.
     * @method getCustomRoles
     * @returns {JSONArray} Custom roles list.
     * @throws {Error} If the request failed due to some error.
     */
    async getCustomRoles() {
        var uriPath = "/restapi/v2/orgs/roles";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.roles;
    }
    /**
     * Create a new custom role in the organization.
     * @method createCustomRole
     * @param {String} roleName - Name of the custom role to be created.
     * @param {String} accessType - Access type for the custom role.
     * @param {Object} permissions - Permissions configuration for the custom role.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created custom role id.
     * @throws {Error} If the request failed due to some error.
     */
    async createCustomRole(roleName, accessType, permissions, config={}) {
        var uriPath = "/restapi/v2/orgs/roles";
        config.roleName = roleName;
        config.accessType = accessType;
        config.permissions = permissions;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.roleId;
    }
    /**
     * Update the existing custom role in the organization.
     * @method updateCustomRole
     * @param {String} roleId - Id of the custom role to be updated.
     * @param {String} roleName - New name for the custom role.
     * @param {String} accessType - New access type for the custom role.
     * @param {Object} permissions - New permissions configuration for the custom role.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateCustomRole(roleId, roleName, accessType, permissions, config={}) {
        var uriPath = "/restapi/v2/orgs/roles/" + roleId;
        config.roleName = roleName;
        config.accessType = accessType;
        config.permissions = permissions;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Delete the specified custom role from the organization.
     * @method deleteCustomRole
     * @param {String} roleId - Id of the custom role to be deleted.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteCustomRole(roleId) {
        var uriPath = "/restapi/v2/orgs/roles/" + roleId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns the access restriction settings configured for the organization.
     * @method getOrgAccessRestrictions
     * @returns {Object} Organization access restriction settings.
     * @throws {Error} If the request failed due to some error.
     */
    async getOrgAccessRestrictions() {
        var uriPath = "/restapi/v2/security-controls/access-restrictions";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Update the access restriction settings of the organization.
     * @method updateOrgAccessRestrictions
     * @param {Object} config={} - Contains the access restriction configurations to be updated.
     * @throws {Error} If the request failed due to some error.
     */
    async updateOrgAccessRestrictions(config={}) {
        var uriPath = "/restapi/v2/security-controls/access-restrictions";
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Returns list of linked workspaces available in the specified organization.
     * @method getLinkedWorkspaces
     * @returns {JSONArray} Linked workspaces list.
     * @throws {Error} If the request failed due to some error.
     */
    async getLinkedWorkspaces() {
        var uriPath = "/restapi/v2/linkedworkspaces";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.linkedWorkspaces;
    }

}

class WorkspaceAPI
{

    constructor(ac, orgId, workspaceId)
    {
        this.ac = ac;
        this.uriPath = "/restapi/v2/workspaces/" + workspaceId
        this.securityControlsUriPath = "/restapi/v2/security-controls/workspaces/" + workspaceId
        this.header = {};
        this.header['ZANALYTICS-ORGID'] = orgId;
        this.orgId = orgId;
        this.workspaceId = workspaceId;
    }

    /**
     * Returns details of the specified workspace.
     * @method getWorkspaceDetails
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Workspace details.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceDetails(config={})
    {
        var result = await this.ac.handleV2Request(this.uriPath, "GET", config, this.header);
        return result.workspaces;
    }

    /**
     * Copy the specified workspace from one organization to another or within the organization.
     * @method copy
     * @param {String} workspaceName - Name of the new workspace.
     * @param {Object} config={} - Contains any additional control attributes.
     * @param {String} destOrgId=null - Id of the organization where the destination workspace is present.
     * @returns {String} Copied workspace id.
     * @throws {Error} If the request failed due to some error.
     */
    async copy(workspaceName, config={}, destOrgId=null)
    {
        config.newWorkspaceName = workspaceName;
        var reqHeader = this.header;
        if(destOrgId != null)
        {
          reqHeader['ZANALYTICS-DEST-ORGID'] = destOrgId;
        }
        var result = await this.ac.handleV2Request(this.uriPath, "POST", config, reqHeader);
        return result.workspaceId;
    }

    /**
     * Rename a specified workspace in the organization.
     * @method rename
     * @param {String} workspaceName - New name for the workspace.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async rename(workspaceName, config={})
    {
        config.workspaceName = workspaceName;
        await this.ac.handleV2Request(this.uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified workspace in the organization.
     * @method delete
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async delete(config={})
    {
        await this.ac.handleV2Request(this.uriPath, "DELETE", config, this.header);
    }

    /**
     * Create a table in the specified workspace.
     * @method createTable
     * @param {Object} tableDesign - Table structure.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} created table id.
     * @throws {Error} If the request failed due to some error.
     */
    async createTable(tableDesign, config={}) {
        var uriPath = this.uriPath + "/tables";
        config.tableDesign = tableDesign;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.viewId;
    }

    /**
     * Create a new query table in the workspace.
     * @method createQueryTable
     * @param {String} sqlQuery - SQL query to construct the query table.
     * @param {String} queryTableName - Name of the query table to be created.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Id of the created query table.
     * @throws {Error} If the request failed due to some error.
     */
    async createQueryTable(sqlQuery, queryTableName, config={}) {
        var uriPath = this.uriPath + "/querytables";
        config.sqlQuery = sqlQuery
        config.queryTableName = queryTableName
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.viewId;
    }

    /**
     * Returns list of all query tables for the specified workspace.
     * @method getQueryTables
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} Query table list.
     * @throws {Error} If the request failed due to some error.
     */
    async getQueryTables(config={}) {
        var uriPath = this.uriPath + "/querytables";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.queryTables;
    }
    /**
     * Update the mentioned query table in the workspace.
     * @method editQueryTable
     * @param {String} viewId - Id of the query table to be updated.
     * @param {String} sqlQuery - New SQL query to be updated.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async editQueryTable(viewId, sqlQuery, config={}) {
        var uriPath = this.uriPath + "/querytables/" + viewId;
        config.sqlQuery = sqlQuery
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns the secret key of the specified workspace.
     * @method getSecretKey
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Workspace secret key.
     * @throws {Error} If the request failed due to some error.
     */
    async getSecretKey(config={})
    {
        var uriPath = this.uriPath + "/secretkey";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.workspaceKey;
    }

    /**
     * Adds a specified workspace as favorite.
     * @method addFavorite
     * @throws {Error} If the request failed due to some error.
     */
    async addFavorite(config={})
    {
        var uriPath = this.uriPath + "/favorite";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove a specified workspace from favorite.
     * @method removeFavorite
     * @throws {Error} If the request failed due to some error.
     */
    async removeFavorite(config={})
    {
        var uriPath = this.uriPath + "/favorite";
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Adds a specified workspace as default.
     * @method addDefault
     * @throws {Error} If the request failed due to some error.
     */
    async addDefault(config={})
    {
        var uriPath = this.uriPath + "/default";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove a specified workspace from default.
     * @method removeDefault
     * @throws {Error} If the request failed due to some error.
     */
    async removeDefault(config={})
    {
        var uriPath = this.uriPath + "/default";
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns list of admins for the specified workspace.
     * @method getAdmins
     * @returns {JSONArray} Workspace admin list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAdmins(config={})
    {
        var uriPath = this.uriPath + "/admins";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.workspaceAdmins;
    }

    /**
     * Add admins for the specified workspace.
     * @method addAdmins
     * @param {JSONArray} emailIds - The email address of the admin users to be added.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addAdmins(emailIds, config={})
    {
        var uriPath = this.uriPath + "/admins";
        config.emailIds = emailIds;

        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove admins from the specified workspace.
     * @method removeAdmins
     * @param {JSONArray} emailIds - The email address of the admin users to be removed.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeAdmins(emailIds, config={})
    {
        var uriPath = this.uriPath + "/admins";
        config.emailIds = emailIds;

        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns shared details of the specified workspace.
     * @method getShareInfo
     * @returns {Object} Workspace share info.
     * @throws {Error} If the request failed due to some error.
     */
    async getShareInfo()
    {
        var uriPath = this.uriPath + "/share";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Share views to the specified users.
     * @method shareViews
     * @param {JSONArray} viewIds - View ids to be shared.
     * @param {JSONArray} emailIds - The email address of the users to whom the views need to be shared.
     * @param {Object} permissions - Contains permission details.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async shareViews(viewIds, emailIds, permissions, config={})
    {
        var uriPath = this.uriPath + "/share";
        config.viewIds = viewIds;
        config.emailIds = emailIds;
        config.permissions = permissions;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove shared views for the specified users.
     * @method removeShare
     * @param {JSONArray} viewIds - View ids whose sharing needs to be removed.
     * @param {JSONArray} emailIds - The email address of the users to whom the sharing need to be removed.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeShare(viewIds, emailIds, config={})
    {
        var uriPath = this.uriPath + "/share";
        if(viewIds!=null)
        {
            config.viewIds = viewIds;
        }
        config.emailIds = emailIds;

        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns shared details of the specified views.
     * @method getSharedDetailsForViews
     * @param {JSONArray} viewIds - The id of the views to be copied.
     * @returns {JSONArray} Folder list.
     * @throws {Error} If the request failed due to some error.
     */
    async getSharedDetailsForViews(viewIds)
    {
        var uriPath = this.uriPath + "/share/shareddetails";
        var config = {};
        config.viewIds = viewIds;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.sharedDetails;
    }

    /**
     * Returns list of all accessible folders for the specified workspace.
     * @method getFolders
     * @returns {JSONArray} Folder list.
     * @throws {Error} If the request failed due to some error.
     */
    async getFolders()
    {
        var uriPath = this.uriPath + "/folders";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.folders;
    }

    /**
     * Create a folder in the specified workspace.
     * @method createFolder
     * @param {String} folderName - Name of the folder to be created.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created folder id.
     * @throws {Error} If the request failed due to some error.
     */
    async createFolder(folderName, config={})
    {
        var uriPath = this.uriPath + "/folders";
        config.folderName = folderName;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.folderId;
    }

    /**
     * Returns list of all accessible views for the specified workspace.
     * @method getViews
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} View list.
     * @throws {Error} If the request failed due to some error.
     */
    async getViews(config={})
    {
        var uriPath = this.uriPath + "/views";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.views;
    }

    /**
     * Copy the specified views from one workspace to another workspace.
     * @method copyViews
     * @param {JSONArray} viewIds - The id of the views to be copied.
     * @param {String} destWorkspaceId - The destination workspace id.
     * @param {Object} config={} - Contains any additional control attributes.
     * @param {String} destOrgId=null - Id of the organization where the destination workspace is present.
     * @returns {JSONArray} View list.
     * @throws {Error} If the request failed due to some error.
     */
    async copyViews(viewIds, destWorkspaceId, config={}, destOrgId=null) {
        var uriPath = this.uriPath + "/views/copy";
        config.viewIds = viewIds;
        config.destWorkspaceId = destWorkspaceId;
        var reqHeader = this.header;
        if(destOrgId != null)
        {
          reqHeader['ZANALYTICS-DEST-ORGID'] = destOrgId;
        }
        var result = await this.ac.handleV2Request(uriPath, "POST", config, reqHeader);
        return result.views;
    }

    /**
     * Enable workspace to the specified white label domain.
     * @method enableDomainAccess
     * @throws {Error} If the request failed due to some error.
     */
    async enableDomainAccess()
    {
        var uriPath = this.uriPath + "/wlaccess";
        await this.ac.handleV2Request(uriPath, "POST", null, this.header);
    }

    /**
     * Disable workspace from the specified white label domain.
     * @method disableDomainAccess
     * @throws {Error} If the request failed due to some error.
     */
    async disableDomainAccess()
    {
        var uriPath = this.uriPath + "/wlaccess";
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Rename a specified folder in the workspace.
     * @method renameFolder
     * @param {String} folderId - Id of the folder.
     * @param {String} folderName - New name for the folder.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async renameFolder(folderId, newFolderName, config={})
    {
        config.folderName = newFolderName;
        var uriPath = this.uriPath + "/folders/" + folderId; 
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified folder in the workspace.
     * @method deleteFolder
     * @param {String} folderId - Id of the folder to be deleted.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteFolder(folderId)
    {
        var uriPath = this.uriPath + "/folders/" + folderId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns list of groups for the specified workspace.
     * @method getGroups
     * @returns {JSONArray} Group list.
     * @throws {Error} If the request failed due to some error.
     */
    async getGroups() {
        var uriPath = this.uriPath + "/groups";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.groups;
    }

    /**
     * Get the details of the specified group.
     * @method getGroupDetails
     * @param {String} groupId - Id of the group.
     * @returns {Object} Details of the specified group.
     * @throws {Error} If the request failed due to some error.
     */
    async getGroupDetails(groupId) {
        var uriPath = this.uriPath + "/groups/" + groupId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.groups;
    }

    /**
     * Create a group in the specified workspace.
     * @method createGroup
     * @param {String} groupName - Name of the group.
     * @param {JSONArray} emailIds - The email address of the users to be added to the group.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created group id.
     * @throws {Error} If the request failed due to some error.
     */
    async createGroup(groupName, emailIds, config={}) {
        var uriPath = this.uriPath + "/groups";

        config.groupName = groupName;
        config.emailIds = emailIds;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.groupId;
    }

    /**
     * Rename a specified group.
     * @method renameGroup
     * @param {String} groupId - Id of the group.
     * @param {String} newGroupName - New name for the group.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async renameGroup(groupId, newGroupName, config={}) {
        config.groupName = newGroupName;
        var uriPath = this.uriPath + "/groups/" + groupId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    
    /**
     * Add users to the specified group.
     * @method addGroupMembers
     * @param {String} groupId - Id of the group.
     * @param {JSONArray} emailIds - The email address of the users to be added to the group.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addGroupMembers(groupId, emailIds, config={}) {
        config.emailIds = emailIds;
        var uriPath = this.uriPath + "/groups/" + groupId + "/members";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    
    /**
     * Remove users from the specified group.
     * @method removeGroupMembers
     * @param {String} groupId - Id of the group.
     * @param {JSONArray} emailIds - The email address of the users to be removed from the group.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeGroupMembers(groupId, emailIds, config={}) {
        config.emailIds = emailIds;
        var uriPath = this.uriPath + "/groups/" + groupId + "/members";
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Delete a specified group.
     * @method deleteGroup
     * @param {String} groupId - The id of the group.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteGroup(groupId) {
        var uriPath = this.uriPath + "/groups/" + groupId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Create a slideshow in the specified workspace.
     * @method createSlideshow
     * @param {String} slideName - Name of the slideshow to be created.
     * @param {JSONArray} viewIds - Ids of the view to be included in the slideshow.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Id of the created slideshow.
     * @throws {Error} If the request failed due to some error.
     */
    async createSlideshow(slideName, viewIds, config={}) {
        var uriPath = this.uriPath + "/slides";
        config.slideName = slideName
        config.viewIds = viewIds
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.slideId;
    }

    /**
     * Update details of the specified slideshow.
     * @method updateSlideshow
     * @param {String} slideId - The id of the slideshow.
     * @param {Object} config={} - Contains the control configurations
     * @throws {Error} If the request failed due to some error.
     */
    async updateSlideshow(slideId, config={}) {
        var uriPath = this.uriPath + "/slides/" + slideId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified slideshow in the workspace.
     * @method deleteSlideshow
     * @param {String} slideId - Id of the slideshow.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteSlideshow(slideId) {
        var uriPath = this.uriPath + "/slides/" + slideId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns list of slideshows for the specified workspace.
     * @method getSlideshows
     * @returns {JSONArray} Slideshow list.
     * @throws {Error} If the request failed due to some error.
     */
    async getSlideshows() {
        var uriPath = this.uriPath + "/slides";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.slideshows;
    }

    /**
     * Returns slide URL to access the specified slideshow.
     * @method getSlideshowUrl
     * @param {String} slideId - Id of the slideshow.
     * @param {Object} config={} - Contains the control configurations
     * @returns {String} Slideshow URL.
     * @throws {Error} If the request failed due to some error.
     */
    async getSlideshowUrl(slideId, config={}) {
        var uriPath = this.uriPath + "/slides/" + slideId + "/publish";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.slideUrl;
    }

    /**
     * Returns details of the specified slideshow.
     * @method getSlideshowDetails
     * @param {String} slideId - Id of the slideshow.
     * @returns {Object} Slideshow details.
     * @throws {Error} If the request failed due to some error.
     */
    async getSlideshowDetails(slideId) {
        var uriPath = this.uriPath + "/slides/" + slideId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.slideInfo;
    }

    /**
     * Create a variable in the workspace.
     * @method createVariable
     * @param {String} variableName - Name of the variable to be created.
     * @param {Number} variableName - Datatype of the variable to be created.
     * @param {Number} variableName - Type of the variable to be created.
     * @param {Object} config={} - Contains the control attributes.
     * @returns {String} Id of the created variable.
     * @throws {Error} If the request failed due to some error.
     */
    async createVariable(variableName, variableDataType, variableType, config={}) {
        var uriPath = this.uriPath + "/variables";
        config.variableName = variableName
        config.variableDataType = variableDataType
        config.variableType = variableType
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.variableId;
    }

    /**
     * Update details of the specified variable in the workspace.
     * @method updateVariable
     * @param {String} variableId - Id of the variable.
     * @param {String} variableName - New name for the variable.
     * @param {Number} variableName - New datatype for the variable.
     * @param {Number} variableName - New type for the variable.
     * @param {Object} config={} - Contains the control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateVariable(variableId, variableName, variableDataType, variableType, config={}) {
        var uriPath = this.uriPath + "/variables/" + variableId;
        config.variableName = variableName
        config.variableDataType = variableDataType
        config.variableType = variableType
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified variable in the workspace.
     * @method deleteVariable
     * @param {String} variableId - Id of the variable.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteVariable(variableId) {
        var uriPath = this.uriPath + "/variables/" + variableId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns list of variables for the specified workspace.
     * @method getVariables
     * @returns {JSONArray} Variable list.
     * @throws {Error} If the request failed due to some error.
     */
    async getVariables() {
        var uriPath = this.uriPath + "/variables";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.variables;
    }

    /**
     * Returns details of the specified variable.
     * @method getVariableDetails
     * @param {String} variableId - Id of the variable.
     * @returns {Object} Variable details.
     * @throws {Error} If the request failed due to some error.
     */
    async getVariableDetails(variableId) {
        var uriPath = this.uriPath + "/variables/" + variableId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Make the specified folder as default.
     * @method makeDefaultFolder
     * @param {String} folderId - Id of the folder.
     * @throws {Error} If the request failed due to some error.
     */
    async makeDefaultFolder(folderId) {
        var uriPath = this.uriPath + "/folders/" + folderId + "/default";
        await this.ac.handleV2Request(uriPath, "PUT", null, this.header);
    }

    /**
     * Returns list of datasources for the specified workspace.
     * @method getDatasources
     * @returns {JSONArray} Datasource list.
     * @throws {Error} If the request failed due to some error.
     */
    async getDatasources() {
        var uriPath = this.uriPath + "/datasources";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.dataSources;
    }

    /**
     * Initiate data sync for the specified datasource.
     * @method syncData
     * @param {String} datasourceId - Id of the datasource.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async syncData(datasourceId, config={}) {
        var uriPath = this.uriPath + "/datasources/" + datasourceId + "/sync";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Update connection details for the specified datasource.
     * @method updateDatasourceConnection
     * @param {String} datasourceId - Id of the datasource.
     * @param {Object} config={} - Contains the control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateDatasourceConnection(datasourceId, config={}) {
        var uriPath = this.uriPath + "/datasources/" + datasourceId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns list of all views available in trash for the specified workspace.
     * @method getTrashViews
     * @returns {JSONArray} Trash view list.
     * @throws {Error} If the request failed due to some error.
     */
    async getTrashViews() {
        var uriPath = this.uriPath + "/trash";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.views;
    }

    /**
     * Restore the specified view from trash.
     * @method restoreTrashView
     * @param {String} viewId - Id of the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async restoreTrashView(viewId, config={}) {
        var uriPath = this.uriPath + "/trash/" + viewId;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Delete the specified view permanently from trash.
     * @method deleteTrashView
     * @param {String} viewId - Id of the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteTrashView(viewId, config={}) {
        var uriPath = this.uriPath + "/trash/" + viewId;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Swaps the hierarchy of a parent folder and a subfolder.
     * @method changeFolderHierarchy
     * @param {String} folderId - Id of the folder.
     * @param {Number} hierarchy - New hierarchy for the folder. (0 - Parent; 1 - Child).
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeFolderHierarchy(folderId, hierarchy, config={}) {
        var uriPath = this.uriPath + "/folders/" + folderId + "/move";
        config.hierarchy = hierarchy;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Place the folder above the reference folder.
     * @method changeFolderPosition
     * @param {String} folderId - Id of the folder.
     * @param {String} referenceFolderId - Id of the reference folder.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeFolderPosition(folderId, referenceFolderId, config={}) {
        var uriPath = this.uriPath + "/folders/" + folderId + "/reorder";
        config.referenceFolderId = referenceFolderId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Move views to the mentioned folder.
     * @method moveViewsToFolder
     * @param {String} folderId - Id of the folder.
     * @param {JSONArray} viewIds - View ids to be moved.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async moveViewsToFolder(folderId, viewIds, config={}) {
        var uriPath = this.uriPath + "/views/movetofolder";
        config.folderId = folderId;
        config.viewIds = viewIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Export the mentioned views as templates.
     * @method exportAsTemplate
     * @param {JSONArray} viewIds - Ids of the view to be exported.
     * @param {String} filePath - Path of the file where the data exported to be stored. ( Should be in 'atpt' format )
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async exportAsTemplate(viewIds, filePath, config={})
    {
        var uriPath = this.uriPath + "/template/data";
        config.viewIds = viewIds;
        await this.ac.handleExportRequest(
            uriPath,
            config,
            this.header,
            { filePath: filePath }
        );
    }

    /**
     * Returns list of users for the specified workspace.
     * @method getWorkspaceUsers
     * @returns {JSONArray} User list.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceUsers() {
        var uriPath = this.uriPath + "/users";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.users;
    }

    /**
     * Add users to the specified workspace.
     * @method addWorkspaceUsers
     * @param {JSONArray} emailIds - The email address of the users to be added.
     * @param {String} role - Role for the users to be added.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addWorkspaceUsers(emailIds, role, config={}) {
        var uriPath = this.uriPath + "/users";
        config.emailIds = emailIds;
        config.role = role;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove users from the specified workspace.
     * @method removeWorkspaceUsers
     * @param {JSONArray} emailIds - The email address of the users to be removed.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeWorkspaceUsers(emailIds, config={}) {
        var uriPath = this.uriPath + "/users";
        config.emailIds = emailIds;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Change users staus in the specified workspace.
     * @method changeWorkspaceUserStatus
     * @param {JSONArray} emailIds - The email address of the users.
     * @param {String} operation - New status for the users ( Values -  activate | deactivate )
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeWorkspaceUserStatus(emailIds, operation, config={}) {
        var uriPath = this.uriPath + "/users/status";
        config.emailIds = emailIds;
        config.operation = operation;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Change role for the specified users.
     * @method changeWorkspaceUserRole
     * @param {JSONArray} emailIds - The email address of the users.
     * @param {String} role - New role for the users.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeWorkspaceUserRole(emailIds, role, config={}) {
        var uriPath = this.uriPath + "/users/role";
        config.emailIds = emailIds;
        config.role = role;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns list of email schedules available in the specified workspace.
     * @method getEmailSchedules
     * @returns {JSONArray} List of email schedules.
     * @throws {Error} If the request failed due to some error.
     */
    async getEmailSchedules() {
        var uriPath = this.uriPath + "/emailschedules";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.emailSchedules;
    }

    /**
     * Create an email schedule in the specified workspace.
     * @method createEmailSchedule
     * @param {String} scheduleName - Name of the email schedule.
     * @param {JSONArray} viewIds - View ids to be mailed.
     * @param {String} format - The format in which the data has to be mailed.
     * @param {JSONArray} emailIds - The recipients' email addresses for sending views.
     * @param {Object} scheduleDetails - Contains schedule frequency, date, and time info.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created email schedule id.
     * @throws {Error} If the request failed due to some error.
     */
    async createEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config={}) {
        var uriPath = this.uriPath + "/emailschedules";

        config.scheduleName = scheduleName;
        config.viewIds = viewIds;
        config.exportType = format;
        config.emailIds = emailIds;
        config.scheduleDetails = scheduleDetails;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.scheduleId;
    }

    /**
     * Update configurations of the specified email schedule in the workspace.
     * @method updateEmailSchedule
     * @param {String} scheduleId - Id for the email schedule.
     * @param {Object} config - Contains the control configurations.
     * @returns {String} Updated email schedule id.
     * @throws {Error} If the request failed due to some error.
     */
    async updateEmailSchedule(scheduleId, config) {
        var uriPath = this.uriPath + "/emailschedules/" + scheduleId;
        var result = await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
        return result.scheduleId;
    }

    /**
     * Trigger configured email schedules instantly.
     * @method triggerEmailSchedule
     * @param {String} scheduleId - Id for the email schedule.
     * @throws {Error} If the request failed due to some error.
     */
    async triggerEmailSchedule(scheduleId) {
        var uriPath = this.uriPath + "/emailschedules/" + scheduleId;
        await this.ac.handleV2Request(uriPath, "POST", null, this.header);
    }

    /**
     * Update email schedule status.
     * @method changeEmailScheduleStatus
     * @param {String} scheduleId - Id for the email schedule.
     * @param {String} operation - New status for the schedule ( Values - activate | deactivate )
     * @throws {Error} If the request failed due to some error.
     */
    async changeEmailScheduleStatus(scheduleId, operation) {
        var uriPath = this.uriPath + "/emailschedules/" + scheduleId + "/status";
        var config = { operation: operation };
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete the specified email schedule in the workspace.
     * @method deleteEmailSchedule
     * @param {String} scheduleId - Id for the email schedule.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteEmailSchedule(scheduleId) {
        var uriPath = this.uriPath + "/emailschedules/" + scheduleId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns list of all aggregate formulas for the specified workspace.
     * @method getAggregateFormulas
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} Aggregate formula list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAggregateFormulas(config={})
    {
        var uriPath = this.uriPath + "/aggregateformulas";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.aggregateFormulas;
    }

    /**
     * Returns list of all dependent views and formulas for the specified aggregate formula.
     * @method getAggregateFormulaDependents
     * @param {String} formulaId - Id of the aggregate formula.
     * @returns {JSONObject} Dependent details.
     * @throws {Error} If the request failed due to some error.
     */
    async getAggregateFormulaDependents(formulaId)
    {
        var uriPath = this.uriPath + "/aggregateformulas/" + formulaId + "/dependents";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Returns the value of the aggregate formula.
     * @method getAggregateFormulaValue
     * @param {String} formulaId - Id of the aggregate formula.
     * @returns {String} Aggregate formula value.
     * @throws {Error} If the request failed due to some error.
     */
    async getAggregateFormulaValue(formulaId)
    {
        var uriPath = this.uriPath + "/aggregateformulas/" + formulaId + "/value";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.formulaValue;
    }

    /**
     * Create a report in the specified workspace.
     * @method createReport
     * @param {Object} config={} - Contains the control attributes.
     * @returns {String} Id of the created view.
     * @throws {Error} If the request failed due to some error.
     */
    async createReport(config={}) {
        var uriPath = this.uriPath + "/reports";
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.viewId;
    }

    /**
     * Update the design and configuration of the specified report.
     * @method updateReport
     * @param {String} viewId - Id of the view.
     * @param {Object} config={} - Contains the control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateReport(viewId, config={}) {
        var uriPath = this.uriPath + "/reports/" + viewId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns details of the specified query table.
     * @method getQueryTableDetails
     * @param {String} queryTableId - Id of the query table.
     * @returns {Object} View details.
     * @throws {Error} If the request failed due to some error.
     */
    async getQueryTableDetails(queryTableId) {
        var uriPath = this.uriPath + "/querytables/" + queryTableId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Returns list of automl analysis for the specified workspace.
     * @method getAutomlAnalysis
     * @returns {Array} AutoML analysis list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAutomlAnalysis() {
        var uriPath = "/restapi/v2/automl/workspaces/" + this.workspaceId + "/analysis";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.analysis;
    }

    /**
     * Retrieve detailed information for a specific AutoML analysis.
     * @method getAutomlAnalysisDetails
     * @param {String} analysisId - Id of the Automl Analysis.
     * @returns {Object} AutoML analysis details.
     * @throws {Error} If the request failed due to some error.
     */
    async getAutomlAnalysisDetails(analysisId) {
        var uriPath = "/restapi/v2/automl/workspaces/" + this.workspaceId + "/analysis/" + analysisId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.analysis;
    }

    /**
     * Returns deployment details available for a AutoML analysis model.
     * @method getDeploymentDetails
     * @param {String} analysisId - Id of the Automl Analysis.
     * @param {String} modelId - Id of the Automl Analysis Model.
     * @returns {Array} AutoML analysis deployment details.
     * @throws {Error} If the request failed due to some error.
     */
    async getDeploymentDetails(analysisId, modelId) {
        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/models/" + modelId +
                    "/deployments";

        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.deployments;
    }

    /**
     * Create a new AutoML analysis within the provided workspace.
     * @method createAutomlAnalysis
     * @param {String} name - Name for the automl analysis to be created.
     * @param {String} trainingTableId - Id of the training table.
     * @param {String} predictionType - REGRESSION / CLASSIFICATION / CLUSTERING.
     * @param {Array} features - List of column names used as features.
     * @param {Number} serverOption - 1 → 8GB, 2 → 16GB, 3 → 32GB.
     * @param {Object} algorithms - Algorithms configuration.
     * @param {Object} config={} - Additional control attributes.
     * @returns {String} Created AutoML Analysis Id.
     * @throws {Error} If the request failed due to some error.
     */
    async createAutomlAnalysis(
        name,
        trainingTableId,
        predictionType,
        features,
        serverOption,
        algorithms,
        config = {}
    ) {
        config.name = name;
        config.trainingTableId = trainingTableId;
        config.predictionType = predictionType;
        config.features = features;
        config.serverOption = serverOption;
        config.algorithms = algorithms;

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis";

        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return String(result.id);
    }

    /**
     * Delete a specified automl analysis from the given workspace.
     * @method deleteAutomlAnalysis
     * @param {String} analysisId - Id of the Automl Analysis to be deleted.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteAutomlAnalysis(analysisId, config = {}) {
        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId;

        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Delete a specified model available in the given automl analysis.
     * @method deleteAutomlAnalysisModel
     * @param {String} analysisId - Id of the Automl Analysis.
     * @param {String} modelId - Id of the model to be deleted.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteAutomlAnalysisModel(analysisId, modelId, config = {}) {

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/models/" + modelId;

        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Deploy the AutoML analysis model.
     * @method createAutomlAnalysisDeployment
     * @returns {Array} Created AutoML Deployment details.
     * @throws {Error} If the request failed due to some error.
     */
    async createAutomlAnalysisDeployment(
        analysisId,
        modelId,
        inputTableId,
        outputTable,
        outputColumns,
        predictionColumn,
        serverOption,
        importType,
        scheduleDetails,
        config = {}
    ) {

        config.inputTableId = inputTableId;
        config.outputTable = outputTable;
        config.outputColumns = outputColumns;
        config.predictionColumn = predictionColumn;
        config.serverOption = serverOption;
        config.importType = importType;

        if (scheduleDetails == null) {
            scheduleDetails = "none";
        }

        config.scheduleDetails = scheduleDetails;

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/models/" + modelId +
                    "/deployments";

        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.deployments;
    }

    /**
     * Execute the AutoML analysis deployment.
     * @method deployAutomlAnalysis
     * @param {String} analysisId - Id of the Automl Analysis.
     * @param {String} deploymentId - Id of the deployment to be executed.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deployAutomlAnalysis(analysisId, deploymentId, config = {}) {

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/deployments/" + deploymentId +
                    "/execute";

        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Delete the AutoML analysis deployment.
     * @method deleteAutomlAnalysisDeployment
     * @param {String} analysisId - Id of the Automl Analysis.
     * @param {String} deploymentId - Id of the deployment to be deleted.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteAutomlAnalysisDeployment(analysisId, deploymentId, config = {}) {

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/deployments/" + deploymentId;

        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Get predictions by providing sample input values for a trained model.
     * @method automlAnalysisPrediction
     * @param {String} analysisId - Id of the Automl Analysis.
     * @param {String} modelId - Id of the Automl Analysis model.
     * @param {Object} features - Column → value map for prediction.
     * @param {Object} config={} - Additional control attributes.
     * @returns {Object} Prediction result.
     * @throws {Error} If the request failed due to some error.
     */
    async automlAnalysisPrediction(analysisId, modelId, features, config = {}) {

        config.features = features;

        var uriPath = "/restapi/v2/automl/workspaces/" +
                    this.workspaceId +
                    "/analysis/" + analysisId +
                    "/models/" + modelId +
                    "/whatif";

        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result;
    }


    /**
     * Returns list of all tags for the specified workspace.
     * @method getTags
     * @returns {JSONArray} Tags list.
     * @throws {Error} If the request failed due to some error.
     */
    async getTags() {
        var uriPath = this.uriPath + "/tags";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.tags;
    }
    /**
     * Create a tag in the specified workspace.
     * @method createTag
     * @param {String} tagName - Name of the tag to be created.
     * @param {String} colorCode - Color of the tag in HEX color code.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created tag id.
     * @throws {Error} If the request failed due to some error.
     */
    async createTag(tagName, colorCode, config={}) {
        var uriPath = this.uriPath + "/tags";
        config.name = tagName;
        config.colorCode = colorCode;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.tagId;
    }
    /**
     * Update details of the specified tag in the workspace.
     * @method updateTag
     * @param {String} tagId - Id of the tag.
     * @param {Object} config={} - Contains the control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateTag(tagId, config={}) {
        var uriPath = this.uriPath + "/tags/" + tagId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Delete the specified tag from the workspace.
     * @method deleteTag
     * @param {String} tagId - Id of the tag.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteTag(tagId) {
        var uriPath = this.uriPath + "/tags/" + tagId;
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }
    /**
     * Adds the specified tag to multiple views in the workspace.
     * @method addTagToViews
     * @param {String} tagId - Id of the tag.
     * @param {JSONArray} viewIds - View ids to be associated with the tag.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addTagToViews(tagId, viewIds, config={}) {
        var uriPath = this.uriPath + "/tags/" + tagId + "/views";
        config.viewIds = viewIds;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    /**
     * Removes the specified tag from multiple views in the workspace.
     * @method removeTagFromViews
     * @param {String} tagId - Id of the tag.
     * @param {JSONArray} viewIds - View ids to be dissociated. Not required when dissociateAll is true.
     * @param {Boolean} dissociateAll - To dissociate the tag from all associated views.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeTagFromViews(tagId, viewIds=null, dissociateAll=false, config={}) {
        var uriPath = this.uriPath + "/tags/" + tagId + "/views";
        if(dissociateAll) {
            config.dissociateAll = true;
        } else {
            config.viewIds = viewIds;
        }
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }
    /**
     * Returns list of views associated with the specified tag.
     * @method getTaggedViews
     * @param {String} tagId - Id of the tag.
     * @returns {JSONArray} Tagged views list.
     * @throws {Error} If the request failed due to some error.
     */
    async getTaggedViews(tagId) {
        var uriPath = this.uriPath + "/tags/" + tagId + "/views";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.views;
    }

    /**
     * Returns list of workspaces linked to the specified master workspace.
     * @method getLinkedWorkspaces
     * @returns {JSONArray} Linked workspaces list.
     * @throws {Error} If the request failed due to some error.
     */
    async getLinkedWorkspaces() {
        var uriPath = this.uriPath + "/linkedworkspaces";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.linkedWorkspaces;
    }
    /**
     * Returns list of organizations and workspaces that can be linked to the specified master workspace.
     * @method getLinkableWorkspaces
     * @returns {JSONArray} Organizations with their linkable workspaces.
     * @throws {Error} If the request failed due to some error.
     */
    async getLinkableWorkspaces() {
        var uriPath = this.uriPath + "/linkedworkspaces/linkable";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.orgs;
    }
    /**
     * Returns the linking compatibility details for the specified client workspaces.
     * @method getWorkspaceLinkingCompatibility
     * @param {JSONArray} clients - Contains the client workspaces to be verified for linking compatibility.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} Client workspace compatibility details.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceLinkingCompatibility(clients, config={}) {
        var uriPath = this.uriPath + "/linkedworkspaces/compatibility";
        config.clients = clients;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.clients;
    }
    /**
     * Link the specified client workspaces to the master workspace.
     * @method linkWorkspaces
     * @param {JSONArray} clients - Contains the client workspaces to be linked with the master workspace.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async linkWorkspaces(clients, config={}) {
        var uriPath = this.uriPath + "/linkedworkspaces";
        config.clients = clients;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    /**
     * Unlink the client workspaces from the specified master workspace.
     * @method unlinkWorkspaces
     * @param {String} scope - Scope of the unlink operation.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async unlinkWorkspaces(scope, config={}) {
        var uriPath = this.uriPath + "/linkedworkspaces";
        config.scope = scope;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }
    /**
     * Sync the metadata of the master workspace to its linked client workspaces.
     * @method syncLinkedWorkspaces
     * @param {String} scope - Scope of the sync operation.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async syncLinkedWorkspaces(scope, config={}) {
        var uriPath = this.uriPath + "/linkedworkspaces/sync";
        config.scope = scope;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    /**
     * Returns the sync details of the specified linked workspaces.
     * @method getLinkedWorkspaceSyncDetails
     * @param {JSONArray} sandboxIds - Ids of the linked workspaces for which the sync details are fetched.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {JSONArray} Linked workspace sync details.
     * @throws {Error} If the request failed due to some error.
     */
    async getLinkedWorkspaceSyncDetails(sandboxIds, config={}) {
        var uriPath = this.uriPath + "/linkedworkspaces/sync";
        config.sandboxIds = sandboxIds;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.workspaces;
    }
    /**
     * Returns the backup configuration and the list of backups available for the specified workspace.
     * @method getWorkspaceBackups
     * @returns {Object} Workspace backup details.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceBackups() {
        var uriPath = this.uriPath + "/backups";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Trigger an instant backup for the specified workspace.
     * @method backupWorkspaceNow
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Triggered backup details.
     * @throws {Error} If the request failed due to some error.
     */
    async backupWorkspaceNow(config={}) {
        var uriPath = this.uriPath + "/backups";
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result;
    }
    /**
     * Returns the status of the specified workspace backup.
     * @method getWorkspaceBackupStatus
     * @param {String} backupId - Id of the backup.
     * @returns {Object} Backup status details.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceBackupStatus(backupId) {
        var uriPath = this.uriPath + "/backups/" + backupId + "/status";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Download the specified workspace backup.
     * @method downloadWorkspaceBackup
     * @param {String} backupId - Id of the backup.
     * @param {String} filePath - Path of the file where the downloaded backup is to be stored.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async downloadWorkspaceBackup(backupId, filePath, config={}) {
        var uriPath = this.uriPath + "/backups/" + backupId + "/download";
        await this.ac.handleExportRequest(
            uriPath,
            config,
            this.header,
            { filePath: filePath }
        );
    }
    /**
     * Restore the specified workspace from the given backup.
     * @method restoreWorkspaceFromBackup
     * @param {String} backupId - Id of the backup.
     * @param {Boolean} confirmRestore - Pass true to confirm that the existing workspace data can be overwritten.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Triggered restore details.
     * @throws {Error} If the request failed due to some error.
     */
    async restoreWorkspaceFromBackup(backupId, confirmRestore, config={}) {
        var uriPath = this.uriPath + "/backups/" + backupId + "/restore";
        config.confirmRestore = confirmRestore;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result;
    }
    /**
     * Returns the status of the specified workspace restore.
     * @method getWorkspaceRestoreStatus
     * @param {String} restoreId - Id of the restore.
     * @returns {Object} Restore status details.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceRestoreStatus(restoreId) {
        var uriPath = this.uriPath + "/restores/" + restoreId + "/status";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Create a dashboard in the specified workspace.
     * @method createDashboard
     * @param {String} displayName - Name of the dashboard.
     * @param {String} layout - Layout configuration of the dashboard.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created dashboard id.
     * @throws {Error} If the request failed due to some error.
     */
    async createDashboard(displayName, layout, config={}) {
        var uriPath = this.uriPath + "/dashboards";
        config.displayName = displayName;
        config.layout = layout;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.dashboardId;
    }
    /**
     * Update the specified dashboard in the workspace.
     * @method updateDashboard
     * @param {String} dashboardId - Id of the dashboard.
     * @param {Object} config={} - Contains the dashboard configurations to be updated.
     * @throws {Error} If the request failed due to some error.
     */
    async updateDashboard(dashboardId, config={}) {
        var uriPath = this.uriPath + "/dashboards/" + dashboardId;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Returns the metadata of the specified dashboard.
     * @method getDashboardMetadata
     * @param {String} dashboardId - Id of the dashboard.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Dashboard configuration.
     * @throws {Error} If the request failed due to some error.
     */
    async getDashboardMetadata(dashboardId, config={}) {
        var uriPath = this.uriPath + "/dashboards/" + dashboardId + "/metadata";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.dashboardConfig;
    }
    /**
     * Returns the metadata of the specified report.
     * @method getReportMetadata
     * @param {String} viewId - Id of the report.
     * @returns {Object} Report configuration.
     * @throws {Error} If the request failed due to some error.
     */
    async getReportMetadata(viewId) {
        var uriPath = this.uriPath + "/reports/" + viewId + "/metadata";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.reportConfig;
    }
    /**
     * Returns list of data alerts available in the specified workspace.
     * @method getAlertsInWorkspace
     * @returns {JSONArray} Data alerts list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAlertsInWorkspace() {
        var uriPath = this.uriPath + "/alerts";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.alerts;
    }
    /**
     * Returns the configuration of the specified data alert.
     * @method getAlertConfiguration
     * @param {String} alertId - Id of the data alert.
     * @returns {Object} Data alert configuration.
     * @throws {Error} If the request failed due to some error.
     */
    async getAlertConfiguration(alertId) {
        var uriPath = this.uriPath + "/alerts/" + alertId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Update the specified data alert in the workspace.
     * @method updateAlert
     * @param {String} alertId - Id of the data alert.
     * @param {String} alertName - Name of the data alert.
     * @param {Object} scheduleDetails - Contains the schedule configurations of the data alert.
     * @param {JSONArray} rules - Contains the rules to be evaluated by the data alert.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateAlert(alertId, alertName, scheduleDetails, rules, config={}) {
        var uriPath = this.uriPath + "/alerts/" + alertId;
        config.alertName = alertName;
        config.scheduleDetails = scheduleDetails;
        config.rules = rules;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Delete the specified data alerts from the workspace.
     * @method deleteAlerts
     * @param {JSONArray} alertIds - Ids of the data alerts to be deleted.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteAlerts(alertIds, config={}) {
        var uriPath = this.uriPath + "/alerts";
        config.alertIds = alertIds;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }
    /**
     * Enable or disable the specified data alerts in the workspace.
     * @method changeAlertStatus
     * @param {JSONArray} alertIds - Ids of the data alerts.
     * @param {Boolean} enabled - Pass true to enable the data alerts and false to disable them.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async changeAlertStatus(alertIds, enabled, config={}) {
        var uriPath = this.uriPath + "/alerts/status";
        config.alertIds = alertIds;
        config.enabled = enabled;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }
    /**
     * Execute the specified data alert immediately.
     * @method runAlert
     * @param {String} alertId - Id of the data alert.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async runAlert(alertId, config={}) {
        var uriPath = this.uriPath + "/alerts/" + alertId + "/execute";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    /**
     * Returns the execution events of the specified data alert.
     * @method getAlertEvents
     * @param {String} alertId - Id of the data alert.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Data alert events along with the page details.
     * @throws {Error} If the request failed due to some error.
     */
    async getAlertEvents(alertId, config={}) {
        var uriPath = this.uriPath + "/alerts/" + alertId + "/events";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result;
    }
    /**
     * Returns the access restriction settings configured for the specified workspace.
     * @method getWorkspaceAccessRestrictions
     * @returns {Object} Workspace access restriction settings.
     * @throws {Error} If the request failed due to some error.
     */
    async getWorkspaceAccessRestrictions() {
        var uriPath = this.securityControlsUriPath + "/access-restrictions";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }
    /**
     * Update the access restriction settings of the specified workspace.
     * @method updateWorkspaceAccessRestrictions
     * @param {Object} config={} - Contains the access restriction configurations to be updated.
     * @throws {Error} If the request failed due to some error.
     */
    async updateWorkspaceAccessRestrictions(config={}) {
        var uriPath = this.securityControlsUriPath + "/access-restrictions";
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

}
class ViewAPI
{

    constructor(ac, orgId, workspaceId, viewId)
    {
        this.ac = ac;
        this.uriPath = "/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId
        this.header = {};
        this.header['ZANALYTICS-ORGID'] = orgId;
    }

    /**
     * Rename a specified view in the workspace.
     * @method rename
     * @param {String} viewName - New name of the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async rename(viewName, config={}) {
        config.viewName = viewName;
        await this.ac.handleV2Request(this.uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified view in the workspace.
     * @method delete
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async delete(config={}) {
        await this.ac.handleV2Request(this.uriPath, "DELETE", config, this.header);
    }

    /**
     * Copy a specified view within the workspace.
     * @method saveAs
     * @param {String} newViewName - The name of the new view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Newly created view id.
     * @throws {Error} If the request failed due to some error.
     */
    async saveAs(newViewName, config={}) {
        var uriPath = this.uriPath + "/saveas";
        config.viewName = newViewName;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.viewId;
    }

    /**
     * Copy the specified formulas from one table to another within the workspace or across workspaces.
     * @method copyFormulas
     * @param {JSONArray} formulaNames - The name of the formula columns to be copied.
     * @param {String} destWorkspaceId - The ID of the destination workspace.
     * @param {Object} config={} - Contains any additional control attributes.
     * @param {String} destOrgId=null - Id of the organization where the destination workspace is present.
     * @throws {Error} If the request failed due to some error.
     */
    async copyFormulas(formulaNames, destWorkspaceId, config={}, destOrgId=null) {
        var uriPath = this.uriPath + "/formulas/copy";
        config.formulaColumnNames = formulaNames;
        config.destWorkspaceId = destWorkspaceId;
        var reqHeader = this.header;
        if(destOrgId != null)
        {
          reqHeader['ZANALYTICS-DEST-ORGID'] = destOrgId;
        }
        await this.ac.handleV2Request(uriPath, "POST", config, reqHeader);
    }

    /**
     * Adds a specified view as favorite.
     * @method addFavorite
     * @throws {Error} If the request failed due to some error.
     */
    async addFavorite(config={})
    {
        var uriPath = this.uriPath + "/favorite";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove a specified view from favorite.
     * @method removeFavorite
     * @throws {Error} If the request failed due to some error.
     */
    async removeFavorite(config={})
    {
        var uriPath = this.uriPath + "/favorite";
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Create reports for the specified table based on the reference table.
     * @method createSimilarViews
     * @param {String} refViewId - The ID of the reference view.
     * @param {String} folderId - The folder id where the views to be saved.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async createSimilarViews(refViewId, folderId, config={}) {
        var uriPath = this.uriPath + "/similarviews";
        config.referenceViewId = refViewId;
        config.folderId = folderId;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Auto generate reports for the specified table.
     * @method autoAnalyse
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async autoAnalyse(config={}) {
        var uriPath = this.uriPath + "/autoanalyse";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Returns permissions for the specified view.
     * @method removeShare
     * @returns {Object} Permission details.
     * @throws {Error} If the request failed due to some error.
     */
    async getMyPermissions()
    {
        var uriPath = this.uriPath +  "/share/userpermissions";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.permissions;
    }

    /**
     * Returns the URL to access the specified view.
     * @method getViewUrl
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} View URL.
     * @throws {Error} If the request failed due to some error.
     */
    async getViewUrl(config={}) {
        var uriPath = this.uriPath + "/publish";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.viewUrl;
    }

    /**
     * Returns embed URL to access the specified view.
     * @method getEmbedUrl
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Embed URL.
     * @throws {Error} If the request failed due to some error.
     */
    async getEmbedUrl(config={}) {
        var uriPath = this.uriPath + "/publish/embed";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.embedUrl;
    }

    /**
     * Returns private URL to access the specified view.
     * @method getPrivateUrl
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Private URL.
     * @throws {Error} If the request failed due to some error.
     */
    async getPrivateUrl(config={}) {
        var uriPath = this.uriPath + "/publish/privatelink";
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.privateUrl;
    }

    /**
     * Create a private URL for the specified view.
     * @method createPrivateUrl
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Private URL.
     * @throws {Error} If the request failed due to some error.
     */
    async createPrivateUrl(config={}) {
        var uriPath = this.uriPath + "/publish/privatelink";
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.privateUrl;
    }

    /**
     * Remove private link access for the specified view.
     * @method removePrivateAccess
     * @throws {Error} If the request failed due to some error.
     */
    async removePrivateAccess() {
        var uriPath = this.uriPath + "/publish/privatelink";
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Make the specified view publically accessible.
     * @method makeViewPublic
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Public URL.
     * @throws {Error} If the request failed due to some error.
     */
    async makeViewPublic(config={}) {
        var uriPath = this.uriPath + "/publish/public";
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.publicUrl;
    }

    /**
     * Remove public access for the specified view.
     * @method removePublicAccess
     * @throws {Error} If the request failed due to some error.
     */
    async removePublicAccess() {
        var uriPath = this.uriPath + "/publish/public";
        await this.ac.handleV2Request(uriPath, "DELETE", null, this.header);
    }

    /**
     * Returns publish configurations for the specified view.
     * @method getPublishConfigurations
     * @returns {Object} Publish details.
     * @throws {Error} If the request failed due to some error.
     */
    async getPublishConfigurations()
    {
        var uriPath = this.uriPath +  "/publish/config";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Update publish configurations for the specified view.
     * @method updatePublishConfigurations
     * @param {Object} config={} - Contains the required control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updatePublishConfigurations(config={}) {
        var uriPath = this.uriPath + "/publish/config";
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Add a column in the specified table.
     * @method addColumn
     * @param {String} columnName - The name of the column.
     * @param {String} dataType - The data-type of the column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created column id.
     * @throws {Error} If the request failed due to some error.
     */
    async addColumn(columnName, dataType, config={}) {
        var uriPath = this.uriPath + "/columns";
        config.columnName = columnName;
        config.dataType = dataType;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.columnId;
    }

    /**
     * Hide the specified columns in the table.
     * @method hideColumns
     * @param {JSONArray} columnIds - Ids of the columns to be hidden.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async hideColumns(columnIds, config={}) {
        var uriPath = this.uriPath + "/columns/hide";
        config.columnIds = columnIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Show the specified hidden columns in the table.
     * @method showColumns
     * @param {JSONArray} columnIds - Ids of the columns to be shown.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async showColumns(columnIds, config={}) {
        var uriPath = this.uriPath + "/columns/show";
        config.columnIds = columnIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Add a single row in the specified table.
     * @method addRow
     * @param {Object} columnValues - Contains the values for the row. The column names are the key.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Column Names and Added Row Values.
     * @throws {Error} If the request failed due to some error.
     */
    async addRow(columnValues, config={})
    {
        var uriPath = this.uriPath + "/rows";
        config.columns = columnValues;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result;
    }


    /**
     * Update rows in the specified table.
     * @method updateRow
     * @param {Object} columnValues - Contains the values for the row. The column names are the key.
     * @param {String} criteria - The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {Object} Updated Columns List and Updated Rows Count.
     * @throws {Error} If the request failed due to some error.
     */
    async updateRow(columnValues, criteria, config={})
    {
        var uriPath = this.uriPath + "/rows";
        config.columns = columnValues;
        if(criteria != null && criteria.length>0)
        {
            config.criteria = criteria;
        }

        var result = await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
        return result;
    }

    /**
     * Delete rows in the specified table.
     * @method deleteRow
     * @param {String} criteria - The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {int} Deleted rows count.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteRow(criteria, config={})
    {
        var uriPath = this.uriPath + "/rows";
        if(criteria != null && criteria.length>0)
        {
            config.criteria = criteria;
        }

        var result = await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
        return result.deletedRows;
    }

    /**
     * Rename a specified column in the table.
     * @method renameColumn
     * @param {String} columnId - Id of the column.
     * @param {String} newColumnName - New name for the column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async renameColumn(columnId, newColumnName, config={}) {
        var uriPath = this.uriPath + "/columns/" + columnId;
        config.columnName = newColumnName;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete a specified column in the table.
     * @method deleteColumn
     * @param {String} columnId - Id of the column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteColumn(columnId, config={}) {
        var uriPath = this.uriPath + "/columns/" + columnId;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Add a lookup in the specified child table.
     * @method addLookup
     * @param {String} columnId - Id of the column.
     * @param {String} refViewId - The id of the table contains the parent column.
     * @param {String} refColumnId - The id of the parent column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addLookup(columnId, refViewId, refColumnId, config={}) {
        var uriPath = this.uriPath + "/columns/" + columnId + "/lookup";
        config.referenceViewId = refViewId;
        config.referenceColumnId = refColumnId;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Remove the lookup for the specified column in the table.
     * @method removeLookup
     * @param {String} columnId - Id of the column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeLookup(columnId, config={}) {
        var uriPath = this.uriPath + "/columns/" + columnId + "/lookup";
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Auto generate reports for the specified column.
     * @method autoAnalyseColumn
     * @param {String} columnId - Id of the column.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async autoAnalyseColumn(columnId, config={}) {
        var uriPath = this.uriPath + "/columns/" + columnId + "/autoanalyse";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Sync data from available datasource for the specified view.
     * @method refetchData
     * @param {String} viewName - New name of the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async refetchData(config={}) {
        var uriPath = this.uriPath + "/sync";
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }

    /**
     * Returns last import details of the specified view.
     * @method getLastImportDetails
     * @returns {int} Last import details.
     * @throws {Error} If the request failed due to some error.
     */
    async getLastImportDetails()
    {
        var uriPath = this.uriPath + "/importdetails";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Returns list of all formula columns for the specified table.
     * @method getFormulaColumns
     * @returns {JSONArray} Formula column list.
     * @throws {Error} If the request failed due to some error.
     */
    async getFormulaColumns()
    {
        var uriPath = this.uriPath + "/formulacolumns";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.formulaColumns;
    }

    /**
     * Add a formula column in the specified table.
     * @method addFormulaColumn
     * @param {String} formulaName - Name of the formula column to be created.
     * @param {String} expression - Formula expression.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created formula column id.
     * @throws {Error} If the request failed due to some error.
     */
    async addFormulaColumn(formulaName, expression, config={}) {
        var uriPath = this.uriPath + "/formulacolumns";
        config.formulaName = formulaName;
        config.expression = expression;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.formulaId;
    }

    /**
     * Edit the specified formula column.
     * @method editFormulaColumn
     * @param {String} formulaId - Id of the formula column to be updated.
     * @param {String} expression - Formula expression.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async editFormulaColumn(formulaId, expression, config={}) {
        var uriPath = this.uriPath + "/formulacolumns/" + formulaId;
        config.expression = expression;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete the specified formula column.
     * @method deleteFormulaColumn
     * @param {String} formulaId - Id of the formula column to be deleted.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteFormulaColumn(formulaId, config={}) {
        var uriPath = this.uriPath + "/formulacolumns/" + formulaId;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns list of all aggregate formulas for the specified table.
     * @method getAggregateFormulas
     * @returns {JSONArray} Aggregate formula list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAggregateFormulas()
    {
        var uriPath = this.uriPath + "/aggregateformulas";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.aggregateFormulas;
    }

    /**
     * Add a aggregate formula in the specified table.
     * @method addAggregateFormula
     * @param {String} formulaName - Name of the aggregate formula to be created.
     * @param {String} expression - Formula expression.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created aggregate formula id.
     * @throws {Error} If the request failed due to some error.
     */
    async addAggregateFormula(formulaName, expression, config={}) {
        var uriPath = this.uriPath + "/aggregateformulas";
        config.formulaName = formulaName;
        config.expression = expression;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.formulaId;
    }

    /**
     * Edit the specified aggregate formula.
     * @method editAggregateFormula
     * @param {String} formulaId - Id of the aggregate formula to be updated.
     * @param {String} expression - Formula expression.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async editAggregateFormula(formulaId, expression, config={}) {
        var uriPath = this.uriPath + "/aggregateformulas/" + formulaId;
        config.expression = expression;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Delete the specified aggregate formula.
     * @method deleteAggregateFormula
     * @param {String} formulaId - Id of the aggregate formula to be deleted.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async deleteAggregateFormula(formulaId, config={}) {
        var uriPath = this.uriPath + "/aggregateformulas/" + formulaId;
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns list of dependents views for the specified view.
     * @method getViewDependents
     * @returns {JSONArray} Dependent view list.
     * @throws {Error} If the request failed due to some error.
     */
    async getViewDependents()
    {
        var uriPath = this.uriPath + "/dependents";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.views;
    }

    /**
     * Returns list of dependents views and formulas for the specified column.
     * @method getColumnDependents
     * @param {String} columnId - Id of the column.
     * @returns {JSONObject} Dependent details.
     * @throws {Error} If the request failed due to some error.
     */
    async getColumnDependents(columnId)
    {
        var uriPath = this.uriPath + "/columns/" + columnId + "/dependents";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Update shared details of the specified view.
     * @method updateSharedDetails
     * @param {Object} config={} - Contains the control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async updateSharedDetails(config={})
    {
        var uriPath = this.uriPath + "/share";
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Retrieves metadata information for the current table, including
     * the list of available columns and associated attributes.
     * @method getTableMetadata
     * @returns {Object} Table metadata details.
     * @throws {Error} If the request failed due to some error.
     */
    async getTableMetadata() {
        var uriPath = this.uriPath + "/metadata";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Updates the column order of the current table.
     * @method reorderColumns
     * @param {Array} columnIds - Full set of column IDs in the new order.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async reorderColumns(columnIds, config = {}) {
        var uriPath = this.uriPath + "/columns/reorder";
        config.columns = columnIds;
        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }


    /**
     * Sorts the data in the table based on the specified columns.
     * @method sortDataByColumns
     * @param {Array|null} columns - List of column IDs to sort by.
     * @param {Number|null} sortOrder - 1 for ascending, 2 for descending.
     * @param {Boolean} resetSort - If true, resets existing sort.
     * @param {Object} config={} - Additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async sortDataByColumns(columns = null, sortOrder = null, resetSort = false, config = {}) {

        var uriPath = this.uriPath + "/data/sort";

        if (resetSort) {
            config.resetSort = "true";
        } else {
            config.sortOrder = sortOrder;
            config.columns = columns;
        }

        await this.ac.handleV2Request(uriPath, "PUT", config, this.header);
    }

    /**
     * Returns list of tags associated with the specified view.
     * @method getViewTags
     * @returns {JSONArray} Tags list.
     * @throws {Error} If the request failed due to some error.
     */
    async getViewTags() {
        var uriPath = this.uriPath + "/tags";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.tags;
    }
    /**
     * Adds multiple tags to the specified view.
     * @method addTagsToView
     * @param {JSONArray} tagIds - Tag ids to be associated with the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async addTagsToView(tagIds, config={}) {
        var uriPath = this.uriPath + "/tags";
        config.tagIds = tagIds;
        await this.ac.handleV2Request(uriPath, "POST", config, this.header);
    }
    /**
     * Removes multiple tags from the specified view.
     * @method removeTagsFromView
     * @param {JSONArray} tagIds - Tag ids to be dissociated. Not required when dissociateAll is true.
     * @param {Boolean} dissociateAll - To dissociate all the associated tags from the view.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async removeTagsFromView(tagIds=null, dissociateAll=false, config={}) {
        var uriPath = this.uriPath + "/tags";
        if(dissociateAll) {
            config.dissociateAll = true;
        } else {
            config.tagIds = tagIds;
        }
        await this.ac.handleV2Request(uriPath, "DELETE", config, this.header);
    }

    /**
     * Returns list of data alerts configured for the specified view.
     * @method getAlertsInView
     * @returns {JSONArray} Data alerts list.
     * @throws {Error} If the request failed due to some error.
     */
    async getAlertsInView() {
        var uriPath = this.uriPath + "/alerts";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result.alerts;
    }
    /**
     * Create a data alert for the specified view.
     * @method createAlert
     * @param {String} alertName - Name of the data alert.
     * @param {Object} scheduleDetails - Contains the schedule configurations of the data alert.
     * @param {JSONArray} rules - Contains the rules to be evaluated by the data alert.
     * @param {Object} config={} - Contains any additional control attributes.
     * @returns {String} Created data alert id.
     * @throws {Error} If the request failed due to some error.
     */
    async createAlert(alertName, scheduleDetails, rules, config={}) {
        var uriPath = this.uriPath + "/alerts";
        config.alertName = alertName;
        config.scheduleDetails = scheduleDetails;
        config.rules = rules;
        var result = await this.ac.handleV2Request(uriPath, "POST", config, this.header);
        return result.alertId;
    }
    /**
     * Returns the view metadata that can be used while configuring a data alert for the specified view.
     * @method getViewMetadataForAlert
     * @returns {Object} View metadata for data alert configuration.
     * @throws {Error} If the request failed due to some error.
     */
    async getViewMetadataForAlert() {
        var uriPath = this.uriPath + "/alerts/metadata";
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

}
class BulkAPI
{

    constructor(ac, orgId, workspaceId)
    {
        this.ac = ac;
        this.uriPath = "/restapi/v2/workspaces/" + workspaceId
        this.bulkUriPath = "/restapi/v2/bulk/workspaces/" + workspaceId
        this.header = {};
        this.header['ZANALYTICS-ORGID'] = orgId;
    }

    /**
     * Create a new table and import the data contained in the mentioned file into the created table.
     * @method importDataInNewTable
     * @param {String} tableName - Name of the new table to be created.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {JSONObject} Import result.
     * @throws {Error} If the request failed due to some error.
     */
    async importDataInNewTable(tableName, fileType, autoIdentify, filePath, config={})
    {
        var uriPath = this.uriPath + "/data";
        config.tableName = tableName;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleImportRequest(uriPath, config, this.header, filePath);
        return result;
    }

    /**
     * Create a new table and import the raw data provided into the created table.
     * @method importRawDataInNewTable
     * @param {String} tableName - Name of the new table to be created.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} data - Raw data to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {JSONObject} Import result.
     * @throws {Error} If the request failed due to some error.
     */
    async importRawDataInNewTable(tableName, fileType, autoIdentify, data, config={})
    {
        var uriPath = this.uriPath + "/data";
        config.tableName = tableName;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleImportRequest(uriPath, config, this.header, null, data);
        return result;
    }

    /**
     * Import the data contained in the mentioned file into the table.
     * @method importData
     * @param {String} viewId - Id of the view where the data to be imported.
     * @param {String} importType - The type of import. Can be one of - append, truncateadd, updateadd.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {JSONObject} Import result.
     * @throws {Error} If the request failed due to some error.
     */
    async importData(viewId, importType, fileType, autoIdentify, filePath, config={})
    {
        var uriPath = this.uriPath + "/views/" + viewId + "/data";
        config.importType = importType;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;
        
        var result = await this.ac.handleImportRequest(uriPath, config, this.header, filePath);
        return result;
    }

    /**
     * Import the raw data provided into the table.
     * @method importRawData
     * @param {String} viewId - Id of the view where the data to be imported.
     * @param {String} importType - The type of import. Can be one of - append, truncateadd, updateadd.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} data - Raw data to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {JSONObject} Import result.
     * @throws {Error} If the request failed due to some error.
     */
    async importRawData(viewId, importType, fileType, autoIdentify, data, config={})
    {
        var uriPath = this.uriPath + "/views/" + viewId + "/data";
        config.importType = importType;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleImportRequest(uriPath, config, this.header, null, data);
        return result;
    }

    /**
     * Asynchronously create a new table and import the data contained in the mentioned file into the created table.
     * @method importBulkDataInNewTable
     * @param {String} tableName - Name of the new table to be created.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {String} Import job id.
     * @throws {Error} If the request failed due to some error.
     */
    async importBulkDataInNewTable(tableName, fileType, autoIdentify, filePath, config={})
    {
        var uriPath = this.bulkUriPath + "/data";
        config.tableName = tableName;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleImportRequest(uriPath, config, this.header, filePath);
        return result.jobId;
    }
    
    /**
     * Create a new table and import the data contained in the mentioned file into the created table.
     * @method importDataInNewTableAsBatches
     * @param {String} tableName - Name of the new table to be created.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Number} batchSize - Number of lines per batch.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {JSONObject} Import result.
     * @throws {Error} If the request failed due to some error.
     */
    async importDataInNewTableAsBatches(tableName, autoIdentify, filePath, batchSize, config={})
    {
        var uriPath = this.bulkUriPath + "/data/batch";
        config.tableName = tableName;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleBatchImportRequest(uriPath, config, this.header, filePath, batchSize);
        return result;
    }

    /**
     * Asynchronously import the data contained in the mentioned file into the table.
     * @method importBulkDataAsBatches
     * @param {String} viewId - Id of the view where the data to be imported.
     * @param {String} importType - The type of import. Can be one of - append, truncateadd, updateadd.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Number} batchSize - Number of lines per batch.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {String} Import job id.
     * @throws {Error} If the request failed due to some error.
     */
    async importBulkDataAsBatches(viewId, importType, autoIdentify, filePath, batchSize, config={})
    {
        var uriPath = this.bulkUriPath + "/views/" + viewId + "/data/batch";
        config.importType = importType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleBatchImportRequest(uriPath, config, this.header, filePath, batchSize);
        return result;
    }
    
    /**
     * Asynchronously import the data contained in the mentioned file into the table.
     * @method importBulkData
     * @param {String} viewId - Id of the view where the data to be imported.
     * @param {String} importType - The type of import. Can be one of - append, truncateadd, updateadd.
     * @param {String} fileType - Type of the file to be imported.
     * @param {String} autoIdentify - Used to specify whether to auto identify the CSV format. Allowable values - true/false.
     * @param {String} filePath - Path of the file to be imported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {String} Import job id.
     * @throws {Error} If the request failed due to some error.
     */
    async importBulkData(viewId, importType, fileType, autoIdentify, filePath, config={})
    {
        var uriPath = this.bulkUriPath + "/views/" + viewId + "/data";
        config.importType = importType;
        config.fileType = fileType;
        config.autoIdentify = autoIdentify;

        var result = await this.ac.handleImportRequest(uriPath, config, this.header, filePath);
        return result.jobId;
    }

    /**
     * Returns the details of the import job.
     * @method getImportJobDetails
     * @param {String} jobId - Id of the job.
     * @return {JSONObject} Import job details.
     * @throws {Error} If the request failed due to some error.
     */
    async getImportJobDetails(jobId)
    {
        var uriPath = this.bulkUriPath + "/importjobs/" + jobId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Export the mentioned table (or) view data.
     * @method exportData
     * @param {String} viewId - Id of the view to be exported.
     * @param {String} responseFormat - The format in which the data is to be exported.
     * @param {String} filePath - Path of the file where the data exported to be stored.
     * @param {Object} config={} - Contains any additional control attributes.
     * @throws {Error} If the request failed due to some error.
     */
    async exportData(viewId, responseFormat, filePath, config={})
    {
        var uriPath = this.uriPath + "/views/" + viewId + "/data";
        config.responseFormat = responseFormat;
        await this.ac.handleExportRequest(
            uriPath,
            config,
            this.header,
            { filePath: filePath }
        );
    }

    /**
     * Export the mentioned table (or) view data as a stream.
     *
     * @param {String} viewId - Id of the view to be exported
     * @param {String} responseFormat - Export format (csv, xls, json, etc.)
     * @param {Object} config - Additional control parameters (optional)
     * @returns {Promise<ReadableStream>} - Stream containing exported data
     */
    async exportDataStream(viewId, responseFormat, config = {}) {
        var uriPath = this.uriPath + "/views/" + viewId + "/data";
        config.responseFormat = responseFormat;

        return await this.ac.handleExportRequest(
            uriPath,
            config,
            this.header,
            { stream: true }
        );
    }


    /**
     * Initiate asynchronous export for the mentioned table (or) view data.
     * @method initiateBulkExport
     * @param {String} viewId - Id of the view to be exported.
     * @param {String} responseFormat - The format in which the data is to be exported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {String} Export job id.
     * @throws {Error} If the request failed due to some error.
     */
    async initiateBulkExport(viewId, responseFormat, config={})
    {
        var uriPath = this.bulkUriPath + "/views/" + viewId + "/data";
        config.responseFormat = responseFormat;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.jobId;
    }

    /**
     * Initiate asynchronous export with the given SQL Query.
     * @method initiateBulkExportUsingSQL
     * @param {String} sqlQuery - The SQL Query whose output is exported.
     * @param {String} responseFormat - The format in which the data is to be exported.
     * @param {Object} config={} - Contains any additional control attributes.
     * @return {String} Export job id.
     * @throws {Error} If the request failed due to some error.
     */
    async initiateBulkExportUsingSQL(sqlQuery, responseFormat, config={})
    {
        var uriPath = this.bulkUriPath + "/data";
        config.sqlQuery = sqlQuery;
        config.responseFormat = responseFormat;
        var result = await this.ac.handleV2Request(uriPath, "GET", config, this.header);
        return result.jobId;
    }

    /**
     * Returns the details of the export job.
     * @method getExportJobDetails
     * @param {String} jobId - Id of the export job.
     * @return {JSONObject} Export job details.
     * @throws {Error} If the request failed due to some error.
     */
    async getExportJobDetails(jobId)
    {
        var uriPath = this.bulkUriPath + "/exportjobs/" + jobId;
        var result = await this.ac.handleV2Request(uriPath, "GET", null, this.header);
        return result;
    }

    /**
     * Download the exported data for the mentioned job id.
     * @method exportBulkData
     * @param {String} jobId - Id of the job to be exported.
     * @param {String} filePath - Path of the file where the data exported to be stored.
     * @throws {Error} If the request failed due to some error.
     */
    async exportBulkData(jobId, filePath)
    {
        var uriPath = this.bulkUriPath + "/exportjobs/" + jobId + "/data";

        await this.ac.handleExportRequest(
            uriPath,
            null,
            this.header,
            { filePath: filePath }
        );
    }

    /**
     * Download the exported bulk data for the given job id as a stream.
     *
     * @param {String} jobId - Export job id
     * @returns {Promise<ReadableStream>} - Stream containing exported data
     */
    async exportBulkDataStream(jobId) {
        const uriPath = this.bulkUriPath + '/exportjobs/' + jobId + '/data';

        return await this.ac.handleExportRequest(
            uriPath,
            null,
            this.header,
            { stream: true }
        );
    }


}


module.exports = AnalyticsClient;

