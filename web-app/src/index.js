import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

var ingredientsList = [];
fetch("/api/get-ingredients", {method:'GET', mode: "no-cors", headers : { 
  'Content-Type': 'application/json;charset=UTF-8',
  'Accept': 'application/json'
  }})
.then(res => res.json())
.then(jsonData => {
  ingredientsList = jsonData;
  console.log(jsonData);
  ReactDOM.render(
    <React.StrictMode>
      <App ingredients={ingredientsList}/>
    </React.StrictMode>,
    document.getElementById('root')
  );
})
.catch(err => {
  console.log(err);
});




// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
