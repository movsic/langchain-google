module "cloudbuild" {
  source = "./../../../../../terraform/cloudbuild"

  library                    = "genai"
  project_id                 = var.project_id
  cloudbuildv2_repository_id = "projects/${var.project_id}/locations/us-central1/connections/langchain-google-connection/repositories/langchain-google-repository"
  cloudbuild_env_vars = {
  }
  cloudbuild_secret_vars = {
    GOOGLE_API_KEY = "projects/${var.project_id}/secrets/google_api_key_secret/versions/latest"
  }
}