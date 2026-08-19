# video_agent
## AI Video Agent  An AI powered video assistant that summarizes YouTube videos and uploaded media, extracts key information, and allows users to ask questions about the video through an interactive AI chat.


# AI Video Agent

An AI powered video assistant that allows users to provide a YouTube URL or upload a video and interact with its content using AI.

## Features

* YouTube video processing
* Video and audio transcription
* Automatic video summarization
* Key points extraction
* Action items extraction
* Important decisions extraction
* Question extraction
* Interactive AI chat
* Ask questions about the video
* Retrieval Augmented Generation for context based answers
* Vector based document retrieval
* Streamlit web interface

## How It Works

```text
YouTube URL / Video Upload
          ↓
     Audio Extraction
          ↓
       Transcription
          ↓
       AI Analysis
          ↓
   ┌──────┴──────┐
   ↓             ↓
Summary      Key Information
   ↓             ↓
   └──────┬──────┘
          ↓
     Vector Database
          ↓
      AI Question
       Answering
```

## Technologies Used

* Python
* Streamlit
* Whisper
* LangChain
* ChromaDB
* Large Language Models
* yt-dlp
* FFmpeg
* Pydub

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Make sure FFmpeg is installed and available in your system PATH.

## Environment Variables

Create a `.env` file in the project directory and add your required API keys:

```env
OPENAI_API_KEY=your_api_key_here
```

Do not upload your `.env` file or API keys to GitHub.

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Usage

1. Open the AI Video Agent.
2. Enter a YouTube video URL or upload a local video.
3. Start processing the video.
4. Wait for transcription and AI analysis to complete.
5. View the generated summary and extracted information.
6. Ask questions about the video using the AI chat.

## Project Structure

```text
video-agent/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
└── utils/
    └── audio_processor.py
```

## Future Improvements

* Support for more video platforms
* Multilingual transcription and translation
* Speaker identification
* Timestamp based answers
* Improved video search
* Voice based interaction
* Cloud deployment
* Better document and video processing

## License

This project is created for educational and development purposes.

