"""Test Terraform cost diff calculation."""
import pytest
from src.terraform_plugin.cost_diff import TerraformCostDiff

@pytest.fixture
def calculator():
    return TerraformCostDiff()

def test_parse_empty_plan(calculator):
    plan = {"resource_changes": []}
    changes = calculator.parse_tf_plan(plan)
    assert changes == []

def test_parse_ec2_creation(calculator):
    """Test parsing EC2 creation."""
    plan = {
        "resource_changes": [
            {
                "type": "aws_instance",
                "address": "aws_instance.web",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {"instance_type": "t3.medium"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    assert len(changes) == 1
    assert changes[0].before_monthly == 0.0

def test_ec2_cost_calculation(calculator):
    """Test cost calculation for EC2."""
    plan = {
        "resource_changes": [
            {
                "type": "aws_instance",
                "address": "aws_instance.web",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {"instance_type": "t3.large"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    # t3.large = 0.0928/hr * 730 hrs/month = 67.744
    assert changes[0].after_monthly == pytest.approx(67.744, abs=0.01)

def test_rds_cost_calculation(calculator):
    """Test cost calculation for RDS."""
    plan = {
        "resource_changes": [
            {
                "type": "aws_db_instance",
                "address": "aws_db_instance.prod",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {"instance_class": "db.t3.medium"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    # db.t3.medium = 0.034/hr * 730 = 24.82
    assert changes[0].after_monthly == pytest.approx(24.82, abs=0.01)

def test_cost_diff_positive(calculator):
    plan = {
        "resource_changes": [
            {
                "type": "aws_instance",
                "address": "aws_instance.web",
                "change": {
                    "actions": ["modify"],
                    "before": {"instance_type": "t3.small"},
                    "after": {"instance_type": "t3.large"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    assert changes[0].delta_monthly > 0

def test_cost_diff_negative(calculator):
    plan = {
        "resource_changes": [
            {
                "type": "aws_instance",
                "address": "aws_instance.web",
                "change": {
                    "actions": ["modify"],
                    "before": {"instance_type": "t3.large"},
                    "after": {"instance_type": "t3.small"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    assert changes[0].delta_monthly < 0

def test_markdown_comment_generation(calculator):
    """Test Markdown comment generation."""
    plan = {
        "resource_changes": [
            {
                "type": "aws_instance",
                "address": "aws_instance.web",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {"instance_type": "t3.medium"}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    comment = calculator.generate_markdown_comment(changes)
    assert "Cost Impact Analysis" in comment
    assert "$" in comment

def test_markdown_comment_no_changes(calculator):
    """Test Markdown comment for no changes."""
    plan = {"resource_changes": []}
    changes = calculator.parse_tf_plan(plan)
    comment = calculator.generate_markdown_comment(changes)
    assert "No cost" in comment

def test_unsupported_resource_type(calculator):
    plan = {
        "resource_changes": [
            {
                "type": "aws_s3_bucket",
                "address": "aws_s3_bucket.data",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {}
                }
            }
        ]
    }
    changes = calculator.parse_tf_plan(plan)
    assert len(changes) == 0
    