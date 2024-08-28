import deepl

def translate_text(text, target_lang='ES'):
    """    Translates all of the detected language (no matter what it is) into spanish     """
    auth_key = '658517c8-cb91-4bfe-9412-fca13e1c578d:fx'  # DeepL API key
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
