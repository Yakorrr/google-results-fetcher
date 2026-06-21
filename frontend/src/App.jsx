import {useState} from 'react';
import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(null);

    // Send search query to the FastAPI backend
    const handleSearch = async () => {
        // Basic validation to prevent empty requests
        if (!query.trim()) return;

        try {
            const response = await fetch('http://localhost:8000/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query}),
            });
            const data = await response.json();
            setResults(data.results);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    // Trigger search on 'Enter' key press
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearch().then(() => {
            });
        }
    };

    // Convert results to JSON and trigger a browser download
    const downloadFile = () => {
        const blob = new Blob([JSON.stringify(results, null, 2)], {
            type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'results.json';
        a.click();
        URL.revokeObjectURL(url); // Clean up memory reference
    };

    return (
        <div className="container">
            <h1>Google Search</h1>
            <div className="search-wrapper">
                <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Enter keyword"
                />
                <button onClick={handleSearch}>Search</button>

                {results && (
                    <div className="download-wrapper">
                        <button
                            onClick={downloadFile}
                            style={{backgroundColor: '#28a745'}}
                        >
                            Download JSON
                        </button>
                    </div>
                )}
            </div>

            <ul className="results-list">
                {results?.map((item, index) => (
                    <li key={index} className="result-item">
                        <a href={item.link} target="_blank" rel="noreferrer">
                            {item.title}
                        </a>
                        <p>{item.snippet}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;