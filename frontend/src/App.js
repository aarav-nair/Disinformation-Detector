import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent form reload on submit
    try {
      const response = await fetch('/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),  // Send URL as JSON
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();  // Get JSON data from Flask
      setContent(data.content);  // Set the scraped content
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  return (
    <div className="container">
      <h1>Submit a URL</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          required
        />
        <button type="submit">Submit</button>
      </form>
      {content && (
        <div className="result">
          <h2>Scraped Content</h2>
          <p>{content}</p>
        </div>
      )}
    </div>
  );
}

export default App;
