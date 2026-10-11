# LowLevel Labs website

A responsive static website for `lowlevellabs.in`, designed for GitHub Pages.

## Files
- `index.html` — homepage
- `styles.css` — layout and visual theme
- `script.js` — article filtering and mobile navigation
- `articles/` — starter technical articles
- `assets/favicon.svg` — site icon
- `CNAME` — custom domain for GitHub Pages

## Preview locally
Open `index.html` in your browser. For a more realistic local server, run `python -m http.server 8000` from this folder and visit `http://localhost:8000`.

## Publish with GitHub Pages
1. Create a **public** GitHub repository named `lowlevellabs-site` (or another name).
2. Upload all files and folders in this project to the repository root. Do not upload the ZIP itself.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/(root)`, then Save.
5. In **Custom domain**, enter `lowlevellabs.in` and save. The included `CNAME` file already contains the domain; GitHub may still ask you to save it in Settings.
6. Wait for the Pages deployment to complete. Enable **Enforce HTTPS** when that option becomes available.

## GoDaddy DNS
At GoDaddy → Domain Portfolio → `lowlevellabs.in` → DNS, configure the following records for the apex/root domain:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `YOUR-GITHUB-USERNAME.github.io` |

Replace `YOUR-GITHUB-USERNAME` with your exact GitHub username. If an existing `A` record for `@` or `CNAME` for `www` conflicts, inspect it before replacing it. Do not remove MX records or email-related TXT records. GitHub's documentation is authoritative if its current UI shows different values.

Then return to **Settings → Pages**, confirm the custom domain, wait for DNS verification and HTTPS provisioning, and test:
- `https://lowlevellabs.in`
- `https://www.lowlevellabs.in`

DNS and HTTPS provisioning may take time. Do not assume it failed immediately after saving.

## Editing content
Edit `index.html` to change the homepage. Each article is a separate HTML file in `articles/`. When adding an article, add a matching card to `index.html` and use a valid relative link.

## Before public launch
The homepage contains three starter articles. Review and update them to match your preferred writing style and verify any technical code against your target kernel/platform. Avoid publishing employer-confidential information, proprietary code, restricted schematics, or internal project details.
