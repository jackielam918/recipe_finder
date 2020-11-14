import './App.css';

import { useState, useCallback, Fragment } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { TextField , Chip, Slider, Button, CircularProgress, Backdrop } from '@material-ui/core';
import { makeStyles } from "@material-ui/core/styles";
import SearchIcon from '@material-ui/icons/Search';
import debounce from 'lodash.debounce';
import RecipesGraph from './RecipesGraph.js'

//Data
import recipesList from './data/recipesList.json'

function App(props) {
  const [ingredientSuggestions, setIngredientSuggestions] = useState([]);
  const [searchingIngredients, setSearchingIngredients] = useState(false);
  const [ingredientInputError, setIngredientInputError] = useState("");
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [sliderValue, setSliderValue] = useState(50);
  const [recipes, setRecipes] = useState([]);
  const [searchingRecipes, setSearchingRecipes] = useState(false);

  const handleSliderChange = (event, newSliderValue) => {
    setSliderValue(newSliderValue);
  };

  const useStyles = makeStyles((theme) => ({
    backdrop: {
      zIndex: theme.zIndex.drawer + 1,
      color: "#fff"
    }
  }));

  const searchIngredients = useCallback(function(typedValue) {
      if (typedValue) {
        setSearchingIngredients(true);
        var filteredIngredients = props.ingredients.filter((ingredient) => ingredient.name.toLowerCase().includes(typedValue));
        setIngredientSuggestions(filteredIngredients);
        setSearchingIngredients(false);
      } 
    }, 
    []
  )

  const handleIngredientTyping = (event) => {
    setSearchingIngredients(false);
    setIngredientSuggestions([]);
    setIngredientInputError("");
    searchIngredients(event.target.value);
  }

  const searchRecipes = () => {
    if (selectedIngredients.length < 3) {
      setIngredientInputError("Please enter at least three ingredients.")
    } else {
      // Fetch Recipe results and initiate visualization
      console.log(selectedIngredients);
      console.log(sliderValue);

      setSearchingRecipes(true);
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scale: sliderValue, ingredients:  selectedIngredients.map(c => c.id), limit: 2})
      };

      fetch('/api/get-recipes', requestOptions)
      .then(res => res.json())
      .then(json => console.log(json));
      
      new Promise((resolve, reject) => {
        setTimeout(() => {
          setSearchingRecipes(false);
          resolve(recipesList);
        }, 1000);
      })
      .then((data) => {
        setRecipes(data)
      })
      .catch((error) => {
        //Handle API error
      });
    }
    
  }

  return (
    <div className="container">
      <Backdrop className={useStyles().backdrop} open={searchingRecipes}>
        <CircularProgress color="inherit" />
      </Backdrop>
      <h1>Recipe Finder</h1>

      <div className="finder">
        <div className="search">
          <Autocomplete 
            multiple
            popupIcon={null}
            options={ingredientSuggestions}
            getOptionLabel={(ingredientSuggestion) => ingredientSuggestion.name}
            open={ingredientSuggestions.length > 0}
            value={selectedIngredients}

            onChange={(event, newSelectedIngredients) => {
              setSelectedIngredients(newSelectedIngredients);
              setIngredientSuggestions([]);
            }}
            
            renderInput={(params) => (
              <TextField 
                {...params} 
                label="Available Ingredients" 
                variant="outlined" 
                onChange={handleIngredientTyping}
                error={ingredientInputError.length > 0}
                helperText={ingredientInputError}
                InputProps={{
                  ...params.InputProps,
                  endAdornment: (
                    <Fragment>
                      {searchingIngredients ? <CircularProgress size={20} /> : null}
                      {params.InputProps.endAdornment}
                    </Fragment>
                  ),
                }}
              />
            )}

            renderTags={(tagValue, getTagProps) =>
              tagValue.map((option, index) => (
                <Chip
                  label={option.name}
                  {...getTagProps({ index })}
                />
              ))
            }
          />

          <p className="sliderLabel">Discovery Scale</p>
          <div className="slider">
            <p className="sliderLimitLabel">Strict</p>
            <Slider value={sliderValue} onChange={handleSliderChange} />
            <p className="sliderLimitLabel">Experiment</p>
          </div>

          <Button 
            variant="contained" 
            color="primary" 
            size="large"
            startIcon={<SearchIcon />}
            onClick={searchRecipes} >
              Find Recipes
          </Button>
        </div>
        <RecipesGraph width={880} height={600} recipes={recipes}/>
      </div>
    </div>
  );
}

export default App;