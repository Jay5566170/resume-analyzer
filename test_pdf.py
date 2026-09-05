from backend.app.utils.pdf_parser import extract_text

# Test with your uploaded file
file_path = "backend/uploads/Mujahid_Khan_CV_PearlSolutions_PythonIntern.pdf"
text = extract_text(file_path)

print(f"📄 Extracted text length: {len(text)}")
print(f"📄 First 200 characters: {text[:200]}")