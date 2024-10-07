variable "project_id" {
  type        = string
  description = "Project id, references existing project."
}

variable "library" {
  type        = string
  description = "Langchain-google library. Changes in this library will trigger cloud build job."
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

variable "cloudbuildv2_repository_id" {
  type        = string
  description = "Cloud build repository id."
}

variable "poetry_version" {
  type        = string
  default     = "1.7.1"
  description = "Poetry version."
}

variable "python_version" {
  type        = string
  default     = "3.11"
  description = "Python version."
}

variable "cloudbuild_env_vars" {
  type        = map(string)
  description = "Map of env vars needed for the cloud build. Format: VAR_NAME=VAR_VALUE"
}

variable "cloudbuild_secret_vars" {
  type        = map(string)
  description = "Map of gcp secret variables needed for the cloud build. Format: VAR_NAME=SECRET_ID"
}