from src.utils.file_operations import construct_path, files_in_directory, file_to_dict
from .locales import Locales

LOCALES_FILE_PATH = construct_path("src/data/locale/{language}/")
LANGUAGES = ["en"]

class LocaleTranslator():
    _instance = None
    KEYS = Locales
    EXISTING_KEYS = Locales.get_existing_keys()

    def __init__(self) -> None:
        if LocaleTranslator._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of LocaleTranslator.")
        
        self.translations = {}
        for language in LANGUAGES:
            translations = self._load_language(language=language)
            self._validate_translations(translations=translations, language=language)
            self.translations[language] = translations

    @staticmethod
    def _load_language(language: str) -> dict[str, str]:
        translations = {}
        files_path = LOCALES_FILE_PATH.format(language=language)
        for file in files_in_directory(files_path, 'json'):
            file_path = files_path + file
            data = file_to_dict(file_path=file_path)
            LocaleTranslator._validate_data(data=data, language=language, file=file)
            translations.update(data)
        return translations

    @staticmethod
    def _validate_data(data: dict, language: str, file: str) -> None:
        for key in data.keys():
            if key not in LocaleTranslator.EXISTING_KEYS:
                raise RuntimeError(f"An error occured while loading the locales for language {language}: key {key} in file {file} does not exist")
    
    @staticmethod
    def _validate_translations(translations: dict, language: str) -> None:
        for key in LocaleTranslator.EXISTING_KEYS:
            if key not in translations:
                raise RuntimeError(f"An error occured while loading the locales for language {language}: missing key {key}")

    @staticmethod
    def get_instance() -> 'LocaleTranslator':
        if LocaleTranslator._instance is None:
            LocaleTranslator._instance = LocaleTranslator()
        return LocaleTranslator._instance
    
    def get(self, key: str, language: str = "en", **kwargs) -> str:
        language_translations = self.translations.get(language, None)
        if language_translations is None:
            raise ValueError(f"No translations found for language {language}")
        
        translation = language_translations.get(key, None)
        if translation is None:
            print(f"No translation found for key {key}")
            translation = f"key_{key}"

        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                raise RuntimeError(f"An error occured while filling the placeholders in key {key} of language {language}: {e}")
        
        return translation