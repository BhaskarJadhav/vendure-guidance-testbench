# 🖥️ Local Developer Setup: Running Vendure on Your PC

This guide walks you through setting up and running this Vendure Headless Commerce stack and Essora SDK environment on your local development machine.

---

## 🛠️ Prerequisites
Make sure you have the following installed on your PC:
1. **Node.js** (v18.x or v20.x recommended)
2. **Python 3.10+** (for running the injection and SDK helper scripts)
3. **Database (PostgreSQL)**: You can either:
   * Have a local PostgreSQL server running, or
   * Use **Docker Desktop** to run the lightweight PostgreSQL container included in the repository.

---

## 🚀 Step-by-Step Setup

### Step 1: Clone and Prepare
1. Open your terminal inside the project directory.
2. Copy the environment variables template to create your `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` in your editor and configure your database parameters if needed. The default values are:
   ```env
   APP_ENV=dev
   PORT=3000
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=vendure
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```

---

### Step 2: Start PostgreSQL
If you are using Docker, run this command to start the database container in the background:
```bash
docker compose up -d postgres
```
*Note: If you have a local PostgreSQL server running instead, make sure you create a database named `vendure` and that the connection details in `.env` match your database user credentials.*

---

### Step 3: Install Node.js Dependencies
Run the package manager installation to install Vendure, its plugins, and developer dependencies:
```bash
npm install
```

---

### Step 4: Populate & Seed the Database
Generate the tables and seed the database with tax zones, shipping rules, and the default product catalogs (Electronics, Appliances, Furniture):
```bash
npm run populate
```
*You should see a series of log messages indicating catalog insertion and initial database seeding completed successfully.*

---

### Step 5: Inject the Essora AI SDK Loader
To load the Essora assistant inside your local Admin UI panel, run the injection script. 
The script automatically detects you are running locally and modifies the correct `index.html` file inside your node_modules:
```bash
python3 inject_essora.py
```
*Output: `Using local developer path: node_modules/.../index.html` followed by `Injected/Updated Essora SDK successfully`.*

---

### Step 6: Boot Up the Vendure Server
Start the local commerce engine:
```bash
npm run start
```

---

## 🌟 Accessing the Local Services

Once the server has bootstrapped, you can access your local commerce engine endpoints:

| Service | Local URL | Credentials |
| :--- | :--- | :--- |
| **Admin UI Panel** | [http://localhost:3000/admin/](http://localhost:3000/admin/) | Username: `superadmin`<br>Password: `superadmin` |
| **GraphQL Shop API** | [http://localhost:3000/shop-api](http://localhost:3000/shop-api) | *N/A (Storefront endpoint)* |
| **GraphQL Admin API** | [http://localhost:3000/admin-api](http://localhost:3000/admin-api) | *N/A (Query playground)* |

---

## 🛠️ Troubleshooting

### 1. Database Connection Failures
* **Error**: `ConnectionRefused` or `password authentication failed`.
* **Fix**: Check that your local PostgreSQL instance is running and that your `.env` contains the correct username, password, and port matching your database.

### 2. Port Conflicts
* **Error**: `EADDRINUSE: address already in use :::3000`.
* **Fix**: Your port `3000` is currently being used by another process. Change `PORT=3000` inside `.env` to another port (e.g. `PORT=3080`) and restart the server. Your Admin UI will then be available on `http://localhost:3080/admin/`.

### 3. Clear/Reset Database
If you want to completely reset and wipe your database to start fresh:
1. Stop the server (`Ctrl + C`).
2. If using Docker, run: `docker compose down -v` to delete the postgres volume, then `docker compose up -d postgres`.
3. If using local PostgreSQL, drop the `vendure` schema and recreate it: `DROP DATABASE vendure; CREATE DATABASE vendure;`.
4. Re-run step 4: `npm run populate`.
