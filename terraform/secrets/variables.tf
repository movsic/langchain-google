variable "project_id" {
  type        = string
  description = "Project id, references existing project."
}

variable "prefix" {
  type        = string
  default     = "langchain-google"
  description = ""
}

variable "github_oauth_token" {
  type        = string
  description = "Github oauth token. https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github"
}

variable "google_api_key" {
  type        = string
  description = "Google api key. https://cloud.google.com/docs/authentication/api-keys#create"
}

variable "google_cse_id" {
  type        = string
  description = "Google CSE id. https://programmablesearchengine.google.com/controlpanel/all"
}