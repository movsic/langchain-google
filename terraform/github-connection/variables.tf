variable "project_id" {
  type        = string
  description = "Project id, references existing project."
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Region for the created resources."
}

variable "prefix" {
  type        = string
  default     = "langchain-google"
  description = "Resources name prefix."
}

variable "github_oauth_token_secret_id" {
  type        = string
  description = "Gcp secret id containing github oauth token."
}

variable "langchain_github_repo" {
  type        = string
  description = "Langchain github repo."
  default     = "https://github.com/langchain-ai/langchain-google.git"
}

variable "github_app_installation_id" {
  type        = string
  description = "Your installation ID can be found in the URL of your Cloud Build GitHub App. In the following URL, https://github.com/settings/installations/1234567, the installation ID is the numerical value 1234567."
}