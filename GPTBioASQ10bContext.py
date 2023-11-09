import openai
import json
import progressbar
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', required=True, help="Test file")
parser.add_argument('-c', '--context', required=True, help="Context file which was the output of BioASQ model")
parser.add_argument('-o', '--output', default='MQ1-GPTBioASQ10bContext.json', help="Output file")
parser.add_argument('-m', '--model', default="text-davinci-003", help="GPT model")
args = parser.parse_args()

testFile = args.test
contextFile = args.context
output_filename = args.output
gpt_model = args.model

print("Using GPT model", gpt_model)

with open('api-key.txt', 'r') as f:
    openai.api_key=f.read().strip()


prompt = """Answer the biomedical question as truthfully as possible using the provided text. Write the answer as the ideal answer given to a medical practitioner.

Text:

"""

with open(testFile) as f:
    test = json.load(f)

with open(contextFile) as f:
    aux = json.load(f) 

contexts_dict = dict()
for q in aux['questions']:
    contexts_dict[q['id']] = q['ideal_answer']

answers = []

print("Saving results to file %s" % output_filename)


with progressbar.ProgressBar(max_value=len(test['questions'])) as bar:
    for i, question in enumerate(test['questions']):
        #if i >= 2:
        #    break

        print("Question:", question['body'])
        print("Question type:", question['type'])

        context = contexts_dict[question['id']] + "\n\n"

        if question['type'] == 'yesno':
            exactanswer = 'yes'
        else:
            exactanswer = ''

        question_prompt = prompt + context + """Q: %s
A: 
""" % (question['body'])
        # print("Question prompt = ", question_prompt)
        # print("Ideal answer:", question['ideal_answer'])
        for attempts in range(2):
            try:
                response = openai.Completion.create(
                    model = gpt_model,
                    prompt = question_prompt,
                    temperature=0,
                    max_tokens=200,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=["\n"])
            except:
                print("Error during the request; waiting for 60 seconds")
                time.sleep(60)
                continue
            break

        answers.append({'id':question['id'],
                         'ideal_answer': response.choices[0].text,
                         'exact_answer': exactanswer})

        print("Generated response:", response.choices[0].text)
        print()

        result = {"questions": answers}
        with open(output_filename, 'w') as f:
            f.write(json.dumps(result, indent=2))

        time.sleep(4)

        bar.update(i)

print("Results saved in file %s" % output_filename)
