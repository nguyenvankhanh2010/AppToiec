package com.example.englishlearningapp.Utils;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import androidx.annotation.NonNull;

import com.example.englishlearningapp.Activity.ExamActivity;
import com.example.englishlearningapp.Models.Question;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import java.util.ArrayList;
import java.util.List;

/**
 * Helper class to load TOEIC38 test data from Firebase
 */
public class TOEIC38TestAdapter {
    private static final String TAG = "TOEIC38TestAdapter";
    private static final String TEST_ID = "toeic38_test";
    
    private FirebaseFirestore db;
    private Context context;
    
    public TOEIC38TestAdapter(Context context) {
        this.context = context;
        this.db = FirebaseFirestore.getInstance();
    }
    
    /**
     * Start the ExamActivity for a specific test type (listening, reading, speaking, writing)
     * @param testType Type of test to load
     */
    public void startTest(String testType) {
        // Map test type to part number
        String partId = mapTestTypeToPart(testType);
        
        // Load test data and start activity
        loadTestData(TEST_ID, partId, testType);
    }
    
    /**
     * Map the test type to the corresponding part ID in Firebase
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
     * Load test data from Firebase and start the ExamActivity
     */
    private void loadTestData(String testId, String partId, String testType) {
        Log.d(TAG, "Loading test data for " + testType);
        
        // First get the test document
        db.collection("Tests").document(testId)
            .get()
            .addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                @Override
                public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                    if (task.isSuccessful() && task.getResult() != null && task.getResult().exists()) {
                        DocumentSnapshot testDoc = task.getResult();
                        String testName = testDoc.getString("nameTest");
                        String testDescription = testDoc.getString("description");
                        
                        Log.d(TAG, "Found test: " + testName);
                        
                        // Now load questions for the specific part
                        loadQuestionsForPart(testId, partId, testType, testName, testDescription);
                    } else {
                        Log.e(TAG, "Test document not found: " + testId);
                    }
                }
            });
    }
    
    /**
     * Load questions for a specific part of the test
     */
    private void loadQuestionsForPart(String testId, String partId, String testType, 
                                    String testName, String testDescription) {
        db.collection("Tests").document(testId)
            .collection("Parts").document(partId)
            .collection("Questions")
            .get()
            .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                @Override
                public void onComplete(@NonNull Task<QuerySnapshot> task) {
                    if (task.isSuccessful()) {
                        List<Question> questions = new ArrayList<>();
                        
                        for (QueryDocumentSnapshot document : task.getResult()) {
                            // Extract question data
                            String questionText = document.getString("questionText");
                            List<String> optionsList = (List<String>) document.get("options");
                            Long correctAnswerLong = document.getLong("correctAnswer");
                            String audioUrl = document.getString("audioUrl");
                            String explanation = document.getString("explanation");
                            String word = document.getString("word");
                            String phoneticText = document.getString("phoneticText");
                            String exampleText = document.getString("exampleText");
                            
                            if (questionText != null && optionsList != null && correctAnswerLong != null) {
                                // Convert options list to array
                                String[] options = optionsList.toArray(new String[0]);
                                int correctAnswer = correctAnswerLong.intValue();
                                
                                // Create Question object
                                Question question = new Question(questionText, options, correctAnswer, audioUrl, explanation);
                                question.setQuestionType(testType);
                                question.setWord(word);
                                question.setPhoneticText(phoneticText);
                                
                                if (exampleText != null) {
                                    question.setExampleText(exampleText);
                                }
                                
                                questions.add(question);
                                Log.d(TAG, "Added question: " + questionText);
                            }
                        }
                        
                        // Start the ExamActivity with the loaded questions
                        if (!questions.isEmpty()) {
                            startExamActivity(testType, testName, testDescription, questions);
                        } else {
                            Log.e(TAG, "No questions found for part: " + partId);
                        }
                    } else {
                        Log.e(TAG, "Error loading questions: " + task.getException());
                    }
                }
            });
    }
    
    /**
     * Start the ExamActivity with the loaded test data
     */
    private void startExamActivity(String testType, String testName, 
                                String testDescription, List<Question> questions) {
        Intent intent = new Intent(context, ExamActivity.class);
        intent.putExtra("testType", testType);
        intent.putExtra("courseId", "toeic38");
        
        // Add the test name and description
        intent.putExtra("test_name", testName);
        intent.putExtra("test_description", testDescription);
        
        // Put the questions into the intent
        ArrayList<Question> questionsList = new ArrayList<>(questions);
        intent.putExtra("questions", questionsList);
        
        // Start the activity
        context.startActivity(intent);
        
        Log.d(TAG, "Started ExamActivity with " + questions.size() + " questions");
    }
    
    /**
     * Usage example in an activity:
     * 
     * TOEIC38TestAdapter testAdapter = new TOEIC38TestAdapter(this);
     * testAdapter.startTest("listening"); // For listening test
     * testAdapter.startTest("reading");   // For reading test
     * testAdapter.startTest("writing");   // For writing test
     * testAdapter.startTest("speaking");  // For speaking test
     */
} 