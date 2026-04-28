# ...................2. AgentCore Observability (Metrics, Logs and Traces).................
.....Uses OpenTelemetry library (open source) - aws-opentelemetry-distro (ADOT) - (https://opentelemetry.io/docs/collector distributions/) -----

# Step 1 - Add opentelemetry-distro in requirements.txt 
# Step 2 - Add opentelemetry-distro in Docker File
# Step 3 - Application Signals (APM) and choose Transaction search --- > Enable Transaction Search (toggle it ON)  -- aws/spans
# Step 4 - Enable Model invocation Logging
# Step 5 - Build the image and push to repo
# Step 6 - Update the AgentCore Runtime Configuration from Console
# Step 7 - Add IAM Permissions to the Role used by the AgentCore Runtime
# Step 8 - Wait 5-10 minutes for changes to take effect

# =============================================================================
# OpenTelemetry Configuration for AWS CloudWatch GenAI Observability - Agents not hosted on Amazon Bedrock AgentCore Runtime,
# =============================================================================

# AWS OpenTelemetry Distribution
OTEL_PYTHON_DISTRO=aws_distro
OTEL_PYTHON_CONFIGURATOR=aws_configurator

# Export Protocol
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_TRACES_EXPORTER=otlp

# CloudWatch Integration (uncomment and configure as needed)
OTEL_EXPORTER_OTLP_LOGS_HEADERS=x-aws-log-group=agents/strands-agent-logs,x-aws-log-stream=default,x-aws-metric-namespace=agents

# Service Identification
OTEL_RESOURCE_ATTRIBUTES=service.name=agentic-travel-strands

# Enable Agent Observability
AGENT_OBSERVABILITY_ENABLED=true

Runtime Metrics - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-runtime-metrics.html

