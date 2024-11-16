import React, { useState } from 'react';
import { Search, Globe, Settings, Loader2 } from 'lucide-react';
import styles from './MetaSearch.module.css';

const MetaSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 10;

  const mockSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      console.log("DATA", data);
      setResults(data.results);
      setCurrentPage(1);
    } catch (error) {
      console.error('Error fetching data');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      mockSearch();
    }
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

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

        {/* Results Section */}
        <div className={styles.resultsWrapper}>
          {loading ? (
            <div className={styles.loader}>
              <Loader2 className="animate-spin" />
            </div>
          ) : (
            currentResults.map((result, index) => (
              <div key={index} className={styles.resultCard}>
                <a
                  href={result.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.resultTitle}
                  dangerouslySetInnerHTML={{ __html: result.title }}
                />
                <p className={styles.resultDescription}>{result.snippet}</p>
                <p className={styles.resultUrl}>{result.link}</p>
              </div>
            ))
          )}
        </div>

        {/* Pagination Controls */}
        {results.length > resultsPerPage && (
          <div className={styles.pagination}>
            {Array.from(
              { length: Math.ceil(results.length / resultsPerPage) },
              (_, i) => (
                <button
                  key={i + 1}
                  onClick={() => handlePageChange(i + 1)}
                  className={`${styles.pageButton} ${
                    currentPage === i + 1 ? styles.active : ''
                  }`}
                >
                  {i + 1}
                </button>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MetaSearch;
