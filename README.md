# CDP Support Chatbot

## Overview

The **CDP Support Chatbot** is a web-based chatbot designed to provide automated support for Customer Data Platform (CDP) platforms. It pulls relevant information from preloaded documentation for platforms like Segment, mParticle, Lytics, and Zeotap. Built using **Flask** for the backend and **NLTK** for natural language processing, the chatbot answers user queries by matching them to structured documentation files.

## Tech Stack

### Frontend:
- **HTML**: Provides the structure of the web application.
- **CSS**: Styles the application, creating a user-friendly interface.
- **JavaScript**: Manages user interactions, including the dynamic starry background animation and chat interface.

### Backend:
- **Flask (Python)**: Manages the server-side logic, routing, and data handling.
- **NLTK**: Used for natural language processing, including tokenization and query processing.
- **fuzzywuzzy**: Python library for fuzzy string matching to help identify the most relevant responses.

## Features

### Multi-Platform Support:
The chatbot supports four platforms: Segment, mParticle, Lytics, and Zeotap.

### Natural Language Processing:
Uses **NLTK** to tokenize and process user queries.

### Fuzzy Matching:
Implements fuzzy string matching with **fuzzywuzzy** to find the most relevant responses from the documentation.

### Background Animation:
A dynamic starry background for an engaging user experience.

### Interactive Chat Interface:
A simple and responsive chatbox for seamless interaction.

## Technologies Used
- **Python**: Backend language for building the Flask application.
- **Flask**: A lightweight WSGI web framework for creating the chatbot application.
- **NLTK**: Natural Language Toolkit for tokenizing and processing user queries.
- **fuzzywuzzy**: Python library for fuzzy string matching to improve the chatbot's accuracy.
- **JavaScript**: For handling frontend user interactions and dynamic background animation.
- **HTML/CSS**: For building the user interface layout and styling.

## Installation & Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/cdp-support-chatbot.git
    cd cdp-support-chatbot
    ```

2. Set up a virtual environment:

   For Windows:

    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the Flask application:

    ```sh
    python app.py
    ```

## Future Enhancements

1. **Support for More Platforms**:
    Extend the chatbot to support additional CDP platforms such as **Salesforce**, **Adobe Experience Cloud**, and **Braze** to broaden its usability.

2. **User Authentication**:
    Implement user authentication to allow users to personalize their experience, save previous queries, and access additional features such as saved conversations or history.

3. **Advanced NLP Techniques**:
    Use more advanced NLP techniques such as **BERT** or **GPT-3** to improve the accuracy and relevance of responses, especially for more complex or ambiguous queries.

4. **Voice Input Integration**:
    Integrate voice recognition technology (like **Web Speech API** or **Google Cloud Speech-to-Text**) to allow users to ask questions verbally instead of typing them.
Google Cloud Speech-to-Text) to allow users to ask questions verbally instead of typing them.
