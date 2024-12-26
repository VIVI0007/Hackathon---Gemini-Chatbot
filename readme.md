# Gemini PDF Chatbot
![Screenshot of the chatbot](image.png "Screenshot")
## Overview
The Gemini PDF Chatbot is an intelligent system designed to extract information from uploaded PDF documents and respond to user queries based on the document content. This project integrates modern AI tools and APIs for effective document processing and conversational interactions.

## Features

### Upload PDFs
- Users can upload PDFs via the sidebar.
- The system processes PDFs to extract text and generate embeddings for contextual understanding.

### Ask Questions
- Users input questions in the chat interface.
- The chatbot retrieves relevant context from the processed documents and generates accurate responses.

### Clear History
- Provides an option to clear chat history and reset the session for new interactions.

### Real-Time Feedback
- Includes loading spinners and success messages to enhance user engagement and provide real-time feedback.

## Technologies Used
- **Streamlit**: For creating a user-friendly interface.
- **Google Generative AI API**: For embedding generation and conversational responses.
- **LangChain**: For handling text splitting, embedding generation, and question-answering.
- **FAISS**: For vector store creation and similarity search.
- **PyPDF2**: For extracting text from PDF files.
- **Python**: For overall project implementation.

## How It Works
1. **Upload PDFs**: Users upload PDFs via the sidebar, and the system processes them to extract text.
2. **Generate Embeddings**: The extracted text is split into chunks and converted into embeddings using Google Generative AI.
3. **Ask Questions**: Users can ask questions in the chat. The chatbot searches for relevant chunks, retrieves context, and generates responses.
4. **Clear History**: Users can reset the chat session at any time.
5. **Feedback**: Users receive visual feedback during processing and interaction.

## Getting Started

### Prerequisites
- Python 3.9 or later
- Google Generative AI API key
- Required Python libraries (listed in `requirements.txt`)

### Setup
1. Clone this repository.
2. Install dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the Google API key in an `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Usage
1. Upload one or more PDFs via the sidebar.
2. Wait for the system to process the files.
3. Ask questions in the chat input box.
4. View responses generated based on the document context.
5. Use the "Clear Chat History" button to reset the session.

## Security
- Implements secure API key handling using environment variables.
- Handles file uploads securely within the application.

## Future Enhancements
- **Bulk Upload Support**: Streamline handling of multiple PDFs.
- **Advanced UI**: Improve user experience with interactive elements.
- **Streaming APIs**: Real-time response generation for smoother interactions.
- **Enhanced Verification**: Techniques to prevent hallucinations by grounding responses in source material.

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Hackathon organizers and mentors for their guidance.
- Open-source contributors for the tools and libraries used.
