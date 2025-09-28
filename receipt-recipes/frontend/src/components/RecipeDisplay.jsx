import React from 'react';
import './RecipeDisplay.css';

const RecipeDisplay = ({ recipes }) => {
  if (!recipes || !recipes.recipes || recipes.recipes.length === 0) {
    return null;
  }

  return (
    <div className="recipe-display-container">
      <h2 className="recipes-title">Generated Recipes</h2>
      <div className="recipes-grid">
        {recipes.recipes.map((recipe, index) => (
          <div key={index} className="recipe-card">
            <div className="recipe-header">
              <h3 className="recipe-name">{recipe.name}</h3>
              <div className="recipe-meta">
                <div className="recipe-servings">
                  <span className="servings-label">Servings:</span>
                  <span className="servings-count">{recipe.servings}</span>
                </div>
                {recipe.prep_time && (
                  <div className="recipe-time">
                    <span className="time-label">Prep:</span>
                    <span className="time-value">{recipe.prep_time}</span>
                  </div>
                )}
                {recipe.cook_time && (
                  <div className="recipe-time">
                    <span className="time-label">Cook:</span>
                    <span className="time-value">{recipe.cook_time}</span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="recipe-content">
              <div className="ingredients-section">
                <h4 className="section-title">Ingredients</h4>
                <ul className="ingredients-list">
                  {recipe.ingredients.map((ingredient, idx) => (
                    <li key={idx} className="ingredient-item">{ingredient}</li>
                  ))}
                </ul>
              </div>
              
              {recipe.instructions && recipe.instructions.length > 0 && (
                <div className="instructions-section">
                  <h4 className="section-title">Instructions</h4>
                  <ol className="instructions-list">
                    {recipe.instructions.map((step, idx) => (
                      <li key={idx} className="instruction-step">{step}</li>
                    ))}
                  </ol>
                </div>
              )}
              
              {recipe.substitutions && (
                <div className="substitutions-section">
                  <h4 className="section-title">Substitutions</h4>
                  <p className="substitutions-text">{recipe.substitutions}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecipeDisplay;