import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from docx import Document
import fitz
import os


#  open file dialog
def open_pdf_file():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:  # if no file is selected
        messagebox.showwarning("No File", "No PDF file selected.")
    return pdf_path



def convert_pdf_to_docx():
    try:
        pdf_path = open_pdf_file()
        if not pdf_path:
            return  

#HERE
        docx_path = pdf_path.replace(".pdf", "_converted.docx")


        doc = Document()
        os.makedirs("pdf_images", exist_ok=True)


        pdf = fitz.open(pdf_path)


        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text")
            if text:
                for line in text.split('\n'):
                    paragraph = doc.add_paragraph(line)


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
        messagebox.showinfo("Success", f"Conversion complete! Saved as {docx_path}")
    except Exception as e:

        messagebox.showerror("Error", f"An error occurred: {str(e)}")



window = tk.Tk()
window.title("PDF to DOCX Converter")
window.geometry("400x200")


pdf_path_label = tk.Label(window, text="No PDF selected", wraplength=300)
pdf_path_label.pack(pady=20)


convert_button = tk.Button(window, text="Select PDF and Convert", command=convert_pdf_to_docx)
convert_button.pack()


window.mainloop()
