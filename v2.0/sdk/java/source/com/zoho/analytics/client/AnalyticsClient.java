// $Id$
package com.zoho.analytics.client;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.logging.Level;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import java.util.logging.Logger;
import zr.org.apache.commons.csv.CSVParser;
import zr.org.apache.commons.csv.CSVPrinter;
import zr.org.apache.commons.csv.CSVStrategy;

/**
 * AnalyticsClient provides the java based language binding to the HTTPS based API of Zoho Analytics.
 */
public class AnalyticsClient {

    private final String client_version = "2.10.0";
    private String analyticsServerURL = "https://@@ANALYTICS_URL";
    private String accountsServerURL = "https://@@ACCOUNTS_URL";

    private final String clientId;
    private final String clientSecret;
    private final String refreshToken;
    private String accessToken;
    private TokenRefreshListener tokenRefreshListener;

    /**
     * Longest access-token lifetime treated as a value in seconds.
     *
     * <p>Zoho Accounts answers a refresh-token grant with <em>both</em> units - the seconds the
     * OAuth 2.0 spec and {@link TokenRefreshListener} use, and milliseconds in the spec's own
     * <code>expires_in</code> field:
     *
     * <pre>
     * {
     *   "access_token":  "1000.d9f4...bf99",
     *   "expires_in_sec": 3600,
     *   "api_domain":    "https://www.zohoapis.in",
     *   "token_type":    "Bearer",
     *   "expires_in":     3600000
     * }
     * </pre>
     *
     * <p>So <code>expires_in_sec</code> is read first and is authoritative. This bound only guards
     * the fallback for a response that omits it: no access token lives longer than a day, so an
     * <code>expires_in</code> above this is a millisecond value and is divided by 1000. Taking
     * <code>expires_in</code> at face value cached a one-hour token for 41 days.
     */
    private static final long MAX_TOKEN_LIFETIME_SECONDS = 86400L;

    private int connectionTimeout = 5000;   //Default 5 seconds
    private int readTimeout = 0;    //Default infinite time

    private String userAgentSuffix;

    private boolean proxy = false;
    private String proxyHost;
    private int proxyPort;
    private String proxyUsername;
    private String proxyPassword;
    
    private static final char[] DELIMITERS = new char[]{',', '\t', ';', ' ', '|'};
    private static final char[] QUOTED_CHARS = new char[]{'\u0000', '\'', '"'};
    
    Map<String, String> headers = new HashMap<>();

    static final Logger LOGGER = Logger.getLogger(AnalyticsClient.class.getName());

    /**
     * TLS protocols allowed for outbound HTTPS calls. TLS 1.3 is preferred;
     * TLS 1.2 is kept as a fallback for older JREs (JDK 8 &lt; 8u261 has no TLS 1.3).
     */
    private static final String[] STRONG_TLS_PROTOCOLS = new String[] { "TLSv1.2", "TLSv1.3" };

    /**
     * Strong cipher suites (IANA names) used when the handshake negotiates TLS 1.2.
     * TLS 1.3 only defines strong AEAD suites, so on that path this list is ignored.
     */
    private static final String[] STRONG_TLS_CIPHERS = new String[] {
        // TLS 1.3 suites
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256",
        // TLS 1.2 strong AEAD suites
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"
    };

    /**
     * Socket factory that wraps the JRE default SSLSocketFactory and pins each
     * created socket to the intersection of {@link #STRONG_TLS_PROTOCOLS} /
     * {@link #STRONG_TLS_CIPHERS} with what the JRE actually supports. If the
     * intersection is empty (very old JRE), this field is {@code null} and the
     * default factory is used so the request still goes through.
     */
    private static final SSLSocketFactory STRONG_SSL_SOCKET_FACTORY = buildStrongSSLSocketFactory();

    private static SSLSocketFactory buildStrongSSLSocketFactory() {
        try {
            SSLContext ctx = SSLContext.getInstance("TLS");
            ctx.init(null, null, null);
            SSLParameters supported = ctx.getSupportedSSLParameters();
            final String[] protocols = intersect(STRONG_TLS_PROTOCOLS, supported.getProtocols());
            final String[] ciphers = intersect(STRONG_TLS_CIPHERS, supported.getCipherSuites());
            if (protocols.length == 0 || ciphers.length == 0) {
                LOGGER.log(Level.WARNING, "JRE does not support any of the configured strong TLS protocols/ciphers; falling back to JRE default SSL configuration");
                return null;
            }
            final SSLSocketFactory delegate = ctx.getSocketFactory();
            return new SSLSocketFactory() {
                @Override public String[] getDefaultCipherSuites() { return ciphers.clone(); }
                @Override public String[] getSupportedCipherSuites() { return delegate.getSupportedCipherSuites(); }
                private java.net.Socket configure(java.net.Socket s) {
                    if (s instanceof SSLSocket) {
                        SSLSocket ss = (SSLSocket) s;
                        ss.setEnabledProtocols(protocols);
                        ss.setEnabledCipherSuites(ciphers);
                    }
                    return s;
                }
                @Override public java.net.Socket createSocket() throws IOException { return configure(delegate.createSocket()); }
                @Override public java.net.Socket createSocket(java.net.Socket s, String host, int port, boolean autoClose) throws IOException { return configure(delegate.createSocket(s, host, port, autoClose)); }
                @Override public java.net.Socket createSocket(String host, int port) throws IOException, UnknownHostException { return configure(delegate.createSocket(host, port)); }
                @Override public java.net.Socket createSocket(String host, int port, java.net.InetAddress localHost, int localPort) throws IOException, UnknownHostException { return configure(delegate.createSocket(host, port, localHost, localPort)); }
                @Override public java.net.Socket createSocket(java.net.InetAddress host, int port) throws IOException { return configure(delegate.createSocket(host, port)); }
                @Override public java.net.Socket createSocket(java.net.InetAddress address, int port, java.net.InetAddress localAddress, int localPort) throws IOException { return configure(delegate.createSocket(address, port, localAddress, localPort)); }
            };
        } catch (Throwable t) {
            LOGGER.log(Level.WARNING, "Could not build strong TLS socket factory; falling back to JRE default", t);
            return null;
        }
    }

