import openai
import json
import progressbar
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', required=True, help="Test file")
parser.add_argument('-o', '--output', default='MQ2-GPTNoContext.json', help="Output file")
parser.add_argument('-m', '--model', default="text-davinci-003", help="GPT model")
args = parser.parse_args()


trainingFile = "BioASQ-training11b/training11b.json"
testFile = args.test
output_filename = args.output
gpt_model = args.model

print("Using GPT model", gpt_model)

with open(trainingFile) as f:
    training = json.load(f)

with open('api-key.txt', 'r') as f:
    openai.api_key=f.read().strip()

training_QA = [(Q['body'],Q['type'],Q['ideal_answer'][0]) for Q in training['questions']]

prompt = """Answer this biomedical question. Write the answer as the ideal answer given to a medical practitioner.

"""

for question, qtype, ideal_answer in training_QA[-10:]:
    prompt += """Q: %s
Q type: %s
A: %s

""" % (question, qtype, ideal_answer)

# print(prompt)

with open(testFile) as f:
    test = json.load(f)

test_QA = [(Q['id'],Q['body'],Q['type']) for Q in test['questions']]

answers = []

print("Saving results in file %s" % output_filename)


with progressbar.ProgressBar(max_value=len(test_QA)) as bar:
    for i, (qid, question, qtype) in enumerate(test_QA):
        print("Question:", question)
        print("Question type:", qtype)

        # if i == 50:
        #     time.sleep(60)

        if qtype == 'yesno':
            exactanswer = 'yes'
        else:
            exactanswer = ''

        question_prompt = prompt + """Question: %s
Question type: %s
Ideal answer: 
""" % (question, qtype)
        # print("Question prompt = ", question_prompt)
        for attempts in range(2):
            try:
                response = openai.Completion.create(
                    model = gpt_model,
                    prompt = question_prompt,
                    temperature=0,
                    max_tokens=100,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=["\n"])
            except:
                print("Error during the request; waiting for 60 seconds")
                time.sleep(60)
                continue
            break

        answers.append({'id':qid,
                         'ideal_answer': response.choices[0].text,
                         'exact_answer': exactanswer})
        print("Response:", response.choices[0].text)
        print()

        result = {"questions": answers}
        with open(output_filename, 'w') as f:
            f.write(json.dumps(result, indent=2))

        time.sleep(4)

        bar.update(i)

print("Results saved in file %s" % output_filename)
