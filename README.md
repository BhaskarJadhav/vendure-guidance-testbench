# Vendure v3 Enterprise Stack & Essora AI SDK Integration Testbench

A fully-automated, containerized, non-interactive deployment of the Vendure v3.x headless commerce engine on Google Cloud Platform (GCP), natively integrated with the **Essora AI Voice Assistant SDK** and validated via structural LLM orchestration.

---

## 🎯 Project Purpose (Why We Built This)

This testbench was created to serve as a production-grade playground for real-time voice-driven commerce. By combining a modern headless commerce platform (**Vendure**) with **Essora's AI Voice SDK** and **LiveKit’s WebRTC engine**, this project enables AI voice agents to:
1. Converse naturally with administrators inside the commerce dashboard.
2. Query products, pricing, and category structures dynamically.
3. Serve as a baseline architecture for voice-activated B2B / B2C storefront experiences.

---

## 🏗️ What We Accomplished (How We Did It)

### 1. GCP VM Provisioning & Firewall Configuration
*   Deployed a Compute Engine virtual machine (`vendure-guidance-testbench`) on GCP at public IP `35.238.201.140`.
*   Opened ports `3000` (Commerce Core & Shop API) and `5001` (Dev Admin UI) through custom VPC ingress firewall rules (`allow-vendure-ingress`).

### 2. Fully-Automated Dockerized Stack
*   Created a containerized architecture utilizing Docker Compose with two services:
    *   `postgres`: A PostgreSQL 16 Alpine database container (`vendure-db`).
    *   `vendure`: A Node.js container (`vendure-server`) running Vendure v3.x.
*   The stack was engineered to compile TypeScript, configure DB connection strings, and seed all products on the very first boot without requiring any interactive CLI inputs.

### 3. Comprehensive Database Seed
*   Seeded the PostgreSQL instance with **6 realistic products (12 unique SKU variants)** spanning three core categories:
    *   **Electronics**: Gaming Laptop, UltraWide Monitor
    *   **Appliances**: Smart Refrigerator, Microwave Oven
    *   **Furniture**: Ergonomic Chair, Standing Desk
*   Configured supporting logistical metadata, including Tax Categories, default shipping methods, India/UK/US shipping zones, and dummy checkout payment handlers.

### 4. Search Reindexing & Background Job Queue Resolution
*   **The Issue**: Monolithic configurations of Vendure v3 do not process background jobs automatically on first boot, leaving search index updates stuck in a `PENDING` state.
*   **The Solution**: Modified the server bootstrapping sequence in `src/index.ts` to programmatically initialize and start the `JobQueueService`.
*   We appended category keywords into product description matrices and built an automated re-indexing pipeline (`src/reindex.ts`) running on port `3001` to prevent port-conflicts. Full-text search for categorizations now functions natively.

### 5. Native Essora AI SDK Injection
*   Located the static precompiled Admin UI build inside the running docker container at `/usr/src/app/node_modules/@vendure/admin-ui-plugin/lib/admin-ui/browser/index.html`.
*   Directly injected the required **LiveKit Client WebRTC UMD bundle** and initialized the **Essora AI SDK** prior to the `</body>` closure, utilizing your preconfigured parameters:
    ```javascript
    Essora.init({
      serverUrl: "https://essora-backend-api-193009628373.asia-south1.run.app",
      livekitUrl: "wss://eassora-ai-june-bctpwpn4.livekit.cloud",
      apiKey: "pk_62af599c2284eaa74b746d0b999927b7",
      user: {
        id: "vendure-admin",
        email: "superadmin@vendure.io",
        name: "Vendure Superadmin"
      }
    });
    ```

---

## 🗺️ Current Platform Status & Architecture Map

*   **Host Virtual Machine**: `35.238.201.140` (GCP Compute Engine, `us-central1-a`)
*   **Shop API Endpoint**: [http://35.238.201.140:3000/shop-api](http://35.238.201.140:3000/shop-api)
*   **Admin UI Panel**: [http://35.238.201.140:3000/admin/](http://35.238.201.140:3000/admin/)
    *   *Note: In production deployments, Vendure compiles and serves the Admin UI statically via port `3000` middleware. This maximizes server performance, minimizes memory footprints, and avoids cross-origin (CORS) connection blocks.*
    *   **Username**: `superadmin`
    *   **Password**: `superadmin`

---

## 🧪 Local Verification & Integration Testing

To execute local structural queries against your cloud-hosted environment using Python's `guidance` LLM engine:

1.  **Activate virtual environment**:
    ```powershell
    .venv\Scripts\activate
    ```
2.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Run the verification script**:
    ```powershell
    python test_guidance_sdk.py
    ```

---

## 🚀 Future Roadmap (What We Will Do Further)

To transition this proof-of-concept into an enterprise-ready system, we propose the following forward-looking enhancements:

### 1. High-Performance CDN Delivery for Admin Assets
*   Instead of injecting scripts inside a running container’s local `node_modules` (which makes container recreation ephemeral), compile the customized Admin UI statically during the Docker build stage and serve it from a global CDN (like Google Cloud CDN or Cloudflare).

### 2. Conversational Checkout & Cart Hook Implementation
*   Develop backend API webhooks in Vendure that allow the Essora Voice AI agent to programmatically add items to a user's cart or complete checkout actions in response to spoken phrases (e.g., *"Add two standing desks to my order"*).

### 3. Advanced Vector & Semantic Search
*   Integrate a Vector Search Plugin (such as pgvector or Milvus) to allow the voice agent to find products via semantic meaning (e.g., *"Find something comfortable to sit on for long working hours"*) rather than relying purely on text-based keyword matching.

### 4. Custom Self-Hosted LiveKit WebRTC Infrastructure
*   Transition from cloud-hosted LiveKit instances to a self-hosted, auto-scaling LiveKit server deployment on Google Kubernetes Engine (GKE) to ensure ultra-low latency audio processing and complete data residency control.
