import streamlit as st
from PIL import Image
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO('runs/content/runs/classify/train/weights/best.pt')
class_labels = model.names

st.title("🛠️ Encrypted Image Decoder")

uploaded_image = st.file_uploader("🔒 Upload an encrypted image", type=["jpg", "png","jpeg"])

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="✅ Uploaded Encrypted Image", use_container_width=True)

    if st.button("🔓 Decrypt"):
        with st.spinner("🧠 Decoding..."):
            results = model.predict(img)
            predicted_class = results[0].probs.top1
            confidence = results[0].probs.data[predicted_class] * 100

            st.success(f"🔍 Predicted Class: **{class_labels[predicted_class]}** (Confidence: **{confidence:.2f}%**)")

            original_image_path = f"originals/{class_labels[predicted_class]}.jpg"
            try:
                original_img = Image.open(original_image_path)
                st.image(original_img, caption="✨ Decrypted Original Image", use_container_width=True)
            except FileNotFoundError:
                st.error("❌ Original image not found. Ensure the 'originals' folder has the correct images!")
# Add a proper button that redirects to the link
st.link_button("📘 Learn More", "https://satishbhande01.github.io/poster_info_page/")
