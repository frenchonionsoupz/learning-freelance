# Learning Freelance blog

## Publish a post

1. In GitHub, open `_posts`.
2. Click **Add file → Create new file**.
3. Name it `YYYY-MM-DD-short-title.md` (for example `2026-10-21-what-i-learned.md`).
4. Paste:

   ```
   ---
   layout: post
   title: "What I learned today"
   ---

   Write your post here.
   ```

5. Click **Commit changes**. GitHub Pages builds the homepage and article automatically.

## Before uploading

Upload the contents of this folder into the **root of the existing repository** with GitHub Pages enabled. Replace the existing `index.html`. Keep any existing `CNAME` file.

Settings → Pages → Build and deployment should remain **Deploy from a branch / main / (root)**.

The email subscription box is intentionally not connected. It does not save addresses.
The example post can be edited or deleted.

## Your domain

`_config.yml` is configured for `https://learningfreelance.com` at the root. If you only access the site using the GitHub project URL ending in `/learning-freelance/`, links to the root may not work until the custom domain is active. Your configured custom domain should load the site at the root.

## File structure

- `index.html`: automatically lists posts.
- `_layouts/default.html`: logo and basic site shell.
- `_layouts/post.html`: individual article pages.
- `_posts/*.md`: your writing.
- `assets/style.css`: green-and-cream design.
- `feed.xml`: basic RSS feed for future email automation.
- `_config.yml`: Jekyll site settings.
