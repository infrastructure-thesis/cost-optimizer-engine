# Example: RDS with Reserved Instance'
# Saves 40% vs on-demand

resource "aws_db_instance" "prod" {
  allocated_storage   = 100
  engine              = "postgre"
  engine_version      = "15.3"
  instance_class      = "db.t3.medium"  # Apply 1-year RI for 40% discount
  username            = "admin"
  password            = random_password.db_password.result
  skip_final_snapshot = false

  tags = {
    Name = "prod-database"
  }
}

# Cost impact:
# On-demand: db.t3.medium = $0.034/hr = $24.82/month
# With 1-year RI: $14.89/month (40% discount)
# Savings: $9.93/month = $119/year
