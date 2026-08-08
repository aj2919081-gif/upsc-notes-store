"""
UPI QR Code generator.
Chalane ke liye (apna UPI ID ke saath):
    python make_qr.py "yourname@upi"
Isse uploads/upi/qr.png ban jayega jise buy page par use kiya jayega.
"""
import os
import sys

UPI_ID = sys.argv[1] if len(sys.argv) > 1 else "yourname@upi"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "upi", "qr.png")

# UPI payment URL
upi_url = f"upi://pay?pa={UPI_ID}&pn=UPSC%20Notes%20Store"

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M

    qr = qrcode.QRCode(version=1, error_correction=ERROR_CORRECT_M, box_size=10, border=3)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print(f"✅ QR code ban gaya: {OUT}")
    print(f"   UPI ID: {UPI_ID}")
except ImportError:
    print("qrcode library install nahi hai. Pehle: pip install qrcode Pillow")
    sys.exit(1)
