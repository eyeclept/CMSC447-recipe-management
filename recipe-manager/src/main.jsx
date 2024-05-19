import ReactDOM from 'react-dom'
import React from 'react'
import { Router, Route, browserHistory, IndexRoute  } from 'react-router'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
