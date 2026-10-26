#$Id$
require 'uri'
require 'json'
require 'net/http'
require 'digest/sha1'
require 'openssl'
require 'base64'
require 'fileutils'
require 'time'
require 'erb'
include ERB::Util
require 'tempfile'

class AnalyticsClient
  CLIENT_VERSION = "2.9.0"
  COMMON_ENCODE_CHAR = "UTF-8"
  DC_URLS = {
    "US"  => { "accounts" => "https://accounts.zoho.com",    "analytics" => "https://analyticsapi.zoho.com" },
    "EU"  => { "accounts" => "https://accounts.zoho.eu",     "analytics" => "https://analyticsapi.zoho.eu" },
    "IN"  => { "accounts" => "https://accounts.zoho.in",     "analytics" => "https://analyticsapi.zoho.in" },
    "AU"  => { "accounts" => "https://accounts.zoho.com.au", "analytics" => "https://analyticsapi.zoho.com.au" },
    "CN"  => { "accounts" => "https://accounts.zoho.com.cn", "analytics" => "https://analyticsapi.zoho.com.cn" },
    "CA"  => { "accounts" => "https://accounts.zohocloud.ca", "analytics" => "https://analyticsapi.zohocloud.ca" },
    "JP"  => { "accounts" => "https://accounts.zoho.jp",     "analytics" => "https://analyticsapi.zoho.jp" },
    "SA"  => { "accounts" => "https://accounts.zoho.sa",     "analytics" => "https://analyticsapi.zoho.sa" },
    "UAE" => { "accounts" => "https://accounts.zoho.ae",     "analytics" => "https://analyticsapi.zoho.ae" }
  }

  def self.new
    Builder.new
  end

  # ========== BUILDER
  #
  # Builder class for configuring and creating an AnalyticsClient instance.
  # Enables fluent method chaining for setting client configuration options
  # such as data center, OAuth credentials, proxy settings, token store path,
  # and direct access token. Enforces mandatory data center presence on build.
  #
  class Builder
    # Initializes a new builder with default (nil) values
    def initialize
      @data_center = nil           # Zoho Analytics data center code (e.g., "US", "EU")
      @oauth = nil                 # OAuth credentials hash (clientId, clientSecret, refreshToken)
      @proxy_details = nil         # Optional proxy configuration hash (host, port, username, password)
      @token_store_path = nil      # Optional filesystem path for encrypted token storage
      @access_token = nil          # Optional direct access token override
      @use_direct_access_token = false  # Flag indicating usage of direct access token (bypass OAuth)
    end

    # Sets the Zoho Analytics data center for this client.
    #
    # @param dc [String] Data center code, mandatory (e.g., "US", "EU")
    # @return [Builder] Returns self for method chaining
    # @raise [ArgumentError] if dc is nil or empty
    def with_data_center(dc)
      raise ArgumentError, "data_center cannot be empty" if dc.nil? || dc.strip.empty?
      @data_center = dc.strip.upcase
      self
    end

    # Sets the OAuth credentials hash for authentication.
    #
    # @param oauth_hash [Hash] OAuth credentials with keys:
    #   - "clientId"
    #   - "clientSecret"
    #   - "refreshToken"
    # @return [Builder] Returns self for method chaining
    def with_oauth(oauth_hash)
      @oauth = oauth_hash
      self
    end

    # Sets the proxy configuration details.
    #
    # @param proxy_details [Hash] Proxy settings with keys:
    #   - :host, :port, :username, :password
    # @return [Builder] Returns self for method chaining
    def with_proxy(proxy_details)
      @proxy_details = proxy_details
      self
    end

    # Sets the path for encrypted token storage.
    # Raises an error if the directory does not exist.
    #
    # @param path [String] Filesystem directory to store encrypted tokens
    # @return [Builder] Returns self for method chaining
    # @raise [ArgumentError] if the specified directory does not exist
    def with_token_store_path(path)
      unless Dir.exist?(path)
        raise ArgumentError, "Token store directory does not exist: #{path}"
      end
      @token_store_path = path
      self
    end


    # Sets a direct access token on the client, bypassing OAuth.
    # Using this token disables automatic token refresh logic.
    #
    # @param token [String] The direct access token string
    # @return [Builder] Returns self for method chaining
    def with_access_token(token)
      @access_token = token
      @use_direct_access_token = true
      self
    end

    # Builds and returns the configured AnalyticsClient instance.
    # Validates mandatory presence of data center before building.
    #
    # @raise [ArgumentError] if data center is not set or empty
    # @return [AnalyticsClient] Constructed client instance
    def build
      raise ArgumentError, "Data center is mandatory. Use with_data_center(dc) before build." if @data_center.nil? || @data_center.empty?

      client = AnalyticsClient.allocate
      client.send(:setup_from_builder, self)
      client
    end
  end



  # ========== INSTANCE SETUP ==========

  def setup_from_builder(builder)
    @data_center = builder.instance_variable_get(:@data_center)
    @oauth = builder.instance_variable_get(:@oauth) || {}

    if @oauth && !@oauth.empty?
      missing_keys = []
      missing_keys << "clientId" unless @oauth.key?("clientId") && !@oauth["clientId"].to_s.strip.empty?
      missing_keys << "clientSecret" unless @oauth.key?("clientSecret") && !@oauth["clientSecret"].to_s.strip.empty?
      missing_keys << "refreshToken" unless @oauth.key?("refreshToken") && !@oauth["refreshToken"].to_s.strip.empty?

      unless missing_keys.empty?
        raise ArgumentError, "OAuth hash is missing required keys or they are empty: #{missing_keys.join(', ')}"
      end
    end

    @proxy_details = builder.instance_variable_get(:@proxy_details)
    @store_path = builder.instance_variable_get(:@token_store_path)
    @access_token = builder.instance_variable_get(:@access_token)
    @use_direct_access_token = builder.instance_variable_get(:@use_direct_access_token)

    @proxy = !!@proxy_details
    if @proxy
      @proxy_host = @proxy_details[:host]
      @proxy_port = @proxy_details[:port]
      @proxy_user_name = @proxy_details[:username]
      @proxy_password = @proxy_details[:password]
    end

    dc = DC_URLS[@data_center]
    raise ArgumentError, "Invalid dataCenter: #{@data_center}. Valid: #{DC_URLS.keys.join(', ')}" unless dc

    @accounts_server_url = dc["accounts"]
    @analytics_server_url = dc["analytics"]
  end



  # ========== ENCRYPTED TOKEN STORAGE ==========

  def token_file_path
    client_id = @oauth["clientId"].to_s
    client_secret = @oauth["clientSecret"].to_s
    hash = Digest::SHA256.hexdigest(client_id + client_secret)
    FileUtils.mkdir_p(@store_path) unless Dir.exist?(@store_path)
    File.join(@store_path, "za_tokens_#{hash}.dat")
  end


  def derive_file_key
    secret = @oauth["clientId"].to_s + @oauth["clientSecret"].to_s
    salt = OpenSSL::Digest::SHA256.digest(secret)[0..15]
    OpenSSL::PKCS5.pbkdf2_hmac_sha1(secret, salt, 20_000, 32)
  end


  def derive_token_key(refresh_token)
    salt = OpenSSL::Digest::SHA256.digest(refresh_token)[0..15]
    OpenSSL::PKCS5.pbkdf2_hmac_sha1(refresh_token, salt, 20_000, 32)
  end

  def encrypt_token(token, refresh_token)
    cipher = OpenSSL::Cipher.new('AES-256-CBC')
    cipher.encrypt
    key = derive_token_key(refresh_token)
    iv = cipher.random_iv
    cipher.key = key
    cipher.iv = iv
    encrypted = cipher.update(token) + cipher.final
    Base64.strict_encode64(iv + encrypted)
  end

  def decrypt_token(encrypted_token, refresh_token)
    data = Base64.strict_decode64(encrypted_token)
    iv = data[0, 16]
    encrypted = data[16..-1]
    decipher = OpenSSL::Cipher.new('AES-256-CBC')
    decipher.decrypt
    decipher.key = derive_token_key(refresh_token)
    decipher.iv = iv
    decipher.update(encrypted) + decipher.final
  end

  def encrypt_and_write_file(token_map)
    cipher = OpenSSL::Cipher.new('AES-256-CBC')
    cipher.encrypt
    key = derive_file_key
    iv = cipher.random_iv
    cipher.key = key
    cipher.iv = iv
    data = token_map.to_json
    encrypted = cipher.update(data) + cipher.final
    File.open(token_file_path, "wb", perm: 0600) { |f| f.write(iv + encrypted) }
  end

  def decrypt_and_read_file
    raw = File.binread(token_file_path)
    iv = raw[0, 16]
    encrypted = raw[16..-1]
    decipher = OpenSSL::Cipher.new('AES-256-CBC')
    decipher.decrypt
    decipher.key = derive_file_key
    decipher.iv = iv
    decrypted = decipher.update(encrypted) + decipher.final
    JSON.parse(decrypted)
  rescue
    {}
  end

  def key_for_refresh_token(refresh_token)
    key = derive_token_key(refresh_token)
    digest = OpenSSL::HMAC.digest('sha256', key, refresh_token)
    Base64.strict_encode64(digest)
  end

  def save_token_to_store(refresh_token, access_token)
    content = decrypt_and_read_file rescue {}
    key = key_for_refresh_token(refresh_token)
    encrypted_access_token = encrypt_token(access_token, refresh_token)
    content[key] = encrypted_access_token
    encrypt_and_write_file(content)
  end

  def load_token_from_store(refresh_token)
    content = decrypt_and_read_file rescue {}
    key = key_for_refresh_token(refresh_token)
    content[key] ? decrypt_token(content[key], refresh_token) : nil
  end
  

  # ========== TOKEN HANDLING LOGIC ==========

  #  Sets the access token directly on the AnalyticsClient instance, bypassing the need for OAuth token refresh or regeneration.
  def set_access_token(token)
    @access_token = token
    @use_direct_access_token = true
    self
  end


  # Select and ensure access token using direct, cached, or refresh flow
  def ensure_access_token
    return if @access_token && !@access_token.to_s.empty?

    unless @oauth
      raise "OAuth credentials are missing. Provide either an access_token or a refresh_token with client_id and client_secret."
    end

    %w[clientId clientSecret refreshToken].each do |key|
      if @oauth[key].to_s.strip.empty?
        raise "Missing #{key} in OAuth configuration"
      end
    end

    refresh_token = @oauth["refreshToken"]

    if @store_path
      token = load_token_from_store(refresh_token)
      if token && !token.empty?
        @access_token = token
        return
      end
    end

    regenerate_access_token
  end


  # Regenerate access_token from refresh_token, persist in token file encrypted per logic above
  def regenerate_access_token
    unless @oauth
      raise "OAuth credentials are missing. Provide either an access_token or a refresh_token with client_id and client_secret."
    end

    url = "#{@accounts_server_url}/oauth/v2/token"
    uri = URI(url)
    http = create_http_client(uri)
    request = Net::HTTP::Post.new(uri)
    request.set_form_data({
      'refresh_token' => @oauth["refreshToken"],
      'client_id'     => @oauth["clientId"],
      'client_secret' => @oauth["clientSecret"],
      'grant_type'    => 'refresh_token'
    })

    response = http.request(request)

    unless response.is_a?(Net::HTTPSuccess)
      raise "Failed to obtain new Zoho Analytics access token: #{response.code} -- #{response.body}"
    end

    json_response = JSON.parse(response.body)
    access_token = json_response["access_token"]
    unless access_token
      raise "Invalid token response: #{response.body}"
    end

    @access_token = access_token
    save_token_to_store(@oauth["refreshToken"], access_token) if @store_path
    cleanup_obsolete_token_files
    @access_token
  end


  def cleanup_obsolete_token_files
    return unless @store_path && Dir.exist?(@store_path)

    Dir.glob(File.join(@store_path, "za_tokens_*.dat")).each do |file|
      begin
        mtime = File.mtime(file)
        if Time.now - mtime > 24 * 60 * 60 # older than 1 day (86400 seconds)
          File.delete(file)
          # You might want to log this deletion for traceability
          # puts "Deleted obsolete token file: #{file}"
        end
      rescue => e
        # Optionally log errors, but continue
        # puts "Error checking or deleting file #{file}: #{e.message}"
      end
    end
  end

  def create_request(method, uri, config)
    encoded_config = nil
    if config && !config.empty?
      encoded_config = "CONFIG=#{ERB::Util.url_encode(config.to_json)}"
    end

    case method.upcase
    when 'GET'
      uri.query = encoded_config if encoded_config
      Net::HTTP::Get.new(uri)
    when 'POST'
      request = Net::HTTP::Post.new(uri)
      request.body = encoded_config if encoded_config
      request.content_type = 'application/x-www-form-urlencoded'
      request
    when 'PUT'
      request = Net::HTTP::Put.new(uri)
      request.body = encoded_config if encoded_config
      request.content_type = 'application/x-www-form-urlencoded'
      request
    when 'DELETE'
      request = Net::HTTP::Delete.new(uri)
      request.body = encoded_config if encoded_config
      request.content_type = 'application/x-www-form-urlencoded'
      request
    else
      raise ArgumentError, "Unsupported HTTP method: #{method}"
    end
  end

  def send_api_request(method, endpoint, config, request_headers)
    ensure_access_token
    uri = URI("#{@analytics_server_url}#{endpoint}")
    http = create_http_client(uri)
    request = create_request(method, uri, config)
    add_headers(request, request_headers)
    request['Authorization'] = "Zoho-oauthtoken #{@access_token}"
    request['User-Agent'] = "Analytics Ruby Client v2_#{CLIENT_VERSION}"
        
    response = http.request(request)
    response = handle_response_errors(response, http: http, request: request)
    
    return nil if response.code.to_i == 204 || response.body.nil? || response.body.strip.empty?

    begin
      result = JSON.parse(response.body)
      return result["data"]
    rescue JSON::ParserError
      raise ParseError.new("Failed to parse response: #{response.body}")
    end
  end


    # Send import API request to the server
    def send_import_api_request(endpoint, config, request_headers, file_path, data = nil)
      ensure_access_token
      url = @analytics_server_url + endpoint
      form_data = { 'CONFIG' => config.to_json }
      form_data['DATA'] = data.to_json if data
      form_data['FILE'] = File.open(file_path) if file_path
      response = submit_import_request(url, config.to_json, request_headers, @access_token, form_data)

      response = handle_import_response_errors(response, url, config, request_headers, form_data)

      begin
        result = JSON.parse(response.body)
        return result["data"]
      rescue JSON::ParserError
        raise ParseError.new("Failed to parse response: #{response.body}")
      ensure
        form_data['FILE'].close if form_data['FILE']
      end
    end

    def handle_import_response_errors(response, url, config, headers, form_data)
      unless response.is_a?(Net::HTTPSuccess)
        if is_oauth_expired(response)
          if @use_direct_access_token
            raise ServerError.new("Direct access token is invalid or expired.", true, response.code.to_i)
          else
            regenerate_access_token
            response = submit_import_request(url, config, headers, @access_token, form_data)
            unless response.is_a?(Net::HTTPSuccess)
              error_code, error_message = extract_error_from_response(response)
              raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
            end
          end
        else
          error_code, error_message = extract_error_from_response(response)
          raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
        end
      end
      response
    end


    # Send batch import API request to the server
    def send_batch_import_api_request(endpoint, config, request_headers, file_path, batch_size, tool_config)
      ensure_access_token
      file_header = File.open(file_path, 'r').readline
      file_lines  = File.readlines(file_path).drop(1) # Skip header
      total_lines = file_lines.size
      total_batch_count = (total_lines.to_f / batch_size).ceil
      config["batchKey"] = "start"
      url = @analytics_server_url + endpoint
      response = nil
      total_batch_count.times do |i|
        batch       = file_lines.slice(i * batch_size, batch_size).join
        batch_content = file_header + batch
        temp_file = Tempfile.new(['batch_data_', '.csv'])
        temp_file.write(batch_content)
        temp_file.rewind

        config["isLastBatch"] = (i == total_batch_count - 1).to_s
        form_data = {
          'CONFIG' => config.to_json,
          'FILE'   => File.open(temp_file.path)
        }

        puts "[DEBUG] Sending batch #{i + 1}/#{total_batch_count}, lines=#{batch.split("\n").size}"

        resp = submit_import_request(url, config.to_json, request_headers, @access_token, form_data)
        resp = handle_import_response_errors(resp, url, config.to_json, request_headers, form_data)

        begin
          response = JSON.parse(resp.body)
          config["batchKey"] = response["data"]["batchKey"]
          sleep(2)
        rescue JSON::ParserError
          raise ParseError.new("Failed to parse response: #{resp.body}")
        ensure
          form_data['FILE'].close if form_data['FILE']
          temp_file.close
          temp_file.unlink
        end
      end
      response["data"]
    end


    # Send export API request to the server
    def send_export_api_request(endpoint, config, request_headers, file_path)
      ensure_access_token
      url = @analytics_server_url + endpoint
      uri = URI(url)
      uri.query = URI.encode_www_form('CONFIG' => config.to_json) if config && !config.empty?
      http = create_http_client(uri)
      request = Net::HTTP::Get.new(uri)
      add_headers(request, request_headers)
      request['Authorization'] = "Zoho-oauthtoken #{@access_token}"
      request['User-Agent'] = "Analytics Ruby Client v2_#{CLIENT_VERSION}"
      response = http.request(request)

      unless response.is_a?(Net::HTTPSuccess)
        if is_oauth_expired(response)
          if @use_direct_access_token
            raise ServerError.new("Direct access token is invalid or expired.", true, response.code.to_i)
          else
            regenerate_access_token
            request['Authorization'] = "Zoho-oauthtoken #{@access_token}"
            response = http.request(request)
            unless response.is_a?(Net::HTTPSuccess)
              error_code, error_message = extract_error_from_response(response)
              raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
            end
          end
        else
          error_code, error_message = extract_error_from_response(response)
          raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
        end
      end

      File.open(file_path, 'wb') { |file| file.write(response.body) }
    end


    # Submit import request (multipart/form-data)
    def submit_import_request(url, config_data, headers, access_token, files)
      uri = URI(url)
      http = create_http_client(uri)
      request = Net::HTTP::Post.new(uri)
      headers&.each { |key, value| request[key] = value }
      request['Authorization'] = "Zoho-oauthtoken #{access_token}"
      request['User-Agent']   = "Analytics Ruby Client v2_#{CLIENT_VERSION}"
      form_data = {}
      form_data['CONFIG'] = config_data.is_a?(Hash) ? config_data.to_json : config_data
      files.each { |key, file| form_data[key] = file }
      request.set_form(form_data, 'multipart/form-data')
      http.request(request)
    end

    def handle_response_errors(response, http:, request:)
      unless response.is_a?(Net::HTTPSuccess)
        if is_oauth_expired(response)
          if @use_direct_access_token
            raise ServerError.new("Direct access token is invalid or expired.", true, response.code.to_i)
          else
            regenerate_access_token
            request['Authorization'] = "Zoho-oauthtoken #{@access_token}"
            response = http.request(request)
            unless response.is_a?(Net::HTTPSuccess)
              error_code, error_message = extract_error_from_response(response)
              raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
            end
          end
        else
          error_code, error_message = extract_error_from_response(response)
          raise ServerError.new("HTTP #{error_code}: #{error_message}", false, error_code)
        end
      end
      response
    end

    def extract_error_from_response(response)
      error_code = response.code.to_i
      error_message = nil
      begin
        body = JSON.parse(response.body)
        if body.is_a?(Hash)
          if body["data"]
            error_code = body["data"]["errorCode"] || error_code
            error_message = body["data"]["errorMessage"] || body["error"]["description"]
          end
          error_code ||= body["errorCode"]
          error_message ||= body["errorMessage"]
        end
      rescue JSON::ParserError
        error_message = response.body
      end
      error_message ||= "Unknown server error"
      [error_code, error_message]
    end

    # Helper: HTTP/Proxy
    def create_http_client(uri)
      if @proxy
        Net::HTTP.new(uri.host, uri.port, @proxy_host, @proxy_port, @proxy_user_name, @proxy_password)
      else
        Net::HTTP.new(uri.host, uri.port)
      end.tap do |http|
        http.use_ssl = (uri.scheme == 'https')
        http.verify_mode = OpenSSL::SSL::VERIFY_PEER
        if http.use_ssl?
          begin
            http.min_version = OpenSSL::SSL::TLS1_2_VERSION if defined?(OpenSSL::SSL::TLS1_2_VERSION)
            http.max_version = OpenSSL::SSL::TLS1_3_VERSION if defined?(OpenSSL::SSL::TLS1_3_VERSION)
          rescue NameError, NotImplementedError
            # Older OpenSSL builds may not expose min_version/max_version;
            # fall back to library defaults (still TLS 1.2+ on modern Ruby).
          end
          begin
            http.ciphers = 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305'
          rescue StandardError
            # If none of the strong cipher names are available, keep defaults
            # so requests still succeed.
          end
        end
      end
    end

    def add_headers(request, headers)
      headers&.each { |key, value| request[key] = value }
    end

    # Check if OAuth token is expired
    def is_oauth_expired(response)
      return false unless response.body
      begin
        json_response = JSON.parse(response.body)
        errorCode = json_response["data"] && json_response["data"]["errorCode"]
        return errorCode == 8535
      rescue JSON::ParserError
        return false
      end
    end

  # Sets the accounts server URL
  # @param url [String] The accounts server URL
  # @return [String] The updated accounts server URL
  def set_accounts_server_url(url)
    @accounts_server_url = url
  end
  
  # Gets the current accounts server URL
  # @return [String] The current accounts server URL
  def get_accounts_server_url
    @accounts_server_url
  end
  
  # Sets the analytics server URL
  # @param url [String] The analytics server URL
  # @return [String] The updated analytics server URL
  def set_analytics_server_url(url)
    @analytics_server_url = url
  end
  
  # Gets the current analytics server URL
  # @return [String] The current analytics server URL
  def get_analytics_server_url
    @analytics_server_url
  end

  # Returns a new OrgAPI instance.
  # @param org_id [String] The id of the organization.
  # @return [OrgAPI] Organization API instance
  def get_org_instance(org_id)
    OrgAPI.new(self, org_id)
  end

  # Returns a new WorkspaceAPI instance.
  # @param org_id [String] The id of the organization.
  # @param workspace_id [String] The id of the workspace.
  # @return [WorkspaceAPI] Workspace API instance
  def get_workspace_instance(org_id, workspace_id)
    WorkspaceAPI.new(self, org_id, workspace_id)
  end

  # Returns a new ViewAPI instance.
  # @param org_id [String] The id of the organization.
  # @param workspace_id [String] The id of the workspace.
  # @param view_id [String] The id of the view.
  # @return [ViewAPI] View API instance
  def get_view_instance(org_id, workspace_id, view_id)
    ViewAPI.new(self, org_id, workspace_id, view_id)
  end

  # Returns a new BulkAPI instance.
  # @param org_id [String] The id of the organization.
  # @param workspace_id [String] The id of the workspace.
  # @return [BulkAPI] Bulk API instance
  def get_bulk_instance(org_id, workspace_id)
    BulkAPI.new(self, org_id, workspace_id)
  end

  # Returns list of all accessible organizations.
  # @return [Array] Organization list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_orgs
    endpoint = "/restapi/v2/orgs"
    response = send_api_request("GET", endpoint, nil, nil)
    response["orgs"]
  end

  # Returns list of all accessible workspaces.
  # @return [Hash] Workspace list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_workspaces
    endpoint = "/restapi/v2/workspaces"
    response = send_api_request("GET", endpoint, nil, nil)
    response
  end

  # Returns list of owned workspaces.
  # @return [Array] Workspace list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_owned_workspaces
    endpoint = "/restapi/v2/workspaces/owned"
    response = send_api_request("GET", endpoint, nil, nil)
    response["workspaces"]
  end

  # Returns list of shared workspaces.
  # @return [Array] Workspace list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_shared_workspaces
    endpoint = "/restapi/v2/workspaces/shared"
    response = send_api_request("GET", endpoint, nil, nil)
    response["workspaces"]
  end

  # Returns list of recently accessed views.
  # @return [Array] View list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_recent_views
    endpoint = "/restapi/v2/recentviews"
    response = send_api_request("GET", endpoint, nil, nil)
    response["views"]
  end

  # Returns list of all accessible dashboards.
  # @return [Hash] Dashboard list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_dashboards
    endpoint = "/restapi/v2/dashboards"
    response = send_api_request("GET", endpoint, nil, nil)
    response
  end

  # Returns list of owned dashboards.
  # @return [Array] Dashboard list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_owned_dashboards
    endpoint = "/restapi/v2/dashboards/owned"
    response = send_api_request("GET", endpoint, nil, nil)
    response["views"]
  end

  # Returns list of shared dashboards.
  # @return [Array] Dashboard list.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_shared_dashboards
    endpoint = "/restapi/v2/dashboards/shared"
    response = send_api_request("GET", endpoint, nil, nil)
    response["views"]
  end

  # Returns details of the specified workspace.
  # @param workspace_id [String] Id of the workspace.
  # @return [Hash] Workspace details.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_workspace_details(workspace_id)
    endpoint = "/restapi/v2/workspaces/#{workspace_id}"
    response = send_api_request("GET", endpoint, nil, nil)
    response["workspaces"]
  end

  # Returns details of the specified view.
  # @param view_id [String] Id of the view.
  # @param config [Hash] Contains any additional control parameters. Can be nil.
  # @return [Hash] View details.
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def get_view_details(view_id, config = {})
    endpoint = "/restapi/v2/views/#{view_id}"
    response = send_api_request("GET", endpoint, config, nil)
    response["views"]
  end
