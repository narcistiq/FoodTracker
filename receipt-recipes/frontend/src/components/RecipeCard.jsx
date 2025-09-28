import React from 'react'
import { ChefHat, List, BookOpen, UploadCloud, FileText } from 'lucide-react'

const COLORS = {
    DARK_BG: '#FAF9F6', 
    ACCENT_BUTTON: '#7FB069', 
    UPLOADER_BG: '#DCD3A1', 

    DARK_TEXT: '#02020B', 
    LIGHT_TEXT: '#F0F0F0', 
    CARD_BG: '#FFFFFF', 
    ACCENT_HOVER: '#6C985A',
};
const SAMPLE_RECIPES_JSON = JSON.stringify([
    {
        Name: "Classic Pancakes",
        Servings: "A simple, fluffy pancake recipe perfect for a Sunday breakfast.",
        Ingredients: [
            "1.5 cups All-Purpose Flour",
            "3.5 tsp Baking Powder",
            "1 tsp Salt",
            "1 tbsp White Sugar",
            "1.25 cups Milk",
            "1 Egg",
            "3 tbsp Melted Butter"
        ],
        'Necessary Substitutions': [
            "egg",
            "flour",
            "banana"
        ]
    }
])
export default function RecipeCard() {
    return (
        <div>
        </div>
    )
}