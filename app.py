from generation.generate import query_llm

if __name__ == "__main__":

    print("==> local basic rag <==")
    lastname = input("What is you name ?")
    print(f"Nice to meet you {lastname} ; How can I help you ? ")
    while True:
        question = input(f"\n{lastname} : ")

        response = query_llm(question)

        print(f"\nSystem : \n {response}")
