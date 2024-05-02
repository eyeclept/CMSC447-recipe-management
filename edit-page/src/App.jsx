import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './view-page.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <body>
    <div class="left-section">
        <h2>Username</h2>
        <div class="option-box">
            <button class="option-buttons">Search</button>
            <button class="option-buttons">My Recipes</button>
            <button class="option-buttons">Favorites</button>
        </div>
    </div>
    
    <div class="center-section">
        <button class="account-options">Sign In</button>
        <button class="account-options">Sign Out</button>
        
        <div class="view-panel">
            <div>
                <button class="view-panel-top">Save</button>
                <button class="view-panel-top">Delete</button>
            </div>
                
            <div>
                <div class="view-panel-middle-left">Intro/Desc</div>
                <div class="view-panel-middle-right">Image(?)</div>
            </div>
            
            <div>
            <div class="view-panel-bottom">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. (Area for recipe)</div>    
            </div>
            
           </div>
        </div>
</body>
    </>
  )
}

export default App
