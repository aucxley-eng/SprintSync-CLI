from datetime import datetime
from rich.console import Console
from rich.table import Table
import utils.auth_tools as auth_tools
from utils.auth_tools import _clear_session
from utils.storage import JSONManager

console = Console()


def cmd_register():
    console.print("\nEnter username:", style="bold cyan")
    username = input("> ")
    console.print("Enter password:", style="bold cyan")
    password = input("> ")
    console.print("Enter role (Admin/User):", style="bold cyan")
    role = input("> ")
    auth_tools.register_users(username, password, role)


def cmd_login():
    console.print("\nEnter username:", style="bold cyan")
    username = input("> ")
    console.print("Enter password:", style="bold cyan")
    password = input("> ")
    auth_tools.login_user(username, password)


def cmd_add_project():
    if not auth_tools.current_user:
        console.print("[red]You must be logged in![/red]")
        return

    console.print("\nEnter project name:", style="bold cyan")
    name = input("> ")
    console.print("Enter description:", style="bold cyan")
    description = input("> ")
    console.print("Enter deadline (YYYY-MM-DD):", style="bold cyan")
    deadline = input("> ")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    JSONManager.add_project(
        name=name,
        description=description,
        status="Active",
        owner=auth_tools.current_user["username"],
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


def print_header():
    console.print("\n╭───────────────────────╮", style="bold cyan")
    console.print("│  SprintSync CLI       │", style="bold cyan")
    console.print("│  Agile Project Manager│", style="bold cyan")
    console.print("╰───────────────────────╯", style="bold cyan")


def main():
    print_header()

    while True:
        # Always read the freshest current_user from the module
        user = auth_tools.current_user

        console.print("")  # blank line for breathing room

        if user:
            console.print(
                f"[bold green]Logged in as:[/bold green] [cyan]{user['username']}[/cyan] "
                f"([magenta]{user['role']}[/magenta])"
            )
            console.print("\n[bold]Select an option:[/bold]")
            console.print("  [cyan]1.[/cyan] Add Project")
            console.print("  [cyan]2.[/cyan] List Projects")
            console.print("  [cyan]9.[/cyan] Switch Account")
            console.print("  [cyan]0.[/cyan] Exit")
            console.print("")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                cmd_add_project()
            elif choice == "2":
                cmd_list_projects()
            elif choice == "9":
                _clear_session()
                auth_tools.current_user = None
                console.print("[yellow]Session cleared. Returning to main menu...[/yellow]")
            elif choice == "0":
                console.print("[bold cyan]Goodbye![/bold cyan]")
                break
            else:
                console.print("[red]Invalid option. Please try again.[/red]")

        else:
            console.print("[bold]Welcome! Please select an option:[/bold]")
            console.print("  [cyan]1.[/cyan] Register")
            console.print("  [cyan]2.[/cyan] Login")
            console.print("  [cyan]0.[/cyan] Exit")
            console.print("")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                cmd_register()
            elif choice == "2":
                cmd_login()
            elif choice == "0":
                console.print("[bold cyan]Goodbye![/bold cyan]")
                break
            else:
                console.print("[red]Invalid option. Please try again.[/red]")


if __name__ == "__main__":
    main()