end

# OrgAPI contains organization-level operations.
  class OrgAPI
    # Initializes a new instance of OrgAPI.
    #
    # @param ac [AnalyticsClient] The analytics client instance
    # @param org_id [String] The organization ID
    def initialize(ac, org_id)
      @ac = ac
      @request_headers = { 'ZANALYTICS-ORGID' => org_id }
    end

    # Create a blank workspace in the specified organization.
    #
    # @param workspace_name [String] The name of the workspace
    # @param config [Hash] Optional configuration parameters
    # @return [Integer] Created workspace ID
    # @raise [ServerError] If server returns an error
    # @raise [ParseError] If the response is not parsable
    def create_workspace(workspace_name, config = {})
      config['workspaceName'] = workspace_name
      endpoint = '/restapi/v2/workspaces/'
      response = @ac.send_api_request('POST', endpoint, config, @request_headers)
      response['workspaceId'].to_i
    end

    # Returns list of admins for a specified organization.
    #
    # @return [Array<Hash>] List of organization admins
    def get_admins
      endpoint = '/restapi/v2/orgadmins'
      response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
      response['orgAdmins']
    end

    # Returns list of users for the specified organization.
    #
    # @return [Array<Hash>] List of users
    def get_users
      endpoint = '/restapi/v2/users'
      response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
      response['users']
    end

    # Add users to the specified organization.
    #
    # @param email_ids [Array<String>] Email addresses to add
    # @param config [Hash] Optional config
    def add_users(email_ids, config = {})
      config['emailIds'] = email_ids
      endpoint = '/restapi/v2/users'
      @ac.send_api_request('POST', endpoint, config, @request_headers)
    end

    # Remove users from the specified organization.
    #
    # @param email_ids [Array<String>] Email addresses to remove
    # @param config [Hash] Optional config
    def remove_users(email_ids, config = {})
      config['emailIds'] = email_ids
      endpoint = '/restapi/v2/users'
      @ac.send_api_request('DELETE', endpoint, config, @request_headers)
    end

    # Activate users in the specified organization.
    #
    # @param email_ids [Array<String>] Email addresses to activate
    # @param config [Hash] Optional config
    def activate_users(email_ids, config = {})
      config['emailIds'] = email_ids
      endpoint = '/restapi/v2/users/active'
      @ac.send_api_request('PUT', endpoint, config, @request_headers)
    end

    # Deactivate users in the specified organization.
    #
    # @param email_ids [Array<String>] Email addresses to deactivate
    # @param config [Hash] Optional config
    def deactivate_users(email_ids, config = {})
      config['emailIds'] = email_ids
      endpoint = '/restapi/v2/users/inactive'
      @ac.send_api_request('PUT', endpoint, config, @request_headers)
    end

    # Change role for the specified users.
    #
    # @param email_ids [Array<String>] Email addresses to modify
    # @param role [String] New role to assign
    # @param config [Hash] Optional config
    def change_user_role(email_ids, role, config = {})
      config['emailIds'] = email_ids
      config['role'] = role
      endpoint = '/restapi/v2/users/role'
      @ac.send_api_request('PUT', endpoint, config, @request_headers)
    end

    # Returns subscription details of the specified organization.
    #
    # @return [Hash] Subscription details
    def get_subscription_details
      endpoint = '/restapi/v2/subscription'
      response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
      response['subscription']
    end

    # Returns resource usage details of the specified organization.
    #
    # @return [Hash] Resource usage details
    def get_resource_details
      endpoint = '/restapi/v2/resources'
      response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
      response['resourceDetails']
    end

    # Returns metadata details of a workspace or a specific view.
    #
    # @param workspace_name [String] Name of the workspace
    # @param view_name [String, nil] Name of the view (optional)
    # @return [Hash] Metadata details
    def get_meta_details(workspace_name, view_name = nil)
      config = { 'workspaceName' => workspace_name }
      config['viewName'] = view_name unless view_name.nil?
      endpoint = '/restapi/v2/metadetails'
      response = @ac.send_api_request('GET', endpoint, config, @request_headers)
      response
    end

    # Returns all AutoML analyses available in the organization.
    #
    # @return [Array<Hash>] AutoML analysis list
    # @raise [ServerError]
    # @raise [ParseError]
    def get_automl_analysis
      endpoint = "/restapi/v2/automl/analysis"
      response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
      response["analysis"]
    end
    # Returns list of all custom roles available in the organization.
    # @return [Array<Hash>] Custom roles list
    def get_custom_roles
      endpoint = "/restapi/v2/orgs/roles"
      response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
      response["roles"]
    end
    # Create a new custom role in the organization.
    # @param role_name [String] Name of the custom role to be created
    # @param access_type [String] Access type for the custom role
    # @param permissions [Hash] Permissions configuration
    # @param config [Hash] Additional control parameters
    # @return [String] Created custom role id
    def create_custom_role(role_name, access_type, permissions, config = {})
      config["roleName"] = role_name
      config["accessType"] = access_type
      config["permissions"] = permissions
      endpoint = "/restapi/v2/orgs/roles"
      response = @ac.send_api_request("POST", endpoint, config, @request_headers)
      response["roleId"].to_s
    end
    # Update the existing custom role in the organization.
    # @param role_id [String] Id of the custom role to be updated
    # @param role_name [String] New name for the custom role
    # @param access_type [String] New access type for the custom role
    # @param permissions [Hash] New permissions configuration
    # @param config [Hash] Additional control parameters
    def update_custom_role(role_id, role_name, access_type, permissions, config = {})
      config["roleName"] = role_name
      config["accessType"] = access_type
      config["permissions"] = permissions
      endpoint = "/restapi/v2/orgs/roles/#{role_id}"
      @ac.send_api_request("PUT", endpoint, config, @request_headers)
    end
    # Delete the specified custom role from the organization.
    # @param role_id [String] Id of the custom role to be deleted
    def delete_custom_role(role_id)
      endpoint = "/restapi/v2/orgs/roles/#{role_id}"
      @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
    end


    # Returns the access restriction settings configured for the organization.
    # @return [Hash] Organization access restriction settings
    def get_org_access_restrictions
      endpoint = "/restapi/v2/security-controls/access-restrictions"
      @ac.send_api_request("GET", endpoint, nil, @request_headers)
    end
    # Update the access restriction settings of the organization.
    # @param config [Hash] Contains the access restriction configurations to be updated
    def update_org_access_restrictions(config = {})
      endpoint = "/restapi/v2/security-controls/access-restrictions"
      @ac.send_api_request("PUT", endpoint, config, @request_headers)
    end
    # Returns list of linked workspaces available in the specified organization.
    # @return [Array<Hash>] Linked workspaces list
    def get_linked_workspaces
      endpoint = "/restapi/v2/linkedworkspaces"
      response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
      response["linkedWorkspaces"]
    end

  end

    # WorkspaceAPI contains workspace-level operations.
    class WorkspaceAPI
      # Initializes a new instance of WorkspaceAPI.
      #
      # @param ac [AnalyticsClient] The analytics client instance
      # @param org_id [String] The organization ID
      # @param workspace_id [String] The workspace ID
      def initialize(ac, org_id, workspace_id)
        @ac = ac
        @endpoint = "/restapi/v2/workspaces/#{workspace_id}"
        @security_controls_endpoint = "/restapi/v2/security-controls/workspaces/#{workspace_id}"
        @request_headers = { 'ZANALYTICS-ORGID' => org_id }
        @workspace_id = workspace_id
      end

      # Copy the specified workspace to a new one.
      #
      # @param new_workspace_name [String] New workspace name
      # @param config [Hash] Optional config
      # @param dest_org_id [String, nil] Destination org ID (optional)
      # @return [Integer] Copied workspace ID
      def copy(new_workspace_name, config = {}, dest_org_id = nil)
        config['newWorkspaceName'] = new_workspace_name
        headers = @request_headers.dup
        headers['ZANALYTICS-DEST-ORGID'] = dest_org_id if dest_org_id
        response = @ac.send_api_request('POST', @endpoint, config, headers)
        response['workspaceId'].to_i
      end

      # Rename the specified workspace.
      #
      # @param workspace_name [String] New name
      # @param config [Hash] Optional config
      def rename(workspace_name, config = {})
        config['workspaceName'] = workspace_name
        @ac.send_api_request('PUT', @endpoint, config, @request_headers)
      end

      # Delete the specified workspace.
      def delete
        @ac.send_api_request('DELETE', @endpoint, nil, @request_headers)
      end

      # Get the secret key for the workspace.
      #
      # @param config [Hash] Optional config
      # @return [String] Secret key
      def get_secret_key(config = {})
        endpoint = "#{@endpoint}/secretkey"
        response = @ac.send_api_request('GET', endpoint, config, @request_headers)
        response['workspaceKey']
      end

      # Mark the workspace as favorite.
      def add_favorite
        endpoint = "#{@endpoint}/favorite"
        @ac.send_api_request('POST', endpoint, nil, @request_headers)
      end

      # Unmark the workspace as favorite.
      def remove_favorite
        endpoint = "#{@endpoint}/favorite"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Set the workspace as default.
      def add_default
        endpoint = "#{@endpoint}/default"
        @ac.send_api_request('POST', endpoint, nil, @request_headers)
      end

      # Unset the workspace from default.
      def remove_default
        endpoint = "#{@endpoint}/default"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Get list of admins for the workspace.
      #
      # @return [Array<Hash>] Admin details
      def get_admins
        endpoint = "#{@endpoint}/admins"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['workspaceAdmins']
      end

      # Add admins to the workspace.
      #
      # @param email_ids [Array<String>] Email addresses
      # @param config [Hash] Optional config
      def add_admins(email_ids, config = {})
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/admins"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Remove admins from the workspace.
      #
      # @param email_ids [Array<String>] Email addresses
      # @param config [Hash] Optional config
      def remove_admins(email_ids, config = {})
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/admins"
        @ac.send_api_request('DELETE', endpoint, config, @request_headers)
      end

      # Get workspace share info.
      #
      # @return [Hash] Share information
      def get_share_info
        endpoint = "#{@endpoint}/share"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response
      end

      # Share views to users.
      #
      # @param view_ids [Array<String>] View IDs to share
      # @param email_ids [Array<String>] User emails
      # @param permissions [Hash] Permission map
      # @param config [Hash] Optional config
      def share_views(view_ids, email_ids, permissions, config = {})
        config['viewIds'] = view_ids
        config['emailIds'] = email_ids
        config['permissions'] = permissions
        endpoint = "#{@endpoint}/share"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Remove shared views for specific users.
      #
      # @param view_ids [Array<String>, nil] View IDs
      # @param email_ids [Array<String>] User emails
      # @param config [Hash] Optional config
      def remove_share(view_ids, email_ids, config = {})
        config['emailIds'] = email_ids
        config['viewIds'] = view_ids if view_ids
        endpoint = "#{@endpoint}/share"
        @ac.send_api_request('DELETE', endpoint, config, @request_headers)
      end

      # Get shared details for the given views.
      #
      # @param view_ids [Array<String>] View IDs
      # @return [Array<Hash>] Shared detail entries
      def get_shared_details_for_views(view_ids)
        config = { 'viewIds' => view_ids }
        endpoint = "#{@endpoint}/share/shareddetails"
        response = @ac.send_api_request('GET', endpoint, config, @request_headers)
        response['sharedDetails']
      end

      # Returns a list of all accessible folders in the workspace.
      #
      # @return [Array<Hash>] Folder list
      def get_folders
        endpoint = "#{@endpoint}/folders"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['folders']
      end

      # Create a new folder in the workspace.
      #
      # @param folder_name [String] Folder name
      # @param config [Hash] Optional config
      # @return [Integer] Created folder ID
      def create_folder(folder_name, config = {})
        config['folderName'] = folder_name
        endpoint = "#{@endpoint}/folders"
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['folderId'].to_i
      end

      # Get list of all views in the workspace.
      #
      # @param config [Hash] Optional config
      # @return [Array<Hash>] View list
      def get_views(config = {})
        endpoint = "#{@endpoint}/views"
        response = @ac.send_api_request('GET', endpoint, config, @request_headers)
        response['views']
      end

      # Create a new table in the workspace.
      #
      # @param table_design [Hash] Table definition
      # @return [Integer] Created view ID
      def create_table(table_design)
        config = { 'tableDesign' => table_design }
        endpoint = "#{@endpoint}/tables"
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['viewId'].to_i
      end

      # Create a new query table in the workspace.
      #
      # @param sql_query [String] SQL definition
      # @param query_table_name [String] Name of query table
      # @param config [Hash] Optional config
      # @return [Integer] Created view ID
      def create_query_table(sql_query, query_table_name, config = {})
        config['sqlQuery'] = sql_query
        config['queryTableName'] = query_table_name
        endpoint = "#{@endpoint}/querytables"
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['viewId'].to_i
      end

      # Update an existing query table.
      #
      # @param view_id [String] View ID
      # @param sql_query [String] New SQL query
      # @param config [Hash] Optional config
      def edit_query_table(view_id, sql_query, config = {})
        config['sqlQuery'] = sql_query
        endpoint = "#{@endpoint}/querytables/#{view_id}"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end
      # Returns list of all query tables for the specified workspace.
      # @param config [Hash] Additional control parameters
      # @return [Array<Hash>] Query table list
      def get_query_tables(config = {})
        endpoint = "#{@endpoint}/querytables"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["queryTables"]
      end

      # Copy views to another workspace.
      #
      # @param view_ids [Array<String>] IDs to copy
      # @param dest_workspace_id [String] Destination workspace ID
      # @param config [Hash] Optional config
      # @param dest_org_id [String, nil] Destination org ID
      # @return [Array<Hash>] Copied views
      def copy_views(view_ids, dest_workspace_id, config = {}, dest_org_id = nil)
        config['viewIds'] = view_ids
        config['destWorkspaceId'] = dest_workspace_id
        endpoint = "#{@endpoint}/views/copy"
        headers = @request_headers.dup
        headers['ZANALYTICS-DEST-ORGID'] = dest_org_id if dest_org_id
        response = @ac.send_api_request('POST', endpoint, config, headers)
        response['views']
      end

      # Enable the workspace for white-label domain access.
      def enable_domain_access
        endpoint = "#{@endpoint}/wlaccess"
        @ac.send_api_request('POST', endpoint, nil, @request_headers)
      end

      # Disable white-label domain access for the workspace.
      def disable_domain_access
        endpoint = "#{@endpoint}/wlaccess"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Rename a folder.
      #
      # @param folder_id [String] Folder ID
      # @param folder_name [String] New name
      # @param config [Hash] Optional config
      def rename_folder(folder_id, folder_name, config = {})
        config['folderName'] = folder_name
        endpoint = "#{@endpoint}/folders/#{folder_id}"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Delete a folder.
      #
      # @param folder_id [String] Folder ID
      def delete_folder(folder_id)
        endpoint = "#{@endpoint}/folders/#{folder_id}"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Get groups in the workspace.
      #
      # @return [Array<Hash>] Group list
      def get_groups
        endpoint = "#{@endpoint}/groups"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['groups']
      end

      # Create a group.
      #
      # @param group_name [String] Name of group
      # @param email_ids [Array<String>] Emails of members
      # @param config [Hash] Optional config
      # @return [Integer] Group ID
      def create_group(group_name, email_ids, config = {})
        config['groupName'] = group_name
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/groups"
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['groupId'].to_i
      end

      # Get details for a group.
      #
      # @param group_id [String] Group ID
      # @return [Hash] Group details
      def get_group_details(group_id)
        endpoint = "#{@endpoint}/groups/#{group_id}"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['groups']
      end

      # Rename a group.
      #
      # @param group_id [String] Group ID
      # @param group_name [String] New name
      # @param config [Hash] Optional config
      def rename_group(group_id, group_name, config = {})
        config['groupName'] = group_name
        endpoint = "#{@endpoint}/groups/#{group_id}"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Delete a group.
      #
      # @param group_id [String] Group ID
      def delete_group(group_id)
        endpoint = "#{@endpoint}/groups/#{group_id}"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Add users to a group.
      #
      # @param group_id [String] Group ID
      # @param email_ids [Array<String>] Email list
      # @param config [Hash] Optional config
      def add_group_members(group_id, email_ids, config = {})
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/groups/#{group_id}/members"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Remove users from a group.
      #
      # @param group_id [String] Group ID
      # @param email_ids [Array<String>] Email list
      # @param config [Hash] Optional config
      def remove_group_members(group_id, email_ids, config = {})
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/groups/#{group_id}/members"
        @ac.send_api_request('DELETE', endpoint, config, @request_headers)
      end

      # Create a slideshow in the workspace.
      #
      # @param slide_name [String] Name of slideshow
      # @param view_ids [Array<String>] View IDs
      # @param config [Hash] Optional config
      # @return [Integer] Slideshow ID
      def create_slideshow(slide_name, view_ids, config = {})
        config['slideName'] = slide_name
        config['viewIds'] = view_ids
        endpoint = "#{@endpoint}/slides"
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['slideId'].to_i
      end

      # Update a slideshow.
      #
      # @param slide_id [String] Slideshow ID
      # @param config [Hash] Update data
      def update_slideshow(slide_id, config = {})
        endpoint = "#{@endpoint}/slides/#{slide_id}"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Delete a slideshow.
      #
      # @param slide_id [String] Slideshow ID
      def delete_slideshow(slide_id)
        endpoint = "#{@endpoint}/slides/#{slide_id}"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Get all slideshows in the workspace.
      #
      # @return [Array<Hash>] Slideshow list
      def get_slideshows
        endpoint = "#{@endpoint}/slides"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['slideshows']
      end

      # Get URL to access a slideshow.
      #
      # @param slide_id [String] Slideshow ID
      # @param config [Hash] Optional config
      # @return [String] Published URL
      def get_slideshow_url(slide_id, config = {})
        endpoint = "#{@endpoint}/slides/#{slide_id}/publish"
        response = @ac.send_api_request('GET', endpoint, config, @request_headers)
        response['slideUrl']
      end

      # Get slideshow details.
      #
      # @param slide_id [String] Slideshow ID
      # @return [Hash] Slideshow details
      def get_slideshow_details(slide_id)
        endpoint = "#{@endpoint}/slides/#{slide_id}"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['slideInfo']
      end
      
      # Create a variable in the workspace.
      #
      # @param variable_name [String] Name of the variable
      # @param variable_datatype [String] Datatype of the variable
      # @param variable_type [String] Type of the variable
      # @param config [Hash] Additional config
      # @return [Integer] Variable ID
      def create_variable(variable_name, variable_datatype, variable_type, config = {})
        endpoint = "#{@endpoint}/variables"
        config['variableName'] = variable_name
        config['variableDataType'] = variable_datatype
        config['variableType'] = variable_type
        response = @ac.send_api_request('POST', endpoint, config, @request_headers)
        response['variableId'].to_i
      end

      # Update a variable in the workspace.
      def update_variable(variable_id, variable_name, variable_datatype, variable_type, config = {})
        endpoint = "#{@endpoint}/variables/#{variable_id}"
        config['variableName'] = variable_name
        config['variableDataType'] = variable_datatype
        config['variableType'] = variable_type
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Delete a variable from the workspace.
      def delete_variable(variable_id)
        endpoint = "#{@endpoint}/variables/#{variable_id}"
        @ac.send_api_request('DELETE', endpoint, nil, @request_headers)
      end

      # Get list of variables in the workspace.
      #
      # @return [Array<Hash>] List of variables
      def get_variables
        endpoint = "#{@endpoint}/variables"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['variables']
      end

      # Get details of a specific variable.
      #
      # @param variable_id [String] ID of the variable
      # @return [Hash] Variable details
      def get_variable_details(variable_id)
        endpoint = "#{@endpoint}/variables/#{variable_id}"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response
      end

      # Mark a folder as default.
      def make_default_folder(folder_id)
        endpoint = "#{@endpoint}/folders/#{folder_id}/default"
        @ac.send_api_request('PUT', endpoint, nil, @request_headers)
      end

      # Get list of data sources.
      #
      # @return [Array<Hash>] List of data sources
      def get_datasources
        endpoint = "#{@endpoint}/datasources"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['dataSources']
      end

      # Trigger data sync for a data source.
      def sync_data(datasource_id, config = {})
        endpoint = "#{@endpoint}/datasources/#{datasource_id}/sync"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Update data source connection.
      def update_datasource_connection(datasource_id, config = {})
        endpoint = "#{@endpoint}/datasources/#{datasource_id}"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Get list of trash views.
      #
      # @return [Array<Hash>] Trash views
      def get_trash_views
        endpoint = "#{@endpoint}/trash"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['views']
      end

      # Restore a view from trash.
      def restore_trash_views(view_id, config = {})
        endpoint = "#{@endpoint}/trash/#{view_id}"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Permanently delete a view from trash.
      def delete_trash_views(view_id, config = {})
        endpoint = "#{@endpoint}/trash/#{view_id}"
        @ac.send_api_request('DELETE', endpoint, config, @request_headers)
      end

      # Change folder hierarchy (parent/child).
      def change_folder_hierarchy(folder_id, hierarchy, config = {})
        endpoint = "#{@endpoint}/folders/#{folder_id}/move"
        config['hierarchy'] = hierarchy
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Reorder folder relative to another folder.
      def change_folder_position(folder_id, reference_folder_id, config = {})
        endpoint = "#{@endpoint}/folders/#{folder_id}/reorder"
        config['referenceFolderId'] = reference_folder_id
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Move views into a folder.
      def move_views_to_folder(folder_id, view_ids, config = {})
        endpoint = "#{@endpoint}/views/movetofolder"
        config['folderId'] = folder_id
        config['viewIds'] = view_ids
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Export views as a template file.
      #
      # @param view_ids [Array<String>] View IDs
      # @param file_path [String] Path to save the file
      # @param config [Hash] Optional config
      def export_as_template(view_ids, file_path, config = {})
        endpoint = "#{@endpoint}/template/data"
        config['viewIds'] = view_ids
        @ac.send_export_api_request(endpoint, config, @request_headers, file_path)
      end

      # Get users in the workspace.
      #
      # @return [Array<Hash>] User list
      def get_workspace_users
        endpoint = "#{@endpoint}/users"
        response = @ac.send_api_request('GET', endpoint, nil, @request_headers)
        response['users']
      end

      # Add users to the workspace.
      def add_workspace_users(email_ids, role, config = {})
        config['emailIds'] = email_ids
        config['role'] = role
        endpoint = "#{@endpoint}/users"
        @ac.send_api_request('POST', endpoint, config, @request_headers)
      end

      # Remove users from the workspace.
      def remove_workspace_users(email_ids, config = {})
        config['emailIds'] = email_ids
        endpoint = "#{@endpoint}/users"
        @ac.send_api_request('DELETE', endpoint, config, @request_headers)
      end

      # Change status (activate/deactivate) of workspace users.
      def change_workspace_user_status(email_ids, operation, config = {})
        config['emailIds'] = email_ids
        config['operation'] = operation
        endpoint = "#{@endpoint}/users/status"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end

      # Change role of workspace users.
      def change_workspace_user_role(email_ids, role, config = {})
        config['emailIds'] = email_ids
        config['role'] = role
        endpoint = "#{@endpoint}/users/role"
        @ac.send_api_request('PUT', endpoint, config, @request_headers)
      end
      
      # Returns list of email schedules available in the specified workspace.
      # @return [Array] list of email schedules
      # @raise [ServerError] if the server fails to process the request
      # @raise [ParseError] if the response can't be parsed
      def get_email_schedules
        endpoint = "#{@endpoint}/emailschedules"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["emailSchedules"]
      end

      # Create an email schedule in the specified workspace.
      # @param schedule_name [String] name of the email schedule
      # @param view_ids [Array] list of view IDs to be mailed
      # @param format [String] format in which data will be mailed
      # @param email_ids [Array] list of recipient email addresses
      # @param schedule_details [Hash] frequency, date, and time details
      # @param config [Hash] additional optional parameters (default: {})
      # @return [String] created email schedule ID
      def create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config = {})
        config["scheduleName"] = schedule_name
        config["viewIds"] = view_ids
        config["exportType"] = format
        config["emailIds"] = email_ids
        config["scheduleDetails"] = schedule_details

        endpoint = "#{@endpoint}/emailschedules"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["scheduleId"].to_s
      end

      # Update configurations of the specified email schedule.
      # @param schedule_id [String] ID of the email schedule to update
      # @param config [Hash] configuration parameters to update
      # @return [String] updated schedule ID
      def update_email_schedule(schedule_id, config)
        endpoint = "#{@endpoint}/emailschedules/#{schedule_id}"
        response = @ac.send_api_request("PUT", endpoint, config, @request_headers)
        response["scheduleId"].to_s
      end

      # Trigger the configured email schedule instantly.
      # @param schedule_id [String] ID of the email schedule to trigger
      def trigger_email_schedule(schedule_id)
        endpoint = "#{@endpoint}/emailschedules/#{schedule_id}"
        @ac.send_api_request("POST", endpoint, nil, @request_headers)
      end

      # Update email schedule status (activate or deactivate).
      # @param schedule_id [String] ID of the email schedule
      # @param operation [String] operation to perform ("activate" or "deactivate")
      def change_email_schedule_status(schedule_id, operation)
        endpoint = "#{@endpoint}/emailschedules/#{schedule_id}/status"
        config = { "operation" => operation }
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Delete the specified email schedule.
      # @param schedule_id [String] ID of the email schedule to delete
      def delete_email_schedule(schedule_id)
        endpoint = "#{@endpoint}/emailschedules/#{schedule_id}"
        @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
      end

      # Returns list of all aggregate formulas for the specified workspace.
      # @param config [Hash] optional parameters (default: {})
      # @return [Array] list of aggregate formulas
      def get_aggregate_formulas(config = {})
        endpoint = "#{@endpoint}/aggregateformulas"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["aggregateFormulas"]
      end

      # Returns dependents for a specified aggregate formula.
      # @param formula_id [String] aggregate formula ID
      # @return [Hash] dependent views and formulas
      def get_aggregate_formula_dependents(formula_id)
        endpoint = "#{@endpoint}/aggregateformulas/#{formula_id}/dependents"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response
      end

      # Returns the value of the aggregate formula.
      # @param formula_id [String] aggregate formula ID
      # @return [String] formula value
      def get_aggregate_formula_value(formula_id)
        endpoint = "#{@endpoint}/aggregateformulas/#{formula_id}/value"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["formulaValue"]
      end

      # Create a report in the specified workspace.
      # @param config [Hash] report parameters
      # @return [Integer] created view ID
      def create_report(config = {})
        endpoint = "#{@endpoint}/reports"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["viewId"].to_i
      end

      # Update the design and configuration of the specified report.
      # @param view_id [String] ID of the report view
      # @param config [Hash] configuration parameters
      def update_report(view_id, config = {})
        endpoint = "#{@endpoint}/reports/#{view_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Returns details of the specified query table.
      #
      # @param query_table_id [String] Query table ID
      # @return [Hash] Query table details
      # @raise [ServerError] If the server fails to process the request
      # @raise [ParseError] If response parsing fails
      def get_query_table_details(query_table_id)
        endpoint = "#{@endpoint}/querytables/#{query_table_id}"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end

      # Returns all AutoML analyses for the workspace.
      #
      # @return [Array<Hash>] AutoML analysis list
      # @raise [ServerError]
      # @raise [ParseError]
      def get_automl_analysis
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["analysis"]
      end


      # Retrieves detailed information for a specific AutoML analysis.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @return [Hash] AutoML analysis details
      # @raise [ServerError]
      # @raise [ParseError]
      def get_automl_analysis_details(analysis_id)
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["analysis"]
      end


      # Returns deployment details for an AutoML analysis model.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param model_id [String] AutoML model ID
      # @return [Array<Hash>] Deployment details
      # @raise [ServerError]
      # @raise [ParseError]
      def get_deployment_details(analysis_id, model_id)
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/models/#{model_id}/deployments"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["deployments"]
      end


      # Creates a new AutoML analysis in the workspace.
      #
      # @param name [String] AutoML analysis name
      # @param training_table_id [String] Training table ID
      # @param prediction_type [String] Prediction type (REGRESSION / CLASSIFICATION / CLUSTERING)
      # @param features [Array<String>] Feature columns
      # @param server_option [Integer] Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB)
      # @param algorithms [Hash] Algorithms configuration
      # @param config [Hash] Additional parameters
      # @return [String] Created AutoML analysis ID
      # @raise [ServerError]
      # @raise [ParseError]
      def create_automl_analysis(
        name,
        training_table_id,
        prediction_type,
        features,
        server_option,
        algorithms,
        config = {}
      )
        config["name"]            = name
        config["trainingTableId"] = training_table_id
        config["predictionType"]  = prediction_type
        config["features"]        = features
        config["serverOption"]    = server_option
        config["algorithms"]      = algorithms

        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["id"].to_s
      end

      # Deletes the specified AutoML analysis from the workspace.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param config [Hash] Additional control parameters
      # @raise [ServerError]
      # @raise [ParseError]
      def delete_automl_analysis(analysis_id, config = {})
      endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}"
      @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Deletes a specific model from the given AutoML analysis.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param model_id [String] AutoML model ID
      # @param config [Hash] Additional control parameters
      # @raise [ServerError]
      # @raise [ParseError]
      def delete_automl_analysis_model(analysis_id, model_id, config = {})
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/models/#{model_id}"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Deploys an AutoML analysis model.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param model_id [String] AutoML model ID
      # @param input_table_id [String] Input table ID
      # @param output_table [String] Output table name
      # @param output_columns [Array<String>] Output column names
      # @param prediction_column [String] Prediction column name
      # @param server_option [Integer] Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB)
      # @param import_type [String] Import type (APPEND, TRUNCATEADD, UPDATEADD)
      # @param schedule_details [Hash, String] Schedule details or "none"
      # @param config [Hash] Additional control parameters
      # @return [Array<Hash>] Deployment details
      # @raise [ServerError]
      # @raise [ParseError]
      def create_automl_analysis_deployment(
        analysis_id,
        model_id,
        input_table_id,
        output_table,
        output_columns,
        prediction_column,
        server_option,
        import_type,
        schedule_details,
        config = {}
      )
        config["inputTableId"]     = input_table_id
        config["outputTable"]     = output_table
        config["outputColumns"]   = output_columns
        config["predictionColumn"] = prediction_column
        config["serverOption"]    = server_option
        config["importType"]      = import_type
        config["scheduleDetails"] = schedule_details.nil? ? "none" : schedule_details

        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/models/#{model_id}/deployments"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["deployments"]
      end

      # Executes an AutoML analysis deployment.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param deployment_id [String] Deployment ID
      # @param config [Hash] Additional control parameters
      # @raise [ServerError]
      # @raise [ParseError]
      def deploy_automl_analysis(analysis_id, deployment_id, config = {})
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/deployments/#{deployment_id}/execute"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Deletes an AutoML analysis deployment.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param deployment_id [String] Deployment ID
      # @param config [Hash] Additional control parameters
      # @raise [ServerError]
      # @raise [ParseError]
      def delete_automl_analysis_deployment(analysis_id, deployment_id, config = {})
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/deployments/#{deployment_id}"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Gets predictions by providing sample input values for a trained AutoML model.
      #
      # @param analysis_id [String] AutoML analysis ID
      # @param model_id [String] AutoML model ID
      # @param features [Hash] Feature values for prediction
      # @param config [Hash] Additional control parameters
      # @return [Hash] Prediction result
      # @raise [ServerError]
      # @raise [ParseError]
      def automl_analysis_prediction(analysis_id, model_id, features, config = {})
        config["features"] = features
        endpoint = "/restapi/v2/automl/workspaces/#{@workspace_id}/analysis/#{analysis_id}/models/#{model_id}/whatif"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Returns list of all tags for the specified workspace.
      # @return [Array<Hash>] Tags list
      def get_tags
        endpoint = "#{@endpoint}/tags"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["tags"]
      end
      # Create a tag in the specified workspace.
      # @param tag_name [String] Name of the tag to be created
      # @param color_code [String] Color of the tag in HEX color code
      # @param config [Hash] Additional control parameters
      # @return [String] Created tag id
      def create_tag(tag_name, color_code, config = {})
        config["name"] = tag_name
        config["colorCode"] = color_code
        endpoint = "#{@endpoint}/tags"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["tagId"].to_s
      end
      # Update details of the specified tag in the workspace.
      # @param tag_id [String] Id of the tag
      # @param config [Hash] Control parameters
      def update_tag(tag_id, config = {})
        endpoint = "#{@endpoint}/tags/#{tag_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end
      # Delete the specified tag from the workspace.
      # @param tag_id [String] Id of the tag
      def delete_tag(tag_id)
        endpoint = "#{@endpoint}/tags/#{tag_id}"
        @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
      end
      # Adds the specified tag to multiple views in the workspace.
      # @param tag_id [String] Id of the tag
      # @param view_ids [Array<String>] View ids to be associated with the tag
      # @param config [Hash] Additional control parameters
      def add_tag_to_views(tag_id, view_ids, config = {})
        config["viewIds"] = view_ids
        endpoint = "#{@endpoint}/tags/#{tag_id}/views"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Removes the specified tag from multiple views in the workspace.
      # @param tag_id [String] Id of the tag
      # @param view_ids [Array<String>, nil] View ids to be dissociated. Not required when dissociate_all is true.
      # @param dissociate_all [Boolean] To dissociate the tag from all associated views
      # @param config [Hash] Additional control parameters
      def remove_tag_from_views(tag_id, view_ids = nil, dissociate_all = false, config = {})
        if dissociate_all
          config["dissociateAll"] = true
        else
          config["viewIds"] = view_ids
        end
        endpoint = "#{@endpoint}/tags/#{tag_id}/views"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end
      # Returns the list of views associated with the specified tag.
      # @param tag_id [String] Id of the tag
      # @return [Array<Hash>] Tagged views list
      def get_tagged_views(tag_id)
        endpoint = "#{@endpoint}/tags/#{tag_id}/views"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["views"]
      end

      # Returns list of workspaces linked to the specified master workspace.
      # @return [Array<Hash>] Linked workspaces list
      def get_linked_workspaces
        endpoint = "#{@endpoint}/linkedworkspaces"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["linkedWorkspaces"]
      end
      # Returns list of organizations and workspaces that can be linked to the specified master workspace.
      # @return [Array<Hash>] Organizations with their linkable workspaces
      def get_linkable_workspaces
        endpoint = "#{@endpoint}/linkedworkspaces/linkable"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["orgs"]
      end
      # Returns the linking compatibility details for the specified client workspaces.
      # @param clients [Array<Hash>] Contains the client workspaces to be verified for linking compatibility
      # @param config [Hash] Additional control parameters
      # @return [Array<Hash>] Client workspace compatibility details
      def get_workspace_linking_compatibility(clients, config = {})
        config["clients"] = clients
        endpoint = "#{@endpoint}/linkedworkspaces/compatibility"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["clients"]
      end
      # Link the specified client workspaces to the master workspace.
      # @param clients [Array<Hash>] Contains the client workspaces to be linked with the master workspace
      # @param config [Hash] Additional control parameters
      def link_workspaces(clients, config = {})
        config["clients"] = clients
        endpoint = "#{@endpoint}/linkedworkspaces"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Unlink the client workspaces from the specified master workspace.
      # @param scope [String] Scope of the unlink operation
      # @param config [Hash] Additional control parameters
      def unlink_workspaces(scope, config = {})
        config["scope"] = scope
        endpoint = "#{@endpoint}/linkedworkspaces"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end
      # Sync the metadata of the master workspace to its linked client workspaces.
      # @param scope [String] Scope of the sync operation
      # @param config [Hash] Additional control parameters
      def sync_linked_workspaces(scope, config = {})
        config["scope"] = scope
        endpoint = "#{@endpoint}/linkedworkspaces/sync"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Returns the sync details of the specified linked workspaces.
      # @param sandbox_ids [Array<String>] Ids of the linked workspaces for which the sync details are fetched
      # @param config [Hash] Additional control parameters
      # @return [Array<Hash>] Linked workspace sync details
      def get_linked_workspace_sync_details(sandbox_ids, config = {})
        config["sandboxIds"] = sandbox_ids
        endpoint = "#{@endpoint}/linkedworkspaces/sync"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["workspaces"]
      end
      # Returns the backup configuration and the list of backups available for the specified workspace.
      # @return [Hash] Workspace backup details
      def get_workspace_backups
        endpoint = "#{@endpoint}/backups"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end
      # Trigger an instant backup for the specified workspace.
      # @param config [Hash] Additional control parameters
      # @return [Hash] Triggered backup details
      def backup_workspace_now(config = {})
        endpoint = "#{@endpoint}/backups"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Returns the status of the specified workspace backup.
      # @param backup_id [String] Id of the backup
      # @return [Hash] Backup status details
      def get_workspace_backup_status(backup_id)
        endpoint = "#{@endpoint}/backups/#{backup_id}/status"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end
      # Download the specified workspace backup.
      # @param backup_id [String] Id of the backup
      # @param file_path [String] Path of the file where the downloaded backup is to be stored
      # @param config [Hash] Additional control parameters
      def download_workspace_backup(backup_id, file_path, config = {})
        endpoint = "#{@endpoint}/backups/#{backup_id}/download"
        @ac.send_export_api_request(endpoint, config, @request_headers, file_path)
      end
      # Restore the specified workspace from the given backup.
      # @param backup_id [String] Id of the backup
      # @param confirm_restore [Boolean] Pass true to confirm that the existing workspace data can be overwritten
      # @param config [Hash] Additional control parameters
      # @return [Hash] Triggered restore details
      def restore_workspace_from_backup(backup_id, confirm_restore, config = {})
        config["confirmRestore"] = confirm_restore
        endpoint = "#{@endpoint}/backups/#{backup_id}/restore"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Returns the status of the specified workspace restore.
      # @param restore_id [String] Id of the restore
      # @return [Hash] Restore status details
      def get_workspace_restore_status(restore_id)
        endpoint = "#{@endpoint}/restores/#{restore_id}/status"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end
      # Create a dashboard in the specified workspace.
      # @param display_name [String] Name of the dashboard
      # @param layout [String] Layout configuration of the dashboard
      # @param config [Hash] Additional control parameters
      # @return [String] Created dashboard id
      def create_dashboard(display_name, layout, config = {})
        config["displayName"] = display_name
        config["layout"] = layout
        endpoint = "#{@endpoint}/dashboards"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["dashboardId"].to_s
      end
      # Update the specified dashboard in the workspace.
      # @param dashboard_id [String] Id of the dashboard
      # @param config [Hash] Contains the dashboard configurations to be updated
      def update_dashboard(dashboard_id, config = {})
        endpoint = "#{@endpoint}/dashboards/#{dashboard_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end
      # Returns the metadata of the specified dashboard.
      # @param dashboard_id [String] Id of the dashboard
      # @param config [Hash] Additional control parameters
      # @return [Hash] Dashboard configuration
      def get_dashboard_metadata(dashboard_id, config = {})
        endpoint = "#{@endpoint}/dashboards/#{dashboard_id}/metadata"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["dashboardConfig"]
      end
      # Returns the metadata of the specified report.
      # @param view_id [String] Id of the report
      # @return [Hash] Report configuration
      def get_report_metadata(view_id)
        endpoint = "#{@endpoint}/reports/#{view_id}/metadata"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["reportConfig"]
      end
      # Returns list of data alerts available in the specified workspace.
      # @return [Array<Hash>] Data alerts list
      def get_alerts_in_workspace
        endpoint = "#{@endpoint}/alerts"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["alerts"]
      end
      # Returns the configuration of the specified data alert.
      # @param alert_id [String] Id of the data alert
      # @return [Hash] Data alert configuration
      def get_alert_configuration(alert_id)
        endpoint = "#{@endpoint}/alerts/#{alert_id}"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end
      # Update the specified data alert in the workspace.
      # @param alert_id [String] Id of the data alert
      # @param alert_name [String] Name of the data alert
      # @param schedule_details [Hash] Contains the schedule configurations of the data alert
      # @param rules [Array<Hash>] Contains the rules to be evaluated by the data alert
      # @param config [Hash] Additional control parameters
      def update_alert(alert_id, alert_name, schedule_details, rules, config = {})
        config["alertName"] = alert_name
        config["scheduleDetails"] = schedule_details
        config["rules"] = rules
        endpoint = "#{@endpoint}/alerts/#{alert_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end
      # Delete the specified data alerts from the workspace.
      # @param alert_ids [Array<String>] Ids of the data alerts to be deleted
      # @param config [Hash] Additional control parameters
      def delete_alerts(alert_ids, config = {})
        config["alertIds"] = alert_ids
        endpoint = "#{@endpoint}/alerts"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end
      # Enable or disable the specified data alerts in the workspace.
      # @param alert_ids [Array<String>] Ids of the data alerts
      # @param enabled [Boolean] Pass true to enable the data alerts and false to disable them
      # @param config [Hash] Additional control parameters
      def change_alert_status(alert_ids, enabled, config = {})
        config["alertIds"] = alert_ids
        config["enabled"] = enabled
        endpoint = "#{@endpoint}/alerts/status"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end
      # Execute the specified data alert immediately.
      # @param alert_id [String] Id of the data alert
      # @param config [Hash] Additional control parameters
      def run_alert(alert_id, config = {})
        endpoint = "#{@endpoint}/alerts/#{alert_id}/execute"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Returns the execution events of the specified data alert.
      # @param alert_id [String] Id of the data alert
      # @param config [Hash] Additional control parameters
      # @return [Hash] Data alert events along with the page details
      def get_alert_events(alert_id, config = {})
        endpoint = "#{@endpoint}/alerts/#{alert_id}/events"
        @ac.send_api_request("GET", endpoint, config, @request_headers)
      end
      # Returns the access restriction settings configured for the specified workspace.
      # @return [Hash] Workspace access restriction settings
      def get_workspace_access_restrictions
        endpoint = "#{@security_controls_endpoint}/access-restrictions"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end
      # Update the access restriction settings of the specified workspace.
      # @param config [Hash] Contains the access restriction configurations to be updated
      def update_workspace_access_restrictions(config = {})
        endpoint = "#{@security_controls_endpoint}/access-restrictions"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

    end
    # ViewAPI contains view level operations.
    class ViewAPI
      def initialize(ac, org_id, workspace_id, view_id)
        @ac = ac
        @endpoint = "/restapi/v2/workspaces/#{workspace_id}/views/#{view_id}"
        @request_headers = { "ZANALYTICS-ORGID" => org_id }
      end

      # Rename a specified view in the workspace.
      # @param view_name [String] New name of the view
      # @param config [Hash] Additional control parameters
      def rename(view_name, config = {})
        config["viewName"] = view_name
        @ac.send_api_request("PUT", @endpoint, config, @request_headers)
      end

      # Delete a specified view in the workspace.
      # @param config [Hash] Additional control parameters
      def delete(config = {})
        @ac.send_api_request("DELETE", @endpoint, config, @request_headers)
      end

      # Copy a specified view within the workspace.
      # @param new_view_name [String] Name of the new view
      # @param config [Hash] Additional control parameters
      # @return [Integer] Created view ID
      def save_as(new_view_name, config = {})
        config["viewName"] = new_view_name
        endpoint = "#{@endpoint}/saveas"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["viewId"].to_i
      end

      # Copy formulas to another workspace or view.
      # @param formula_names [Array] Names of formulas
      # @param dest_workspace_id [String] Destination workspace ID
      # @param config [Hash] Additional control parameters
      # @param dest_org_id [String, nil] Optional destination org ID
      def copy_formulas(formula_names, dest_workspace_id, config = {}, dest_org_id = nil)
        config["formulaColumnNames"] = formula_names
        config["destWorkspaceId"] = dest_workspace_id
        endpoint = "#{@endpoint}/formulas/copy"
        headers = @request_headers.dup
        headers["ZANALYTICS-DEST-ORGID"] = dest_org_id if dest_org_id
        @ac.send_api_request("POST", endpoint, config, headers)
      end

      # Adds a specified view as favorite.
      def add_favorite
        endpoint = "#{@endpoint}/favorite"
        @ac.send_api_request("POST", endpoint, nil, @request_headers)
      end

      # Removes a specified view from favorites.
      def remove_favorite
        endpoint = "#{@endpoint}/favorite"
        @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
      end

      # Create similar reports based on a reference view.
      # @param ref_view_id [String]
      # @param folder_id [String]
      # @param config [Hash]
      def create_similar_views(ref_view_id, folder_id, config = {})
        config["referenceViewId"] = ref_view_id
        config["folderId"] = folder_id
        endpoint = "#{@endpoint}/similarviews"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Auto generate reports.
      # @param config [Hash]
      def auto_analyse(config = {})
        endpoint = "#{@endpoint}/autoanalyse"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Get user permissions for the view.
      # @return [Hash]
      def get_my_permissions
        endpoint = "#{@endpoint}/share/userpermissions"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["permissions"]
      end

      # Get the URL to access the view.
      # @param config [Hash]
      # @return [String]
      def get_view_url(config = {})
        endpoint = "#{@endpoint}/publish"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["viewUrl"]
      end

      # Get embed URL of the view.
      # @param config [Hash]
      # @return [String]
      def get_embed_url(config = {})
        endpoint = "#{@endpoint}/publish/embed"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["embedUrl"]
      end

      # Get private URL of the view.
      # @param config [Hash]
      # @return [String]
      def get_private_url(config = {})
        endpoint = "#{@endpoint}/publish/privatelink"
        response = @ac.send_api_request("GET", endpoint, config, @request_headers)
        response["privateUrl"]
      end

      # Create private URL for the view.
      # @param config [Hash]
      # @return [String]
      def create_private_url(config = {})
        endpoint = "#{@endpoint}/publish/privatelink"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["privateUrl"]
      end

      # Remove private access for the view.
      def remove_private_access
        endpoint = "#{@endpoint}/publish/privatelink"
        @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
      end

      # Make the view publicly accessible.
      # @param config [Hash]
      # @return [String]
      def make_view_public(config = {})
        endpoint = "#{@endpoint}/publish/public"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["publicUrl"]
      end

      # Remove public access for the view.
      def remove_public_access
        endpoint = "#{@endpoint}/publish/public"
        @ac.send_api_request("DELETE", endpoint, nil, @request_headers)
      end

      # Get publish configurations of the view.
      # @return [Hash]
      def get_publish_configurations
        endpoint = "#{@endpoint}/publish/config"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response
      end

      # Update publish configurations of the view.
      # @param config [Hash]
      def update_publish_configurations(config = {})
        endpoint = "#{@endpoint}/publish/config"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Add a column to the view.
      # @param column_name [String]
      # @param data_type [String]
      # @param config [Hash]
      # @return [Integer]
      def add_column(column_name, data_type, config = {})
        config["columnName"] = column_name
        config["dataType"] = data_type
        endpoint = "#{@endpoint}/columns"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["columnId"].to_i
      end

      # Hide columns in the view.
      # @param column_ids [Array]
      def hide_columns(column_ids)
        config = { "columnIds" => column_ids }
        endpoint = "#{@endpoint}/columns/hide"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Show hidden columns in the view.
      # @param column_ids [Array]
      def show_columns(column_ids)
        config = { "columnIds" => column_ids }
        endpoint = "#{@endpoint}/columns/show"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Adds a single row in the specified table.
      # @param column_values [Hash] Column name to value mapping.
      # @param config [Hash] Additional control parameters.
      # @return [Hash] Response containing column names and added row values.
      def add_row(column_values, config = {})
        config["columns"] = column_values
        endpoint = "#{@endpoint}/rows"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response
      end

      # Updates rows in the specified table.
      # @param column_values [Hash] Column name to updated value mapping.
      # @param criteria [String, nil] Criteria to filter rows for update.
      # @param config [Hash] Additional control parameters.
      # @return [Hash] Updated columns list and row count.
      def update_row(column_values, criteria, config = {})
        config["columns"] = column_values
        config["criteria"] = criteria unless criteria.nil?
        endpoint = "#{@endpoint}/rows"
        response = @ac.send_api_request("PUT", endpoint, config, @request_headers)
        response
      end

      # Deletes rows in the specified table.
      # @param criteria [String, nil] Criteria to filter rows for deletion.
      # @param config [Hash] Additional control parameters.
      # @return [String] Deleted row details.
      def delete_row(criteria, config = {})
        config["criteria"] = criteria unless criteria.nil?
        endpoint = "#{@endpoint}/rows"
        response = @ac.send_api_request("DELETE", endpoint, config, @request_headers)
        response["deletedRows"]
      end

      # Renames a specified column in the table.
      # @param column_id [String] ID of the column.
      # @param column_name [String] New column name.
      # @param config [Hash] Additional control parameters.
      def rename_column(column_id, column_name, config = {})
        config["columnName"] = column_name
        endpoint = "#{@endpoint}/columns/#{column_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Deletes a specified column in the table.
      # @param column_id [String] ID of the column.
      # @param config [Hash] Additional control parameters.
      def delete_column(column_id, config = {})
        endpoint = "#{@endpoint}/columns/#{column_id}"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Adds a lookup in the specified child table.
      # @param column_id [String] Child column ID.
      # @param ref_view_id [String] Parent table ID.
      # @param ref_column_id [String] Parent column ID.
      # @param config [Hash] Additional control parameters.
      def add_lookup(column_id, ref_view_id, ref_column_id, config = {})
        config["referenceViewId"] = ref_view_id
        config["referenceColumnId"] = ref_column_id
        endpoint = "#{@endpoint}/columns/#{column_id}/lookup"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Removes the lookup for the specified column in the table.
      # @param column_id [String] Column ID.
      # @param config [Hash] Additional control parameters.
      def remove_lookup(column_id, config = {})
        endpoint = "#{@endpoint}/columns/#{column_id}/lookup"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Auto generates reports for the specified column.
      # @param column_id [String] Column ID.
      # @param config [Hash] Additional control parameters.
      def auto_analyse_column(column_id, config = {})
        endpoint = "#{@endpoint}/columns/#{column_id}/autoanalyse"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Syncs data from the available data source for the view.
      # @param config [Hash] Additional control parameters.
      def refetch_data(config = {})
        endpoint = "#{@endpoint}/sync"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end

      # Returns last import details of the view.
      # @return [Hash] Last import details.
      def get_last_import_details
        endpoint = "#{@endpoint}/importdetails"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response
      end

      # Returns list of all formula columns for the table.
      # @return [Array<Hash>] Formula columns.
      def get_formula_columns
        endpoint = "#{@endpoint}/formulacolumns"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["formulaColumns"]
      end

      # Adds a formula column to the table.
      # @param formula_name [String] Name of the formula column.
      # @param expression [String] Formula expression.
      # @param config [Hash] Additional control parameters.
      # @return [String] Formula ID.
      def add_formula_column(formula_name, expression, config = {})
        config["formulaName"] = formula_name
        config["expression"] = expression
        endpoint = "#{@endpoint}/formulacolumns"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["formulaId"]
      end

      # Edits a formula column.
      # @param formula_id [String] Formula column ID.
      # @param expression [String] New formula expression.
      # @param config [Hash] Additional control parameters.
      def edit_formula_column(formula_id, expression, config = {})
        config["expression"] = expression
        endpoint = "#{@endpoint}/formulacolumns/#{formula_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Deletes a formula column.
      # @param formula_id [String] Formula column ID.
      # @param config [Hash] Additional control parameters.
      def delete_formula_column(formula_id, config = {})
        endpoint = "#{@endpoint}/formulacolumns/#{formula_id}"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Returns list of all aggregate formulas for the table.
      # @return [Array<Hash>] Aggregate formulas.
      def get_aggregate_formulas
        endpoint = "#{@endpoint}/aggregateformulas"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["aggregateFormulas"]
      end

      # Adds an aggregate formula to the table.
      # @param formula_name [String] Formula name.
      # @param expression [String] Formula expression.
      # @param config [Hash] Additional control parameters.
      # @return [String] Formula ID.
      def add_aggregate_formula(formula_name, expression, config = {})
        config["formulaName"] = formula_name
        config["expression"] = expression
        endpoint = "#{@endpoint}/aggregateformulas"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["formulaId"]
      end

      # Edits an aggregate formula.
      # @param formula_id [String] Formula ID.
      # @param expression [String] New formula expression.
      # @param config [Hash] Additional control parameters.
      def edit_aggregate_formula(formula_id, expression, config = {})
        config["expression"] = expression
        endpoint = "#{@endpoint}/aggregateformulas/#{formula_id}"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Deletes an aggregate formula.
      # @param formula_id [String] Formula ID.
      # @param config [Hash] Additional control parameters.
      def delete_aggregate_formula(formula_id, config = {})
        endpoint = "#{@endpoint}/aggregateformulas/#{formula_id}"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Returns the dependent views of this view.
      # @return [Array<Hash>] List of dependent views.
      def get_view_dependents
        endpoint = "#{@endpoint}/dependents"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["views"]
      end

      # Returns list of dependent views and formulas for the specified column.
      # @param column_id [String] The ID of the column
      # @return [Hash] Dependent details
      # @raise [ServerError] If the server received the request but did not process it
      # @raise [ParseError] If the response could not be parsed
      def get_column_dependents(column_id)
        endpoint = "#{@endpoint}/columns/#{column_id}/dependents"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response
      end

      # Updates the shared details of the specified view.
      # @param config [Hash] Contains the control parameters
      # @raise [ServerError] If the server received the request but did not process it
      # @raise [ParseError] If the response could not be parsed
      def update_shared_details(config = {})
        endpoint = "#{@endpoint}/share"
        @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Returns metadata details like columns present for the specified table.
      #
      # @return [Hash] Table metadata details
      # @raise [ServerError] If the server has received the request but did not process it
      # @raise [ParseError] If the client was unable to parse the response
      def get_table_metadata
        endpoint = "#{@endpoint}/metadata"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response
      end

      # Updates the column order of the current table.
      #
      # @param column_ids [Array<String>] List of column IDs in the new order
      # @param config [Hash] Additional control parameters
      # @raise [ServerError] If the server has received the request but did not process it
      # @raise [ParseError] If the client was unable to parse the response
      def reorder_columns(column_ids, config = {})
      config["columns"] = column_ids
      endpoint = "#{@endpoint}/columns/reorder"
      @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Sorts the data in the current table based on the specified columns.
      #
      # @param columns [Array<String>, nil] Column IDs to sort by
      # @param sort_order [Integer, nil] Sort order (1 = Ascending, 2 = Descending)
      # @param reset_sort [Boolean] Whether to reset existing sort configuration
      # @param config [Hash] Additional control parameters
      #
      # @raise [ServerError] If the server has received the request but did not process it
      # @raise [ParseError] If the client was unable to parse the response
      def sort_data_by_columns(columns = nil, sort_order = nil, reset_sort = false, config = {})
      if reset_sort
        config["resetSort"] = "true"
      else
        config["sortOrder"] = sort_order
        config["columns"]   = columns
      end

      endpoint = "#{@endpoint}/data/sort"
      @ac.send_api_request("PUT", endpoint, config, @request_headers)
      end

      # Returns the list of tags associated with the specified view.
      # @return [Array<Hash>] Tags list
      def get_view_tags
        endpoint = "#{@endpoint}/tags"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["tags"]
      end
      # Adds multiple tags to the specified view.
      # @param tag_ids [Array<String>] Tag ids to be associated with the view
      # @param config [Hash] Additional control parameters
      def add_tags_to_view(tag_ids, config = {})
        config["tagIds"] = tag_ids
        endpoint = "#{@endpoint}/tags"
        @ac.send_api_request("POST", endpoint, config, @request_headers)
      end
      # Removes multiple tags from the specified view.
      # @param tag_ids [Array<String>, nil] Tag ids to be dissociated. Not required when dissociate_all is true.
      # @param dissociate_all [Boolean] To dissociate all tags from the view
      # @param config [Hash] Additional control parameters
      def remove_tags_from_view(tag_ids = nil, dissociate_all = false, config = {})
        if dissociate_all
          config["dissociateAll"] = true
        else
          config["tagIds"] = tag_ids
        end
        endpoint = "#{@endpoint}/tags"
        @ac.send_api_request("DELETE", endpoint, config, @request_headers)
      end

      # Returns list of data alerts configured for the specified view.
      # @return [Array<Hash>] Data alerts list
      def get_alerts_in_view
        endpoint = "#{@endpoint}/alerts"
        response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
        response["alerts"]
      end
      # Create a data alert for the specified view.
      # @param alert_name [String] Name of the data alert
      # @param schedule_details [Hash] Contains the schedule configurations of the data alert
      # @param rules [Array<Hash>] Contains the rules to be evaluated by the data alert
      # @param config [Hash] Additional control parameters
      # @return [String] Created data alert id
      def create_alert(alert_name, schedule_details, rules, config = {})
        config["alertName"] = alert_name
        config["scheduleDetails"] = schedule_details
        config["rules"] = rules
        endpoint = "#{@endpoint}/alerts"
        response = @ac.send_api_request("POST", endpoint, config, @request_headers)
        response["alertId"].to_s
      end
      # Returns the view metadata that can be used while configuring a data alert for the specified view.
      # @return [Hash] View metadata for data alert configuration
      def get_view_metadata_for_alert
        endpoint = "#{@endpoint}/alerts/metadata"
        @ac.send_api_request("GET", endpoint, nil, @request_headers)
      end

