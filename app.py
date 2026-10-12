import spaces  # Import before torch for Hugging Face ZeroGPU compatibility.

import tempfile
import traceback

import gradio as gr
import numpy as np
import torch
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, MusicgenForConditionalGeneration

MODEL_ID = "facebook/musicgen-small"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load once at startup so the model is ready when ZeroGPU allocates the GPU.
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID).to(DEVICE)
model.eval()


@spaces.GPU(duration=120)
def generate_music(prompt, seconds, progress=gr.Progress()):
    prompt = (prompt or "").strip()
    if not prompt:
        raise gr.Error("Please describe the music you want to create.")

    try:
        progress(0.1, desc="Preparing your prompt...")
        inputs = processor(text=[prompt], padding=True, return_tensors="pt")
        inputs = {key: value.to(DEVICE) for key, value in inputs.items()}

        progress(0.25, desc=f"Generating music on {DEVICE.upper()}...")
        with torch.inference_mode():
            audio_values = model.generate(
                **inputs,
                max_new_tokens=int(seconds) * 50,
                do_sample=True,
                guidance_scale=3.0,
            )

        audio = audio_values[0].detach().float().cpu().numpy()
        if audio.ndim == 2:
            audio = audio.T
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        sample_rate = int(model.config.audio_encoder.sampling_rate)

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
            "Generation failed. Try a shorter clip or wait and retry. Details: " + str(exc)
        ) from exc


with gr.Blocks(title="Lite Music AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 🎵 Lite Music AI\n"
        "Create a short music clip from a text description. The model runs on hosted compute; "
        "you do not need to install Python on your computer."
    )
    gr.Markdown(
        "**Free hosting note:** this app is configured for Hugging Face ZeroGPU. "
        "Availability and free GPU quotas depend on your Hugging Face account and platform limits."
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
        "### Model and usage\n"
        "This app uses Meta's MusicGen Small model (facebook/musicgen-small). "
        "Its published license is **CC-BY-NC 4.0 (non-commercial use only)**. "
        "Review the [model card](https://huggingface.co/facebook/musicgen-small) and license "
        "before publishing or using generated audio. Do not use it commercially unless you "
        "have verified you have the necessary rights."
    )

if __name__ == "__main__":
    demo.launch()
