# Email Subscriber Worker — Project Spec

## Overview

A Cloudflare Worker + D1 system that manages email subscriptions across multiple mailing lists. Users subscribe via a form, confirm via double opt-in, and receive email notifications when the list owner sends one. The admin triggers sends manually via a CLI.

The system supports multiple independent mailing lists (e.g. `ethanswan.com`, `other-project`) within a single Worker and database.

## Tech Stack

- **Runtime**: Cloudflare Workers
- **Language**: TypeScript
- **Database**: Cloudflare D1 (SQLite)
- **Email**: Resend API (https://resend.com)
- **CLI**: TypeScript, runnable via `tsx`

---

# Part A: Build Instructions (for the implementing agent)

## Project Structure

```
email-worker/
├── src/
│   ├── worker.ts          # Cloudflare Worker (all endpoints)
│   └── cli.ts             # CLI for admin operations
├── schema.sql             # D1 table schema
├── wrangler.toml          # Cloudflare Worker config
├── package.json
├── tsconfig.json
└── .gitignore
```

## Database Schema (`schema.sql`)

```sql
CREATE TABLE subscribers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  list TEXT NOT NULL,
  token TEXT UNIQUE NOT NULL,
  confirmed INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now')),
  UNIQUE(email, list)
);
```

- `list` identifies which mailing list the subscriber belongs to (e.g. `"ethanswan"`, `"other-project"`).
- A person can subscribe to multiple lists — the UNIQUE constraint is on `(email, list)`, not just `email`.
- `token` is globally unique (a random UUID), so confirmation and unsubscribe links work without needing to know the list.
- `confirmed` is 0 until the user clicks the confirmation link.

## Worker Endpoints (`src/worker.ts`)

The worker needs access to the following bindings/env vars:
- `DB` — D1 database binding
- `RESEND_API_KEY` — Resend API key (set via `wrangler secret`)
- `SEND_SECRET` — shared secret for admin endpoints (set via `wrangler secret`)
- `FROM_EMAIL` — the "from" email address (set via `wrangler secret` or in `wrangler.toml` vars)
- `WORKER_URL` — the worker's public URL, used to construct confirmation/unsubscribe links (set in `wrangler.toml` vars)

### `POST /subscribe` (Public)

- Accepts JSON body: `{ "email": "...", "list": "..." }`
- Validates that the email contains `@`
- Validates that `list` is a non-empty string
- Generates a random UUID token
- Inserts a row into `subscribers` with `confirmed = 0` and the given `list`
- Sends a confirmation email via Resend with a link to `/confirm?token=<token>`
- Returns `200 { "ok": true }` on success
- Returns `409 { "error": "Already subscribed" }` if the `(email, list)` pair already exists (UNIQUE constraint violation)
- Returns `400 { "error": "Invalid email" }` for bad input
- Returns `400 { "error": "Missing list" }` if list is not provided
- CORS: Allow `POST` and `OPTIONS` from any origin (since multiple sites may use this Worker)

### `GET /confirm?token=<token>` (Public, token-authenticated)

- Looks up the subscriber by token
- Sets `confirmed = 1`
- Returns a simple HTML page saying "You're subscribed!" (doesn't need to be fancy, just a readable message in the browser)
- Returns 404 if token not found

### `GET /unsubscribe?token=<token>` (Public, token-authenticated)

- Looks up the subscriber by token
- Deletes the row from `subscribers`
- Returns a simple HTML page saying "You've been unsubscribed."
- Returns 404 if token not found

### `POST /send` (Admin, Bearer token auth)

- Requires header: `Authorization: Bearer <SEND_SECRET>`
- Accepts JSON body: `{ "list": "...", "subject": "...", "html": "..." }`
- Queries all subscribers where `confirmed = 1` AND `list` matches
- Sends an email to each via Resend API
- Each email's HTML should have the subscriber's unsubscribe link appended at the bottom: `<p><a href="https://<WORKER_URL>/unsubscribe?token=<token>">Unsubscribe</a></p>`
- Returns `200 { "sent": <count> }`
- Returns `400` if `list` is missing
- Returns `401` if auth fails

### `POST /admin/delete` (Admin, Bearer token auth)

- Requires header: `Authorization: Bearer <SEND_SECRET>`
- Accepts JSON body: `{ "email": "...", "list": "..." }`
- Deletes the subscriber with that `(email, list)` pair
- Returns `200 { "ok": true }` on success
- Returns `404` if not found
- Returns `401` if auth fails

### `GET /admin/list` (Admin, Bearer token auth)

- Requires header: `Authorization: Bearer <SEND_SECRET>`
- Accepts optional query param: `?list=<list>` to filter by list. If omitted, returns all subscribers across all lists.
- Returns JSON array of all matching subscribers with their email, list, confirmed status, and created_at
- Returns `401` if auth fails

### CORS

All responses to public endpoints should include CORS headers allowing any origin (`*`), since multiple sites may embed the subscribe form. Use an `OPTIONS` handler for preflight requests.

### Error Handling

Return JSON error responses with appropriate HTTP status codes. Don't leak internal details.

## CLI (`src/cli.ts`)

A command-line tool for admin operations. Should be runnable via `npx tsx src/cli.ts <command>`.

The CLI reads config from environment variables:
- `WORKER_URL` — the deployed worker URL
- `SEND_SECRET` — the admin secret

These can be set in a `.env` file (use `dotenv` or similar). Add `.env` to `.gitignore`.

### Commands

#### `send`

```
npx tsx src/cli.ts send --list ethanswan --subject "New post: Title" --html "<p>Check out <a href='...'>my new post</a></p>"
```

Calls `POST /send` with the given list, subject, and HTML body.

Alternatively, support reading HTML from stdin or a file:

```
npx tsx src/cli.ts send --list ethanswan --subject "New post: Title" --html-file email.html
```

The `--list` flag is required.

#### `list`

```
npx tsx src/cli.ts list
npx tsx src/cli.ts list --list ethanswan
```

Calls `GET /admin/list` (optionally filtered by list) and prints the subscribers in a readable table format.

#### `delete`

```
npx tsx src/cli.ts delete --email "someone@example.com" --list ethanswan
```

Calls `POST /admin/delete`. Both `--email` and `--list` are required.

### CLI dependencies

Use `commander` for argument parsing. Use `dotenv` for loading `.env` files.

## `wrangler.toml`

```toml
name = "email-subscribe"
main = "src/worker.ts"
compatibility_date = "2024-01-01"

[vars]
WORKER_URL = "https://email-subscribe.<account>.workers.dev"
FROM_EMAIL = "blog@ethanswan.com"

[[d1_databases]]
binding = "DB"
database_name = "email-subscribers"
database_id = "<to be filled in after creation>"
```

Secrets (`RESEND_API_KEY`, `SEND_SECRET`) are NOT in this file — they're set via `wrangler secret put`.

## `package.json`

Should include:
- `wrangler` as a dev dependency
- `tsx` as a dev dependency
- `commander` as a dependency
- `dotenv` as a dependency
- TypeScript and relevant `@cloudflare/workers-types` for type checking
- Scripts: `"deploy": "wrangler deploy"`, `"dev": "wrangler dev"`

## `.gitignore`

```
node_modules/
.env
.wrangler/
dist/
```

## TypeScript Config

Standard config targeting ES2022, with `@cloudflare/workers-types` included for Worker type definitions.

## Implementation Notes

- Use `crypto.randomUUID()` for token generation (available in Workers runtime).
- For Resend, it's a simple `fetch` call to `https://api.resend.com/emails` with a JSON body and `Authorization: Bearer <key>` header. No SDK needed.
- The CLI and Worker share no code — the CLI is just an HTTP client that calls the Worker's endpoints. No shared modules needed.
- Keep it simple. No frameworks, no ORMs.

---

# Part B: Setup & Deployment Instructions (for the blog owner)

These are the manual steps to set up infrastructure and deploy.

## 1. Create a Resend Account

1. Sign up at https://resend.com
2. Add and verify your sending domain (`ethanswan.com`) — Resend will give you DNS records to add
3. Generate an API key
4. Save the API key somewhere safe — you'll need it in step 5

## 2. Create the GitHub Repo

1. Create a new repo (e.g. `email-worker`) on GitHub
2. Clone it locally
3. Have the agent populate the code (Part A above)
4. Push to GitHub

## 3. Install Wrangler

```bash
npm install -g wrangler
```

## 4. Authenticate with Cloudflare

```bash
wrangler login
```

This opens a browser window to authenticate.

## 5. Create the D1 Database

```bash
wrangler d1 create email-subscribers
```

This outputs a database ID. Copy it into `wrangler.toml` in the `database_id` field.

## 6. Apply the Schema

```bash
wrangler d1 execute email-subscribers --file=schema.sql
```

## 7. Set Secrets

```bash
# The Resend API key from step 1
wrangler secret put RESEND_API_KEY

# A random secret for admin auth — generate one with: openssl rand -hex 32
wrangler secret put SEND_SECRET
```

## 8. Deploy the Worker

```bash
npm install
wrangler deploy
```

Note the deployed URL (e.g. `https://email-subscribe.<account>.workers.dev`). Update `WORKER_URL` in `wrangler.toml` if needed, and redeploy.

## 9. Configure Local CLI

Create a `.env` file in the repo root:

```
WORKER_URL=https://email-subscribe.<account>.workers.dev
SEND_SECRET=<the same secret from step 7>
```

Test it:

```bash
npx tsx src/cli.ts list
```

## 10. Add the Subscribe Form to Your Hugo Site

Add a form to the appropriate Hugo template (e.g. a partial in `layouts/partials/`):

```html
<form id="subscribe-form">
  <input type="email" id="subscribe-email" placeholder="you@example.com" required />
  <button type="submit">Subscribe</button>
</form>
<p id="subscribe-message" style="display:none;"></p>
<script>
  document.getElementById("subscribe-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("subscribe-email").value;
    const msg = document.getElementById("subscribe-message");
    try {
      const res = await fetch("https://email-subscribe.<account>.workers.dev/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, list: "ethanswan" }),
      });
      const data = await res.json();
      if (data.ok) {
        msg.textContent = "Check your email to confirm your subscription.";
      } else {
        msg.textContent = data.error || "Something went wrong.";
      }
    } catch {
      msg.textContent = "Something went wrong.";
    }
    msg.style.display = "block";
  });
</script>
```

Style this with Tailwind as desired. Note the `list: "ethanswan"` in the JSON body — change this value for different sites/lists.

## 11. Test the Full Flow

1. Subscribe with your own email via the form
2. Check your email for the confirmation link
3. Click the confirmation link
4. Run `npx tsx src/cli.ts list --list ethanswan` to verify you're confirmed
5. Run `npx tsx src/cli.ts send --list ethanswan --subject "Test" --html "<p>Hello!</p>"` to send a test email
6. Verify you received it and the unsubscribe link works

## 12. Optional: Cloudflare Rate Limiting

In the Cloudflare dashboard, add a rate limiting rule for the `/subscribe` endpoint to prevent abuse (e.g. max 5 requests per minute per IP). This is available on the free tier under Security → WAF → Rate Limiting Rules.
