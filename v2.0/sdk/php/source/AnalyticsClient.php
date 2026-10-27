<?php
	/**
		* AnalyticsClient provides the PHP based language binding to the https based API of ZohoAnalytics.
	*/
	class AnalyticsClient
	{
		/**
			* @var const CLIENT_VERSION It contain the API client version.It is a constant one.
		*/
		const CLIENT_VERSION = "2.10.0";
		/**
			* @var string $analytics_server_url The base request API URL.
		*/
		private $analytics_server_url = "https://@@ANALYTICS_URL";
		/**
			* @var string $accounts_server_url Account URL.
		*/
		private $accounts_server_url = "https://@@ACCOUNTS_URL";
		/**
			* @var boolean $proxy It will indicate whether the proxy is set or not.
		*/
		private $proxy = FALSE;
		/**
			* @var string $proxy_host The hostname/ip address of the proxy-server.
		*/
		private $proxy_host;
		/**
			* @var int $proxy_port The proxy server port.
		*/
		private $proxy_port;
		/**
			* @var string $proxy_user_name The user name for proxy-server authentication.
		*/
		private $proxy_user_name;
		/**
			* @var string $proxy_password The password for proxy-server authentication.
		*/
		private $proxy_password;
		/**
			* @var string $proxy_type Can be any one ( HTTP , HTTPS , BOTH ).Specify "BOTH" if same configuration can be used for both HTTP and HTTPS.
		*/
		private $proxy_type;
		/**
			* @var int $connection_timeout It is a time value until a connection is established.
		*/
		private $connection_timeout;
		/**
			* @var int $read_timeout It is a time value until waiting to read data.
		*/
		private $read_timeout;

		/**
			* @internal The client ID string that has been obtained during the client registration.
		*/
		private $client_id;

		/**
			* @internal The client secret string that has been obtained during the client registration.
		*/
		private $client_secret;

		/**
			* @internal The refresh token string that has been obtained through accounts API
		*/
		private $refresh_token;

		/**
			* @internal The access token string that has been obtained through accounts API
		*/
		private $access_token;
		
		/**
  			* Creates a new Zoho AnalyticsClient instance.
  			* @param string $client_id Client id of the user.
  			* @param string $client_secret Client secret of the user.
  			* @param string $refresh_token Refresh token of the user.
  			* <a href="https://www.zoho.com/analytics/api/#oauth" target="_blank">click here</a> to know about OAuth.
			* @link 
  		*/
		function __construct($client_id, $client_secret, $refresh_token) {
			$this->client_id = $client_id;
			$this->client_secret = $client_secret;
			$this->refresh_token = $refresh_token;
		}
		
		/**
	     * Returns a new OrgAPI instance.
	     * @param string $org_id The ID of the organization.
	     * @return OrgAPI instance.
	     */
		function getOrgInstance($org_id) {
			return new OrgAPI($this, $org_id);
		}

		/**
	     * Returns a new WorkspaceAPI instance.
	     * @param string $org_id The ID of the organization.
	     * @param string $workspace_id The ID of the workspace.
	     * @return WorkspaceAPI instance.
	     */
		function getWorkspaceInstance($org_id, $workspace_id) {
			return new WorkspaceAPI($this, $org_id, $workspace_id);
		}

		/**
	     * Returns a new ViewAPI instance.
	     * @param string $org_id The ID of the organization.
	     * @param string $workspace_id The ID of the workspace.
	     * @param string $view_id The ID of the view.
	     * @return ViewAPI instance.
	     */
		function getViewInstance($org_id, $workspace_id, $view_id) {
			return new ViewAPI($this, $org_id, $workspace_id, $view_id);
		}

		/**
	     * Returns a new BulkAPI instance.
	     * @param string $org_id The ID of the organization.
	     * @param string $workspace_id The ID of the workspace.
	     * @return BulkAPI instance.
	     */
		function getBulkInstance($org_id, $workspace_id) {
			return new BulkAPI($this, $org_id, $workspace_id);
		}

		/**
  			* Returns the timeout until a connection is established.A value of zero means the timeout is not used.
  			* @return int Connection timeout limit. 
  		*/
		function getConnectionTimeout() {
			return $this->connection_timeout;
		}
		
		/**
  			* Sets the timeout until a connection is established. A value of zero means the timeout is not used. The default value is 15000.
  			* @param int $time_limit An integer value.
  		*/
		function setConnectionTimeout($time_limit) {
			$this->connection_timeout = $time_limit;
		}
		
		/**
  			* Returns the timeout until waiting to read data. A value of zero means the timeout is not used. The default value is 15000.
  			* @return int Read timeout limit. 
  		*/
		function getReadTimeout() {
			return $this->read_timeout;
		}
		
		/**
  			* Sets the timeout until waiting to read data. A value of zero means the timeout is not used. The default value is 15000.
  			* @param int $time_limit An integer value.
  		*/
		function setReadTimeout($time_limit) {
			$this->read_timeout = $time_limit;
		}

		/**
  			* Used to specify the proxy server details.
  			* @param string $proxy_host The hostname/ip address of the proxy-server.
  			* @param int $proxy_port The proxy server port.
  			* @param string $proxy_type Can be any one ( HTTP , HTTPS , BOTH ).Specify "BOTH" if same configuration can be used for both HTTP and HTTPS.
  			* @param string $proxy_user_name The user name for proxy-server authentication.
  			* @param string $proxy_password The password for proxy-server authentication.
  		*/
		function setProxy($proxy_host, $proxy_port, $proxy_type, $proxy_user_name, $proxy_password) {
			$this->proxy = TRUE;
			$this->proxy_host = $proxy_host;
			$this->proxy_port = $proxy_port;
			$this->proxy_user_name = $proxy_user_name;
			$this->proxy_password = $proxy_password;
			$this->proxy_type = $proxy_type;
		}

                
                /**
  			* @internal Send batch import API request and get response from the server.
  		*/
  		protected function sendBatchImportAPIRequest(
			$endpoint,
			$file_path,
			$batch_size,
			$config,
			$request_headers,
			$tool_config = array()
		) {
			if ($this->access_token == null) {
				$this->regenerateAnalyticsOAuthToken();
			}
		
			$request_url = $this->analytics_server_url . $endpoint;
			$config["batchKey"] = "start";
		
			/* ---------- CSV CONFIG ---------- */
		
			$delimiter_index = isset($config["delimiter"]) ? $config["delimiter"] : 0;
			$delimiters = array(",", "\t", ";", " ", "|");
			$delimiter = $delimiters[$delimiter_index];
		
			$quote_index = isset($config["quoted"]) ? $config["quoted"] : 2;
			$quote_chars = array("\0", "'", '"');
			$enclosure = $quote_chars[$quote_index];
		
			$is_first_row_header = isset($tool_config["isFirstRowHeader"])
				? $tool_config["isFirstRowHeader"]
				: true;
		
		
			$csv = new SplFileObject($file_path, "r");
			$csv->setFlags(SplFileObject::READ_CSV);
			$csv->setCsvControl($delimiter, $enclosure);
		
			if ($is_first_row_header) {
				$headers = $csv->fgetcsv();
				if ($headers === false) {
					return null;
				}
			} else {
				if (empty($tool_config["columnHeaders"])) {
					throw new Exception(
						"columnHeaders cannot be empty when isFirstRowHeader is false"
					);
				}
				$headers = $tool_config["columnHeaders"];
			}
		
			$is_last_batch = false;
		
			while (!$is_last_batch) {
		
				$temp_file = tmpfile();
				$meta = stream_get_meta_data($temp_file);
				$temp_path = $meta["uri"];
		
				// Write CSV safely
				fputcsv($temp_file, $headers, $delimiter, $enclosure);
		
				$record_count = 0;
		
				while ($record_count < $batch_size && !$csv->eof()) {
					$row = $csv->fgetcsv();
		
					if ($row === false || $row === array(null)) {
						continue;
					}
		
					fputcsv($temp_file, $row, $delimiter, $enclosure);
					$record_count++;
				}
		
				if ($record_count === 0) {
					fclose($temp_file);
					break;
				}
		
				$is_last_batch = $csv->eof();
				$config["isLastBatch"] = $is_last_batch ? "true" : "false";
		
				$post_fields = array(
					"FILE"   => new CURLFile($temp_path),
					"CONFIG" => json_encode($config)
				);
		
				$respArr = $this->submitImportRequest(
					"POST",
					$request_url,
					$request_headers,
					$this->access_token,
					$post_fields
				);
		
				$resp_code = $respArr["statusCode"];
				$resp_content = $respArr["response"];
		
				if (substr($resp_code, 0, 1) != '2' && $resp_content != false &&
					$this->isOAuthExpired($resp_content)) {
		
					$this->regenerateAnalyticsOAuthToken();
		
					$respArr = $this->submitImportRequest(
						"POST",
						$request_url,
						$request_headers,
						$this->access_token,
						$post_fields
					);
		
					$resp_code = $respArr["statusCode"];
					$resp_content = $respArr["response"];
				}
		
				if (substr($resp_code, 0, 1) != '2') {
					fclose($temp_file);
					throw new ServerException($resp_content, false);
				}
		
				if ($resp_content !== false) {
					$response = json_decode($resp_content, true);
					if (json_last_error()) {
						$resp_content = stripslashes($resp_content);
						$response = json_decode($resp_content, true);
					}
					if (json_last_error()) {
						fclose($temp_file);
						throw new ParseException(
							"Returned JSON format is not proper. Could possibly be version mismatch"
						);
					}
		
					$config["batchKey"] = $response["data"]["batchKey"];
				}
		
				fclose($temp_file);
		
				if (!$is_last_batch) {
					sleep(2);
				}
			}
		
			return isset($response) ? $response : null;
		}
		
                
  		/**
  			* @internal Send import API request and get response from the server.
  		*/
  		protected function sendImportAPIRequest($endpoint, $post_fields, $request_headers) {
  			$request_url = $this->analytics_server_url . $endpoint;
  			$response = NULL;

			if($this->access_token == null) {
				$this->regenerateAnalyticsOAuthToken();
			}

			$respArr = $this->submitImportRequest("POST", $request_url, $request_headers, $this->access_token, $post_fields);
			
			$resp_code = $respArr["statusCode"];
			$resp_content = $respArr["response"];
			
			if(substr($resp_code, 0, 1) != '2' && $resp_content != FALSE && $this->isOAuthExpired($resp_content)) {
				$this->regenerateAnalyticsOAuthToken();
				$respArr = $this->submitImportRequest("POST", $request_url, $request_headers, $this->access_token, $post_fields);
				$resp_code = $respArr["statusCode"];
				$resp_content = $respArr["response"];
			}

			if(substr($resp_code, 0, 1) != '2') {
				throw new ServerException($resp_content, FALSE);
			}

			//For success - no response case
			if($resp_content == FALSE) {
				return;
			}

			
			$json_response = json_decode($resp_content, TRUE);
			if(json_last_error() != JSON_ERROR_NONE) {
				$resp_content = stripslashes($resp_content);
				$json_response = json_decode($resp_content, TRUE);
			}
			if(json_last_error()) {
				throw new ParseException("Returned JSON format is not proper. Could possibly be version mismatch");
			}

			return $json_response;
		}

		/**
  			* @internal Send import API request and get response from the server.
  		*/
		protected function submitImportRequest($request_method, $request_uri, $request_headers, $access_token = NULL, $post_fields = NULL) {
			
			if($access_token != NULL) {
				$request_headers[]  = "Authorization: Zoho-oauthtoken " . $access_token;
			}
			$request_headers[] = "User-Agent: Analytics PHP Client v2_" . self::CLIENT_VERSION;

			$HTTP_request = curl_init();
			$this->applyTlsHardening($HTTP_request);
			curl_setopt($HTTP_request, CURLOPT_URL, $request_uri);
			curl_setopt($HTTP_request, CURLOPT_RETURNTRANSFER, TRUE);
			curl_setopt($HTTP_request, CURLOPT_FOLLOWLOCATION, TRUE);
			
			//Setting request method
			curl_setopt($HTTP_request, CURLOPT_CUSTOMREQUEST, $request_method);
			
			//Setting request header
			curl_setopt($HTTP_request, CURLOPT_HTTPHEADER, $request_headers);
			
			//Setting connection and read timeout
			curl_setopt($HTTP_request, CURLOPT_CONNECTTIMEOUT, $this->connection_timeout);
			curl_setopt($HTTP_request, CURLOPT_TIMEOUT, $this->read_timeout);
			
			//Adding post fileds data
			if($post_fields != NULL) {
				curl_setopt($HTTP_request, CURLOPT_POST, 1);
				curl_setopt($HTTP_request, CURLOPT_POSTFIELDS, $post_fields);
			}
			
			//Setting proxy configuration
			if($this->proxy == TRUE) {
				curl_setopt($HTTP_request, CURLOPT_PROXY, $this->proxy_host);
				curl_setopt($HTTP_request, CURLOPT_PROXYTYPE, $this->proxy_type);
				curl_setopt($HTTP_request, CURLOPT_PROXYPORT, $this->proxy_port);
				curl_setopt($HTTP_request, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
				curl_setopt($HTTP_request, CURLOPT_PROXYUSERPWD, "$this->proxy_user_name:$this->proxy_password");
			}

    		$HTTP_response = curl_exec($HTTP_request);
			$HTTP_status_code = curl_getinfo($HTTP_request, CURLINFO_HTTP_CODE);

			if($HTTP_response == FALSE && substr($HTTP_status_code, 0, 1) != '2'){
				throw new IOException(curl_error($HTTP_request), $HTTP_status_code);
			}
			$respObj = array();
			$respObj["statusCode"] = $HTTP_status_code;
			$respObj["response"] = $HTTP_response;
			curl_close($HTTP_request);
			
			return $respObj;
		}

		/**
			*@internal Send the export API request.
		*/
		protected function sendExportAPIRequest(
			$endpoint,
			$config,
			$request_headers,
			$file_path = null,
			$stream = false
		) {
			if ($this->access_token == null) {
				$this->regenerateAnalyticsOAuthToken();
			}
		
			$request_url = $this->analytics_server_url . $endpoint;
		
			if (is_array($config) && !empty($config)) {
				$request_url .= "?CONFIG=" . urlencode(json_encode($config));
			}
		
			$fileHandle = null;
			if (!$stream) {
				if ($file_path === null) {
					throw new Exception("file_path is required when stream=false");
				}
				$fileHandle = fopen($file_path, "wb");
			}
		
			$resp = $this->submitExportRequest(
				$request_url,
				$request_headers,
				$this->access_token,
				$fileHandle
			);
		
			$statusCode   = $resp["statusCode"];
			$resp_content = $resp["response"];
		
			if (substr($statusCode, 0, 1) !== '2' && $resp_content && $this->isOAuthExpired($resp_content)) {
				$this->regenerateAnalyticsOAuthToken();
				$resp = $this->submitExportRequest(
					$request_url,
					$request_headers,
					$this->access_token,
					$fileHandle
				);
				$statusCode   = $resp["statusCode"];
				$resp_content = $resp["response"];
			}
		
			if ($fileHandle !== null) {
				fclose($fileHandle);
			}
		
			if (substr($statusCode, 0, 1) !== '2') {
				throw new ServerException($resp_content, false);
			}
		
			if ($stream) {
				$streamHandle = fopen("php://temp", "w+");
				fwrite($streamHandle, $resp_content);
				rewind($streamHandle);
				return $streamHandle;
			}
		
			return null;
		}
		
		
		
		protected function submitExportRequest(
			$request_url,
			$request_headers,
			$access_token,
			$fileHandle = null
		) {
			$ch = curl_init();
			$this->applyTlsHardening($ch);
		
			if ($access_token != null) {
				$request_headers[] = "Authorization: Zoho-oauthtoken " . $access_token;
			}
			$request_headers[] = "User-Agent: Analytics PHP Client v2_" . self::CLIENT_VERSION;
		
			curl_setopt($ch, CURLOPT_URL, $request_url);
			curl_setopt($ch, CURLOPT_HTTPGET, true);
			curl_setopt($ch, CURLOPT_HTTPHEADER, $request_headers);
			curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
			curl_setopt($ch, CURLOPT_FAILONERROR, false);
			curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $this->connection_timeout);
			curl_setopt($ch, CURLOPT_TIMEOUT, $this->read_timeout);
		
			$responseBody = '';
		
			curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $data) use ($fileHandle, &$responseBody) {
				$responseBody .= $data;
				if ($fileHandle !== null) {
					fwrite($fileHandle, $data);
				}
				return strlen($data);
			});
		
			curl_exec($ch);
			$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		
			if ($responseBody === false && substr($statusCode, 0, 1) !== '2') {
				throw new IOException(curl_error($ch), $statusCode);
			}
		
			curl_close($ch);
		
			return [
				"statusCode" => $statusCode,
				"response"   => $responseBody
			];
		}
		

		/**
			*@internal Send the API request.
		*/
  		protected function sendAPIRequest($request_method, $endpoint, $config, $request_headers) {
  			$request_url = $this->analytics_server_url . $endpoint;
  			$response = NULL;
  			
  			if ($config != NULL) {
  				$config = array_diff($config, array(""));
				if(is_array($config) && count($config) > 0) {
					$parameters =  "CONFIG=" . urlencode(json_encode($config));
					$request_url = $request_url . "?" . $parameters;
				}
  			}

			if($this->access_token == null) {
				$this->regenerateAnalyticsOAuthToken();
			}

			$respArr = $this->submitRequest($request_method, $request_url, $request_headers, $this->access_token);
			
			$resp_code = $respArr["statusCode"];
			$resp_content = $respArr["response"];
			
			if(substr($resp_code, 0, 1) != '2' && $resp_content != FALSE && $this->isOAuthExpired($resp_content)) {
				$this->regenerateAnalyticsOAuthToken();
				$respArr = $this->submitRequest($request_method, $request_url, $request_headers, $this->access_token);
				$resp_code = $respArr["statusCode"];
				$resp_content = $respArr["response"];
			}

			if(substr($resp_code, 0, 1) != '2') {
				throw new ServerException($resp_content, FALSE);
			}

			//For success - no response case
			if($resp_content == FALSE) {
				return;
			}

			$json_response = json_decode($resp_content, TRUE);
			if(json_last_error() != JSON_ERROR_NONE) {
				$resp_content = stripslashes($resp_content);
				$json_response = json_decode($resp_content, TRUE);
			}
			if(json_last_error()) {
				throw new ParseException("Returned JSON format is not proper. Could possibly be version mismatch");
			}

			return $json_response;
		}

		/**
  			* @internal Send request and get response from the server.
  		*/
		protected function submitRequest($request_method, $request_uri, $request_headers, $access_token = NULL) {
			$post_fields = NULL;
			
			if($access_token != NULL) {
				$request_headers[]  = "Authorization: Zoho-oauthtoken " . $access_token;
			}
			$request_headers[] = "User-Agent: Analytics PHP Client v2_" . self::CLIENT_VERSION;

			$HTTP_request = curl_init();
			$this->applyTlsHardening($HTTP_request);
			curl_setopt($HTTP_request, CURLOPT_URL, $request_uri);
			curl_setopt($HTTP_request, CURLOPT_RETURNTRANSFER, TRUE);
			curl_setopt($HTTP_request, CURLOPT_FOLLOWLOCATION, TRUE);
			
			//Setting request method
			curl_setopt($HTTP_request, CURLOPT_CUSTOMREQUEST, $request_method);
			
			//Setting request header
			curl_setopt($HTTP_request, CURLOPT_HTTPHEADER, $request_headers);
			
			//Setting connection and read timeout
			curl_setopt($HTTP_request, CURLOPT_CONNECTTIMEOUT, $this->connection_timeout);
			curl_setopt($HTTP_request, CURLOPT_TIMEOUT, $this->read_timeout);
			
			//Adding post fileds data
			if($post_fields != NULL) {
				curl_setopt($HTTP_request, CURLOPT_POST, 1);
				curl_setopt($HTTP_request, CURLOPT_POSTFIELDS, $post_fields);
			}
			
			//Setting proxy configuration
			if($this->proxy == TRUE) {
				curl_setopt($HTTP_request, CURLOPT_PROXY, $this->proxy_host);
				curl_setopt($HTTP_request, CURLOPT_PROXYTYPE, $this->proxy_type);
				curl_setopt($HTTP_request, CURLOPT_PROXYPORT, $this->proxy_port);
				curl_setopt($HTTP_request, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
				curl_setopt($HTTP_request, CURLOPT_PROXYUSERPWD, "$this->proxy_user_name:$this->proxy_password");
			}

    		$HTTP_response = curl_exec($HTTP_request);
			$HTTP_status_code = curl_getinfo($HTTP_request, CURLINFO_HTTP_CODE);

			if($HTTP_response == FALSE && substr($HTTP_status_code, 0, 1) != '2'){
				throw new IOException(curl_error($HTTP_request), $HTTP_status_code);
			}
			$respObj = array();
			$respObj["statusCode"] = $HTTP_status_code;
			$respObj["response"] = $HTTP_response;
			curl_close($HTTP_request);
			
			return $respObj;
		}

		/**
			*@internal For getting OAuth token to invoke API.
		*/
  		private function regenerateAnalyticsOAuthToken() {
  			$endpoint = $this->accounts_server_url . "/oauth/v2/token";
  			$parameters = "client_id=" . $this->client_id . "&client_secret=" . $this->client_secret . "&refresh_token=" . $this->refresh_token . "&grant_type=refresh_token";

  			$request_url = $endpoint . "?" . $parameters;
			$respArr = $this->submitRequest("POST", $request_url, NULL, NULL);
			$oauth_status_code = $respArr["statusCode"];
			$oauth_response = $respArr["response"];
			if($oauth_response != FALSE) {
				if($oauth_status_code == 200) {
					$json_response = json_decode($oauth_response, TRUE);
					if(json_last_error() != JSON_ERROR_NONE){
						$oauth_response = stripslashes($oauth_response);
						$json_response = json_decode($oauth_response, TRUE);
					}
					if(json_last_error()) {
						throw new ParseException("Regenerate OAuthToken response is not proper. Invalid JSON data. Response - " . $oauth_response);
					}
					if(array_key_exists("access_token", $json_response)) {
						$this->access_token = $json_response["access_token"];
						return ;
					}
				}
				throw new ServerException($oauth_response, TRUE);
			}
			else {
				throw new Exception("Internal error occurred.");
			}
  		}

		/**
			*@internal For validating OAuth token.
		*/
  		private function isOAuthExpired($resp_content) {
  			$json_response = json_decode($resp_content, TRUE);
			if(json_last_error() != JSON_ERROR_NONE){
				$resp_content = stripslashes($resp_content);
				$json_response = json_decode($resp_content, TRUE);
			}
			if(json_last_error()) {
				throw new ParseException("API response is not proper. Invalid JSON data. Response - " . $resp_content);
			}
			$error_code = $json_response["data"]["errorCode"];
			if($error_code == 8535) {
				return TRUE;
			}
			else {
				return FALSE;
			}
  		}

		/**
			* @internal Apply strong TLS hardening to a curl handle.
			*
			* Restricts the handshake to TLS 1.2+ and (where supported) constrains the
			* cipher list to strong AEAD suites. Errors are suppressed and the
			* CURLOPT_TLS13_CIPHERS constant is feature-detected so the request still
			* goes through on older PHP / libcurl versions rather than being rejected.
		*/
		private function applyTlsHardening($ch) {
			@curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, TRUE);
			@curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
			// CURL_SSLVERSION_TLSv1_2 = 6
			@curl_setopt($ch, CURLOPT_SSLVERSION, 6);
			@curl_setopt($ch, CURLOPT_SSL_CIPHER_LIST,
				'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305');
			if (defined('CURLOPT_TLS13_CIPHERS')) {
				@curl_setopt($ch, CURLOPT_TLS13_CIPHERS,
					'TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256');
			}
		}
	}

	class OrgAPI extends AnalyticsClient
	{
		private $ac;
		private $req_headers = array();

		/**
  			* Creates a new OrgAPI instance.
  			* @param AnalyticsClient $ac AnalyticsClient instance.
  			* @param string $org_id The ID of the organization.
  		*/
		function __construct($ac, $org_id) {
			$this->ac = $ac;
			$this->req_headers[] = "ZANALYTICS-ORGID: " . $org_id;
		}

		/**
	     * Returns the workspaces of the specified organization that the authenticated user can reach.
	     * An Account Admin and an Organization Admin receive every active workspace of the organization,
	     * every other user receives only the workspaces shared with them.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Workspace list.
	     */
		function getOrgWorkspaces() {
			$endpoint = "/restapi/v2/orgs/workspaces";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["workspaces"];
		}

		/**
	     * Returns the dashboards of the specified organization that the authenticated user may read,
	     * across the workspaces the user can reach or across the workspaces named in workspaceIds.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Dashboards of the page along with the paging details.
	     */
		function getOrgDashboards($config = array()) {
			$endpoint = "/restapi/v2/orgs/dashboards";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Returns the views the authenticated user opened most recently in the specified organization,
	     * newest first. At most 20 items are returned.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() View list.
	     */
		function getOrgRecentItems() {
			$endpoint = "/restapi/v2/orgs/recentitems";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Returns details of the specified view in the organization.
	     * @param string $view_id The ID of the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() View details.
	     */
		function getViewDetails($view_id, $config = array()) {
			$endpoint = "/restapi/v2/views/" . $view_id;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Returns a new BulkAPI instance.
	     * @param string $workspace_name Name of the workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created workspace id.
	     */
		function createWorkspace($workspace_name, $config = array()) {
			$endpoint = "/restapi/v2/workspaces";
			$config["workspaceName"] = $workspace_name;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["workspaceId"];
		}

		/**
	     * Returns list of admins for a specified organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Organization admin list.
	     */
		function getAdmins() {
			$endpoint = "/restapi/v2/orgadmins";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["orgAdmins"];
		}

		/**
	     * Returns subscription details of the specified organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Subscription details.
	     */
		function getSubscriptionDetails() {
			$endpoint = "/restapi/v2/subscription";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["subscription"];
		}

		/**
	     * Returns resource usage details of the specified organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Resource details.
	     */
		function getResourceDetails() {
			$endpoint = "/restapi/v2/resources";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["resourceDetails"];
		}

		/**
	     * Returns list of users for the specified organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() User list.
	     */
		function getUsers() {
			$endpoint = "/restapi/v2/users";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["users"];
		}

		/**
	     * Add users to the specified organization.
	     * @param array() $email_ids The email address of the users to be added.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function addUsers($email_ids, $config = array()) {
			$endpoint = "/restapi/v2/users";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Remove users from the specified organization.
	     * @param array() $email_ids The email address of the users to be removed.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeUsers($email_ids, $config = array()) {
			$endpoint = "/restapi/v2/users";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Activate users in the specified organization.
	     * @param array() $email_ids The email address of the users to be activated.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function activateUsers($email_ids, $config = array()) {
			$endpoint = "/restapi/v2/users/active";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Deactivate users in the specified organization.
	     * @param array() $email_ids The email address of the users to be deactivated.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deactivateUsers($email_ids, $config = array()) {
			$endpoint = "/restapi/v2/users/inactive";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Change role for the specified users.
	     * @param array() $email_ids The email address of the users.
	     * @param string $role New role for the users.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function changeUserRole($email_ids, $role, $config = array()) {
			$endpoint = "/restapi/v2/users/role";
			$config["emailIds"] = $email_ids;
			$config["role"] = $role;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns details of the specified workspace/view.
	     * @param string $workspace_name Name of the workspace.
	     * @param string $view_name Name of the view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Workspace (or) View meta details.
	     */
		function getMetaDetails($workspace_name, $view_name) {
			$endpoint = "/restapi/v2/metadetails";
			$config = array();
			$config["workspaceName"] = $workspace_name;
			if ($view_name != NULL) {
				$config["viewName"] = $view_name;
			}
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}

		/**
		 * Returns all AutoML analysis available in an organization.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array List of AutoML analysis.
		 */
		function getAutoMLAnalysis() {
			$endpoint = "/restapi/v2/automl/analysis";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["analysis"];
		}
		/**
		 * Returns list of custom roles for the specified organization.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array Custom role list.
		 */
		function getCustomRoles() {
			$endpoint = "/restapi/v2/orgs/roles";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["roles"];
		}
		/**
		 * Create a new custom role in the specified organization.
		 *
		 * @param string $role_name Name of the custom role to be created.
		 * @param string $access_type Access type for the custom role.
		 * @param array $permissions Contains the permission details for the custom role.
		 * @param array $config Optional control parameters.
		 * @return string Created custom role id.
		 */
		function createCustomRole($role_name, $access_type, $permissions, $config = array()) {
			$endpoint = "/restapi/v2/orgs/roles";
			$config["roleName"] = $role_name;
			$config["accessType"] = $access_type;
			$config["permissions"] = $permissions;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return (string) $response["data"]["roleId"];
		}
		/**
		 * Update the specified custom role in the organization.
		 *
		 * @param string $role_id Id of the custom role.
		 * @param string $role_name New name for the custom role.
		 * @param string $access_type Access type for the custom role.
		 * @param array $permissions Contains the permission details for the custom role.
		 * @param array $config Optional control parameters.
		 */
		function updateCustomRole($role_id, $role_name, $access_type, $permissions, $config = array()) {
			$endpoint = "/restapi/v2/orgs/roles/" . $role_id;
			$config["roleName"] = $role_name;
			$config["accessType"] = $access_type;
			$config["permissions"] = $permissions;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}
		/**
		 * Delete the specified custom role from the organization.
		 *
		 * @param string $role_id Id of the custom role.
		 */
		function deleteCustomRole($role_id) {
			$endpoint = "/restapi/v2/orgs/roles/" . $role_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns the access restriction settings configured for the organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Organization access restriction settings.
	     */
		function getOrgAccessRestrictions() {
			$endpoint = "/restapi/v2/security-controls/access-restrictions";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Update the access restriction settings of the organization.
	     * @param array() $config Contains the access restriction configurations to be updated.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateOrgAccessRestrictions($config = array()) {
			$endpoint = "/restapi/v2/security-controls/access-restrictions";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of linked workspaces available in the specified organization.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Linked workspaces list.
	     */
		function getLinkedWorkspaces() {
			$endpoint = "/restapi/v2/linkedworkspaces";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["linkedWorkspaces"];
		}

	}

	class WorkspaceAPI extends AnalyticsClient
	{
		private $ac;
		private $workspace_end_point;
		private $security_controls_end_point;
		private $workspace_id;
		private $req_headers = array();

		/**
  			* Creates a new WorkspaceAPI instance.
  			* @param AnalyticsClient $ac AnalyticsClient instance.
  			* @param string $org_id The ID of the organization.
  			* @param string $workspace_id The ID of the workspace.
  		*/
		function __construct($ac, $org_id, $workspace_id) {
			$this->ac = $ac;
			$this->workspace_end_point = "/restapi/v2/workspaces/" . $workspace_id;
			$this->security_controls_end_point = "/restapi/v2/security-controls/workspaces/" . $workspace_id;
			$this->req_headers[] = "ZANALYTICS-ORGID: " . $org_id;
			$this->workspace_id = $workspace_id;
		}

		/**
  			* Returns details of the specified workspace.
  			* @param array() $config Contains any additional control parameters. Can be null.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  			* @return array() Workspace details.
  		*/
		function getWorkspaceDetails($config = array()) {
			$response = $this->ac->sendAPIRequest("GET", $this->workspace_end_point, $config, $this->req_headers);
			return $response["data"]["workspaces"];
		}

		/**
  			* Copy the specified workspace from one organization to another or within the organization.
  			* @param string $new_workspace_name Name of the new workspace.
  			* @param array() $config Contains any additional control parameters. Can be null.
  			* @param string $dest_org_id Id of the organization where the destination workspace is present. Can be null.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  			* @return string Copied workspace id.
  		*/
		function copy($new_workspace_name, $config = array(), $dest_org_id=NULL) {
			$config["newWorkspaceName"] = $new_workspace_name;
			$request_headers = $this->req_headers;
			if ($dest_org_id != NULL) {
				$request_headers[]  = "ZANALYTICS-DEST-ORGID: " . $dest_org_id;
			}
			$response = $this->ac->sendAPIRequest("POST", $this->workspace_end_point, $config, $request_headers);
			return $response["data"]["workspaceId"];
		}

		/**
  			* Rename a specified workspace in the organization.
  			* @param string $workspace_name New name for the workspace.
  			* @param array() $config Contains any additional control parameters. Can be null.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function rename($workspace_name, $config = array()) {
			$config["workspaceName"] = $workspace_name;
			$this->ac->sendAPIRequest("PUT", $this->workspace_end_point, $config, $this->req_headers);
		}

		/**
  			* Delete a specified workspace in the organization.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function delete() {
			$this->ac->sendAPIRequest("DELETE", $this->workspace_end_point, NULL, $this->req_headers);
		}

		/**
  			* Returns the secret key of the specified workspace.
  			* @param array() $config Contains any additional control parameters. Can be null.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  			* @return string Workspace secret key.
  		*/
		function getSecretKey($config = array()) {
			$endpoint = $this->workspace_end_point . "/secretkey";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["workspaceKey"];
		}

		/**
  			* Adds a specified workspace as favorite.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function addFavorite() {
			$endpoint = $this->workspace_end_point . "/favorite";
			$this->ac->sendAPIRequest("POST", $endpoint, NULL, $this->req_headers);
		}

		/**
  			* Remove a specified workspace from favorite.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function removeFavorite() {
			$endpoint = $this->workspace_end_point . "/favorite";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
  			* Adds a specified workspace as default.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function addDefault() {
			$endpoint = $this->workspace_end_point . "/default";
			$this->ac->sendAPIRequest("POST", $endpoint, NULL, $this->req_headers);
		}

		/**
  			* Remove a specified workspace from default.
  			* @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
  			* @throws ServerException If the server has received the request but did not process the request due to some error.
  			* @throws ParseException If the server has responded but client was not able to parse the response.
  		*/
		function removeDefault() {
			$endpoint = $this->workspace_end_point . "/default";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns list of admins for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Workspace admin list.
	     */
		function getAdmins() {
			$endpoint = $this->workspace_end_point . "/admins";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["workspaceAdmins"];
		}

		/**
	     * Add admins for the specified workspace.
	     * @param array() $email_ids The email address of the admin users to be added.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function addAdmins($email_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/admins";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Remove admins from the specified workspace.
	     * @param array() $email_ids The email address of the admin users to be removed.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeAdmins($email_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/admins";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns shared details of the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Workspace share info.
	     */
		function getShareInfo() {
			$endpoint = $this->workspace_end_point . "/share";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Share views to the specified users.
	     * @param array() $view_ids View ids which to be shared.
	     * @param array() $email_ids The email address of the users to whom the views need to be shared.
	     * @param array() $permissions Contains permission details.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function shareViews($view_ids, $email_ids, $permissions, $config = array()) {
			$endpoint = $this->workspace_end_point . "/share";
			$config["viewIds"] = $view_ids;
			$config["emailIds"] = $email_ids;
			$config["permissions"] = $permissions;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Remove shared views for the specified users.
	     * @param array() $view_ids View ids whose sharing needs to be removed.
	     * @param array() $email_ids The email address of the users to whom the sharing need to be removed.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeShare($view_ids, $email_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/share";
			$config["emailIds"] = $email_ids;
			if ($view_ids != NULL) {
				$config["viewIds"] = $view_ids;
			}
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns shared details of the specified views.
	     * @param array() $view_ids View ids for which sharing details are required.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function getSharedDetailsForViews($view_ids) {
			$endpoint = $this->workspace_end_point . "/share/shareddetails";
			$config = array();
			$config["viewIds"] = $view_ids;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["sharedDetails"];
		}

		/**
	     * Returns list of all accessible folders for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Folder list.
	     */
		function getFolders() {
			$endpoint = $this->workspace_end_point . "/folders";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["folders"];
		}

		/**
	     * Create a folder in the specified workspace.
	     * @param string $folder_name Name of the folder to be created.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created folder id.
	     */
		function createFolder($folder_name, $config = array()) {
			$endpoint = $this->workspace_end_point . "/folders";
			$config["folderName"] = $folder_name;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["folderId"];
		}

        /**
	     * Rename a specified folder in the workspace.
	     * @param string $folder_id Id of the folder.
	     * @param string $folder_name New name for the folder.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function renameFolder($folder_id, $folder_name, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/folders/" . $folder_id;
            $config["folderName"] = $folder_name;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Swaps the hierarchy of a parent folder and a subfolder.
	     * @param string $folder_id Id of the folder.
	     * @param int $hierarchy New hierarchy for the folder. (0 - Parent; 1 - Child)
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function changeFolderHierarchy($folder_id, $hierarchy, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/folders/" . $folder_id . "/move";
            $config["hierarchy"] = $hierarchy;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Place the folder above the reference folder.
	     * @param string $folder_id Id of the folder.
	     * @param string $reference_folder_id Id of the reference folder.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function changeFolderPosition($folder_id, $reference_folder_id, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/folders/" . $folder_id . "/reorder";
            $config["reference_folder_id"] = $reference_folder_id;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Place the folder above the reference folder.
	     * @param string $folder_id Id of the folder.
	     * @param string $referenceFolderId Id of the reference folder.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function moveViewsToFolder($folder_id, $view_ids, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/views/movetofolder";
            $config["viewIds"] = $view_ids;
            $config["folderId"] = $folder_id;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Delete a specified folder in the workspace.
	     * @param string $folder_id Id of the folder.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteFolder($folder_id) {
        	$endpoint = $this->workspace_end_point . "/folders/" . $folder_id;
            $this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
        }

		/**
	     * Returns list of all accessible views for the specified workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() View list.
	     */
		function getViews($config = array()) {
			$endpoint = $this->workspace_end_point . "/views";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Create a table in the specified workspace.
	     * @param array() $table_design Table structure.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created table id.
	     */
		function createTable($table_design) {
			$endpoint = $this->workspace_end_point . "/tables";
			$config = array();
			$config["tableDesign"] = $table_design;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["viewId"];
		}

		/**
	     * Create a new query table in the workspace.
	     * @param string $sql_query SQL query to construct the query table.
	     * @param string $query_table_name Name of the query table to be created.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created query table id.
	     */
		function createQueryTable($sql_query, $query_table_name, $config = array()) {
			$endpoint = $this->workspace_end_point . "/querytables";
			$config["sqlQuery"] = $sql_query;
			$config["queryTableName"] = $query_table_name;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["viewId"];
		}

		/**
	     * Returns list of all query tables for the specified workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Query table list.
	     */
		function getQueryTables($config = array()) {
			$endpoint = $this->workspace_end_point . "/querytables";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["queryTables"];
		}
		/**
	     * Update the mentioned query table in the workspace.
	     * @param string $view_id Id of the query table to be updated.
	     * @param string $sql_query SQL query to construct the query table.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function editQueryTable($view_id, $sql_query, $config = array()) {
			$endpoint = $this->workspace_end_point . "/querytables/" . $view_id;
			$config["sqlQuery"] = $sql_query;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Copy the specified views from one workspace to another workspace.
	     * @param array() $view_ids The id of the views to be copied.
	     * @param string $dest_workspace_id The destination workspace id.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @param string $dest_org_id Id of the organization where the destination workspace is present. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() View list.
	     */
		function copyViews($view_ids, $dest_workspace_id, $config = array(), $dest_org_id=NULL) {
			$endpoint = $this->workspace_end_point . "/views/copy";
			$config["viewIds"] = $view_ids;
			$config["destWorkspaceId"] = $dest_workspace_id;
			$request_headers = $this->req_headers;
			if ($dest_org_id != NULL) {
				$request_headers[]  = "ZANALYTICS-DEST-ORGID: " . $dest_org_id;
			}
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $request_headers);
			return $response["data"]["views"];
		}

		/**
	     * Returns list of groups for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Group list.
	     */
		function getGroups() {
			$endpoint = $this->workspace_end_point . "/groups";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["groups"];
		}

        /**
	     * Get the details of the specified group.
	     * @param string $group_id Id of the group.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Details of the specified group.
	     */
		function getGroupDetails($group_id) {
        	$endpoint = $this->workspace_end_point . "/groups/" . $group_id;
            $response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
            return $response["data"]["groups"];
        }

		/**
	     * Create a group in the specified workspace.
	     * @param string $group_name Name of the group.
	     * @param array() $email_ids The email address of the users to be added to the group.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created group id.
	     */
		function createGroup($group_name, $email_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/groups";
			$config["groupName"] = $group_name;
			$config["emailIds"] = $email_ids;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["groupId"];
		}

        /**
	     * Rename a specified group.
	     * @param string $group_id Id of the group.
	     * @param string $new_group_name New name for the group.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function renameGroup($group_id, $new_group_name, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/groups/" . $group_id;
            $config["groupName"] = $new_group_name;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Delete a specified group.
	     * @param string $group_id Id of the group.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteGroup($group_id) {
        	$endpoint = $this->workspace_end_point . "/groups/" . $group_id;
            $this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
        }

        /**
	     * Add users to the specified group.
	     * @param string $group_id Id of the group.
	     * @param array() $email_ids The email address of the users to be added to the group.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function addGroupMembers($group_id, $email_ids, $config = array()) {
            $endpoint = $this->workspace_end_point . "/groups/" . $group_id . "/members";
            $config["emailIds"] = $email_ids;
            $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Remove users from the specified group.
	     * @param string $group_id Id of the group.
	     * @param array() $email_ids The email address of the users to be removed from the group.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeGroupMembers($group_id, $email_ids, $config = array()) {
            $endpoint = $this->workspace_end_point . "/groups/" . $group_id . "/members";
            $config["emailIds"] = $email_ids;
            $this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
        }

		/**
	     * Create a slideshow in the specified workspace.
	     * @param string $slide_name Name of the slideshow.
	     * @param array() $view_ids Ids of the view to be included in the slideshow.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created slideshow id.
	     */
		function createSlideshow($slide_name, $view_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/slides";
			$config["slideName"] = $slide_name;
			$config["viewIds"] = $view_ids;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["slideId"];
		}

        /**
	     * Update details of the specified slideshow.
	     * @param string $slide_id Id of the slideshow.
	     * @param array() $config Contains the control configurations
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created slideshow id.
	     */
		function updateSlideshow($slide_id, $config = array()) {
        	$endpoint = $this->workspace_end_point . "/slides/" . $slide_id;
            $endpoint = $this->slide_end_point;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Delete a specified slideshow in the workspace.
	     * @param string $slide_id Id of the slideshow.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteSlideshow($slide_id) {
            $endpoint = $this->workspace_end_point . "/slides/" . $slide_id;
            $this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
        }

        /**
	     * Returns list of slideshows for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Slideshow list.
	     */
		function getSlideshows() {
			$endpoint = $this->workspace_end_point . "/slides";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["slideshows"];
		}

        /**
	     * Returns details of the specified slideshow.
	     * @param string $slide_id Id of the slideshow.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Slideshow details.
	     */
		function getSlideshowDetails($slide_id) {
            $endpoint = $this->workspace_end_point . "/slides/" . $slide_id;
            $response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
            return $response["data"]["slideInfo"];
        }

        /**
	     * Returns slide URL to access the specified slideshow.
	     * @param string $slide_id Id of the slideshow.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Slideshow URL.
	     */
        function getSlideshowUrl($slide_id, $config = array()) {
            $endpoint = $this->workspace_end_point . "/slides/" . $slide_id . "/publish";
            $response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
            return $response["data"]["slideUrl"];
        }

		/**
	     * Enable workspace to the specified white label domain.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
        function enableDomainAccess() {
			$endpoint = $this->workspace_end_point . "/wlaccess";
			$this->ac->sendAPIRequest("POST", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Disable workspace from the specified white label domain.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
        function disableDomainAccess() {
			$endpoint = $this->workspace_end_point . "/wlaccess";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Create a variable in the workspace.
	     * @param string $variable_name Name of the variable to be created.
	     * @param string $variable_datatype Datatype of the variable to be created.
	     * @param string $variable_type Type of the variable to be created.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created variable id.
	     */
		function createVariable($variable_name, $variable_datatype, $variable_type, $config = array()) {
			$endpoint = $this->workspace_end_point . "/variables";
			$config["variableName"] = $variable_name;
			$config["variableDataType"] = $variable_datatype;
			$config["variableType"] = $variable_type;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["variableId"];
		}

		/**
	     * Update details of the specified variable in the workspace.
	     * @param string $variable_id Id of the variable.
	     * @param string $variable_name New name for the variable.
	     * @param string $variable_datatype New datatype for the variable.
	     * @param string $variable_type New type for the variable.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateVariable($variable_id, $variable_name, $variable_datatype, $variable_type, $config = array()) {
			$endpoint = $this->workspace_end_point . "/variables/" . $variable_id;
			$config["variableName"] = $variable_name;
			$config["variableDataType"] = $variable_datatype;
			$config["variableType"] = $variable_type;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Delete the specified variable in the workspace.
	     * @param string $variable_id Id of the variable.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteVariable($variable_id) {
			$endpoint = $this->workspace_end_point . "/variables/" . $variable_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns list of variables for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Variables list.
	     */
		function getVariables() {
			$endpoint = $this->workspace_end_point . "/variables";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["variables"];
		}

        /**
	     * Returns details of the specified variable.
	     * @param string $variable_id Id of the variable.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Variable details.
	     */
		function getVariableDetails($variable_id) {
            $endpoint = $this->workspace_end_point . "/variables/" . $variable_id;
            $response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
            return $response["data"];
        }

        /**
	     * Make the specified folder as default.
	     * @param string $folder_id Id of the folder.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function makeDefaultFolder($folder_id) {
			$endpoint = $this->workspace_end_point . "/folders/" . $folder_id . "/default";
			$this->ac->sendAPIRequest("PUT", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns list of datasources for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Datasource list.
	     */
		function getDatasources() {
			$endpoint = $this->workspace_end_point . "/datasources";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["dataSources"];
		}

		/**
	     * Initiate data sync for the specified datasource.
	     * @param string $datasource_id Id of the datasource.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function syncData($datasource_id, $config=array()) {
			$endpoint = $this->workspace_end_point . "/datasources/" . $datasource_id . "/sync";
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Update connection details for the specified datasource.
	     * @param string $datasource_id Id of the datasource.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateDatasourceConnection($datasource_id, $config=array()) {
			$endpoint = $this->workspace_end_point . "/datasources/" . $datasource_id;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of all views available in trash for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Trash view list.
	     */
		function getTrashViews() {
			$endpoint = $this->workspace_end_point . "/trash";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Restore the specified view from trash.
	     * @param string $view_id Id of the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function restoreTrashView($view_id, $config=array()) {
			$endpoint = $this->workspace_end_point . "/trash/" . $view_id;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Delete the specified view permanently from trash.
	     * @param string $view_id Id of the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteTrashView($view_id, $config=array()) {
			$endpoint = $this->workspace_end_point . "/trash/" . $view_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of users for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() User list.
	     */
		function getWorkspaceUsers() {
			$endpoint = $this->workspace_end_point . "/users";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["users"];
		}

		/**
	     * Add users to the specified workspace.
	     * @param array() $email_ids The email address of the users to be added.
	     * @param string $role Role of the user to be added.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function addWorkspaceUsers($email_ids, $role, $config = array()) {
			$endpoint = $this->workspace_end_point . "/users";
			$config["emailIds"] = $email_ids;
			$config["role"] = $role;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Remove users from the specified workspace.
	     * @param array() $email_ids The email address of the users to be removed.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeWorkspaceUsers($email_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/users";
			$config["emailIds"] = $email_ids;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Change users staus in the specified workspace.
	     * @param array() $email_ids The email address of the users.
	     * @param string $operation New status for the users ( Values -  activate | deactivate )
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function changeWorkspaceUserStatus($email_ids, $operation, $config = array()) {
			$endpoint = $this->workspace_end_point . "/users/status";
			$config["emailIds"] = $email_ids;
			$config["operation"] = $operation;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Change role of the specified users in the workspace.
	     * @param array() $email_ids The email address of the users.
	     * @param string $role Name of the role.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function changeWorkspaceUserRole($email_ids, $role, $config = array()) {
			$endpoint = $this->workspace_end_point . "/users/role";
			$config["emailIds"] = $email_ids;
			$config["role"] = $role;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Export the mentioned table (or) view data.
	     * @param array() $view_ids Ids of the view to be exported.
	     * @param string $file_path Path of the file where the data exported to be stored. ( Should be in 'atpt' format )
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function exportAsTemplate($view_ids, $file_path, $config = array()) {
			$endpoint = $this->data_end_point . "/template/data";
			$config["viewIds"] = $view_ids;
		
			$this->ac->sendExportAPIRequest(
				$endpoint,
				$config,
				$this->req_headers,
				$file_path,
				false
			);
		}
		

		/**
		 * Returns list of email schedules available in the specified workspace.
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 * @return array() List of email schedules.
		 */
		function getEmailSchedules() {
		    $endpoint = $this->workspace_end_point . "/emailschedules";
		    $response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
		    return $response["data"]["emailSchedules"];
		}

		/**
		 * Create an email schedule in the specified workspace.
		 * @param string $schedule_name Name of the email schedule.
		 * @param array() $view_ids View ids to be mailed.
		 * @param string $format The format in which the data has to be mailed.
		 * @param array() $email_ids The recipients' email addresses for sending views.
		 * @param array() $schedule_details Contains schedule frequency, date, and time info.
		 * @param array() $config Contains any additional control parameters. Can be null.
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 * @return string Created email schedule id.
		 */
		function createEmailSchedule($schedule_name, $view_ids, $format, $email_ids, $schedule_details, $config = array()) {
		    $endpoint = $this->workspace_end_point . "/emailschedules";
		    $config["scheduleName"] = $schedule_name;
		    $config["viewIds"] = $view_ids;
		    $config["exportType"] = $format;
		    $config["emailIds"] = $email_ids;
		    $config["scheduleDetails"] = $schedule_details;
		    $response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		    return $response["data"]["scheduleId"];
		}

		/**
		 * Update configurations of the specified email schedule in the workspace.
		 * @param string $schedule_id Id for the email schedule.
		 * @param array() $config Contains the control configurations.
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 * @return string Updated schedule id.
		 */
		function updateEmailSchedule($schedule_id, $config) {
		    $endpoint = $this->workspace_end_point . "/emailschedules/" . $schedule_id;
		    $response = $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		    return $response["data"]["scheduleId"];
		}

		/**
		 * Trigger configured email schedules instantly.
		 * @param string $schedule_id Id for the email schedule.
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 */
		function triggerEmailSchedule($schedule_id) {
		    $endpoint = $this->workspace_end_point . "/emailschedules/" . $schedule_id;
		    $this->ac->sendAPIRequest("POST", $endpoint, NULL, $this->req_headers);
		}

		/**
		 * Update email schedule status.
		 * @param string $schedule_id Id for the email schedule.
		 * @param string $operation New status for the schedule (Values - activate | deactivate).
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 */
		function changeEmailScheduleStatus($schedule_id, $operation) {
		    $endpoint = $this->workspace_end_point . "/emailschedules/" . $schedule_id . "/status";
		    $config = array("operation" => $operation);
		    $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Delete the specified email schedule in the workspace.
		 * @param string $schedule_id Id for the email schedule.
		 * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
		 * @throws ServerException If the server has received the request but did not process the request due to some error.
		 * @throws ParseException If the server has responded but client was not able to parse the response.
		 */
		function deleteEmailSchedule($schedule_id) {
		    $endpoint = $this->workspace_end_point . "/emailschedules/" . $schedule_id;
		    $this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns list of all aggregate formulas for the specified workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Aggregate formula list.
	     */
		function getAggregateFormulas($config = array()) {
			$endpoint = $this->workspace_end_point . "/aggregateformulas";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["aggregateFormulas"];
		}

		/**
	     * Returns list of all dependent views and formulas for the specified aggregate formula.
	     * @param string $formula_id Id for the aggregate formula.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Dependent details.
	     */
		function getAggregateFormulaDependents($formula_id) {
			$endpoint = $this->workspace_end_point . "/aggregateformulas/" . $formula_id . "/dependents";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Returns the value of the aggregate formula.
	     * @param string $formula_id Id for the aggregate formula.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Aggregate formula value.
	     */
		function getAggregateFormulaValue($formula_id) {
			$endpoint = $this->workspace_end_point . "/aggregateformulas/" . $formula_id . "/value";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["formulaValue"];
		}

		/**
	     * Create a report in the specified workspace.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created view id.
	     */
		function createReport($config = array()) {
			$endpoint = $this->workspace_end_point . "/reports";
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["viewId"];
		}

		/**
	     * Update the design and configuration of the specified report.
	     * @param string $view_id Id of the view.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateReport($view_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/reports/" . $view_id;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Returns details of the specified query table.
		 *
		 * @param string $query_table_id Id of the query table.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array Query table details.
		 */
		function getQueryTableDetails($query_table_id) {
			$endpoint = $this->workspace_end_point . "/querytables/" . $query_table_id;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
		 * Returns list of AutoML analysis for the specified workspace.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array List of AutoML analysis.
		 */
		function getAutoMLAnalysis() {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id . "/analysis";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["analysis"];
		}

		/**
		 * Retrieve detailed information for a specific AutoML analysis.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array AutoML analysis details.
		 */
		function getAutoMLAnalysisDetails($analysis_id) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id . "/analysis/" . $analysis_id;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["analysis"];
		}

		/**
		 * Returns deployment details available for an AutoML analysis model.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $model_id Id of the AutoML model.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return array Deployment details.
		 */
		function getDeploymentDetails($analysis_id, $model_id) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/models/" . $model_id . "/deployments";

			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["deployments"];
		}

		/**
		 * Creates a new AutoML analysis within the workspace.
		 *
		 * @param string $name Name of the AutoML analysis.
		 * @param string $training_table_id Training table ID.
		 * @param string $prediction_type Prediction type (REGRESSION | CLASSIFICATION | CLUSTERING).
		 * @param array  $features Feature column names.
		 * @param int    $server_option Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB).
		 * @param array  $algorithms Algorithms configuration.
		 * @param array  $config Optional configuration parameters.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 * @return string Created AutoML analysis ID.
		 */
		function createAutoMLAnalysis(
			$name,
			$training_table_id,
			$prediction_type,
			$features,
			$server_option,
			$algorithms,
			$config = array()
		) {
			$config["name"] = $name;
			$config["trainingTableId"] = $training_table_id;
			$config["predictionType"] = $prediction_type;
			$config["features"] = $features;
			$config["serverOption"] = $server_option;
			$config["algorithms"] = $algorithms;

			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id . "/analysis";
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return (string) $response["data"]["id"];
		}

		/**
		 * Delete a specified AutoML analysis from the workspace.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param array $config Optional control parameters.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 */
		function deleteAutoMLAnalysis($analysis_id, $config = array()) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id . "/analysis/" . $analysis_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Delete a specific model from an AutoML analysis.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $model_id Id of the model to delete.
		 * @param array $config Optional control parameters.
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server fails to process the request.
		 * @throws ParseException If the response cannot be parsed.
		 */
		function deleteAutoMLAnalysisModel($analysis_id, $model_id, $config = array()) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/models/" . $model_id;

			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Create a deployment for an AutoML analysis model.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $model_id Id of the AutoML model.
		 * @param string $input_table_id Input table ID.
		 * @param string $output_table Output table name.
		 * @param array $output_columns Columns to include in output table.
		 * @param string $prediction_column Prediction column name.
		 * @param int $server_option Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB).
		 * @param string $import_type Import type (APPEND | TRUNCATEADD | UPDATEADD).
		 * @param array|null $schedule_details Schedule configuration.
		 * @param array $config Optional control parameters.
		 * @throws IOException
		 * @throws ServerException
		 * @throws ParseException
		 * @return array Deployment details.
		 */
		function createAutoMLAnalysisDeployment(
			$analysis_id,
			$model_id,
			$input_table_id,
			$output_table,
			$output_columns,
			$prediction_column,
			$server_option,
			$import_type,
			$schedule_details = null,
			$config = array()
		) {
			$config["inputTableId"] = $input_table_id;
			$config["outputTable"] = $output_table;
			$config["outputColumns"] = $output_columns;
			$config["predictionColumn"] = $prediction_column;
			$config["serverOption"] = $server_option;
			$config["importType"] = $import_type;
			$config["scheduleDetails"] = $schedule_details === null ? "none" : $schedule_details;

			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/models/" . $model_id . "/deployments";

			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["deployments"];
		}

		/**
		 * Execute an AutoML analysis deployment.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $deployment_id Id of the deployment.
		 * @param array $config Optional control parameters.
		 * @throws IOException
		 * @throws ServerException
		 * @throws ParseException
		 */
		function deployAutoMLAnalysis($analysis_id, $deployment_id, $config = array()) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/deployments/" . $deployment_id . "/execute";

			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Delete an AutoML analysis deployment.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $deployment_id Id of the deployment.
		 * @param array $config Optional control parameters.
		 * @throws IOException
		 * @throws ServerException
		 * @throws ParseException
		 */
		function deleteAutoMLAnalysisDeployment($analysis_id, $deployment_id, $config = array()) {
			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/deployments/" . $deployment_id;

			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Generate predictions using a trained AutoML model.
		 *
		 * @param string $analysis_id Id of the AutoML analysis.
		 * @param string $model_id Id of the AutoML model.
		 * @param array $features Feature-value mapping.
		 * @param array $config Optional control parameters.
		 * @throws IOException
		 * @throws ServerException
		 * @throws ParseException
		 * @return array Prediction result.
		 */
		function autoMLAnalysisPrediction($analysis_id, $model_id, $features, $config = array()) {
			$config["features"] = $features;

			$endpoint = "/restapi/v2/automl/workspaces/" . $this->workspace_id .
						"/analysis/" . $analysis_id .
						"/models/" . $model_id . "/whatif";

			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}



		/**
	     * Returns list of all tags for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Tags list.
	     */
		function getTags() {
			$endpoint = $this->workspace_end_point . "/tags";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["tags"];
		}
		/**
	     * Create a tag in the specified workspace.
	     * @param string $tag_name Name of the tag to be created.
	     * @param string $color_code Color of the tag in HEX color code.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return string Created tag id.
	     */
		function createTag($tag_name, $color_code, $config = array()) {
			$endpoint = $this->workspace_end_point . "/tags";
			$config["name"] = $tag_name;
			$config["colorCode"] = $color_code;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["tagId"];
		}
		/**
	     * Update details of the specified tag in the workspace.
	     * @param string $tag_id Id of the tag.
	     * @param array() $config Contains the control parameters.
	     */
		function updateTag($tag_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/tags/" . $tag_id;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Delete the specified tag from the workspace.
	     * @param string $tag_id Id of the tag.
	     */
		function deleteTag($tag_id) {
			$endpoint = $this->workspace_end_point . "/tags/" . $tag_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}
		/**
	     * Adds the specified tag to multiple views in the workspace.
	     * @param string $tag_id Id of the tag.
	     * @param array() $view_ids View ids to be associated with the tag.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function addTagToViews($tag_id, $view_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/tags/" . $tag_id . "/views";
			$config["viewIds"] = $view_ids;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Removes the specified tag from multiple views in the workspace.
	     * @param string $tag_id Id of the tag.
	     * @param array() $view_ids View ids to be dissociated. Not required when dissociate_all is true.
	     * @param boolean $dissociate_all To dissociate the tag from all associated views.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function removeTagFromViews($tag_id, $view_ids = NULL, $dissociate_all = false, $config = array()) {
			$endpoint = $this->workspace_end_point . "/tags/" . $tag_id . "/views";
			if ($dissociate_all) {
				$config["dissociateAll"] = true;
			} else {
				$config["viewIds"] = $view_ids;
			}
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Returns the list of views associated with the specified tag.
	     * @param string $tag_id Id of the tag.
	     * @return array() Tagged views list.
	     */
		function getTaggedViews($tag_id) {
			$endpoint = $this->workspace_end_point . "/tags/" . $tag_id . "/views";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Returns list of workspaces linked to the specified master workspace.
	     * @return array() Linked workspaces list.
	     */
		function getLinkedWorkspaces() {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["linkedWorkspaces"];
		}
		/**
	     * Returns list of organizations and workspaces that can be linked to the specified master workspace.
	     * @return array() Organizations with their linkable workspaces.
	     */
		function getLinkableWorkspaces() {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces/linkable";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["orgs"];
		}
		/**
	     * Returns the linking compatibility details for the specified client workspaces.
	     * @param array() $clients Contains the client workspaces to be verified for linking compatibility.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Client workspace compatibility details.
	     */
		function getWorkspaceLinkingCompatibility($clients, $config = array()) {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces/compatibility";
			$config["clients"] = $clients;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["clients"];
		}
		/**
	     * Link the specified client workspaces to the master workspace.
	     * @param array() $clients Contains the client workspaces to be linked with the master workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function linkWorkspaces($clients, $config = array()) {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces";
			$config["clients"] = $clients;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Unlink the client workspaces from the specified master workspace.
	     * @param string $scope Scope of the unlink operation.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function unlinkWorkspaces($scope, $config = array()) {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces";
			$config["scope"] = $scope;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Sync the metadata of the master workspace to its linked client workspaces.
	     * @param string $scope Scope of the sync operation.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function syncLinkedWorkspaces($scope, $config = array()) {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces/sync";
			$config["scope"] = $scope;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Returns the sync details of the specified linked workspaces.
	     * @param array() $sandbox_ids Ids of the linked workspaces for which the sync details are fetched.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Linked workspace sync details.
	     */
		function getLinkedWorkspaceSyncDetails($sandbox_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/linkedworkspaces/sync";
			$config["sandboxIds"] = $sandbox_ids;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["workspaces"];
		}
		/**
	     * Returns the backup configuration and the list of backups available for the specified workspace.
	     * @return array() Workspace backup details.
	     */
		function getWorkspaceBackups() {
			$endpoint = $this->workspace_end_point . "/backups";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Trigger an instant backup for the specified workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Triggered backup details.
	     */
		function backupWorkspaceNow($config = array()) {
			$endpoint = $this->workspace_end_point . "/backups";
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Returns the status of the specified workspace backup.
	     * @param string $backup_id Id of the backup.
	     * @return array() Backup status details.
	     */
		function getWorkspaceBackupStatus($backup_id) {
			$endpoint = $this->workspace_end_point . "/backups/" . $backup_id . "/status";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Download the specified workspace backup.
	     * @param string $backup_id Id of the backup.
	     * @param string $file_path Path of the file where the downloaded backup is to be stored.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function downloadWorkspaceBackup($backup_id, $file_path, $config = array()) {
			$endpoint = $this->workspace_end_point . "/backups/" . $backup_id . "/download";
			$this->ac->sendExportAPIRequest(
				$endpoint,
				$config,
				$this->req_headers,
				$file_path,
				false
			);
		}
		/**
	     * Restore the specified workspace from the given backup.
	     * @param string $backup_id Id of the backup.
	     * @param boolean $confirm_restore Pass true to confirm that the existing workspace data can be overwritten.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Triggered restore details.
	     */
		function restoreWorkspaceFromBackup($backup_id, $confirm_restore, $config = array()) {
			$endpoint = $this->workspace_end_point . "/backups/" . $backup_id . "/restore";
			$config["confirmRestore"] = $confirm_restore;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Returns the status of the specified workspace restore.
	     * @param string $restore_id Id of the restore.
	     * @return array() Restore status details.
	     */
		function getWorkspaceRestoreStatus($restore_id) {
			$endpoint = $this->workspace_end_point . "/restores/" . $restore_id . "/status";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Create a dashboard in the specified workspace.
	     * @param string $display_name Name of the dashboard.
	     * @param string $layout Layout configuration of the dashboard.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return string Created dashboard id.
	     */
		function createDashboard($display_name, $layout, $config = array()) {
			$endpoint = $this->workspace_end_point . "/dashboards";
			$config["displayName"] = $display_name;
			$config["layout"] = $layout;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["dashboardId"];
		}
		/**
	     * Update the specified dashboard in the workspace.
	     * @param string $dashboard_id Id of the dashboard.
	     * @param array() $config Contains the dashboard configurations to be updated.
	     */
		function updateDashboard($dashboard_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/dashboards/" . $dashboard_id;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Returns the metadata of the specified dashboard.
	     * @param string $dashboard_id Id of the dashboard.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Dashboard configuration.
	     */
		function getDashboardMetadata($dashboard_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/dashboards/" . $dashboard_id . "/metadata";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["dashboardConfig"];
		}
		/**
	     * Returns the metadata of the specified report.
	     * @param string $view_id Id of the report.
	     * @return array() Report configuration.
	     */
		function getReportMetadata($view_id) {
			$endpoint = $this->workspace_end_point . "/reports/" . $view_id . "/metadata";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["reportConfig"];
		}
		/**
	     * Returns list of data alerts available in the specified workspace.
	     * @return array() Data alerts list.
	     */
		function getAlertsInWorkspace() {
			$endpoint = $this->workspace_end_point . "/alerts";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["alerts"];
		}
		/**
	     * Returns the configuration of the specified data alert.
	     * @param string $alert_id Id of the data alert.
	     * @return array() Data alert configuration.
	     */
		function getAlertConfiguration($alert_id) {
			$endpoint = $this->workspace_end_point . "/alerts/" . $alert_id;
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Update the specified data alert in the workspace.
	     * @param string $alert_id Id of the data alert.
	     * @param string $alert_name Name of the data alert.
	     * @param array() $schedule_details Contains the schedule configurations of the data alert.
	     * @param array() $rules Contains the rules to be evaluated by the data alert.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function updateAlert($alert_id, $alert_name, $schedule_details, $rules, $config = array()) {
			$endpoint = $this->workspace_end_point . "/alerts/" . $alert_id;
			$config["alertName"] = $alert_name;
			$config["scheduleDetails"] = $schedule_details;
			$config["rules"] = $rules;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Delete the specified data alerts from the workspace.
	     * @param array() $alert_ids Ids of the data alerts to be deleted.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function deleteAlerts($alert_ids, $config = array()) {
			$endpoint = $this->workspace_end_point . "/alerts";
			$config["alertIds"] = $alert_ids;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Enable or disable the specified data alerts in the workspace.
	     * @param array() $alert_ids Ids of the data alerts.
	     * @param boolean $enabled Pass true to enable the data alerts and false to disable them.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function changeAlertStatus($alert_ids, $enabled, $config = array()) {
			$endpoint = $this->workspace_end_point . "/alerts/status";
			$config["alertIds"] = $alert_ids;
			$config["enabled"] = $enabled;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Execute the specified data alert immediately.
	     * @param string $alert_id Id of the data alert.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function runAlert($alert_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/alerts/" . $alert_id . "/execute";
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Returns the execution events of the specified data alert.
	     * @param string $alert_id Id of the data alert.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return array() Data alert events along with the page details.
	     */
		function getAlertEvents($alert_id, $config = array()) {
			$endpoint = $this->workspace_end_point . "/alerts/" . $alert_id . "/events";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Returns the access restriction settings configured for the specified workspace.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Workspace access restriction settings.
	     */
		function getWorkspaceAccessRestrictions() {
			$endpoint = $this->security_controls_end_point . "/access-restrictions";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}
		/**
	     * Update the access restriction settings of the specified workspace.
	     * @param array() $config Contains the access restriction configurations to be updated.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateWorkspaceAccessRestrictions($config = array()) {
			$endpoint = $this->security_controls_end_point . "/access-restrictions";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

	}
	class ViewAPI extends AnalyticsClient
	{
		private $ac;
		private $view_end_point;
		private $req_headers = array();

		/**
  			* Creates a new ViewAPI instance.
  			* @param AnalyticsClient $ac AnalyticsClient instance.
  			* @param string $org_id The ID of the organization.
  			* @param string $workspace_id The ID of the workspace.
  			* @param string $view_id The ID of the view.
  		*/
		function __construct($ac, $org_id, $workspace_id, $view_id) {
			$this->ac = $ac;
			$this->view_end_point = "/restapi/v2/workspaces/" . $workspace_id . "/views/" . $view_id;
			$this->req_headers[] = "ZANALYTICS-ORGID: " . $org_id;
		}

		/**
	     * Add a single row in the specified table.
	     * @param array() $column_values Contains the values for the row. The column names are the key.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Column Names and Added Row Values.
	     */
		function addRow($column_values, $config = array()) {
			$endpoint = $this->view_end_point . "/rows";
			$config["columns"] = $column_values;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Update rows in the specified table.
	     * @param array() $column_values Contains the values for the row. The column names are the key.
	     * @param array() $criteria The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Updated Columns List and Updated Rows Count.
	     */
		function updateRow($column_values, $criteria, $config = array()) {
			$endpoint = $this->view_end_point . "/rows";
			$config["columns"] = $column_values;
			if ($criteria != NULL) {
				$config["criteria"] = $criteria;
			}
			$response = $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Delete rows in the specified table.
	     * @param array() $criteria The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return int Deleted rows count.
	     */
		function deleteRow($criteria, $config = array()) {
			$endpoint = $this->view_end_point . "/rows";
			if ($criteria != NULL) {
				$config["criteria"] = $criteria;
			}
			$response = $this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
			return $response["data"]["deletedRows"];
		}

		/**
	     * Rename a specified view in the workspace.
	     * @param string $view_name New name of the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function rename($view_name, $config = array()) {
			$config["viewName"] = $view_name;
			$this->ac->sendAPIRequest("PUT", $this->view_end_point, $config, $this->req_headers);
		}

		/**
	     * Delete a specified view in the workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function delete($config = array()) {
			$this->ac->sendAPIRequest("DELETE", $this->view_end_point, $config, $this->req_headers);
		}

		/**
	     * Copy a specified view within the workspace.
	     * @param string $new_view_name The name of the new view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created view id.
	     */
		function saveAs($new_view_name, $config = array()) {
			$endpoint = $this->view_end_point . "/saveas";
			$config["viewName"] = $new_view_name;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["viewId"];
		}

		/**
	     * Copy the specified formulas from one table to another within the workspace or across workspaces.
	     * @param string $formulaNames  The name of the formula columns to be copied.
	     * @param string $dest_workspace_id The id of the destination workspace.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @param string $dest_org_id Id of the organization where the destination workspace is present. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function copyFormulas($formulaNames, $dest_workspace_id, $config = array(), $dest_org_id=NULL) {
			$endpoint = $this->view_end_point . "/formulas/copy";
			$config["formulaColumnNames"] = $formulaNames;
			$config["destWorkspaceId"] = $dest_workspace_id;
			$request_headers = $this->req_headers;
			if ($dest_org_id != NULL) {
				$request_headers[]  = "ZANALYTICS-DEST-ORGID: " . $dest_org_id;
			}
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $request_headers);
		}

		/**
	     * Adds a specified view as favorite.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function addFavorite() {
			$endpoint = $this->view_end_point . "/favorite";
			$this->ac->sendAPIRequest("POST", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Remove a specified view from favorite.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeFavorite() {
			$endpoint = $this->view_end_point . "/favorite";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Create reports for the specified table based on the reference table.
	     * @param string $ref_view_id  The ID of the reference view.
	     * @param string $folder_id The folder id where the views to be saved.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function createSimilarViews($ref_view_id, $folder_id, $config = array()) {
			$endpoint = $this->view_end_point . "/similarviews";
			$config["referenceViewId"] = $ref_view_id;
			$config["folderId"] = $folder_id;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Auto generate reports for the specified table.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function autoAnalyse($config = array()) {
			$endpoint = $this->view_end_point . "/autoanalyse";
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns permissions for the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Permission details.
	     */
		function getMyPermissions() {
			$endpoint = $this->view_end_point . "/share/userpermissions";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["permissions"];
		}

		/**
	     * Returns the URL to access the specified view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string View URL.
	     */
		function getViewURL($config = array()) {
			$endpoint = $this->view_end_point . "/publish";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["viewUrl"];
		}

		/**
	     * Returns embed URL to access the specified view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Embed URL.
	     */
		function getEmbedURL($config = array()) {
			$endpoint = $this->view_end_point . "/publish/embed";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["embedUrl"];
		}

		/**
	     * Returns private URL to access the specified view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Private URL.
	     */
		function getPrivateURL($config = array()) {
			$endpoint = $this->view_end_point . "/publish/privatelink";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["privateUrl"];
		}

		/**
	     * Create a private URL for the specified view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string private URL.
	     */
		function createPrivateURL($config = array()) {
			$endpoint = $this->view_end_point . "/publish/privatelink";
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["privateUrl"];
		}

		/**
	     * Remove private link access for the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removePrivateAccess() {
			$endpoint = $this->view_end_point . "/publish/privatelink";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Make the specified view publically accessible.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string public URL.
	     */
		function makeViewPublic($config = array()) {
			$endpoint = $this->view_end_point . "/publish/public";
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["publicUrl"];
		}

		/**
	     * Remove public access for the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removePublicAccess() {
			$endpoint = $this->view_end_point . "/publish/public";
			$this->ac->sendAPIRequest("DELETE", $endpoint, NULL, $this->req_headers);
		}

		/**
	     * Returns publish configurations for the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Publish details.
	     */
		function getPublishConfigurations() {
			$endpoint = $this->view_end_point . "/publish/config";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Update publish configurations for the specified view.
	     * @param array() $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updatePublishConfigurations($config = array()) {
			$endpoint = $this->view_end_point . "/publish/config";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Add a column in the specified table.
	     * @param string $column_name The name of the column.
	     * @param string $data_type The data-type of the column.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created column id.
	     */
		function addColumn($column_name, $data_type, $config = array()) {
			$endpoint = $this->view_end_point . "/columns";
			$config["columnName"] = $column_name;
			$config["dataType"] = $data_type;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["columnId"];
		}

        /**
	     * Rename a specified column in the table.
	     * @param string $column_id Id of the column.
	     * @param string $column_name New name for the column.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function renameColumn($column_id, $column_name) {
            $config = array();
            $config["columnName"] = $column_name;
            $endpoint = $this->view_end_point . "/columns/" . $column_id;
            $this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Delete a specified column in the table.
	     * @param string $column_id Id of the column.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteColumn($column_id, $config = array()) {
        	$endpoint = $this->view_end_point . "/columns/" . $column_id;
            $this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Add a lookup in the specified child table.
	     * @param string $column_id Id of the column.
	     * @param string $ref_view_id The id of the table contains the parent column.
	     * @param string $ref_column_id The id of the parent column.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function createLookup($column_id, $ref_view_id, $ref_column_id, $config = array()) {
            $endpoint = $this->view_end_point . "/columns/" . $column_id . "/lookup";
            $config["referenceViewId"] = $ref_view_id;
            $config["referenceColumnId"] = $ref_column_id;
            $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Remove the lookup for the specified column in the table.
	     * @param string $column_id Id of the column.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function removeLookup($column_id, $config = array()) {
            $endpoint = $this->view_end_point . "/columns/" . $column_id . "/lookup";
            $this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
        }

        /**
	     * Auto generate reports for the specified column.
	     * @param string $column_id Id of the column.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function autoAnalyseColumn($column_id, $config = array()) {
            $endpoint = $this->view_end_point . "/columns/" . $column_id . "/autoanalyse";
            $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
        }

		/**
	     * Hide the specified columns in the table.
	     * @param array() $column_ids Ids of the columns to be hidden.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function hideColumns($column_ids) {
			$endpoint = $this->view_end_point . "/columns/hide";
			$config = array();
			$config["columnIds"] = $column_ids;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Show the specified hidden columns in the table.
	     * @param array() $column_ids Ids of the columns to be hidden.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function showColumns($column_ids) {
			$endpoint = $this->view_end_point . "/columns/show";
			$config = array();
			$config["columnIds"] = $column_ids;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Sync data from available datasource for the specified view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function refetchData($config = array()) {
			$endpoint = $this->view_end_point . "/sync";
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns last import details of the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Last data import details.
	     */
		function getLastImportDetails() {
			$endpoint = $this->view_end_point . "/importdetails";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Returns list of all formula columns for the specified table.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Formula column list.
	     */
		function getFormulaColumns() {
			$endpoint = $this->view_end_point . "/formulacolumns";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["formulaColumns"];
		}

		/**
	     * Add a formula column in the specified table.
	     * @param string $formula_name Name of the formula column to be created.
	     * @param string $expression Formula expression.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created column id.
	     */
		function addFormulaColumn($formula_name, $expression, $config = array()) {
			$endpoint = $this->view_end_point . "/formulacolumns";
			$config["formulaName"] = $formula_name;
			$config["expression"] = $expression;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["formulaId"];
		}

		/**
	     * Edit the specified formula column.
	     * @param string $formula_id Id of the formula column to be updated.
	     * @param string $expression Formula expression.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function editFormulaColumn($formula_id, $expression, $config = array()) {
			$endpoint = $this->view_end_point . "/formulacolumns/" . $formula_id;
			$config["expression"] = $expression;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Delete the specified formula column.
	     * @param string $formula_id Id of the formula column to be deleted.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteFormulaColumn($formula_id, $config = array()) {
			$endpoint = $this->view_end_point . "/formulacolumns/" . $formula_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of all aggregate formulas for the specified table.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Aggregate formula list.
	     */
		function getAggregateFormulas() {
			$endpoint = $this->view_end_point . "/aggregateformulas";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["aggregateFormulas"];
		}

		/**
	     * Add an aggregate formula in the specified table.
	     * @param string $formula_name Name of the aggregate formula to be created.
	     * @param string $expression Formula expression.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Created column id.
	     */
		function addAggregateFormula($formula_name, $expression, $config = array()) {
			$endpoint = $this->view_end_point . "/aggregateformulas";
			$config["formulaName"] = $formula_name;
			$config["expression"] = $expression;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["formulaId"];
		}

		/**
	     * Edit the specified aggregate formula.
	     * @param string $formula_id Id of the aggregate formula to be updated.
	     * @param string $expression Formula expression.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function editAggregateFormula($formula_id, $expression, $config = array()) {
			$endpoint = $this->view_end_point . "/aggregateformulas/" . $formula_id;
			$config["expression"] = $expression;
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Delete the specified aggregate formula.
	     * @param string $formula_id Id of the aggregate formula to be deleted.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function deleteAggregateFormula($formula_id, $config = array()) {
			$endpoint = $this->view_end_point . "/aggregateformulas/" . $formula_id;
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of dependents views for the specified view.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Dependent view list.
	     */
		function getViewDependents() {
			$endpoint = $this->view_end_point . "/dependents";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["views"];
		}

		/**
	     * Returns dependent details for the specified column.
	     * @param string $formula_id Id of the formula column to be updated.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Dependent details.
	     */
		function getColumnDependents($column_id) {
			$endpoint = $this->view_end_point . "/columns/" . $column_id . "/dependents";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Update the existing sharing configuration for the specified view.
	     * @param $config Contains the control parameters.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function updateSharedDetails($config = array()) {
			$endpoint = $this->view_end_point . "/share";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Retrieves metadata information for the current table.
		 * Returns metadata details such as available columns and their attributes.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server received the request but failed to process it.
		 * @throws ParseException If the server response could not be parsed.
		 *
		 * @return array Table metadata details.
		 */
		function getTableMetadata() {
			$endpoint = $this->view_end_point . "/metadata";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
		 * Updates the column order of the current table.
		 *
		 * @param array $column_ids List of column IDs in the desired order.
		 * @param array $config Optional configuration parameters.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server received the request but failed to process it.
		 * @throws ParseException If the server response could not be parsed.
		 */
		function reorderColumns($column_ids, $config = array()) {
			$config["columns"] = $column_ids;
			$endpoint = $this->view_end_point . "/columns/reorder";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}

		/**
		 * Sorts the data in the table based on specified columns.
		 *
		 * @param array|null $columns List of column IDs to sort by.
		 * @param int|null $sort_order Sorting order (1 → Ascending, 2 → Descending).
		 * @param boolean $reset_sort If true, resets existing sort configuration.
		 * @param array $config Optional configuration parameters.
		 *
		 * @throws IOException If any communication related error(s) occur.
		 * @throws ServerException If the server received the request but failed to process it.
		 * @throws ParseException If the server response could not be parsed.
		 */
		function sortDataByColumns($columns = NULL, $sort_order = NULL, $reset_sort = false, $config = array()) {

			if ($reset_sort) {
				$config["resetSort"] = "true";
			} else {
				$config["columns"]   = $columns;
				$config["sortOrder"] = $sort_order;
			}

			$endpoint = $this->view_end_point . "/data/sort";
			$this->ac->sendAPIRequest("PUT", $endpoint, $config, $this->req_headers);
		}		

		/**
	     * Returns the list of tags associated with the specified view.
	     * @return array() Tags list.
	     */
		function getViewTags() {
			$endpoint = $this->view_end_point . "/tags";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["tags"];
		}
		/**
	     * Adds multiple tags to the specified view.
	     * @param array() $tag_ids Tag ids to be associated with the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function addTagsToView($tag_ids, $config = array()) {
			$endpoint = $this->view_end_point . "/tags";
			$config["tagIds"] = $tag_ids;
			$this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
		}
		/**
	     * Removes multiple tags from the specified view.
	     * @param array() $tag_ids Tag ids to be dissociated. Not required when dissociate_all is true.
	     * @param boolean $dissociate_all To dissociate all the associated tags from the view.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     */
		function removeTagsFromView($tag_ids = NULL, $dissociate_all = false, $config = array()) {
			$endpoint = $this->view_end_point . "/tags";
			if ($dissociate_all) {
				$config["dissociateAll"] = true;
			} else {
				$config["tagIds"] = $tag_ids;
			}
			$this->ac->sendAPIRequest("DELETE", $endpoint, $config, $this->req_headers);
		}

		/**
	     * Returns list of data alerts configured for the specified view.
	     * @return array() Data alerts list.
	     */
		function getAlertsInView() {
			$endpoint = $this->view_end_point . "/alerts";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"]["alerts"];
		}
		/**
	     * Create a data alert for the specified view.
	     * @param string $alert_name Name of the data alert.
	     * @param array() $schedule_details Contains the schedule configurations of the data alert.
	     * @param array() $rules Contains the rules to be evaluated by the data alert.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @return string Created data alert id.
	     */
		function createAlert($alert_name, $schedule_details, $rules, $config = array()) {
			$endpoint = $this->view_end_point . "/alerts";
			$config["alertName"] = $alert_name;
			$config["scheduleDetails"] = $schedule_details;
			$config["rules"] = $rules;
			$response = $this->ac->sendAPIRequest("POST", $endpoint, $config, $this->req_headers);
			return $response["data"]["alertId"];
		}
		/**
	     * Returns the view metadata that can be used while configuring a data alert for the specified view.
	     * @return array() View metadata for data alert configuration.
	     */
		function getViewMetadataForAlert() {
			$endpoint = $this->view_end_point . "/alerts/metadata";
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

	}
	class BulkAPI extends AnalyticsClient
	{
		private $ac;
		private $data_end_point;
		private $bulk_data_end_point;
		private $req_headers = array();

		/**
  			* Creates a new BulkAPI instance.
  			* @param AnalyticsClient $ac AnalyticsClient instance.
  			* @param string $org_id The ID of the organization.
  			* @param string $workspace_id The ID of the workspace.
  		*/
		function __construct($ac, $org_id, $workspace_id) {
			$this->ac = $ac;
			$this->data_end_point = "/restapi/v2/workspaces/" . $workspace_id;
			$this->bulk_data_end_point = "/restapi/v2/bulk/workspaces/" . $workspace_id;
			$this->req_headers[] = "ZANALYTICS-ORGID: " . $org_id;
		}

		/**
	     * Create a new table and import the data contained in the mentioned file into the created table.
	     * @param string $table_name Name of the new table to be created.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Import result.
	     */
		function importDataInNewTable($table_name, $file_type, $auto_identify, $file_path, $config = array()) {
			$endpoint = $this->data_end_point . "/data";
			$config["tableName"] = $table_name;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
			$file_data = explode('/', $file_path);
			$filename = end($file_data);
            $post_fields['FILE'] = new CURLFile($file_path, 'json/csv', $filename);
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Import the data contained in the mentioned file into the table.
	     * @param string $view_id Id of the view where the data to be imported.
	     * @param string $import_type The type of import. Can be one of - append, truncateadd, updateadd.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Import result.
	     */
		function importData($view_id, $import_type, $file_type, $auto_identify, $file_path, $config = array()) {
			$endpoint = $this->data_end_point . "/views/" . $view_id . "/data";
			$config["importType"] = $import_type;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
			$file_data = explode('/', $file_path);
			$filename = end($file_data);
            $post_fields['FILE'] = new CURLFile($file_path, 'json/csv', $filename);
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Create a new table and import the raw data provided into the created table.
	     * @param string $table_name Name of the new table to be created.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $data Raw data to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Import result.
	     */
		function importRawDataInNewTable($table_name, $file_type, $auto_identify, $data, $config = array()) {
			$endpoint = $this->data_end_point . "/data";
			$config["tableName"] = $table_name;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
            $post_fields['DATA'] = $data;
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Import the data contained in the mentioned file into the table.
	     * @param string $view_id Id of the view where the data to be imported.
	     * @param string $import_type The type of import. Can be one of - append, truncateadd, updateadd.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $data Raw data to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Import result.
	     */
		function importRawData($view_id, $import_type, $file_type, $auto_identify, $data, $config = array()) {
			$endpoint = $this->data_end_point . "/views/" . $view_id . "/data";
			$config["importType"] = $import_type;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
            $post_fields['DATA'] = $data;
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Asynchronously create a new table and import the data contained in the mentioned file into the created table.
	     * @param string $table_name Name of the new table to be created.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Import job id.
	     */
		function importBulkDataInNewTable($table_name, $file_type, $auto_identify, $file_path, $config = array()) {
			$endpoint = $this->bulk_data_end_point . "/data";
			$config["tableName"] = $table_name;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
			$file_data = explode('/', $file_path);
			$filename = end($file_data);
            $post_fields['FILE'] = new CURLFile($file_path, 'json/csv', $filename);
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"]["jobId"];
		}

		/**
	     * Asynchronously import the data contained in the mentioned file into the table.
	     * @param string $view_id Id of the view where the data to be imported.
	     * @param string $import_type The type of import. Can be one of - append, truncateadd, updateadd.
	     * @param string $file_type Type of the file to be imported.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Import job id.
	     */
		function importBulkData($view_id, $import_type, $file_type, $auto_identify, $file_path, $config = array()) {
			$endpoint = $this->bulk_data_end_point . "/views/" . $view_id . "/data";
			$config["importType"] = $import_type;
			$config["fileType"] = $file_type;
			$config["autoIdentify"] = $auto_identify;

			$post_fields = array();
			$post_fields["CONFIG"] = json_encode($config);
			$file_data = explode('/', $file_path);
			$filename = end($file_data);
            $post_fields['FILE'] = new CURLFile($file_path, 'json/csv', $filename);
			
			$response = $this->ac->sendImportAPIRequest($endpoint, $post_fields, $this->req_headers);
			return $response["data"]["jobId"];
		}
                
                /**
	     * Asynchronously create a new table and import the data contained in the mentioned file into the created table.
	     * @param string $table_name Name of the new table to be created.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
         * @param int $batch_size Number of lines per batch.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Import job id.
	     */
		function importBulkDataInNewTableAsBatches($table_name, $auto_identify, $file_path, $batch_size, $config = array(), $tool_config = array()) {
			$endpoint = $this->bulk_data_end_point . "/data" . "/batch";
			$config["tableName"] = $table_name;
			$config["autoIdentify"] = $auto_identify;
                        $response = $this->ac->sendBatchImportAPIRequest($endpoint, $file_path, $batch_size, $config, $this->req_headers);
			return $response["data"]["jobId"];
		}

	     /**
	     * Asynchronously import the data contained in the mentioned file into the table.
	     * @param string $view_id Id of the view where the data to be imported.
	     * @param string $import_type The type of import. Can be one of - append, truncateadd, updateadd.
	     * @param string $auto_identify Used to specify whether to auto identify the CSV format.
	     * @param string $file_path Path of the file to be imported.
             * @param int $batch_size Number of lines per batch.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Import job id.
	     */
		function importBulkDataAsBatches($view_id, $import_type, $auto_identify, $file_path, $batch_size, $config = array()) {
			$endpoint = $this->bulk_data_end_point . "/views/" . $view_id . "/data" . "/batch";
			$config["importType"] = $import_type;
			$config["autoIdentify"] = $auto_identify;
			$response = $this->ac->sendBatchImportAPIRequest($endpoint, $file_path, $batch_size, $config, $this->req_headers);
			return $response["data"]["jobId"];
		}

		/**
	     * Returns the details of the import job.
	     * @param string $job_id Id of the job.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Import job details.
	     */
		function getImportJobDetails($job_id) {
			$endpoint = $this->bulk_data_end_point . "/importjobs/" . $job_id;
			
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Export the mentioned table (or) view data.
	     * @param string $view_id Id of the view to be exported.
	     * @param string $response_format The format in which the data is to be exported.
	     * @param string $file_path Path of the file where the data exported to be stored.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function exportData($view_id, $response_format, $file_path, $config = array()) {
			$endpoint = $this->data_end_point . "/views/" . $view_id . "/data";
			$config["responseFormat"] = $response_format;
		
			$this->ac->sendExportAPIRequest(
				$endpoint,
				$config,
				$this->req_headers,
				$file_path,
				false
			);
		}

		/**
		 * Export the specified view data as a stream.
		 *
		 * @param string $view_id Id of the view to be exported.
		 * @param string $response_format Format in which the data is to be exported.
		 * @param array  $config Optional configuration parameters.
		 *
		 * @return resource PHP stream object containing the exported data.
		 *
		 * @throws ServerException If the server received but failed to process the request.
		 * @throws ParseException  If the response could not be parsed.
		 */
		function exportDataStream($view_id, $response_format, $config = array()) {

			$endpoint = $this->data_end_point . "/views/" . $view_id . "/data";
			$config["responseFormat"] = $response_format;

			return $this->ac->sendExportAPIRequest(
				$endpoint,
				$config,
				$this->req_headers,
				null,
				true
			);
		}

		

		/**
	     * Initiate asynchronous export for the mentioned table (or) view data.
	     * @param string $view_id Id of the view to be exported.
	     * @param string $response_format The format in which the data is to be exported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Export job id.
	     */
		function initiateBulkExport($view_id, $response_format, $config = array()) {
			$endpoint = $this->bulk_data_end_point . "/views/" . $view_id . "/data";
			$config["responseFormat"] = $response_format;
			
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["jobId"];
		}

		/**
	     * Initiate asynchronous export with the given SQL Query.
	     * @param string $sql_query The SQL Query whose output is exported.
	     * @param string $response_format The format in which the data is to be exported.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return string Export job id.
	     */
		function initiateBulkExportUsingSQL($sql_query, $response_format, $config = array()) {
			$endpoint = $this->bulk_data_end_point . "/data";
			$config["sqlQuery"] = $sql_query;
			$config["responseFormat"] = $response_format;
			
			$response = $this->ac->sendAPIRequest("GET", $endpoint, $config, $this->req_headers);
			return $response["data"]["jobId"];
		}

		/**
	     * Returns the details of the export job.
	     * @param string $job_id Id of the job.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     * @return array() Export job details.
	     */
		function getExportJobDetails($job_id) {
			$endpoint = $this->bulk_data_end_point . "/exportjobs/" . $job_id;
	
			$response = $this->ac->sendAPIRequest("GET", $endpoint, NULL, $this->req_headers);
			return $response["data"];
		}

		/**
	     * Download the exported data for the mentioned job id.
	     * @param string $job_id Id of the job.
	     * @param string $file_path Path of the file where the data exported to be stored.
	     * @param array() $config Contains any additional control parameters. Can be null.
	     * @throws IOException If any communication related error(s) like request time out occurs when trying to contact the service.
	     * @throws ServerException If the server has received the request but did not process the request due to some error.
	     * @throws ParseException If the server has responded but client was not able to parse the response.
	     */
		function exportBulkData($job_id, $file_path) {
			$endpoint = $this->bulk_data_end_point . "/exportjobs/" . $job_id . "/data";
		
			$this->ac->sendExportAPIRequest(
				$endpoint,
				null,
				$this->req_headers,
				$file_path,
				false
			);
		}

		/**
		 * Download exported bulk data for the specified job id as a stream.
		 *
		 * @param string $job_id Id of the export job.
		 *
		 * @return resource PHP stream object containing the exported data.
		 *
		 * @throws ServerException If the server received but failed to process the request.
		 * @throws ParseException  If the response could not be parsed.
		 */
		function exportBulkDataStream($job_id) {

			$endpoint = $this->bulk_data_end_point . "/exportjobs/" . $job_id . "/data";

			return $this->ac->sendExportAPIRequest(
				$endpoint,
				null,
				$this->req_headers,
				null,
				true
			);
		}
	}


	/**
		*ServerException is thrown if the report server has received the request but did not process the request due to some error. 
	*/
	class ServerException extends Exception
	{
		/**
			* @var int The error code sent by the server.
		*/
		private $error_code;
		/**
			* @var string The error message sent by the server.
		*/
		private $error_message;

		/**
			* @internal Creates a new Server_Exception instance.
		*/
		function __construct($resp_content, $is_iam_error){
			$json_response = json_decode($resp_content, TRUE);
			if(json_last_error() != JSON_ERROR_NONE) {
				$resp_content = stripslashes($resp_content);
				$json_response = json_decode($resp_content, TRUE);
			}
			if(json_last_error()){
				throw new ParseException("API response is not proper. Invalid JSON data. Response - " . $resp_content);
			}

			if($is_iam_error){
				$this->error_message = "Exception while generating oauth token. Response - " . $resp_content;
				$this->error_code = 0;
			}
			else{
				$this->error_message = $json_response["data"]["errorMessage"];
				$this->error_code = $json_response["data"]["errorCode"];
			}
			
		}

		/**
			* Get the error message sent by the server.
			* @return string The error message.
		*/
		function getErrorMessage() {
			return $this->error_message;
		}

		/**
			* Get the error code sent by the server.
			* @return int The error code.
		*/
		function getErrorCode() {
			return $this->error_code;
		}
	}

	/**
		* ParseException is thrown if the server has responded but client was not able to parse the response. Possible reasons could be version mismatch.The client might have to be updated to a newer version.
	*/
	class ParseException extends Exception
	{
		/**
			* @var string The error message sent by the server.
		*/
		private $error_message;

		/**
			* @internal Creates a new Parse_Exception instance.
		*/
		function __construct($error_message){
			$this->error_message = $error_message;
		}

		/**
			* Get the complete response content as sent by the server.
			* @return string The complete response content.
		*/
		function getErrorMessage(){
			return $this->error_message;
		}
	}

	/**
		*IOException is thrown when an input or output operation is failed or interpreted.
	*/

	class IOException extends Exception
	{
		/**
			* @var string The error message sent by the server.
		*/
		private $error_message;

		/**
			* @internal Creates a new IO_Exception instance.
		*/
		function __construct($error_message){
			$this->error_message = $error_message;
		}

		/**
			* Get the complete response content as sent by the server.
			* @return string The complete response content.
		*/
		function getErrorMessage(){
			return $this->error_message;
		}
	}

