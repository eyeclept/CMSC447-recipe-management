import React,{ useState } from 'react'
import './home-page.css'

export default function App() {
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
        <div class="browse-panel">
           <div>
               <div class="random-shown">RECIPE 1</div>
               <div class="random-shown">RECIPE 2</div>
               <div class="random-shown">RECIPE 3</div>
           </div>
           <div>
               <div class="random-shown">RECIPE 4</div>
               <div class="random-shown">RECIPE 5</div>
               <div class="random-shown">RECIPE 6</div>
               
           </div>
           <div>
               <div class="random-shown">RECIPE 7</div>
               <div class="random-shown">RECIPE 8</div>
               <div class="random-shown">RECIPE 9</div>
               
           </div>
        </div>
    </div>
    
</body>
    </>
  )
}

