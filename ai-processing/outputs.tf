output "lambda_function_name" {
  description = "Name of the AI processor Lambda function"
  value       = aws_lambda_function.ai_processor.function_name
}

output "lambda_function_arn" {
  description = "ARN of the AI processor Lambda function"
  value       = aws_lambda_function.ai_processor.arn
}