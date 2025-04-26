import streamlit as st
import cv2

st.title("📷 Live Object Counting")

cap = cv2.VideoCapture(0)  # Open webcam

if not cap.isOpened():
    st.error("❌ Webcam not found! Check your camera settings.")
    cap.release()
else:
    st.write("✅ Webcam connected.")

frame_holder = st.empty()  # Placeholder for live feed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.error("❌ Error capturing frame!")
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    frame_holder.image(frame, channels="RGB", use_column_width=True)  # Update Streamlit UI

    if st.button("Stop"):
        break  # Stop the loop when button is clicked

cap.release()
cv2.destroyAllWindows()
st.write("📌 Webcam closed.")
