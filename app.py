from flask import Flask, render_template, request,jsonify
import openai
import time
from util import *
import logging
app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

user_chat={}
summary_index ={}

logging.basicConfig(filename='olduser.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/getchat', methods=["GET"]) 

def returnchat():


    data=request.get_json()

    user_input = data.get('user_input')
    name = data.get('name')
    num = data.get('number')
    print(user_input)

    ID = str(name)+str(num)

    return jsonify({'result': user_chat[ID],'name':name,'num':num})
        #return chat_response


@app.route("/vitals_form", methods=["POST"])
                         
def chatbot():
    start = time.time()

    #You can ask as many questions as you like but one at a time,use chat history to iteratively ask questions.(You can never violate this)
            
    if request.method == "POST":
        
        data=request.get_json()

        patient_data = data.get('patient_data')
        user_input = data.get('user_input')

        relevant_data,name,num=get_patient_data(patient_data)

        print("[INFO] Patient Summary: ",relevant_data)
        print("[INFO] Patient Name: ",name)
        print("[INFO] Patient Number: ",num)
        #return "nONE"

        """ count = data.get('count')

        if count is not None:

            count = int(count)

        else:
           count = 0
        """
        if name == None:

            name = "new_user"

        if num == None:
            num = generate_random_string()

        print(user_input)

    ID = str(name)+str(num)

    if  user_input =='DELETE CHAT':
        print("Del")    
        del user_chat[ID]
        del summary_index[ID]


    else:
        

        if ID not in user_chat.keys():
            print("New ID")
            user_chat[ID] = []
            summary_index[ID] = None
            user_input="Hello"
            user_chat[ID].append({"role": "user", "content": user_input})
            greet = "Hello! Welcome to EZSHIFA.\nHow can I assist you today?\n"
            user_chat[ID].append({"role": "assistant", "content": greet})
            return jsonify({'result': greet,'suggestion': None,'Questions': [],'Remedy': [],'Medicine': []})

        prompt ="""             
            You are an highly investigative AI Doctor that is an expert in medical health and is part of a hospital system called EZSHIFA.
            You know about symptoms and signs of various types of illnesses.
            You have been provided with your previous chat history with the patient.
            If a response includes a need for serious medical attention with a doctor, recommend them to book an appointment with our professional healthworkers at EZSHIFA.
            You have been provided with patient past data.
            You must go through all of the following Stages to diagnose the patient after inquiring about complaint:

            Stage 1 (Collect Patient Information):

                    *Obtain basic demographic information (age, gender, occupation, etc.).
                    *Ask about the patient's medical history, including any existing conditions, allergies, and previous surgeries.
                    
            Stage 2 (Chief Complaint):

                    *Ask the patient about the main reason for their visit.
                    *Encourage the patient to describe their symptoms in detail, including the onset, duration, and any aggravating or alleviating factors.
                    *Elicit a detailed description of the chief complaint, including any precipitating events or factors.
                    *Determine the impact of symptoms on daily activities and quality of life.
            Stage 3 (History of Present Illness):

                    *Gather a comprehensive history of the current illness.
                    *Explore the progression of symptoms, associated signs, and any self-administered treatments.
                    *Use the "OLDCARTS" acronym to explore the characteristics of symptoms: Onset, Location, Duration, Characteristics, Aggravating factors, Relieving factors, Timing, and Severity.
                    *Investigate any self-treatment or home remedies tried by the patient.
            Stage 4 (Review of Symptoms) :

                    *Systematically inquire about the patient's symptoms in various organ systems such as Constitutional Symptoms,Integumentary System,HEENT(Head,Eyes,Ears,Nose,Throat),Cardiovascular System,Respiratory System,Gastrointestinal System,Genitourinary System,Musculoskeletal System,Neurological System,Endocrine System,Hematologic System,Psychiatric System,Allergic/Immunologic System,Reproductive System (Male/Female),Lymphatic System.
                    *Identify any additional symptoms that may not be directly related to the chief complaint.
                    *Encourage patients to report any changes or abnormalities even if not directly related to the chief complaint.
                    *Inquire about recent travel history and potential exposure to infectious diseases.
            Stage 5 (Past Medical History):
                    *Explore the patient's immunization history, including influenza, pneumonia, and other relevant vaccines.
                    *Ask about the use of complementary and alternative therapies.
                    *Explore the patient's past medical conditions, surgeries, hospitalizations, and medication history.
                    *Explore the relation between patient's current medical condition and provided past medical condition/diagnosis.
            Stage 6 (Family History):
                    *Probe for specific details in family history, such as the age of onset and outcomes of diseases.
                    *Inquire about any relevant family medical history, as some conditions may have a hereditary component.
                    *Inquire about hereditary conditions and consanguinity.
            Stage 7 (Social History):
                    *Discuss sleep patterns, including duration and any difficulties falling or staying asleep.
                    *Assess occupational history, including exposure to toxins or hazardous substances.
                    *Ask about lifestyle factors such as diet, exercise, tobacco and alcohol use, and any occupational or environmental exposures.
            Stage 8 (Medication and Allergies):
                    *Inquire and assess occupational history, including exposure to toxins or hazardous substances.
                    *Document the patient's current medications, including prescription and over-the-counter drugs.
                    *Verify any known allergies.
                    *Inquire about over-the-counter medications, herbal supplements, and vitamins.
                    *Explore any adverse reactions to medications and allergies in detail.
            Stage 9 (Assessment and Differential Diagnosis):
                    *Analyze the gathered information to form an initial assessment.
                    *Develop a differential diagnosis, considering various possible causes for the symptoms.
                    *Inquire and consider the patient's preferences, values, and beliefs in formulating the assessment.            
            Stage 10 (Patient Educaion):        
                    *Encourage questions and actively involve the patient in their care plan.
                    *Acknowledge uncertainty when discussing potential diagnoses and tests.
                    *Educate the patient about their condition, treatment options, and preventive measures.
            Stage 11 (Treatment Plan):
                    *Prescribe necessary tests for confirmation of diagnosis only if necessary.
                    *Propose a treatment plan(Remedies+Medicine) based on the assessment and differential diagnosis.
                    *Discuss potential interventions, medications, lifestyle modifications, or referrals to specialists.
                    *Address any questions or concerns the patient may have.            
            You must use chat history for context.
            You must iteratively go through the above stages(Use chat history.
            You must not skip any stage or any instructions within a stage.(Use chat history)
            You must only ask a single question at a time(You can never violate this).
            You must only inquire a single piece of information from patient in a question(You can never violate this).
            """
        # to move from one stage to another.)(You can never violate this)
        messages=[{"role": "system", "content": relevant_data}]
        messages.append({"role": "system", "content": prompt})
        
        check = False
        for i in user_chat[ID]:#Check if there are pending questions, if yes return them.

            
            if i["role"]=="user" and i["content"] is None:

                i["content"]=user_input
                check = True
                continue

            if check== True:

                print("[INFO] Pending question detected.....")
                suggestions = text_suggestions(i['content'],openai)
                
                logging.info(f'result={i["content"]}, user_input={user_input}, num={num},name={name}')
                return jsonify({'result': i["content"],'suggestion': suggestions,'Questions': [],'Remedy': [],'Medicine': []})







        user_chat[ID].append({"role": "user", "content": user_input})

        for i in user_chat[ID]:
            messages.append(i)


        print("[INFO] USER CHAT: ",user_chat[ID])
        #print("[INFO] MESSAGES: ",messages)

        chat_history = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview", # You can experiment with other models as well
        messages=messages,
        seed = 2,
        temperature = 0.1
        )

        chat_response = chat_history["choices"][0]["message"]["content"]

        token_count = chat_history['usage']['total_tokens']
        output_token = len(chat_response)
        input_token = token_count - output_token

        print("[INFO] GPT RESPONSE: ",chat_response)

        #print('Total tokens used:',token_count)
        #print("Input token: ",input_token)

        #128000
        if token_count>4000:# If chat becomes too long summarize half of it to reduce tokens and keep context.
    
            print("SUMMARIZING....")
        
            if summary_index[ID] is None:
                
                summary_index[ID]=[2,len(user_chat[ID])//2]

            else:
                
                summary_index[ID][1] = len(user_chat[ID])//2
            
            SUMMARY = GenerateSummary(user_chat[ID][summary_index[ID][0]:summary_index[ID][1]],openai)

            #del user_chat[ID][summary_index[ID][0]:summary_index[ID][1]]
            user_chat[ID][summary_index[ID][0]:summary_index[ID][1]] = SUMMARY

            #summary_index[ID][0]=summary_index[ID][1]
            print(user_chat[ID])

        question = find_numbered_question_sentences(chat_response)

        
        if len(question)>2:#If bots response is more than question threshold, extract questions and them to chat.

            print("[INFO] Questions length violation detected.....")
            for i in question:
                
                if len(i)>0:

                    user_chat[ID].append({"role": "assistant", "content": i})
                    user_chat[ID].append({"role": "user", "content": None})

            suggestions = text_suggestions(question[0],openai)
            logging.info(f'result={question[0]}, user_input={user_input}, num={num},name={name}')
            return jsonify({'result': question[0],'suggestion': suggestions,'Questions': [],'Remedy': [],'Medicine': []})
    
        """if len(question)>1:

            question = "".join(question)
            suggestions = text_suggestions(question,openai)
            user_chat[ID].append({"role": "assistant", "content": question})
            logging.info(f'result={question}, user_input={user_input}, num={num},name={name}')
            return jsonify({'result': question,'suggestion': suggestions,'Questions': [],'Remedy': [],'Medicine': []})
        """
        
        user_chat[ID].append({"role": "assistant", "content": chat_response})
        suggestions = text_suggestions(chat_response,openai)
        end = time.time()
        print("[INFO] Total Response Time: ",(end-start))
        logging.info(f'result={chat_response}, user_input={user_input}, num={num},name={name}')
        return jsonify({'result': chat_response,'suggestion': suggestions,'Questions': [],'Remedy': [],'Medicine': []})
        #return chat_response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3012, debug=True)
    #app.run(debug=True)