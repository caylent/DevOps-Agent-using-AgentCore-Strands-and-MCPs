# AI-Powered Processing Stack using Strands SDK and Bedrock
# Deploys intelligent VM processing with AI-powered recommendations

data "archive_file" "ai_lambda" {
  type        = "zip"
  output_path = "${path.module}/ai_lambda.zip"
  excludes    = ["__pycache__", "*.pyc", ".pytest_cache", "tests/"]
  
  source {
    content = templatefile("${path.module}/optimized_processor.py", {})
    filename = "optimized_processor.py"
  }
  
  source {
    content = file("${path.module}/requirements.txt")
    filename = "requirements.txt"
  }
  
  dynamic "source" {
    for_each = fileset("${path.module}/tools", "**/*")
    content {
      content  = file("${path.module}/tools/${source.value}")
      filename = "tools/${source.value}"
    }
  }
}

resource "aws_cloudwatch_log_group" "ai_lambda" {
  name              = "/aws/lambda/${var.project_id}-ai-processor"
  retention_in_days = 7
  tags              = var.default_tags
}

resource "aws_lambda_function" "ai_processor" {
  filename         = data.archive_file.ai_lambda.output_path
  function_name    = "${var.project_id}-ai-processor"
  role            = var.lambda_execution_role_arn
  handler         = "optimized_processor.sync_handler"
  description     = "AI-powered VM to EC2 processing using Strands SDK and Bedrock"
  
  source_code_hash = data.archive_file.ai_lambda.output_base64sha256
  runtime          = "python3.11"
  timeout          = 900
  memory_size      = 1024

  # Performance optimizations for AI workloads
  reserved_concurrent_executions = 5  # Lower concurrency for AI processing

  environment {
    variables = {
      DYNAMODB_TABLE         = var.dynamodb_table_name
      BEDROCK_REGION         = var.bedrock_region
      DEBUG_MODE             = "false"
      MAX_WORKERS            = "10"
      SINK_TYPE              = "s3"
      ANALYTICS_TYPE         = "dynamodb"
      LLM_TYPE               = "bedrock"
      
      # AI-specific settings
      BEDROCK_MODEL_ID       = "us.anthropic.claude-sonnet-4-20250514-v1:0"
      
      # Performance settings
      PYTHONPATH             = "/opt/python"
      PYTHONIOENCODING       = "utf-8"
    }
  }

  # Enable X-Ray tracing for observability
  tracing_config {
    mode = "Active"
  }

  # Configure dead letter queue for failed invocations
  dead_letter_config {
    target_arn = aws_sqs_queue.ai_processor_dlq.arn
  }

  depends_on = [
    aws_cloudwatch_log_group.ai_lambda,
  ]

  tags = merge(var.default_tags, { 
    Name           = "${var.project_id}-ai-processor"
    Type           = "AI-Processing"
    ProcessingType = "AI-Powered"
    Runtime        = "python3.11"
    AI_Provider    = "Bedrock"
  })
}

# Dead Letter Queue for failed invocations
resource "aws_sqs_queue" "ai_processor_dlq" {
  name                      = "${var.project_id}-ai-processor-dlq"
  message_retention_seconds = 1209600  # 14 days
  
  tags = merge(var.default_tags, {
    Name      = "${var.project_id}-ai-processor-dlq"
    Type      = "DeadLetterQueue"
    Component = "ai-processing"
  })
}

# CloudWatch Alarms for monitoring AI processing
resource "aws_cloudwatch_metric_alarm" "ai_processor_errors" {
  alarm_name          = "${var.project_id}-ai-processor-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "3"  # Lower threshold for AI processing
  alarm_description   = "This metric monitors AI processor errors"
  alarm_actions       = []

  dimensions = {
    FunctionName = aws_lambda_function.ai_processor.function_name
  }

  tags = var.default_tags
}

resource "aws_cloudwatch_metric_alarm" "ai_processor_duration" {
  alarm_name          = "${var.project_id}-ai-processor-duration"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Average"
  threshold           = "750000"  # 12.5 minutes (close to 15 min limit)
  alarm_description   = "This metric monitors AI processor execution duration"
  alarm_actions       = []

  dimensions = {
    FunctionName = aws_lambda_function.ai_processor.function_name
  }

  tags = var.default_tags
}