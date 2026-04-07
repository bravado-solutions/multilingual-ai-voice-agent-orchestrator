import os
import azure.cognitiveservices.speech as speechsdk

class SpeechService:
    def __init__(self):
        self.config = speechsdk.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION")
        )
        self.supported_languages = [
            "en-US", "es-ES", "fr-FR", "ar-AE", "hi-IN", 
            "de-DE", "it-IT", "zh-CN", "ja-JP"
        ]
        
        self.auto_detect = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=self.supported_languages
        )
        
        # Mapping for high-quality Neural Voices
        self.voices = {
            "en-US": "en-US-AvaNeural",      # English (US)
            "es-ES": "es-ES-ElviraNeural",   # Spanish (Spain)
            "fr-FR": "fr-FR-DeniseNeural",   # French (France)
            "ar-AE": "ar-AE-FatimaNeural",   # Arabic (UAE)
            "hi-IN": "hi-IN-SwaraNeural",    # Hindi (India)
            "de-DE": "de-DE-KatjaNeural",    # German (Germany)
            "it-IT": "it-IT-ElsaNeural",     # Italian (Italy)
            "zh-CN": "zh-CN-XiaoxiaoNeural", # Chinese (Mandarin)
            "ja-JP": "ja-JP-NanamiNeural"    # Japanese (Japan)
        }

    def listen(self):
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.config,
            auto_detect_source_language_config=self.auto_detect
        )
        print(" Bravado AI is listening...")
        result = recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            lang = result.properties.get(
                speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult
            )
            return result.text, lang
        print(" Could not recognize speech")
        return None, None

    def speak(self, text, lang):
        voice = self.voices.get(lang, "en-US-AvaNeural")
        self.config.speech_synthesis_voice_name = voice
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.config)
        synthesizer.speak_text_async(text).get()
