import React,{ useState } from 'react'
import './login-page.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <body>
  <div class="login-page">
    <div class="website-name">Website Name (TM)</div>
    
    
    <div>
    <label class="label-login">Username:</label>
    <input type="text"></input>
    </div>
    <div>
    <label class="label-login">Password: </label>
    <input type="password"></input>
    </div>

    <div class="button-wrapper">
        
            <button class="login-button">Login</button>
            <button class="login-button">Forgot?</button>
        
    </div>
  </div>
</body>
    </>
  )
}

export default App
