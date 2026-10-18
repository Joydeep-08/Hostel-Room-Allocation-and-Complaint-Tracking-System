# Hostel Room Allocation and Complaint Tracking System

This repository contains a working hostel administration system using React/Vite on the frontend, FastAPI and SQLAlchemy on the backend, and MySQL 8/InnoDB as the authoritative database.

## Repository structure

```text
database/
  schema.sql        # MySQL DDL, constraints, indexes, and integrity triggers
  sample_data.sql   # Synthetic demonstration records only
  reports.sql       # Joins, aggregates, subqueries, and reporting examples
docs/
  architecture.md  # Architecture, Mermaid ER diagram, and business rules
backend/
  app/              # FastAPI application package
  migrations/       # Alembic migration environment
  requirements.txt  # Backend dependencies
frontend/
  src/              # React dashboard and responsive styles
  package.json       # Vite frontend scripts and dependencies
```

## Database setup and verification

Requirements: MySQL 8.x and the MySQL client.

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p hostel_management < database/sample_data.sql
mysql -u root -p hostel_management < database/reports.sql
mysql -u root -p hostel_management -e "SHOW TABLES; SELECT COUNT(*) AS beds FROM beds;"
```

The sample password hashes are deliberately synthetic placeholders and are not valid production credentials. The authentication phase will generate real Argon2 hashes and will never commit secrets.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` and `http://localhost:8000/health`. The database health endpoint requires valid credentials in `backend/.env`.

If the server reports that `database_url` or `jwt_secret_key` is missing, the `.env` file has not been created. Run `cp .env.example .env`, then replace the placeholder database password and JWT secret in `backend/.env`. Keep quoted values such as `APP_NAME="Hostel Management API"` quoted if you source the file in a shell. The API finds that file reliably whether Uvicorn is started from the repository root or the `backend` directory.

After loading `sample_data.sql`, replace its deliberately invalid administrator hash with a real local password:

```bash
cd backend
PYTHONPATH=. .venv/bin/python scripts/set_admin_password.py
```

The script prompts for the password without displaying or storing it. It updates `admin@hostel.local` as the active `Farhan Wajid` administrator.

Run the current backend test with:

```bash
PYTHONPATH=. pytest
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard is available at `http://localhost:5173`. Set `VITE_API_URL` when the API is not running on `http://localhost:8000`. Dashboard cards and activity use authenticated, database-backed API data.

## Implemented workflows

- `POST /api/auth/login` — OAuth2 form login with JWT access token.
- `POST /api/auth/register` — resident self-registration.
- `GET /api/auth/me` — current authenticated user.
- `GET /api/dashboard/stats` — database-calculated occupancy, complaint, and fee statistics.
- Resident, room, bed, allocation, complaint, invoice, and payment CRUD workflows.
- Administrator-only deletion and fee status controls.
- Resident-only complaint submission and fee payment.
- Room, bed, and allocation monthly pricing in rupees.
- Automatic current-period unpaid invoices and allocation-dependent fee amounts.
- Academic-year allocation end dates and live dashboard activity/statistics.
- Conflict and authorization alerts in the frontend for invalid or unauthorized actions.

## DBMS concepts demonstrated

- Primary/foreign keys, unique/check/not-null constraints, indexes, and InnoDB transactions.
- 1NF: each bed, payment, notification, and complaint update is a separate row.
- 2NF/3NF: room, hostel, resident, and invoice attributes are stored once and referenced by keys.
- `INNER JOIN`, `LEFT JOIN`, `WHERE`, `ORDER BY`, `GROUP BY`, `HAVING`, aggregates, `EXISTS`, and generated-column unique indexes.
- Allocation integrity through generated active keys, row-level locking in the future API service, and a cross-table maintenance trigger.

## Verification

Backend tests and the frontend production build can be run with:

```bash
cd backend
PYTHONPATH=. .venv/bin/pytest -q
PYTHONPATH=. .venv/bin/python -m py_compile app/main.py

cd ../frontend
npm run build
```

The application supports local development and the free deployment setup below.

## Free deployment

The repository includes deployment configuration for a free Render backend and a Vercel frontend:

- `render.yaml` provisions the FastAPI service from `backend/`.
- `frontend/vercel.json` keeps React Router routes working on direct page loads.

### 1. Create the Aiven MySQL database

Create a MySQL service in Aiven using its free plan. Create or select a database named `hostel_management`, then load the schema and sample data from a local terminal:

```bash
mysql -h YOUR_HOST -P YOUR_PORT -u YOUR_USER -p YOUR_DATABASE < database/schema.sql
mysql -h YOUR_HOST -P YOUR_PORT -u YOUR_USER -p YOUR_DATABASE < database/sample_data.sql
```

Use the connection values from Aiven to form the SQLAlchemy URL:

```text
mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE
```

If Aiven assigns a different database name, replace the first line (`USE hostel_management;`) in both `database/schema.sql` and `database/sample_data.sql` with the assigned name before importing. Do not run `database/reports.sql` unless you want the optional reporting queries.

### 2. Deploy the backend to Render

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint** and select the repository.
3. Render detects `render.yaml` and creates the `hostel-management-api` web service.
4. Set these environment variables on the service:
   - `DATABASE_URL`: the AlwaysData SQLAlchemy URL.
   - `CORS_ORIGINS`: the Vercel frontend URL, for example `https://your-app.vercel.app`.
5. Deploy and open `/health` on the generated Render URL.
6. Reset the administrator password against the hosted database if needed. Do not commit that password or any secret.

### 3. Deploy the frontend to Vercel

1. In Vercel, choose **Add New > Project** and select the same repository.
2. Set the project root directory to `frontend`.
3. Vercel detects Vite and uses `npm run build`.
4. Add the environment variable:
   - `VITE_API_URL`: the Render backend URL, without a trailing slash.
5. Deploy the project.
6. Copy the Vercel URL back into Render's `CORS_ORIGINS` variable and redeploy the backend.

Free services may sleep, have storage limits, or change their free-tier terms. Never commit `backend/.env`, database credentials, JWT secrets, or administrator passwords.
