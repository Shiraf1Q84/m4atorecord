# Video to Minutes Converter

This is a Streamlit app that allows you to convert a video file into minutes of text. It uses the OpenAI API for audio transcription and ChatGPT for summarization and creating minutes.

## Installation and Setup

Before running the app, make sure you have the required libraries installed. You can install them using pip:

```bash
pip install streamlit openai moviepy pydub python-dotenv
```

## Getting Started

1. Obtain an OpenAI API Key:
   - You need to have an OpenAI API key to use this app. If you don't have one, sign up at [OpenAI](https://beta.openai.com/signup/) to get your API key.

2. Create a `.env` file:
   - Create a file named `.env` in the same directory as this script.
   - Add your OpenAI API key to the `.env` file like this:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

3. Run the App:
   - Run the Streamlit app by executing the following command in your terminal:
     ```bash
     streamlit run app.py
     ```

4. Use the App:
   - Once the app is running, you can upload a video file (in MP4 format).
   - The app will convert the video to audio, split it into manageable chunks, transcribe the audio, and then summarize the transcriptions.
   - You can then view and download the generated minutes.

## App Workflow

1. **Set API Key**:
   - Enter your OpenAI API key in the sidebar.

2. **Upload Video**:
   - Click the "Upload a video file" button and select a video file (MP4 format).

3. **Processing**:
   - The app will process the video by converting it to audio, splitting the audio into chunks, transcribing each chunk, and summarizing the transcriptions.

4. **Generated Minutes**:
   - The app will display the generated minutes of text in the main section.

5. **Copy and Download**:
   - You can copy the minutes by clicking the "Copy the Script" button.
   - To download the minutes as a text file, click the "Download Minutes" button.

