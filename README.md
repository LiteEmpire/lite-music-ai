# Lite Music AI 🎵

Lite Music AI is a fresh, browser-based music-making prototype published from this GitHub repository.

## Run it

Open `index.html` in a modern browser, or publish the repository with GitHub Pages. The app uses the browser's Web Audio API to synthesize short instrumental patterns based on the words in your prompt. It does not upload prompts or require an API key.

## Publish with GitHub Pages

A GitHub Actions workflow is included at `.github/workflows/pages.yml`.

1. Open this repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. Open **Actions** and allow the workflow to finish.
5. Your site should be published at `https://liteempire.github.io/lite-music-ai/`.

If GitHub asks you to approve Pages permissions, follow the prompts shown in the repository settings.

## Important: what this version does

This first version is a **prompt-driven procedural music prototype**, not a trained neural text-to-music model. It composes simple synthesized sounds in your browser using the selected style and keywords. GitHub Pages hosts static files; it does not provide the GPU/compute required to run a large AI music model.

A future true AI version will need a model plus an inference host or compatible browser-side model. Any host may have usage limits or require setup.

## Files

- `index.html` — complete responsive interface and browser audio composer.
- `.github/workflows/pages.yml` — deploys the static site to GitHub Pages.

## Privacy

Audio is generated locally in the browser. This prototype does not send prompts to an external service.

## License and model notes

No pretrained music model is bundled in this prototype. If a model is added in a future version, its license and any restrictions must be reviewed before publishing or commercial use.