end
# BulkAPI contains data operations.
class BulkAPI
  # Initializes the BulkAPI object.
  #
  # @param ac [Object] The API client instance.
  # @param org_id [String] The organization ID.
  # @param workspace_id [String] The workspace ID.
  def initialize(ac, org_id, workspace_id)
    @ac = ac
    @endpoint = "/restapi/v2/workspaces/#{workspace_id}"
    @bulk_endpoint = "/restapi/v2/bulk/workspaces/#{workspace_id}"
    @request_headers = { "ZANALYTICS-ORGID" => org_id }
  end

  # Imports data from a file to a new table.
  #
  # @param table_name [String] Name of the new table to be created.
  # @param file_type [String] Type of the file (e.g., "csv", "json").
  # @param auto_identify [String] Whether to auto-identify the file format ("true" or "false").
  # @param file_path [String] Local path to the import file.
  # @param config [Hash] Additional optional parameters.
  # @return [Hash] The response data from the API.
  def import_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
    endpoint = "#{@endpoint}/data"
    config["tableName"] = table_name
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    response = @ac.send_import_api_request(endpoint, config, @request_headers, file_path)
    response
  end

  # Imports data in batches to a new table asynchronously.
  #
  # @param table_name [String] Name of the new table to be created.
  # @param auto_identify [String] Whether to auto-identify the file format.
  # @param file_path [String] Path to the data file.
  # @param batch_size [Integer] Number of rows per batch.
  # @param config [Hash] Additional control parameters.
  # @param tool_config [Hash] Internal tool configuration.
  # @return [String] Job ID for the asynchronous batch import.
  def import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config = {}, tool_config = {})
    endpoint = "#{@bulk_endpoint}/data/batch"
    config["tableName"] = table_name
    config["autoIdentify"] = auto_identify
    response = @ac.send_batch_import_api_request(endpoint, config, @request_headers, file_path, batch_size, tool_config)
    response["jobId"]
  end

  # Imports raw data (as a string or byte array) to a new table.
  #
  # @param table_name [String] Name of the new table to be created.
  # @param file_type [String] Type of the raw data (e.g., "csv").
  # @param auto_identify [String] Whether to auto-identify format.
  # @param data [String] Raw data content.
  # @param config [Hash] Additional parameters.
  # @return [Hash] Import result from the API.
  def import_raw_data_in_new_table(table_name, file_type, auto_identify, data, config = {})
    endpoint = "#{@endpoint}/data"
    config["tableName"] = table_name
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    response = @ac.send_import_api_request(endpoint, config, @request_headers, nil, data)
    response
  end

  # Imports data to an existing view from a file.
  #
  # @param view_id [String] The ID of the target view.
  # @param import_type [String] Type of import: "APPEND", "TRUNCATEADD", or "UPDATEADD".
  # @param file_type [String] File format (e.g., "csv").
  # @param auto_identify [String] Whether to auto-identify the format.
  # @param file_path [String] Path to the input file.
  # @param config [Hash] Optional additional parameters.
  # @return [Hash] API response data.
  def import_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
    endpoint = "#{@endpoint}/views/#{view_id}/data"
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    config["importType"] = import_type
    response = @ac.send_import_api_request(endpoint, config, @request_headers, file_path)
    response
  end

  # Imports raw data to an existing view.
  #
  # @param view_id [String] ID of the target view.
  # @param import_type [String] Type of import (APPEND, etc.).
  # @param file_type [String] Format of the raw data.
  # @param auto_identify [String] Whether to auto-identify format.
  # @param data [String] Raw data content.
  # @param config [Hash] Additional parameters.
  # @return [Hash] API response data.
  def import_raw_data(view_id, import_type, file_type, auto_identify, data, config = {})
    endpoint = "#{@endpoint}/views/#{view_id}/data"
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    config["importType"] = import_type
    response = @ac.send_import_api_request(endpoint, config, @request_headers, nil, data)
    response
  end

  # Initiates asynchronous import of data into a new table.
  #
  # @param table_name [String] Target table name.
  # @param file_type [String] File format (e.g., "csv").
  # @param auto_identify [String] Whether to auto-detect file format.
  # @param file_path [String] Path to the data file.
  # @param config [Hash] Additional parameters.
  # @return [String] Job ID of the import operation.
  def import_bulk_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
    endpoint = "#{@bulk_endpoint}/data"
    config["tableName"] = table_name
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    response = @ac.send_import_api_request(endpoint, config, @request_headers, file_path)
    response["jobId"]
  end

  # Initiates asynchronous import of data into an existing view.
  #
  # @param view_id [String] Target view ID.
  # @param import_type [String] Type of import (APPEND, etc.).
  # @param file_type [String] File format.
  # @param auto_identify [String] Whether to auto-detect format.
  # @param file_path [String] Path to the file.
  # @param config [Hash] Additional parameters.
  # @return [String] Job ID.
  def import_bulk_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
    endpoint = "#{@bulk_endpoint}/views/#{view_id}/data"
    config["fileType"] = file_type
    config["autoIdentify"] = auto_identify
    config["importType"] = import_type
    response = @ac.send_import_api_request(endpoint, config, @request_headers, file_path)
    response["jobId"]
  end
  
  # Create a new table and import the data contained in the mentioned file into the created table.
  #
  # @param table_name [String] Name of the new table to be created.
  # @param auto_identify [String] Used to specify whether to auto identify the CSV format. Allowable values - true/false.
  # @param file_path [String] Path of the file to be imported.
  # @param batch_size [Integer] Number of lines per batch.
  # @param config [Hash] Contains any additional control parameters. Can be nil.
  # @param tool_config [Hash] Contains any additional control parameters for the library. Can be nil.
  # @return [String] Import job id
  # @raise [ServerError] If the server has received the request but did not process the request due to some error.
  # @raise [ParseError] If the server has responded but client was not able to parse the response.
  def import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config = {}, tool_config = {})
    endpoint = "#{@bulk_endpoint}/data/batch"
    config = {} unless config
    config["tableName"] = table_name
    config["autoIdentify"] = auto_identify
    response = @ac.send_batch_import_api_request(endpoint, config, @request_headers, file_path, batch_size, tool_config)
    response["jobId"]
  end

  # Asynchronously imports data to an existing view in batches.
  #
  # @param view_id [String] Target view ID.
  # @param import_type [String] Type of import.
  # @param auto_identify [String] Whether to auto-identify format.
  # @param file_path [String] File path for input.
  # @param batch_size [Integer] Number of rows per batch.
  # @param config [Hash] Additional options.
  # @param tool_config [Hash] Internal config for SDK tool.
  # @return [String] Job ID of the batch import.
  def import_data_as_batches(view_id, import_type, auto_identify, file_path, batch_size, config = {}, tool_config = {})
    endpoint = "#{@bulk_endpoint}/views/#{view_id}/data/batch"
    config["importType"] = import_type
    config["autoIdentify"] = auto_identify
    response = @ac.send_batch_import_api_request(endpoint, config, @request_headers, file_path, batch_size, tool_config)
    response["jobId"]
  end

  # Retrieves the details of an import job by its ID.
  #
  # @param job_id [String] The job ID to query.
  # @return [Hash] Job details and status.
  def get_import_job_details(job_id)
    endpoint = "#{@bulk_endpoint}/importjobs/#{job_id}"
    response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
    response
  end

  # Exports the specified view's data to a file.
  #
  # @param view_id [String] ID of the view to export.
  # @param response_format [String] Format in which to export the data.
  # @param file_path [String] Path to the file where exported data will be stored.
  # @param config [Hash] Optional configuration parameters.
  # @raise [ServerError] If the server receives but fails to process the request.
  # @raise [ParseError] If the response cannot be parsed.
  def export_data(view_id, response_format, file_path, config = {})
    endpoint = "#{@endpoint}/views/#{view_id}/data"
    config['responseFormat'] = response_format
    @ac.send_export_api_request(endpoint, config, @request_headers, file_path)
  end

  # Initiates an asynchronous export for the given view.
  #
  # @param view_id [String] ID of the view to be exported.
  # @param response_format [String] Format of the exported data (e.g., "csv", "json").
  # @param config [Hash] Additional optional parameters.
  # @return [String] Job ID of the export operation.
  # @raise [StandardError] If the server fails to process or response is invalid.
  def initiate_bulk_export(view_id, response_format, config = {})
    endpoint = "#{@bulk_endpoint}/views/#{view_id}/data"
    config["responseFormat"] = response_format
    response = @ac.send_api_request("GET", endpoint, config, @request_headers)
    response["jobId"]
  end

  # Initiates an asynchronous export using a SQL query.
  #
  # @param sql_query [String] SQL query to run for export.
  # @param response_format [String] Format of the exported data.
  # @param config [Hash] Additional control parameters.
  # @return [String] Job ID of the export task.
  # @raise [StandardError] On server error or invalid response.
  def initiate_bulk_export_using_sql(sql_query, response_format, config = {})
    endpoint = "#{@bulk_endpoint}/data"
    config["responseFormat"] = response_format
    config["sqlQuery"] = sql_query
    response = @ac.send_api_request("GET", endpoint, config, @request_headers)
    response["jobId"]
  end

  # Retrieves details of a specific export job.
  #
  # @param job_id [String] The export job ID.
  # @return [Hash] Export job metadata and status.
  # @raise [StandardError] If the request fails or response is invalid.
  def get_export_job_details(job_id)
    endpoint = "#{@bulk_endpoint}/exportjobs/#{job_id}"
    response = @ac.send_api_request("GET", endpoint, nil, @request_headers)
    response
  end

  # Downloads the exported data for a given job ID.
  #
  # @param job_id [String] ID of the export job to download.
  # @param file_path [String] Path to save the exported file.
  # @return [nil]
  # @raise [StandardError] If the download fails.
  def export_bulk_data(job_id, file_path)
    endpoint = "#{@bulk_endpoint}/exportjobs/#{job_id}/data"
    @ac.send_export_api_request(endpoint, nil, @request_headers, file_path)
  end
end

# Custom error classes
class ServerError < StandardError
  attr_reader :response_content, :error_code, :is_oauth_error
  def initialize(response_content, is_oauth_error=false, error_code=nil)
    @response_content = response_content
    @is_oauth_error = is_oauth_error
    @error_code = error_code
    super(response_content)
  end
end

class ParseError < StandardError
end
