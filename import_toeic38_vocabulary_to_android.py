import json
import os

# Define the path to the Android app's assets folder
ANDROID_ASSETS_PATH = "app/src/main/assets/"

def create_android_vocabulary_data():
    """Format vocabulary data for Android app"""
    # Check if the vocabulary JSON file exists
    if not os.path.exists("toeic38_vocabulary.json"):
        print("Error: toeic38_vocabulary.json file not found!")
        print("Please run fetch_toeic38_vocabulary.py first.")
        return False
    
    try:
        # Load the TOEIC38 vocabulary data
        with open("toeic38_vocabulary.json", "r", encoding="utf-8") as f:
            toeic38_data = json.load(f)
        
        print(f"Loaded vocabulary data for {len(toeic38_data)} lessons")
        
        # Create the assets directory if it doesn't exist
        os.makedirs(ANDROID_ASSETS_PATH, exist_ok=True)
        
        # Process vocabulary data for each lesson
        all_vocabulary = []
        course_id = "toeic38"
        
        for lesson_id, lesson_data in toeic38_data.items():
            lesson_vocabulary = []
            title = lesson_data.get("title", f"Lesson {lesson_id}")
            
            # Process each vocabulary item
            for item in lesson_data.get("vocabulary", []):
                english = item.get("english", "")
                vietnamese = item.get("vietnamese", "")
                phonetic = item.get("phonetic", "")
                
                if not english or not vietnamese:
                    continue
                
                vocab_item = {
                    "english": english.strip(),
                    "vietnamese": vietnamese.strip(),
                    "phonetic": phonetic.strip(),
                    "isSelected": False
                }
                
                lesson_vocabulary.append(vocab_item)
            
            # Create lesson-specific vocabulary file
            lesson_output = {
                "lessonId": lesson_id,
                "courseId": course_id,
                "title": title,
                "vocabulary": lesson_vocabulary
            }
            
            # Save lesson vocabulary to a separate file in assets
            lesson_filename = f"{ANDROID_ASSETS_PATH}{lesson_id}_vocabulary.json"
            with open(lesson_filename, "w", encoding="utf-8") as f:
                json.dump(lesson_output, f, ensure_ascii=False, indent=2)
            
            print(f"Created vocabulary file for {title} with {len(lesson_vocabulary)} words")
            
            # Add vocabulary to the complete list
            for item in lesson_vocabulary:
                item_with_ids = item.copy()
                item_with_ids["lessonId"] = lesson_id
                item_with_ids["courseId"] = course_id
                all_vocabulary.append(item_with_ids)
        
        # Create a combined file with all vocabulary
        all_vocab_output = {
            "courseId": course_id,
            "title": "TOEIC Advanced: Essential Meeting Vocabulary",
            "vocabulary": all_vocabulary
        }
        
        combined_filename = f"{ANDROID_ASSETS_PATH}toeic38_all_vocabulary.json"
        with open(combined_filename, "w", encoding="utf-8") as f:
            json.dump(all_vocab_output, f, ensure_ascii=False, indent=2)
        
        print(f"Created combined vocabulary file with {len(all_vocabulary)} words")
        
        # Create a snippet of code to load this vocabulary in VocabularyActivity
        create_code_snippet()
        
        return True
        
    except Exception as e:
        print(f"Error creating Android vocabulary data: {e}")
        return False

def create_code_snippet():
    """Create a code snippet to load the vocabulary data in the Android app"""
    code_snippet = """
    // Method to load TOEIC38 vocabulary from assets
    private void loadToeic38VocabularyFromAssets() {
        try {
            // Determine the appropriate file to load based on lessonId
            String assetFileName;
            if (lessonId != null) {
                assetFileName = lessonId + "_vocabulary.json";
            } else {
                assetFileName = "toeic38_all_vocabulary.json";
            }
            
            Log.d(TAG, "Loading vocabulary from assets: " + assetFileName);
            
            // Load vocabulary from assets
            String jsonString = loadJSONFromAsset(assetFileName);
            if (jsonString == null) {
                // Try the combined file if specific lesson file not found
                jsonString = loadJSONFromAsset("toeic38_all_vocabulary.json");
                if (jsonString == null) {
                    Log.e(TAG, "Could not load vocabulary from assets");
                    loadSampleVocabulary();
                    return;
                }
            }
            
            // Parse JSON
            JSONObject jsonObject = new JSONObject(jsonString);
            
            // If lesson-specific file, extract vocabulary array
            if (lessonId != null && jsonObject.has("vocabulary")) {
                JSONArray vocabularyArray = jsonObject.getJSONArray("vocabulary");
                parseVocabularyArray(vocabularyArray);
            } 
            // If all vocabulary file, filter by lessonId
            else if (jsonObject.has("vocabulary")) {
                JSONArray allVocabulary = jsonObject.getJSONArray("vocabulary");
                List<VocabularyItem> filteredList = new ArrayList<>();
                
                for (int i = 0; i < allVocabulary.length(); i++) {
                    JSONObject item = allVocabulary.getJSONObject(i);
                    if (lessonId == null || lessonId.equals(item.optString("lessonId"))) {
                        VocabularyItem vocabItem = new VocabularyItem(
                            item.optString("english", ""),
                            item.optString("vietnamese", ""),
                            item.optString("phonetic", "")
                        );
                        filteredList.add(vocabItem);
                    }
                }
                
                if (!filteredList.isEmpty()) {
                    vocabularyList.clear();
                    vocabularyList.addAll(filteredList);
                    updateVocabularyUI();
                    return;
                }
            }
            
            // If we couldn't load or parse the vocabulary, load sample data
            if (vocabularyList.isEmpty()) {
                loadSampleVocabulary();
            }
        } catch (Exception e) {
            Log.e(TAG, "Error loading vocabulary from assets: " + e.getMessage());
            loadSampleVocabulary();
        }
    }
    
    private void parseVocabularyArray(JSONArray vocabularyArray) throws JSONException {
        vocabularyList.clear();
        
        for (int i = 0; i < vocabularyArray.length(); i++) {
            JSONObject item = vocabularyArray.getJSONObject(i);
            VocabularyItem vocabItem = new VocabularyItem(
                item.optString("english", ""),
                item.optString("vietnamese", ""),
                item.optString("phonetic", "")
            );
            vocabularyList.add(vocabItem);
        }
        
        updateVocabularyUI();
    }
    
    private String loadJSONFromAsset(String fileName) {
        String json = null;
        try {
            InputStream is = getAssets().open(fileName);
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            json = new String(buffer, "UTF-8");
        } catch (IOException e) {
            Log.e(TAG, "Error loading JSON from assets: " + e.getMessage());
            return null;
        }
        return json;
    }
    """
    
    # Write the code snippet to a file
    with open("load_toeic38_vocabulary_code.java", "w", encoding="utf-8") as f:
        f.write(code_snippet)
    
    print("Created Java code snippet in load_toeic38_vocabulary_code.java")
    print("You can copy this code into VocabularyActivity.java")

if __name__ == "__main__":
    print("Creating vocabulary data files for Android app...")
    if create_android_vocabulary_data():
        print("\nSuccess! Vocabulary files have been created in the Android assets folder.")
        print("You can now implement the code to load these files in your VocabularyActivity.")
    else:
        print("\nFailed to create vocabulary files. Please check the error messages above.") 