    private static String[] intersect(String[] desired, String[] supported) {
        Set<String> sup = new HashSet<>(Arrays.asList(supported));
        List<String> out = new ArrayList<>();
        for (String s : desired) { if (sup.contains(s)) { out.add(s); } }
        return out.toArray(new String[0]);
    }

    /**
     * Creates a new <code>AnalyticsClient</code> instance.
     * @param clientId The client ID string that has been obtained during the client registration.
     * @param clientSecret The client secret string that has been obtained during the client registration.
     * @param refreshToken The refresh token string that has been obtained through accounts API.
     */
    public AnalyticsClient(String clientId, String clientSecret, String refreshToken) {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.refreshToken = refreshToken;
    }

    /**
     * Creates a new <code>AnalyticsClient</code> instance that reports every access token it obtains
     * to <code>tokenRefreshListener</code>, so the token can be cached and re-supplied through
     * {@link #setAccessToken(String)} instead of exchanging the refresh token again.
     *
     * <p>This is the preferred way to register a listener: a client built this way is created with
     * its listener already in place and {@link #setTokenRefreshListener(TokenRefreshListener)} will
     * refuse to replace it, so no later code can re-point where tokens are delivered.
     *
     * @param clientId The client ID string that has been obtained during the client registration.
     * @param clientSecret The client secret string that has been obtained during the client registration.
     * @param refreshToken The refresh token string that has been obtained through accounts API.
     * @param tokenRefreshListener The listener notified whenever a new access token is obtained.
     *                             Must not be <code>null</code>; use the three-argument constructor
     *                             when no listener is wanted.
     */
    public AnalyticsClient(String clientId, String clientSecret, String refreshToken,
                           TokenRefreshListener tokenRefreshListener) {
        this(clientId, clientSecret, refreshToken);
        if(tokenRefreshListener == null) {
            throw new IllegalArgumentException("tokenRefreshListener must not be null; "
                    + "use AnalyticsClient(clientId, clientSecret, refreshToken) instead.");
        }
        this.tokenRefreshListener = tokenRefreshListener;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    /**
     * Registers a listener that is notified whenever this client obtains a new OAuth access token,
     * so the token can be cached and later re-supplied through {@link #setAccessToken(String)}
     * instead of exchanging the refresh token again.
     *
     * <p>Opt-in: when no listener is registered - the default - the client behaves exactly as it
     * did before this hook existed.
     *
     * <p><strong>Write-once.</strong> A listener may be registered only once per client, whether by
     * this method or by
     * {@link #AnalyticsClient(String, String, String, TokenRefreshListener) the four-argument
     * constructor}; a second call is refused, and <code>null</code> is rejected rather than treated
     * as a way to clear one. Access tokens are therefore delivered for the life of the client to the
     * one listener it started with, and no later code can re-point or unhook that delivery. Prefer
     * the four-argument constructor, which leaves no window in which a client exists without its
     * listener.
     *
     * @param tokenRefreshListener The listener to notify. Must not be <code>null</code>.
     * @throws IllegalArgumentException if <code>tokenRefreshListener</code> is <code>null</code>
     * @throws IllegalStateException if a listener is already registered on this client
     */
    public void setTokenRefreshListener(TokenRefreshListener tokenRefreshListener) {
        if(tokenRefreshListener == null) {
            throw new IllegalArgumentException("tokenRefreshListener must not be null.");
        }
        if(this.tokenRefreshListener != null) {
            throw new IllegalStateException("A token refresh listener is already registered on this client.");
        }
        this.tokenRefreshListener = tokenRefreshListener;
    }

    /**
     * Creates a new <code>OrgAPI</code> instance.
     * @param orgId The ID of the organization.
     * @return OrgAPI instance.
     */
    public OrgAPI getOrgInstance(long orgId) {
        return new OrgAPI(this, orgId);
    }

    /**
     * Creates a new <code>WorkspaceAPI</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     * @return WorkspaceAPI instance.
     */
    public WorkspaceAPI getWorkspaceInstance(long orgId, long workspaceId) {
        return new WorkspaceAPI(this, orgId, workspaceId);
    }

    /**
     * Creates a new <code>ViewAPI</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     * @param viewId The ID of the view.
     * @return ViewAPI instance.
     */
    public ViewAPI getViewInstance(long orgId, long workspaceId, long viewId) {
        return new ViewAPI(this, orgId, workspaceId, viewId);
    }

    /**
     * Creates a new <code>BulkAPI</code> instance.
     * @param orgId The ID of the organization.
     * @param workspaceId The ID of the workspace.
     * @return BulkAPI instance.
     */
    public BulkAPI getBulkInstance(long orgId, long workspaceId) {
        return new BulkAPI(this, orgId, workspaceId);
    }

    /**
     * Sets the analytics server URL.
     * @param serverURL The server URL.
     */
    public void setAnalyticsServerURL(String serverURL) {
        this.analyticsServerURL = serverURL;
    }

    /**
     * Sets the accounts server URL.
     * @param serverURL The server URL.
     */
    public void setAccountsServerURL(String serverURL) {
        this.accountsServerURL = serverURL;
    }

    /**
     * Returns the timeout until a connection is established. A value of zero means the timeout is not used.
     * The default value is 5000.
     * @return A <code>int</code> value.
     */
    public int getConnectionTimeout() {
        return this.connectionTimeout;
    }

    /**
     * Sets the timeout until a connection is established. A value of zero means the timeout is not used.
     * The default value is 5000.
     * @param timeout Contains connection timeout value.
     */
    public void setConnectionTimeout(int timeout) {
        this.connectionTimeout = timeout;
    }

    /**
     * Returns the read timeout value which will wait for the packet to receive from the server end.
     * The default value is 0.
     * @return A <code>int</code> value.
     */
    public int getReadTimeout() {
        return this.readTimeout;
    }

    /**
     * Sets the read timeout which will wait for data response from the server end.
     * The default value is 0.
     * @param timeout Contains read timeout value.
     */
    public void setReadTimeout(int timeout) {
        this.readTimeout = timeout;
    }

    /**
     * Returns the product token appended to the <code>User-Agent</code> header, or
     * <code>null</code> when none is set.
     * @return A <code>String</code> value.
     */
    public String getUserAgentSuffix() {
        return this.userAgentSuffix;
    }

    /**
     * Appends a product token to the <code>User-Agent</code> header sent on every request, for
     * applications that embed this SDK rather than calling it directly. The SDK's own identity is
     * always sent first and cannot be replaced, so the server still sees which client library
     * made the call:
     *
     * <pre>User-Agent: Analytics Java Client v2_2.10.0 za-cli/1.0.0 (Linux; Java/17.0.12)</pre>
     *
     * RFC 9110 defines <code>User-Agent</code> as an ordered list of product tokens for exactly
     * this case, which is why an embedding application should use this rather than inventing its
     * own header: the value already reaches access logs, rate limiting and traffic analytics with
     * no server-side change.
     *
     * <p>Use the <code>name/version</code> form, optionally followed by a parenthesised comment.
     * Characters that cannot appear in a header value &mdash; CR, LF and other control characters
     * &mdash; are stripped, so a caller cannot inject a second header through this value. A
     * <code>null</code> or blank argument clears the suffix.</p>
     *
     * @param suffix Contains the product token to append, e.g. <code>za-cli/1.0.0</code>.
     */
    public void setUserAgentSuffix(String suffix) {
        if(suffix == null) {
            this.userAgentSuffix = null;
            return;
        }
        StringBuilder cleaned = new StringBuilder(suffix.length());
        for(int i = 0; i < suffix.length(); i++) {
            char c = suffix.charAt(i);
            // Keep printable US-ASCII only: anything else cannot travel in a header value, and CR/LF
            // would let a caller append headers of its own.
            if(c >= 0x20 && c < 0x7F) {
                cleaned.append(c);
            }
        }
        String value = cleaned.toString().trim();
        this.userAgentSuffix = value.isEmpty() ? null : value;
    }

    /**
     * To specify the proxy server details. (When configuring the proxy settings, ensure that the 'Basic' authentication scheme is not disabled by the JDK).
     * @param proxyHost The hostname/IP address of the proxy server.
     * @param proxyPort The proxy server port.
     * @param proxyUsername The user name for proxy-server authentication.
     * @param proxyPassword The password for proxy server authentication.
     */
    public void setProxy(String proxyHost, int proxyPort, String proxyUsername, String proxyPassword) {
        this.proxy = true;
        this.proxyHost = proxyHost;
        this.proxyPort = proxyPort;
        this.proxyUsername = proxyUsername;
        this.proxyPassword = proxyPassword;
    }

    /**
     * Internal method to send API request.
     */
    protected JSONObject sendAPIRequest(String reqMethod, String endPoint, JSONObject config, Map<String, String> reqHeaders)
            throws ServerException, ParseException, IOException, JSONException {

        if (this.accessToken == null) {
            regenerateOAuthToken();
        }
        Map<String, String> responseMap;
        String reqUrl = this.analyticsServerURL + endPoint;
        String configParam = null;

        switch (reqMethod.toUpperCase()) {
            case "GET":
                String encodedParam = (config == null) ? "" : "CONFIG=" + URLEncoder.encode(config.toString(), "UTF-8");
                if (!encodedParam.isEmpty()) {
                    reqUrl += "?" + encodedParam;
                }
                responseMap = submitRequest(reqMethod, reqUrl, reqHeaders, this.accessToken, null);
                break;

            case "POST":
            case "PUT":
            case "DELETE":
                if (reqHeaders == null) {
                    reqHeaders = new HashMap<>();
                }
                reqHeaders.put("Content-Type", "application/x-www-form-urlencoded");
                configParam = (config == null) ? null : "CONFIG=" + URLEncoder.encode(config.toString(), "UTF-8");
                responseMap = submitRequest(reqMethod, reqUrl, reqHeaders, this.accessToken, configParam);
                break;

            default:
                throw new IllegalArgumentException("Unsupported HTTP method: " + reqMethod);
        }

        String httpStatusCode = responseMap.get("httpStatusCode");
        String response = responseMap.get("response");

        JSONObject responseJObj = response.isEmpty() ? new JSONObject() : getJSONResponse(response);

        // Handle token expiration
        if (!httpStatusCode.startsWith("2") && this.isOAuthExpired(responseJObj)) {
            regenerateOAuthToken();
            responseMap = submitRequest(reqMethod, reqUrl, reqHeaders, this.accessToken, configParam);

            httpStatusCode = responseMap.get("httpStatusCode");
            response = responseMap.get("response");
            responseJObj = response.isEmpty() ? new JSONObject() : getJSONResponse(response);
        }

        // Error response
        if (!httpStatusCode.startsWith("2")) {
            JSONObject dataObj = responseJObj.getJSONObject("data");
            throw new ServerException(Integer.parseInt(httpStatusCode), dataObj.getInt("errorCode"), dataObj.getString("errorMessage"));
        }

        return responseJObj;
    }

    /**
     * Internal method to parse JSON data.
     */
    private JSONObject getJSONResponse(String response) throws ParseException {
        JSONObject responseJObj;
        try{
            responseJObj = new JSONObject(response);
        }
        catch (Exception ex){
            throw new ParseException(response, "Exception while parsing the response.", ex);
        }
        return responseJObj;
    }

    /**
     * Internal method to send HTTP request.
     */
    private Map<String, String> submitRequest(String reqMethod, String reqUrl, Map<String, String> reqHeaders, String oAuthToken, String reqBody) throws IOException {

        HttpURLConnection urlCon = getConnection(reqUrl, reqMethod, reqHeaders, oAuthToken);

        if (reqBody != null && !reqBody.isEmpty()) {
            urlCon.setDoOutput(true);
            try (OutputStream os = urlCon.getOutputStream()) {
                byte[] input = reqBody.getBytes("UTF-8");
                os.write(input, 0, input.length);
            }
        }

        Map<String, String> respMap = new HashMap<>();
        respMap.put("httpStatusCode", String.valueOf(urlCon.getResponseCode()));
        respMap.put("response", getResponse(urlCon));
        return respMap;
    }

    /**
     * Internal method to send API request.
     */
    protected JSONObject sendExportAPIRequest(String endPoint, JSONObject config, Map<String, String> reqHeaders, Object dataHandler) throws ServerException, ParseException, IOException, JSONException {
        if(this.accessToken == null){
            regenerateOAuthToken();
        }
        String params = (config == null) ? "" : "CONFIG=" + URLEncoder.encode(config.toString(), "UTF-8");
        String reqUrl = this.analyticsServerURL + endPoint + "?" + params;
        Map<String, String> responseMap = submitExportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
        String httpStatusCode = responseMap.get("httpStatusCode");
        String response = responseMap.get("response");
        JSONObject responseJObj = new JSONObject();
        if(!response.isEmpty()){
            responseJObj = getJSONResponse(response);
        }
        if(!httpStatusCode.startsWith("2") && this.isOAuthExpired(responseJObj)){
            regenerateOAuthToken();
            responseMap = submitExportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
            httpStatusCode = responseMap.get("httpStatusCode");
            response = responseMap.get("response");
            if(!response.isEmpty()){
                responseJObj = getJSONResponse(response);
            }
        }
        if(!httpStatusCode.startsWith("2")){
            JSONObject dataObj = responseJObj.getJSONObject("data");
            throw new ServerException(Integer.parseInt(httpStatusCode), dataObj.getInt("errorCode"), dataObj.getString("errorMessage"));
        }
        return responseJObj;
    }

    /**
     * Internal method to send HTTP request.
     */
    private Map<String, String> submitExportRequest(String reqUrl, Map<String, String> reqHeaders, String oAuthToken, Object dataHandler) throws IOException {

        String reqMethod = "GET";
        HttpURLConnection urlCon = getConnection(reqUrl, reqMethod, reqHeaders, oAuthToken);
        String responseCode;
        String response = "";
        Map<String, String> respMap = new HashMap<>();

        responseCode = urlCon.getResponseCode() + "";
        StringBuilder sb = new StringBuilder();

        if(urlCon.getErrorStream() != null) {
            BufferedReader br = null;
            try
            {
                br = new BufferedReader(new InputStreamReader(urlCon.getErrorStream()));
                for(int c; (c = br.read()) >= 0; ) {
                    sb.append((char) c);
                }
            }
            finally
            {
                if (br != null) {
                    br.close();
                }
            }
        }
        else if(urlCon.getResponseCode() == HttpURLConnection.HTTP_OK)
        {
            InputStream is = null;
            OutputStream os = null;
            try
            {
                is = urlCon.getInputStream();
                if(dataHandler instanceof File)
                {
                    os = new BufferedOutputStream(new FileOutputStream((File)dataHandler));
                }
                else
                {
                    os = (OutputStream)dataHandler;
                }

                byte[] arr = new byte[1024];
                int length = 0;
                while ((length =is.read(arr)) > -1)
                {
                    os.write(arr,0,length);
                }
            }
            finally
            {
                if (is != null){try{is.close();}catch (Exception ex){throw ex;}}
                if (os != null){try{os.close();}catch (Exception ex){throw ex;}}
            }
        }

        response = sb.toString();

        respMap.put("httpStatusCode", responseCode);
        respMap.put("response", response);
        return respMap;
    }

    /**
     * Internal method to send API request.
     */
    protected JSONObject sendImportAPIRequest(String endPoint, JSONObject config, Map<String, String> reqHeaders, Object dataHandler) throws ServerException, ParseException, IOException, JSONException {
        if(this.accessToken == null){
            regenerateOAuthToken();
        }
        String params = (config == null) ? "" : "CONFIG=" + URLEncoder.encode(config.toString(), "UTF-8");
        String reqUrl = this.analyticsServerURL + endPoint + "?" + params;
        Map<String, String> responseMap = submitImportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
        String httpStatusCode = responseMap.get("httpStatusCode");
        String response = responseMap.get("response");
        JSONObject responseJObj = new JSONObject();
        if(!response.isEmpty()){
            responseJObj = getJSONResponse(response);
        }
        if(!httpStatusCode.startsWith("2") && this.isOAuthExpired(responseJObj)){
            regenerateOAuthToken();
            responseMap = submitImportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
            httpStatusCode = responseMap.get("httpStatusCode");
            response = responseMap.get("response");
            if(!response.isEmpty()){
                responseJObj = getJSONResponse(response);
            }
        }
        if(!httpStatusCode.startsWith("2")){
            JSONObject dataObj = responseJObj.getJSONObject("data");
            throw new ServerException(Integer.parseInt(httpStatusCode), dataObj.getInt("errorCode"), dataObj.getString("errorMessage"));
        }
        return responseJObj;
    }

    /**
     * Internal method to send API request.
     */
    protected JSONObject sendBatchImportAPIRequest(String endPoint, Map<String, String> reqHeaders, Object dataHandler) throws ServerException, ParseException, IOException, JSONException {
        if(this.accessToken == null){
            regenerateOAuthToken();
        }
        String reqUrl = this.analyticsServerURL + endPoint;
        Map<String, String> responseMap = submitImportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
        String httpStatusCode = responseMap.get("httpStatusCode");
        String response = responseMap.get("response");
        JSONObject responseJObj = new JSONObject();
        if(!response.isEmpty()){
            responseJObj = getJSONResponse(response);
        }
        if(!httpStatusCode.startsWith("2") && this.isOAuthExpired(responseJObj)){
            regenerateOAuthToken();
            responseMap = submitImportRequest(reqUrl, reqHeaders, this.accessToken, dataHandler);
            httpStatusCode = responseMap.get("httpStatusCode");
            response = responseMap.get("response");
            if(!response.isEmpty()){
                responseJObj = getJSONResponse(response);
            }
        }
        if(!httpStatusCode.startsWith("2")){
            JSONObject dataObj = responseJObj.getJSONObject("data");
            throw new ServerException(Integer.parseInt(httpStatusCode), dataObj.getInt("errorCode"), dataObj.getString("errorMessage"));
        }
        return responseJObj;
    }

    /**
     * Internal method.
     */
    private Map<String, String> submitImportRequest(String reqUrl, Map<String, String> reqHeaders, String accessToken, Object dataHandler) throws IOException, ServerException, ParseException {

        HttpURLConnection urlCon = getConnection(reqUrl, "POST", reqHeaders, accessToken);
        urlCon.setRequestMethod("POST");
        urlCon.setDoOutput(true);

        String boundary = UUID.randomUUID().toString();
        urlCon.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

        OutputStream outputStream = urlCon.getOutputStream();
        try(PrintWriter writer = new PrintWriter(new OutputStreamWriter(outputStream, "UTF-8"), true)) {

            // Adding dataHandler as multipart form data
            if (dataHandler instanceof File) {
                File file = (File) dataHandler;
                writer.append("--" + boundary).append("\r\n");
                writer.append("Content-Disposition: form-data; name=\"FILE\"; filename=\"" + file.getName() + "\"").append("\r\n");
                writer.append("Content-Type: application/octet-stream").append("\r\n\r\n");
                writer.flush();

                try(FileInputStream inputStream = new FileInputStream(file))
                {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = inputStream.read(buffer)) != -1) {
                        outputStream.write(buffer, 0, bytesRead);
                    }
                    outputStream.flush();
                    inputStream.close();

                    writer.append("\r\n");
                    writer.flush();
                }
            } else if (dataHandler instanceof String) {
                writer.append("--" + boundary).append("\r\n");
                writer.append("Content-Disposition: form-data; name=\"DATA\"").append("\r\n\r\n");
                writer.append((String) dataHandler).append("\r\n");
                writer.flush();
            }

            writer.append("--" + boundary + "--").append("\r\n");
        }

