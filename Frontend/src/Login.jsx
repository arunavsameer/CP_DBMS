import React, { useState, useEffect, useRef } from 'react';
import Editor, { loader } from '@monaco-editor/react';
import githubDark from 'monaco-themes/themes/GitHub Dark.json';
import './App.css';
import axios from 'axios';

const Login = ({ onLogin, onSwitch, onBackToHome }) => {
  const defaultCode = `#include <iostream>
using namespace std;

int main(){
    string username = ""; // Enter your username here
    string password = ""; // Enter your password here
    cout << "Welcome, " << username << " !" << endl;
    return 0;
}
  `;

  const [code, setCode] = useState(defaultCode);
  const editorRef = useRef(null);

  useEffect(() => {
    loader.init().then((monacoInstance) => {
      monacoInstance.editor.defineTheme('github-dark', {
        ...githubDark,
        colors: {
          ...githubDark.colors,
          'editor.background': '#000000',
        },
      });
    });
  }, []);

  const handleEditorChange = (value) => {
    setCode(value);
  };

  // In Login.jsx
  const handleRunCode = async () => {
    const usernameMatch = code.match(/string username = "(.*)";/);
    const passwordMatch = code.match(/string password = "(.*)";/);

    const username = usernameMatch ? usernameMatch[1] : '';
    const password = passwordMatch ? passwordMatch[1] : '';

    if (username && password) {
      try {
        const response = await axios.post('http://localhost:5000/api/users/login', { username, password });
        alert(response.data.message);
        onLogin(username);
      } catch (error) {
        alert(error.response ? error.response.data.message : 'Login failed');
      }
    } else {
      alert("Please enter a username and password in the code editor.");
    }
  };

  const handleEditorMount = (editor) => {
    editorRef.current = editor;

    const lineNumber = code.split('\n').findIndex(line => line.includes('string username')) + 1;
    const column = code.indexOf('string username = "') + 'string username = "'.length - code.lastIndexOf('\n', code.indexOf('string username = ""'));

    editor.setPosition({ lineNumber, column });
    editor.focus();
  };

  return (
    <div className="login-page">
      {/* Back to Homepage Button */}
      <button className="back-button" onClick={onBackToHome}>Back to Homepage</button>
      
      <h1 className="header">Codeforces Analytics - Login</h1>
      <div className="editor-container">
        <Editor
          height="38vh"
          defaultLanguage="cpp"
          value={code}
          theme="github-dark"
          onChange={handleEditorChange}
          onMount={handleEditorMount}
          options={{
            fontSize: 20,
            minimap: { enabled: false },
            wordWrap: 'on',
            scrollbar: {
              vertical: 'hidden',
              horizontal: 'hidden',
            },
            overviewRulerLanes: 0,
            scrollBeyondLastLine: false,
            lineNumbers: 'off',
            readOnly: false,
          }}
        />
      </div>
      <div className="button-container">
        <button onClick={handleRunCode}>
          Run Code
        </button>
        <button onClick={onSwitch}>
          Register
        </button>
      </div>
    </div>
  );
};

export default Login;
