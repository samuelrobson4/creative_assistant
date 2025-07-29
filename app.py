import streamlit as st
import cv2
import tempfile
from PIL import Image
import numpy as np
import time
import mediapipe as mp
import openai
import os
import base64
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("Point and Create: AI Creative Assistant")

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ---------------------- Utilities ---------------------- #

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_landmark_data(hand_landmarks):
    return [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in hand_landmarks.landmark]

def get_index_tip_px(landmarks, image_shape):
    h, w = image_shape[:2]
    index_tip = landmarks[8]
    x_px = int(index_tip["x"] * w)
    y_px = int(index_tip["y"] * h)
    return (x_px, y_px)

def crop_around_point(img, center, size=400):
    h, w, _ = img.shape
    x, y = center
    x1 = max(0, x - size // 2)
    y1 = max(0, y - size // 2)
    x2 = min(w, x + size // 2)
    y2 = min(h, y + size // 2)
    return img[y1:y2, x1:x2]

# ---------------------- UI + Capture ---------------------- #

if "assistant_output" not in st.session_state:
    st.session_state["assistant_output"] = None

import io
from PIL import Image

uploaded_frame = st.camera_input("📸 Live View - Frame your hand and click Capture")

if uploaded_frame is not None:
    # Proper decoding of PIL Image → NumPy array
    image = Image.open(io.BytesIO(uploaded_frame.getvalue())).convert("RGB")
    frame_rgb = np.array(image)

    # Now safe to pass to MediaPipe
    results = hands.process(frame_rgb)

    st.session_state["crop_path"] = None
    st.session_state["assistant_output"] = None
    st.session_state["hand_data"] = None

    if results.multi_hand_landmarks:
        hand_landmarks_raw = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame_rgb, hand_landmarks_raw, mp_hands.HAND_CONNECTIONS)
        hand_data = extract_landmark_data(hand_landmarks_raw)
        st.session_state["hand_data"] = hand_data

        # Crop around index finger if possible
        try:
            fingertip_px = get_index_tip_px(hand_data, frame_rgb.shape)
            cropped = crop_around_point(frame_rgb, fingertip_px, size=400)
            crop_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
            Image.fromarray(cropped).save(crop_path)
            st.session_state["crop_path"] = crop_path
        except Exception as e:
            st.warning(f"Could not crop around finger: {e}")
    else:
        st.warning("No hand detected. Sending full image only.")

    # Save full frame
    full_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
    Image.fromarray(frame_rgb).save(full_path)
    st.session_state["image_path"] = full_path

# ---------------------- GPT Output Layout ---------------------- #

if "image_path" in st.session_state:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🖼️ Captured View")
        st.image(st.session_state["image_path"], caption="Full Frame", use_container_width=True)

    with col2:
        st.markdown("### 🤖 Assistant Response")

        # Call GPT if needed
        if st.session_state["assistant_output"] is None and openai_api_key:
            try:
                openai.api_key = openai_api_key
                full_base64 = encode_image(st.session_state["image_path"])
                messages = [
                    {"role": "system", "content": "You are a vision-language assistant who helps people find inspiring ideas for art, cooking and other forms of creation. Interpret the user's gesture and what they might be pointing at. Then provide a creative idea for what they could do with that object"},
                    {"role": "user", "content": [
                        {"type": "text", "text": "This is the scene. Please describe what the user is doing and what they appear to be pointing at then provide a creative idea for how they could develop that art piece further whether it be food, painting, ceramics, or any art piece."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{full_base64}"}}
                    ]}
                ]

                if st.session_state.get("crop_path"):
                    crop_base64 = encode_image(st.session_state["crop_path"])
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "This is a close-up of where the index finger is. Please focus on this region:"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{crop_base64}"}}
                        ]
                    })

                if st.session_state.get("hand_data"):
                    summary = f"Hand landmark data: {st.session_state['hand_data'][:5]} ... (truncated)"
                    messages.append({"role": "user", "content": summary})

                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5
                )
                st.session_state["assistant_output"] = response.choices[0].message.content

            except Exception as e:
                st.session_state["assistant_output"] = f"⚠️ OpenAI API error: {e}"

        # Show assistant output box
        if st.session_state["assistant_output"]:
            st.markdown(
                f"""
                <div style="border:1px solid #ccc; padding:15px; border-radius:10px; background-color:#f9f9f9;">
                {st.session_state["assistant_output"]}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="border:1px dashed #aaa; padding:15px; border-radius:10px; background-color:#fafafa; color:#777;">
                Assistant response will appear here after capture and analysis.
                </div>
                """,
                unsafe_allow_html=True
            )