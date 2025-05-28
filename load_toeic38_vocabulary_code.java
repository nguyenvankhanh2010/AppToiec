
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
    