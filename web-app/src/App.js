import './App.css';

import React from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { TextField , Chip, Slider, Button } from '@material-ui/core';

function App() {
  const [options, setOptions] = React.useState([]);
  const [sliderValue, setSliderValue] = React.useState(50);

  const handleSliderChange = (event, newSliderValue) => {
    setSliderValue(newSliderValue);
  };

  return (
    <div className="container">
      <h1>Recipe Finder</h1>

      <div className="finder">
        <div className="search">
          <Autocomplete 
            multiple
            options={top100Films}
            getOptionLabel={(option) => option.name}

            renderInput={(params) => (
              <TextField {...params} label="Available Ingredients" variant="outlined" />
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

          <Button variant="contained" color="primary" size="large">Find Recipes</Button>
        </div>
        <div class="results"></div>
      </div>
      
    </div>
  );
}

export default App;

const top100Films = [
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
