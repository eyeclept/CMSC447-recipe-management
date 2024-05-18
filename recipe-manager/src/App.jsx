import { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router-dom';
import { BrowserRouter, Link, useParams } from "react-router-dom";
import './App.css'
import ReactDOM from 'react-dom/client'
import React from 'react'
import './index.css'




function logout(){
  setToken('')
  localStorage.removeItem('recipe-manager-token')

}


function changeURL(pathName){
  window.location.pathname = pathName;
}



function App() {

  return (
    
      <Routes>
        <Route path='/view/:id' element={<ViewPage />}/>
        <Route path='/loginpage' element={<LoginPage />} />
        <Route path="/search" element={<SearchPage />}/>
        <Route path="/" element={<HomePage />} />
        <Route path="/myrecipes" element={<MyRecipes />} />
        <Route path='/myfavorites' element={<MyFavorites />} />
        <Route path='/createuser' element={<RegUser />} />
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
        //try{
          //const response = await fetch('/recipes/trending');
          //if(!response.ok){
            //throw new Error("Failed to Fetch Data");
          //}
          const recipe = {'description': '',
          'directions': '["In saucepan slowly stir the chicken broth into cornstarch. '/
                        'Cook, stirring constantly, until slightly thickened.", "Slowly '/
                        'pour in the well beaten egg; stir once gently.", "Remove from '/
                        'heat. Garnish with sliced green onion.", "Makes 4 servings."]',
          'ingredients': '["2 (13 3/4 oz.) cans chicken broth", "1 Tbsp. cornstarch", '/
                         '"1 well beaten egg", "2 Tbsp. sliced (1/4-inch) green onion"]',
          'keywords': '',
          'recipe_id': '78',
          'title': 'Egg Drop Soup'};//await response.json();
          setData(prevRecipes => [...prevRecipes, recipe])

        //}
        //catch(error){
          //console.error("Could not fetch Recipe", error);
        //}
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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        <div className="browse-panel">
          {data.map((recipe, index) => (
            <Link to={`/view/${recipe.recipe_id}`} className='random-shown' key={index}>
              {recipe.title}
              </Link>
          ))}
          {/* <div>
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
               
           </div>*/}
        </div>
    </div>
    
</body>
  );
}

function LoginPage(){
  function submitLogin(event){
    const username = event.target.username.value;
    const password = event.target.password.value;
    event.preventDefault();
    fetch('/login', {
      method:'POST',
      headers:{'content-type':'application/json'},
      body:JSON.stringify({username, password})
      }
    )
    .then(response => response.json())
    .then(data => {
      console.log('successful login');
      data.localStorage.setItem('recipe-manager-token', data.access_token)
    })
    .catch((error) => {
      console.error('Error when Logging in');
    });
  }

  return(
    <body>
  <div className="login-page">
    <div className="website-name">Website Name (TM)</div>
    
    <form onSubmit={submitLogin}>
      <div>
      
        <label className="label-login">Username:</label>
        <input className='login-input' id='username' type="text" required></input>
        </div>
        <div>
        <label className="label-login">Password: </label>
        <input className='login-input' id='password' type="password" required></input>
      
      </div>
      </form>
    <div className="button-wrapper">
            <button className="login-button" type='submit'>Login</button>
    </div>
  </div>
</body>
  )
}

function RegUser(){

  function createUser(event){
    event.preventDefault();
    const username = event.target.username.value
    const password = event.target.password.value
    fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  return(
    
  <div className="login-page">
    <div className="website-name">Website Name (TM)</div>
    
    <form onSubmit={createUser}>
      <div>
      
        <label className="label-login">Username:</label>
        <input className='login-input' id='username' type="text" required></input>
        </div>
        <div>
        <label className="label-login">Password: </label>
        <input className='login-input' id='password' type="password" required></input>
      
      </div>
      </form>
    <div className="button-wrapper">
            <button className="login-button" type='submit'>Register</button>
    </div>
  </div>

  )
}

function ViewPage(){
  const [page, setPage] = useState('')
  const {recipeId} = useParams();
  useEffect(() => {
    const fetchRecipe = async () => {
      try{
        const response = await fetch('/recipes/single/' + recipeId);
        if(!response.ok){
          throw new Error("Failed to Fetch Data");
        }
        const recipe = await response.json();
        setPage(recipe)

      }
      catch(error){
        console.error("Could not fetch Recipe", error);
      }
    };
    fetchRecipe();
  },[recipeId]);

  const changeURL = (url) => {
    window.location.href = url;
  };

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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        
        <div className="view-panel">
            <div>
                <button className="view-panel-top">Save</button>
                <button className="view-panel-top">Delete</button>
            </div>
                
            <div>
                <div className="view-panel-middle-left">{page.description}</div>
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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        
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
  const [data, setData] = useState([]);
  useEffect(() => {
      const fetchRandom = async () => {
        //try{
          //const response = await fetch('/recipes/user/<username>');
          //if(!response.ok){
            //throw new Error("Failed to Fetch Data");
          //}
          const recipe = 1;//await response.json();
          setData(prevRecipes => [...prevRecipes, recipe])

        //}
        //catch(error){
          //console.error("Could not fetch Recipe", error);
        //}
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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
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
  const [data, setData] = useState([]);
  useEffect(() => {
      const fetchRandom = async () => {
        //try{
          //const response = await fetch('/recipes/favorites/<username>');
          //if(!response.ok){
            //throw new Error("Failed to Fetch Data");
          //}
          const recipe = 1;//await response.json();
          setData(prevRecipes => [...prevRecipes, recipe])

        //}
        //catch(error){
          //console.error("Could not fetch Recipe", error);
        //}
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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options">Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
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
