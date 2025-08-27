variable "project_id" {
  type        = string
  description = "Project identifier"
}

variable "default_tags" {
  type        = map(string)
  description = "Default tags for resources"
}

variable "lambda_execution_role_arn" {
  type        = string
  description = "ARN of the Lambda execution role"
}

variable "dynamodb_table_name" {
  type        = string
  description = "Name of the central DynamoDB table"
}

variable "bedrock_region" {
  type        = string
  description = "AWS region for Bedrock"
  default     = "us-east-1"
}