import os
import tempfile
import traceback

import gradio as gr
import numpy as np
import torch
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, MusicgenForConditionalGeneration

MODEL_ID = "facebook/musicgen-small"
processor = None
model = None
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_model():
    global processor, model
    if model is None:
        processor = AutoProcessor.from_pretrained(MODEL_ID)
        model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID)
        model.to(device)
        model.eval()
    return processor, model


def generate_music(prompt, seconds, progress=gr.Progress()):
    prompt = (prompt or "").strip()
    if not prompt:
        raise gr.Error("Please describe the music you want to create.")
    try:
        progress(0.05, desc="Loading the local AI model (first run downloads it)...")
        current_processor, current_model = load_model()
        progress(0.2, desc="Preparing your prompt...")
        inputs = current_processor(text=[prompt], padding=True, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}
        max_new_tokens = int(seconds) * 50
        progress(0.3, desc=f"Generating on {device.upper()}...")
        with torch.inference_mode():
            audio_values = current_model.generate(
                **inputs, max_new_tokens=max_new_tokens,
                do_sample=True, guidance_scale=3.0,
            )
        audio = audio_values[0].detach().float().cpu().numpy()
        if audio.ndim == 2:
            audio = audio.T
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        sample_rate = int(current_model.config.audio_encoder.sampling_rate)
        handle = tempfile.NamedTemporaryFile(prefix="lite_music_ai_", suffix=".wav", delete=False)
        output_path = handle.name
        handle.close()
        write_wav(output_path, sample_rate, audio_int16)
        progress(1.0, desc="Done!")
        return output_path
    except gr.Error:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise gr.Error(
            "Music generation failed. Check available RAM/disk space and whether the "
            "first model download completed. Details: " + str(exc)
        ) from exc


with gr.Blocks(title="Lite Music AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 🎵 Lite Music AI\n"
        "Create music from a text description using an open model running on your own computer. "
        "No paid AI-provider API key is required."
    )
    gr.Markdown(
        "**First run:** the model downloads from Hugging Face and needs internet. "
        "After it is cached, generation runs locally. CPU generation can be very slow."
    )
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(
                label="Describe your music",
                placeholder="Epic, energetic action music with powerful drums and heroic synths",
                lines=4,
                max_lines=6,
            )
            duration = gr.Radio(
                choices=[("5 seconds (quick test)", 5), ("8 seconds", 8), ("10 seconds", 10)],
                value=5,
                label="Clip length",
            )
            generate = gr.Button("Generate music", variant="primary")
        with gr.Column():
            output = gr.Audio(label="Your generated music", type="filepath")
    generate.click(fn=generate_music, inputs=[prompt, duration], outputs=output)
    gr.Markdown(
        "### Important\n"
        "This app uses Meta's MusicGen Small model (facebook/musicgen-small). "
        "Check its model card and license before use. The model is licensed for "
        "**non-commercial use only**; do not use generated results commercially unless "
        "you have verified that you have the necessary rights.\n\n"
        "This is a local demo, not a hosted music-generation website. Your computer does the work."
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