        Map<String, String> respMap = new HashMap<>();
        respMap.put("httpStatusCode", String.valueOf(urlCon.getResponseCode()));
        respMap.put("response", getResponse(urlCon));
        return respMap;
    }

    /**
     * Internal method.
     */
    private String getResponse(HttpURLConnection urlCon) throws IOException {
        BufferedReader br = null;
        String response = "";
        try
        {
            if(urlCon.getErrorStream() != null) {
                br = new BufferedReader(new InputStreamReader(urlCon.getErrorStream()));
            }
            else {
                br = new BufferedReader(new InputStreamReader(urlCon.getInputStream()));
            }

            StringBuilder sb = new StringBuilder();
            for(int c; (c = br.read()) >= 0; ) {
                sb.append((char) c);
            }
            response = sb.toString();
        }
        finally
        {
            if(br!=null){ br.close(); }
        }
        return response;
    }

    /**
     * Internal method to check oauth token status.
     */
    private HttpURLConnection getConnection(String reqUrl, String reqMethod, Map<String, String> reqHeaders, String oAuthToken) throws IOException
    {
        URL url = new URL(reqUrl);
        HttpURLConnection urlCon;
        if(this.proxy) {
            Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(this.proxyHost, this.proxyPort));
            urlCon = (HttpURLConnection)url.openConnection(proxy);
        }
        else {
            urlCon = (HttpURLConnection)url.openConnection();
        }

        // Restrict HTTPS connections to TLS 1.2 / 1.3 with strong AEAD cipher suites.
        // Best-effort: if STRONG_SSL_SOCKET_FACTORY is null (JRE doesn't support any
        // of our preferred protocols/ciphers) we leave the default in place so the
        // request still goes through.
        if (urlCon instanceof HttpsURLConnection && STRONG_SSL_SOCKET_FACTORY != null) {
            ((HttpsURLConnection)urlCon).setSSLSocketFactory(STRONG_SSL_SOCKET_FACTORY);
        }

        //Setting HTTP request method
        urlCon.setRequestMethod(reqMethod);

        //Setting connection and read timeout
        urlCon.setConnectTimeout(connectionTimeout);
        urlCon.setReadTimeout(this.readTimeout);

        urlCon.setUseCaches(false);
        urlCon.setInstanceFollowRedirects(false);

        if(headers != null){
            Set<String> headerKeys = headers.keySet();
            for(String key : headerKeys){
                urlCon.setRequestProperty(key, headers.get(key));
            }
        }

        if(reqHeaders != null){
            Set<String> headerKeys = reqHeaders.keySet();
            for(String key : headerKeys){
                urlCon.setRequestProperty(key, reqHeaders.get(key));
            }
        }

        //Setting request headers
        //urlCon.setRequestProperty("Content-Type", "application/json");  //No I18N
        // Set last and unconditionally, so neither headers nor reqHeaders can replace the SDK's own
        // identity. An embedding application appends its token through setUserAgentSuffix instead;
        // the SDK's product token always stays first, keeping existing prefix matching on the server
        // side working unchanged.
        String userAgent = "Analytics Java Client v2_" + this.client_version;   //No I18N
        if(this.userAgentSuffix != null) {
            userAgent = userAgent + " " + this.userAgentSuffix;   //No I18N
        }
        urlCon.setRequestProperty("User-Agent", userAgent);   //No I18N
        if(oAuthToken != null) {
            urlCon.setRequestProperty("Authorization", "Zoho-oauthtoken " + oAuthToken);    //No I18N
        }

        if(reqMethod.equals("POST") || reqMethod.equals("PUT")) {
            urlCon.setDoOutput(true);
        }

        if(this.proxy && (Authenticator.getDefault()==null || !Authenticator.getDefault().getClass().getName().equals(ZAuthenticator.class.getName()))) {
            // Capturing the previously existing authenticator before replacing it.
            Authenticator previousAuthenticator = Authenticator.getDefault();
            Authenticator.setDefault(new ZAuthenticator(this, previousAuthenticator));
        }

        return urlCon;
    }

    public static class ZAuthenticator
            extends Authenticator
    {
        private AnalyticsClient analyticsClient;
        private final Authenticator previousAuthenticator;

        public ZAuthenticator(AnalyticsClient analyticsClient, Authenticator previousAuthenticator) {
            super();
            this.analyticsClient = analyticsClient;
            this.previousAuthenticator = previousAuthenticator;
        }
        @Override
        protected PasswordAuthentication getPasswordAuthentication() {
            if(this.getRequestorType().equals(RequestorType.PROXY) && this.getRequestingHost().equals(analyticsClient.proxyHost) && this.getRequestingPort() == analyticsClient.proxyPort) {
                return new PasswordAuthentication(analyticsClient.proxyUsername, analyticsClient.proxyPassword.toCharArray());
            }
            else {
                return previousAuthenticator != null ? previousAuthenticator.requestPasswordAuthenticationInstance(this.getRequestingHost(), this.getRequestingSite(), this.getRequestingPort(), this.getRequestingProtocol(), this.getRequestingPrompt(), this.getRequestingScheme(), this.getRequestingURL(), this.getRequestorType()) : null;
            }
        }
    }



    public void setHeaders(String key, String value) throws Exception
    {
        if (key == null || value == null) {
            throw new IllegalArgumentException("Key or value cannot be null.");
        }

        // Key validation (alphanumeric and hyphen for simplicity)
        if (!key.matches("^[A-Za-z0-9-]+$")) {
            throw new IllegalArgumentException("Invalid header key.");
        }

        // Value validation (no newlines)
        if (value.contains("\n") || value.contains("\r")) {
            throw new IllegalArgumentException("Header value cannot contain newline characters.");
        }

        headers.put(key, value);
    }

    /**
     * Internal method to check oauth token status.
     */
    private boolean isOAuthExpired(JSONObject response) {
        try{
            int errorCode = response.getJSONObject("data").getInt("errorCode");
            return errorCode == 8535;
        }catch (Exception ex){
            //Skipping the exception here.
        }
        return false;
    }

    /**
     * Internal method to generate OAuth token.
     */
    private void regenerateOAuthToken() throws ServerException, ParseException, IOException, JSONException {
        if(this.clientId == null)
        {
            if (this.accessToken == null)
            {
                this.accessToken = "1000.00000000000000000000000000000000.00000000000000000000000000000000";
            }
            return;
        }
        String reqUrl = this.accountsServerURL + "/oauth/v2/token";
        String params = "client_id=" + this.clientId + "&client_secret=" + this.clientSecret
                + "&refresh_token=" + this.refreshToken + "&grant_type=refresh_token";
                Map<String, String> reqHeaders = new HashMap<>();
        reqHeaders.put("Content-Type", "application/x-www-form-urlencoded");
        Map<String, String> responseObj = submitRequest("POST", reqUrl, reqHeaders, null, params);
        String statusCode = responseObj.get("httpStatusCode");
        JSONObject respJObj = getJSONResponse(responseObj.get("response"));
        if(statusCode.startsWith("2") && respJObj.has("access_token")){
            this.accessToken = respJObj.getString("access_token");
            notifyTokenRefreshed(respJObj);
        }else{
            throw new ServerException(Integer.parseInt(statusCode), 0, respJObj.getString("error"));
        }
    }

    /**
     * Internal method to hand a freshly obtained access token to the registered listener, if any.
     * A listener failure is logged and swallowed: caching is an optimisation, and losing it must
     * never fail the API call that triggered the refresh.
     */
    private void notifyTokenRefreshed(JSONObject tokenResponse) {
        TokenRefreshListener listener = this.tokenRefreshListener;
        if(listener == null) {
            return;
        }
        long expiresInSeconds = -1L;
        try {
            if(tokenResponse.has("expires_in_sec")) {
                // Authoritative, and already in the unit this listener documents.
                expiresInSeconds = tokenResponse.getLong("expires_in_sec");
            } else if(tokenResponse.has("expires_in")) {
                long reported = tokenResponse.getLong("expires_in");
                expiresInSeconds = reported > MAX_TOKEN_LIFETIME_SECONDS ? reported / 1000L : reported;
            }
        } catch (JSONException ex) {
            LOGGER.log(Level.FINE, "Token response carried an unusable token lifetime", ex);
        }
        try {
            listener.onTokenRefreshed(this.accessToken, expiresInSeconds);
        } catch (RuntimeException ex) {
            LOGGER.log(Level.WARNING, "Access token refresh listener failed; continuing without caching", ex);
        }
    }

