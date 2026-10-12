---
title: Lite Music AI
emoji: 🎵
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.49.1
python_version: 3.10.13
app_file: app.py
---

# Lite Music AI 🎵

A text-to-music demo using Meta's MusicGen Small model. This repository is configured for **Hugging Face Spaces with ZeroGPU**, so visitors can use the interface in a browser without installing Python locally.

## Deploy it online

1. Sign in to Hugging Face at https://huggingface.co/.
2. Create a new Space at https://huggingface.co/new-space.
3. Name it lite-music-ai (or another available name), choose **Gradio**, set visibility to **Public**, and select **ZeroGPU** hardware if your account is eligible.
4. Once the Space is created, open its **Files** tab and upload these three files from this GitHub repository: app.py, requirements.txt, and README.md. You can view each file in this repository and copy/download its contents in your browser; no local Python installation is needed.
5. Wait for the Space to build. The model downloads automatically on its first startup. When the Space shows **Running**, open the app tab and generate a short clip.

**Important:** Hugging Face's free hosting rules can change. Free personal accounts must meet Hugging Face's eligibility requirements to host ZeroGPU Spaces. If ZeroGPU is not offered for your account, do not choose paid hardware; pause here and check the current options at https://huggingface.co/docs/hub/spaces-zerogpu.

## Using the app

1. Enter a music description.
2. Choose 5, 8, or 10 seconds.
3. Click **Generate music** and wait for the audio result.

## Requirements and limits

- You only need a web browser on your own computer; the hosted Space runs the Python app.
- The first startup needs to download the model and Python packages.
- Free GPU capacity can queue, pause, or have daily usage limits.
- Model startup and generation can take time.

## Model license

This app uses facebook/musicgen-small. The model's published license is **CC-BY-NC 4.0 (non-commercial use only)**. Review the [model card](https://huggingface.co/facebook/musicgen-small) and license before using the model or its outputs. Do not use it commercially unless you have confirmed you have the rights to do so. Also consider copyright and platform rules when writing prompts or publishing generated audio.

## Privacy

The app runs on the hosted Space. Your prompt is processed by that hosting service and model; this is not a fully offline/private local app. Avoid entering personal or sensitive information.

## Troubleshooting

- **Build error:** open the Space's **Logs** tab and inspect the first error.
- **Space sleeps or queues:** wait for it to wake or try again later; free capacity is shared.
- **Out of memory or GPU time limit:** try a 5-second clip.
- **Model download error:** retry after checking the Space's build/runtime logs.

## Code

- app.py: Gradio interface and music generation.
- requirements.txt: Python dependencies.
