import './App.css';

import React, { useCallback } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { TextField , Chip, Slider, Button, CircularProgress } from '@material-ui/core';
import debounce from 'lodash.debounce';

function App() {
  const [ingredientSuggestions, setIngredientSuggestions] = React.useState([]);
  const [searchingIngredients, setSearchingIngredients] = React.useState(false);
  const [ingredientInputError, setIngredientInputError] = React.useState("");
  const [selectedIngredients, setSelectedIngredients] = React.useState([]);
  const [sliderValue, setSliderValue] = React.useState(50);

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
    if (selectedIngredients.length < 3) {
      setIngredientInputError("Please enter at least three ingredients.")
    } else {
      // Fetch Recipe results and initiate visualization
      console.log(selectedIngredients);
      console.log(sliderValue);
    }
    
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
                    <React.Fragment>
                      {searchingIngredients ? <CircularProgress size={20} /> : null}
                      {params.InputProps.endAdornment}
                    </React.Fragment>
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
            onClick={searchRecipes}
          >
              Find Recipes
          </Button>
        </div>
        <div class="results"></div>
      </div>
      
    </div>
  );
}

export default App;

const ingredientsList = [
  { name: "Salt", id: 1 },
  { name: "Pepper", id: 2 },
  { name: "Olive oil", id: 3 },
  { name: "Flour", id: 4 },
  { name: "Ground beef", id: 5 },
  { name: "Basil", id: 6 },
  { name: "Dill", id: 7 },
  { name: "Avocado", id: 8 },
  { name: "Cashew", id: 9 },
  { name: "Peanut", id: 10 },
  { name: "Tomato", id: 11 },
  { name: "Cucumber", id: 12 },
  { name: "Cilantro", id: 13 },
  { name: "Chicken breast", id: 14 },
  { name: "Potato", id: 15 },
  { name: "Broccoli", id: 16 },
  { name: "Ginger", id: 17 },
  { name: "Soy Sauce", id: 18 },
  { name: "Lettuce", id: 19 },
  { name: "Butter", id: 20 },
]
