# Example: EC2 right-sizing
# Before: t3.2xlarge running at 8% CPU
# After: t3.large (75% cost reduction)

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.large"  # Changed from t3.2xlarge

  tags = {
    Name = "web-server"
  }
}

# Cost impact:
# Before: t3.2xlarge = $0.3712/hr = $271/month
# After: t3.large = $0.0928/hr = $68/month
# Savings: $203/month = $2,436/year
