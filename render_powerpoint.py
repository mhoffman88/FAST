import streamlit as st
from pptx import Presentation
from pdf2image import convert_from_bytes
import subprocess
import os

def render_powerpoint_with_pdf():
    """
    Render PowerPoint presentations using PDF conversion for better quality.
    """
    
    st.subheader("📊 PowerPoint Presentations")
    
    # Directory containing PowerPoint files
    pptx_dir = "powerpoints"  # Change this to your directory
    
    # Get list of PowerPoint files
    if not os.path.exists(pptx_dir):
        st.warning(f"No PowerPoint directory found at '{pptx_dir}'")
        return
    
    pptx_files = [f for f in os.listdir(pptx_dir) if f.endswith('.pptx')]
    
    if not pptx_files:
        st.warning("No PowerPoint files found in the directory.")
        return
    
    # User selects which presentation to view
    selected_file = st.selectbox(
        "Select a presentation:",
        pptx_files,
        index=0
    )
    
    pptx_path = os.path.join(pptx_dir, selected_file)
    
    # Load the presentation to count slides
    prs = Presentation(pptx_path)
    total_slides = len(prs.slides)
    
    # Initialize session state for slide navigation
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
    
    # Reset slide counter when a new file is selected
    if 'last_selected_file' not in st.session_state:
        st.session_state.last_selected_file = selected_file
    elif st.session_state.last_selected_file != selected_file:
        st.session_state.current_slide = 0
        st.session_state.last_selected_file = selected_file
    
    # Display current slide number
    st.write(f"**Slide {st.session_state.current_slide + 1} of {total_slides}**")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            if st.session_state.current_slide > 0:
                st.session_state.current_slide -= 1
                st.rerun()
    
    with col2:
        # Slider to jump to specific slide
        slide_number = st.slider(
            "Go to slide:",
            1,
            total_slides,
            st.session_state.current_slide + 1
        )
        st.session_state.current_slide = slide_number - 1
    
    with col3:
        if st.button("Next ➡️", use_container_width=True):
            if st.session_state.current_slide < total_slides - 1:
                st.session_state.current_slide += 1
                st.rerun()
    
    # Convert PowerPoint to PDF and then to images
    try:
        pdf_path = convert_pptx_to_pdf(pptx_path)
        images = convert_from_bytes(open(pdf_path, 'rb').read())
        
        if st.session_state.current_slide < len(images):
            st.image(
                images[st.session_state.current_slide],
                caption=f"Slide {st.session_state.current_slide + 1}",
                use_column_width=True
            )
        else:
            st.error("Could not display slide")
            
    except Exception as e:
        st.error(f"Error rendering presentation: {e}")


def convert_pptx_to_pdf(pptx_path):
    """
    Convert PPTX to PDF using LibreOffice (requires installation).
    Returns the path to the generated PDF.
    """
    pdf_path = pptx_path.replace('.pptx', '.pdf')
    
    try:
        subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pptx_path),
            pptx_path
        ], check=True, capture_output=True)
        
        return pdf_path
        
    except Exception as e:
        raise Exception(f"Error converting PPTX to PDF: {e}")
