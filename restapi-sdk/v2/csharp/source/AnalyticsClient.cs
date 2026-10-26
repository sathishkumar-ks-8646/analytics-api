using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Web;

namespace ZohoAnalytics
{
    /// <summary>
    /// AnalyticsClient provides the C# based language binding to the HTTPS based API of Zoho Analytics.
    /// </summary>
    public class AnalyticsClient : IAnalyticsClient
    {
        /// <exclude></exclude>
        private const string _clientVersion = "2.9.0";

        /// <exclude></exclude>
        private string _analyticsServerURL = "https://@@ANALYTICS_URL";

        /// <exclude></exclude>
        private string _accountsServerURL = "https://@@ACCOUNTS_URL";



        /// <exclude></exclude>
        private readonly string _clientId;

        /// <exclude></exclude>
        private readonly string _clientSecret;

        /// <exclude></exclude>
        private readonly string _refreshToken;

        /// <exclude></exclude>
        private string _accessToken;


        /// <exclude></exclude>
        private int _connectionTimeout = 0;

        /// <exclude></exclude>
        private int _readTimeout = 0;



        /// <exclude></exclude>
        private bool _proxy = false;

        /// <exclude></exclude>
        private string _proxyHost;

        /// <exclude></exclude>
        private int _proxyPort;

        /// <exclude></exclude>
        private string _proxyUsername;

        /// <exclude></exclude>
        private string _proxyPassword;

        /// <summary>
        /// Creates a new AnalyticsClient instance.
        /// </summary>
        /// <param name="clientId">The client ID string that has been obtained during the client registration.</param>
        /// <param name="clientSecret">The client secret string that has been obtained during the client registration.</param>
        /// <param name="refreshToken">The refresh token string that has been obtained through accounts API.</param>
        public AnalyticsClient(string clientId, string clientSecret, string refreshToken)
        {
            _clientId = clientId;
            _clientSecret = clientSecret;
            _refreshToken = refreshToken;
            _accessToken = refreshToken;
        }

        /// <summary>
        /// Creates a new OrgAPI instance.
        /// </summary>
        /// <param name="orgId">The ID of the organization.</param>
        /// <returns>OrgAPI instance.</returns>
        public IOrgAPI GetOrgInstance(long orgId)
        {
            return new OrgAPI(this, orgId);
        }

        /// <summary>
        /// Creates a new WorkspaceAPI instance.
        /// </summary>
        /// <param name="orgId">The ID of the organization.</param>
        /// <param name="workspaceId">The ID of the workspace.</param>
        /// <returns>WorkspaceAPI instance.</returns>
        public IWorkspaceAPI GetWorkspaceInstance(long orgId, long workspaceId)
        {
            return new WorkspaceAPI(this, orgId, workspaceId);
        }

        /// <summary>
        /// Creates a new ViewAPI instance.
        /// </summary>
        /// <param name="orgId">The ID of the organization.</param>
        /// <param name="workspaceId">The ID of the workspace.</param>
        /// <param name="viewId">The ID of the view.</param>
        /// <returns>ViewAPI instance.</returns>
        public IViewAPI GetViewInstance(long orgId, long workspaceId, long viewId)
        {
            return new ViewAPI(this, orgId, workspaceId, viewId);
        }

        /// <summary>
        /// Creates a new BulkAPI instance.
        /// </summary>
        /// <param name="orgId">The ID of the organization.</param>
        /// <param name="workspaceId">The ID of the workspace.</param>
        /// <returns>BulkAPI instance.</returns>
        public IBulkAPI GetBulkInstance(long orgId, long workspaceId)
        {
            return new BulkAPI(this, orgId, workspaceId);
        }

        /// <summary>
        /// Returns list of all accessible organizations.
        /// </summary>
        /// <returns>Organizations list.</returns>
        public JsonElement GetOrgs()
        {
            string endPoint = "/restapi/v2/orgs";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("orgs"));
        }

        /// <summary>
        /// Returns list of all accessible workspaces.
        /// </summary>
        /// <returns>All workspaces list.</returns>
        public JsonElement GetWorkspaces()
        {
            string endPoint = "/restapi/v2/workspaces";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Returns list of owned workspaces.
        /// </summary>
        /// <returns>Owned workspaces list.</returns>
        public JsonElement GetOwnedWorkspaces()
        {
            string endPoint = "/restapi/v2/workspaces/owned";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("workspaces"));
        }

