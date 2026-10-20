LEARNING FREELANCE / KIT DRAFT AUTOMATION

This version deliberately creates DRAFTS ONLY. No emails are sent automatically.
It only reacts to NEW files inside _posts (not edits) that have email: true.
It also requires their filename date to be within 2 days of today.
Past imported articles will not be sent.

1. In Kit, open Settings -> Developer -> V4 API keys and create a key.
2. In GitHub, open your repo -> Settings -> Secrets and variables -> Actions.
3. Add a repository secret named KIT_API_KEY with the key. Never commit or share it.
4. Upload the .github and scripts folders from this ZIP to the ROOT of your existing repo. Do not delete other site files.
   If GitHub web drag/drop refuses folder uploads, add the two files individually:
   .github/workflows/kit-newsletter.yml
   scripts/kit_newsletter.py
5. Test with a brand NEW _posts/YYYY-MM-DD-test-name.md containing:

---
layout: post
title: "Test from Learning Freelance"
subtitle: "This is the email inbox preview"
email: true
---

This is a test.

6. Commit. In GitHub -> Actions, open Create Kit newsletter drafts and look for a green check.
7. In Kit -> Broadcasts, find a new DRAFT and verify its subject, preview, content, and recipient options.
8. DO NOT SEND TO EVERYONE. Use Kit's test-email option or target only yourself first.

Important: The script builds an article URL from its Markdown filename slug using your Jekyll permalink /:title/.
If you use nonstandard permalinks, that link must be changed.

Later, after testing, we can add automated scheduling with audience safeguards.
