# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "zoho_analytics_client"
  spec.version       = "2.9.0"
  spec.authors       = ["Zoho Analytics"]
  spec.email         = ["support@zohoanalytics.com"]

  spec.summary       = "Ruby SDK for Zoho Analytics API"
  spec.description   = "A Ruby client library for Zoho Analytics API. Supports OAuth 2.0 authentication with encrypted token storage. Provides API access for organizations, workspaces, data import/export, and more."
  spec.homepage      = "https://www.zoho.com/analytics/"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 2.0.0"

  spec.metadata = {
    "homepage_uri" => spec.homepage,
    "documentation_uri" => "https://www.zoho.com/analytics/api/"
  }

  # Specify which files should be added to the gem when it is released.
  spec.files = ["lib/zoho_analytics_client.rb"]
  spec.require_paths = ["lib"]
end

