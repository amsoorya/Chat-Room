# Multilingual Chat Application

A real-time chat application that allows users to communicate across language barriers through automatic translation.


## Features

- **Real-time messaging** across different languages
- **Automatic translation** between 9 supported languages
- **Multi-room support** for different conversation groups
- **User presence** tracking to see who's online
- **Simple UI** built with Streamlit

## Supported Languages

- English
- Spanish
- French
- German
- Chinese
- Japanese
- Russian
- Arabic
- Hindi

## Requirements

- Python 3.7+
- Streamlit
- googletrans library
- Internet connection for translation services

## Installation

1. Clone this repository or download the source code

2. Install required packages:
   ```bash
   pip install streamlit googletrans==4.0.0-rc1 requests
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Set your username**: Enter a username in the sidebar
2. **Select your language**: Choose your preferred language from the dropdown
3. **Join a room**: Enter a room name and click "Join/Update"
4. **Start chatting**: Type messages in your language, and they'll be automatically translated for others
5. **Refresh chat**: Use the "Refresh Chat" button to manually check for new messages

## How It Works

- Uses a simple file-based database (`chat_data.json`) to store messages and user data
- The Google Translate API translates messages between users with different language preferences
- Messages are automatically displayed in each user's preferred language
- The app automatically refreshes every 5 seconds to check for new messages

## Data Storage

The application stores chat data in a JSON file:
- Chat messages
- User information
- Room details

No personal information beyond usernames is collected.

## Known Issues

- The translation service may occasionally have rate limits or connectivity issues
- File-based storage is not suitable for large-scale deployment

## Future Enhancements

- Database integration for better scalability
- Voice message support
- Media file sharing
- Better offline support

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For questions, feedback, or issues, please contact:

**Jaya Soorya**  
Email: amjayasoorya@gmail.com

## License

This project is open source and available under the [MIT License](LICENSE).
