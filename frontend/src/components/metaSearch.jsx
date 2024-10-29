import React, { useState } from 'react';
import { Search, Globe, Settings, Loader2 } from 'lucide-react';
import styles from './MetaSearch.module.css';

const MetaSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedEngines, setSelectedEngines] = useState({
    google: true,
    bing: true,
    duckduckgo: true
  });

  const searchEngines = [
    { id: 'google', name: 'Google' },
    { id: 'bing', name: 'Bing' },
    { id: 'duckduckgo', name: 'DuckDuckGo' }
  ];

  const mockSearch = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mockResults = [
      {
        title: 'Sample Result 1',
        description: 'This is a description for the first search result that matches your query.',
        url: 'https://example.com/1',
        engine: 'google'
      },
      {
        title: 'Sample Result 2',
        description: 'Another relevant search result from a different search engine.',
        url: 'https://example.com/2',
        engine: 'bing'
      },
      {
        title: 'Sample Result 3',
        description: 'A third search result from yet another search engine.',
        url: 'https://example.com/3',
        engine: 'duckduckgo'
      }
    ];
    
    setResults(mockResults);
    setLoading(false);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      mockSearch();
    }
  };

  const toggleEngine = (engineId) => {
    setSelectedEngines(prev => ({
      ...prev,
      [engineId]: !prev[engineId]
    }));
  };

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.logoWrapper}>
            <Globe className={styles.logo} />
            <h1 className={styles.title}>MetaSearch</h1>
          </div>
          <Settings className={styles.settingsIcon} />
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className={styles.searchForm}>
          <div className={styles.searchWrapper}>
            <div className={styles.inputWrapper}>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your search query..."
                className={styles.searchInput}
              />
              <Search className={styles.searchIcon} />
            </div>
            <button
              type="submit"
              disabled={loading}
              className={styles.searchButton}
            >
              Search
            </button>
          </div>
        </form>

        {/* Search Engine Toggles */}
        <div className={styles.engineToggles}>
          {searchEngines.map(engine => (
            <button
              key={engine.id}
              onClick={() => toggleEngine(engine.id)}
              className={`${styles.engineButton} ${
                selectedEngines[engine.id] ? styles.active : ''
              } ${styles[engine.id]}`}
            >
              {engine.name}
            </button>
          ))}
        </div>

        {/* Results Section */}
        <div className={styles.resultsWrapper}>
          {loading ? (
            <div className={styles.loader}>
              <Loader2 className="animate-spin" />
            </div>
          ) : (
            results.map((result, index) => (
              <div key={index} className={styles.resultCard}>
                <div className={`${styles.engineLabel} ${styles[result.engine]}`}>
                  {result.engine.charAt(0).toUpperCase() + result.engine.slice(1)}
                </div>
                <a
                  href={result.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.resultTitle}
                >
                  {result.title}
                </a>
                <p className={styles.resultDescription}>{result.description}</p>
                <p className={styles.resultUrl}>{result.url}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MetaSearch;