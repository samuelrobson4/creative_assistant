# Point and Create Assistant

This interactive Streamlit prototype allows users to **point at a region in a live camera feed** and receive a response from **GPT-4o** based on what they’re gesturing toward.

It’s a lightweight, spatially grounded demo that blends **computer vision**, **gesture tracking**, and **LLM interpretability** — perfect for prototyping AI co-pilots for physical tasks.

---

## 🧠 What It Does

- 📷 Captures a webcam image via Streamlit
- ✋ Detects a hand and recognizes pointing using MediaPipe
- 📍 Crops the region being pointed at
- 🧾 Sends the cropped region and prompt to OpenAI GPT-4o
- 💬 Displays the assistant’s multimodal response

---

## 🔍 Why It Matters

This app is a sandbox for exploring:

- **Interpretability** — What happens when we give the model focused spatial input?
- **Physical-world grounding** — Can a model reason about real-world objects we gesture toward?
- **AI co-pilots for physical tasks** — Think: home assistants, repair guides, recipe helpers

---

## 🚀 How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/speak-point-gpt4o.git
cd speak-point-gpt4o
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI key in a `.env` file

Create a file named `.env` in the root of your project:

```env
OPENAI_API_KEY=sk-...
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🧾 Requirements

These are defined in `requirements.txt`, but key packages include:

- `streamlit`
- `mediapipe`
- `openai`
- `opencv-python`
- `pillow`
- `numpy`
- `python-dotenv`

---

## 🧪 Example Use Cases

- Interpretable gesture-based interfaces for physical environments
- Prototyping AI assistants that understand *where* you’re pointing
- Spatial reasoning experiments with GPT-4o multimodal input

---

## 🛠️ Roadmap Ideas

- [ ] Live webcam preview before capture
- [ ] Voice + gesture input loop
- [ ] Grad-CAM style token attention overlays
- [ ] Gesture classification beyond pointing
- [ ] Streamlit Cloud or Vercel deployment

---

## 👤 Made by

**Samuel Robson**  
Product-minded strategist and AI prototyper  
🎓 MIMS @ UC Berkeley  
🛠️ Interpretability · Tangible Interfaces · Human-Centered AI

[GitHub](https://github.com/samuelrobson4) · [LinkedIn](https://www.linkedin.com/in/samuelrobson1/)