import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")  # Langflow API Token

# Dictionary of supported languages for output
OUTPUT_LANGUAGES = {
  "English": "en",
  "हिंदी (Hindi)": "hi",
  "தமிழ் (Tamil)": "ta",
  "తెలుగు (Telugu)": "te",
  "മലയാളം (Malayalam)": "ml",
  "ಕನ್ನಡ (Kannada)": "kn",
  "ਪੰਜਾਬੀ (Punjabi)": "pa",
  "ગુજરાતી (Gujarati)": "gu",
  "অসমীয়া (Assamese)": "as",
  "বাংলা (Bengali)": "bn",
  "ଓଡିଆ (Odia)": "or",
  "മെ സാഹചര്യ (Meitei)": "mni",
  "བོད་ཡིག (Tibetan)": "bo",
  "சோழி (Chola)": "cv",
  "सिंधी (Sindhi)": "sd",
  "संताली (Santali)": "sat",
  "रामाणी (Rajasthani)": "raj",
  "कश्मीरी (Kashmiri)": "ks",
  "कोकणी (Konkani)": "kok",
  "लद्दाखी (Ladakhi)": "lzh",
  "मराठी (Marathi)": "mr",
  "नेपाली (Nepali)": "ne",
  "भोजपुरी (Bhojpuri)": "bho",
  "संथाली (Santhali)": "sat",
  "सुमेर (Sumerian)": "su",
  "Spanish": "es",
  "French": "fr",
  "German": "de",
  "Chinese (Simplified)": "zh",
  "Chinese (Traditional)": "zh-TW",
  "Japanese": "ja",
  "Korean": "ko",
  "Arabic": "ar",
  "Russian": "ru",
  "Portuguese": "pt",
  "Italian": "it",
  "Dutch": "nl",
  "Swedish": "sv",
  "Turkish": "tr",
  "Polish": "pl",
  "Greek": "el",
  "Thai": "th",
  "Vietnamese": "vi",
  "Finnish": "fi",
  "Czech": "cs",
  "Hungarian": "hu",
  "Romanian": "ro",
  "Hebrew": "he",
  "Ukrainian": "uk",
  "Bengali (Bangladesh)": "bn-BD",
  "Serbian": "sr",
  "Indonesian": "id",
  "Malay": "ms"
}


# Google Cloud Vision Credentials
CREDENTIALS_FILE = "gg.json"

# Langflow API URL
LANGFLOW_API_URL = os.getenv("LANGFLOW_API_URL")
