import requests
import streamlit as st
from datetime import datetime

# import base64
# from io import BytesIO
# from PIL import Image

# Imports
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# apiUrl = "http://127.0.0.1:8000/test?media_type=midi"
apiUrl = "http://127.0.0.1:8000/test_generate"

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
    # usf_file = None # User Selected Format file
    # wav_file = None  # audio file for the player (streamlit won't play a midi file)

    with st.form(key="my_form"):
        format = st.selectbox("Select a file format", ["midi", "wav", "mp3"], help="Choose a file format")
        # images = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image file")
        images = st.file_uploader("Upload images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, help="Choose image files")
        # option = st.selectbox("Select a key", ["C", "D", "E"], help="Choose a key")
        # value = st.slider("Choose a tempo", 0, 200, 120, help="Select a tempo between 0 and 200")
        submit_button = st.form_submit_button(label="Submit")
        
        # # If we watend to submit btn aligned right 
        # button_container = st.container()
        # with button_container:
        #     submit_button = st.form_submit_button(label="Submit")
    
    if submit_button and images is not None:
        files = []
        for image in images:
            files.append(('images', (image.name, image.getvalue(), image.type)))

        data = {'format': format}
        
        response = requests.post("http://localhost:8000/test_generate", files=files, data=data) # TODO: replace placeholder with  proper api url
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            # st.markdown("### RESPONSE 200")
            
            response_files = response.json()  # Get the JSON response from FastAPI
            print("🌼🌼 response_files >>>>>\n")
            print(response_files)
            loaded = False
            
            for idx, file_dict in enumerate(response_files):
                st.markdown(f"### Files for Uploaded Image #{idx + 1}:")
                usf_file = None # User Selected Format file
                wav_file = None  # audio file for the player (streamlit won't play a midi file)
                
                for file_type, file_url in file_dict.items():
                    print("🌼🌼 file_dict 🌼🌼", file_dict)
                    print("🌼🌼 file_type 🌼🌼", file_type)
                    print("🌼🌼 file_url 🌼🌼", file_url)
                    
                    if file_url:
                        # Fetch the actual content of the file
                        file_content = requests.get(file_url).content
                        
                        if file_type == format:
                            print("🎧🎧 usf_file (file_type == format) 🎧🎧")
                            usf_file = (file_type, file_url, file_content)
                            
                        if file_type == 'wav':
                            print("🎧🎧 wav_file (file_type == 'wav') 🎧🎧")
                            wav_file = (file_type, file_url)
                        
                    else:
                        st.error(f"Failed to generate {format.upper()} file.")
                            
                print("🌼🌼 wav_file 🌼🌼", wav_file)
                print("🌼🌼 usf_file 🌼🌼", usf_file)
                st.audio(wav_file[1], format=f"audio/{wav_file[0]}", start_time=0)
                st.download_button(
                    label=f"Download {usf_file[0].upper()} File",
                    data=usf_file[2],
                    file_name=usf_file[1].split('/')[-1],
                    mime=f"audio/{usf_file[0]}"
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