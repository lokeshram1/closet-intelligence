# ClosetComplement 👗

### Intelligent Visual Personal Stylist

ClosetComplement is a visual personal styling application that helps users discover clothing items that complement what they already own.

The application analyzes a photo of a retail clothing rack, identifies potential clothing items, compares them with the user's existing wardrobe, and generates personalized outfit combinations.

---

## ✨ Features

- 📸 **Visual Clothing Detection**
  - Analyzes retail/store images
  - Identifies visible clothing and accessories
  - Detects categories, colors, patterns, and style characteristics

- 👚 **Personal Wardrobe Matching**
  - Uses the user's existing wardrobe as context
  - Avoids recommending isolated purchases
  - Finds items that work with clothes the user already owns

- 🧥 **Outfit Recommendations**
  - Generates three distinct outfit combinations
  - Combines new retail items with existing wardrobe pieces
  - Considers color harmony, layering, fit, and occasion

- 🎯 **Confidence-Based Detection**
  - Assigns confidence levels to detected retail items
  - Avoids making recommendations from unclear or blurry items

- 🔄 **Structured AI Output**
  - Returns recommendations in JSON format
  - Designed for easy integration with a frontend application

---

## 🧠 How It Works

```text
        Retail Store Image
                │
                ▼
       ┌─────────────────┐
       │  Image Analysis │
       └────────┬────────┘
                │
                ▼
       Detect Clothing Items
                │
                ▼
       ┌─────────────────┐
       │ User's Wardrobe │
       │     Profile     │
       └────────┬────────┘
                │
                ▼
       Compare & Find Matches
                │
                ▼
       ┌─────────────────┐
       │ Styling Engine  │
       └────────┬────────┘
                │
                ▼
       Generate 3 Outfits
                │
                ▼
       ┌─────────────────┐
       │ JSON Response   │
       └─────────────────┘
