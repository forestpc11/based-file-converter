import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import fitz
import os
from moviepy import VideoFileClip  # corrected
import subprocess  #  ffmpeg


def open_file(filetypes):
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    if not file_path:
        messagebox.showwarning("No File", "No file selected.")
    return file_path


def update_status(message):
    status_bar.config(text=message)
    window.update_idletasks()


def convert_pdf_to_docx():
    try:
        update_status("Converting PDF to DOCX...")
        pdf_path = open_file([("PDF Files", "*.pdf")])
        if not pdf_path:
            return

        docx_path = pdf_path.replace(".pdf", "_converted.docx")
        doc = Document()
        os.makedirs("pdf_images", exist_ok=True)
        pdf = fitz.open(pdf_path)

        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text")
            if text:
                for line in text.split('\n'):
                    doc.add_paragraph(line)

            for img_index, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_filename = os.path.join("pdf_images", f"page{page_num}_img{img_index}.{image_ext}")
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)

                doc.add_picture(image_filename)
#HERE
        doc.save(docx_path)
        update_status(f"Conversion complete! Saved as {docx_path}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def convert_mp4_to_wav():
    try:
        update_status("Converting MP4 to WAV...")
        video_path = open_file([("MP4 Files", "*.mp4")])
        if not video_path:
            return

        audio_path = video_path.replace(".mp4", ".wav")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        update_status(f"Audio extracted and saved as {audio_path}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def convert_mp3_to_wav():
    try:
        update_status("Converting MP3 to WAV...")
        mp3_path = open_file([("MP3 Files", "*.mp3")])
        if not mp3_path:
            return

        wav_path = mp3_path.replace(".mp3", ".wav")

        # convert
        subprocess.run(["ffmpeg", "-i", mp3_path, wav_path], check=True)
        update_status(f"MP3 converted to WAV and saved as {wav_path}")
    except subprocess.CalledProcessError as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"ffmpeg failed: {e}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def convert_docx_to_pdf():
    try:
        update_status("Converting DOCX to PDF...")
        docx_path = open_file([("DOCX Files", "*.docx")])
        if not docx_path:
            return

        pdf_path = docx_path.replace(".docx", ".pdf")
        doc = Document(docx_path)
        pdf_writer = fitz.open()

        for para in doc.paragraphs:
            pdf_writer.new_page().insert_text((0, 0), para.text)

        pdf_writer.save(pdf_path)
        update_status(f"DOCX converted to PDF and saved as {pdf_path}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def convert_mov_to_mp4():
    try:
        update_status("Converting MOV to MP4...")
        mov_path = open_file([("MOV Files", "*.mov")])
        if not mov_path:
            return
#thanks alot billy
        mp4_path = mov_path.replace(".mov", ".mp4")
        subprocess.run(["ffmpeg", "-i", mov_path, mp4_path], check=True)
        update_status(f"MOV converted to MP4 and saved as {mp4_path}")
    except subprocess.CalledProcessError as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"ffmpeg failed: {e}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


window = tk.Tk()
window.title("File Converter")
window.geometry("400x300")

# status bar
status_bar = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Buttons
pdf_button = tk.Button(window, text="Select PDF and Convert to DOCX", command=convert_pdf_to_docx)
pdf_button.pack(pady=10)

mov_button = tk.Button(window, text="Select MOV and Convert to MP4", command=convert_mov_to_mp4)
mov_button.pack(pady=10)

mp4_button = tk.Button(window, text="Select MP4 and Convert to WAV", command=convert_mp4_to_wav)
mp4_button.pack(pady=10)

mp3_button = tk.Button(window, text="Select MP3 and Convert to WAV", command=convert_mp3_to_wav)
mp3_button.pack(pady=10)

docx_button = tk.Button(window, text="Select DOCX and Convert to PDF", command=convert_docx_to_pdf)
docx_button.pack(pady=10)

window.mainloop()
