import os
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from wordfreq import word_frequency
import whisper_timestamped as whisper

#blank pipeline with ony lemmatizer
source=spacy.load("en_core_web_sm")
nlp = spacy.blank("en")
nlp.add_pipe('lemmatizer',source=source)


# Path to folder containing audio files
folder_path = "/home/zach/Music/"

# Create dictionary to store results
results = {}

model=whisper.load_model("small",device="cpu")

# Loop through all files in the folder
for filename in sorted(os.listdir(folder_path)):
    # Check if file is an audio file
    if filename.endswith(".mp3") or filename.endswith(".wav"):
        file_path = os.path.join(folder_path, filename)
        audio=whisper.load_audio(file_path)
        audio=whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio)
        _, probs = model.detect_language(mel)
        if not max(probs, key=probs.get) == "en":
            continue
        audio=whisper.load_audio(file_path)
        # Transcribe audio file to text using whisper_timestamped
        transcription = whisper.transcribe(model,audio,language="en")
        # Process text with SpaCy
      #  print(transcription)
        
        # Loop through all lemmas in the document
        for segment in transcription['segments']:
            for word in segment['words']:
                word = word['text']
                doc = nlp(word)
                for token in doc:
                    lemma = token.lemma_
                    # Check if lemma is a stop word
                    if lemma not in STOP_WORDS:
                        #check if not a punctuation or number or space or empty or pronoun
                        if not lemma.isspace() and not lemma == "" and not token.pos_ == "PRON" and not token.pos_=="SYM" and not token.pos_=="NUM":
                        # Check if lemma is in results
                            if lemma not in results:
                                # Add lemma to results
                                results[lemma] = {
                                    "frequency": word_frequency(lemma, "en"),
                                    "occurrences": []
                                }
                            # Add occurrence to results
                            results[lemma]["occurrences"].append({
                                "file": file_path,
                                "start": segment['words'][0]['start'],
                                "end": segment['words'][-1]['end']
                            })
        #save
        with open("results.json", "w") as f:
            json.dump(results, f)
        print("Processed", filename)

    else:
        print("File is not an audio file", filename)

# Save results to JSON file
import json
with open("results.json", "w") as f:
    json.dump(results, f)