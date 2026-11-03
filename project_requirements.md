# MasteryPath AI

## 1. Problem Statement

Students often study from PDFs, notes, and other study materials, but they may not know whether they have actually understood each topic. They can move to the next topic even when they are still confused about an earlier concept. MasteryPath AI aims to solve this problem by explaining the study material, asking questions to check the student's understanding, finding the topics they are having difficulty with, and explaining those topics again. The system allows the student to practice until they understand the topic well enough before moving to the next part.


## 2. Project Objective

The main objective of MasteryPath AI is to create a learning system that helps students understand study material step by step. It will divide a PDF into three parts, explain each part according to the student's level, provide quizzes to check their understanding, identify topics they find difficult, and explain those topics again. The student will move to the next part only after reaching the required level of understanding.

## 3. Target Users

The main target users of MasteryPath AI are college and university students who study using PDFs, notes, and other educational materials. It can be especially useful for students who want to learn technical subjects at their own level and practice concepts until they understand them.

## 4. Input

The system will take a PDF containing the study material as the main input. The student will also provide the subject, their profession or area of study, and their understanding level such as Beginner, Intermediate, or Advanced. These inputs will be used to provide
explanations and questions that are suitable for the student.

## 5. Output

The system will provide a simple explanation of each part of the PDF based on the student's level. It will generate quizzes and exercises to check the student's understanding and show which topics are understood and which need more practice. For topics that are not understood, the system will provide another explanation and practice questions. It will also show the student's mastery level and progress through the PDF.

## 6. Functional Requirements

1. The system should allow the student to enter the subject, profession or area, and understanding level.

2. The system should allow the student to upload a PDF.

3. The system should process the PDF and divide it into three learning parts.

4. The system should explain each part in a simple way based on the student's understanding level.

5. The system should create quizzes or exercises based on the part that the student has learned.

6. The system should check the student's answers and identify which topics are understood and which topics need improvement.

7. The system should explain the topics that the student did not understand.

8. The system should allow the student to create or request another quiz for the topics they need to practice.

9. The system should check the student's understanding again after the additional practice.

10. The system should use a 70% mastery level as the initial rule for deciding whether the student can move to the next part.

11. If the student's mastery level is below 70%, the system should continue the learning and practice process for the weak topics.

12. If the student's mastery level is 70% or higher, the system should allow the student to move to the next part.

13. The system should track the student's progress and learning performance.

## 7. Non-Functional Requirements

1. The system should have a simple and easy-to-use interface.

2. The explanations and questions should be clear and easy for the student to understand.

3. The system should give results within a reasonable amount of time.

4. The system should provide consistent results for the same input.

5. The system should handle incorrect or incomplete student answers properly.

6. Student learning progress and data should be stored safely.

7. The system should be designed so that new features can be added in the future.

## 8. MVP Scope

1. Student enters subject, profession/area, and level.

2. Student uploads a PDF.

3. PDF is divided into 3 parts.

4. System explains Part 1.

5. System generates a quiz for Part 1.

6. Student answers the quiz.

7. System checks the answers and identifies weak topics.

8. System explains the weak topics again.

9. Student takes another quiz.

10. System calculates a mastery score.

11. If mastery >= 70%, Part 2 is unlocked.

12. If mastery < 70%, the student continues practicing the weak topics.

13. The same process is repeated for Part 2 and Part 3.

14. Student progress is displayed.

## 9. Success Metrics

1. The PDF should be divided into three meaningful learning parts.

2. The explanations should be relevant to the content of the PDF and suitable for the student's selected level.

3. The generated questions should be related to the concepts explained in the current part.

4. The system should correctly identify the topics that the student answers incorrectly.

5. The system should provide useful explanations for the topics the student finds difficult.

6. The student's mastery score should increase after additional explanation and practice.

7. The system should correctly follow the 70% rule to decide whether the student can move to the next part.

8. The system should keep track of the student's quiz scores, attempts, mastered topics, and weak topics.

## 10. Future Enhancements

1. Add Teach-Back Mode where students explain a concept in their own words and the system evaluates their understanding.

2. Add different explanation styles such as real-world examples, simple explanations, step-by-step explanations, and visual explanations.

3. Add a personalized learning dashboard to show detailed progress, strengths, and weak areas.

4. Add a system that can predict the student's mastery using previous quiz attempts, mistakes, and learning history.

5. Add support for more advanced PDF content such as images, tables, and diagrams.

6. Add more types of questions such as short answers, fill in the blanks, and scenario-based questions.

7. Add a learning history so students can return to previously studied PDFs and continue from where they stopped.

8. Add more advanced recommendations for what the student should study next.