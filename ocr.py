from typing import Tuple

def extract_text_from_image_if_possible(path: str) -> Tuple[str, str | None]:
    """
    Tries to OCR the given image path. If Tesseract is not installed,
    returns a friendly note and empty text so the app remains stable.
    """
    note = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        note = ("OCR note: Tesseract is not installed on this system. "
                "Install it to enable OCR for images.")
        return "", note

    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return text or "", None
    except Exception as e:
        return "", f"OCR failed: {e}"
