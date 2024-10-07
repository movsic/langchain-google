module "cloudbuild" {
  source = "./../../../../../terraform/cloudbuild"

  library                    = "community"
  project_id                 = var.project_id
  cloudbuildv2_repository_id = "projects/${var.project_id}/locations/us-central1/connections/langchain-google-connection/repositories/langchain-google-repository"
  cloudbuild_env_vars = {
    DATA_STORE_ID  = google_discovery_engine_data_store.data_store.id
    IMAGE_GCS_PATH = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    PROCESSOR_NAME = google_document_ai_processor.docai_layout_parser_processor.id
  }
  cloudbuild_secret_vars = {
    GOOGLE_API_KEY = "projects/${var.project_id}/secrets/google_api_key_secret/versions/latest"
    GOOGLE_CSE_ID  = "projects/${var.project_id}/secrets/google_cse_id_secret/versions/latest"
  }
}

resource "google_document_ai_processor" "docai_layout_parser_processor" {
  location     = "us"
  display_name = "docai_layout_parser_processor"
  type         = "LAYOUT_PARSER_PROCESSOR"
}

resource "google_discovery_engine_data_store" "data_store" {
  project           = var.project_id
  location          = "global"
  data_store_id     = "data-store"
  display_name      = "data-store"
  industry_vertical = "GENERIC"
  content_config    = "NO_CONTENT"
}