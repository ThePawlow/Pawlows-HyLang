# 📝 Pawlow's HyLang
<div align="center">

> A tool for generating `.lang` files from `.yaml` files to improve project organization and localization management.

### Fan of my work?
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E5H93UN)

![GitHub stars](https://img.shields.io/github/stars/ThePawlow/Pawlows-PermKit?style=social)
![GitHub forks](https://img.shields.io/github/forks/ThePawlow/Pawlows-PermKit?style=social)

</div>

---

## ✨ Features
- ✅ **Single source of truth** - Maintain all translations in one place
- 🤝 **Better collaboration** - YAML is human-readable and easy for translators to work with
- 📈 **Scalability** - Easily manage translations across multiple languages and projects
- 🔧 **Build integration** - Integrate into your build pipeline for automated generation

## 📦 Installation
> python3 -m venv .venv && source .venv/bin/activate.fish && pip install . --upgrade pip

## 🚀 Usage
### CLI-Mode
Create a YAML file with your translations:

**translations.yaml**
```yaml
ui:
  greeting: Hello, World!
  farewell: Goodbye!
  welcome_message: Welcome!
```

Generate your `.lang` files:
```bash
./main.py --cli -i ./examples/source_example.yaml --verbose
```

**Result:**
```
src/main/resources/Server/Languages/
├── en_US.lang
```

Each `.lang` file contains the key-value pairs for that locale:

**en_US.lang**
```
ui.greeting=Hello, World!
ui.farewell=Goodbye!
ui.welcome_message=Welcome!
```

### GUI-Mode
Create a YAML file with your translations:

```bash
./main.py
```

## ⚙️ Configuration
You can customize the output format and behavior using a config file:

**hylang.config.yaml**
```yaml
[output]
directory = "./src/main/resources/Server/Languages"
```

## 🤝 Contributing
### 💎 Fan of my work?
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E5H93UN)

### 🌟 Projects using HyLang
- [**Pawlow's PermKit**](https://github.com/ThePawlow/Pawlows-PermKit) - A permission management system utilizing HyLang for localization

## 🛠️ PR
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
MIT License - see LICENSE file for details
