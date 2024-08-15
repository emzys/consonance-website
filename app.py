import streamlit as st
from datetime import datetime

# Custom CSS
st.markdown(
    """
    <style>
    /* Sticky Navbar */
    nav {
        margin-top: 60px; /* TODO: delete when stupid streamlit header is not in the way anymore */
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #f8f9fa;
        padding: 10px 48px;
        z-index: 1000; /* Ensure it stays on top */
        display: flex;
        justify-content: space-between;
    }
    
    nav form {
        display: flex;
        align-items: center;
    }

    nav button {
        padding: 8px 16px;
        font-size: 16px;
        cursor: pointer;
    }
    
    nav button:hover {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
    }

    /* Sticky Footer */
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f8f9fa;
        padding: 10px;
        text-align: center;
        z-index: 1000; /* Ensure it stays on top */
    }
    
    button {
        transition: border-color 0.3s ease, color 0.3s ease;
    }
    
    .btn-refresh {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 2.5rem;
        margin: 0px;
        line-height: 1.6;
        color: inherit;
        width: auto;
        user-select: none;
        background-color: rgb(255, 255, 255);
        border: 1px solid rgba(49, 51, 63, 0.2);
    }

    /* Ensure content doesn't hide behind navbar and footer */
    .main {
        margin-top: 70px; /* Space for the navbar */
        margin-bottom: 50px; /* Space for the footer */
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    st.title("Convert music sheet to MIDI:")

# Body with a form and file display
def body():
    midi_file = None

    with st.form(key="my_form"):
        image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], help="Choose an image file")
        option = st.selectbox("Select a key", ["key1", "key2", "key3"], help="Choose a key")
        value = st.slider("Choose a value", 0, 100, 50, help="Select a value between 0 and 100")
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        # Simulate API response with a MIDI file
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
