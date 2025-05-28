package com.example.englishlearningapp.Utils;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.example.englishlearningapp.Activity.ExamActivity;
import com.example.englishlearningapp.Models.Question;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class to load test data from JSON file when Firebase is not available
 */
public class TOEIC38TestJSONLoader {
    private static final String TAG = "TOEIC38TestJSONLoader";
    
    private Context context;
    
    public TOEIC38TestJSONLoader(Context context) {
        this.context = context;
    }
    
    /**
     * Start a test from the local JSON file
     * @param testType The type of test to load (listening, reading, writing, speaking)
     */
    public void startTest(String testType) {
        // Map test type to part ID
        String partId = mapTestTypeToPart(testType);
        
        try {
            // Load the test data from JSON
            JSONObject testData = loadJSONFromAsset("toeic38_test_data.json");
            if (testData == null) {
                Log.e(TAG, "Failed to load test data from JSON");
                return;
            }
            
            // Extract test info
            String testName = testData.getString("nameTest");
            String testDescription = testData.getString("description");
            
            // Extract questions for the specified part
            JSONObject parts = testData.getJSONObject("parts");
            if (!parts.has(partId)) {
                Log.e(TAG, "Part not found in test data: " + partId);
                return;
            }
            
            JSONObject part = parts.getJSONObject(partId);
            JSONArray questionsArray = part.getJSONArray("questions");
            
            // Convert JSON questions to Question objects
            List<Question> questions = parseQuestions(questionsArray, testType);
            
            // Start the exam activity
            if (!questions.isEmpty()) {
                startExamActivity(testType, testName, testDescription, questions);
            } else {
                Log.e(TAG, "No questions loaded for part: " + partId);
            }
            
        } catch (JSONException e) {
            Log.e(TAG, "Error parsing JSON test data: " + e.getMessage());
        }
    }
    
    /**
     * Map the test type to the corresponding part ID in the JSON
     */
    private String mapTestTypeToPart(String testType) {
        switch (testType) {
            case "listening":
                return "part_1";
            case "reading":
                return "part_2";
            case "writing":
                return "part_3";
            case "speaking":
                return "part_4";
            default:
                return "part_1"; // Default to listening
        }
    }
    
    /**
     * Load JSON from asset file
     */
    private JSONObject loadJSONFromAsset(String fileName) {
        String json = null;
        try {
            InputStream is = context.getAssets().open(fileName);
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            json = new String(buffer, "UTF-8");
            return new JSONObject(json);
        } catch (IOException | JSONException e) {
            Log.e(TAG, "Error loading JSON from asset: " + e.getMessage());
            return null;
        }
    }
    
    /**
     * Parse questions from JSON array
     */
    private List<Question> parseQuestions(JSONArray questionsArray, String testType) throws JSONException {
        List<Question> questions = new ArrayList<>();
        
        for (int i = 0; i < questionsArray.length(); i++) {
            JSONObject questionJson = questionsArray.getJSONObject(i);
            
            // Extract question data
            String questionText = questionJson.getString("questionText");
            JSONArray optionsArray = questionJson.getJSONArray("options");
            int correctAnswer = questionJson.getInt("correctAnswer");
            String audioUrl = questionJson.optString("audioUrl", "");
            String explanation = questionJson.optString("explanation", "");
            String word = questionJson.optString("word", "");
            String phoneticText = questionJson.optString("phoneticText", "");
            String exampleText = questionJson.optString("exampleText", "");
            
            // Convert options array to string array
            String[] options = new String[optionsArray.length()];
            for (int j = 0; j < optionsArray.length(); j++) {
                options[j] = optionsArray.getString(j);
            }
            
            // Create Question object
            Question question = new Question(questionText, options, correctAnswer, audioUrl, explanation);
            question.setQuestionType(testType);
            question.setWord(word);
            question.setPhoneticText(phoneticText);
            
            if (!exampleText.isEmpty()) {
                question.setExampleText(exampleText);
            }
            
            questions.add(question);
        }
        
        return questions;
    }
    
    /**
     * Start the ExamActivity with loaded questions
     */
    private void startExamActivity(String testType, String testName, 
                                String testDescription, List<Question> questions) {
        Intent intent = new Intent(context, ExamActivity.class);
        intent.putExtra("testType", testType);
        intent.putExtra("courseId", "toeic38");
        
        // Add test metadata
        intent.putExtra("test_name", testName);
        intent.putExtra("test_description", testDescription);
        
        // Add questions list
        ArrayList<Question> questionsList = new ArrayList<>(questions);
        intent.putExtra("questions", questionsList);
        
        // Start the activity
        context.startActivity(intent);
        
        Log.d(TAG, "Started ExamActivity with " + questions.size() + " questions from JSON loader");
    }
    
    /**
     * Usage example in an activity:
     * 
     * TOEIC38TestJSONLoader jsonLoader = new TOEIC38TestJSONLoader(this);
     * jsonLoader.startTest("listening");
     */
} 