import './App.css';

import { useState, useCallback, Fragment } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { TextField , Chip, Slider, Button, CircularProgress } from '@material-ui/core';
import debounce from 'lodash.debounce';

//Data
import ingredientsList from './data/ingredientsList.json';
import recipesList from './data/recipesList.json';

import RecipesGraph from './RecipesGraph';

function App() {
  const [ingredientSuggestions, setIngredientSuggestions] = useState([]);
  const [searchingIngredients, setSearchingIngredients] = useState(false);
  const [ingredientInputError, setIngredientInputError] = useState("");
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [sliderValue, setSliderValue] = useState(50);
  const [searchedRecipes, setRecipes] = useState([]);

  const handleSliderChange = (event, newSliderValue) => {
    setSliderValue(newSliderValue);
  };

  const searchIngredients = useCallback(debounce(function(typedValue) {
      if (typedValue) {
        setSearchingIngredients(true);

        new Promise((resolve, reject) => {
          setTimeout(() => {
            setSearchingIngredients(false);
            resolve(ingredientsList.filter((ingredient) => ingredient.name.toLowerCase().includes(typedValue)));
          }, 500);
        })
        .then((data) => {
          setIngredientSuggestions(data)
          if (data.length < 1) {
            setIngredientInputError(`'${typedValue} is not a known ingredient. Please try again`);
          }
        })
        .catch((error) => {
          setIngredientInputError("An error occurred. Please try again.")
        })
      } 
    }, 500), 
    []
  )

  const handleIngredientTyping = (event) => {
    setSearchingIngredients(false);
    setIngredientSuggestions([]);
    setIngredientInputError("");
    searchIngredients(event.target.value);
  }

  const searchRecipes = () => {
    // if (selectedIngredients.length < 3) {
    //   setIngredientInputError("Please enter at least three ingredients.")
    // } else {
      // Fetch Recipe results and initiate visualization
      console.log(selectedIngredients);
      console.log(sliderValue);
      new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(searchedRecipes);
        }, 500);
      })
      .then((data) => {
        // graph payload (with minimalist structure)
        setRecipes(data)
      })
      .catch((error) => {
        setIngredientInputError("An error occurred. Please try again.")
      })
    //}
    
  }

  return (
    <div className="container">
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
            onClick={searchRecipes} >
              Find Recipes
          </Button>
        </div>
        <RecipesGraph data={recipesList}/>
      </div>
      
    </div>
  );
}

export default App;