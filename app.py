import io
import requests
import streamlit as st
from datetime import datetime
# from pydub import AudioSegment 
from midi2audio import FluidSynth  # Required for MIDI to WAV conversion
import tempfile

# Imports
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

apiUrl = "http://127.0.0.1:8000/test?media_type=midi"

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
    music_file = None

    with st.form(key="my_form"):
        format = st.selectbox("Select a file format", ["midi", "wav", "mp3"], help="Choose a file format")
        image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image file")
        option = st.selectbox("Select a key", ["C", "D", "E"], help="Choose a key")
        value = st.slider("Choose a tempo", 0, 200, 120, help="Select a tempo between 0 and 200")
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button and image is not None:
        # Send the file and other data to the FastAPI backend
        files = {'image': image.getvalue()}
        data = {'format': format, 'key': option, 'tempo': value}
        response1 = requests.post("http://localhost:8000/generate", files=files, data=data) # TODO: replace placeholder with  proper api url
        response = requests.get(apiUrl) # TODO: replace placeholder with  proper api url
        
        # print(f"Response1 status: {response1.status_code}")
        # print(response1)
        # print(f"Response1 content: {response1.content}")
        # print("\n")
        # print(f"Response status: {response.status_code}")
        # print(response)
        # print(f"Response content: {response.content}")

        
        if response.status_code == 200:
            # music_file = response.json().get(format)
            music_file = response.content
            
            if format == "midi":
                # Convert MIDI to WAV for playback using midi2audio
                with tempfile.NamedTemporaryFile(suffix=".mid") as midi_tempfile:
                    midi_tempfile.write(music_file)
                    midi_tempfile.flush()

                    fs = FluidSynth()
                    with tempfile.NamedTemporaryFile(suffix=".wav") as wav_tempfile:
                        fs.midi_to_audio(midi_tempfile.name, wav_tempfile.name)
                        
                        # Play the WAV file
                        st.markdown("### File Output")
                        st.audio(wav_tempfile.read(), format="audio/wav", start_time=0)

            else:
                st.markdown("### File Output")
                st.audio(music_file, format=f"audio/{format}", start_time=0)

            
            st.download_button(
                label=f"Download {format.upper()} File",
                data=music_file,
                file_name=f"your_music_file.{ 'mid' if format == 'midi' else format }",
                mime=f"audio/{format}"
            )
        else:
            st.error(f"Failed to generate {format.upper()} file.")

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