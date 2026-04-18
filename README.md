# Interview_Schedular

Flask interview scheduling app with single and bulk interview invites.

## Run

1. Create a `.env` file or keep editing `.env.example`.
2. Set your SMTP credentials and API settings.
3. Set `PUBLIC_BASE_URL` to the public HTTPS URL where this app is deployed if you want people on different networks to join from email. Camera and microphone access only work on HTTPS or `localhost`, so plain HTTP LAN links will not work in modern browsers.
4. Set your Groq API values:
   - `GROQ_API_KEY`
   - `GROQ_MODEL` if you want to override the default
   - `GROQ_BASE_URL` only if you use a custom Groq-compatible endpoint
5. Set your email provider values:
   - `RESEND_API_KEY`
   - `RESEND_FROM` should be a verified sender for your Resend account
   - `RESEND_REPLY_TO`
   - or configure SMTP with `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, and optionally `SMTP_FROM`
6. If you deploy on Render, set `PUBLIC_BASE_URL` to your live `https://...onrender.com` URL so invite links in emails always open the deployed site.
7. Install dependencies:
   `pip install -r requirements.txt`
8. Start the app:
   `python main.py`
9. Open `http://localhost:8000`.

## Deploy on Render

1. Push this repository to GitHub.
2. In Render, create a new Web Service from the repository and let it use `render.yaml`.
3. Use the bundled Render Postgres database in `render.yaml`. The web service is configured to use `DATABASE_URL` from that database.
4. Set these environment variables in Render:
   - `PUBLIC_BASE_URL` set to your Render service URL, for example `https://your-app.onrender.com`
   - `RESEND_API_KEY`
   - `RESEND_FROM`
   - `RESEND_REPLY_TO`
   - `GROQ_API_KEY`
   - optionally `GROQ_MODEL`
   - or use the SMTP variables if you prefer that delivery method
5. Render will use the public service URL for invite links, so interviews can be opened from phones and laptops anywhere.
6. For higher traffic, upgrade the web service plan in Render to `standard` or above.

## If interview links or email still fail

1. Reschedule a fresh interview after redeploying. Older rows do not have the timezone offset saved.
2. Make sure you are opening the deployed `https://...onrender.com/interview?token=...` link, not a local LAN or `http://` address.
3. If Resend returns a delivery error, verify the `RESEND_FROM` address is allowed by your Resend account.
4. If you prefer, switch to SMTP by setting the SMTP variables and leaving `RESEND_API_KEY` empty.

## Bulk scheduling

- Use the dashboard bulk form to paste up to 100 candidates.
- Supported line formats:
  - `Name, email@example.com`
  - `Name <email@example.com>`
  - `email@example.com`

  Author
  Thahaseen Gulam
