import openai
import json
import progressbar
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', required=True, help="Test file")
parser.add_argument('-o', '--output', default='MQ1-GPTZero.json', help="Output file")
parser.add_argument('-m', '--model', default="text-davinci-003", help="GPT model")
args = parser.parse_args()


testFile = args.test
output_filename = args.output
gpt_model = args.model

print("Using GPT model", gpt_model)

with open(testFile) as f:
    test = json.load(f)

with open('api-key.txt', 'r') as f:
    openai.api_key=f.read().strip()

test_QA = [(Q['id'],Q['body'],Q['type']) for Q in test['questions']]

answers = []

print("Saving results to file %s" % output_filename)

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

#        question_prompt = prompt + "Question: " + question
        question_prompt = question+"END"

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
                    stop=["END"])
            except:
                print("Error during the request; waiting for 60 seconds")
                time.sleep(60)
                continue
            break

        answers.append({'id':qid,
                         'ideal_answer': response.choices[0].text.strip(),
                         'exact_answer': exactanswer})

        print("Response:", response.choices[0].text.strip())
        print()

        result = {"questions": answers}
        with open(output_filename, 'w') as f:
            f.write(json.dumps(result, indent=2))

        time.sleep(4) # To ensure at most 20 requests per second

        bar.update(i)

print("Results saved in file %s" % output_filename)
