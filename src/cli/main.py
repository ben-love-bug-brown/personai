"""
PersonAI CLI Entry Point

Command-line interface for PersonAI.
"""

import click
import json
from datetime import datetime

from ..revenue import create_orchestrator
from ..revenue.base import RevenueModel, RevenueConfig


@click.group()
def cli():
    """PersonAI - Your autonomous AI partner"""
    pass


@cli.command()
@click.argument("message")
def chat(message: str):
    """Chat with PersonAI"""
    click.echo(f"You: {message}")
    click.echo("PersonAI: [Chat functionality coming soon]")


@cli.command()
def status():
    """Check PersonAI status"""
    orchestrator = create_orchestrator()
    status = orchestrator.get_status()
    
    click.echo("=" * 50)
    click.echo("PersonAI Status")
    click.echo("=" * 50)
    click.echo(f"Total Revenue: ${status['total_revenue']:.2f}")
    click.echo(f"Active Models: {status['enabled_models']}/{status['total_models']}")
    click.echo()
    click.echo("Revenue Models:")
    click.echo("-" * 50)
    
    for name, model_status in status["models"].items():
        enabled = "✓" if model_status["enabled"] else "✗"
        click.echo(f"  {enabled} {name}")
        click.echo(f"     Status: {model_status['status']}")
        click.echo(f"     Revenue: ${model_status['total_revenue']:.2f}")
        click.echo(f"     Allocation: {model_status['allocation']:.0f}%")
        click.echo()


@cli.command()
def revenue():
    """Generate revenue from all enabled models"""
    orchestrator = create_orchestrator()
    
    click.echo("Running revenue generation cycle...")
    results = orchestrator.execute_all()
    
    click.echo("=" * 50)
    click.echo("Revenue Generation Results")
    click.echo("=" * 50)
    
    total = 0.0
    for result in results:
        status_icon = "✓" if result.success else "✗"
        click.echo(f"{status_icon} {result.model}: ${result.amount:.2f}")
        if result.error:
            click.echo(f"   Error: {result.error}")
        total += result.amount
    
    click.echo("-" * 50)
    click.echo(f"Total: ${total:.2f}")


@cli.command()
@click.argument("model_name")
def run_model(model_name: str):
    """Run a specific revenue model"""
    orchestrator = create_orchestrator()
    
    click.echo(f"Running {model_name}...")
    result = orchestrator.execute_model(model_name)
    
    if result:
        status_icon = "✓" if result.success else "✗"
        click.echo(f"{status_icon} Result: ${result.amount:.2f}")
        if result.details:
            click.echo("Details:")
            for key, value in result.details.items():
                click.echo(f"  {key}: {value}")
    else:
        click.echo(f"Model {model_name} not found")


@cli.command()
def report():
    """Generate revenue report"""
    orchestrator = create_orchestrator()
    report = orchestrator.get_report()
    
    click.echo("=" * 50)
    click.echo("Revenue Report")
    click.echo("=" * 50)
    click.echo(f"Generated: {report.timestamp.isoformat()}")
    click.echo(f"Total Revenue: ${report.total_revenue:.2f}")
    click.echo(f"Active Models: {report.active_models}")
    click.echo()
    click.echo("Summary:")
    click.echo(json.dumps(report.summary, indent=2))


@cli.command()
@click.argument("model_name")
def enable_model(model_name: str):
    """Enable a revenue model"""
    orchestrator = create_orchestrator()
    
    if model_name in orchestrator.models:
        orchestrator.allocation[model_name] = 20.0
        orchestrator.models[model_name].config.enabled = True
        orchestrator.models[model_name].config.allocation = 20.0
        orchestrator._save_config()
        click.echo(f"Enabled {model_name}")
    else:
        click.echo(f"Model {model_name} not found")


@cli.command()
@click.argument("model_name")
def disable_model(model_name: str):
    """Disable a revenue model"""
    orchestrator = create_orchestrator()
    
    if model_name in orchestrator.models:
        orchestrator.allocation[model_name] = 0.0
        orchestrator.models[model_name].config.enabled = False
        orchestrator.models[model_name].config.allocation = 0.0
        orchestrator._save_config()
        click.echo(f"Disabled {model_name}")
    else:
        click.echo(f"Model {model_name} not found")


if __name__ == "__main__":
    cli()
