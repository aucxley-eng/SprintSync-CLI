import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from utils.auth_tools import register_users, login_user, logout_user, current_user
from utils.storage import JSONManager

console = Console()


def cmd_register():
    console.print("Enter username:", style="bold cyan")
    username = input()
    console.print("Enter password:", style="bold cyan")
    password = input()
    console.print("Enter role (Admin/User):", style="bold cyan")
    role = input()
    register_users(username, password, role)


def cmd_login():
    console.print("Enter username:", style="bold cyan")
    username = input()
    console.print("Enter password:", style="bold cyan")
    password = input()
    login_user(username, password)


def cmd_logout():
    logout_user()


def cmd_add_project():
    if not current_user:
        console.print("[red]You must be logged in![/red]")
        return

    console.print("Enter project name:", style="bold cyan")
    name = input()
    console.print("Enter description:", style="bold cyan")
    description = input()
    console.print("Enter deadline (YYYY-MM-DD):", style="bold cyan")
    deadline = input()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    JSONManager.add_project(
        name=name,
        description=description,
        status="Active",
        owner=current_user["username"],  # directly reference auth_tools current_user
        time=now,
        deadline=deadline
    )


def cmd_list_projects():
    projects = JSONManager.list_projects()
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="SprintSync Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Owner", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Deadline", style="red")
    table.add_column("Tasks", style="blue")

    for proj in projects:
        table.add_row(
            str(proj["id"]),
            proj["name"],
            proj["owner"],
            proj["status"],
            proj["deadline"],
            str(len(proj["tasks"]))
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="SprintSync CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("register")
    subparsers.add_parser("login")
    subparsers.add_parser("logout")
    subparsers.add_parser("add-project")
    subparsers.add_parser("list-projects")

    args = parser.parse_args()

    console.print("╭───────────────────────╮", style="bold cyan")
    console.print("│ SprintSync CLI        │", style="bold cyan")
    console.print("│ Agile Project Manager │", style="bold cyan")
    console.print("╰───────────────────────╯", style="bold cyan")

    if args.command == "register":
        cmd_register()
    elif args.command == "login":
        cmd_login()
    elif args.command == "logout":
        cmd_logout()
    elif args.command == "add-project":
        cmd_add_project()
    elif args.command == "list-projects":
        cmd_list_projects()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()