# 📝 Pawlow's HyLang

> A tool for generating `.lang` files from `.toml` files to improve project organization and localization management.

## 📖 Overview

The tool streamlines the process of managing language files in your projects by allowing you to define translations in a structured TOML format and automatically generate the corresponding `.lang` files used by your application/ mod.

## ✨ Features

- 🔄 **TOML to .lang conversion** - Write your translations in easy-to-read TOML format
- 📁 **Improved organization** - Keep all your translations in a centralized, structured format
- ⚡ **Automated generation** - Generate multiple `.lang` files from a single source
- 🔀 **Version control friendly** - TOML files are easier to diff and merge than scattered language files

## 📦 Installation

Ensure Python 3 is installed

## 🚀 Usage

Create a TOML file with your translations:

**translations.toml**
```toml
[en_US]
greeting = "Hello, World!"
farewell = "Goodbye!"
welcome_message = "Welcome to our application"
```

Generate your `.lang` files:

```bash
hylang generate translations.toml --output ./src/main/resources/Server/Languages/
```

**Result:**
```
src/main/resources/Server/Languages/
├── en_US.lang
```

Each `.lang` file contains the key-value pairs for that locale:

**en_US.lang**
```
greeting=Hello, World!
farewell=Goodbye!
welcome_message=Welcome to our application
```

## ⚙️ Configuration

You can customize the output format and behavior using a config file:

**hylang.config.toml**
```toml
[output]
directory = "./src/main/resources/Server/Languages"
```

## 💡 Why Pawlows-HyLang?

- ✅ **Single source of truth** - Maintain all translations in one place
- 🤝 **Better collaboration** - TOML is human-readable and easy for translators to work with
- 📈 **Scalability** - Easily manage translations across multiple languages and projects
- 🔧 **Build integration** - Integrate into your build pipeline for automated generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details
