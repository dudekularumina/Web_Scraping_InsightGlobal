# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
import dateutil.parser as parser
import time
import re
import spacy

# Load the spaCy language model
nlp1 = spacy.load('en_core_web_sm')
def date_format(posted_on):
    import re
    try:
        # Regular expression to extract time units (weeks, days, hours, mins, secs)
        matches = re.search(r"(\d+ weeks?,? )?(\d+ days?,? )?(\d+ hours?,? )?(\d+ mins?,? )?(\d+ secs? )?ago", posted_on)
        
        # Dictionary to hold extracted time units
        time_units = {'week': 0, 'day': 0, 'hour': 0, 'min': 0, 'sec': 0}

        # Iterate through matched groups and update the time_units dictionary
        for i in range(1, len(time_units) + 1):
            if matches.group(i):
                value_unit = matches.group(i).rstrip(', ')
                if len(value_unit.split()) == 2:
                    value, unit = value_unit.split()
                    time_units[unit.rstrip('s')] = int(value)

        # Calculate the datetime object by subtracting the time units from today's date
        calculated_date = datetime.today() - timedelta(
            weeks=time_units['week'],
            days=time_units['day'],
            hours=time_units['hour'],
            minutes=time_units['min'],
            seconds=time_units['sec']
        )

        # Format the calculated date with timestamp as 'YYYY-MM-DD HH:MM:SS'
        formatted_date = calculated_date.strftime("%Y-%m-%d %H:%M:%S")
    
    except Exception as e:
        # Handle exceptions during parsing or formatting
        try:
            # Try parsing the posted_on string using dateutil.parser
            parsed_date = parser.parse(posted_on)
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            # If parsing fails, return the original posted_on string
            formatted_date = posted_on
    
    return formatted_date

def clean_posted(date):
    date=date.lower()
    date=date.replace('today','0 days ago').replace('yesterday','1 days ago').replace('just now','0 days ago')
    date=date.replace("+","")
    return date

def clean_text(text):
        '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
        and remove words containing numbers.'''
        if isinstance(text, (str, float)):
        # If the value is a string or float, apply your cleaning operations
            text = re.sub('\\[.*?\\]', '', str(text))

            #text = re.sub('\n', '', text)
            #text = re.sub('\t', '', text)
            text = re.sub('₹','',text)
            return str(text)  

def clean_phone(text):
    try:
        clean_phone_number = re.sub('[^0-9]+', '', text)
        formatted_phone_number = re.sub("(\\d)(?=(\\d{3})+(?!\\d))", r"\\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]
        return formatted_phone_number
    except:
        return text


# def extract_job_title(job_title_string): 
#     # Define delimiters used to split the string
#     delimiters = [' - ', ':', '//'] 
    
#     # Initialize the extracted title
#     extracted_title = job_title_string.strip()
    
#     # Iterate through delimiters and split the string
#     for delimiter in delimiters:
#         parts = job_title_string.split(delimiter)
#         title = parts[0].strip()  # Take the first part and remove leading/trailing spaces
        
#         # Check if the extracted title is not empty and does not contain digits
#         if title and not any(char.isdigit() for char in title):
#             extracted_title = title
#             break
    
#     return extracted_title
 


def extract_email(text):
    
    try:
        # Regular expression pattern to match email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Find all email addresses in the input text
        emails_found = re.findall(email_pattern, text)

        # Return the first email address found (if any)
        if emails_found:
            return emails_found
        else:
            return None
    except Exception as e:
        # Handle any exceptions that occur during email extraction
        print(f"An error occurred during email extraction: {e}")
        return None


def extract_mobile_number(text):
   
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                    [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    mob_num_regex1 = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|([(]?(\d{3})?[)]?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})))'''
    phone = re.findall(re.compile(mob_num_regex1), text)

    if phone:
        number = ''.join(phone[0])
        return number
    else:
        number =" "
        return number


def extract_skills(skillslist, text):
    doc = nlp1(text)
    # Extract noun chunks
    noun_chunks = [chunk for chunk in doc.noun_chunks]
    tokens = [token.text for token in nlp1 if not token.is_stop]
    skills=list(skillslist['Skill'])
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_job_title_from_text(text):
    # Use regular expression to remove digits from the text
    title_without_numbers = re.sub(r'\d+', '', text)
    
    # Apply the existing extract_job_title function to get the job title from the modified text
    return (title_without_numbers)

def format_job_description(job_description):
    # Use regular expressions to find and replace headings with bold text and two new lines
    formatted_description = re.sub(r'(\b[A-Z][\w\s]+:)', r'**\1**\n\n', job_description)
    
    # Add bullet points for lists
    formatted_description = re.sub(r'\n- ', r'\n- ', formatted_description)
    
    # Merge "Location" details into one line
    formatted_description = re.sub(r'\nLocation : (.+)', r'**Location :** \1', formatted_description)
    
    return formatted_description

def extract_job_title_from_text(text):
    return  (text)