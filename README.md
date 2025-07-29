🖐️ Speak & Point with GPT-4o

An Interpretability-Driven Gesture Interface for Multimodal AI Systems

Overview
This prototype explores how AI systems—particularly multimodal LLMs like GPT-4o—can be directed through natural, physical gestures rather than traditional UI elements. Using MediaPipe hand tracking, camera input, and GPT-4o’s image-text reasoning, it allows a user to point at a region and have the assistant interpret and respond to what the user is referencing.

⸻

🎯 Why This Matters for Interpretability

LLMs are often opaque: users don’t know what the model is attending to, why it gave a response, or how it connects inputs to outputs.
This project provides a physical interface layer that helps:
	•	✅ Localize user intent: By detecting where a user is pointing, we can spatially crop and isolate what they’re referring to.
	•	✅ Constrain model attention: By feeding GPT-4o a cropped image region, we help ground the assistant’s focus—mirroring interpretability ideas like saliency or Grad-CAM in vision models.
	•	✅ Bridge human-AI alignment: The assistant doesn’t just process an image; it’s guided by a natural human gesture. This opens the door to co-pilots that are physically contextual, not just linguistically smart.

⸻

🧠 Architecture
	•	📸 st.camera_input() — Live image capture via Streamlit
	•	✋ MediaPipe Hands — Extracts fingertip position and detects pointing gestures
	•	📦 Cropping logic — Extracts a region around the fingertip (context-aware attention proxy)
	•	🧠 GPT-4o — Receives a multimodal prompt: user’s spoken intent + the image crop
	•	🖼️ GPT Response — Shown side-by-side with the annotated image


💡 Use Cases
	•	A kitchen assistant that responds to gestures like “what is this?” while pointing at an ingredient
	•	A workshop tool that explains objects or instructions based on visual reference
	•	A live demo scaffold for interpretability education: “what did the model focus on when I pointed here?”

⸻

🛠️ Built With
	•	Python, Streamlit
	•	MediaPipe (hand tracking)
	•	OpenAI GPT-4o (Vision + Text)
	•	PIL, NumPy, cv2