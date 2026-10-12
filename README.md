# Lite Music AI 🎵

A simple text-to-music app that runs the model on your own computer. It does not require a paid AI provider or API key.

## What it does

- Turns a text description into a short music clip.
- Offers 5-, 8-, and 10-second generation lengths.
- Runs locally using Meta's MusicGen Small model.
- Uses Gradio for a simple browser interface.

## Requirements

- Windows 10/11, macOS, or Linux.
- Python 3.10 or 3.11 recommended.
- Internet for the first model download.
- Several GB of free disk space and RAM. A compatible NVIDIA GPU helps a lot; CPU generation may be very slow.

**Laptop note:** on a lower-powered computer such as an older office laptop, the model may be slow or run out of memory. Start with the 5-second option and close other applications.

## Run on Windows

1. Install Python 3.10 or 3.11 from https://www.python.org/downloads/. During installation, enable **Add Python to PATH**.
2. Download this repository using GitHub's **Code → Download ZIP**, then extract it.
3. Open the extracted lite-music-ai folder in File Explorer.
4. Click the address bar, type cmd, and press Enter.
5. Create and activate a virtual environment:

   ```bat
   py -3.11 -m venv .venv
   .venv\\Scripts\\activate
   python -m pip install --upgrade pip
   ```

6. Install dependencies:

   ```bat
   pip install -r requirements.txt
   ```

   If PyTorch installation fails or you want GPU acceleration, follow the current instructions at https://pytorch.org/get-started/locally/.

7. Start the app:

   ```bat
   python app.py
   ```

8. Wait for the first model download, then open http://127.0.0.1:7860 if it does not open automatically.
9. Enter a music description, choose a duration, and click **Generate music**.

## Important model license

This app uses facebook/musicgen-small. The model's published license is **CC-BY-NC 4.0 (non-commercial use only)**. Review the model card at https://huggingface.co/facebook/musicgen-small and its license terms before using the model or its outputs. Do not use it for commercial purposes unless you have confirmed you have the rights to do so. Also consider copyright and platform rules when writing prompts or publishing generated audio.

## Privacy and network use

The app runs on your computer. The first run needs internet to download the model and Python packages. Once the model is cached, music generation itself runs locally; this app does not send prompts to a paid AI-provider API.

## Troubleshooting

- **Very slow:** CPU generation can take a long time. Try 5 seconds, wait, and check system memory.
- **Out of memory:** close other programs and retry with a shorter clip. If it still fails, the computer may not be powerful enough for this model.
- **Download/install error:** check your internet connection and retry the failed command.
- **Port already in use:** close the other app using port 7860 or change server_port=7860 near the bottom of app.py.

## License

The code in this repository is provided as-is. The MusicGen model has its own license and usage conditions; see the model card linked above.
