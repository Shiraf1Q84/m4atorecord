import streamlit as st
import os
import openai
from pydub import AudioSegment
import tempfile

# Initialize the OpenAI API
def get_api():
    user_api_key = st.sidebar.text_input(
        label="OpenAI API key",
        placeholder="Paste your OpenAI API key here",
        type="password"
    )
    return user_api_key

# Function to convert M4A to MP3
def convert_m4a_to_mp3(m4a_file_path):
    mp3_file_path = os.path.splitext(m4a_file_path)[0] + '.mp3'
    audio = AudioSegment.from_file(m4a_file_path, format="m4a")
    audio.export(mp3_file_path, format="mp3")
    return mp3_file_path

def split_audio(mp3_file_path, interval_ms, output_folder):
    audio = AudioSegment.from_file(mp3_file_path)
    file_name, ext = os.path.splitext(os.path.basename(mp3_file_path))
    mp3_file_path_list = []
    n_splits = len(audio) // interval_ms
    for i in range(n_splits + 1):
        start = i * interval_ms
        end = (i + 1) * interval_ms
        split = audio[start:end]
        output_file_name = os.path.join(output_folder, f"{file_name}_{i}.mp3")
        split.export(output_file_name, format="mp3")
        mp3_file_path_list.append(output_file_name)
    return mp3_file_path_list

def transcribe_audio(mp3_file_path, api_key):
    try:
        openai.api_key = api_key  # Set the API key
        with open(mp3_file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']
    except Exception as e:
        return f"Error in transcribe_audio: {str(e)}"

import openai
import openai
import streamlit


def generate_minutes_chunks(transcription_list, agenda_text, api_key, max_tokens=2048, model="gpt-3.5-turbo"):
    chunks = []
    for text in transcription_list:
        prompt = "##The following text is a transcription a conversation that took place at the meeting. The agenda for the meeting is as follow##agenda_text = {" + agenda_text + "} "+ "##The following is the content of the meeting.##text ={" + text + "}"
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional minute-taker.Be sure to answer in Japanese.Please complement as much as possible, taking into account the context, any misspellings or unintelligible meanings."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,  # Adjust as needed
            api_key=api_key,
            # stream=True,
        )
        # result_area = streamlit.empty()
        # text = ''
        # for chunk in response:
        #     next = chunk.choices[0].message.content
        #     text += next
        #     result_area.write(text)
            
        minutes_chunk = response.choices[0].message.content
        chunks.append(minutes_chunk)
        st.write(f"Chunk :")
        st.write(minutes_chunk)
        st.write("----")
    return chunks



def main():
    st.title("議事録生成📑")

    user_api_key = get_api()

    # Add agenda upload
    agenda_text = st.text_area("Upload Meeting Agenda (Text)", height=500)

    uploaded_file = st.file_uploader("Upload an audio file", type=["m4a"])

    if uploaded_file:
        st.sidebar.info("Processing... Please wait.")

        temp_dir_path = tempfile.mkdtemp()
        m4a_file_path = os.path.join(temp_dir_path, "uploaded.m4a")
        uploaded_file.seek(0)
        with open(m4a_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.sidebar.text("Converting audio to mp3...")
        mp3_file_path = convert_m4a_to_mp3(m4a_file_path)
        st.sidebar.text("Splitting audio into chunks...")
        interval_ms = 200_000  # 60 seconds = 60,000 milliseconds
        mp3_file_path_list = split_audio(mp3_file_path, interval_ms, temp_dir_path)
        st.sidebar.text("Transcribing and summarizing...")

        transcription_list = [transcribe_audio(mp3_file, user_api_key) for mp3_file in mp3_file_path_list]

        st.sidebar.text("Processing complete!")

        # Include agenda text in minutes generation with chunks
        minutes_chunks = generate_minutes_chunks(transcription_list, agenda_text, user_api_key)

        st.subheader("Generated Minutes")

        # for i, chunk in enumerate(minutes_chunks):
        #     st.write(f"Chunk {i + 1}:")
        #     st.write(chunk)
        #     st.write("----")

        st.button("Copy the Script")
        #st.download_button(
        #    "Download Minutes",
        #    "\n\n".join(minutes_chunks).encode("utf-8"),
        #    file_name="minutes.txt",
        #    key="download-button",
        #)

if __name__ == "__main__":
    main()
