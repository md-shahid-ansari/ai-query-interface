import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ChatInterface.css';

function ChatInterface() {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([
        { text: 'How may I help you?', sender: 'bot' }
    ]);
    const chatWindowRef = useRef(null);
    const textareaRef = useRef(null);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;

            if (textareaRef.current.scrollHeight > textareaRef.current.clientHeight) {
                textareaRef.current.style.overflowY = 'auto';
            } else {
                textareaRef.current.style.overflowY = 'hidden';
            }
        }
    }, [query]);

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]);

    const handleQuery = async () => {
        if (query.trim() === '') return;

        const userMessage = { text: query, sender: 'user' };
        setMessages((prevMessages) => [...prevMessages, userMessage]);
        setQuery('');

        try {
            const result = await axios.post('http://localhost:5000/query', { query });
            const botMessage = { text: result.data.response || 'Sorry, I didn\'t understand that.', sender: 'bot' };
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error querying the server:', error);
            const errorMessage = { text: 'Error communicating with the server. Please try again later.', sender: 'bot' };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        }
    };

    const handleChange = (e) => {
        setQuery(e.target.value);
    };

    return (
        <div className="chat-interface">
            <h1>AI-Powered Data Query Interface</h1>
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message-wrapper ${msg.sender}`}>
                        <div className={`chat-message ${msg.sender}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
            </div>
            <div className="input-area">
                <textarea
                    ref={textareaRef}
                    value={query}
                    onChange={handleChange}
                    placeholder="Enter your query..."
                    className="form-control"
                />
                <button className="btn btn-primary" onClick={handleQuery}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default ChatInterface;
