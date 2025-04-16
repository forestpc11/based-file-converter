import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from docx import Document
import fitz
import os
from moviepy import VideoFileClip
import subprocess


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

        doc.save(docx_path)
        update_status(f"Conversion complete! Saved as {docx_path}")
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


def convert_file():
    try:
        input_format = input_format_var.get()
        output_format = output_format_var.get()

        if input_format == output_format:
            messagebox.showinfo("Invalid Selection", "Please select different input and output formats.")
            return

        filetypes = [(f"{input_format.upper()} files", f"*.{input_format.lower()}")]
        input_path = open_file(filetypes)
        if not input_path:
            return

        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.{output_format}"

        update_status(f"Converting {input_format.upper()} to {output_format.upper()}...")

        if input_format in ["mp4", "mov", "mpg", "webm"] and output_format in ["mp3", "wav", "aac", "flac", "wma"]:
            clip = VideoFileClip(input_path)
            clip.audio.write_audiofile(output_path)
        else:
            subprocess.run(["ffmpeg", "-i", input_path, output_path], check=True)

        update_status(f"Conversion complete! Saved as {output_path}")

    except subprocess.CalledProcessError as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"ffmpeg failed: {e}")
    except Exception as e:
        update_status("Error occurred during conversion.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


window = tk.Tk()
window.title("File Converter")
window.geometry("500x400")

frame = tk.Frame(window)
frame.pack(pady=20)

input_label = tk.Label(frame, text="Input Format:")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

input_format_var = tk.StringVar()
input_dropdown = ttk.Combobox(frame, textvariable=input_format_var)
input_dropdown['values'] = ["mp4", "mp3", "wav", "aac", "flac", "mov", "m4a", "wma", "mpg", "webm", "webp"]
input_dropdown.grid(row=0, column=1, padx=5, pady=5)

output_label = tk.Label(frame, text="Output Format:")
output_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

output_format_var = tk.StringVar()
output_dropdown = ttk.Combobox(frame, textvariable=output_format_var)
output_dropdown['values'] = ["mp4", "mp3", "wav", "aac", "flac", "mov", "m4a", "wma", "mpg", "webm", "webp"]
output_dropdown.grid(row=1, column=1, padx=5, pady=5)

convert_button = tk.Button(window, text="Convert File", command=convert_file, height=2, width=20)
convert_button.pack(pady=10)

pdf_button = tk.Button(window, text="Convert PDF to DOCX", command=convert_pdf_to_docx)
pdf_button.pack(pady=5)

docx_button = tk.Button(window, text="Convert DOCX to PDF", command=convert_docx_to_pdf)
docx_button.pack(pady=5)

status_bar = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

window.mainloop()
