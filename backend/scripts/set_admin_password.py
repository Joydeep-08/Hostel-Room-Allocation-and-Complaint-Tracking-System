from getpass import getpass

from argon2 import PasswordHasher
from sqlalchemy import text

from app.db import SessionLocal


def main() -> None:
    email = input("Administrator email [admin@hostel.local]: ").strip() or "admin@hostel.local"
    password = getpass("New administrator password: ")
    confirmation = getpass("Confirm password: ")
    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    with SessionLocal.begin() as db:
        result = db.execute(
            text("""
                UPDATE users
                SET password_hash = :password_hash,
                    full_name = 'Farhan Wajid',
                    role = 'administrator',
                    is_active = TRUE
                WHERE email = :email
            """),
            {"email": email, "password_hash": PasswordHasher().hash(password)},
        )
        if result.rowcount != 1:
            raise SystemExit(f"No user found for {email}. Load sample_data.sql or create the account first.")

    print(f"Administrator password updated for {email}.")


if __name__ == "__main__":
    main()