/*

    public JSONObject importDataInBatches(String endPoint, JSONObject config, Map<String, String> reqHeaders, File csvFile, int batchSize, JSONObject toolConfig) throws IOException,ServerException,ParseException, Exception
    {
        LOGGER.log(Level.FINEST,"Starting Import Data In Batches {0}", csvFile.getAbsolutePath());
        LOGGER.log(Level.FINEST,"File size : {0}", csvFile.length());

        BufferedReader reader = null;
        FileInputStream fis = null;
        StringBuilder buf = null;

        String batchKey = "start";
        String jobId = "";
        boolean isLastBatch = false;
        int bufSize = 10000;
        int lineCount = 100;

        String columnHeaders = null;
        boolean isFirstRowHeader = toolConfig.optBoolean("isFirstRowHeader", true);
        if(!isFirstRowHeader)
        {
            JSONArray colHeaders = toolConfig.optJSONArray("columnHeaders");
            if(colHeaders == null || colHeaders.length()<=0)
            {
                throw new Exception("columnHeaders cannot be empty");
            }

            columnHeaders = "";
            for(int i=0; i<colHeaders.length(); i++)
            {
                columnHeaders += colHeaders.getString(i).trim() + ",";
            }
            columnHeaders = columnHeaders.substring(0, columnHeaders.lastIndexOf(",")-1);
        }

        try
        {
            String curLine = null;
            BOMHandler bomHandler = new BOMHandler();
            int length = bomHandler.handleBOMAndSetEncoding(new HashMap(), csvFile);
            fis = new FileInputStream(csvFile);
            if(length != 0)
            {
                byte[] bom = new byte[4];
                fis.read(bom, 0, length);
            }
            reader = new BufferedReader(new InputStreamReader(fis, bomHandler.fileEncoding));

            if(columnHeaders==null)
            {
                columnHeaders = reader.readLine();
            }

            //For Sync Batch Import Cases
//            boolean isLastBatchCommitted = true;
            while (true)
            {
                int currentBatchLineCount = 0;
                buf = new StringBuilder(bufSize);


//                    if(importType.equalsIgnoreCase("TRUNCATEADD"))
//                    {
//                        if(isLastBatchCommitted)
//                        {
//                            curImportType = "APPEND";
//                        }
//                    }

                //For Sync Batch Import case only
                // skip top rows should be sent only for 1st batch, hence overwriting it as zero for rest of the batches
                //config.put("skipTop", "0");

                writeLine(buf,columnHeaders);
                do
                {
                    if(curLine != null)
                    {
                        writeLine(buf,curLine);
                    }
                    else
                    {
                        curLine = reader.readLine();
                        if (curLine == null)
                        {
                            isLastBatch = true;
                            break;
                        }
                        writeLine(buf,curLine);
                    }
                    curLine = null;
                    currentBatchLineCount++;
                }while (currentBatchLineCount < lineCount);
                curLine = reader.readLine();

                if(curLine == null)
                {
                    isLastBatch = true;
                }

                if (currentBatchLineCount > 0 || columnHeaders != null)
                {
                    config.put("batchKey", batchKey);
                    config.put("isLastBatch", isLastBatch);

                    bufSize = buf.length();
                    LOGGER.log(Level.FINEST,"Lines read : {0}", currentBatchLineCount);
                    LOGGER.log(Level.FINEST,"Size : {0}", bufSize);

                    File tempZippedFile = getZippedFile(csvFile.getName(), buf.toString());
                    try
                    {
                        JSONObject response = this.sendImportAPIRequest(endPoint, config, reqHeaders, tempZippedFile);
                        batchKey = response.getJSONObject("data").getString("batchKey");
                        jobId = response.getJSONObject("data").getString("jobId");
                        lineCount = batchSize;
                        LOGGER.log(Level.FINEST,"Finished current batch");
                    }
                    catch (Exception ex)
                    {
                        throw ex;
                    }
                    finally
                    {
                        if(tempZippedFile.exists())
                        {
                            tempZippedFile.delete();
                        }
                    }
                }
                if (curLine == null)
                {
                    break;
                }
                else
                {
                    try
                    {
                        Thread.sleep(2000);
                    }
                    catch (Exception ex)
                    {
                        throw new RuntimeException(ex);
                    }
                }
            }
        }
        finally
        {
            if (reader != null){try{reader.close();}catch(Exception ex){LOGGER.log(Level.SEVERE, null, ex);}}
            if(fis != null){try{fis.close();}catch(Exception ex){LOGGER.log(Level.SEVERE, null, ex);}}
        }
        LOGGER.log(Level.FINEST,"Finished importing {0}",csvFile.getAbsolutePath());

        JSONObject response = new JSONObject();
        response.put("batchKey", batchKey);
        response.put("jobId", jobId);

        return response;
    }
*/
    public JSONObject importDataInBatches(String endPoint, JSONObject config, Map<String, String> reqHeaders, File csvFile, int batchSize, JSONObject toolConfig) throws Exception {
        LOGGER.log(Level.FINEST, "Starting Import Data In Batches {0}", csvFile.getAbsolutePath());

        String batchKey = "start";
        String jobId = "";
        boolean isLastBatch = false;

        // Extract CSV configuration from the config JSONObject
        boolean autoIdentify = config.optBoolean("autoIdentify", true);

        int delimiter = config.optInt("delimiter", 0);
        char delimiterchar = DELIMITERS[delimiter];

        int quote = config.optInt("quoted", 2);
        char quotedChar = QUOTED_CHARS[quote];

        char commentChar = config.optString("commentChar", "").length() > 0 ? config.optString("commentChar").charAt(0) : CSVStrategy.COMMENTS_DISABLED;

        CSVStrategy strategy;
        if (autoIdentify) {
            strategy = CSVStrategy.DEFAULT_STRATEGY;
        } else {
            strategy = new CSVStrategy(delimiterchar, quotedChar, commentChar);
        }

        BOMHandler bomHandler = new BOMHandler();
        int bomLength = bomHandler.handleBOMAndSetEncoding(new HashMap(), csvFile);

        FileInputStream fis = null;
        Reader reader = null;
        CSVParser parser = null;

        try {
            fis = new FileInputStream(csvFile);
            if (bomLength != 0) {
                fis.skip(bomLength);
            }

            reader = new InputStreamReader(fis, bomHandler.fileEncoding);
            parser = new CSVParser(reader, strategy);

            String[] columnHeaders;
            boolean isFirstRowHeader = toolConfig.optBoolean("isFirstRowHeader", true);

            if (isFirstRowHeader) {
                columnHeaders = parser.getLine();
            } else {
                JSONArray colHeadersJson = toolConfig.optJSONArray("columnHeaders");
                if (colHeadersJson == null || colHeadersJson.length() == 0) {
                    throw new Exception("columnHeaders cannot be empty when isFirstRowHeader is false");
                }
                columnHeaders = new String[colHeadersJson.length()];
                for (int i = 0; i < colHeadersJson.length(); i++) {
                    columnHeaders[i] = colHeadersJson.getString(i);
                }
            }

            String[] currentRecord = null;
            while (!isLastBatch) {
                StringWriter sw = new StringWriter();
                CSVPrinter printer = new CSVPrinter(sw);
                printer.setStrategy(strategy);

                // Write headers for each batch
                printer.println(columnHeaders);

                int currentBatchLineCount = 0;
                while (currentBatchLineCount < batchSize && (currentRecord = parser.getLine()) != null) {
                    printer.println(currentRecord);
                    currentBatchLineCount++;
                }

                if (currentRecord == null) {
                    isLastBatch = true;
                }

                if (currentBatchLineCount > 0) {
                    config.put("batchKey", batchKey);
                    config.put("isLastBatch", isLastBatch);

                    File tempZippedFile = getZippedFile(csvFile.getName(), sw.toString());
                    try {
                        JSONObject response = this.sendImportAPIRequest(endPoint, config, reqHeaders, tempZippedFile);
                        JSONObject data = response.getJSONObject("data");
                        batchKey = data.getString("batchKey");
                        jobId = data.getString("jobId");
                        LOGGER.log(Level.FINEST, "Finished current batch. Records: {0}", currentBatchLineCount);
                    } finally {
                        if (tempZippedFile.exists()) {
                            tempZippedFile.delete();
                        }
                    }
                }

                if (!isLastBatch) {
                    Thread.sleep(2000);
                }
            }
        } finally {
            // Close resources in reverse order of creation
            if (reader != null) {
                try { reader.close(); } catch (IOException e) { LOGGER.log(Level.SEVERE, null, e); }
            }
            if (fis != null) {
                try { fis.close(); } catch (IOException e) { LOGGER.log(Level.SEVERE, null, e); }
            }
        }

        JSONObject finalResponse = new JSONObject();
        finalResponse.put("batchKey", batchKey);
        finalResponse.put("jobId", jobId);
        return finalResponse;
    }
    
    class BOMHandler
    {
        String fileEncoding = "UTF-8";  // No I18N
        int length = 0;

        public BOMHandler()
        {
        }

        /**
         * Internally used in ReportClient importDataInBatches()
         * identify file encoding and the length of the BOM
         * The byte order mark (BOM) is a Unicode character used to signal the endianness (byte order) of a text file or stream.
         * Its code point is U+FEFF. BOM use is optional, and, if used, should appear at the start of the text stream.
         * JAVA doesn't support it. So remove the characters
         * BOM characters for UTFs
         * 00 00 FE FF  |   UTF-32, big-endian
         * FF FE 00 00  |   UTF-32, little-endian
         * FE FF        |   UTF-16, big-endian
         * FF FE        |   UTF-16, little-endian
         * EF BB BF     |   UTF-8
         * @param importConfig contains any additional control parameters.
         */
        protected int handleBOMAndSetEncoding(Map importConfig, File file) throws Exception
        {//Kindly refer the following link to know about file encoding. http://java.sun.com/developer/technicalArticles/Intl/Supplementary/     ----   http://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/

            String fileEncode = (String) importConfig.get("ZOHO_FILE_ENCODING");
            if(fileEncode != null)
            {
                fileEncoding = fileEncode;
            }
            String removeBOM = (String) importConfig.get("ZOHO_REMOVE_BOM");
            if( removeBOM != null && "true".equalsIgnoreCase(removeBOM))
            {
                setFileEncodingAndRemoveBOM(file);
            }
            return length;
        }



        /**
         * Internally used in handleBOMAndGetEncoding()
         * @return the file encoding
         */

        protected void setFileEncodingAndRemoveBOM(File file) throws Exception
        {

            InputStream is = null;

            byte[] bomByte = new byte[4];

            try
            {
                is = new BufferedInputStream(new FileInputStream(file));
                is.read(bomByte, 0, 4);
            }
            catch (Exception e)
            {
                throw e;
            }
            finally
            {
                if(is != null)
                {
                    is.close();
                }
            }

            if ( (bomByte[0] == (byte)0xFE) && (bomByte[1] == (byte)0xFF) )
            {
                fileEncoding = "UTF-16BE";  // No I18N
                length = 2;
            }
            else if ( (bomByte[0] == (byte)0xFF) && (bomByte[1] == (byte)0xFE) )
            {
                fileEncoding = "UTF-16LE";  // No I18N
                length = 2;
            }
            else if((bomByte[0] == (byte) 0x00) && (bomByte[1] == (byte) 0x00) && (bomByte[2] == (byte) 0xFE) && (bomByte[3] == (byte) 0xFF))
            {
                fileEncoding = "UTF-32BE";  // No I18N
                length = 4;
            }
            else if ( (bomByte[0] == (byte)0xFF) && (bomByte[1] == (byte)0xFE) && (bomByte[2] == (byte)0x00) && (bomByte[3] == (byte)0x00))
            {
                fileEncoding = "UTF-32LE";  // No I18N
                length = 4;
            }
            else if( (bomByte[0] == (byte)0xEF) && (bomByte[1] == (byte)0xBB) &&(bomByte[2] == (byte)0xBF) )
            {
                fileEncoding = "UTF-8";   // No I18N
                length = 3;
            }
        }
    }

    protected void writeLine(Appendable writer,String curLine) throws IOException
    {
        writer.append(curLine);
        writer.append('\n');
    }

    static File getZippedFile(String csvFileName,String csvContent) throws IOException
    {
        byte[] buf =  csvContent.getBytes("UTF-8");
        File tempFile= File.createTempFile(csvFileName, ".zip");
        tempFile.deleteOnExit();
        ZipOutputStream zos = null;
        try
        {
            zos =  new ZipOutputStream(new FileOutputStream(tempFile));
            zos.setLevel(9);
            zos.putNextEntry(new ZipEntry(csvFileName));
            zos.write(buf);
            return tempFile;
        }
        finally
        {
            close(zos);
        }
    }

    public static void close(Closeable... args)
    {
        for(Closeable c:args)
        {
            if(c != null)
            {
                try{c.close();}catch(Exception ex){LOGGER.log(Level.SEVERE, null, ex);}
            }
        }
    }
}