        /// <summary>
        /// Returns list of shared workspaces.
        /// </summary>
        /// <returns>Shared workspaces list.</returns>
        public JsonElement GetSharedWorkspaces()
        {
            string endPoint = "/restapi/v2/workspaces/shared";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("workspaces"));
        }

        /// <summary>
        /// Returns list of recently accessed views.
        /// </summary>
        /// <returns>Recent views list.</returns>
        public JsonElement GetRecentViews()
        {
            string endPoint = "/restapi/v2/recentviews";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("views"));
        }

        /// <summary>
        /// Returns list of all accessible dashboards.
        /// </summary>
        /// <returns>All dashboards list.</returns>
        public JsonElement GetDashboards()
        {
            string endPoint = "/restapi/v2/dashboards";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("dashboards"));
        }

        /// <summary>
        /// Returns list of owned dashboards.
        /// </summary>
        /// <returns>Owned dashboards list.</returns>
        public JsonElement GetOwnedDashboards()
        {
            string endPoint = "/restapi/v2/dashboards/owned";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("dashboards"));
        }

        /// <summary>
        /// Returns list of shared dashboards.
        /// </summary>
        /// <returns>Shared dashboards list.</returns>
        public JsonElement GetSharedDashboards()
        {
            string endPoint = "/restapi/v2/dashboards/shared";
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("dashboards"));
        }

        /// <summary>
        /// Returns details of the specified workspace.
        /// </summary>
        /// <param name="workspaceId">Id of the workspace.</param>
        /// <returns>Workspace details.</returns>
        public JsonElement GetWorkspaceDetails(long workspaceId)
        {
            string endPoint = "/restapi/v2/workspaces/" + workspaceId;
            dynamic response = SendAPIRequest("GET", endPoint, null, null);
            return (response.GetProperty("data").GetProperty("workspaces"));
        }

        /// <summary>
        /// Returns details of the specified view.
        /// </summary>
        /// <param name="viewId">Id of the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>View details.</returns>
        public JsonElement GetViewDetails(long viewId, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/views/" + viewId;
            dynamic response = SendAPIRequest("GET", endPoint, config, null);
            return (response.GetProperty("data").GetProperty("views"));
        }

        /// <summary>
        /// Sets the analytics server URL.
        /// </summary>
        /// <param name="serverUrl">ZohoAnalytics server URL</param>
        public void SetAnalyticsServerURL(string serverUrl)
        {
            _analyticsServerURL = serverUrl;
        }

        /// <summary>
        /// Sets the accounts server URL.
        /// </summary>
        /// <param name="serverUrl">ZohoAccounts server URL</param>
        public void SetAccountsServerURL(string serverUrl)
        {
            _accountsServerURL = serverUrl;
        }

        /// <summary>
        /// Returns the timeout until a connection is established.
        /// </summary>
        /// <returns>The timeout value.</returns>
        public int GetConnectionTimeout()
        {
            return _connectionTimeout;
        }

        /// <summary>
        /// Sets the timeout until a connection is established.
        /// </summary>
        /// <param name="timeout">The timeout value.</param>
        public void SetConnectionTimeout(int timeout)
        {
            _connectionTimeout = timeout;
        }

        /// <summary>
        /// Returns the read timeout value which will wait for the packet to receive from the server end.
        /// </summary>
        /// <returns>The timeout value.</returns>
        public int GetReadTimeout()
        {
            return _readTimeout;
        }

        /// <summary>
        /// Sets the read timeout which will wait for data response from the server end.
        /// </summary>
        /// <param name="timeout">The timeout value.</param>
        public void SetReadTimeout(int timeout)
        {
            _readTimeout = timeout;
        }

        /// <summary>
        /// To specify the proxy server details.
        /// </summary>
        /// <param name="proxyHost">The hostname/IP address of the proxy server.</param>
        /// <param name="proxyPort">The proxy server port.</param>
        /// <param name="proxyUsername">The user name for proxy-server authentication.</param>
        /// <param name="proxyPassword">The password for proxy server authentication.</param>
        public void SetProxy(string proxyHost, int proxyPort, string proxyUsername, string proxyPassword)
        {
            _proxy = true;
            _proxyHost = proxyHost;
            _proxyPort = proxyPort;
            _proxyUsername = proxyUsername;
            _proxyPassword = proxyPassword;
        }

        /// <exclude></exclude>
        internal dynamic SendImportAPIRequest(string endPoint, Dictionary<string, object> config, Dictionary<string, string> _reqHeaders, string filePath, string rawData)
        {
            bool isRawDataImport = (rawData != null);
            DebugLog($"SendImportAPIRequest: endpoint={endPoint} | isRawDataImport={isRawDataImport} | filePath={filePath}");
            if (_accessToken == null)
            {
                DebugLog("SendImportAPIRequest: Access token is null, regenerating OAuth token.");
                RegenerateOAuthToken();
            }

            string reqUrl = _analyticsServerURL + endPoint;

            string parameters = "";
            if (config != null)
            {
                parameters = parameters + "CONFIG=" + HttpUtility.UrlEncode(JsonSerializer.Serialize(config));
            }

            if (!string.IsNullOrEmpty(parameters))
            {
                reqUrl = reqUrl + "?" + parameters;
            }

            string postBody = null;
            if (isRawDataImport)
            {
                postBody = "DATA=" + HttpUtility.UrlEncode(rawData);
            }

            DebugLog($"SendImportAPIRequest: Request URL constructed | isRawDataImport={isRawDataImport}");

            Dictionary<string, string> responseObj;
            if (isRawDataImport)
            {
                responseObj = SubmitRequest("POST", reqUrl, _reqHeaders, _accessToken, postBody);
            }
            else
            {
                responseObj = SubmitImportRequest(reqUrl, _reqHeaders, _accessToken, filePath);
            }

            dynamic jObj = null;
            string statusCode = null;
            string response = null;
            responseObj.TryGetValue("httpStatusCode", out statusCode);

            responseObj.TryGetValue("response", out response);
            DebugLog($"SendImportAPIRequest: HTTP {statusCode} | Response: {response}");

            if (!statusCode.StartsWith("2") && IsOAuthExpired(response))
            {
                DebugLog("SendImportAPIRequest: OAuth expired, regenerating and retrying.");
                RegenerateOAuthToken();
                if (isRawDataImport)
                {
                    responseObj = SubmitRequest("POST", reqUrl, _reqHeaders, _accessToken, postBody);
                }
                else
                {
                    responseObj = SubmitImportRequest(reqUrl, _reqHeaders, _accessToken, filePath);
                }
                responseObj.TryGetValue("httpStatusCode", out statusCode);
                responseObj.TryGetValue("response", out response);
                DebugLog($"SendImportAPIRequest: Retry HTTP {statusCode} | Response: {response}");
            }

            if (!statusCode.StartsWith("2"))
            {
                try
                {
                    JsonDocument jsonDocument = JsonDocument.Parse(response);
                    jObj = jsonDocument.RootElement;
                    int errorCode = jObj.GetProperty("data").GetProperty("errorCode").GetInt32();
                    string errorMessage = jObj.GetProperty("data").GetProperty("errorMessage").GetString();
                    DebugLog($"SendImportAPIRequest: ServerException - ErrorCode={errorCode} | ErrorMessage={errorMessage} | HTTP {statusCode}");
                    throw new ServerException(int.Parse(statusCode), errorCode, errorMessage);
                }
                catch (ServerException ex)
                {
                    throw ex;
                }
                catch (Exception ex)
                {
                    DebugLog($"SendImportAPIRequest: Exception - {ex.Message}");
                    throw new Exception("Error Occured - " + ex.Message);
                }
            }
            else if (!string.IsNullOrEmpty(response))
            {
                DebugLog("SendImportAPIRequest: Success.");
                JsonDocument jsonDocument = JsonDocument.Parse(response);
                jObj = jsonDocument.RootElement;
            }
            return jObj;
        }

        /// <exclude></exclude>
        internal string ReadNextRawCsvRecordString(StreamReader reader, char quoteChar)
        {
            if (reader.EndOfStream)
                return null;

            var recordBuilder = new StringBuilder();
            bool inQuotes = false;

            while (true)
            {
                string line = reader.ReadLine();

                if (line == null)
                {
                    // End of stream: return whatever has been collected
                    return recordBuilder.Length > 0 ? recordBuilder.ToString() : null;
                }

                int i = 0;
                while (i < line.Length)
                {
                    char current = line[i];

                    if (quoteChar != '\0' && current == quoteChar)
                    {
                        // Handle escaped quote (e.g. '' or "")
                        bool isEscaped = (i + 1 < line.Length) && line[i + 1] == quoteChar;

                        if (isEscaped)
                        {
                            // Skip both quotes (escaped)
                            i += 2;
                            continue;
                        }
                        else
                        {
                            // Toggle quote state
                            inQuotes = !inQuotes;
                        }
                    }

                    i++;
                }

                recordBuilder.Append(line);

                if (!inQuotes)
                {
                    // This line completes the record
                    return recordBuilder.ToString();
                }
                else
                {
                    // Multiline record still open
                    recordBuilder.AppendLine(); // preserve newline
                }
            }
        }

        // No logging unless explicitly enabled via SetDebugLogPath
        private static string _logFile = null;

        /// <summary>
        /// Sets the file path for the debug log.
        /// Call this before making any API calls.
        /// </summary>
        /// <param name="logFilePath">Full path to the log file. E.g. "C:\Logs\ZohoAnalytics.log"</param>
        public static void SetDebugLogPath(string logFilePath)
        {
            if (string.IsNullOrWhiteSpace(logFilePath))
                throw new ArgumentException("Log file path cannot be null or empty.");

            string directory = Path.GetDirectoryName(logFilePath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                Directory.CreateDirectory(directory); // create folder if it doesn't exist

            _logFile = logFilePath;
        }

        private static void DebugLog(string message)
        {
            if (_logFile == null)
                return;

            try
            {
                File.AppendAllText(_logFile,
                    $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] {message}{Environment.NewLine}");
            }
            catch { /* never let logging break the import */ }
        }

        /// <exclude></exclude>
        internal dynamic SendBatchImportAPIRequest(string endPoint, Dictionary<string, object> config, Dictionary<string, string> _reqHeaders, string filePaths, int batchSize)
        {
            if (_accessToken == null)
            {
                RegenerateOAuthToken();
            }

            dynamic jObj = null;
            config["isLastBatch"] = "false";
            config["batchKey"] = "start";

            char quoteChar = '"';
            if (config.TryGetValue("quoted", out object quoteValueObj))
            {
                int quoteCode = -1;
                if (quoteValueObj is int i) quoteCode = i;
                else if (quoteValueObj is string s && int.TryParse(s, out int parsed)) quoteCode = parsed;

                switch (quoteCode)
                {
                    case 0: quoteChar = '\0'; break;
                    case 1: quoteChar = '\''; break;
                    case 2: quoteChar = '"'; break;
                    default: quoteChar = '"'; break;
                }
            }

            Encoding fileEncoding = Encoding.UTF8;

            int batchNumber = 0;

            using (var reader = new StreamReader(filePaths, fileEncoding, detectEncodingFromByteOrderMarks: true))
            {
                string header = ReadNextRawCsvRecordString(reader, quoteChar);
                if (header == null)
                {
                    DebugLog("File is empty or header could not be read.");
                    return null;
                }

                DebugLog($"Header read successfully: {header}");

                string nextRecordBuffer = null;
                bool hasMoreRecords = true;

                while (hasMoreRecords)
                {
                    batchNumber++;
                    var chunk = new List<string>();

                    for (int i = 0; i < batchSize; i++)
                    {
                        string record;
                        if (nextRecordBuffer != null)
                        {
                            record = nextRecordBuffer;
                            nextRecordBuffer = null;
                        }
                        else
                        {
                            record = ReadNextRawCsvRecordString(reader, quoteChar);
                        }

                        if (record != null)
                            chunk.Add(record);
                        else
                        {
                            hasMoreRecords = false;
                            break;
                        }
                    }

                    if (!chunk.Any())
                    {
                        DebugLog($"Batch {batchNumber}: Empty chunk, stopping.");
                        break;
                    }

                    nextRecordBuffer = ReadNextRawCsvRecordString(reader, quoteChar);
                    hasMoreRecords = nextRecordBuffer != null;
                    config["isLastBatch"] = (!hasMoreRecords).ToString().ToLower();

                    DebugLog($"Batch {batchNumber}: {chunk.Count} records | isLastBatch: {config["isLastBatch"]}");

                    string reqUrl = _analyticsServerURL + endPoint;
                    string parameters = "CONFIG=" + HttpUtility.UrlEncode(JsonSerializer.Serialize(config));
                    reqUrl += "?" + parameters;

                    string tempfilePath = Path.Combine(Path.GetTempPath(),
                        $"TempFile_{DateTime.Now:yyyyMMddHHmmssfff}_{Guid.NewGuid()}.csv");

                    try
                    {
                        using (var writer = new StreamWriter(tempfilePath, false, Encoding.UTF8))
                        {
                            writer.WriteLine(header);
                            foreach (var line in chunk)
                                writer.WriteLine(line);
                        }

                        DebugLog($"Batch {batchNumber}: Temp file created at {tempfilePath}");

                        var responseObj = SubmitImportRequest(reqUrl, _reqHeaders, _accessToken, tempfilePath);
                        responseObj.TryGetValue("httpStatusCode", out string statusCode);
                        responseObj.TryGetValue("response", out string response);

                        DebugLog($"Batch {batchNumber}: HTTP {statusCode} | Response: {response}");

                        if (!statusCode.StartsWith("2") && IsOAuthExpired(response))
                        {
                            DebugLog($"Batch {batchNumber}: OAuth expired, regenerating and retrying.");
                            RegenerateOAuthToken();
                            responseObj = SubmitImportRequest(reqUrl, _reqHeaders, _accessToken, tempfilePath);
                            responseObj.TryGetValue("httpStatusCode", out statusCode);
                            responseObj.TryGetValue("response", out response);
                            DebugLog($"Batch {batchNumber}: Retry HTTP {statusCode} | Response: {response}");
                        }

                        if (!statusCode.StartsWith("2"))
                        {
                            try
                            {
                                // Guard against HTML/non-JSON responses
                                if (string.IsNullOrWhiteSpace(response) || !response.TrimStart().StartsWith("{"))
                                {
                                    string preview = response?.Substring(0, Math.Min(300, response?.Length ?? 0));
                                    DebugLog($"Batch {batchNumber}: Non-JSON response (HTTP {statusCode}): {preview}");
                                    throw new Exception($"Non-JSON response (HTTP {statusCode}): {preview}");
                                }

                                JsonDocument jsonDocument = JsonDocument.Parse(response);
                                jObj = jsonDocument.RootElement;
                                int errorCode = jObj.GetProperty("data").GetProperty("errorCode").GetInt32();
                                string errorMessage = jObj.GetProperty("data").GetProperty("errorMessage").GetString();

                                // Construct ServerException and log using its own methods before throwing
                                var serverEx = new ServerException(int.Parse(statusCode), errorCode, errorMessage);
                                DebugLog($"Batch {batchNumber}: ServerException - " +
                                        $"HTTP {serverEx.GetHTTPStatusCode()} | " +
                                        $"ErrorCode {serverEx.GetErrorCode()} | " +
                                        $"Message: {serverEx.GetErrorMessage()}");
                                throw serverEx;
                            }
                            catch (ServerException) { throw; }
                            catch (Exception ex)
                            {
                                DebugLog($"Batch {batchNumber}: Exception - {ex.Message}");
                                throw new Exception("Error Occurred - " + ex.Message);
                            }
                        }
                        else if (!string.IsNullOrEmpty(response))
                        {
                            JsonDocument jsonDocument = JsonDocument.Parse(response);
                            jObj = jsonDocument.RootElement;
                            config["batchKey"] = jObj.GetProperty("data").GetProperty("batchKey").GetString();
                            DebugLog($"Batch {batchNumber}: Success. batchKey = {config["batchKey"]}");
                        }
                    }
                    catch (ServerException ex)
                    {
                        // Log all three fields via ServerException's own methods
                        DebugLog($"Batch {batchNumber}: ServerException caught - " +
                                $"HTTP {ex.GetHTTPStatusCode()} | " +
                                $"ErrorCode {ex.GetErrorCode()} | " +
                                $"Message: {ex.GetErrorMessage()}");
                        throw;
                    }
                    catch (Exception ex)
                    {
                        DebugLog($"Batch {batchNumber}: General exception - {ex.Message}");
                        throw;
                    }
                    finally
                    {
                        if (File.Exists(tempfilePath))
                        {
                            File.Delete(tempfilePath);
                            DebugLog($"Batch {batchNumber}: Temp file deleted.");
                        }
                    }

                    if (!hasMoreRecords) break;

                    Thread.Sleep(2000);
                }
            }

            DebugLog($"Import completed. Total batches processed: {batchNumber}");
            return jObj;
        }

        /// <exclude></exclude>
        private Dictionary<string, string> SubmitImportRequest(string reqUrl, Dictionary<string, string> _reqHeaders, string oauthToken, string filePath)
        {
            DebugLog($"SubmitImportRequest: URL: {reqUrl} | filePath: {filePath}");
            Dictionary<string, string> respObj = new Dictionary<string, string>();
            // Enable TLS 1.2 + TLS 1.3 (3072 = Tls12, 12288 = Tls13). On older OS/.NET
            // versions Tls13 is unsupported; fall back to TLS 1.2 only so the request
            // still goes through on a strong cipher rather than being rejected.
            try
            {
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)(3072 | 12288);
            }
            catch (NotSupportedException)
            {
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;
            }
            HttpWebRequest request = WebRequest.Create(reqUrl) as HttpWebRequest;
            Stream responseStream;
            StreamReader reader;
            Stream importReqStream;
            Stream readStream = null;
            string fileName = Path.GetFileName(filePath);
            WebResponse response = null;
            int statusCode = 0;
            string responseStr = "";
            try
            {

                Encoding encoding = Encoding.UTF8;
                string boundary = string.Format("----------{0:N}", Guid.NewGuid());
                string contentType = "multipart/form-data; boundary=" + boundary;
                string header = string.Format("--{0}\r\nContent-Disposition: form-data; name=\"{1}\"; filename=\"{2}\";\r\nContent-Type: {3}\r\n\r\n",
                            boundary,
                            "FILE",
                            fileName,
                            "application/octet-stream");

                importReqStream = new System.IO.MemoryStream();
                importReqStream.Write(encoding.GetBytes(header), 0, encoding.GetByteCount(header));

                // Write the file data directly to the Stream, rather than serializing it to a string.
                using (readStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    //readStream = File.OpenRead(filePath);
                    readStream.CopyTo(importReqStream);
                    string footer = "\r\n--" + boundary + "--\r\n";
                    importReqStream.Write(encoding.GetBytes(footer), 0, encoding.GetByteCount(footer));
                    importReqStream.Position = 0;
                    byte[] importData = new byte[importReqStream.Length];
                    importReqStream.Read(importData, 0, importData.Length);
                    importReqStream.Close();


                    // Set up the request properties.
                    request.Method = "POST";
                    request.ContentType = contentType;
                    request.CookieContainer = new CookieContainer();
                    request.ContentLength = importData.Length;
                    request.Headers["Authorization"] = "Zoho-oauthtoken " + oauthToken;
                    request.UserAgent = "Analytics C# Client v2_" + _clientVersion;


                    if (_reqHeaders != null)
                    {
                        Dictionary<string, string>.KeyCollection headerNames = _reqHeaders.Keys;
                        foreach (string headerName in headerNames)
                        {
                            request.Headers[headerName] = _reqHeaders[headerName];
                        }
                    }

                    if (_proxy)
                    {
                        WebProxy proxyConfig = new WebProxy(_proxyHost, _proxyPort);
                        proxyConfig.BypassProxyOnLocal = false;
                        proxyConfig.Credentials = new NetworkCredential(_proxyUsername, _proxyPassword);
                        request.Proxy = proxyConfig;
                    }

                    // Send the form data to the request.
                    using (Stream requestStream = request.GetRequestStream())
                    {
                        requestStream.Write(importData, 0, importData.Length);
                        requestStream.Close();
                    }

                    response = request.GetResponse();
                }
            }
            catch (WebException webEx)
            {
                response = webEx.Response;
                if (response == null)
                {
                    DebugLog($"SubmitImportRequest: WebException with null response - {webEx.ToString()}");
                    throw new Exception("WebException with no response - " + webEx.Message);
                }

                var httpResponse = response as HttpWebResponse;
                DebugLog($"SubmitImportRequest: WebException - HTTP {(int)httpResponse.StatusCode} {httpResponse.StatusDescription} | URL: {reqUrl} | {webEx.ToString()}");

                if (httpResponse.StatusCode == HttpStatusCode.ProxyAuthenticationRequired)
                {
                    DebugLog($"SubmitImportRequest: Proxy authentication failed - {httpResponse.StatusDescription}");
                    throw new Exception("Invalid proxy - " + httpResponse.StatusDescription);
                }
            }
            catch (Exception ex)
            {
                DebugLog($"SubmitImportRequest: General exception - URL: {reqUrl} | {ex.ToString()}");
                throw new Exception("Error Occurred - " + ex.Message);
            }
            finally
            {
                if (readStream != null)
                {
                    readStream.Close();
                }
                if (response != null)
                {
                    statusCode = (int)(response as HttpWebResponse).StatusCode;
                    responseStream = response.GetResponseStream();
                    reader = new StreamReader(responseStream);
                    responseStr = reader.ReadToEnd();
                    response.Close();
                }
            }
            respObj["httpStatusCode"] = statusCode.ToString();
            respObj["response"] = responseStr;
            DebugLog($"SubmitImportRequest: Completed - HTTP {statusCode}");
            return respObj;
        }

        /// <exclude></exclude>
        internal Stream SendExportAPIRequest(
            string endPoint,
            Dictionary<string, object> config,
            Dictionary<string, string> reqHeaders,
            string filePath = null,
            bool stream = false)
        {
            DebugLog($"SendExportAPIRequest: endpoint={endPoint} | filePath={filePath} | stream={stream}");
            if (_accessToken == null)
            {
                DebugLog("SendExportAPIRequest: Access token is null, regenerating OAuth token.");
                RegenerateOAuthToken();
            }

            string reqUrl = _analyticsServerURL + endPoint;
            if (config != null && config.Count > 0)
            {
                string parameters =
                    "CONFIG=" + HttpUtility.UrlEncode(JsonSerializer.Serialize(config));
                reqUrl += "?" + parameters;
            }

            DebugLog($"SendExportAPIRequest: Sending request to URL.");
            HttpWebResponse response = SubmitExportRequestRaw(reqUrl, reqHeaders, _accessToken);
            DebugLog($"SendExportAPIRequest: HTTP {(int)response.StatusCode}");

            // ---- ERROR HANDLING (no buffering on success) ----
            if (!((int)response.StatusCode).ToString().StartsWith("2"))
            {
                using var reader = new StreamReader(response.GetResponseStream());
                string errorBody = reader.ReadToEnd();
                DebugLog($"SendExportAPIRequest: Error response - {errorBody}");

                if (IsOAuthExpired(errorBody))
                {
                    DebugLog("SendExportAPIRequest: OAuth expired, regenerating and retrying.");
                    RegenerateOAuthToken();
                    response = SubmitExportRequestRaw(reqUrl, reqHeaders, _accessToken);
                    DebugLog($"SendExportAPIRequest: Retry HTTP {(int)response.StatusCode}");
                }
            }

            if (!((int)response.StatusCode).ToString().StartsWith("2"))
            {
                using var reader = new StreamReader(response.GetResponseStream());
                string errorBody = reader.ReadToEnd();

                JsonDocument json = JsonDocument.Parse(errorBody);
                int errorCode = json.RootElement
                    .GetProperty("data")
                    .GetProperty("errorCode")
                    .GetInt32();

                string errorMessage = json.RootElement
                    .GetProperty("data")
                    .GetProperty("errorMessage")
                    .GetString();

                DebugLog($"SendExportAPIRequest: ServerException - ErrorCode={errorCode} | ErrorMessage={errorMessage} | HTTP {(int)response.StatusCode}");
                throw new ServerException(
                    (int)response.StatusCode,
                    errorCode,
                    errorMessage
                );
            }

            // ---- STREAM MODE ----
            if (stream)
            {
                DebugLog("SendExportAPIRequest: Success. Returning response stream.");
                return response.GetResponseStream();
            }

            // ---- FILE MODE (chunked write) ----
            if (string.IsNullOrEmpty(filePath))
            {
                throw new ArgumentException("filePath is required when stream=false");
            }

            DebugLog($"SendExportAPIRequest: Success. Writing response to file: {filePath}");
            using Stream responseStream = response.GetResponseStream();
            using FileStream fileStream = new FileStream(
                filePath,
                FileMode.Create,
                FileAccess.Write,
                FileShare.None,
                bufferSize: 1024 * 1024,
                useAsync: false
            );

            byte[] buffer = new byte[1024 * 1024];
            int bytesRead;
            while ((bytesRead = responseStream.Read(buffer, 0, buffer.Length)) > 0)
            {
                fileStream.Write(buffer, 0, bytesRead);
            }

            DebugLog("SendExportAPIRequest: File write completed.");
            return null;
        }


        /// <exclude></exclude>
        private HttpWebResponse SubmitExportRequestRaw(
            string reqUrl,
            Dictionary<string, string> reqHeaders,
            string oauthToken)
        {
            DebugLog($"SubmitExportRequestRaw: Sending GET request | URL: {reqUrl}");
            // Enable TLS 1.2 + TLS 1.3. Fall back to TLS 1.2 only on platforms where
            // TLS 1.3 is not supported, so the request still proceeds over a strong cipher.
            try
            {
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)(3072 | 12288);
            }
            catch (NotSupportedException)
            {
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;
            }

            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(reqUrl);
            request.Method = "GET";
            request.UserAgent = "Analytics C# Client v2_" + _clientVersion;

            if (oauthToken != null)
            {
                request.Headers["Authorization"] = "Zoho-oauthtoken " + oauthToken;
            }

            if (reqHeaders != null)
            {
                foreach (var kv in reqHeaders)
                {
                    request.Headers[kv.Key] = kv.Value;
                }
            }

            if (_connectionTimeout > 0)
                request.Timeout = _connectionTimeout;

            if (_readTimeout > 0)
                request.ReadWriteTimeout = _readTimeout;

            if (_proxy)
            {
                request.Proxy = new WebProxy(_proxyHost, _proxyPort)
                {
                    Credentials = new NetworkCredential(_proxyUsername, _proxyPassword)
                };
            }

            try
            {
                HttpWebResponse resp = (HttpWebResponse)request.GetResponse();
                DebugLog($"SubmitExportRequestRaw: HTTP {(int)resp.StatusCode}");
                return resp;
            }
            catch (WebException webEx)
            {
                if (webEx.Response != null)
                {
                    var httpResp = (HttpWebResponse)webEx.Response;
                    DebugLog($"SubmitExportRequestRaw: WebException - HTTP {(int)httpResp.StatusCode} {httpResp.StatusDescription} | URL: {reqUrl} | {webEx.ToString()}");
                    return httpResp;
                }
                DebugLog($"SubmitExportRequestRaw: WebException with null response - {webEx.ToString()}");
                throw;
            }
            catch (Exception ex)
            {
                DebugLog($"SubmitExportRequestRaw: General exception - {ex.ToString()}");
                throw;
            }
        }


        /// <exclude></exclude>
        internal dynamic SendAPIRequest(string reqMethod, string endPoint, Dictionary<string, object> config, Dictionary<string, string> _reqHeaders)
        {
            DebugLog($"SendAPIRequest: method={reqMethod} | endpoint={endPoint}");
            if (_accessToken == null)
            {
                DebugLog("SendAPIRequest: Access token is null, regenerating OAuth token.");
                RegenerateOAuthToken();
            }

            string reqUrl = _analyticsServerURL + endPoint;
            if (config != null)
            {
                string parameters = "CONFIG=" + HttpUtility.UrlEncode(JsonSerializer.Serialize(config));
                reqUrl = reqUrl + "?" + parameters;
            }

            Dictionary<string, string> responseObj = SubmitRequest(reqMethod, reqUrl, _reqHeaders, _accessToken);
            dynamic jObj = null;
            string statusCode;
            string response;
            responseObj.TryGetValue("httpStatusCode", out statusCode);
            responseObj.TryGetValue("response", out response);
            DebugLog($"SendAPIRequest: HTTP {statusCode} | Response: {response}");

            if (!statusCode.StartsWith("2") && IsOAuthExpired(response))
            {
                DebugLog("SendAPIRequest: OAuth expired, regenerating and retrying.");
                RegenerateOAuthToken();
                responseObj = SubmitRequest(reqMethod, reqUrl, _reqHeaders, _accessToken);
                responseObj.TryGetValue("httpStatusCode", out statusCode);
                responseObj.TryGetValue("response", out response);
                DebugLog($"SendAPIRequest: Retry HTTP {statusCode} | Response: {response}");
            }

            if (!statusCode.StartsWith("2"))
            {
                try
                {
                    JsonDocument jsonDocument = JsonDocument.Parse(response);
                    jObj = jsonDocument.RootElement;
                    int errorCode = jObj.GetProperty("data").GetProperty("errorCode").GetInt32();
                    string errorMessage = jObj.GetProperty("data").GetProperty("errorMessage").GetString();
                    DebugLog($"SendAPIRequest: ServerException - ErrorCode={errorCode} | ErrorMessage={errorMessage} | HTTP {statusCode}");
                    throw new ServerException(int.Parse(statusCode), errorCode, errorMessage);
                }
                catch (ServerException ex)
                {
                    throw ex;
                }
                catch (Exception ex)
                {
                    DebugLog($"SendAPIRequest: Exception - {ex.Message}");
                    throw new Exception("Error Occured - " + ex.Message);
                }
            }
            else if (!string.IsNullOrEmpty(response))
            {
                DebugLog("SendAPIRequest: Success.");
                JsonDocument jsonDocument = JsonDocument.Parse(response);
                JsonElement root = jsonDocument.RootElement;
                jObj = jsonDocument.RootElement;
            }

            return jObj;
        }

        /// <exclude></exclude>
        private Dictionary<string, string> SubmitRequest(string reqMethod, string reqUrl, Dictionary<string, string> _reqHeaders, string oauthToken, string postBody = null)
        {
            DebugLog($"SubmitRequest: method={reqMethod} | URL: {reqUrl} | hasBody={postBody != null}");
            Dictionary<string, string> respObj = new Dictionary<string, string>();
            WebResponse response = null;
            StreamReader reader = null;
            Stream responseStream = null;
            int statusCode = 0;
            string responseStr = "";
            try
            {
                // Enable TLS 1.2 + TLS 1.3. Fall back to TLS 1.2 only on platforms where
                // TLS 1.3 is not supported, so the request still proceeds over a strong cipher.
                try
                {
                    ServicePointManager.SecurityProtocol = (SecurityProtocolType)(3072 | 12288);
                }
                catch (NotSupportedException)
                {
                    ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;
                }

                HttpWebRequest request = WebRequest.Create(reqUrl) as HttpWebRequest;
                request.Method = reqMethod;
                request.UserAgent = "Analytics C# Client v2_" + _clientVersion;
                if (oauthToken != null)
                {
                    request.Headers["Authorization"] = "Zoho-oauthtoken " + oauthToken;
                }
                if (_reqHeaders != null)
                {
                    Dictionary<string, string>.KeyCollection headerNames = _reqHeaders.Keys;
                    foreach (string headerName in headerNames)
                    {
                        request.Headers[headerName] = _reqHeaders[headerName];
                    }
                }
                if (_connectionTimeout != 0)
                {
                    request.Timeout = _connectionTimeout;
                }
                if (_readTimeout != 0)
                {
                    request.ReadWriteTimeout = _readTimeout;
                }
                if (_proxy)
                {
                    WebProxy proxyConfig = new WebProxy(_proxyHost, _proxyPort);
                    proxyConfig.BypassProxyOnLocal = false;
                    proxyConfig.Credentials = new NetworkCredential(_proxyUsername, _proxyPassword);
                    request.Proxy = proxyConfig;
                }
                if (postBody != null)
                {
                    byte[] bodyBytes = Encoding.UTF8.GetBytes(postBody);
                    request.ContentType = "application/x-www-form-urlencoded";
                    request.ContentLength = bodyBytes.Length;
                    using (Stream requestStream = request.GetRequestStream())
                    {
                        requestStream.Write(bodyBytes, 0, bodyBytes.Length);
                    }
                }
                response = request.GetResponse();
            }
            catch (WebException webEx)
            {
                response = webEx.Response;
                if (response == null)
                {
                    DebugLog($"SubmitRequest: WebException with null response - {webEx.ToString()}");
                    throw new Exception("WebException with no response - " + webEx.Message);
                }
                var httpResponse = response as HttpWebResponse;
                DebugLog($"SubmitRequest: WebException - HTTP {(int)httpResponse.StatusCode} {httpResponse.StatusDescription} | URL: {reqUrl} | {webEx.ToString()}");
                if (httpResponse.StatusCode == HttpStatusCode.ProxyAuthenticationRequired)
                {
                    DebugLog($"SubmitRequest: Proxy authentication failed - {httpResponse.StatusDescription}");
                    throw new Exception("Invalid proxy - " + httpResponse.StatusDescription);
                }
            }
            catch (Exception ex)
            {
                DebugLog($"SubmitRequest: General exception - URL: {reqUrl} | {ex.ToString()}");
                throw new Exception("Error Occured - " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (responseStream != null)
                {
                    responseStream.Close();
                }
                if (response != null)
                {
                    statusCode = (int)(response as HttpWebResponse).StatusCode;
                    responseStream = response.GetResponseStream();
                    reader = new StreamReader(responseStream);
                    responseStr = reader.ReadToEnd();
                    response.Close();
                }
            }
            respObj["httpStatusCode"] = statusCode.ToString();
            respObj["response"] = responseStr;
            DebugLog($"SubmitRequest: Completed - HTTP {statusCode}");
            return respObj;
        }

        /// <exclude></exclude>
        private bool IsOAuthExpired(string response)
        {
            try
            {
                JsonDocument jsonDocument = JsonDocument.Parse(response);
                dynamic jObj = jsonDocument.RootElement;
                int errorCode = jObj.GetProperty("data").GetProperty("errorCode").GetInt32();
                bool expired = (errorCode == 8535);
                DebugLog($"IsOAuthExpired: errorCode={errorCode} | expired={expired}");
                return expired;
            }
            catch (Exception)
            {
                DebugLog("IsOAuthExpired: Could not parse response, returning false.");
                return false;
            }
        }

        /// <exclude></exclude>
        private void RegenerateOAuthToken()
        {
            DebugLog("RegenerateOAuthToken: Requesting new access token.");
            string reqUrl = _accountsServerURL + "/oauth/v2/token";
            string parameters = "client_id=" + _clientId + "&client_secret=" + _clientSecret + "&refresh_token=" + _refreshToken + "&grant_type=refresh_token";
            Dictionary<string, string> responseObj = SubmitRequest("POST", reqUrl, null, null, parameters);
            string statusCode;
            string response;
            responseObj.TryGetValue("httpStatusCode", out statusCode);
            responseObj.TryGetValue("response", out response);

            JsonDocument jsonDocument = JsonDocument.Parse(response);
            dynamic jObj = jsonDocument.RootElement;
            if (statusCode.StartsWith("2"))
            {
                try
                {
                    string accesstoken = jObj.GetProperty("access_token").GetString();
                    //Console.WriteLine("Accesstoken - " + accesstoken);
                    _accessToken = accesstoken;
                    DebugLog("RegenerateOAuthToken: Access token regenerated successfully.");
                }
                catch (KeyNotFoundException)
                {
                    string errorMessage = jObj.GetProperty("error").GetString();
                    DebugLog($"RegenerateOAuthToken: KeyNotFoundException - {errorMessage}");
                    throw new ServerException(int.Parse(statusCode), 0, errorMessage);
                }
                catch (Exception ex)
                {
                    DebugLog($"RegenerateOAuthToken: Exception - {ex.Message}");
                    throw new Exception("Unkown Error - " + ex.Message);
                }
            }
            else
            {
                DebugLog($"RegenerateOAuthToken: Failed - HTTP {statusCode} | Response: {response}");
                throw new ServerException(int.Parse(statusCode), 0, response);
            }
        }
    }

    /// <summary>
    /// OrgAPI contains organization level operations.
    /// </summary>
    public class OrgAPI : IOrgAPI
    {
        /// <exclude></exclude>
        private readonly AnalyticsClient _aClient;

        /// <exclude></exclude>
        private readonly Dictionary<string, string> _reqHeaders = new Dictionary<string, string>();

        /// <exclude></exclude>
        internal OrgAPI(AnalyticsClient ac, long orgId)
        {
            _aClient = ac;
            _reqHeaders.Add("ZANALYTICS-ORGID", orgId.ToString());
        }

        /// <summary>
        /// Create a blank workspace in the specified organization.
        /// </summary>
        /// <param name="workspaceName">Name of the workspace.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>New workspace id.</returns>
        public long CreateWorkspace(string workspaceName, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/workspaces/";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["workspaceName"] = workspaceName;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("workspaceId").GetString());
        }

        /// <summary>
        /// Returns list of admins for a specified organization.
        /// </summary>
        /// <returns>Organization admins list.</returns>
        public JsonElement GetAdmins()
        {
            string endPoint = "/restapi/v2/orgadmins";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("orgAdmins");
        }

        /// <summary>
        /// Returns list of users for the specified organization.
        /// </summary>
        /// <returns>List of users.</returns>
        public JsonElement GetUsers()
        {
            string endPoint = "/restapi/v2/users";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("users");
        }

        /// <summary>
        /// Add users to the specified organization.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be added.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddUsers(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/users";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove users from the specified organization.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be removed.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveUsers(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/users";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Activate users in the specified organization.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be activated.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ActivateUsers(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/users/active";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Deactivate users in the specified organization.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be deactivated.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeactivateUsers(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/users/inactive";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Change role for the specified users.
        /// </summary>
        /// <param name="emailIds">The email address of the users.</param>
        /// <param name="role">Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN".</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeUserRole(List<string> emailIds, string role, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/users/role";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            config["role"] = role;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns details of the specified workspace/view.
        /// </summary>
        /// <param name="workspaceName">The name of the workspace.</param>
        /// <param name="viewName">The name of the view.</param>
        /// <returns>Workspace/view details.</returns>
        public JsonElement GetMetaDetails(string workspaceName, string viewName)
        {
            string endPoint = "/restapi/v2/metadetails";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["workspaceName"] = workspaceName;
            if (viewName != null)
            {
                config["viewName"] = viewName;
            }
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Returns subscription details of the specified organization.
        /// </summary>
        /// <returns>Subscription details.</returns>
        public JsonElement GetSubscriptionDetails()
        {
            string endPoint = "/restapi/v2/subscription";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("subscription");
        }

        /// <summary>
        /// Returns resource usage details of the specified organization.
        /// </summary>
        /// <returns>Resource details.</returns>
        public JsonElement GetResourceDetails()
        {
            string endPoint = "/restapi/v2/resources";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("resourceDetails");
        }

        /// <summary>
        /// Returns all the AutoML analysis available in an organization.
        /// </summary>
        /// <returns>AutoML analysis list.</returns>
        public JsonElement GetAutomlAnalysis()
        {
            string endPoint = "/restapi/v2/automl/analysis";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("analysis");
        }
        /// <summary>
        /// Returns list of all custom roles available in the organization.
        /// </summary>
        /// <returns>Custom roles list.</returns>
        public JsonElement GetCustomRoles()
        {
            string endPoint = "/restapi/v2/orgs/roles";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("roles");
        }
        /// <summary>
        /// Create a new custom role in the organization.
        /// </summary>
        /// <param name="roleName">Name of the custom role.</param>
        /// <param name="accessType">Access type for the custom role.</param>
        /// <param name="permissions">Permissions configuration for the custom role.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>New custom role id.</returns>
        public long CreateCustomRole(string roleName, string accessType, Dictionary<string, object> permissions, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/orgs/roles";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["roleName"] = roleName;
            config["accessType"] = accessType;
            config["permissions"] = permissions;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("roleId").GetString());
        }
        /// <summary>
        /// Update the existing custom role in the organization.
        /// </summary>
        /// <param name="roleId">Id of the custom role to be updated.</param>
        /// <param name="roleName">New name for the custom role.</param>
        /// <param name="accessType">New access type for the custom role.</param>
        /// <param name="permissions">New permissions configuration for the custom role.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void UpdateCustomRole(long roleId, string roleName, string accessType, Dictionary<string, object> permissions, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/orgs/roles/" + roleId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["roleName"] = roleName;
            config["accessType"] = accessType;
            config["permissions"] = permissions;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }
        /// <summary>
        /// Delete the specified custom role from the organization.
        /// </summary>
        /// <param name="roleId">Id of the custom role to be deleted.</param>
        public void DeleteCustomRole(long roleId)
        {
            string endPoint = "/restapi/v2/orgs/roles/" + roleId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }


        /// <summary>
        /// Returns the access restriction settings configured for the organization.
        /// </summary>
        /// <returns>Organization access restriction settings.</returns>
        public JsonElement GetOrgAccessRestrictions()
        {
            string endPoint = "/restapi/v2/security-controls/access-restrictions";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Update the access restriction settings of the organization.
        /// </summary>
        /// <param name="config">Contains the access restriction configurations to be updated.</param>
        public void UpdateOrgAccessRestrictions(Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/security-controls/access-restrictions";
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of linked workspaces available in the specified organization.
        /// </summary>
        /// <returns>Linked workspaces list.</returns>
        public JsonElement GetLinkedWorkspaces()
        {
            string endPoint = "/restapi/v2/linkedworkspaces";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("linkedWorkspaces");
        }

    }

    /// <summary>
    /// WorkspaceAPI contains workspace level operations.
    /// </summary>
    public class WorkspaceAPI : IWorkspaceAPI
    {
        /// <exclude></exclude>
        private readonly AnalyticsClient _aClient;

        /// <exclude></exclude>
        private readonly string _workspaceEndPoint;

        /// <exclude></exclude>
        private readonly string _securityControlsEndPoint;
        
        /// <exclude></exclude>
        private readonly long _workspaceId;

        /// <exclude></exclude>
        private readonly Dictionary<string, string> _reqHeaders = new Dictionary<string, string>();

        /// <exclude></exclude>
        internal WorkspaceAPI(AnalyticsClient ac, long orgId, long workspaceId)
        {
            _workspaceId = workspaceId;
            _aClient = ac;
            _workspaceEndPoint = "/restapi/v2/workspaces/" + workspaceId;
            _securityControlsEndPoint = "/restapi/v2/security-controls/workspaces/" + workspaceId;
            _reqHeaders.Add("ZANALYTICS-ORGID", orgId.ToString());
        }

        /// <summary>
        /// Rename a specified workspace in the organization.
        /// </summary>
        /// <param name="workspaceName">New name of the workspace.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void Rename(string workspaceName, Dictionary<string, object> config)
        {
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["workspaceName"] = workspaceName;
            _aClient.SendAPIRequest("PUT", _workspaceEndPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified workspace in the organization.
        /// </summary>
        public void Delete()
        {
            _aClient.SendAPIRequest("DELETE", _workspaceEndPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns the secret key of the specified workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Workspace secret key.</returns>
        public string GetSecretKey(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/secretkey";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("workspaceKey").GetString();
        }

        /// <summary>
        /// Copy the specified workspace from one organization to another or within the organization.
        /// </summary>
        /// <param name="newWorkspaceName">Name of the new workspace.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <param name="destOrgId">Id of the organization where the destination workspace is present. Can be null.</param>
        /// <returns>New workspace id.</returns>
        public long Copy(string newWorkspaceName, Dictionary<string, object> config, long? destOrgId)
        {
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["newWorkspaceName"] = newWorkspaceName;
            if (destOrgId != null)
            {
                _reqHeaders["ZANALYTICS-DEST-ORGID"] = destOrgId.ToString();
            }
            dynamic response = _aClient.SendAPIRequest("POST", _workspaceEndPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("workspaceId").GetString());
        }

        /// <summary>
        /// Adds a specified workspace as favorite.
        /// </summary>
        public void AddFavorite()
        {
            string endPoint = _workspaceEndPoint + "/favorite";
            _aClient.SendAPIRequest("POST", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Remove a specified workspace from favorite.
        /// </summary>
        public void RemoveFavorite()
        {
            string endPoint = _workspaceEndPoint + "/favorite";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Adds a specified workspace as default.
        /// </summary>
        public void AddDefault()
        {
            string endPoint = _workspaceEndPoint + "/default";
            _aClient.SendAPIRequest("POST", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Remove a specified workspace from default.
        /// </summary>
        public void RemoveDefault()
        {
            string endPoint = _workspaceEndPoint + "/default";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Enable workspace to the specified white label domain.
        /// </summary>
        public void EnableDomainAccess()
        {
            string endPoint = _workspaceEndPoint + "/wlaccess";
            _aClient.SendAPIRequest("POST", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Disable workspace from the specified white label domain.
        /// </summary>
        public void DisableDomainAccess()
        {
            string endPoint = _workspaceEndPoint + "/wlaccess";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns list of all accessible views for the specified workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Views list.</returns>
        public JsonElement GetViews(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/views";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("views"));
        }

        /// <summary>
        /// Create a table in the specified workspace.
        /// </summary>
        /// <param name="tableDesign">Table structure.</param>
        /// <returns>Table id.</returns>
        public long CreateTable(Dictionary<string, object> tableDesign)
        {
            string endPoint = _workspaceEndPoint + "/tables";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["tableDesign"] = tableDesign;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("viewId").GetString());
        }

        /// <summary>
        /// Copy the specified views from one workspace to another workspace.
        /// </summary>
        /// <param name="viewIds">The id of the views to be copied.</param>
        /// <param name="destWorkspaceId">The destination workspace id.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <param name="destOrgId">Id of the organization where the destination workspace is present. Can be null.</param>
        /// <returns>Views list.</returns>
        public JsonElement CopyViews(List<long> viewIds, long destWorkspaceId, Dictionary<string, object> config, long? destOrgId)
        {
            string endPoint = _workspaceEndPoint + "/views/copy";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["viewIds"] = viewIds;
            config["destWorkspaceId"] = destWorkspaceId;
            if (destOrgId != null)
            {
                _reqHeaders["ZANALYTICS-DEST-ORGID"] = destOrgId.ToString();
            }
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("views"));
        }

        /// <summary>
        /// Returns list of all accessible folders for the specified workspace.
        /// </summary>
        /// <returns>Folders list.</returns>
        public JsonElement GetFolders()
        {
            string endPoint = _workspaceEndPoint + "/folders";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("folders"));
        }

        /// <summary>
        /// Create a folder in the specified workspace.
        /// </summary>
        /// <param name="folderName">The name of the folder.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Folder id.</returns>
        public long CreateFolder(string folderName, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/folders";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["folderName"] = folderName;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("folderId").GetString());
        }

        /// <summary>
        /// Rename a specified folder in the workspace.
        /// </summary>
        /// <param name="folderId">The id of the folder.</param>
        /// <param name="folderName">The new name of the folder.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RenameFolder(long folderId, string folderName, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/folders/" + folderId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["folderName"] = folderName;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified folder in the workspace.
        /// </summary>
        /// <param name="folderId">The id of the folder.</param>
        public void DeleteFolder(long folderId)
        {
            string endPoint = _workspaceEndPoint + "/folders/" + folderId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns list of groups for the specified workspace.
        /// </summary>
        /// <returns>Groups list.</returns>
        public JsonElement GetGroups()
        {
            string endPoint = _workspaceEndPoint + "/groups";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("groups"));
        }

        /// <summary>
        /// Returns details of the specified group.
        /// </summary>
        /// <param name="groupId">The id of the group.</param>
        /// <returns>Group details.</returns>
        public JsonElement GetGroupDetails(long groupId)
        {
            string endPoint = _workspaceEndPoint + "/groups/" + groupId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("groups"));
        }

        /// <summary>
        /// Create a group in the specified workspace.
        /// </summary>
        /// <param name="groupName">Name of the group.</param>
        /// <param name="emailIds">The email address of the users to be added to the group.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Group id.</returns>
        public long CreateGroup(string groupName, List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/groups";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["groupName"] = groupName;
            config["emailIds"] = emailIds;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("groupId").GetString());
        }

        /// <summary>
        /// Rename a specified group.
        /// </summary>
        /// <param name="groupId">The id of the group.</param>
        /// <param name="groupName">The new name of the group.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RenameGroup(long groupId, string groupName, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/groups/" + groupId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["groupName"] = groupName;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified group.
        /// </summary>
        /// <param name="groupId">The id of the group.</param>
        public void DeleteGroup(long groupId)
        {
            string endPoint = _workspaceEndPoint + "/groups/" + groupId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Add users to the specified group.
        /// </summary>
        /// <param name="groupId">The id of the group.</param>
        /// <param name="emailIds">The email address of the users to be added to the group.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddGroupMembers(long groupId, List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/groups/" + groupId + "/members";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove users from the specified group.
        /// </summary>
        /// <param name="groupId">The id of the group.</param>
        /// <param name="emailIds">The email address of the users to be removed from the group.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveGroupMembers(long groupId, List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/groups/" + groupId + "/members";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of admins for the specified workspace.
        /// </summary>
        /// <returns>Workspace admins list.</returns>
        public JsonElement GetAdmins()
        {
            string endPoint = _workspaceEndPoint + "/admins";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("workspaceAdmins"));
        }

        /// <summary>
        /// Add admins for the specified workspace.
        /// </summary>
        /// <param name="emailIds">The email address of the admin users to be added.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddAdmins(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/admins";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove admins from the specified workspace.
        /// </summary>
        /// <param name="emailIds">The email address of the admin users to be removed.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveAdmins(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/admins";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns shared details of the specified workspace.
        /// </summary>
        /// <returns>Shared details.</returns>
        public JsonElement GetShareInfo()
        {
            string endPoint = _workspaceEndPoint + "/share";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));

        }

        /// <summary>
        /// Share views to the specified users.
        /// </summary>
        /// <param name="viewIds">View ids which to be shared.</param>
        /// <param name="emailIds">The email address of the users to whom the views need to be shared.</param>
        /// <param name="permissions">Contains permission details.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ShareViews(List<long> viewIds, List<string> emailIds, Dictionary<string, bool> permissions, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/share";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            config["viewIds"] = viewIds;
            config["permissions"] = permissions;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove shared views for the specified users.
        /// </summary>
        /// <param name="viewIds">View ids whose sharing needs to be removed.</param>
        /// <param name="emailIds">The email address of the users to whom the sharing need to be removed.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveShare(List<long> viewIds, List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/share";
            config = (config == null) ? new Dictionary<string, object>() : config;
            if (viewIds != null)
            {
                config["viewIds"] = viewIds;
            }
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns shared details of the specified views.
        /// </summary>
        /// <param name="viewIds">View ids for which sharing details are required.</param>
        /// <returns>Shared details.</returns>
        public JsonElement GetSharedDetailsForViews(List<long> viewIds)
        {
            string endPoint = _workspaceEndPoint + "/share/shareddetails";
            Dictionary<string, object> config = new Dictionary<string, object>();
            if (viewIds != null)
            {
                config["viewIds"] = viewIds;
            }
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("sharedDetails"));
        }

        /// <summary>
        /// Returns list of slideshows for the specified workspace.
        /// </summary>
        /// <returns>Slideshow list.</returns>
        public JsonElement GetSlideshows()
        {
            string endPoint = _workspaceEndPoint + "/slides";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("slideshows"));
        }

        /// <summary>
        /// Returns details of the specified slideshow.
        /// </summary>
        /// <param name="slideId">The id of the slideshow.</param>
        /// <returns>Slideshow details.</returns>
        public JsonElement GetSlideshowDetails(long slideId)
        {
            string endPoint = _workspaceEndPoint + "/slides/" + slideId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("slideInfo"));
        }

        /// <summary>
        /// Returns slide URL to access the specified slideshow.
        /// </summary>
        /// <param name="slideId">The id of the slideshow.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Slideshow URL.</returns>
        public string GetSlideshowURL(long slideId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/slides/" + slideId + "/publish";
            config = (config == null) ? new Dictionary<string, object>() : config;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("slideUrl").GetString());
        }

        /// <summary>
        /// Create a slideshow in the specified workspace.
        /// </summary>
        /// <param name="slideName">Name of the slideshow to be created.</param>
        /// <param name="viewIds">Ids of the view to be included in the slideshow.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Slideshow id.</returns>
        public long CreateSlideshow(string slideName, List<long> viewIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/slides";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["slideName"] = slideName;
            config["viewIds"] = viewIds;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("slideId").GetString());
        }

        /// <summary>
        /// Update details of the specified slideshow.
        /// </summary>
        /// <param name="slideId">The id of the slideshow.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void UpdateSlideshow(long slideId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/slides/" + slideId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified slideshow in the workspace.
        /// </summary>
        /// <param name="slideId">The id of the slideshow.</param>
        public void DeleteSlideshow(long slideId)
        {
            string endPoint = _workspaceEndPoint + "/slides/" + slideId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Create a variable in the workspace.
        /// </summary>
        /// <param name="variableName">Name of the variable to be created.</param>
        /// <param name="variableDataType">Datatype of the variable to be created.</param>
        /// <param name="variableType">Type of the variable to be created.</param>
        /// <param name="config">Contains the control configurations.</param>
        /// <returns>Variable id.</returns>
        public long CreateVariable(string variableName, int variableDataType, int variableType, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/variables";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["variableName"] = variableName;
            config["variableDataType"] = variableDataType;
            config["variableType"] = variableType;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("variableId").GetString());
        }

        /// <summary>
        /// Update details of the specified variable in the workspace.
        /// </summary>
        /// <param name="variableId">Id for the variable.</param>
        /// <param name="variableName">New name for the variable.</param>
        /// <param name="variableDataType">New datatype for the variable.</param>
        /// <param name="variableType">New type for the variable.</param>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdateVariable(long variableId, string variableName, int variableDataType, int variableType, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/variables/" + variableId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["variableName"] = variableName;
            config["variableDataType"] = variableDataType;
            config["variableType"] = variableType;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified variable in the workspace.
        /// </summary>
        /// <param name="variableId">The id of the variable.</param>
        public void DeleteVariable(long variableId)
        {
            string endPoint = _workspaceEndPoint + "/variables/" + variableId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns list of variables for the specified workspace.
        /// </summary>
        /// <returns>Variables list.</returns>
        public JsonElement GetVariables()
        {
            string endPoint = _workspaceEndPoint + "/variables";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("variables"));
        }

        /// <summary>
        /// Returns details of the specified variable.
        /// </summary>
        /// <param name="variableId">The id of the variable.</param>
        /// <returns>Variable details.</returns>
        public JsonElement GetVariableDetails(long variableId)
        {
            string endPoint = _workspaceEndPoint + "/variables/" + variableId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Make the specified folder as default.
        /// </summary>
        /// <param name="folderId">The id of the folder.</param>
        public void MakeDefaultFolder(long folderId)
        {
            string endPoint = _workspaceEndPoint + "/folders/" + folderId + "/default";
            _aClient.SendAPIRequest("PUT", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns list of datasources for the specified workspace.
        /// </summary>
        /// <returns>Datasource list.</returns>
        public JsonElement GetDatasources()
        {
            string endPoint = _workspaceEndPoint + "/datasources";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("dataSources"));
        }


        /// <summary>
        /// Initiate data sync for the specified datasource.
        /// </summary>
        /// <param name="datasourceId">Id of the datasource.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void SyncData(long datasourceId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/datasources/" + datasourceId + "/sync";
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Update connection details for the specified datasource.
        /// </summary>
        /// <param name="datasourceId">Id of the datasource.</param>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdateDatasourceConnection(long datasourceId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/datasources/" + datasourceId;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of all views available in trash for the specified workspace.
        /// </summary>
        /// <returns>Views list.</returns>
        public JsonElement GetTrashViews()
        {
            string endPoint = _workspaceEndPoint + "/trash";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("views"));
        }

        /// <summary>
        /// Restore the specified view from trash.
        /// </summary>
        /// <param name="viewId">Id of the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RestoreTrashView(long viewId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/trash/" + viewId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified view permanently from trash.
        /// </summary>
        /// <param name="viewId">Id of the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeleteTrashView(long viewId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/trash/" + viewId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Swaps the hierarchy of a parent folder and a subfolder.
        /// </summary>
        /// <param name="folderId">Id of the folder.</param>
        /// <param name="hierarchy">New hierarchy for the folder. (0 - Parent; 1 - Child)</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeFolderHierarchy(long folderId, int hierarchy, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/folders/" + folderId + "/move";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["hierarchy"] = hierarchy;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Place the folder above the reference folder.
        /// </summary>
        /// <param name="folderId">Id of the folder.</param>
        /// <param name="referenceFolderId">Id of the reference folder.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeFolderPosition(long folderId, long referenceFolderId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/folders/" + folderId + "/reorder";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["referenceFolderId"] = referenceFolderId;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Move views to the mentioned folder.
        /// </summary>
        /// <param name="folderId">Id of the folder.</param>
        /// <param name="viewIds">View ids to be moved.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void MoveViewsToFolder(long folderId, List<long> viewIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/views/movetofolder";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["folderId"] = folderId;
            config["viewIds"] = viewIds;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of users for the specified workspace.
        /// </summary>
        /// <returns>List of users.</returns>
        public JsonElement GetWorkspaceUsers()
        {
            string endPoint = _workspaceEndPoint + "/users";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("users");
        }

        /// <summary>
        /// Add users to the specified workspace.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be added.</param>
        /// <param name="role">Role of the users to be added.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddWorkspaceUsers(List<string> emailIds, string role, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/users";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            config["role"] = role;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove users from the specified workspace.
        /// </summary>
        /// <param name="emailIds">The email address of the users to be removed.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveWorkspaceUsers(List<string> emailIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/users";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Change users staus in the specified workspace.
        /// </summary>
        /// <param name="emailIds">The email address of the users.</param>
        /// <param name="operation">New status for the users ( Values -  activate | deactivate )</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeWorkspaceUserStatus(List<string> emailIds, string operation, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/users/status";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            config["operation"] = operation;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Change role for the specified users.
        /// </summary>
        /// <param name="emailIds">The email address of the users.</param>
        /// <param name="role">Name of the role.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeWorkspaceUserRole(List<string> emailIds, string role, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/users/role";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["emailIds"] = emailIds;
            config["role"] = role;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Create a new query table in the workspace.
        /// </summary>
        /// <param name="sqlQuery">SQL query to construct the query table.</param>
        /// <param name="queryTableName">Name of the query table to be created.</param>
        /// <param name="config">Contains the control configurations.</param>
        /// <returns>View id.</returns>
        public long CreateQueryTable(string sqlQuery, string queryTableName, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/querytables";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["sqlQuery"] = sqlQuery;
            config["queryTableName"] = queryTableName;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("viewId").GetString());
        }

        /// <summary>
        /// Returns list of all query tables for the specified workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Query table list.</returns>
        public JsonElement GetQueryTables(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/querytables";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("queryTables");
        }
        
        /// <summary>
        /// Update the mentioned query table in the workspace.
        /// </summary>
        /// <param name="viewId">Id of the query table to be updated.</param>
        /// <param name="sqlQuery">New SQL query to be updated.</param>
        /// <param name="config">Contains the control configurations.</param>
        public void EditQueryTable(long viewId, string sqlQuery, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/querytables/" + viewId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["sqlQuery"] = sqlQuery;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Export the views as templates.
        /// </summary>
        /// <param name="viewId">Ids of the view to be exported.</param>
        /// <param name="filePath">Path of the file where the data exported to be stored. ( Should be in 'atpt' format )</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ExportAsTemplate(List<long> viewIds, string filePath, Dictionary<string, object> config)
        {
            if (viewIds == null || viewIds.Count == 0)
            {
                throw new ArgumentException("viewIds cannot be null or empty.");
            }

            if (string.IsNullOrEmpty(filePath))
            {
                throw new ArgumentException("filePath cannot be null or empty.");
            }

            string endPoint = _workspaceEndPoint + "/template/data";

            config = config ?? new Dictionary<string, object>();
            config["viewIds"] = viewIds;

            using (Stream responseStream = _aClient.SendExportAPIRequest(endPoint, config, _reqHeaders))
            using (FileStream outputStream = new FileStream(
                filePath,
                FileMode.Create,
                FileAccess.Write,
                FileShare.None,
                bufferSize: 1024 * 1024,
                useAsync: false))
            {
                try
                {
                    responseStream.CopyTo(outputStream);
                }
                catch (Exception ex)
                {
                    throw new Exception(
                        "Exception occurred while writing template export response to file. " + ex.Message,
                        ex
                    );
                }
            }
        }

        /// <summary>
        /// Returns list of email schedules available in the specified workspace.
        /// </summary>
        /// <returns>List of email schedules.</returns>
        public JsonElement GetEmailSchedules()
        {
            string endPoint = _workspaceEndPoint + "/emailschedules";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("emailSchedules");
        }

        /// <summary>
        /// Create an email schedule in the specified workspace.
        /// </summary>
        /// <param name="scheduleName">Name of the email schedule.</param>
        /// <param name="viewIds">View ids to be mailed.</param>
        /// <param name="format">The format in which the data has to be mailed.</param>
        /// <param name="emailIds">The recipients' email addresses for sending views.</param>
        /// <param name="scheduleDetails">Contains schedule frequency, date, and time info.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Email schedule id.</returns>
        public long CreateEmailSchedule(string scheduleName, List<long> viewIds, string format, List<string> emailIds, Dictionary<string, object> scheduleDetails, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/emailschedules";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["scheduleName"] = scheduleName;
            config["viewIds"] = viewIds;
            config["exportType"] = format;
            config["emailIds"] = emailIds;
            config["scheduleDetails"] = scheduleDetails;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("scheduleId").GetString());
        }

        /// <summary>
        /// Update configurations of the specified email schedule in the workspace.
        /// </summary>
        /// <param name="scheduleId">Id for the email schedule.</param>
        /// <param name="config">Contains the control configurations.</param>
        /// <returns>Updated schedule id.</returns>
        public long UpdateEmailSchedule(long scheduleId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/emailschedules/" + scheduleId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            dynamic response = _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("scheduleId").GetString());
        }

        /// <summary>
        /// Trigger configured email schedules instantly.
        /// </summary>
        /// <param name="scheduleId">Id for the email schedule.</param>
        public void TriggerEmailSchedule(long scheduleId)
        {
            string endPoint = _workspaceEndPoint + "/emailschedules/" + scheduleId;
            _aClient.SendAPIRequest("POST", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Update email schedule status.
        /// </summary>
        /// <param name="scheduleId">Id for the email schedule.</param>
        /// <param name="operation">New status for the schedule ( Values -  activate | deactivate )</param>
        public void ChangeEmailScheduleStatus(long scheduleId, string operation)
        {
            string endPoint = _workspaceEndPoint + "/emailschedules/" + scheduleId + "/status";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["operation"] = operation;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified email schedule in the workspace.
        /// </summary>
        /// <param name="scheduleId">Id for the email schedule.</param>
        public void DeleteEmailSchedule(long scheduleId)
        {
            string endPoint = _workspaceEndPoint + "/emailschedules/" + scheduleId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns list of all aggregate formulas for the specified workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Aggregate formula list</returns>
        public JsonElement GetAggregateFormulas(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/aggregateformulas";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("aggregateFormulas"));
        }

        /// <summary>
        /// Returns list of all dependent views and formulas for the specified aggregate formula.
        /// </summary>
        /// <param name="formulaId">Id of the aggregate formula.</param>
        /// <returns>Dependent details</returns>
        public JsonElement GetAggregateFormulaDependents(long formulaId)
        {
            string endPoint = _workspaceEndPoint + "/aggregateformulas/" + formulaId + "/dependents";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Returns the value of the aggregate formula.
        /// </summary>
        /// <param name="formulaId">Id of the aggregate formula.</param>
        /// <returns>Aggregate formula value</returns>
        public string GetAggregateFormulaValue(long formulaId)
        {
            string endPoint = _workspaceEndPoint + "/aggregateformulas/" + formulaId + "/value";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("formulaValue").GetString());
        }

        /// <summary>
        /// Create a report in the specified workspace.
        /// </summary>
        /// <param name="config">Contains the control configurations.</param>
        /// <returns>Created view id.</returns>
        public long CreateReport(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/reports";
            config = (config == null) ? new Dictionary<string, object>() : config;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("viewId").GetString());
        }

        /// <summary>
        /// Update the design and configuration of the specified report.
        /// </summary>
        /// <param name="viewId">Id for the view.</param>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdateReport(long viewId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/reports/" + viewId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns details of the specified query table.
        /// </summary>
        /// <param name="queryTableId">Id of the query table.</param>
        /// <returns>Query table details.</returns>
        public JsonElement GetQueryTableDetails(long queryTableId)
        {
            string endPoint = _workspaceEndPoint + "/querytables/" + queryTableId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Returns list of AutoML analysis for the specified workspace.
        /// </summary>
        /// <returns>AutoML analysis list.</returns>
        public JsonElement GetAutomlAnalysis()
        {
            string endPoint = "/restapi/v2/automl/workspaces/" + _workspaceId + "/analysis";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("analysis");
        }

        /// <summary>
        /// Retrieve detailed information for a specific AutoML analysis.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML Analysis.</param>
        /// <returns>AutoML analysis details.</returns>
        public JsonElement GetAutomlAnalysisDetails(long analysisId)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId;

            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("analysis");
        }

        /// <summary>
        /// Returns deployment details available for an AutoML analysis model.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML analysis.</param>
        /// <param name="modelId">Id of the AutoML model.</param>
        /// <returns>Deployment details.</returns>
        public JsonElement GetDeploymentDetails(long analysisId, long modelId)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/models/" + modelId + "/deployments";

            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("deployments");
        }

        /// <summary>
        /// Create a new AutoML analysis within the provided workspace.
        /// </summary>
        /// <returns>Created AutoML Analysis Id.</returns>
        public long CreateAutomlAnalysis(
            string name,
            long trainingTableId,
            string predictionType,
            List<string> features,
            int serverOption,
            Dictionary<string, object> algorithms,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" + _workspaceId + "/analysis";

            config = (config == null) ? new Dictionary<string, object>() : config;

            config["name"] = name;
            config["trainingTableId"] = trainingTableId;
            config["predictionType"] = predictionType;
            config["features"] = features;
            config["serverOption"] = serverOption;
            config["algorithms"] = algorithms;

            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("id").GetString());
        }

        /// <summary>
        /// Delete a specified AutoML analysis from the given workspace.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML Analysis to be deleted.</param>
        /// <param name="config">Contains any additional control parameters. Can be null.</param>
        public void DeleteAutomlAnalysis(long analysisId, Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId;

            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified model available in the given AutoML analysis.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML Analysis.</param>
        /// <param name="modelId">Id of the model to be deleted.</param>
        /// <param name="config">Contains any additional control parameters. Can be null.</param>
        public void DeleteAutomlAnalysisModel(
            long analysisId,
            long modelId,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/models/" + modelId;

            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Deploy the AutoML analysis model.
        /// </summary>
        /// <returns>Deployment details.</returns>
        public JsonElement CreateAutomlAnalysisDeployment(
            long analysisId,
            long modelId,
            long inputTableId,
            string outputTable,
            List<string> outputColumns,
            string predictionColumn,
            int serverOption,
            string importType,
            Dictionary<string, object> scheduleDetails,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/models/" + modelId + "/deployments";

            config = (config == null) ? new Dictionary<string, object>() : config;

            config["inputTableId"] = inputTableId;
            config["outputTable"] = outputTable;
            config["outputColumns"] = outputColumns;
            config["predictionColumn"] = predictionColumn;
            config["serverOption"] = serverOption;
            config["importType"] = importType;
            config["scheduleDetails"] = (scheduleDetails == null) ? "none" : scheduleDetails;

            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("deployments");
        }

        /// <summary>
        /// Execute the AutoML analysis deployment.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML Analysis.</param>
        /// <param name="deploymentId">Id of the deployment to execute.</param>
        /// <param name="config">Contains any additional control parameters. Can be null.</param>
        public void DeployAutomlAnalysis(
            long analysisId,
            long deploymentId,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/deployments/" + deploymentId + "/execute";

            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the AutoML analysis deployment.
        /// </summary>
        /// <param name="analysisId">Id of the AutoML Analysis.</param>
        /// <param name="deploymentId">Id of the deployment to be deleted.</param>
        /// <param name="config">Contains any additional control parameters. Can be null.</param>
        public void DeleteAutomlAnalysisDeployment(
            long analysisId,
            long deploymentId,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/deployments/" + deploymentId;

            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Get predictions by providing sample input values for a trained model.
        /// </summary>
        /// <returns>Prediction details.</returns>
        public JsonElement AutomlAnalysisPrediction(
            long analysisId,
            long modelId,
            Dictionary<string, object> features,
            Dictionary<string, object> config)
        {
            string endPoint = "/restapi/v2/automl/workspaces/" +
                            _workspaceId + "/analysis/" + analysisId +
                            "/models/" + modelId + "/whatif";

            config = (config == null) ? new Dictionary<string, object>() : config;
            config["features"] = features;

            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return response.GetProperty("data");
        }

                /// <summary>
        /// Returns list of all tags for the specified workspace.
        /// </summary>
        /// <returns>Tags list.</returns>
        public JsonElement GetTags()
        {
            string endPoint = _workspaceEndPoint + "/tags";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("tags");
        }

        /// <summary>
        /// Create a tag in the specified workspace.
        /// </summary>
        /// <param name="tagName">Name of the tag to be created.</param>
        /// <param name="colorCode">Color of the tag in HEX color code.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Created tag id.</returns>
        public string CreateTag(string tagName, string colorCode, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/tags";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["name"] = tagName;
            config["colorCode"] = colorCode;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("tagId").GetString();
        }

        /// <summary>
        /// Update details of the specified tag in the workspace.
        /// </summary>
        /// <param name="tagId">Id of the tag.</param>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdateTag(long tagId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/tags/" + tagId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified tag from the workspace.
        /// </summary>
        /// <param name="tagId">Id of the tag.</param>
        public void DeleteTag(long tagId)
        {
            string endPoint = _workspaceEndPoint + "/tags/" + tagId;
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Adds the specified tag to multiple views in the workspace.
        /// </summary>
        /// <param name="tagId">Id of the tag.</param>
        /// <param name="viewIds">View ids to be associated with the tag.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddTagToViews(long tagId, List<long> viewIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/tags/" + tagId + "/views";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["viewIds"] = viewIds;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Removes the specified tag from multiple views in the workspace.
        /// </summary>
        /// <param name="tagId">Id of the tag.</param>
        /// <param name="viewIds">View ids to be dissociated. Not required when dissociateAll is true.</param>
        /// <param name="dissociateAll">If true, dissociates the tag from all associated views.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveTagFromViews(long tagId, List<long> viewIds, bool dissociateAll, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/tags/" + tagId + "/views";
            config = (config == null) ? new Dictionary<string, object>() : config;
            if (dissociateAll)
            {
                config["dissociateAll"] = true;
            }
            else
            {
                config["viewIds"] = viewIds;
            }
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns the list of views associated with the specified tag.
        /// </summary>
        /// <param name="tagId">Id of the tag.</param>
        /// <returns>Tagged views list.</returns>
        public JsonElement GetTaggedViews(long tagId)
        {
            string endPoint = _workspaceEndPoint + "/tags/" + tagId + "/views";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("views");
        }



        /// <summary>
        /// Returns list of workspaces linked to the specified master workspace.
        /// </summary>
        /// <returns>Linked workspaces list.</returns>
        public JsonElement GetLinkedWorkspaces()
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("linkedWorkspaces");
        }

        /// <summary>
        /// Returns list of organizations and workspaces that can be linked to the specified master workspace.
        /// </summary>
        /// <returns>Organizations with their linkable workspaces.</returns>
        public JsonElement GetLinkableWorkspaces()
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces/linkable";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("orgs");
        }

        /// <summary>
        /// Returns the linking compatibility details for the specified client workspaces.
        /// </summary>
        /// <param name="clients">Contains the client workspaces to be verified for linking compatibility.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Client workspace compatibility details.</returns>
        public JsonElement GetWorkspaceLinkingCompatibility(List<Dictionary<string, object>> clients, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces/compatibility";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["clients"] = clients;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("clients");
        }

        /// <summary>
        /// Link the specified client workspaces to the master workspace.
        /// </summary>
        /// <param name="clients">Contains the client workspaces to be linked with the master workspace.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void LinkWorkspaces(List<Dictionary<string, object>> clients, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["clients"] = clients;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Unlink the client workspaces from the specified master workspace.
        /// </summary>
        /// <param name="scope">Scope of the unlink operation.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void UnlinkWorkspaces(string scope, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["scope"] = scope;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Sync the metadata of the master workspace to its linked client workspaces.
        /// </summary>
        /// <param name="scope">Scope of the sync operation.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void SyncLinkedWorkspaces(string scope, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces/sync";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["scope"] = scope;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns the sync details of the specified linked workspaces.
        /// </summary>
        /// <param name="sandboxIds">Ids of the linked workspaces for which the sync details are fetched.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Linked workspace sync details.</returns>
        public JsonElement GetLinkedWorkspaceSyncDetails(List<long> sandboxIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/linkedworkspaces/sync";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["sandboxIds"] = sandboxIds;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("workspaces");
        }

        /// <summary>
        /// Returns the backup configuration and the list of backups available for the specified workspace.
        /// </summary>
        /// <returns>Workspace backup details.</returns>
        public JsonElement GetWorkspaceBackups()
        {
            string endPoint = _workspaceEndPoint + "/backups";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Trigger an instant backup for the specified workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Triggered backup details.</returns>
        public JsonElement BackupWorkspaceNow(Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/backups";
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Returns the status of the specified workspace backup.
        /// </summary>
        /// <param name="backupId">Id of the backup.</param>
        /// <returns>Backup status details.</returns>
        public JsonElement GetWorkspaceBackupStatus(long backupId)
        {
            string endPoint = _workspaceEndPoint + "/backups/" + backupId + "/status";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Download the specified workspace backup.
        /// </summary>
        /// <param name="backupId">Id of the backup.</param>
        /// <param name="filePath">Path of the file where the downloaded backup is to be stored.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DownloadWorkspaceBackup(long backupId, string filePath, Dictionary<string, object> config)
        {
            if (string.IsNullOrEmpty(filePath))
            {
                throw new ArgumentException("filePath cannot be null or empty.");
            }

            string endPoint = _workspaceEndPoint + "/backups/" + backupId + "/download";
            _aClient.SendExportAPIRequest(endPoint, config, _reqHeaders, filePath);
        }

        /// <summary>
        /// Restore the specified workspace from the given backup.
        /// </summary>
        /// <param name="backupId">Id of the backup.</param>
        /// <param name="confirmRestore">Pass true to confirm that the existing workspace data can be overwritten.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Triggered restore details.</returns>
        public JsonElement RestoreWorkspaceFromBackup(long backupId, bool confirmRestore, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/backups/" + backupId + "/restore";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["confirmRestore"] = confirmRestore;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Returns the status of the specified workspace restore.
        /// </summary>
        /// <param name="restoreId">Id of the restore.</param>
        /// <returns>Restore status details.</returns>
        public JsonElement GetWorkspaceRestoreStatus(long restoreId)
        {
            string endPoint = _workspaceEndPoint + "/restores/" + restoreId + "/status";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Create a dashboard in the specified workspace.
        /// </summary>
        /// <param name="displayName">Name of the dashboard.</param>
        /// <param name="layout">Layout configuration of the dashboard.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>New dashboard id.</returns>
        public long CreateDashboard(string displayName, string layout, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/dashboards";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["displayName"] = displayName;
            config["layout"] = layout;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("dashboardId").GetString());
        }

        /// <summary>
        /// Update the specified dashboard in the workspace.
        /// </summary>
        /// <param name="dashboardId">Id of the dashboard.</param>
        /// <param name="config">Contains the dashboard configurations to be updated.</param>
        public void UpdateDashboard(long dashboardId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/dashboards/" + dashboardId;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns the metadata of the specified dashboard.
        /// </summary>
        /// <param name="dashboardId">Id of the dashboard.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Dashboard configuration.</returns>
        public JsonElement GetDashboardMetadata(long dashboardId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/dashboards/" + dashboardId + "/metadata";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data").GetProperty("dashboardConfig");
        }

        /// <summary>
        /// Returns the metadata of the specified report.
        /// </summary>
        /// <param name="viewId">Id of the report.</param>
        /// <returns>Report configuration.</returns>
        public JsonElement GetReportMetadata(long viewId)
        {
            string endPoint = _workspaceEndPoint + "/reports/" + viewId + "/metadata";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("reportConfig");
        }

        /// <summary>
        /// Returns list of data alerts available in the specified workspace.
        /// </summary>
        /// <returns>Data alerts list.</returns>
        public JsonElement GetAlertsInWorkspace()
        {
            string endPoint = _workspaceEndPoint + "/alerts";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("alerts");
        }

        /// <summary>
        /// Returns the configuration of the specified data alert.
        /// </summary>
        /// <param name="alertId">Id of the data alert.</param>
        /// <returns>Data alert configuration.</returns>
        public JsonElement GetAlertConfiguration(long alertId)
        {
            string endPoint = _workspaceEndPoint + "/alerts/" + alertId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Update the specified data alert in the workspace.
        /// </summary>
        /// <param name="alertId">Id of the data alert.</param>
        /// <param name="alertName">Name of the data alert.</param>
        /// <param name="scheduleDetails">Contains the schedule configurations of the data alert.</param>
        /// <param name="rules">Contains the rules to be evaluated by the data alert.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void UpdateAlert(long alertId, string alertName, Dictionary<string, object> scheduleDetails, List<Dictionary<string, object>> rules, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/alerts/" + alertId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["alertName"] = alertName;
            config["scheduleDetails"] = scheduleDetails;
            config["rules"] = rules;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified data alerts from the workspace.
        /// </summary>
        /// <param name="alertIds">Ids of the data alerts to be deleted.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeleteAlerts(List<long> alertIds, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/alerts";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["alertIds"] = alertIds;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Enable or disable the specified data alerts in the workspace.
        /// </summary>
        /// <param name="alertIds">Ids of the data alerts.</param>
        /// <param name="enabled">Pass true to enable the data alerts and false to disable them.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ChangeAlertStatus(List<long> alertIds, bool enabled, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/alerts/status";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["alertIds"] = alertIds;
            config["enabled"] = enabled;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Execute the specified data alert immediately.
        /// </summary>
        /// <param name="alertId">Id of the data alert.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RunAlert(long alertId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/alerts/" + alertId + "/execute";
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns the execution events of the specified data alert.
        /// </summary>
        /// <param name="alertId">Id of the data alert.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Data alert events along with the page details.</returns>
        public JsonElement GetAlertEvents(long alertId, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/alerts/" + alertId + "/events";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Returns the access restriction settings configured for the specified workspace.
        /// </summary>
        /// <returns>Workspace access restriction settings.</returns>
        public JsonElement GetWorkspaceAccessRestrictions()
        {
            string endPoint = _securityControlsEndPoint + "/access-restrictions";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Update the access restriction settings of the specified workspace.
        /// </summary>
        /// <param name="config">Contains the access restriction configurations to be updated.</param>
        public void UpdateWorkspaceAccessRestrictions(Dictionary<string, object> config)
        {
            string endPoint = _securityControlsEndPoint + "/access-restrictions";
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

    }

    /// <summary>
    /// ViewAPI contains view level operations.
    /// </summary>
    public class ViewAPI : IViewAPI
    {
        /// <exclude></exclude>
        private readonly AnalyticsClient _aClient;

        /// <exclude></exclude>
        private readonly long _viewId;

        /// <exclude></exclude>
        private readonly string _viewEndPoint;

        /// <exclude></exclude>
        private readonly Dictionary<string, string> _reqHeaders = new Dictionary<string, string>();

        /// <exclude></exclude>
        internal ViewAPI(AnalyticsClient ac, long orgId, long workspaceId, long viewId)
        {
            _aClient = ac;
            _viewId = viewId;
            _viewEndPoint = "/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId;
            _reqHeaders.Add("ZANALYTICS-ORGID", orgId.ToString());
        }

        /// <summary>
        /// Add a single row in the specified table.
        /// </summary>
        /// <param name="columnValues">Contains the values for the row. The column names are the key.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Added rows details.</returns>
        public JsonElement AddRow(Dictionary<string, string> columnValues, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/rows";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["columns"] = columnValues;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Update rows in the specified table.
        /// </summary>
        /// <param name="columnValues">Contains the values for the row. The column names are the key.</param>
        /// <param name="criteria">The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Updated rows details.</returns>
        public JsonElement UpdateRow(Dictionary<string, string> columnValues, string criteria, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/rows";
            config = (config == null) ? new Dictionary<string, object>() : config;
            if (criteria != null)
            {
                config["criteria"] = criteria;
            }
            config["columns"] = columnValues;
            dynamic response = _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Delete rows in the specified table.
        /// </summary>
        /// <param name="criteria">The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Deleted rows count.</returns>
        public int DeleteRow(string criteria, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/rows";
            config = (config == null) ? new Dictionary<string, object>() : config;
            if (criteria != null)
            {
                config["criteria"] = criteria;
            }
            dynamic response = _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
            return int.Parse(response.GetProperty("data").GetProperty("deletedRows").GetString());
        }

        /// <summary>
        /// Rename a specified view in the workspace.
        /// </summary>
        /// <param name="newViewName">The new name of the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void Rename(string newViewName, Dictionary<string, object> config)
        {
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["viewName"] = newViewName;
            _aClient.SendAPIRequest("PUT", _viewEndPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified view in the workspace.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void Delete(Dictionary<string, object> config)
        {
            _aClient.SendAPIRequest("DELETE", _viewEndPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Copy a specified view within the workspace.
        /// </summary>
        /// <param name="newViewName">The name of the new view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>View id.</returns>
        public long SaveAs(string newViewName, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/saveas";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["viewName"] = newViewName;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("viewId").GetString());
        }

        /// <summary>
        /// Create reports for the specified table based on the reference table.
        /// </summary>
        /// <param name="refViewId">The ID of the reference view.</param>
        /// <param name="folderId">The folder id where the views to be saved.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void CreateSimilarViews(long refViewId, long folderId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/similarviews";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["referenceViewId"] = refViewId;
            config["folderId"] = folderId;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Auto generate reports for the specified table.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AutoAnalyse(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/autoanalyse";
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Adds a specified view as favourite.
        /// </summary>
        public void AddFavorite()
        {
            string endPoint = _viewEndPoint + "/favorite";
            _aClient.SendAPIRequest("POST", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Remove a specified view from favourite.
        /// </summary>
        public void RemoveFavorite()
        {
            string endPoint = _viewEndPoint + "/favorite";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns the URL to access the specified view.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>View URL.</returns>
        public string GetViewURL(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("viewUrl").GetString());
        }

        /// <summary>
        /// Returns embed URL to access the specified view.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Embed URL.</returns>
        public string GetEmbedURL(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish/embed";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("embedUrl").GetString());
        }

        /// <summary>
        /// Returns private URL to access the specified view.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Private URL.</returns>
        public string GetPrivateURL(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish/privatelink";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("privateUrl").GetString());
        }

        /// <summary>
        /// Create a private URL for the specified view.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Private URL.</returns>
        public string CreatePrivateURL(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish/privatelink";
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("privateUrl").GetString());
        }

        /// <summary>
        /// Remove private link access for the specified view.
        /// </summary>
        public void RemovePrivateAccess()
        {
            string endPoint = _viewEndPoint + "/publish/privatelink";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Make the specified view publically accessible.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>View URL.</returns>
        public string MakeViewPublic(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish/public";
            config = (config == null) ? new Dictionary<string, object>() : config;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return (response.GetProperty("data").GetProperty("publicUrl").GetString());
        }

        /// <summary>
        /// Remove public access for the specified view.
        /// </summary>
        public void RemovePublicAccess()
        {
            string endPoint = _viewEndPoint + "/publish/public";
            _aClient.SendAPIRequest("DELETE", endPoint, null, _reqHeaders);
        }

        /// <summary>
        /// Returns publish configurations for the specified view.
        /// </summary>
        /// <returns>Publish details.</returns>
        public JsonElement GetPublishConfigurations()
        {
            string endPoint = _viewEndPoint + "/publish/config";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Update publish configurations for the specified view.
        /// </summary>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdatePublishConfigurations(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/publish/config";
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns permissions for the specified view.
        /// </summary>
        /// <returns>Permission details.</returns>
        public JsonElement GetMyPermissions()
        {
            string endPoint = _viewEndPoint + "/share/userpermissions";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data").GetProperty("permissions"));
        }

        /// <summary>
        /// Add a column in the specified table.
        /// </summary>
        /// <param name="columnName">The name of the column.</param>
        /// <param name="dataType">The data-type of the column.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Column id.</returns>
        public long AddColumn(string columnName, string dataType, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["columnName"] = columnName;
            config["dataType"] = dataType;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("columnId").GetString());
        }

        /// <summary>
        /// Rename a specified column in the table.
        /// </summary>
        /// <param name="columnId">The id of the column.</param>
        /// <param name="columnName">The new name of the column.</param>
        public void RenameColumn(long columnId, string columnName)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["columnName"] = columnName;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete a specified column in the table.
        /// </summary>
        /// <param name="columnId">The id of the column.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeleteColumn(long columnId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Add a lookup in the specified child table.
        /// </summary>
        /// <param name="columnId">The id of the column.</param>
        /// <param name="refViewId">The ID of the table contains the parent column.</param>
        /// <param name="refColumnId">The ID of the parent column.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddLookup(long columnId, long refViewId, long refColumnId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId + "/lookup";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["referenceViewId"] = refViewId;
            config["referenceColumnId"] = refColumnId;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Remove the lookup for the specified column in the table.
        /// </summary>
        /// <param name="columnId">The id of the column.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveLookup(long columnId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId + "/lookup";
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Hide the specified columns in the table.
        /// </summary>
        /// <param name="columnIds">The array of column ids to be hidden.</param>
        public void HideColumns(List<long> columnIds)
        {
            string endPoint = _viewEndPoint + "/columns/hide";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["columnIds"] = columnIds;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Show the specified hidden columns in the table.
        /// </summary>
        /// <param name="columnIds">The array of column ids to be shown.</param>
        public void ShowColumns(List<long> columnIds)
        {
            string endPoint = _viewEndPoint + "/columns/show";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config["columnIds"] = columnIds;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Auto generate reports for the specified column.
        /// </summary>
        /// <param name="columnId">The id of the column.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AutoAnalyseColumn(long columnId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId + "/autoanalyse";
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Copy the specified formulas from one table to another within the workspace or across workspaces.
        /// </summary>
        /// <param name="formulaNames">The name of the formula columns to be copied.</param>
        /// <param name="destWorkspaceId">The ID of the destination workspace.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <param name="destOrgId">Id of the organization where the destination workspace is present. Can be null.</param>
        public void CopyFormulas(List<string> formulaNames, long destWorkspaceId, Dictionary<string, object> config, long? destOrgId)
        {
            string endPoint = _viewEndPoint + "/formulas/copy";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["formulaColumnNames"] = formulaNames;
            config["destWorkspaceId"] = destWorkspaceId;
            if (destOrgId != null)
            {
                _reqHeaders.Add("ZANALYTICS-DEST-ORGID", destOrgId.ToString());
            }
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Sync data from available datasource for the specified view.
        /// </summary>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RefetchData(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/sync";
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns last import details of the specified view.
        /// </summary>
        /// <returns>Last import details.</returns>
        public JsonElement GetLastImportDetails()
        {
            string endPoint = _viewEndPoint + "/importdetails";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Returns list of all formula columns for the specified table.
        /// </summary>
        /// <returns>Formula list</returns>
        public JsonElement GetFormulaColumns()
        {
            string endPoint = _viewEndPoint + "/formulacolumns";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("formulaColumns");
        }

        /// <summary>
        /// Add a formula column in the specified table.
        /// </summary>
        /// <param name="formulaName">Name of the formula column to be created.</param>
        /// <param name="expression">Formula expression.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Formula id.</returns>
        public long AddFormulaColumn(string formulaName, string expression, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/formulacolumns";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["formulaName"] = formulaName;
            config["expression"] = expression;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("formulaId").GetString());
        }

        /// <summary>
        /// Edit the specified formula column.
        /// </summary>
        /// <param name="formulaId">Id of the formula column to be updated.</param>
        /// <param name="expression">Formula expression.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void EditFormulaColumn(long formulaId, string expression, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/formulacolumns/" + formulaId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["expression"] = expression;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified formula column.
        /// </summary>
        /// <param name="formulaId">Id of the formula column to be deleted.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeleteFormulaColumn(long formulaId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/formulacolumns/" + formulaId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of all aggregate formulas for the specified table.
        /// </summary>
        /// <returns>Aggregate formula list</returns>
        public JsonElement GetAggregateFormulas()
        {
            string endPoint = _viewEndPoint + "/aggregateformulas";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("aggregateFormulas");
        }

        /// <summary>
        /// Add a aggregate formula in the specified table.
        /// </summary>
        /// <param name="formulaName">Name of the formula to be created.</param>
        /// <param name="expression">Formula expression.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Formula id.</returns>
        public long AddAggregateFormula(string formulaName, string expression, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/aggregateformulas";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["formulaName"] = formulaName;
            config["expression"] = expression;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("formulaId").GetString());
        }

        /// <summary>
        /// Edit the specified aggregate formula.
        /// </summary>
        /// <param name="formulaId">Id of the aggregate formula to be updated.</param>
        /// <param name="expression">Formula expression.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void EditAggregateFormula(long formulaId, string expression, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/aggregateformulas/" + formulaId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["expression"] = expression;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Delete the specified aggregate formula.
        /// </summary>
        /// <param name="formulaId">Id of the formula column to be deleted.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void DeleteAggregateFormula(long formulaId, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/aggregateformulas/" + formulaId;
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of dependents views for the specified view.
        /// </summary>
        /// <returns>Dependent view list.</returns>
        public JsonElement GetViewDependents()
        {
            string endPoint = _viewEndPoint + "/dependents";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("views");
        }

        /// <summary>
        /// Returns list of dependents views and formulas for the specified column.
        /// </summary>
        /// <param name="columnId">Id of the column.</param>
        /// <returns>Dependent details.</returns>
        public JsonElement GetColumnDependents(long columnId)
        {
            string endPoint = _viewEndPoint + "/columns/" + columnId + "/dependents";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Update the existing sharing configuration for views.
        /// </summary>
        /// <param name="config">Contains the control configurations.</param>
        public void UpdateSharedDetails(Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/share";
            config = (config == null) ? new Dictionary<string, object>() : config;
            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Retrieves metadata information for the current table, including the list of available columns and associated attributes.
        /// </summary>
        /// <returns>Table metadata details.</returns>
        public JsonElement GetTableMetadata()
        {
            string endPoint = _viewEndPoint + "/metadata";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Updates the column order of the current table.
        /// </summary>
        /// <param name="columnIds">A list containing the full set of column IDs in the new order.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ReorderColumns(List<long> columnIds, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/columns/reorder";

            config = (config == null) ? new Dictionary<string, object>() : config;
            config["columns"] = columnIds;

            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Sorts the data in the table based on the specified columns.
        /// </summary>
        /// <param name="columns">List of column IDs to sort by.</param>
        /// <param name="sortOrder">
        /// Sorting order indicator.
        /// 1 -> Ascending  
        /// 2 -> Descending
        /// </param>
        /// <param name="resetSort">If true, resets any existing sort configuration.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void SortDataByColumns(List<long> columns, int? sortOrder, bool resetSort, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/data/sort";

            config = (config == null) ? new Dictionary<string, object>() : config;

            if (resetSort)
            {
                config["resetSort"] = "true";
            }
            else
            {
                config["sortOrder"] = sortOrder;
                config["columns"] = columns;
            }

            _aClient.SendAPIRequest("PUT", endPoint, config, _reqHeaders);
        }

                /// <summary>
        /// Returns the list of tags associated with the specified view.
        /// </summary>
        /// <returns>Tags list.</returns>
        public JsonElement GetViewTags()
        {
            string endPoint = _viewEndPoint + "/tags";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("tags");
        }

        /// <summary>
        /// Adds multiple tags to the specified view.
        /// </summary>
        /// <param name="tagIds">Tag ids to be associated with the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void AddTagsToView(List<long> tagIds, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/tags";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["tagIds"] = tagIds;
            _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Removes multiple tags from the specified view.
        /// </summary>
        /// <param name="tagIds">Tag ids to be dissociated. Not required when dissociateAll is true.</param>
        /// <param name="dissociateAll">If true, dissociates all tags from the view.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void RemoveTagsFromView(List<long> tagIds, bool dissociateAll, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/tags";
            config = (config == null) ? new Dictionary<string, object>() : config;
            if (dissociateAll)
            {
                config["dissociateAll"] = true;
            }
            else
            {
                config["tagIds"] = tagIds;
            }
            _aClient.SendAPIRequest("DELETE", endPoint, config, _reqHeaders);
        }

        /// <summary>
        /// Returns list of data alerts configured for the specified view.
        /// </summary>
        /// <returns>Data alerts list.</returns>
        public JsonElement GetAlertsInView()
        {
            string endPoint = _viewEndPoint + "/alerts";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data").GetProperty("alerts");
        }

        /// <summary>
        /// Create a data alert for the specified view.
        /// </summary>
        /// <param name="alertName">Name of the data alert.</param>
        /// <param name="scheduleDetails">Contains the schedule configurations of the data alert.</param>
        /// <param name="rules">Contains the rules to be evaluated by the data alert.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>New data alert id.</returns>
        public long CreateAlert(string alertName, Dictionary<string, object> scheduleDetails, List<Dictionary<string, object>> rules, Dictionary<string, object> config)
        {
            string endPoint = _viewEndPoint + "/alerts";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["alertName"] = alertName;
            config["scheduleDetails"] = scheduleDetails;
            config["rules"] = rules;
            dynamic response = _aClient.SendAPIRequest("POST", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("alertId").GetString());
        }

        /// <summary>
        /// Returns the view metadata that can be used while configuring a data alert for the specified view.
        /// </summary>
        /// <returns>View metadata for data alert configuration.</returns>
        public JsonElement GetViewMetadataForAlert()
        {
            string endPoint = _viewEndPoint + "/alerts/metadata";
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return response.GetProperty("data");
        }

    }

    /// <summary>
    /// BulkAPI contains bulk data operation.
    /// </summary>
    public class BulkAPI : IBulkAPI
    {
        /// <exclude></exclude>
        private readonly AnalyticsClient _aClient;

        /// <exclude></exclude>
        private readonly string _workspaceEndPoint;

        /// <exclude></exclude>
        private readonly string _workspaceBulkEndPoint;

        /// <exclude></exclude>
        private readonly Dictionary<string, string> _reqHeaders = new Dictionary<string, string>();

        /// <exclude></exclude>
        internal BulkAPI(AnalyticsClient ac, long orgId, long workspaceId)
        {
            _workspaceEndPoint = "/restapi/v2/workspaces/" + workspaceId;
            _workspaceBulkEndPoint = "/restapi/v2/bulk/workspaces/" + workspaceId;
            _aClient = ac;
            _reqHeaders.Add("ZANALYTICS-ORGID", orgId.ToString());
        }

        /// <summary>
        /// Create a new table and import the data contained in the mentioned file into the created table.
        /// </summary>
        /// <param name="tableName">Name of the new table to be created.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Import result.</returns>
        public JsonElement ImportDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["tableName"] = tableName;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, filePath, null);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Import the data contained in the mentioned file into the table.
        /// </summary>
        /// <param name="viewId">Id of the view where the data to be imported.</param>
        /// <param name="importType">The import type.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Import result.</returns>
        public JsonElement ImportData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/views/" + viewId + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["importType"] = importType;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, filePath, null);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Create a new table and import the raw data provided into the created table.
        /// </summary>
        /// <param name="tableName">Name of the new table to be created.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="rawData">Raw data to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Import result.</returns>
        public JsonElement ImportRawDataInNewTable(string tableName, string fileType, bool autoIdentify, string rawData, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["tableName"] = tableName;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, null, rawData);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Import the raw data provided into the table.
        /// </summary>
        /// <param name="viewId">Id of the view where the data to be imported.</param>
        /// <param name="importType">The import type.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="rawData">Raw data to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Import result.</returns>
        public JsonElement ImportRawData(long viewId, string importType, string fileType, bool autoIdentify, string rawData, Dictionary<string, object> config)
        {
            string endPoint = _workspaceEndPoint + "/views/" + viewId + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["importType"] = importType;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, null, rawData);
            return response.GetProperty("data");
        }

        /// <summary>
        /// Asynchronously create a new table and import the data contained in the mentioned file into the created table.
        /// </summary>
        /// <param name="tableName">Name of the new table to be created.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>The created job id.</returns>
        public long ImportBulkDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["tableName"] = tableName;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, filePath, null);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Asynchronously create a new table and import the data contained in the mentioned file into the created table.
        /// </summary>
        /// <param name="tableName">Name of the new table to be created.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="batchSize">Number of lines per batch.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>The created job id.</returns>
        public long ImportBulkDataInNewTableAsBatches(string tableName, bool autoIdentify, string filePath, int batchSize, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/data/batch";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["tableName"] = tableName;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendBatchImportAPIRequest(endPoint, config, _reqHeaders, filePath, batchSize);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Import the data contained in the mentioned file into the table.
        /// </summary>
        /// <param name="viewId">Id of the view where the data to be imported.</param>
        /// <param name="importType">The import type.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="batchSize">Number of lines per batch.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>The created job id.</returns>
        public long ImportBulkDataAsBatches(long viewId, string importType, bool autoIdentify, string filePath, int batchSize, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/views/" + viewId + "/data/batch";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["importType"] = importType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendBatchImportAPIRequest(endPoint, config, _reqHeaders, filePath, batchSize);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Asynchronously import the data contained in the mentioned file into the table.
        /// </summary>
        /// <param name="viewId">Id of the view where the data to be imported.</param>
        /// <param name="importType">The import type.</param>
        /// <param name="fileType">Type of the file to be imported.</param>
        /// <param name="autoIdentify">Used to specify whether to auto identify the CSV format. Allowable values - true/false.</param>
        /// <param name="filePath">Path of the file to be imported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>The created job id.</returns>
        public long ImportBulkData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/views/" + viewId + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["importType"] = importType;
            config["fileType"] = fileType;
            config["autoIdentify"] = autoIdentify.ToString();
            dynamic response = _aClient.SendImportAPIRequest(endPoint, config, _reqHeaders, filePath, null);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Returns the details of the import job.
        /// </summary>
        /// <param name="jobId">Id of the import job.</param>
        /// <returns>Import result.</returns>
        public JsonElement GetImportJobDetails(long jobId)
        {
            string endPoint = _workspaceBulkEndPoint + "/importjobs/" + jobId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Export the mentioned table (or) view data.
        /// </summary>
        /// <param name="viewId">Id of the view to be exported.</param>
        /// <param name="responseFormat">The format in which the data has to be exported.</param>
        /// <param name="filePath">Path of the file where the data exported to be stored.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        public void ExportData(
            long viewId,
            string responseFormat,
            string filePath,
            Dictionary<string, object> config = null)
        {
            string endPoint = _workspaceEndPoint + "/views/" + viewId + "/data";
            config ??= new Dictionary<string, object>();
            config["responseFormat"] = responseFormat;

            _aClient.SendExportAPIRequest(
                endPoint,
                config,
                _reqHeaders,
                filePath,
                stream: false
            );
        }

        /// <summary>
        /// /// Exports the specified table or view data and returns a stream containing the exported data.
        /// </summary>
        /// <param name="viewId">Id of the view to be exported.</param>
        /// <param name="responseFormat">The format in which the data has to be exported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Stream containing the exported data.</returns>
        public Stream ExportData(
            long viewId,
            string responseFormat,
            Dictionary<string, object> config = null)
        {
            string endPoint = _workspaceEndPoint + "/views/" + viewId + "/data";
            config ??= new Dictionary<string, object>();
            config["responseFormat"] = responseFormat;

            return _aClient.SendExportAPIRequest(
                endPoint,
                config,
                _reqHeaders,
                filePath: null,
                stream: true
            );
        }


        /// <summary>
        /// Initiate asynchronous export for the mentioned table (or) view data.
        /// </summary>
        /// <param name="viewId">Id of the view to be exported.</param>
        /// <param name="responseFormat">The format in which the data is to be exported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Export job id.</returns>
        public long InitiateBulkExport(long viewId, string responseFormat, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/views/" + viewId + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["responseFormat"] = responseFormat;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Initiate asynchronous export with the given SQL Query.
        /// </summary>
        /// <param name="sqlQuery">The SQL Query whose output is exported.</param>
        /// <param name="responseFormat">The format in which the data is to be exported.</param>
        /// <param name="config">Contains any additional control configurations. Can be null.</param>
        /// <returns>Export job id.</returns>
        public long InitiateBulkExportUsingSQL(string sqlQuery, string responseFormat, Dictionary<string, object> config)
        {
            string endPoint = _workspaceBulkEndPoint + "/data";
            config = (config == null) ? new Dictionary<string, object>() : config;
            config["responseFormat"] = responseFormat;
            config["sqlQuery"] = sqlQuery;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, config, _reqHeaders);
            return long.Parse(response.GetProperty("data").GetProperty("jobId").GetString());
        }

        /// <summary>
        /// Returns the details of the export job.
        /// </summary>
        /// <param name="jobId">Id of the export job.</param>
        /// <returns>Export job details.</returns>
        public JsonElement GetExportJobDetails(long jobId)
        {
            string endPoint = _workspaceBulkEndPoint + "/exportjobs/" + jobId;
            dynamic response = _aClient.SendAPIRequest("GET", endPoint, null, _reqHeaders);
            return (response.GetProperty("data"));
        }

        /// <summary>
        /// Export the mentioned job id and write data directly to file (streamed).
        /// </summary>
        /// <param name="jobId">Id of the job to be exported.</param>
        /// <param name="filePath">Path of the file where the data exported to be stored.</param>
        public void ExportBulkData(long jobId, string filePath)
        {
            if (string.IsNullOrEmpty(filePath))
            {
                throw new ArgumentException("filePath cannot be null or empty.");
            }

            string endPoint = _workspaceBulkEndPoint + "/exportjobs/" + jobId + "/data";

            using (Stream responseStream = _aClient.SendExportAPIRequest(endPoint, null, _reqHeaders))
            using (FileStream outputStream = new FileStream(
                filePath,
                FileMode.Create,
                FileAccess.Write,
                FileShare.None,
                bufferSize: 1024 * 1024,   // 1 MB buffer
                useAsync: false))
            {
                try
                {
                    responseStream.CopyTo(outputStream);
                }
                catch (Exception ex)
                {
                    throw new Exception("Exception occurred while writing export response to file. " + ex.Message, ex);
                }
            }
        }

        /// <summary>
        /// Export the mentioned job id and return a live response stream.
        /// Caller is responsible for closing the stream.
        /// </summary>
        /// <param name="jobId">Id of the job to be exported.</param>
        /// <returns>Stream containing the exported data.</returns>
        public Stream ExportBulkData(long jobId)
        {
            string endPoint = _workspaceBulkEndPoint + "/exportjobs/" + jobId + "/data";
            return _aClient.SendExportAPIRequest(endPoint, null, _reqHeaders);
        }

    }

    /// <summary>
    /// ServerException is thrown if the analytics server has received the request but did not process the request due to some error. For example if authorization fails.
    /// </summary>
    public sealed class ServerException : Exception
    {

        /// <exclude></exclude>
        private readonly int httpStatusCode;

        /// <exclude></exclude>
        private readonly int errorCode;

        /// <exclude></exclude>
        private readonly string errorMessage;


        /// <exclude></exclude>
        public ServerException(int httpStatusCode, int errorCode, string errorMessage)
        {
            this.httpStatusCode = httpStatusCode;
            this.errorCode = errorCode;
            this.errorMessage = errorMessage;
        }

        /// <summary>
        /// Gets the HTTP status code.
        /// </summary>
        /// <returns>The HTTP status code.</returns>
        public int GetHTTPStatusCode()
        {
            return httpStatusCode;
        }

        /// <summary>
        /// Gets the error code.
        /// </summary>
        /// <returns>The error code.</returns>
        public int GetErrorCode()
        {
            return errorCode;
        }

        /// <summary>
        /// Gets the error message.
        /// </summary>
        /// <returns>The error message.</returns>
        public string GetErrorMessage()
        {
            return errorMessage;
        }
    }
}
