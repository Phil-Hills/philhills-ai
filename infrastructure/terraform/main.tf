provider "google" {
  project = var.project_id
  region  = "us-central1"
}

resource "google_iam_workload_identity_pool" "magnolia_pool" {
  workload_identity_pool_id = "magnolia-pool"
  display_name              = "Magnolia Lab Pool"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.magnolia_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account" "sentinel_agent" {
  account_id   = "sentinel-agent"
  display_name = "Sentinel Reputation Guard"
}

resource "google_service_account_iam_member" "wif_binding" {
  service_account_id = google_service_account.sentinel_agent.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.magnolia_pool.name}/attribute.repository/${var.github_repo}"
}

resource "google_project_iam_member" "ai_platform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.sentinel_agent.email}"
}
