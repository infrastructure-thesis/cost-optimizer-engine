"""Calculate the cost difference between Terraform plans."""
import json
from dataclasses import dataclass

@dataclass
class ResourceCostChange:
    """Represents the cost change of a resource."""
    resource_address: str
    before_monthly: float
    after_monthly: float
    delta_monthly: float
    annual_impact: float
    
class TerraformCostDiff:
    """Calculate cost changes from Terraform plans."""
    
    # Simplified AWS pricing (normally from pricing API)
    PRICING = {
        "t3.micro": 0.0116,
        "t3.small": 0.0232,
        "t3.medium": 0.0464,
        "t3.large": 0.0928,
        "t3.xlarge": 0.1856,
        "t3.2xlarge": 0.3712,
        "db.t3.small": 0.017,
        "db.t3.medium": 0.034,
        "db.t3.large": 0.068,
        "db.r6i.2xlarge": 1.64,
    }
    
    def parse_tf_plan(self, tf_plan: dict) -> list:
        """Parse Terraform plan JSON."""
        changes = []
        
        for resource in tf_plan.get("resource_changes", []):
            if resource["change"]["actions"] == ["no-op"]:
                continue
            
            change = self.analyze_resource_change(resource)
            if change:
                changes.append(change)
                
        return changes
    
    def analyze_resource_change(self, resource: dict) -> ResourceCostChange | None:
        """Analyze single resource change."""
        resource_type = resource["type"]
        if resource_type not in ["aws_instance", "aws_db_instance"]:
            return None
    
        address = resource["address"]
        actions = resource["change"]["actions"]
    
        # For creation: before = $0, after = new cost
        # For deletion: before = old cost, after = $0
        # For modification: before = old cost, after = new cost
    
        before_cost = self.get_resource_cost(resource, "before")
        after_cost = self.get_resource_cost(resource, "after")
    
        # If creation, treat before as 0
        if before_cost is None and after_cost is not None:
            before_cost = 0.0
    
        # If deletion, treat after as 0
        if after_cost is None and before_cost is not None:
            after_cost = 0.0
    
        # If still can't determine, skip
        if before_cost is None or after_cost is None:
            return None
    
        return ResourceCostChange(
            resource_address=address,
            before_monthly=before_cost,
            after_monthly=after_cost,
            delta_monthly=after_cost - before_cost,
            annual_impact=(after_cost - before_cost) * 12,
        )
        
    def get_resource_cost(self, resource: dict, stage: str) -> float | None:
        """Get monthly cost for resource at given stage."""
        data = resource["change"].get(stage)
        if data is None:
            return None
        
        # Extract instance type
        instance_type = data.get("instance_type") or data.get("instance_class")
        if not instance_type:
            return None
        
        # Get hourly rate
        hourly_rate = self.PRICING.get(instance_type)
        if hourly_rate is None:
            return None
        
        # Convert to monthly (730 hours/month)
        return hourly_rate * 730
    
    def generate_markdown_comment(self, changes: list) -> str:
        """Generate PR comment in Markdown."""
        if not changes:
            return "✅ No cost impact detected"
    
        total_delta = sum(c.delta_monthly for c in changes)
        total_annual = sum(c.annual_impact for c in changes)
    
        md = "## 💰 Cost Impact Analysis\n\n"
        md += f"**Total monthly impact:** ${total_delta:,.2f}\n"
        md += f"**Total annual impact:** ${total_annual:,.2f}\n\n"
        md += "### Resource Changes\n"
    
        for change in changes:
            md += f"\n**{change.resource_address}**\n"
            md += f"- Before: ${change.before_monthly:,.2f}/month\n"
            md += f"- After: ${change.after_monthly:,.2f}/month\n"
            md += f"- Delta: ${change.delta_monthly:+,.2f}/month\n"
            md += f"- Annual: ${change.annual_impact:+,.2f}\n"
    
        if total_delta > 0:
            md += "\n⚠️ **Cost increase detected.**\n"
        elif total_delta < 0:
            md += f"\n✅ **Cost reduction.** Saves ${abs(total_delta):,.2f}/month.\n"
    
        return md
 