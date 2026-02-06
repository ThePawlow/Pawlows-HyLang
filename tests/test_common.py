import pytest
from pytest_cases import parametrize_with_cases, case, parametrize
from pathlib import Path
from common import HyLangFile, Translations


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def test_yaml_file() -> Translations:
    return HyLangFile(Path("test.yaml")).load_yaml()


# =============================================================================
# Test Cases: YAML to Lang conversion
# =============================================================================

class YamlToLangCases:
    """Test cases for converting YAML-style dict to lang-style dict."""

    @case(id="simple_nested")
    def case_simple_nested(self):
        yaml_input = {'example': {'entry': "Viewing the Admin Menu"}}
        expected = {'example.entry': "Viewing the Admin Menu"}
        exception = None
        return yaml_input, expected, exception

    @case(id="deeply_nested")
    def case_deeply_nested(self):
        yaml_input = {'a': {'b': {'c': {'d': 'value'}}}}
        expected = {'a.b.c.d': 'value'}
        exception = None
        return yaml_input, expected, exception

    @case(id="multiple_keys_at_same_level")
    def case_multiple_keys(self):
        yaml_input = {
            'messages': {
                'greeting': 'Hello',
                'farewell': 'Goodbye'
            }
        }
        expected = {
            'messages.greeting': 'Hello',
            'messages.farewell': 'Goodbye'
        }
        exception = None
        return yaml_input, expected, exception

    @case(id="single_level")
    def case_single_level(self):
        yaml_input = {'key': 'value'}
        expected = {'key': 'value'}
        exception = None
        return yaml_input, expected, exception

    @case(id="empty_dict_throws")
    def case_empty_dict_throws(self):
        yaml_input = {}
        expected = None
        exception = ValueError
        return yaml_input, expected, exception

    @case(id="none_value_throws")
    def case_none_value_throws(self):
        yaml_input = {'key': {'subkey': None}}
        expected = None
        exception = ValueError
        return yaml_input, expected, exception


# =============================================================================
# Test Cases: Lang to YAML conversion
# =============================================================================

class LangToYamlCases:
    """Test cases for converting lang-style dict to YAML-style dict."""

    @case(id="simple_dotted")
    def case_simple_dotted(self):
        lang_input = {'example.entry': "Viewing the Admin Menu"}
        expected = {'example': {'entry': "Viewing the Admin Menu"}}
        exception = None
        return lang_input, expected, exception

    @case(id="deeply_dotted")
    def case_deeply_dotted(self):
        lang_input = {'a.b.c.d': 'value'}
        expected = {'a': {'b': {'c': {'d': 'value'}}}}
        exception = None
        return lang_input, expected, exception

    @case(id="multiple_keys_shared_prefix")
    def case_multiple_keys_shared_prefix(self):
        lang_input = {
            'messages.greeting': 'Hello',
            'messages.farewell': 'Goodbye'
        }
        expected = {
            'messages': {
                'greeting': 'Hello',
                'farewell': 'Goodbye'
            }
        }
        exception = None
        return lang_input, expected, exception

    @case(id="no_dots")
    def case_no_dots(self):
        lang_input = {'key': 'value'}
        expected = {'key': 'value'}
        exception = None
        return lang_input, expected, exception

    @case(id="empty_dict_throws")
    def case_empty_dict_throws(self):
        lang_input = {}
        expected = None
        exception = ValueError
        return lang_input, expected, exception

class LangToYamlPrefixCases:
    """Test cases for invalid characters in lang-style keys."""

    @parametrize("invalid_key", [
        "mes$sages.greeting",
        "messages.gre$eting",
        "messages.greeting!",
        "mess@ges.greeting",
        "messages.greet#ing",
        "mess ages.greeting",  # space
        "messages..greeting",  # double dot
        ".messages.greeting",  # leading dot
        "messages.greeting.",  # trailing dot
    ])
    @case(id="invalid_char_{invalid_key}")
    def case_invalid_characters(self, invalid_key):
        lang_input = {invalid_key: 'value'}
        expected = None
        exception = ValueError
        return lang_input, expected, exception

