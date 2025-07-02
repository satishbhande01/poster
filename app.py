import streamlit as st
from PIL import Image,ExifTags
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO('runs/content/runs/classify/train/weights/best.pt')
class_labels = model.names

st.title("🛠️ Encrypted Image Decoder")

st.write("""
🎨 **Welcome!**

This project is my way of integrating **AI** with something that would conventionally be considered *off the charts*...  
*Hehe, get it? Charts!* 

Inspired by the idea of **visual encryption**, this app uses **YOLOv8** to decode encrypted segments from a poster grid and recover the original image behind the scenes.


Think of it as AI solving a visual puzzle — try uploading one of the encrypted images and watch the magic unfold!

Feel free to use your Camera Directly from this app itself and get a nice zoom on the box of your interest!
""")


uploaded_image = st.file_uploader("🔒 Upload an encrypted image (One of the images from the grid)", type=["jpg", "png","jpeg"])

def fix_image_rotation(img: Image.Image) -> Image.Image:
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except Exception as e:
        # If there's no EXIF or something fails, just return as-is
        pass

if uploaded_image:
    img = Image.open(uploaded_image)
    img = fix_image_rotation(img)
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

st.write("""
By no means was this a perfectly functional project — it was more of a way to test my creativity.

In fact, try uploading a completely random image... you'll still get a confident prediction! 😅  
Which, of course, just means that my model needs more training data — and it should be learning **only from the poster**, not the rest.
""")

st.markdown("Feel free to reach out to me via [LinkedIn](https://www.linkedin.com/in/satish-bhande-6179a11b6/) to let me know if you had any guesses of what the images could actually be and do let me know if you had fun! Lastly...Sincerly Thank you for taking out your time.")

st.write("Once you are done Decrypting...Click the Learn More Button to gain more insights about this project.")
st.link_button("📘 Learn More", "https://satishbhande01.github.io/poster_info_page/")
