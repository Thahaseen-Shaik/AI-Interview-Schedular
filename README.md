AI Interview Scheduler

An AI Interview Scheduler Application that allows recruiters to schedule single and bulk interview invites, send email notifications, and conduct interviews via secure links with optional AI integration.

🚀 Features
📅 Schedule single interview invites
📩 Send bulk interview invitations (up to 100 candidates)
🔗 Secure interview links with tokens
📧 Email integration using Resend API or SMTP
🌐 Public access via HTTPS (camera & mic supported)
🤖 AI-powered features using Groq API
☁️ Easy deployment on Render
🛠️ Tech Stack
Backend: Python, Flask
Database: PostgreSQL (Render)
Email: Resend API / SMTP
AI: Groq API
Deployment: Render
⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Configure Environment Variables

Create a .env file (or edit .env.example) and set the following:

🌐 App Configuration
PUBLIC_BASE_URL=https://your-domain.com
🤖 Groq API (Optional)
GROQ_API_KEY=your_api_key
GROQ_MODEL=your_model_name (optional)
GROQ_BASE_URL=your_custom_url (optional)
📧 Email Configuration (Choose One)

Option 1: Resend API

RESEND_API_KEY=your_resend_api_key
RESEND_FROM=verified_sender_email
RESEND_REPLY_TO=reply_email

Option 2: SMTP

SMTP_HOST=your_smtp_host
SMTP_PORT=your_port
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
SMTP_FROM=sender_email
3. Install Dependencies
pip install -r requirements.txt
4. Run the Application
python main.py

Open in browser:

http://localhost:8000
☁️ Deployment on Render
Push your code to GitHub
Go to Render
Create a New Web Service
Connect your repository
Render will automatically use render.yaml
🔑 Set Environment Variables in Render
PUBLIC_BASE_URL=https://your-app.onrender.com
RESEND_API_KEY=your_key
RESEND_FROM=your_email
RESEND_REPLY_TO=reply_email
GROQ_API_KEY=your_key

(Or use SMTP instead of Resend)

🗄️ Database
Uses Render PostgreSQL
DATABASE_URL is automatically configured
📌 Important Notes
Use HTTPS for camera & microphone access
Avoid using HTTP or LAN URLs
Always open interview links like:
https://your-app.onrender.com/interview?token=...
❗ Troubleshooting
🔄 Interview link not working?
→ Reschedule after redeployment (timezone issue)
📧 Email not delivered?
→ Verify sender in Resend
→ Or switch to SMTP
🔗 Link not opening?
→ Use deployed HTTPS link, not localhost
📊 Bulk Scheduling Format

You can paste up to 100 candidates in the dashboard.

Supported formats:

Name, email@example.com
Name <email@example.com>
email@example.com
👨‍💻 Author

Thahaseen Gulam

📜 License

This project is licensed under the MIT License.
