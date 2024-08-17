import requests
import streamlit as st
from datetime import datetime

# Imports
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Navbar with a refresh button
def navbar():
    st.markdown(
        """
        <nav>
            <h4>Consonance</h4>
            <form action="/" method="get">
                <button class="btn-refresh" type="submit">Refresh</button>
            </form>
        </nav>
        """, 
        unsafe_allow_html=True
    )

# Header with app title
def header():
    st.title("Music sheet converter:")

# Body with a form and file display
def body():
    midi_file = None

    with st.form(key="my_form"):
        format = st.selectbox("Select a file format", ["MIDI", "WAV", "mp3"], help="Choose a file format")
        image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image file")
        option = st.selectbox("Select a key", ["C", "D", "E"], help="Choose a key")
        value = st.slider("Choose a tempo", 0, 200, 120, help="Select a tempo between 0 and 200")
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button and image is not None:
        # Send the file and other data to the FastAPI backend
        files = {'image': image.getvalue()}
        data = {'format': format, 'key': option, 'tempo': value}
        response = requests.post("http://localhost:8000/generate", files=files, data=data) # TODO: replace placeholder with  proper api url
        
        if response.status_code == 200:
            midi_file = response.json().get('midi')
            st.markdown("### MIDI File Output")
            st.audio(midi_file, format="audio/midi", start_time=0)
            st.download_button(
                label="Download MIDI File",
                data=midi_file,  # Assuming midi_file is the binary content of the file
                file_name="your_midi_file.mid",
                mime="audio/midi"
            )
        else:
            st.error("Failed to generate MIDI file.")

# Footer with dynamic year
def footer():
    current_year = datetime.now().year
    st.markdown(
        f"""
        <footer>
            {current_year} © Consonance Inc. All rights reserved.
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

    # # Hide the Streamlit viewer badge
    # st.markdown(
    #     """
    #     <script>
    #     document.addEventListener('DOMContentLoaded', function() {
    #         const badge = document.querySelector('.viewerBadge_container__r5tak');
    #         if (badge) {
    #             badge.style.display = 'none';
    #         }
    #     });
    #     </script>
    #     """,
    #     unsafe_allow_html=True
    # )
    
    # # Hide the Streamlit viewer badge
    # st.markdown(
    #     """
    #     <script type="text/javascript">
    #     console.log("SIEMA!")
    #     const hideBadge = () => {
    #         const badge = document.querySelector('.viewerBadge_container__r5tak');
    #         console.log("YELLOW badge",badge)
    #         if (badge) {
    #             badge.style.display = 'none';
    #         }
    #     };

    #     const observer = new MutationObserver(hideBadge);
    #     observer.observe(document.body, { childList: true, subtree: true });

    #     hideBadge();  // Initial check in case the badge is already present
    #     </script>
    #     """,
    #     unsafe_allow_html=True
    # )
    
    # Hide the Streamlit viewer badge
    st.markdown(
        """
        <script type="text/javascript">
        function removeBadge() {
            const badge = document.querySelector('.viewerBadge_container__r5tak');
            if (badge) {
                badge.style.display = 'none';
            }
        }

        // Check for the badge periodically
        const interval = setInterval(removeBadge, 100);

        // Also observe changes in the DOM to detect the badge
        const observer = new MutationObserver(removeBadge);
        observer.observe(document.body, { childList: true, subtree: true });

        // Stop the interval once the badge is removed
        removeBadge();
        </script>
        """,
        unsafe_allow_html=True
    )