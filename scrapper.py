from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models.openai import ChatOpenAI


def questions(url_list, query):
	openai = ChatOpenAI(
		api_key="",
		model_name = "gpt-4",
		max_tokens = 2048
		)
	loader_list = []
	for i in url_list:
		print('loading url: %s' % i)
		loader_list.append(WebBaseLoader(i))

	index = VectorstoreIndexCreator().from_loaders(loader_list)
	ans = index.query(query)
	print("")
	print(ans)

url_list = [
	"https://restfulapi.net/",
	"https://www.ibm.com/topics/rest-apis",
	"https://www.redhat.com/en/topics/api/what-is-a-rest-api",
	"https://www.geeksforgeeks.org/rest-api-introduction/"
]

prompt = '''
	Given the context, please provide the following:
	1. summary of what it is
	2. summary of what it does
	3. summary of how to use it
	4. Please provide 5 intresting prompts that could be used with this API
'''

questions(url_list, prompt)