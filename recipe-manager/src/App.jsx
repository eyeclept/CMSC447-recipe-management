import { useEffect, useState } from 'react'
import {Router, Route, Routes } from 'react-router-dom';
import { BrowserRouter } from "react-router-dom";
import './App.css'
import ReactDOM from 'react-dom/client'
import React from 'react'
import './index.css'




function changeURL(pathName){
  window.location.pathname = pathName;
}


function App() {

  return (
    
      <Routes>
        <Route path='/view' element={<ViewPage />}/>
        <Route path='/login' element={<LoginPage />} />
        <Route path="/search" element={<SearchPage />}/>
        <Route path="/" element={<HomePage />} />
        <Route path="/myrecipes" element={<MyRecipes />} />
        <Route path='/myfavorites' element={<MyFavorites />} />
      </Routes>
    
    
  );
}

function HomePage(){
/*{data.map((recipe, index) => (
            <div key={index} className="random-shown">
              {recipe.name} */


  const [data, setData] = useState([]);
  useEffect(() => {
      const fetchRandom = async () => {
        try{
          const response = await fetch('/recipes/trending');
          if(!response.ok){
            throw new Error("Failed to Fetch Data");
          }
          const recipe = await response.json();
          setData(prevRecipes => [...prevRecipes, recipe])

        }
        catch(error){
          console.error("Could not fetch Recipe", error);
        }
      };
      for(let i = 0; i < 9; i++){
        fetchRandom();
      }

    },[]);

  return (
    
    <body>
    <div className="left-section">

        <div className="option-box">
            <button className="option-buttons" onClick={() => changeURL('/')}>Home</button>
            <button className="option-buttons" onClick={() => changeURL('/search')}>Search</button>
            <button className="option-buttons" onClick={() => changeURL('/myrecipes')}>My Recipes</button>
            <button className="option-buttons" onClick={() => changeURL('/myfavorites')}>Favorites</button>
        </div>
    </div>
    
    <div className="center-section">
        <button className="account-options" onClick={() => changeURL('/login')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <div className="browse-panel">
           <div>
               <div className="random-shown">RECIPE 1</div>
               <div className="random-shown">RECIPE 2</div>
               <div className="random-shown">RECIPE 3</div>
           </div>
           <div>
               <div className="random-shown">RECIPE 4</div>
               <div className="random-shown">RECIPE 5</div>
               <div className="random-shown">RECIPE 6</div>
               
           </div>
           <div>
               <div className="random-shown">RECIPE 7</div>
               <div className="random-shown">RECIPE 8</div>
               <div className="random-shown">RECIPE 9</div>
               
           </div>
        </div>
    </div>
    
</body>
  );
}

function LoginPage(){
  return(
    <body>
  <div className="login-page">
    <div className="website-name">Website Name (TM)</div>
    
    
    <div>
    <label className="label-login">Username:</label>
    <input className='login-input' type="text"></input>
    </div>
    <div>
    <label className="label-login">Password: </label>
    <input className='login-input' type="password"></input>
    </div>

    <div className="button-wrapper">
        
            <button className="login-button">Login</button>
            <button className="login-button">Forgot?</button>
        
    </div>
  </div>
</body>
  )
}

function ViewPage(){
  return(
    <body>
    <div className="left-section">

    <div className="option-box">
      <button className="option-buttons" onClick={() => changeURL('/')}>Home</button>
      <button className="option-buttons" onClick={() => changeURL('/search')}>Search</button>
      <button className="option-buttons" onClick={() => changeURL('/myrecipes')}>My Recipes</button>
      <button className="option-buttons" onClick={() => changeURL('/myfavorites')}>Favorites</button>
    </div>
    </div>
    
    <div className="center-section">
        <button className="account-options" onClick={() => changeURL('/login')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        
        <div className="view-panel">
            <div>
                <button className="view-panel-top">Save</button>
                <button className="view-panel-top">Delete</button>
            </div>
                
            <div>
                <div className="view-panel-middle-left">Intro/Desc</div>
                <div className="view-panel-middle-right">Image(?)</div>
            </div>
            
            <div>
            <div className="view-panel-bottom">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. (Area for recipe)</div>    
            </div>
            
           </div>
        </div>
</body>
  )
}

function SearchPage(){
  return(
    <body>
    <div className="left-section">

        <div className="option-box">
            <button className="option-buttons" onClick={() => changeURL('/')}>Home</button>
            <button className="option-buttons" onClick={() => changeURL('/search')}>Search</button>
            <button className="option-buttons" onClick={() => changeURL('/myrecipes')}>My Recipes</button>
            <button className="option-buttons" onClick={() => changeURL('/myfavorites')}>Favorites</button>
        </div>
    </div>
    
    <div className="center-section">
        <button className="account-options" onClick={() => changeURL('/login')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        
        <div>
        <input type="text"></input>
        <button className="filter-button">Filter Options</button>
        </div>
        
        <div className="browse-panel">
           <div>
               <div className="random-shown">RECIPE 1</div>
               <div className="random-shown">RECIPE 2</div>
               <div className="random-shown">RECIPE 3</div>
           </div>
           <div>
               <div className="random-shown">RECIPE 4</div>
               <div className="random-shown">RECIPE 5</div>
               <div className="random-shown">RECIPE 6</div>
               
           </div>
        </div>
    </div>
    
</body>
  );
}

function MyRecipes(){
    const [data, setData] = useState('');

  return (
    
    <body>
    <div className="left-section">

        <div className="option-box">
            <button className="option-buttons" onClick={() => changeURL('/')}>Home</button>
            <button className="option-buttons" onClick={() => changeURL('/search')}>Search</button>
            <button className="option-buttons" onClick={() => changeURL('/myrecipes')}>My Recipes</button>
            <button className="option-buttons" onClick={() => changeURL('/myfavorites')}>Favorites</button>
        </div>
    </div>
    
    <div className="center-section">
        <button className="account-options" onClick={() => changeURL('/login')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <div className="browse-panel">
           <div>
               <div className="random-shown">RECIPE 1</div>
               <div className="random-shown">RECIPE 2</div>
               <div className="random-shown">RECIPE 3</div>
           </div>
           <div>
               <div className="random-shown">RECIPE 4</div>
               <div className="random-shown">RECIPE 5</div>
               <div className="random-shown">RECIPE 6</div>
               
           </div>
           <div>
               <div className="random-shown">RECIPE 7</div>
               <div className="random-shown">RECIPE 8</div>
               <div className="random-shown">RECIPE 9</div>
               
           </div>
        </div>
    </div>
    
</body>
  );
}

function MyFavorites(){
  const [data, setData] = useState('');

  return (
    
    <body>
    <div className="left-section">

        <div className="option-box">
            <button className="option-buttons" onClick={() => changeURL('/')}>Home</button>
            <button className="option-buttons" onClick={() => changeURL('/search')}>Search</button>
            <button className="option-buttons" onClick={() => changeURL('/myrecipes')}>My Recipes</button>
            <button className="option-buttons" onClick={() => changeURL('/myfavorites')}>Favorites</button>
        </div>
    </div>
    
    <div className="center-section">
        <button className="account-options" onClick={() => changeURL('/login')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <div className="browse-panel">
           <div>
               <div className="random-shown">RECIPE 1</div>
               <div className="random-shown">RECIPE 2</div>
               <div className="random-shown">RECIPE 3</div>
           </div>
           <div>
               <div className="random-shown">RECIPE 4</div>
               <div className="random-shown">RECIPE 5</div>
               <div className="random-shown">RECIPE 6</div>
               
           </div>
           <div>
               <div className="random-shown">RECIPE 7</div>
               <div className="random-shown">RECIPE 8</div>
               <div className="random-shown">RECIPE 9</div>
               
           </div>
        </div>
    </div>
    
</body>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    {<App />}
  </BrowserRouter>
);

export default App
