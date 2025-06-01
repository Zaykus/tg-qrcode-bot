function generateQR() {
    const text = document.getElementById('text').value;
    const color = document.getElementById('qr-color').value;
    
    if (!text) {
        alert('Please enter some text first!');
        return;
    }

    // Clear previous QR code
    document.getElementById('qrcode').innerHTML = '';

    // Generate new QR code with selected color
    QRCode.toCanvas(document.getElementById('qrcode'), text, {
        color: {
            dark: color,
            light: '#ffffff'
        },
        width: 256,
        margin: 1
    }, function (error) {
        if (error) console.error(error);
    });
}

// Initialize Telegram WebApp
if (window.Telegram?.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();
}
