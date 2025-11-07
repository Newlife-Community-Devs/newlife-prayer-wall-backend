from email_validator import validate_email as email_validate, EmailNotValidError
from typing import Optional
import re
import typer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError, EmailStr
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash, verify_password

app = typer.Typer()


app = typer.Typer()

# Configure allowed email domains (add your allowed domains here)
ALLOWED_EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "prayerwall.com",
    "example.com",  # Remove this in production
]


def validate_email_domain(email: str) -> tuple[bool, str]:
    """Check if email domain is in allowed list."""
    domain = email.split("@")[-1].lower()
    if domain not in ALLOWED_EMAIL_DOMAINS:
        allowed_domains = "\n  - ".join(ALLOWED_EMAIL_DOMAINS)
        return False, f"Email domain not allowed. Allowed domains are:\n  - {allowed_domains}"
    return True, "Email domain is allowed"


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"


def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format using `email_validator`."""
    try:
        email_validate(email)
        return True, "Email is valid"
    except EmailNotValidError:
        return False, "Invalid email format"


def validate_full_name(full_name: Optional[str]) -> tuple[bool, str]:
    """Validate full name if provided."""
    if full_name is None:
        return True, "Full name is optional"
    if len(full_name.strip()) < 2:
        return False, "Full name must be at least 2 characters long"
    if not re.match(r"^[a-zA-Z\s\-']+$", full_name):
        return False, "Full name can only contain letters, spaces, hyphens and apostrophes"
    return True, "Full name is valid"


def create_admin_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> User:
    """Create a new admin user with validation."""
    # Validate email format
    is_valid, msg = validate_email(email)
    if not is_valid:
        raise ValueError(msg)

    # Validate email domain
    is_valid, msg = validate_email_domain(email)
    if not is_valid:
        raise ValueError(msg)

    # Validate password
    is_valid, msg = validate_password(password)
    if not is_valid:
        raise ValueError(msg)

    # Validate full name if provided
    if full_name:
        is_valid, msg = validate_full_name(full_name)
        if not is_valid:
            raise ValueError(msg)

    # Create user
    try:
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_admin=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError(f"User with email {email} already exists")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error creating user: {str(e)}")


def print_password_requirements():
    """Print password requirements to the console."""
    typer.echo("Password requirements:")
    typer.echo("- At least 8 characters long")
    typer.echo("- At least one uppercase letter")
    typer.echo("- At least one lowercase letter")
    typer.echo("- At least one number")
    typer.echo("- At least one special character (!@#$%^&*(),.?\":{}|>)")


def get_admin_by_email(db: Session, email: str) -> Optional[User]:
    """Get admin user by email."""
    return db.query(User).filter(User.email == email, User.is_admin == True).first()


@app.command()
def change_password():
    """Change password for an existing admin user."""
    db = None
    try:
        db = SessionLocal()
        email = typer.prompt("Admin email")
        admin = get_admin_by_email(db, email)
        if not admin:
            typer.echo(typer.style(
                f"No admin user found with email: {email}",
                fg=typer.colors.RED,
            ))
            return

        # Verify current password
        current_password = typer.prompt(
            "Current password",
            hide_input=True,
        )
        if not verify_password(current_password, admin.hashed_password):
            typer.echo(typer.style(
                "Current password is incorrect",
                fg=typer.colors.RED,
            ))
            return

        # Get and validate new password
        print_password_requirements()
        new_password = typer.prompt(
            "New password",
            hide_input=True,
            confirmation_prompt=True,
        )
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            typer.echo(typer.style(
                f"Invalid password: {msg}", fg=typer.colors.RED))
            return

        # Update password
        setattr(admin, "hashed_password", get_password_hash(new_password))
        db.add(admin)
        db.commit()

        typer.echo(typer.style(
            "✓ Password changed successfully!",
            fg=typer.colors.GREEN,
            bold=True,
        ))
    except Exception as e:
        typer.echo(typer.style(
            f"Error changing password: {str(e)}", fg=typer.colors.RED))
    finally:
        if db is not None:
            db.close()


@app.command()
def deactivate_admin():
    """Deactivate an admin user account."""
    db = None
    try:
        db = SessionLocal()
        email = typer.prompt("Admin email to deactivate")
        admin = get_admin_by_email(db, email)
        if not admin:
            typer.echo(typer.style(
                f"No admin user found with email: {email}",
                fg=typer.colors.RED,
            ))
            return

        # Confirm deactivation
        if not typer.confirm(f"Are you sure you want to deactivate admin {admin.email}?"):
            typer.echo("Operation cancelled.")
            return

        setattr(admin, "is_active", False)
        db.add(admin)
        db.commit()

        typer.echo(typer.style(
            f"✓ Admin user {admin.email} has been deactivated",
            fg=typer.colors.GREEN,
            bold=True,
        ))
    except Exception as e:
        typer.echo(typer.style(
            f"Error deactivating admin: {str(e)}", fg=typer.colors.RED))
    finally:
        if db is not None:
            db.close()


@app.command()
def reactivate_admin():
    """Reactivate a deactivated admin user account."""
    db = None
    try:
        db = SessionLocal()
        email = typer.prompt("Admin email to reactivate")
        admin = db.query(User).filter(User.email == email,
                                      User.is_admin == True).first()
        if not admin:
            typer.echo(typer.style(
                f"No admin user found with email: {email}", fg=typer.colors.RED,
            ))
            return

        if getattr(admin, "is_active", False):
            typer.echo(typer.style(
                f"Admin {admin.email} is already active", fg=typer.colors.YELLOW,
            ))
            return

        setattr(admin, "is_active", True)
        db.add(admin)
        db.commit()

        typer.echo(typer.style(
            f"✓ Admin user {admin.email} has been reactivated",
            fg=typer.colors.GREEN,
            bold=True,
        ))
    except Exception as e:
        typer.echo(typer.style(
            f"Error reactivating admin: {str(e)}", fg=typer.colors.RED))
    finally:
        if db is not None:
            db.close()


@app.command()
def list_admins():
    """List all admin users in the system."""
    db = None
    try:
        db = SessionLocal()
        admins = db.query(User).filter(User.is_admin == True).all()

        if not admins:
            typer.echo(typer.style(
                "No admin users found.", fg=typer.colors.YELLOW))
            return

        typer.echo("\nAdmin Users:")
        typer.echo("=" * 50)
        for user in admins:
            typer.echo(typer.style(
                f"\nID: {user.id}", fg=typer.colors.BLUE, bold=True))
            typer.echo(f"Email: {user.email}")
            typer.echo(f"Name: {user.full_name or 'Not provided'}")
            typer.echo(
                f"Active: {'Yes' if getattr(user, 'is_active', False) else 'No'}")
        typer.echo("\n" + "=" * 50)
    except Exception as e:
        typer.echo(typer.style(
            f"Error listing admin users: {str(e)}", fg=typer.colors.RED, bold=True), err=True)
    finally:
        if db is not None:
            db.close()


@app.command()
def create_admin(
    email: str = typer.Option(..., prompt="Email address"),
    password: str = typer.Option(
        ...,
        prompt="Password",
        hide_input=True,
        confirmation_prompt=True,
    ),
    full_name: Optional[str] = typer.Option(
        None, prompt="Full name (optional)"),
):
    """Create an admin user in the database with input validation."""
    db: Optional[Session] = None
    try:
        # Show password requirements before prompt
        print_password_requirements()

        db = SessionLocal()
        user = create_admin_user(db, email, password, full_name)
        typer.echo(typer.style(
            f"✓ Admin user created successfully! ID: {user.id}", fg=typer.colors.GREEN, bold=True))
    except ValueError as e:
        typer.echo(typer.style(
            f"Error: {str(e)}", fg=typer.colors.RED, bold=True), err=True)
    except Exception as e:
        typer.echo(typer.style(
            f"Unexpected error: {str(e)}", fg=typer.colors.RED, bold=True), err=True)
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    app()