# =============================================================================
# Test Cases: Roundtrip conversion
# =============================================================================

class RoundtripCases:
    """Test cases for verifying roundtrip conversion integrity."""

    @case(id="yaml_roundtrip_simple")
    def case_yaml_roundtrip_simple(self):
        original = {'example': {'entry': "Viewing the Admin Menu"}}
        direction = "yaml"
        exception = None
        return original, direction, exception

    @case(id="yaml_roundtrip_complex")
    def case_yaml_roundtrip_complex(self):
        original = {
            'menu': {
                'file': {
                    'new': 'New File',
                    'open': 'Open File',
                    'save': 'Save File'
                },
                'edit': {
                    'undo': 'Undo',
                    'redo': 'Redo'
                }
            }
        }
        direction = "yaml"
        exception = None
        return original, direction, exception

    @case(id="lang_roundtrip_simple")
    def case_lang_roundtrip_simple(self):
        original = {'example.entry': "Viewing the Admin Menu"}
        direction = "lang"
        exception = None
        return original, direction, exception

    @case(id="lang_roundtrip_complex")
    def case_lang_roundtrip_complex(self):
        original = {
            'menu.file.new': 'New File',
            'menu.file.open': 'Open File',
            'menu.edit.undo': 'Undo'
        }
        direction = "lang"
        exception = None
        return original, direction, exception


# =============================================================================
# Tests: YAML to Lang
# =============================================================================

class TestConversion:
    @parametrize_with_cases("yaml_input,expected,exception", cases=YamlToLangCases)
    def test__converts_correctly(self, yaml_input, expected, exception):
        if exception:
            with pytest.raises(exception):
                HyLangFile.convert_yamldict_to_langdict(yaml_input)
        else:
            result = HyLangFile.convert_yamldict_to_langdict(yaml_input)
            assert result == expected

    @parametrize_with_cases("lang_input,expected,exception", cases=LangToYamlPrefixCases)
    def test__lang_to_yaml_prefix_validation(self, lang_input, expected, exception):
        if exception:
            with pytest.raises(exception):
                HyLangFile.convert_langdict_to_yamldict(lang_input)
        else:
            result = HyLangFile.convert_langdict_to_yamldict(lang_input)
            assert result == expected

    @parametrize_with_cases("lang_input,expected,exception", cases=LangToYamlCases)
    def test__converts_correctly(self, lang_input, expected, exception):
        if exception:
            with pytest.raises(exception):
                HyLangFile.convert_langdict_to_yamldict(lang_input)
        else:
            result = HyLangFile.convert_langdict_to_yamldict(lang_input)
            assert result == expected
        
    @parametrize_with_cases("original,direction,exception", cases=RoundtripCases)
    def test__data_survives_full_cycle(self, original, direction, exception):
        """Ensure data survives a full conversion cycle."""
        if exception:
            with pytest.raises(exception):
                if direction == "yaml":
                    flattened = HyLangFile.convert_yamldict_to_langdict(original)
                    HyLangFile.convert_langdict_to_yamldict(flattened)
                else:
                    nested = HyLangFile.convert_langdict_to_yamldict(original)
                    HyLangFile.convert_yamldict_to_langdict(nested)
        else:
            if direction == "yaml":
                flattened = HyLangFile.convert_yamldict_to_langdict(original)
                restored = HyLangFile.convert_langdict_to_yamldict(flattened)
            else:
                nested = HyLangFile.convert_langdict_to_yamldict(original)
                restored = HyLangFile.convert_yamldict_to_langdict(nested)
            assert restored == original


# =============================================================================
# Tests: File Loading (using fixtures)
# =============================================================================

def TestYamlfile():
    def test__can_load(test_yaml_file):
        assert test_yaml_file is not None

    def test__is_data_valid_if_present(test_yaml_file):
        assert test_yaml_file["example"] is not None

    def test__is_exception_thrown_if_data_in_wrong_format():
        with pytest.raises(Exception):
            HyLangFile(Path("invalid.yaml")).load_yaml()