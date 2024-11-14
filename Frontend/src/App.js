import React, { useState } from 'react';
import './Login.css';
import Login from './Login';
import Register from './Register';
import './App.css';
import './Register.css';
import HomePage from './components/HomePage';
import UserAnalytics from './components/UserAnalytics';
import axios from 'axios';

function App() {
  const [handle, setHandle] = useState('');
  const [userData, setUserData] = useState(null);
  const [ratingHistory, setRatingHistory] = useState([]);
  const [problemStats, setProblemStats] = useState(null);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [loading, setLoading] = useState(false);

  // Function to fetch user data from Codeforces API
  const fetchUserData = async (username) => {
    setLoading(true); // Start loading indicator
    try {
      const userResponse = await axios.get(`https://codeforces.com/api/user.info?handles=${username}`);
      setUserData(userResponse.data.result[0]);

      const ratingResponse = await axios.get(`https://codeforces.com/api/user.rating?handle=${username}`);
      setRatingHistory(ratingResponse.data.result);

      const problemStatsResponse = await axios.get(`https://codeforces.com/api/user.status?handle=${username}`);
      const problems = problemStatsResponse.data.result;

      const problemDifficulties = {};
      const verdicts = {};
      const languages = {};

      problems.forEach((problem) => {
        if (problem.verdict === 'OK') {
          const difficulty = problem.problem.rating || 'Unrated';
          problemDifficulties[difficulty] = (problemDifficulties[difficulty] || 0) + 1;
        }
        verdicts[problem.verdict] = (verdicts[problem.verdict] || 0) + 1;
        languages[problem.programmingLanguage] = (languages[problem.programmingLanguage] || 0) + 1;
      });

      setProblemStats({
        totalSolved: Object.values(problemDifficulties).reduce((a, b) => a + b, 0),
        difficulties: problemDifficulties,
        verdicts,
        languages,
      });

      setError(null);
    } catch (err) {
      setError('User not found or API error');
      setUserData(null);
      setRatingHistory([]);
      setProblemStats(null);
    } finally {
      setLoading(false); // Stop loading indicator
    }
  };

  // Handle form submission to fetch user data
  const handleSubmit = (e) => {
    e.preventDefault();
    if (handle) fetchUserData(handle);
  };

  // Navigation function to change the current page
  const navigateTo = (page) => setCurrentPage(page);

  return (
    <div className="App">
      {/* Render HomePage component */}
      {currentPage === 'home' && (
        <HomePage
          onLoginClick={() => navigateTo('login')}
          onRegisterClick={() => navigateTo('register')}
          onUserAnalyticsClick={() => navigateTo(isAuthenticated ? 'userAnalytics' : 'login')}
        />
      )}

      {/* Render Login component */}
      {currentPage === 'login' && (
        <Login
          onLogin={(username) => {
            setIsAuthenticated(true);
            setHandle(username); // Update handle in state
            fetchUserData(username); // Fetch data based on the entered username
            navigateTo('userAnalytics');
          }}
          onSwitch={() => navigateTo('register')}
          onBackToHome={() => navigateTo('home')}
        />
      )}

      {/* Render Register component */}
      {currentPage === 'register' && (
        <Register
          onRegister={(username) => {
            setIsAuthenticated(true);
            setHandle(username); // Update handle in state
            fetchUserData(username); // Fetch data based on the entered username
            navigateTo('userAnalytics');
          }}
          onSwitch={() => navigateTo('login')}
          onBackToHome={() => navigateTo('home')}
        />
      )}

      {/* Render UserAnalytics component for authenticated users */}
      {currentPage === 'userAnalytics' && isAuthenticated && (
        <UserAnalytics
          handle={handle}
          setHandle={setHandle}
          handleSubmit={handleSubmit}
          userData={userData}
          error={error}
          ratingHistory={ratingHistory}
          problemStats={problemStats}
          loading={loading}
          onBackToHome={() => navigateTo('home')}
        />
      )}
    </div>
  );
}

export default App;
