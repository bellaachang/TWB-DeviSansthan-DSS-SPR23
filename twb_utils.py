# util.py
# this python file contains the functions referenced in the instruction manual that create the question bank dataset for text and image based questions  

import pandas as pd
import regex as re
import random
import numpy as np


def create_table(question_type, filepath, expression): 
    """
    Create a table of questions from ChatGPT word problems with the specified question type.

    Args:
    question_type (String): the arithmetic operation that the question uses (addition, subtraction, divison, etc.) -- This isn't case-sensitive
    filepath (String): the filepath to the csv file that contains the Chat GPT generated output (example: "/work/CHATGPT/area-qs.csv")
    expression (function): the function that creates a mathematical expression from the word problem

    Returns (dataframe): 
        the final question table with the columns: "Question," "Category," "Expression," "Solution," and "Answer Choices"  
    """

    questions_table = pd.read_csv(filepath) #loads in the data 
    questions_table = questions_table.rename(columns = {questions_table.columns[0]: 'Question'})

    question_type = question_type.lower()
    
    questions_table["Expression"] = questions_table["Question"].str.findall('\d+') #finds all numbers in the question 
    questions_table["Expression"] = questions_table["Expression"].apply(expression) 

    questions_table["Solution"] = questions_table["Expression"].apply(eval).astype(int)
    questions_table["Category"] = [question_type] * len(questions_table)

    answer_choices_list = [] #list of possible answer choices 
    for index, row in questions_table.iterrows():
        solution = row["Solution"]
        possible_answer_choices = np.linspace(solution - 10, solution + 10, 21) #create an array of numbers centered around the solution
        possible_answer_choices = possible_answer_choices.astype(int)
        answer_choices = random.sample(sorted(possible_answer_choices[possible_answer_choices != solution]), 3) #randomly choose 3 of those numbers from the possible answer choices
        answer_choices.append(solution) #append the solution to the possible answer choices
        random.shuffle(answer_choices) #shuffle the answer choices 
        answer_choices_list.append(answer_choices) #append this answer choices to the overall list 

    questions_table["Answer Choices"] = answer_choices_list

    return questions_table



def image_based_qs(phenome_df):

    """
    Create a table of questions from ChatGPT word problems with the specified question type.

    Args:
    phenome_df (Dataframe): Dataframe of the phenome list output that we downloaded from Chat GPT 

    Returns (dataframe): 
        the final question table with the columns: 'Generated Question', 'Answer Choices', 
                                 'Answer', 'Phoneme', 'Image' 
    """

    generated_english_questions = pd.DataFrame(columns=['Generated Question', 'Answer Choices', 
                                 'Answer', 'Phoneme', 'Image'])
    generated_english_questions

    q_index = 0
    for index, row in phoneme_list.iterrows():
        phoneme = row['English Phoneme']
        for word_index in range(len(row['Word List'])):
            generated_english_questions.loc[q_index, "Generated Question"] = "Select the correct " + phoneme + " sound word in the picture"
            generated_english_questions.loc[q_index, "Answer"] = row['Word List'][word_index]
            answer_choices = random.sample(row['Word List'][:word_index] + row['Word List'][word_index+1:], min(3, len(row['Word List']))) + [row['Word List'][word_index]]
            random.shuffle(answer_choices) 
            generated_english_questions.loc[q_index, "Answer Choices"] = answer_choices
            generated_english_questions.loc[q_index, "Phoneme"] = phoneme
            q_index += 1
    
    return dataframe

#function expressions

def perimeter_expr(row):
    if row["Shape"] == 'square':
        return row["Numbers"][0] + "* 4"
    elif row["Shape"] == 'rectangle':
        return "2*" + row["Numbers"][0] + "+ 2 *" + row["Numbers"][1]
    else:
        return 0 

def area_expr(x):
    return x[0] + "**2"

def multi_expr(x):
    return x[0] + "*" + x[1]

def sub_expr(x):
    return x[0] + "-" + x[1]

def add_expr(x):
    return x[0] + "+" + x[1]

def div_expr(x):
    return x[0] + "\\" + x[1]