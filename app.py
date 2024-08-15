import streamlit as st
from datetime import datetime

# Function to refresh the page
def refresh_page():
    st.experimental_rerun()

# Navbar with a refresh button
def navbar():
    st.markdown(
        """
        <nav style="background-color: #f8f9fa; padding: 10px; text-align: right;">
            <button onclick="window.location.reload();" style="padding: 8px 16px; font-size: 16px; cursor: pointer;">Refresh</button>
        </nav>
        """, 
        unsafe_allow_html=True
    )

# Header with app title
def header():
    st.title("Consonance")

# Body with a form and file display
def body():
    midi_file = None

    with st.form(key="my_form"):
        image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image file")
        option = st.selectbox("Select a key", ["key1", "key2", "key3"], help="Choose a key")
        value = st.slider("Choose a value", 0, 100, 50, help="Select a value between 0 and 100")
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        # Here you would send the form data to your API and get a response with the MIDI file
        # For demonstration purposes, let's simulate an API response
        midi_file = "path_to_your_midi_file.mid"  # Replace with the actual API response

        st.markdown("### MIDI File Output")
        st.audio(midi_file, format="audio/midi", start_time=0)
        st.download_button(
            label="Download MIDI File",
            data=open(midi_file, 'rb').read(),  # Ensure the file is opened in binary mode
            file_name="your_midi_file.mid",
            mime="audio/midi"
        )

# Footer with dynamic year
def footer():
    current_year = datetime.now().year
    st.markdown(
        f"""
        <footer style="background-color: #f8f9fa; padding: 10px; text-align: center;">
            © {current_year} ♥ by the Dream Team. All rights reserved.
        </footer>
        """, 
        unsafe_allow_html=True
    )

# Main layout
def main():
    navbar()
    header()
    body()
    footer()

if __name__ == "__main__":
    main()
