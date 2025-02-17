variable "cloud_run_service_name" {
  type        = string
  description = "the name of cloud run service upon deployment"
  default     = "explore-assistant-api"
}

variable "deployment_region" {
  type        = string
  description = "Region to deploy the Cloud Run service. Example: us-central1"
  default     = "us-southeast1"
}

variable "project_id" {
  type = string
}

variable "image" {
  description = "The full path to image on your Google artifacts repo"
  type        = string
}


variable "explore-assistant-cr-oauth-client-id" {
  type        = string
  description = "GCP Client ID for cloud run to perform oauth verifications."
}

variable "explore-assistant-cr-sa-id" {
  type = string
  description = "service account for cloud run to use & make vertexai requests."
}

resource "google_service_account" "explore_assistant_sa" {
  account_id   = var.explore-assistant-cr-sa-id
  display_name = "Looker Explore Assistant Cloud Run SA"
}

resource "google_project_iam_member" "iam_permission_looker_aiplatform" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = format("serviceAccount:%s", google_service_account.explore_assistant_sa.email)
}
resource "google_project_iam_member" "iam_permission_bq_user" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = format("serviceAccount:%s", google_service_account.explore_assistant_sa.email)
}
resource "google_project_iam_member" "iam_permission_bq_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = format("serviceAccount:%s", google_service_account.explore_assistant_sa.email)
}

resource "google_cloud_run_service" "default" {
  name     = var.cloud_run_service_name
  location = var.deployment_region
  project  = var.project_id

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
    spec {
      service_account_name = google_service_account.explore_assistant_sa.email
      containers {
        image = "${var.image}"
        resources {
          limits = {
            memory = "4Gi"
            cpu    = "1000m"
          }
        }
        env {
          name  = "OAUTH_CLIENT_ID"
          value = var.explore-assistant-cr-oauth-client-id
        }
        env {
          name  = "REGION_NAME"
          value = var.deployment_region
        }
        env {
          name  = "PROJECT_NAME"
          value = var.project_id
        }
      }
    }
  }



  traffic {
    percent         = 100
    latest_revision = true
  }
}

### IAM permissions for Cloud Run (public access)
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.default.location
  project  = google_cloud_run_service.default.project
  service  = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "cloud_run_uri" {
  value = google_cloud_run_service.default.status[0].url
}

output "cloud_run_data" {
  value = google_cloud_run_service.default
}
