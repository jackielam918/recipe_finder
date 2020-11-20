import './App.css';

import { useState, useCallback, useEffect } from 'react';
import { Autocomplete, Alert } from '@material-ui/lab';
import { TextField, Chip, Slider, Button, CircularProgress, Backdrop } from '@material-ui/core';
import { makeStyles } from "@material-ui/core/styles";
import SearchIcon from '@material-ui/icons/Search';
import RecipesGraph from './RecipesGraph.js'

function App(props) {
  const [ingredients, setIngredients] = useState([]);
  const [ingredientSuggestions, setIngredientSuggestions] = useState([]);
  const [ingredientInputError, setIngredientInputError] = useState("");
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [discoveryScale, setDiscoveryScale] = useState(50);
  const [limitScale, setLimitScale] = useState(20);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [disabledForm, setDisabledForm] = useState(false);
  const [searchError, setSearchError] = useState(false);
  const [searchErrorText, setSearchErrorText] = useState("");

  useEffect(() => {
    fetchIngredients();
  }, []);

  const fetchIngredients = () => {
    setLoading(true);
    fetch("/api/get-ingredients", {method:'GET', mode: "no-cors", headers : { 
      'Content-Type': 'application/json;charset=UTF-8',
      'Accept': 'application/json'
    }})
    .then(res => res.json())
    .then(jsonData => {
      setIngredients(jsonData);
      setDisabledForm(false);
      setLoading(false);
    })
    .catch(err => {
      setDisabledForm(true);
      setLoading(false);
    });
  };

  const handleDiscoveryScaleChange = (event, newDiscoveryScale) => {
    setDiscoveryScale(newDiscoveryScale);
  };

  const handleLimitScaleChange = (event, newLimitScale) => {
    setLimitScale(newLimitScale);
  };

  const useStyles = makeStyles((theme) => ({
    backdrop: {
      zIndex: theme.zIndex.drawer + 1,
      color: "#fff"
    }
  }));

  const searchIngredients = useCallback(function(typedValue) {
      if (typedValue) {
        var filteredIngredients = ingredients.filter((ingredient) => ingredient.name.toLowerCase().includes(typedValue));
        setIngredientSuggestions(filteredIngredients);
      } 
    }, 
    []
  )

  const handleIngredientTyping = (event) => {
    setIngredientSuggestions([]);
    setIngredientInputError("");
    searchIngredients(event.target.value);
  }

  const searchRecipes = () => {
    setSearchError(false);
    if (selectedIngredients.length < 3) {
      setIngredientInputError("Please enter at least three ingredients.")
    } else {
      // Fetch Recipe results and initiate visualization
      console.log(selectedIngredients);
      console.log(discoveryScale);
      console.log(limitScale)
      
      const ingredientids = selectedIngredients.map(c => c.id);

      setLoading(true);
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scale: (100 - discoveryScale), ingredients:  ingredientids, limit: limitScale})
      };

      fetch('/api/get-recipes', requestOptions)
      .then(res => res.json())
      .then(json => {
        // json.map(c => c["selected_ingredients"] = ingredientids);
        setRecipes(json);
        setLoading(false);
        if (json.length == 0) {
          setSearchErrorText("No recipes matched the search criteria. Please update your criteria and try again!");
          setSearchError(true);
        }
      })
      .catch((error) => {
        setLoading(false);
        setRecipes([]);
        setSearchErrorText("An error occurred while searcing for recipes. Please try again!");
        setSearchError(true);
      });
    }
  }

  return (
    <div className="container">
      <Backdrop className={useStyles().backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
      <h1>Recipe Finder</h1>

      <div className="finder">
        <div className="search">
          { disabledForm ? 
            <Alert className="alert" variant="filled" severity="error">
              An error occurred while loading the form. Please try again by clicking the button below! <br/> <br/>
              <Button
                variant="contained" 
                color="primary" 
                size="large"
                onClick={fetchIngredients}>
                  Retry
                </Button>
            </Alert>: 
            null }

            { searchError ? 
            <Alert className="alert" variant="filled" severity="error">
              {searchErrorText}
            </Alert>: 
            null }
          <Autocomplete 
            disabled={disabledForm}
            multiple
            popupIcon={null}
            options={ingredients}
            getOptionLabel={(ingredient) => ingredient.name}
            value={selectedIngredients}
            noOptionsText="No ingredients matched."

            onChange={(event, newSelectedIngredients) => {
              setSelectedIngredients(newSelectedIngredients);
            }}
            
            renderInput={(params) => (
              <TextField 
                {...params} 
                label="Available Ingredients" 
                variant="outlined" 
                onChange={handleIngredientTyping}
                error={ingredientInputError.length > 0}
                helperText={ingredientInputError}
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

          <p className="sliderLabel">Discovery Scale:</p>
          <div className="slider">
            <p className="sliderLimitLabel">Strict</p>
            <Slider 
              disabled={disabledForm}
              value={discoveryScale} 
              min={0}
              max={100}
              onChange={handleDiscoveryScaleChange} />
            <p className="sliderLimitLabel">Experiment</p>
          </div>

          <p className="sliderLabel valueDisplay">Number of Results:</p>
          <div className="slider">
            <Slider 
              disabled={disabledForm}
              value={limitScale} 
              min={5}
              max={50}
              valueLabelDisplay="on"
              onChange={handleLimitScaleChange} />
          </div>

          <Button 
            disabled={disabledForm}
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