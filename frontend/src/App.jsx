// frontend/App.jsx
import {useState} from 'react';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(null);

    const handleSearch = async () => {
        const response = await fetch('http://localhost:8000/api/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query}),
        });

        const data = await response.json();
        setResults(data.results);
    };

    const downloadFile = () => {
        const blob = new Blob([JSON.stringify(results, null, 2)], {
            type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'results.json';
        a.click();
    };

    return (
        <div>
            <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter keyword"
            />
            <button onClick={handleSearch}>Search</button>

            {results && (
                <button onClick={downloadFile}>Download JSON</button>
            )}
        </div>
    );
}

export default App;