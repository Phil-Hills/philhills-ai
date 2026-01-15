variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "github_repo" {
  description = "The GitHub repository (Formatted as Organization/Repo)"
  type        = string
  default     = "Phil-Hills/philhills-ai"
}
