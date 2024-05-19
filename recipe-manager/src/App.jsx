import { useEffect, useState } from 'react'
import {Route, Routes, useNavigate } from 'react-router-dom';
import { BrowserRouter, Link, useSearchParams} from "react-router-dom";
import './App.css'
import ReactDOM from 'react-dom/client'
import React from 'react'
import './index.css'

async function getUsername(){

try{
  const token = localStorage.getItem('recipe-manager-token')
  //console.log(token + "kill")
  let res = await fetch('http://localhost:5000/user/me', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'content-type': 'application/json',
        'Authorization': `Bearer ${token}` 
      }
    })
    
    const asyncData = await res.json()
    //console.log(asyncData)
    return (asyncData)
  }catch(error){
    console.error('Failed to Find Username')
    return "Username not found"
  }
}

function logout(){
  localStorage.removeItem('recipe-manager-token')
  changeURL('/')
}


function changeURL(pathName){
  window.location.pathname = pathName
}



function App() {

  return (
    
      <Routes>
        <Route path='/view' element={<ViewPage />}/>
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

  const nav = useNavigate()
  const [data, setData] = useState([]);
  useEffect(() => {
      const fetchRandom = async () => {
        try{
          const response = await fetch('http://localhost:5000/recipes/trending');
          if(!response.ok){
            throw new Error("Failed to Fetch Data");
          }
          //console.log(response)
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
        <button className="account-options" onClick={() => changeURL('/loginpage')}>Sign In</button>
        <button className="account-options" onClick={() => logout()}>Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        <div className="browse-panel">
          {data.map((recipe, index) => (
            <button onClick={() => nav({pathname: '/view', search: '?recipe=' + recipe.recipe_id
          })} className='random-shown' key={index}>
              {recipe.title}
              </button>
          ))}
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
    fetch('http://localhost:5000/login', {
      method:'POST',
      headers:{'content-type':'application/json'},
      body:JSON.stringify({username, password})
      }
    )
    .then(response => response.json())
    .then(data => {
      
      localStorage.setItem('recipe-manager-token', data.access_token)
      //console.log(localStorage.getItem('recipe-manager-token'))
      changeURL('/')
    })
    .catch((error) => {
      console.error('Error when Logging in',error);
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
      <button className="login-button" type='submit'>Login</button>
      </form>
      
  </div>
</body>
  )
}

function RegUser(){

  function createUser(event){
    event.preventDefault();
    const username = event.target.username.value
    const password = event.target.password.value
    fetch('http://localhost:5000/register', {
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
      <button className="login-button" type='submit'>Register</button>
      </form>

            
  </div>

  )
}

function ViewPage(){
  const [page, setPage] = useState('')
  let [recipeId] = useSearchParams();
  //const token = localStorage.getItem('recipe-manager-token')
  //console.log(recipeId.get('recipe') + 'recipe ID')
  //console.log("Hello World!")
  useEffect(() => {
    const fetchRecipe = async () => {
      try{
        const response = await fetch('http://localhost:5000/recipes/single/' + recipeId.get('recipe'));
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

  //console.log(page)

  const handleInput = (event) => {
    const { id, innerText } = event.target.innerText;
    setPage((prevPage) => ({
      ...prevPage,
      [id]: innerText
    }));
  };
  //console.log(page)
  function saveChanges(event){
    
    event.preventDefault();
    //console.log("ZONE A")
    const token = localStorage.getItem('recipe-manager-token');
    //console.log(token + " ZONE B")
    getUsername().then((response) => {
      console.log(response)
      return (fetch('http://localhost:5000/recipes/user/' + response.username, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ 
        "title": document.getElementById('title').innerText,
        "ingredients": document.getElementById('ing').innerText,
        "directions": [],
        "description": document.getElementById('desc').innerText,
        "keywords": [],
        "recipe_id": recipeId.get('recipe')
      })
    }));
    

  });
  }
  async function delRecipe(event){
    event.preventDefault();
    //console.log("ZONE A")
    const response = await getUsername()
    //const username = response.username
    const token = localStorage.getItem('recipe-manager-token');
    //console.log(token + " ZONE B")
  
      //console.log(response)
      const delResonse = await fetch('http://localhost:5000/recipes/user/' + response.username +"?recipe_id="+ recipeId.get('recipe'), {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await delResonse.json()
    //console.log(data)
    changeURL('/myrecipes')
  }

  async function favRecipe(event){
    event.preventDefault()
    const RECIPE_ID = 'recipe_id'; 
    const response = await getUsername()
    const token = localStorage.getItem('recipe-manager-token');
    const url = new URL('http://localhost:5000/recipes/favorites/');
    const favResponse = await fetch(url + response.username +'?recipe_id='+ recipeId.get('recipe'), {
      method: 'PUT',
      headers:{
        'content-type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        [RECIPE_ID]: recipeId.get('recipe')
      })
    })
    const data = await favResponse.json()
    console.log('Favorite added')
    
  }
  
  //let oldTitle = toString(page.title) 
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
        <button className="account-options" onClick={() => logout()}>Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        
        <form className="view-panel" suppressContentEditableWarning>
            <div>
                <button  className="view-panel-top" type='submit' onClick={saveChanges}>Save</button>
                <button className='view-panel-top' type='submit' onClick={delRecipe}>Delete</button>
                <button className='view-panel-top' onClick={favRecipe}>Favorite</button>
            </div>
                
            <div>
                <div onInput={handleInput} contentEditable='true' id='title' suppressContentEditableWarning className="view-panel-middle-left">{page.title}</div>
                <div  onInput={handleInput} contentEditable='true' id='ing' suppressContentEditableWarning className="view-panel-middle-right">{page.ingredients}</div>
            </div>
            
            <div>
            <div  onInput={handleInput} contentEditable='true' id='desc' suppressContentEditableWarning className="view-panel-bottom">{page.description}</div>    
            </div>
            
           </form>
        </div>
</body>
  )
}

function SearchPage(){
  const nav = useNavigate()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  async function search(event){
    event.preventDefault()
    const url = new URL('http://localhost:5000/recipes/search');
    url.searchParams.append('query', query);
    const token = localStorage.getItem('recipe-manager-token');
    //let searchString = document.getElementById('searchParams').innerText
    const searchResponse = await (fetch(url, {
      method: 'GET',
      headers:{'content-type':'application/json',
        'Authorization': `Bearer ${token}`,
        'query': query
      }
      
    }))
    console.log(searchResponse)
    const data = await searchResponse.json()
    setResults(data)
    //console.log(data)

  }
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
        <button className="account-options" onClick={() => logout()}>Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        
        <form onSubmit={search}>

        <input type="text" onChange={(e) => setQuery(e.target.value)} id='searchParams'></input>
        <button className='filter-button'type='submit' >Search</button>
        </form>
        
        <div className="browse-panel">
        {results.map((results, index) => (
            <button onClick={() => nav({pathname: '/view', search: '?recipe=' + results.recipe_id
          })} className='random-shown' key={index}>
              {results.title}
              </button>
          ))}
        </div>
    </div>
    
</body>
  );
}

function MyRecipes(){
  //const [data, setData] = useState([]);
  const [own, setOwn] = useState([]);
  const token = localStorage.getItem('recipe-manager-token')
  const nav = useNavigate()
  useEffect(() => {
    const fetchRandom = async () => {
      const userResponse = await getUsername();
      //console.log(userResponse.username)
      const username = userResponse.username;
      //console.log(username)
      
      try{
        const response = await fetch('http://localhost:5000/recipes/user/' + username, 
        {method:'GET', 
        headers: {
          Accept: 'application/json',
          'content-type': 'application/json',
          'Authorization': `Bearer ${token}` 
        }});
        //console.log(response)
        if(!response.ok){
          throw new Error("Failed to Fetch Data");
        }
        //console.log(response)
        const idList = await response.json();
        
        
        //console.log(idList)
        if (Array.isArray(idList)) {
          setOwn(idList); 
        } else {
          console.error('idList is not an array:', idList);
        }
        
  
        //console.log(own)

      }
      catch(error){
        console.error("Could not fetch Recipe", error);
      }
    };
    //for(let i = 0; i < 9; i++){
      fetchRandom();
   // }
  },[]);

    function createNew(event){
      
      event.preventDefault();
      const token = localStorage.getItem('recipe-manager-token')
      getUsername().then((response) => {
        return (fetch('http://localhost:5000/recipes/user/' + response.username, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ 
          "title": "",
          "ingredients": [],
          "directions": "",
          "description": "",
          "keywords": []
        })
      }))

  
    }).then((response) => {
      //console.log(response + " create new recipe response")
      return response.json()
    }
    )
    .then(data => {
      //console.log(data.recipe_id + "recipe id")
      //const queryParams = new URLSearchParams(data).toString()
      //changeURL('/view', queryParams)
      
      nav({
        pathname: '/view',
        search: '?recipe=' + data.recipe_id
      })
    })
    .catch((error) => {
      console.error('Error end:', error);
    });
      
  }


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
        <button className="account-options" onClick={() => logout()}>Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        <div className="browse-panel">
        <div>
          <div>
            <button className ="view-panel-top" onClick={createNew}>Create New</button>
        </div>
        {own.map((recipe, index) => (
          <button className='random-shown' key={index} onClick={() => nav({pathname: '/view', search: '?recipe=' + recipe.recipe_id
            })}>{recipe.title}</button>
        ))}
           </div>
        </div>
    </div>
    
</body>
  );
}

function MyFavorites(){
  const nav = useNavigate()
  const [own, setOwn] = useState([]);
  const token = localStorage.getItem('recipe-manager-token')
  useEffect(() => {
    const fetchRandom = async () => {
      const userResponse = await getUsername();
      //console.log(userResponse.username)
      const username = userResponse.username;
      //console.log(username)
      
      try{
        const response = await fetch('http://localhost:5000/recipes/favorites/' + username, 
        {method:'GET', 
        headers: {
          Accept: 'application/json',
          'content-type': 'application/json',
          'Authorization': `Bearer ${token}` 
        }});
        //console.log(response)
        if(!response.ok){
          throw new Error("Failed to Fetch Data");
        }
        //console.log(response)
        const idList = await response.json();
        
        
        //console.log(idList)
        if (Array.isArray(idList)) {
          setOwn(idList); 
        } else {
          console.error('idList is not an array:', idList);
        }
        
  
        //console.log(own)

      }
      catch(error){
        console.error("Could not fetch Recipe", error);
      }
    };
    //for(let i = 0; i < 9; i++){
      fetchRandom();
   // }
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
        <button className="account-options" onClick={() => logout()}>Sign Out</button>
        <button className="account-options" onClick={() => changeURL('/createuser')}>Register</button>
        <div className="browse-panel">
        {own.map((recipe, index) => (
          <button className='random-shown' key={index} onClick={() => nav({pathname: '/view', search: '?recipe=' + recipe.recipe_id
            })}>{recipe.title}</button>
        ))}
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
