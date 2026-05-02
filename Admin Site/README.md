# LearnPath Admin Site

This is the independent **Admin Panel** for the LearnPath ecosystem. It is completely isolated from the User Site, running its own secure backend and dynamic UI.

## 🚀 Local Development

1. **Navigate to the Admin Site directory:**
   ```bash
   cd "Admin Site"
   ```

2. **Set up the Backend Environment:**
   ```bash
   cd admin-backend
   python -m venv venv
   # Activate venv:
   # Windows: .\venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   - Copy `.env.example` to `.env` in the root of the `Admin Site`.
   - Update `MONGO_URI` to point to your MongoDB Atlas cluster.

4. **Run the Backend:**
   ```bash
   python app.py
   ```
   *The admin backend runs on `http://localhost:5001` to prevent conflicts with the user site.*

5. **Run the Frontend:**
   - Open `admin-frontend/index.html` in your browser.
   - Login using: `admin@learnpath.com` / `admin`.

---

## ☁️ Vercel Deployment

This project is pre-configured to be deployed natively on Vercel as a Serverless Python API alongside static HTML files.

1. **Install Vercel CLI (optional):**
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel:**
   - Run `vercel` from inside the `Admin Site/` directory, OR connect your GitHub repository directly in the Vercel Dashboard.
   - Vercel will automatically read the `vercel.json` file.

3. **Configure Vercel Environment Variables:**
   Go to your Vercel Project Settings > Environment Variables, and add:
   - `MONGO_URI` (Your MongoDB Atlas connection string)
   - `MONGO_DB_NAME` (e.g., `learnpath`)
   - `ADMIN_SECRET_KEY`
   - `ADMIN_JWT_SECRET`

Once deployed, the frontend will be served at your Vercel URL, and all API calls will be automatically routed to the serverless Python functions under `/api/`.
