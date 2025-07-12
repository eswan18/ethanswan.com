# [ethanswan.com](https://ethanswan.com)

[![Netlify Status](https://api.netlify.com/api/v1/badges/5c5270e1-d609-4a19-9798-43c634a951e2/deploy-status)](https://app.netlify.com/sites/ethanswan/deploys)

My personal website. Built with [Hugo](https://gohugo.io).

## Running Locally

Because I am using both hugo and tailwind, running live rebuilds requires having both active simultaneously.
My preferred approach is to open two terminal windows (or tmux panes) and run `hugo serve` in one from the base of the repo, while running `npm run watch` in the other from the `tailwind/` folder.

Tailwind will rebuild whenever a file in `content/` or `layouts/` has a change that impacts CSS classes, and it puts its output file in `assets/css`.
Hugo is watching that output folder, and will thus rebuild the site when Tailwind updates the file there.

## Preparing for Deployment
As of now, I don't have anything set up in Netlify related to Tailwind.  
Things should still work fine as long as the `assets/css/tailwind-style.css` file is committed, though.
