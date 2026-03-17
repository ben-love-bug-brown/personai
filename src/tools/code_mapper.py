"""
Code-to-Roadmap Mapper
Extracts functions/classes from codebase and cross-references with roadmap.
Exposes via zo.space API for the native bridge.
"""

import ast
import json
import os
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path("/home/workspace/personai")
ROADMAP_FILE = PROJECT_ROOT / "data" / "roadmap.json"


def load_roadmap() -> dict[str, Any]:
    """Load the roadmap JSON."""
    with open(ROADMAP_FILE) as f:
        return json.load(f)


def extract_functions_and_classes(filepath: Path) -> dict[str, Any]:
    """Extract all functions and classes from a Python file."""
    if not filepath.exists():
        return {"functions": [], "classes": [], "imports": []}
    
    with open(filepath) as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"functions": [], "classes": [], "imports": [], "parse_error": str(e)}
    
    functions = []
    classes = []
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node),
                "decorators": [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
            })
        elif isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "docstring": ast.get_docstring(node),
                "methods": methods,
                "subclasses": [c.name for c in node.body if isinstance(c, ast.ClassDef)]
            })
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            else:
                imports.append(node.module)
    
    return {"functions": functions, "classes": classes, "imports": imports}


def scan_src_directory(src_dir: Path = PROJECT_ROOT / "src") -> dict[str, Any]:
    """Scan all Python files in src/ directory."""
    results = {}
    
    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        rel_path = py_file.relative_to(PROJECT_ROOT)
        module_name = str(rel_path).replace("/", ".").replace(".py", "")
        
        results[str(rel_path)] = {
            "module": module_name,
            "path": str(py_file),
            **extract_functions_and_classes(py_file)
        }
    
    return results


def build_file_to_roadmap_mapping() -> dict[str, Any]:
    """Build mapping from source files to roadmap tasks."""
    roadmap = load_roadmap()
    mapping = {}
    
    for phase in roadmap.get("phases", []):
        for task in phase.get("tasks", []):
            task_file = task.get("file", "")
            if task_file:
                mapping[task_file] = {
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "phase": phase["id"],
                    "phase_name": phase["name"],
                    "status": task["status"]
                }
    
    return mapping


def generate_codebase_report() -> dict[str, Any]:
    """Generate full codebase analysis report."""
    src_scan = scan_src_directory()
    roadmap_mapping = build_file_to_roadmap_mapping()
    roadmap = load_roadmap()
    
    # Calculate stats
    total_files = len(src_scan)
    total_functions = sum(len(v["functions"]) for v in src_scan.values())
    total_classes = sum(len(v["classes"]) for v in src_scan.values())
    
    # Cross-reference with roadmap
    cross_referenced = []
    unreferenced = []
    
    for file_path, file_data in src_scan.items():
        matched = False
        for road_file, road_info in roadmap_mapping.items():
            if road_file in file_path or file_path.startswith(road_file.rstrip("/")):
                cross_referenced.append({
                    "file": file_path,
                    "roadmap_task": road_info
                })
                matched = True
                break
        if not matched:
            unreferenced.append(file_path)
    
    return {
        "generated_at": "2026-03-17T22:05:00",
        "stats": {
            "total_files": total_files,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "roadmap_tasks": roadmap.get("total_tasks", 0),
            "completed_tasks": roadmap.get("completed", 0),
            "in_progress_tasks": roadmap.get("in_progress", 0),
            "pending_tasks": roadmap.get("pending", 0)
        },
        "roadmap_completion_percent": roadmap.get("completion_percent", 0),
        "cross_referenced": cross_referenced,
        "unreferenced_files": unreferenced,
        "source_files": src_scan,
        "roadmap": roadmap
    }


def get_roadmap_coverage() -> dict[str, Any]:
    """Get roadmap coverage analysis."""
    roadmap = load_roadmap()
    src_scan = scan_src_directory()
    
    coverage = {
        "by_phase": [],
        "uncovered_files": [],
        "covered_files": []
    }
    
    # Map files to phases
    file_to_phase = {}
    for phase in roadmap.get("phases", []):
        for task in phase.get("tasks", []):
            task_file = task.get("file", "")
            if task_file:
                file_to_phase[task_file] = phase["id"]
    
    for file_path in src_scan:
        matched = False
        for road_file, phase_id in file_to_phase.items():
            if road_file in file_path:
                coverage["covered_files"].append({
                    "file": file_path,
                    "phase": phase_id
                })
                matched = True
                break
        if not matched:
            coverage["uncovered_files"].append(file_path)
    
    return coverage


if __name__ == "__main__":
    # CLI output for testing
    report = generate_codebase_report()
    print(json.dumps(report["stats"], indent=2))
    print(f"\nCross-referenced: {len(report['cross_referenced'])}")
    print(f"Unreferenced: {len(report['unreferenced_files'])}")
