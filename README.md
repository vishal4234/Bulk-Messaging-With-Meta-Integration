# Bulk Messaging with Meta Integration

## 📌 Project Overview
Bulk Messaging with Meta Integration is a web-based platform that enables businesses to send bulk messages via WhatsApp. The project leverages Flask and MongoDB to provide an efficient messaging solution for organizations to engage customers through automated and personalized messaging.

## 🚀 Features
- **Bulk Messaging**: Send messages to multiple users simultaneously.
- **WhatsApp Integration**: Utilizes WhatsApp for message delivery.
- **User Authentication**: Secure login and registration system.
- **Custom Message Templates**: Users can create and manage message templates.
- **CSV Upload Support**: Bulk import contacts from CSV files.
- **Message Tracking**: View message status and analytics.
- **Data Security**: Ensures compliance with WhatsApp policies and data privacy regulations.

## 🏗️ Tech Stack
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Cloud Infrastructure**: AWS (Optional)

## 📂 Project Structure
```
Bulk-Messaging-Meta/
│── static/               # Frontend assets (CSS, JS)
│── templates/            # HTML templates
│── uploads/              # Uploaded CSV files
│── app.py                # Main Flask application
│── process.py            # WhatsApp message automation script
│── requirements.txt       # Project dependencies
│── README.md             # Project documentation
```

## 🛠️ Installation & Setup
### Prerequisites
- Python 3.x
- MongoDB installed locally or on cloud (MongoDB Atlas)
- WhatsApp Web account

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bulk-messaging-meta.git
   cd bulk-messaging-meta
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure MongoDB connection in `app.py`:
   ```python
   client = MongoClient("your-mongodb-connection-string")
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```
5. Open the application in your browser at `http://127.0.0.1:8080/`

## 📌 Usage
1. **Register/Login**: Create an account and log in.
2. **Upload Contacts**: Add contacts manually or upload a CSV file.
3. **Create Templates**: Define and save message templates.
4. **Send Messages**: Select contacts and send messages through WhatsApp.
5. **Track Messages**: Monitor delivery status and logs.

## 📈 Future Enhancements
- AI-powered chatbots for automated replies.
- Improved analytics and reporting dashboard.
- Multi-platform support (SMS, Email, etc.).
- Enhanced security and encryption mechanisms.

## 🤝 Contributors
- Vishaka Kolambe
- Janhavi Narkhede
- Harshada Pimpale
- Vishal Prajapati

## 📜 License
This project is licensed under the MIT License.

